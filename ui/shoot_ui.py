"""Screenshot the two interfaces for the README, in a real browser.

    python ui/shoot_ui.py

`shoot_pages.py` photographs whole pages into `docs/_shots/`, which is ignored
by git — those are for looking at while working. These are the pictures the
README ships, so they are committed, cropped to the part worth showing, and
taken at a width that stays legible when GitHub scales them down.

Each shot is taken from the live page rather than drawn: a screenshot of a
dashboard that no longer renders is worse than none.
"""
from __future__ import annotations

import argparse
import socket
import sys
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "media" / "ui"

CHROME_GLOB = "AppData/Local/ms-playwright/chromium-*/chrome-win64/chrome.exe"


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def serve(directory: Path, port: int) -> ThreadingHTTPServer:
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(directory), **kwargs)

        def log_message(self, *args):
            pass

    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def chrome() -> str | None:
    for candidate in sorted(Path.home().glob(CHROME_GLOB), reverse=True):
        return str(candidate)
    return None


def shoot(page, url: str, out: Path, *, clip_to: str | None = None,
          click: str | None = None, wait: int = 1200) -> None:
    page.goto(url, wait_until="networkidle")
    if click:
        page.click(click)
    page.wait_for_timeout(wait)
    out.parent.mkdir(parents=True, exist_ok=True)
    if clip_to:
        element = page.locator(clip_to).first
        element.screenshot(path=str(out))
    else:
        page.screenshot(path=str(out))
    print(f"  {out.relative_to(ROOT)}  {out.stat().st_size / 1e6:.2f} MB")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--panel", default=None,
                    help="a running Observatory to photograph, e.g. http://127.0.0.1:8777")
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright

    port = free_port()
    httpd = serve(ROOT / "docs", port)
    base = f"http://127.0.0.1:{port}"
    time.sleep(0.4)
    try:
        with sync_playwright() as pw:
            executable = chrome()
            browser = pw.chromium.launch(executable_path=executable) if executable \
                else pw.chromium.launch()
            page = browser.new_page(viewport={"width": 1280, "height": 1000},
                                    device_scale_factor=2)
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))

            # The dashboard: the table every result lives in, and the rounds.
            shoot(page, f"{base}/index.html", OUT / "dashboard-scoreboard.png",
                  clip_to="#overview .card")
            shoot(page, f"{base}/index.html", OUT / "dashboard-rounds.png",
                  clip_to="#overview .card:nth-of-type(2)")
            shoot(page, f"{base}/analytics.html", OUT / "analytics.png",
                  clip_to=".card")

            if args.panel:
                shoot(page, args.panel, OUT / "observatory-demos.png",
                      click="#nav-demos", wait=2500)
                shoot(page, args.panel, OUT / "observatory-projects.png",
                      click="#nav-projects", wait=2000)
            else:
                print("  (no --panel given: the Observatory shots need it running)")
            browser.close()
            if errors:
                print("  page errors:", errors)
                raise SystemExit(1)
    finally:
        httpd.shutdown()


if __name__ == "__main__":
    main()
