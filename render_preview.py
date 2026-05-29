"""Render a PNG preview of a shared map by screenshotting its embed page.

Run as a subprocess by the web app (see ensure_preview in main.py):
    python render_preview.py <share_id> <output_path> [base_url]

Uses Playwright/Chromium from a separate .render-venv so the browser never
runs inside the web process.
"""
import sys
from playwright.sync_api import sync_playwright

HIDE_CHROME = ".embed-badge{display:none!important;}.leaflet-control-container{display:none!important;}"


def main():
    if len(sys.argv) < 3:
        print("usage: render_preview.py <share_id> <output_path> [base_url]", file=sys.stderr)
        sys.exit(2)
    share_id = sys.argv[1]
    out_path = sys.argv[2]
    base = sys.argv[3] if len(sys.argv) > 3 else "http://127.0.0.1:8000"
    url = f"{base}/embed/{share_id}"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=2)
            page.goto(url, wait_until="networkidle", timeout=45000)
            page.add_style_tag(content=HIDE_CHROME)
            page.wait_for_timeout(4000)  # let tiles + markers settle
            page.screenshot(path=out_path)
        finally:
            browser.close()


if __name__ == "__main__":
    main()
