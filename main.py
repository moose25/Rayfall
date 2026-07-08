from fastapi import FastAPI, Query, HTTPException, Request, Header, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import subprocess
import sqlite3
import gzip
import json
import os
import secrets
import threading
from datetime import datetime, timezone

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get("RAYFALL_DB", os.path.join(BASE_DIR, "data", "rayfall.db"))

# Limits for shared snapshots
MAX_QSOS = 50000
MAX_COMPRESSED_BYTES = 8 * 1024 * 1024

# Preview-image rendering (runs Chromium in a separate venv, out of process)
PREVIEW_DIR = os.path.join(BASE_DIR, "data", "previews")
RENDER_PYTHON = os.path.join(BASE_DIR, ".render-venv", "bin", "python")
RENDER_SCRIPT = os.path.join(BASE_DIR, "render_preview.py")
RENDER_LOCAL_BASE = os.environ.get("RAYFALL_LOCAL_BASE", "http://127.0.0.1:8000")
FALLBACK_IMAGE = os.path.join(BASE_DIR, "static", "rayfall.png")
_render_lock = threading.Lock()

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Use Jinja2 templates from templates/
templates = Jinja2Templates(directory="templates")


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    try:
        con.execute("PRAGMA journal_mode=WAL")
        con.execute(
            """CREATE TABLE IF NOT EXISTS shares (
                id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                payload BLOB NOT NULL,
                delete_token TEXT NOT NULL,
                views INTEGER NOT NULL DEFAULT 0
            )"""
        )
        con.execute(
            """CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts TEXT NOT NULL,
                type TEXT NOT NULL,
                share_id TEXT
            )"""
        )
        con.commit()
    finally:
        con.close()


def get_db():
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA busy_timeout=5000")
    con.row_factory = sqlite3.Row
    return con


def log_event(con, event_type, share_id=None):
    con.execute(
        "INSERT INTO events (ts, type, share_id) VALUES (?, ?, ?)",
        (datetime.now(timezone.utc).isoformat(), event_type, share_id),
    )


def base_url(request: Request) -> str:
    override = os.environ.get("RAYFALL_BASE_URL")
    if override:
        return override.rstrip("/")
    host = request.headers.get("host") or request.url.netloc
    proto = request.headers.get("x-forwarded-proto") or request.url.scheme
    return f"{proto}://{host}"


def _load_share(share_id: str):
    con = get_db()
    try:
        row = con.execute("SELECT payload FROM shares WHERE id = ?", (share_id,)).fetchone()
    finally:
        con.close()
    if row is None:
        return None
    return json.loads(gzip.decompress(row["payload"]).decode("utf-8"))


def preview_path(share_id: str) -> str:
    return os.path.join(PREVIEW_DIR, f"{share_id}.png")


def ensure_preview(share_id: str) -> bool:
    """Return True if a preview PNG exists (rendering it if needed). Cached on disk."""
    out = preview_path(share_id)
    if os.path.exists(out) and os.path.getsize(out) > 0:
        return True
    if not os.path.exists(RENDER_PYTHON):
        return False
    os.makedirs(PREVIEW_DIR, exist_ok=True)
    with _render_lock:
        if os.path.exists(out) and os.path.getsize(out) > 0:
            return True
        try:
            subprocess.run(
                [RENDER_PYTHON, RENDER_SCRIPT, share_id, out, RENDER_LOCAL_BASE],
                timeout=90, check=True, capture_output=True,
            )
        except Exception:
            return False
    return os.path.exists(out) and os.path.getsize(out) > 0


init_db()


@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    root = base_url(request)
    og = {
        "title": "Rayfall — Ham Radio QSO Map Viewer",
        "description": "Plot your amateur radio contacts on an interactive map. Load from QRZ or an ADIF file, then share or embed your map.",
        "image": f"{root}/static/rayfall.png",
        "url": f"{root}/",
    }
    return templates.TemplateResponse(request, "index.html", {"mode": "edit", "share_id": "", "og": og})


