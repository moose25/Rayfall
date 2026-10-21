<p align="center">
  <img src="static/rayfall.png" alt="RayfallLogo" height="100">
</p>

# Rayfall: QRZ Logbook Map Viewer

Rayfall is a dynamic ham radio mapping interface that pulls your logbook data from QRZ and plots your QSOs on an interactive Leaflet map. You can explore contacts by date range, filter by band and mode, and visually analyze your contacts across different locations and timeframes.

> **Built by N2CLW**

## Available at [rayfall.me](https://rayfall.me)
---

## Features

* **Interactive Leaflet Map**
* **Multiple import methods:**
  * QRZ API integration (supports multiple logbooks)
  * ADI/ADIF file import (no API key required!)
* **Date range selection**
* **Color-coded pins by band or by QTH**
* **Multi-QTH support:** logs that span multiple locations (travel, POTA, Field Day) get a separate marker per QTH, plus a QTH filter row and per-QSO "From QTH" info
* **Customizable display options:**
  * Multiple pin icon styles (teardrop, circle, square, star)
  * QTH station icons: clean shapes (dot, plus, square, signal) or emoji, with a color picker and optional grid label
  * Custom grid square colors and opacity
  * Multiple basemap styles
  * Optional on-map legend for band/QTH colors
* **Grid square overlay with 4/6-character precision**
* **Map lines from each QTH to its QSOs (toggle on/off)**
* **Filter QSOs by band, mode, or originating QTH**
* **High-resolution map export (300 DPI for printing),** with an optional **Select Export Area** to crop the capture to exactly the region you drag out
* **KML export** — open your QTHs, contacts, and QSO paths in Google Earth for a free-zoom overview of a whole-world log
* **Share & embed** — publish a read-only snapshot link (`rayfall.me/m/...`), embed the live map in forums or websites with an iframe, or download the preview image for your QRZ page
* **Hide Controls** — collapse the whole header so the map fills the window (great on notebook screens)
* **Auto-reads your QTH(s) from log data** (`MY_GRIDSQUARE`, `MY_LAT`/`MY_LON`)
* **Works offline with ADI files** — import, map, and export (JPEG/KML) without an internet-dependent backend

---

## Screenshot

![RayfallScreenshot](static/rayfallScreenshot.png)

---

## Installation

### Prerequisites

* Python 3.11+
* pip
* Git

### 1. Clone the Repository

```bash
git clone https://github.com/moose25/rayfall.git
cd rayfall
```

### 2. Set Up a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note:** Required packages include FastAPI, uvicorn, and Jinja2. You can also install them manually:

```bash
pip install fastapi uvicorn jinja2
```

### 4. Start the Server

```bash
uvicorn main:app --reload
```

This starts the server locally at: `http://127.0.0.1:8000`

#### Port already in use?

Rayfall uses port **8000** by default. If that port is taken by another app,
the server won't start and you'll see an error:

* **Windows:** `[WinError 10013] ... an attempt was made to access a socket ...`
  (or `10048`)
* **macOS / Linux:** `[Errno 48] Address already in use`

Check whether a port is free, then run Rayfall on a free one with `--port`:

```bash
# See what's using a port (example: 8000)
# Windows:
netstat -ano | findstr :8000
# macOS / Linux:
lsof -i :8000

# Start Rayfall on a different port, e.g. 8001
uvicorn main:app --reload --port 8001
```

Then open the matching URL, e.g. `http://127.0.0.1:8001`.

> **Tip (Windows):** port 8000 can also fall inside a reserved range claimed by
> Hyper-V / WSL / Docker, which blocks it even when nothing is listening. List
> reserved ranges with `netsh int ipv4 show excludedportrange protocol=tcp` and
> pick a port outside them.

---

## Updating

To update an existing install to the latest version:

### 1. Pull the Latest Code

```bash
cd rayfall
git pull
```

### 2. Activate the Virtual Environment

```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Update Dependencies

```bash
pip install -r requirements.txt
```

### 4. Restart the Server

Stop the running server (`Ctrl+C`) and start it again:

```bash
uvicorn main:app --reload
```

> **Note:** If you run Rayfall as a service (e.g. systemd), restart it with your
> service manager instead — for example `sudo systemctl restart rayfall`.

---

## Usage Instructions

### Getting Started

**New users?** Click the **"📖 How to Use Rayfall"** button (top-right) for interactive tutorials!

### Method 1: QRZ API (Online)

1. Visit `http://127.0.0.1:8000` in your browser.
2. Click the **"Change API Key"** button in the top-right.
3. Paste in your **QRZ Logbook API key** and click **Save**.
4. Choose a start and end date and click **Load from QRZ**.
5. Filter contacts by band/mode and customize display options.

