"""Check the dashboard without opening a browser.

Catches the things that silently break a static page: a stylesheet or script the
page references but does not ship, an image with no file behind it, a CSS custom
property used but never defined (one typo put `#e0a martins` in a colour), a
dark-mode block that is not inside its media query, and any number hard-coded
into the HTML instead of read from the run data.

    python ui/check_page.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = [ROOT / "docs" / "index.html", ROOT / "docs" / "analytics.html"]

COLOUR = re.compile(r"^(#[0-9a-fA-F]{3,8}|rgb|hsl|var\(|transparent|currentColor|[a-z-]+)")


def check(page: Path) -> list[str]:
    html = page.read_text(encoding="utf-8")
    PAGE = page
    problems: list[str] = []

    # every local file the page asks for must exist
    for ref in re.findall(r'(?:src|href)="([^"]+)"', html):
        if ref.startswith(("http", "data:", "#", "mailto:")):
            continue
        if not (PAGE.parent / ref).exists():
            problems.append(f"references a file that is not there: {ref}")

    # no third-party assets: the page must stand on its own
    for ref in re.findall(r'(?:src|href)="(https?://[^"]+)"', html):
        problems.append(f"loads something remote, so the page is not self-contained: {ref}")

    # custom properties: used but never defined
    defined = set(re.findall(r"(--[a-z0-9-]+)\s*:", html))
    # `var(--s${i + 1})` in a template literal is a family of variables built at
    # run time, not a variable called `--s`; matching it was this checker's own
    # first false positive.
    used = set(re.findall(r"var\((--[a-z0-9-]+)(?!\$\{)", html))
    interpolated = set(re.findall(r"var\((--[a-z0-9-]+)\$\{", html))
    for prefix in interpolated:
        if not any(name.startswith(prefix) for name in defined):
            problems.append(f"builds {prefix}... at run time but defines no such variable")
    for name in sorted(used - defined):
        problems.append(f"uses {name} but never defines it")

    # a malformed colour value, like a word accidentally typed into one
    for name, value in re.findall(r"(--[a-z0-9-]+)\s*:\s*([^;]+);", html):
        value = value.strip()
        if name.endswith(("bg", "ink", "line", "accent", "good", "warn", "panel", "panel-2")):
            if not COLOUR.match(value) or " " in value and not value.startswith(("rgb", "hsl", "var")):
                problems.append(f"{name} does not look like a colour: {value!r}")

    # the dark-mode override must stay inside its media query, or it fires on
    # every default page
    for match in re.finditer(r':root:not\(\[data-theme="light"\]\)', html):
        before = html[:match.start()]
        depth = before.count("@media") - len(re.findall(r"@media[^{]*\{(?:[^{}]|\{[^{}]*\})*\}", before))
        if depth <= 0:
            problems.append("the dark-only selector sits outside its media query")

    # structural sanity: the overview has tabs, the analytics page does not
    if page.name == "index.html":
        for tab in ("overview", "doom", "crafter", "brogue", "bugs"):
            if f'id="{tab}"' not in html:
                problems.append(f"no section for the {tab} tab")
            if f'data-tab="{tab}"' not in html:
                problems.append(f"no button for the {tab} tab")

    # the page must not carry results of its own
    data = ROOT / "docs" / "data" / "results.js"
    if not data.exists():
        problems.append("docs/data/results.js is missing: run ui/export.py")
    else:
        body = html.split("<body>", 1)[1]
        for suspicious in re.findall(r">\s*(\d+\.\d+)\s*<", body):
            problems.append(f"a number is typed into the page rather than read from the data: {suspicious}")
    return problems


def main() -> int:
    data = ROOT / "docs" / "data" / "results.js"
    if data.exists():
        payload = json.loads(data.read_text().split("=", 1)[1].rsplit(";", 1)[0])
        print(f"data: doom={'yes' if payload['doom']['eval'] else 'no'} "
              f"crafter={'yes' if payload['crafter']['eval'] else 'no'} "
              f"brogue={'yes' if payload['brogue']['play'] else 'no'} "
              f"media={sum(len(v) for v in payload['media'].values())} files "
              f"clips={len(payload.get('clips', []))}")
    total = 0
    for page in PAGES:
        problems = check(page)
        total += len(problems)
        if problems:
            print(f"\n{page.name}: {len(problems)} problem(s)")
            for item in problems:
                print("  - " + item)
        else:
            print(f"{page.name}: checks out")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
