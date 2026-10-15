"""Open the dashboard in a real browser, screenshot it, and fail on console errors.

The static checker in `check_page.py` reads the HTML; it cannot tell whether the
JavaScript threw on load and left a blank page. This opens each page in headless
Chromium, waits for it to settle, records anything the console complained about,
and saves a screenshot to look at.

    python ui/shoot_pages.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "docs" / "_shots"

PAGES = [
    ("index", "index.html"),
    ("analytics", "analytics.html"),
    ("game-boxing", "game.html?g=boxing"),
]
EXTRA_PAGES = [("observatory", ROOT / "observatory" / "index.html"),
               ("observatory-boxing", ROOT / "observatory" / "index.html"),
               ("observatory-doom", ROOT / "observatory" / "index.html")]


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("playwright is not installed; skipping the browser check")
        return 0

    SHOTS.mkdir(parents=True, exist_ok=True)
    problems: list[str] = []
    with sync_playwright() as pw:
        # Use the Chrome already on the machine rather than downloading another
        # browser: playwright's bundled build is version-pinned and a mismatch
        # costs a 130 MB download for a screenshot.
        try:
            browser = pw.chromium.launch(channel="chrome")
        except Exception:
            browser = pw.chromium.launch()
        try:
            jobs = [(n, (ROOT / "docs" / t.split("?")[0]), t) for n, t in PAGES] +                    [(n, p, p.name + ("#/" + n.split("-", 1)[1] if "-" in n else ""))
                    for n, p in EXTRA_PAGES]
            for name, base, target in jobs:
                page = browser.new_page(viewport={"width": 1280, "height": 1000})
                errors: list[str] = []
                page.on("console", lambda m: errors.append(f"{m.type}: {m.text}")
                        if m.type in ("error", "warning") else None)
                page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
                url = base.as_uri()
                if "?" in target:
                    url += "?" + target.split("?", 1)[1]
                if "#" in target:
                    url += "#" + target.split("#", 1)[1]
                page.goto(url, wait_until="load")
                page.wait_for_timeout(1200)

                # A page that rendered has content below the header.
                body_text = page.inner_text("body")
                if len(body_text) < 400:
                    problems.append(f"{name}: the page rendered almost nothing "
                                    f"({len(body_text)} characters)")
                for err in errors:
                    # A missing clip is expected while a game is still training.
                    if "net::ERR_FILE_NOT_FOUND" in err or "Failed to load resource" in err:
                        continue
                    problems.append(f"{name}: {err}")

                shot = SHOTS / f"{name}.png"
                page.screenshot(path=str(shot), full_page=True)
                print(f"{name:<13} {len(body_text):>6} chars  -> {shot.relative_to(ROOT)}")
                page.close()
        finally:
            browser.close()

    if problems:
        print(f"\n{len(problems)} problem(s):")
        for item in problems:
            print("  - " + item)
        return 1
    print("\nevery page rendered with a clean console")
    return 0


if __name__ == "__main__":
    sys.exit(main())