### Method 2: ADI File Import (Offline)

1. Visit `http://127.0.0.1:8000` in your browser.
2. Click **"Import ADI File"** and select your `.adi` or `.adif` file.
3. Your QSOs load instantly - no API key needed!
4. Filter contacts by band/mode and customize display options.

**See [QUICK_START_ADI.md](QUICK_START_ADI.md) for detailed ADI import guide.**

### Display Customization

Click the **"⚙️ Display Options"** button to access:
- **Map Style**: Light, Dark, Topographic, Satellite, Streets
- **QTH Icon**: Clean shapes (Dot, Plus, Square, Signal) or emoji, with a color picker and optional grid label under each marker
- **Color Pins by QTH**: color every contact by the QTH it was made from (great for multi-location trips)
- **Pin Style**: Teardrop, Circle, Square, or Star markers
- **Grid Squares**: Custom colors, opacity, and precision (4 or 6 chars)

All contacts with grid squares or lat/lon information will be plotted. Need more room for the map? **⏶ Hide Controls** (top-right) collapses the header; the floating **⚙️ Show Controls** chip brings it back.

### Exporting & Sharing

- **Export Map (300 DPI)** downloads a print-ready JPEG of the current view. Use **📐 Select Export Area** first to drag out exactly the region you want captured.
- **🌍 Export KML** downloads your QTHs, contacts, and QSO paths (colored per QTH) for Google Earth — ideal for browsing a whole-world log at any zoom level. Respects your active filters and works offline.
- **🔗 Share Map** publishes a read-only snapshot with a link, an iframe embed code, and a downloadable preview image (handy for QRZ pages, which block iframes).

### Need Help?

The **"📖 How to Use Rayfall"** button provides:
- Step-by-step setup instructions
- ADI import guide for all major logging software
- Display customization tutorials
- Filtering and export tips
- Pro tips for advanced usage

> ✅ You can switch logbooks anytime by clicking the API Key button again.

---

## QRZ API Key Info

Rayfall **does not store your API key on a server**. Instead:

* It saves it to `localStorage` in your browser.
* The backend reads the key from request headers.
* No secret is ever exposed in the source code.

> 🔐 This makes it safe to share or host this code publicly.

To generate a QRZ Logbook API Key:

1. Go to [https://logbook.qrz.com/](https://logbook.qrz.com/)
2. Click on **Settings > API**
3. Copy your unique API key

---

## Customization

### Change the Default Map Location

Rayfall centers on VA by default. Once a valid log is loaded, it updates to your actual QTH using the first valid `MY_LAT`/`MY_LON` (or the centre of `MY_GRIDSQUARE`) from the log. Logs that span multiple QTHs will show one marker per location.

If you'd like to hardcode a default starting location, edit:

```js
map = L.map('map').setView([XXX, XXX], 4);
```


### Styling

Edit the styles directly in the `<style>` block inside `index.html`. All controls and map elements can be styled using standard CSS.

---

## Directory Structure

```
rayfall/
├── main.py                 # FastAPI backend (QRZ proxy, share/embed API, previews)
├── render_preview.py       # Headless share-preview renderer (optional, needs Playwright)
├── templates/
│   └── index.html          # Frontend map UI (all CSS/JS lives here)
├── static/                 # Logo, marker, and preview images
├── data/                   # Created at runtime: shares DB + cached previews (gitignored)
├── requirements.txt        # Python dependencies
└── README.md               # You're reading this
```

---


## Maintenance Banner

Show a site-wide banner during updates or outages. State lives in `data/maintenance.json`
and is read per request, so toggling it takes effect without restarting the app (open
pages pick it up within ~60s; new loads immediately).

```bash
./maintenance.sh on "Back in 10 minutes while we deploy"   # enable (custom message optional)
./maintenance.sh off                                       # disable
./maintenance.sh status                                    # show current state
```

## Contributing

Pull requests and forks are welcome! If you find a bug or want to suggest a feature, feel free to open an issue or PR.

---

## License

This project is open source and available under the MIT License.

---

## Created by

**Chris Williams (N2CLW)**

* [qrz.com/db/N2CLW](https://www.qrz.com/db/N2CLW)
* [github.com/moose25](https://github.com/moose25)

---

> 73 and happy DXing!