class SharePayload(BaseModel):
    v: int = 1
    qsos: list
    settings: dict = {}
    view: dict = {}
    meta: dict = {}


@app.post("/api/share")
def create_share(payload: SharePayload, request: Request, background_tasks: BackgroundTasks):
    if not payload.qsos:
        raise HTTPException(status_code=400, detail="No QSOs to share")
    if len(payload.qsos) > MAX_QSOS:
        raise HTTPException(status_code=413, detail=f"Too many QSOs (limit {MAX_QSOS})")

    raw = json.dumps(payload.model_dump(), separators=(",", ":")).encode("utf-8")
    blob = gzip.compress(raw)
    if len(blob) > MAX_COMPRESSED_BYTES:
        raise HTTPException(status_code=413, detail="Shared map is too large")

    delete_token = secrets.token_urlsafe(16)
    created_at = datetime.now(timezone.utc).isoformat()

    con = get_db()
    try:
        share_id = None
        for _ in range(5):
            candidate = secrets.token_urlsafe(7)
            try:
                con.execute(
                    "INSERT INTO shares (id, created_at, payload, delete_token) VALUES (?, ?, ?, ?)",
                    (candidate, created_at, blob, delete_token),
                )
                share_id = candidate
                break
            except sqlite3.IntegrityError:
                continue
        if share_id is None:
            raise HTTPException(status_code=500, detail="Could not allocate share id")
        log_event(con, "create", share_id)
        con.commit()
    finally:
        con.close()

    # Pre-warm the preview image so links unfurl immediately when shared
    background_tasks.add_task(ensure_preview, share_id)

    root = base_url(request)
    return {
        "id": share_id,
        "url": f"{root}/m/{share_id}",
        "embed_url": f"{root}/embed/{share_id}",
        "preview_url": f"{root}/preview/{share_id}.png",
        "delete_token": delete_token,
    }


@app.get("/api/share/{share_id}")
def get_share(share_id: str):
    con = get_db()
    try:
        row = con.execute("SELECT payload FROM shares WHERE id = ?", (share_id,)).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Share not found")
        con.execute("UPDATE shares SET views = views + 1 WHERE id = ?", (share_id,))
        log_event(con, "view", share_id)
        con.commit()
    finally:
        con.close()
    return json.loads(gzip.decompress(row["payload"]).decode("utf-8"))


@app.delete("/api/share/{share_id}")
def delete_share(share_id: str, token: str = Query(default=None), x_delete_token: str = Header(default=None)):
    supplied = token or x_delete_token
    if not supplied:
        raise HTTPException(status_code=400, detail="Missing delete token")
    con = get_db()
    try:
        row = con.execute("SELECT delete_token FROM shares WHERE id = ?", (share_id,)).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Share not found")
        if not secrets.compare_digest(row["delete_token"], supplied):
            raise HTTPException(status_code=403, detail="Invalid delete token")
        con.execute("DELETE FROM shares WHERE id = ?", (share_id,))
        con.commit()
    finally:
        con.close()
    return {"deleted": True}


def _share_exists(share_id: str) -> bool:
    con = get_db()
    try:
        return con.execute("SELECT 1 FROM shares WHERE id = ?", (share_id,)).fetchone() is not None
    finally:
        con.close()


