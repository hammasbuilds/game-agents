"""Drive the live Observatory panel through every section and fail on anything broken.

    python ui/check_observatory.py --panel http://127.0.0.1:8777/

`check_live.py` covers the published dashboard in docs/. This covers the thing
docs/ cannot be: a running control panel with a token, three APIs behind it and
buttons that start real subprocesses. Those are exactly the parts that broke
during the build -- /api/jobs dying inside its handler and closing the socket,
films 404ing because the page is served from observatory/ while the media sits
in docs/, a training launch failing silently against my own overwrite guard --
and none of them are visible to a reader of the HTML.

Every assertion here is about something the page must show or do. A section that
renders nothing is a failure, not a pass.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "docs" / "screenshots" / "observatory"


def chrome_kwargs() -> dict:
    if Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe").exists():
        return {"channel": "chrome"}
    for candidate in sorted(Path.home().glob(
            "AppData/Local/ms-playwright/chromium-*/chrome-win64/chrome.exe"), reverse=True):
        return {"executable_path": str(candidate)}
    return {}


def api(base: str, path: str) -> dict:
    with urllib.request.urlopen(base.rstrip("/") + path, timeout=30) as response:
        return json.load(response)


DEAD_VIDEOS = """() => [...document.querySelectorAll('video')]
    .filter(v => v.error || (v.readyState === 0 && v.networkState === 3))
    .map(v => v.getAttribute('src'))"""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--panel", default="http://127.0.0.1:8777/")
    ap.add_argument("--shots", action="store_true", help="save a shot of each view")
    ap.add_argument("--no-train", action="store_true",
                    help="skip the start/stop test (it launches a real trainer)")
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright

    base = args.panel.rstrip("/")
    problems: list[str] = []
    checked: list[str] = []

    def ok(label: str) -> None:
        checked.append(label)
        print(f"  ok    {label}")

    def bad(label: str) -> None:
        problems.append(label)
        print(f"  FAIL  {label}")

    def judge(condition: bool, good: str, ill: str) -> None:
        ok(good) if condition else bad(ill)

    # ---- the APIs the page cannot render without ---------------------------
    jobs = api(base, "/api/jobs")
    if jobs.get("problem"):
        bad(f"/api/jobs reports a problem: {jobs['problem']}")
    else:
        judge(bool(jobs.get("games")),
              f"/api/jobs: {len(jobs.get('games') or [])} games, "
              f"{len(jobs.get('schema') or {})} config fields",
              "/api/jobs returned no games")
    demos = api(base, "/api/demos").get("demos") or []
    judge(bool(demos), f"/api/demos: {len(demos)} films", "/api/demos is empty")
    projects = api(base, "/api/projects").get("projects") or []
    judge(bool(projects), f"/api/projects: {len(projects)} rows", "/api/projects is empty")

    if args.shots:
        SHOTS.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, **chrome_kwargs())
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        logged: list[str] = []
        page.on("pageerror", lambda e: logged.append(f"page error: {e}"))
        page.on("console", lambda m: logged.append(f"console {m.type}: {m.text}")
                if m.type == "error" else None)
        def note_failure(request) -> None:
            # Leaving a view cancels the films it was still loading, and the
            # browser reports every cancellation as a failed request. Those are
            # not broken links -- each of these URLs serves 200 -- so only a
            # real transport or status failure counts.
            text = (request.failure or "")
            if "favicon" in request.url or "ERR_ABORTED" in text:
                return
            logged.append(f"request failed ({text.strip() or 'no reason given'}): {request.url}")

        page.on("requestfailed", note_failure)

        def shot(name: str) -> None:
            if args.shots:
                page.screenshot(path=str(SHOTS / f"{name}.png"), full_page=True)

        # ---- overview: a card per project -----------------------------------
        page.goto(base + "/", wait_until="domcontentloaded")
        page.wait_for_timeout(3500)
        cards = page.locator("#main .grid .card").count()
        judge(bool(cards), f"overview: {cards} project cards", "overview rendered no cards")
        playing = page.locator("#main .thumb video").count()
        judge(bool(playing), f"overview: {playing} cards play a film",
              "overview: not one card plays a film")
        shot("01-overview")

        # ---- a project page, with its numbers and its films ------------------
        first = (jobs.get("games") or [{}])[0]
        key = first.get("key") if isinstance(first, dict) else str(first)
        page.goto(f"{base}/#/{key}", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        if page.locator("#main .head h2").count():
            ok(f"project page '{key}': {page.locator('#main .head h2').first.inner_text()}")
        else:
            bad(f"project page '{key}' rendered no heading")
        tiles = page.locator("#main .tiles > *").count()
        judge(bool(tiles), f"project page: {tiles} number tiles", "project page: no tiles")
        films = page.locator("#main video").count()
        judge(bool(films), f"project page: {films} films", "project page: no films")
        broken = page.evaluate(DEAD_VIDEOS)
        judge(not broken, "project page: every film loads",
              f"project page: {len(broken)} film(s) did not load: {broken[:3]}")
        shot("02-project")

        # ---- the training form, and a real start/stop ------------------------
        fields = page.locator("#main [data-field]").count()
        judge(bool(fields), f"training form: {fields} inputs", "training form: no inputs")
        def trainer(game: str) -> dict | None:
            """The train job for this game, or None. Not a count of all jobs.

            Counting was wrong twice over: a restart replaces the entry for a
            game rather than adding one, so a working start looked like a
            no-op; and reading a "state" key that job_status() never emits made
            the stop check pass on [None], reporting success while measuring
            nothing at all.
            """
            for job in api(base, "/api/jobs")["jobs"]:
                if job.get("kind") == "train" and job.get("game") == game:
                    return job
            return None

        def toggle(label: str, want_running: bool) -> bool:
            """Press the one train button, whichever way it currently reads.

            Then wait for the state to actually change rather than for a fixed
            number of seconds: stopping asks the run to end and gives it up to
            twelve seconds to do so, and an eight-second guess called a working
            stop a failure.
            """
            button = page.locator(f"#main button:has-text('{label} training')")
            if not button.count():
                return False
            button.first.click()
            for _ in range(30):
                page.wait_for_timeout(1000)
                if bool((trainer(key) or {}).get("running")) == want_running:
                    break
            return True

        running = bool((trainer(key) or {}).get("running"))
        if args.no_train:
            ok("training form: start/stop skipped")
        elif running and not toggle("stop", False):
            bad(f"{key} is training and the panel offers no stop button")
        else:
            if running:
                # The button is a toggle, so a run left over from an earlier
                # pass makes it read "stop training" and a checker that only
                # looks for "start training" declares the feature missing.
                judge(not (trainer(key) or {}).get("running"),
                      "stop training: the leftover trainer was stopped",
                      "stop training: the leftover trainer kept running")
            if not toggle("start", True):
                bad("no 'start training' button on the project page")
            else:
                job = trainer(key)
                if not (job and job.get("running")):
                    bad(f"start training: no running trainer for {key} (got {job})")
                else:
                    ok(f"start training: pid {job['pid']} running, "
                       f"log {Path(job['log']).name}")
                    if not toggle("stop", False):
                        bad("start worked but no stop button appeared")
                    else:
                        job = trainer(key)
                        judge(not (job and job.get("running")),
                              "stop training: the trainer is no longer running",
                              f"stop training: pid {(job or {}).get('pid')} still running")

        # ---- the sweep panel -------------------------------------------------
        selects = page.locator("#main select").count()
        judge(bool(selects), f"sweep panel: {selects} selector(s)",
              "sweep panel: no selector")

        # ---- demos -----------------------------------------------------------
        page.click("#nav-demos")
        page.wait_for_timeout(3500)
        films = page.locator("#main video").count()
        judge(bool(films), f"demos view: {films} films", "demos view: no films")
        dead = page.evaluate(DEAD_VIDEOS)
        judge(not dead, "demos view: every film loads",
              f"demos view: {len(dead)} film(s) did not load: {dead[:3]}")
        shot("03-demos")

        # ---- projects & tools ------------------------------------------------
        page.click("#nav-projects")
        page.wait_for_timeout(3500)
        rows = page.locator("#main .pgrid > *").count()
        judge(bool(rows), f"projects view: {rows} rows", "projects view: no rows")
        links = page.evaluate("""() => [...document.querySelectorAll('#main a[href]')]
            .map(a => a.href).filter(h => h.startsWith('http'))""")
        judge(bool(links), f"projects view: {len(links)} outward links",
              "projects view: no GitHub or live-page links")
        shot("04-projects")

        # ---- theme -----------------------------------------------------------
        was = page.evaluate("() => document.documentElement.dataset.theme || 'unset'")
        page.click("#theme")
        page.wait_for_timeout(900)
        now = page.evaluate("() => document.documentElement.dataset.theme || 'unset'")
        judge(now != was, f"theme toggle: {was} -> {now}",
              f"theme toggle changed nothing (stayed {was})")

        # ---- the machine line is live, not typed in --------------------------
        machine = page.locator("#machine").inner_text()
        judge(bool(machine.strip()), f"machine line: {machine[:70]}", "machine line empty")

        browser.close()

    for line in logged:
        bad(line)

    print(f"\n{len(checked)} check(s) passed")
    if problems:
        print(f"{len(problems)} problem(s):")
        for line in problems:
            print(f"  - {line}")
        sys.exit(1)
    print("the panel works end to end")


if __name__ == "__main__":
    main()
