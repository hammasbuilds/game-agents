"""Record the untrained robot and the trained one walking the same episode.

    python film.py --env Walker2d-v5 --seed 3

MuJoCo renders at whatever size it is asked for, so there is no reason for this
film to be small. The policy sees a vector of joint angles either way — the
camera and the agent share nothing here, which is exactly the point the DOOM
work had to be rebuilt to achieve.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import gymnasium as gym
import numpy as np
import torch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT))

from film import side_by_side, write_clip                        # noqa: E402
from walker.policy import GaussianActorCritic, RunningNorm       # noqa: E402


def load(path: Path):
    state = torch.load(path, map_location="cpu", weights_only=False)
    model = GaussianActorCritic(state["obs_dim"], state["act_dim"])
    model.load_state_dict(state["model"])
    model.eval()
    norm = RunningNorm((state["obs_dim"],))
    # The normaliser travels with the weights. A policy restored without it
    # reads its inputs in different units from the ones it trained on, which
    # looks exactly like a policy that forgot how to walk.
    norm.load_state_dict(state["norm"])
    return model, norm, state


def record(model, norm, env_id: str, seed: int, size: int, max_steps: int = 1000):
    env = gym.make(env_id, render_mode="rgb_array", width=size, height=size)
    obs, _ = env.reset(seed=seed)
    frames, total, steps = [env.render()], 0.0, 0
    while steps < max_steps:
        if model is None:
            action = env.action_space.sample()
        else:
            with torch.no_grad():
                action, _, _ = model.act(torch.from_numpy(norm(obs[None])), greedy=True)
            action = action[0]
        obs, reward, terminated, truncated, _ = env.step(
            np.clip(action, env.action_space.low, env.action_space.high))
        total += float(reward)
        steps += 1
        frames.append(env.render())
        if terminated or truncated:
            break
    env.close()
    return frames, total, steps


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--env", default="Walker2d-v5")
    ap.add_argument("--run", default=None)
    ap.add_argument("--seed", type=int, default=3)
    ap.add_argument("--size", type=int, default=480, help="render size, not agent input")
    ap.add_argument("--width", type=int, default=420, help="panel width in the film")
    ap.add_argument("--fps", type=int, default=25)
    ap.add_argument("--gif-width", type=int, default=340, dest="gif_width")
    ap.add_argument("--gif-frames", type=int, default=60, dest="gif_frames")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    run = Path(args.run or HERE / "runs" / args.env.split("-")[0].lower())
    untrained_path = run / "ckpt_000.pt"
    trained_path = run / "policy.pt"

    strips = []
    for label, path in (("untrained", untrained_path), ("trained (PPO)", trained_path)):
        model, norm, state = load(path)
        frames, total, steps = record(model, norm, args.env, args.seed, args.size)
        print(f"  {label:<14} return {total:>8.1f} over {steps} steps "
              f"({state['step']:,} training steps)", flush=True)
        strips.append((label, f"{args.env} · return {total:.0f} · {steps} steps", frames))

    out = Path(args.out or ROOT / "docs" / "media" / "walker"
               / f"{args.env.split('-')[0].lower()}.mp4")
    frames = side_by_side(strips, width=args.width)
    print(f"\n{len(frames)} frames at {frames[0].shape[1]}x{frames[0].shape[0]}")
    write_clip(frames, out, fps=args.fps, gif=True,
               gif_width=args.gif_width, gif_max_frames=args.gif_frames)


if __name__ == "__main__":
    main()
