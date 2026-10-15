"""Score every checkpoint, then film them playing the same level side by side.

This is the artefact the whole arcade exists to produce: one video in which the
untrained network and the trained one play **the same seed at the same time**,
each labelled with how long it had trained and what it is scoring. Nobody has to
read a learning curve to see the difference, and nobody has to press play --
the clips autoplay, muted and looping, wherever they are shown.

    python -m arcade.progress --game boxing

Writes, under docs/media/<game>/:
    ladder.json      score of every checkpoint over the same evaluation seeds
    step_000.mp4     the untrained network, alone
    step_100.mp4     the final network, alone
    progress.mp4     all checkpoints at once, side by side
    progress.gif     the same, small enough for a README
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from .envs import CATALOGUE
from .play import load, rollout, score

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "docs" / "media"
PANEL_W, PANEL_H = 260, 330
LABEL_H = 42


def _font(size: int):
    """A readable font, falling back to PIL's built-in one.

    The default bitmap font is about 11 pixels tall, which survives a README and
    disappears in a feed where the video plays at a third of its size.
    """
    from PIL import ImageFont

    for name in ("segoeuib.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


TITLE_FONT = _font(17)
SUB_FONT = _font(14)


def label_panel(frame: np.ndarray, title: str, subtitle: str) -> Image.Image:
    """One agent's view, with who it is written underneath."""
    img = Image.fromarray(frame).convert("RGB").resize((PANEL_W, PANEL_H - LABEL_H),
                                                       Image.LANCZOS)
    panel = Image.new("RGB", (PANEL_W, PANEL_H), (12, 14, 18))
    panel.paste(img, (0, 0))
    draw = ImageDraw.Draw(panel)
    draw.text((8, PANEL_H - LABEL_H + 2), title, fill=(236, 240, 247), font=TITLE_FONT)
    draw.text((8, PANEL_H - LABEL_H + 19), subtitle, fill=(150, 175, 215), font=SUB_FONT)
    return panel


def compose(strips: list[tuple[str, str, list[np.ndarray]]]) -> list[np.ndarray]:
    """Lay several episodes out left to right, playing together.

    Episodes end at different times -- that is itself the result, since an
    untrained agent usually dies first -- so a finished one holds its last frame
    rather than disappearing and shuffling the others sideways.
    """
    length = max(len(frames) for _, _, frames in strips)
    out = []
    for i in range(length):
        panels = []
        for title, subtitle, frames in strips:
            frame = frames[min(i, len(frames) - 1)]
            panels.append(label_panel(frame, title, subtitle))
        canvas = Image.new("RGB", (PANEL_W * len(panels), PANEL_H), (12, 14, 18))
        for j, panel in enumerate(panels):
            canvas.paste(panel, (j * PANEL_W, 0))
        out.append(np.asarray(canvas))
    return out


