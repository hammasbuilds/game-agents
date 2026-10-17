"""Load every page in a real browser and fail on anything it logs.

    python ui/check_live.py

`check_page.py` reads the HTML: files referenced but not shipped, CSS variables
used but never defined, numbers typed in rather than read from the data. It
cannot catch JavaScript, and twice in one day a page shipped broken anyway:

* a second `const body` in the same scope, which killed the whole dashboard;
* a change to the shape of the clips payload, after which one page called
  `endsWith` on an object and lost the section that plays the films.

Both were invisible to a static check and obvious to a browser one second after
loading. This serves `docs/` on a free port, visits each page, clicks every tab,
and reports console errors, page errors and failed requests.
"""
from __future__ import annotations

import argparse
import socket
import subprocess
import sys
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

# Requests that fail for reasons the page cannot help: a browser asks for these
# whether or not the page mentions them.
IGNORED = ("/favicon.ico",)


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def serve(directory: Path, port: int) -> ThreadingHTTPServer:
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(directory), **kwargs)

        def log_message(self, *args):       # quiet
            pass

    httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def chrome() -> str | None:
    """Playwright's own browser if it is installed, else None.

    This box has chromium 1243 but not the headless shell a newer playwright
    wants, and the download is throttled to nothing, so the full browser is used
    when the shell is missing.
    """
    base = Path.home() / "AppData/Local/ms-playwright"
    for candidate in sorted(base.glob("chromium-*/chrome-win64/chrome.exe"), reverse=True):
        return str(candidate)
    return None


def check(pages: list[str], base: str, verbose: bool = True) -> list[str]:
    from playwright.sync_api import sync_playwright

    problems: list[str] = []
    with sync_playwright() as pw:
        executable = chrome()
        browser = pw.chromium.launch(executable_path=executable) if executable \
            else pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 1000})
        seen: list[str] = []
        page.on("pageerror", lambda e: seen.append(f"page error: {e}"))
        page.on("console", lambda m: seen.append(f"console {m.type}: {m.text}")
                if m.type == "error" else None)
        page.on("response", lambda r: seen.append(f"{r.status} {r.url}")
                if r.status >= 400 and not r.url.endswith(IGNORED) else None)

        for name in pages:
            seen.clear()
            url = f"{base}/{name}"
            page.goto(url, wait_until="networkidle")
            page.wait_for_timeout(900)
            tabs = page.locator("#tabs button")
            for i in range(tabs.count()):
                tabs.nth(i).click()
                page.wait_for_timeout(500)
            if seen:
                problems.extend(f"{name}: {line}" for line in seen)
                if verbose:
                    print(f"{name}: {len(seen)} problem(s)")
                    for line in seen:
                        print(f"  - {line}")
            elif verbose:
                print(f"{name}: clean"
                      + (f" ({tabs.count()} tabs clicked)" if tabs.count() else ""))
        browser.close()
    return problems


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pages", nargs="*",
                    default=["index.html", "analytics.html", "game.html?g=racing"])
    ap.add_argument("--base", default=None,
                    help="check a running server instead of serving docs/")
    args = ap.parse_args()

    httpd = None
    base = args.base
    if base is None:
        port = free_port()
        httpd = serve(DOCS, port)
        base = f"http://127.0.0.1:{port}"
        time.sleep(0.4)
    try:
        problems = check(args.pages, base)
    finally:
        if httpd is not None:
            httpd.shutdown()

    print(f"\n{len(problems)} problem(s) across {len(args.pages)} page(s)")
    raise SystemExit(1 if problems else 0)


if __name__ == "__main__":
    main()
