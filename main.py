from fastapi import FastAPI, Query, HTTPException, Request, Header
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import subprocess

app = FastAPI()

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Use Jinja2 templates from templates/
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

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
                "my_lon": dms_to_decimal(qso.get("my_lon", ""))
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