def _show(path: Path) -> str:
    """A short name for a path that may or may not sit under the repository."""
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def write_clip(frames: list[np.ndarray], path: Path, fps: int = 20,
               gif: bool = False) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        import imageio.v2 as imageio
        # H.264 refuses odd dimensions.
        even = [f[:f.shape[0] // 2 * 2, :f.shape[1] // 2 * 2] for f in frames]
        imageio.mimwrite(path, even, fps=fps, quality=8, macro_block_size=None)
    except Exception as exc:
        # Only the encoding belongs in here. Wrapping the logging too meant a
        # failure to *print* the filename was reported as "no mp4" on a video
        # that had in fact been written perfectly well.
        print(f"  (no mp4 for {path.name}: {type(exc).__name__}: {exc})")
    else:
        print(f"  {_show(path)}  {path.stat().st_size / 1e6:.1f} MB")
    if gif:
        # A GIF is a sequence of full frames with no inter-frame compression, so
        # it grows without bound: the first boxing reel came out at 12.5 MB for
        # 891 frames, which is not a thing to put in a README. Cap the length and
        # drop frames evenly rather than truncating, so the clip still shows the
        # whole episode rather than its first few seconds.
        budget = 150
        stride = max(2, len(frames) // budget + 1)
        small = []
        for frame in frames[::stride]:
            img = Image.fromarray(frame)
            if img.width > 520:
                img = img.resize((520, round(img.height * 520 / img.width)), Image.LANCZOS)
            small.append(img.convert("P", palette=Image.ADAPTIVE, colors=48))
        gif_path = path.with_suffix(".gif")
        small[0].save(gif_path, save_all=True, append_images=small[1:],
                      duration=max(40, int(1000 * stride / fps)), loop=0, optimize=True)
        print(f"  {_show(gif_path)}  {gif_path.stat().st_size / 1e6:.1f} MB")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True, choices=sorted(CATALOGUE))
    ap.add_argument("--run", default=None, help="training directory (default runs_arcade/<game>)")
    ap.add_argument("--episodes", type=int, default=8, help="evaluation episodes per checkpoint")
    ap.add_argument("--film-seed", type=int, default=12345)
    ap.add_argument("--max-steps", type=int, default=2500)
    ap.add_argument("--panels", type=int, default=3, help="how many checkpoints to film")
    args = ap.parse_args()

    game = CATALOGUE[args.game]
    run_dir = Path(args.run or ROOT / "runs_arcade" / args.game)
    saved = json.loads((run_dir / "checkpoints.json").read_text())

    # Trust the directory over the registry. The weights are the artefact; the
    # registry is a note about them, and a run stopped between the two leaves
    # checkpoints that are real and unlisted.
    listed = {entry["path"] for entry in saved}
    for path in sorted(run_dir.glob("ckpt_*.pt")):
        if path.name in listed:
            continue
        tag = path.stem.replace("ckpt_", "")
        import torch
        blob = torch.load(path, map_location="cpu", weights_only=False)
        saved.append({"tag": tag, "update": None, "steps": int(blob.get("step", 0)),
                      "path": path.name, "return_mean": None})
        print(f"found an unlisted checkpoint on disk: {path.name} "
              f"at {blob.get('step', 0):,} steps")
    saved.sort(key=lambda entry: entry["steps"])
    out_dir = MEDIA / args.game

    # -- the ladder --------------------------------------------------------
    seeds = [50_000 + i for i in range(args.episodes)]
    ladder = [{"tag": "random", "steps": None,
               **score(None, game, seeds, max_steps=args.max_steps)}]
    for entry in saved:
        row = score(run_dir / entry["path"], game, seeds, max_steps=args.max_steps)
        ladder.append({"tag": entry["tag"], "steps": entry["steps"], **row})
        print(f"{entry['tag']:>6}  {entry['steps']:>9} steps  "
              f"score {row['return_mean']:8.2f} +- {row['return_std']:.2f}", flush=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "ladder.json").write_text(json.dumps(
        {"game": game.key, "title": game.title, "env_id": game.env_id,
         "evaluation_seeds": seeds, "ladder": ladder}, indent=1))

    # -- the films ---------------------------------------------------------
    pick = [saved[0]] + ([saved[len(saved) // 2]] if len(saved) > 2 and args.panels > 2 else []) \
        + [saved[-1]]
    strips = []
    for entry in pick:
        model, loaded_game, _ = load(run_dir / entry["path"])
        episode = rollout(model, loaded_game, args.film_seed,
                          max_steps=args.max_steps, record=True)
        trained = "untrained" if entry["steps"] == 0 else f"{entry['steps']:,} steps"
        strips.append((trained, f"score {episode.total_reward:.0f}", episode.frames))
        write_clip(episode.frames, out_dir / f"step_{entry['tag']}.mp4")
        print(f"filmed {entry['tag']}: {len(episode.frames)} frames, "
              f"score {episode.total_reward:.0f}", flush=True)

    write_clip(compose(strips), out_dir / "progress.mp4", gif=True)
    print(f"\nwrote {out_dir.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
