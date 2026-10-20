"""Drive the Observatory through every feature, recording a film and shots.

    python ui/demo_drive.py --panel http://127.0.0.1:8777/

Everything here is a real click on the running panel: real values typed into the
training form, a real job started and stopped, the real demonstration films
playing. If a control does nothing, this script says so rather than carrying on
— a demonstration of a feature that does not work is worse than no
demonstration.

The video is for a feed and is not committed. The screenshots are, one per
feature, each taken *after* the feature has produced its result.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHOTS = ROOT / "docs" / "screenshots"
VIEWPORT = {"width": 1280, "height": 720}


def chrome_channel_or_path():
    """System Chrome by channel; fall back to the playwright chromium on disk."""
    if Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe").exists():
        return {"channel": "chrome"}
    for candidate in sorted(Path.home().glob(
            "AppData/Local/ms-playwright/chromium-*/chrome-win64/chrome.exe"), reverse=True):
        return {"executable_path": str(candidate)}
    return {}


def to_mp4(webm: Path, mp4: Path) -> None:
    import imageio_ffmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    mp4.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([ffmpeg, "-y", "-i", str(webm), "-c:v", "libx264",
                    "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                    "-r", "25", str(mp4)],
                   check=True, capture_output=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--panel", default="http://127.0.0.1:8777/")
    ap.add_argument("--out", default=str(Path.home() / "Desktop" / "game-agents-demo.mp4"))
    ap.add_argument("--slow", type=int, default=250)
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright

    SHOTS.mkdir(parents=True, exist_ok=True)
    video_dir = Path(tempfile.mkdtemp(prefix="obs-demo-"))
    problems: list[str] = []
    saved: list[str] = []

    def shot(page, name: str) -> None:
        path = SHOTS / f"{name}.png"
        page.screenshot(path=str(path), full_page=True)
        saved.append(str(path.relative_to(ROOT)))
        print(f"  shot  {path.relative_to(ROOT)}")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, slow_mo=args.slow,
                                     **chrome_channel_or_path())
        context = browser.new_context(viewport=VIEWPORT, record_video_dir=str(video_dir),
                                      record_video_size=VIEWPORT)
        page = context.new_page()
        page.on("pageerror", lambda e: problems.append(f"page error: {e}"))
        page.on("console", lambda m: problems.append(f"console {m.type}: {m.text}")
                if m.type == "error" else None)

        # ---- the overview ---------------------------------------------------
        page.goto(args.panel, wait_until="networkidle")
        page.wait_for_timeout(2500)
        shot(page, "01-overview")
        page.mouse.wheel(0, 600)
        page.wait_for_timeout(1500)
        page.mouse.wheel(0, -600)

        # ---- one game, end to end -------------------------------------------
        page.locator(".card").first.click()
        page.wait_for_timeout(2500)
        page.mouse.wheel(0, 500)
        page.wait_for_timeout(1500)
        shot(page, "02-game-page")

        # ---- the training form, with real values ----------------------------
        form = page.locator(".cfg, .sweep, form").first
        if form.count():
            arch = page.locator('[data-field="arch"]').first
            if arch.count():
                arch.select_option(index=1)       # a different architecture
                page.wait_for_timeout(900)
            for field, value in (("steps", "300000"), ("lr", "0.00025"),
                                 ("entropy", "0.015")):
                box = page.locator(f'[data-field="{field}"]').first
                if box.count():
                    # Clear by selecting rather than fill(""): choosing an
                    # architecture refills the form from its preset, and typing
                    # into a box that refilled itself appends to the preset --
                    # which is how a learning rate of 0.00015000025 reached a
                    # screenshot.
                    box.click()
                    box.press("Control+a")
                    box.type(value, delay=90)
                    box.press("Tab")
                    page.wait_for_timeout(600)
            page.wait_for_timeout(1200)
            shot(page, "03-training-settings")

        # ---- start a run, see it appear, stop it ----------------------------
        start = page.get_by_role("button", name="start training").first
        if start.count():
            start.click()
            # Wait for the job to actually exist, not for a fixed number of
            # seconds: the first version screenshotted a page where nothing had
            # started and called it "training started".
            try:
                page.wait_for_selector("button:has-text('stop training')", timeout=15000)
            except Exception:
                problems.append("clicking start training did not produce a running job")
            page.wait_for_timeout(3000)
            shot(page, "04-training-started")
            stop = page.get_by_role("button", name="stop training").first
            if stop.count():
                stop.click()
                page.wait_for_timeout(4000)
                shot(page, "05-training-stopped")
            else:
                problems.append("a run started and no stop button appeared")
        else:
            problems.append("no start training button on the game page")

        # ---- the demonstrations ---------------------------------------------
        page.click("#nav-demos")
        page.wait_for_timeout(3500)
        shot(page, "06-demonstrations")
        page.mouse.wheel(0, 900)
        page.wait_for_timeout(2500)
        first_video = page.locator(".dcard video").first
        first_video.evaluate("v => v.play()")
        page.wait_for_timeout(3500)
        shot(page, "07-demonstration-playing")

        # ---- the launcher ----------------------------------------------------
        page.click("#nav-projects")
        page.wait_for_timeout(3000)
        shot(page, "08-projects")
        page.mouse.wheel(0, 1200)
        page.wait_for_timeout(2000)
        shot(page, "09-projects-scrolled")

        # ---- the theme --------------------------------------------------------
        page.click("#theme")
        page.wait_for_timeout(2000)
        shot(page, "10-light-theme")
        page.click("#theme")
        page.wait_for_timeout(1500)

        video = page.video
        context.close()
        browser.close()
        webm = Path(video.path()) if video else None

    if webm and webm.exists():
        mp4 = Path(args.out)
        to_mp4(webm, mp4)
        print(f"\n  video {mp4}  {mp4.stat().st_size / 1e6:.1f} MB")
    else:
        print("\n  no video recorded")
    shutil.rmtree(video_dir, ignore_errors=True)

    print(f"\n{len(saved)} screenshots")
    if problems:
        print(f"{len(problems)} problem(s) the browser reported:")
        for line in problems:
            print(f"  - {line}")
        raise SystemExit(1)
    print("no console errors, no page errors")


if __name__ == "__main__":
    main()
