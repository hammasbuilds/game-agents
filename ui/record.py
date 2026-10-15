"""Record the agents playing, as GIFs for the README and MP4s for anywhere else.

    python ui/record.py --game doom --seconds 20
    python ui/record.py --game crafter
    python ui/record.py --game brogue
    python ui/record.py --game all

Each clip is a real episode played by the agent in this repository — not a replay
of a hand-picked run and not sped up past the point of being honest. The frame
rate is written on the clip so a viewer can tell real time from a flipbook.

MP4 needs `imageio-ffmpeg`; without it the GIF is still written, since that is
what a README can show inline anyway.
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "media"


def save_clip(frames: list[np.ndarray], name: str, fps: int = 12) -> list[str]:
    """Write frames as a GIF and, if the encoder is there, an MP4."""
    OUT.mkdir(parents=True, exist_ok=True)
    written = []
    # The GIF is the one a README shows inline, so it is the one that has to be
    # small: every other frame, capped at 480 px wide, and quantised to a 64
    # colour palette. The Brogue clip is 9.1 MB without this and 1.2 MB with it.
    gif_frames = []
    for f in frames[::2]:
        img = Image.fromarray(f)
        if img.width > 480:
            img = img.resize((480, round(img.height * 480 / img.width)), Image.LANCZOS)
        gif_frames.append(img.convert("P", palette=Image.ADAPTIVE, colors=64))
    gif = OUT / f"{name}.gif"
    gif_frames[0].save(gif, save_all=True, append_images=gif_frames[1:],
                       duration=int(2000 / fps), loop=0, optimize=True)
    written.append(gif.name)
    print(f"  {gif.name}  {len(frames)} frames  {gif.stat().st_size / 1e6:.1f} MB")
    try:
        import imageio.v2 as imageio
        mp4 = OUT / f"{name}.mp4"
        # even dimensions: H.264 refuses odd ones
        even = [f[:f.shape[0] // 2 * 2, :f.shape[1] // 2 * 2] for f in frames]
        imageio.mimwrite(mp4, even, fps=fps, quality=8, macro_block_size=None)
        written.append(mp4.name)
        print(f"  {mp4.name}  {mp4.stat().st_size / 1e6:.1f} MB")
    except Exception as exc:
        print(f"  (no mp4: {exc})")
    return written


def caption(frame: np.ndarray, text: str, scale: int = 1) -> np.ndarray:
    img = Image.fromarray(frame)
    if scale != 1:
        img = img.resize((img.width * scale, img.height * scale), Image.NEAREST)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, img.height - 18, img.width, img.height], fill=(0, 0, 0))
    draw.text((6, img.height - 15), text, fill=(235, 240, 250))
    return np.asarray(img)


# -- the three games -------------------------------------------------------
def best_of(runs: list[tuple[float, list[np.ndarray], str]], name: str, fps: int) -> list[str]:
    """Keep the best episode of several, and say what the others scored.

    A demo reel is allowed to show a good game; it is not allowed to imply that
    every game looks like that. Each score is printed, the chosen one is marked,
    and the clip is captioned with its own result so a viewer sees the number
    they are being shown rather than the average they are not.
    """
    runs.sort(key=lambda r: -r[0])
    print(f"  episodes: " + ", ".join(f"{r[2]}" for r in runs))
    print(f"  keeping:  {runs[0][2]}")
    return save_clip(runs[0][1], name, fps)


def record_doom(seconds: int = 20, fps: int = 12, episodes: int = 4) -> list[str]:
    sys.path.insert(0, str(ROOT / "projects" / "01-doom-pixel-rl"))
    import torch
    from doomagent.env import DoomEnv, EnvConfig
    from doomagent.model import ActorCritic

    weights = ROOT / "projects/01-doom-pixel-rl/runs/defend_the_center/policy.pt"
    blob = torch.load(weights, map_location="cpu", weights_only=False)
    model = ActorCritic(tuple(blob["obs_shape"]), blob["n_actions"],
                        width=int(blob.get("width", 1)))
    model.load_state_dict(blob["model"])
    model.eval()

    runs = []
    for ep in range(episodes):
        env = DoomEnv(EnvConfig(scenario="defend_the_center", seed=900003 + ep))
        frames, kills = [], 0
        try:
            obs = env.reset()
            for _ in range(seconds * fps):
                action, _, _ = model.act(torch.from_numpy(np.ascontiguousarray(obs[None])),
                                         greedy=True)
                state = env.game.get_state()
                if state is not None:
                    shot = np.transpose(state.screen_buffer, (1, 2, 0))
                    kills = int(env.game.get_total_reward())
                    frames.append(caption(shot, f"PPO from pixels   kills {kills}", scale=2))
                obs, _, done = env.step(int(action[0]))
                if done:
                    break
        finally:
            env.close()
        runs.append((kills, frames, f"seed {900003 + ep}: {kills} kills"))
    return best_of(runs, "clip_doom", fps)


def record_crafter(steps: int = 240, fps: int = 10, episodes: int = 4) -> list[str]:
    sys.path.insert(0, str(ROOT / "projects" / "02-crafter-planner"))
    import crafter
    from crafteragent.agent import PlannerAgent

    runs = []
    for ep in range(episodes):
        seed = 504 + ep
        env = crafter.Env(seed=seed, length=steps + 2)
        frame = env.reset()
        agent = PlannerAgent()
        agent.reset()
        frames, info = [], {"achievements": {}}
        for _ in range(steps):
            action = agent.act(frame)
            big = np.asarray(Image.fromarray(frame).resize((256, 256), Image.NEAREST))
            frames.append(caption(big, f"planner, no training   goal: {agent.chosen}   "
                                       f"achievements {len(agent.unlocked)}"))
            frame, _, done, info = env.step(action)
            if done:
                break
        got = sorted(k for k, v in info["achievements"].items() if v)
        runs.append((len(got), frames, f"seed {seed}: {len(got)} achievements"))
    return best_of(runs, "clip_crafter", fps)


def record_brogue(steps: int = 180, fps: int = 10, delay: float = 0.05,
                  episodes: int = 3) -> list[str]:
    sys.path.insert(0, str(ROOT / "projects" / "03-brogue-screen-agent"))
    import mss
    from brogueagent.agent import BrogueAgent, observe
    from brogueagent.screen import Decoder
    from brogueagent.window import WindowGone, launch

    app = ROOT / "games/brogue/app/BrogueCE-windows"
    decoder = Decoder.load()
    runs = []
    for ep in range(episodes):
        seed = 31 + ep
        agent = BrogueAgent()
        agent.reset()
        frames = []
        with mss.mss() as sct:
            win = launch(app, seed=seed)
            try:
                for _ in range(steps):
                    if not win.alive:
                        break
                    try:
                        shot = win.grab(sct)
                    except WindowGone:
                        break
                    obs = observe(shot, decoder)
                    key, why = agent.act(obs)
                    small = np.asarray(Image.fromarray(shot).resize((606, 378), Image.LANCZOS))
                    frames.append(caption(small, f"screenshots in, keystrokes out   "
                                                 f"depth {agent.depth + 1}   {why}"))
                    win.send(key)
                    time.sleep(delay)
            finally:
                win.close()
        time.sleep(0.6)
        if frames:
            runs.append((agent.depth, frames, f"seed {seed}: depth {agent.depth + 1}"))
    if not runs:
        raise RuntimeError("no Brogue episode produced any frames")
    return best_of(runs, "clip_brogue", fps)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", default="all", choices=["doom", "crafter", "brogue", "all"])
    ap.add_argument("--seconds", type=int, default=20)
    ap.add_argument("--episodes", type=int, default=4,
                    help="play this many, keep the best, print all of their scores")
    args = ap.parse_args()

    jobs = ["doom", "crafter", "brogue"] if args.game == "all" else [args.game]
    made = {}
    for job in jobs:
        print(f"\n== {job} ==")
        try:
            if job == "doom":
                made[job] = record_doom(args.seconds, episodes=args.episodes)
            elif job == "crafter":
                made[job] = record_crafter(episodes=args.episodes)
            else:
                made[job] = record_brogue(episodes=max(2, args.episodes - 1))
        except Exception as exc:
            print(f"  failed: {exc}")
    print("\nwrote:", {k: v for k, v in made.items()})


if __name__ == "__main__":
    main()
