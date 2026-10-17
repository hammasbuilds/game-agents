"""Cut a short clip, a screenshot and a comparison still out of each film.

    python -m ui.shorts --out ../game-playing-agents

A full demonstration runs from twelve seconds to nearly two minutes, which is
right for someone who came to watch and wrong for a README or a feed. This makes
the short forms of each one, from the same film rather than from a fresh run:

* `demo.mp4` / `demo.gif` — eight seconds from the liveliest part of the film
* `screenshot.png` — one frame, full resolution
* `comparison.png` — the same frame with the panel labels left on, because the
  films are already untrained-beside-trained and the labels carry the scores

"Liveliest" is measured, not guessed: the window whose frames differ most from
each other. Taking the opening eight seconds gave clips of a car on an empty
track and a robot standing still, because the interesting part of a run is
rarely at the beginning.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from film.record import write_clip                                # noqa: E402
from observatory.demos import demos                               # noqa: E402

MEDIA = ROOT / "docs" / "media"


def read_frames(path: Path, stride: int = 1) -> list[np.ndarray]:
    import imageio.v3 as iio
    frames = []
    for i, frame in enumerate(iio.imiter(path)):
        if i % stride == 0:
            frames.append(np.asarray(frame))
    return frames


def liveliest(frames: list[np.ndarray], window: int) -> int:
    """Start index of the window whose frames differ most from one another.

    Mean absolute difference between consecutive frames, summed over the window.
    A still car and a still robot both score zero, which is the point.
    """
    if len(frames) <= window:
        return 0
    step = max(1, len(frames) // 240)          # sample, so long films stay cheap
    motion = np.zeros(len(frames))
    previous = frames[0].astype(np.int16)
    for i in range(step, len(frames), step):
        current = frames[i].astype(np.int16)
        motion[i] = np.abs(current - previous).mean()
        previous = current
    totals = np.convolve(motion, np.ones(window), mode="valid")
    return int(np.argmax(totals))


def cut(path: Path, out_dir: Path, seconds: float = 8.0, fps: int = 15) -> dict:
    import imageio.v3 as iio
    meta = iio.immeta(path)
    source_fps = float(meta.get("fps") or fps)
    frames = read_frames(path)
    if not frames:
        return {}
    window = min(len(frames), max(1, int(seconds * source_fps)))
    start = liveliest(frames, window)
    clip = frames[start:start + window]

    out_dir.mkdir(parents=True, exist_ok=True)
    write_clip(clip, out_dir / "demo.mp4", fps=int(round(source_fps)), gif=True,
               gif_width=420, gif_max_frames=48)

    # One frame from the middle of the chosen window: the still and the
    # comparison are the same picture, because the film is already a comparison
    # and the panel labels carry the scores.
    still = Image.fromarray(clip[len(clip) // 2])
    still.save(out_dir / "screenshot.png")
    still.save(out_dir / "comparison.png")
    return {"source": path.name, "seconds": round(len(clip) / source_fps, 1),
            "from_second": round(start / source_fps, 1),
            "frames": len(clip), "size": list(still.size)}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True, help="repository to write the media into")
    ap.add_argument("--seconds", type=float, default=8.0)
    ap.add_argument("--only", nargs="*", default=None, help="limit to these folders")
    args = ap.parse_args()

    out_root = Path(args.out)
    # Which film belongs to which numbered folder of the new repository.
    FOLDERS = {
        "doom/defend_the_center_640x480.mp4": "01-doom",
        "crafter/planner_vs_random.mp4": "02-crafter",
        "brogue/seed1.mp4": "03-brogue",
        "walker/walker2d.mp4": "04-walker",
        "racing/progress.mp4": "05-racing",
        "boxing/progress.mp4": "06-boxing",
        "platformer/progress.mp4": "07-kangaroo",
        "pingpong/progress.mp4": "08-pong",
    }
    known = {d.key: d for d in demos()}
    for key, folder in FOLDERS.items():
        if args.only and folder not in args.only:
            continue
        source = MEDIA / key
        if not source.exists():
            print(f"  {folder:<12} no film at {key}")
            continue
        info = cut(source, out_root / folder / "media", seconds=args.seconds)
        title = known[key].title if key in known else key
        print(f"  {folder:<12} {title:<42} {info.get('seconds')}s from "
              f"{info.get('from_second')}s of {info.get('source')}")


if __name__ == "__main__":
    main()