@app.get("/m/{share_id}", response_class=HTMLResponse)
async def view_share(request: Request, share_id: str):
    data = _load_share(share_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Share not found")
    count = len(data.get("qsos", []))
    root = base_url(request)
    og = {
        "title": f"{count:,} QSOs mapped on Rayfall" if count else "A QSO map on Rayfall",
        "description": "An interactive amateur radio contact map. Explore the contacts, or build and share your own at rayfall.me.",
        "image": f"{root}/preview/{share_id}.png",
        "url": f"{root}/m/{share_id}",
    }
    return templates.TemplateResponse(request, "index.html", {"mode": "view", "share_id": share_id, "og": og})


@app.get("/embed/{share_id}", response_class=HTMLResponse)
async def embed_share(request: Request, share_id: str):
    if not _share_exists(share_id):
        raise HTTPException(status_code=404, detail="Share not found")
    resp = templates.TemplateResponse(request, "index.html", {"mode": "embed", "share_id": share_id})
    resp.headers["Content-Security-Policy"] = "frame-ancestors *"
    return resp


@app.get("/preview/{share_id}.png")
def preview_image(share_id: str):
    headers = {"Cache-Control": "public, max-age=86400"}
    if _share_exists(share_id) and ensure_preview(share_id):
        return FileResponse(preview_path(share_id), media_type="image/png", headers=headers)
    return FileResponse(FALLBACK_IMAGE, media_type="image/png", headers=headers)


def dms_to_decimal(coord_str):
    """
    Converts a coordinate string like 'N039 02.244' or 'W077 24.538' to decimal degrees.
    """
    try:
        direction = coord_str[0]
        degrees_minutes = coord_str[1:].strip()
        degrees, minutes = degrees_minutes.split(" ")
        degrees = float(degrees)
        minutes = float(minutes)
        decimal = degrees + (minutes / 60)

        if direction in ["S", "W"]:
            decimal *= -1
        return round(decimal, 6)
    except Exception:
        return None  # If malformed or missing


def parse_adif_block(adif_text: str):
    entries = adif_text.split("<eor>")
    parsed_qsos = []

    for entry in entries:
        qso = {}
        fields = entry.strip().split("<")
        for field in fields:
            if ">" in field:
                key_value = field.split(">")
                if len(key_value) == 2:
                    key_raw, value = key_value
                    key_parts = key_raw.split(":")
                    key = key_parts[0].lower()
                    qso[key] = value.strip()
        if qso:
            filtered_qso = {
                "call": qso.get("call"),
                "band": qso.get("band"),
                "mode": qso.get("mode"),
                "qso_date": qso.get("qso_date"),
                "time_on": qso.get("time_on"),
                "gridsquare": qso.get("gridsquare"),
                "country": qso.get("country"),
                "state": qso.get("state"),
                "distance": qso.get("distance"),
                "lat": dms_to_decimal(qso.get("lat", "")),
                "lon": dms_to_decimal(qso.get("lon", "")),
                "my_lat": dms_to_decimal(qso.get("my_lat", "")),
                "my_lon": dms_to_decimal(qso.get("my_lon", "")),
                "my_gridsquare": qso.get("my_gridsquare"),
            }
            parsed_qsos.append(filtered_qso)

    return parsed_qsos


@app.get("/api/logs")
def get_logs(
    start: str = Query(...),
    end: str = Query(...),
    x_api_key: str = Header(default=None)
):
    if not x_api_key:
        raise HTTPException(status_code=400, detail="Missing x-api-key header")

    start_datetime = f"{start}T00:00:00"
    end_datetime = f"{end}T23:59:59"

    command = [
        "curl", "-X", "POST", "https://logbook.qrz.com/api",
        "-d", f"KEY={x_api_key}",
        "-d", "ACTION=FETCH",
        "-d", f"OPTION=BETWEEN:{start}+{end}"
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=False, check=True)
        output = result.stdout.decode("latin-1").strip()

        if "RESULT=FAIL" in output or "COUNT=0" in output:
            return {
                "message": "No QSOs found or QRZ rejected request",
                "response": output
            }

        # Clean escaped characters
        output = output.replace("&gt;", ">").replace("&lt;", "<").replace("&amp;", "&")

        # Parse only the fields we want
        parsed_qsos = parse_adif_block(output)

        return {
            "count": len(parsed_qsos),
            "qsos": parsed_qsos
        }

    except subprocess.CalledProcessError as e:
        return {
            "error": "Curl failed",
            "detail": e.stderr
        }
