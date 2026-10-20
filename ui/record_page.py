"""Record any local page for N seconds as an MP4 and a GIF.

    python ui/record_page.py http://127.0.0.1:8846/anatomy.html docs/media/anatomy/game-agents

Used for the isometric anatomy animation, which is a CSS animation on a page
rather than a rendered video: recording the page is how it becomes something a
feed will play. The GIF is the one that autoplays on LinkedIn and in a README;
the MP4 is smaller and sharper for everything else.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def chrome_kwargs() -> dict:
    if Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe").exists():
        return {"channel": "chrome"}
    for candidate in sorted(Path.home().glob(
            "AppData/Local/ms-playwright/chromium-*/chrome-win64/chrome.exe"), reverse=True):
        return {"executable_path": str(candidate)}
    return {}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("out", help="path without extension; .mp4 and .gif are written")
    ap.add_argument("--seconds", type=float, default=18.5)
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--height", type=int, default=720)
    ap.add_argument("--gif-width", type=int, default=720, dest="gif_width")
    ap.add_argument("--gif-fps", type=int, default=12, dest="gif_fps")
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright
    import imageio_ffmpeg

    viewport = {"width": args.width, "height": args.height}
    tmp = Path(tempfile.mkdtemp(prefix="anatomy-"))
    problems: list[str] = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, **chrome_kwargs())
        context = browser.new_context(viewport=viewport, record_video_dir=str(tmp),
                                      record_video_size=viewport)
        page = context.new_page()
        page.on("pageerror", lambda e: problems.append(f"page error: {e}"))
        page.on("console", lambda m: problems.append(f"console {m.type}: {m.text}")
                if m.type == "error" else None)
        page.goto(args.url, wait_until="networkidle")
        # Start at the top of the loop so the clip does not open mid-animation.
        page.evaluate("document.getAnimations().forEach(a => { a.cancel(); a.play(); })")
        page.wait_for_timeout(int(args.seconds * 1000))
        video = page.video
        context.close()
        browser.close()
        source = Path(video.path()) if video else None

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    mp4 = out.with_suffix(".mp4")
    subprocess.run([ffmpeg, "-y", "-i", str(source), "-c:v", "libx264", "-pix_fmt",
                    "yuv420p", "-movflags", "+faststart", "-r", "25", str(mp4)],
                   check=True, capture_output=True)

    gif = out.with_suffix(".gif")
    palette = tmp / "palette.png"
    chain = f"fps={args.gif_fps},scale={args.gif_width}:-1:flags=lanczos"
    subprocess.run([ffmpeg, "-y", "-i", str(mp4), "-vf", f"{chain},palettegen=stats_mode=diff",
                    str(palette)], check=True, capture_output=True)
    subprocess.run([ffmpeg, "-y", "-i", str(mp4), "-i", str(palette), "-lavfi",
                    f"{chain}[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=3",
                    "-loop", "0", str(gif)], check=True, capture_output=True)

    shutil.rmtree(tmp, ignore_errors=True)
    print(f"  {mp4.relative_to(ROOT) if mp4.is_relative_to(ROOT) else mp4}  "
          f"{mp4.stat().st_size / 1e6:.1f} MB")
    print(f"  {gif.relative_to(ROOT) if gif.is_relative_to(ROOT) else gif}  "
          f"{gif.stat().st_size / 1e6:.1f} MB")
    if problems:
        print("  problems:", problems)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
