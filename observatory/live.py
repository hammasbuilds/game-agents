"""Open a game in a window and let the agent play it, now, while you watch.

    python -m observatory.live --game racing
    python -m observatory.live --game doom
    python -m observatory.live --game brogue

This is the "show me" path rather than the "measure it" path: it opens the real
game window and drives it with the best checkpoint that exists, so there is
something to watch rather than a file to open afterwards. It picks the latest
checkpoint on disk, which means it also works *during* training — start it on a
run that is an hour in and you see what an hour bought.
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def latest_checkpoint(game: str) -> Path | None:
    run = ROOT / "runs_arcade" / game
    saved = sorted(run.glob("ckpt_*.pt"))
    return saved[-1] if saved else None


def play_arcade(game: str, episodes: int, checkpoint: Path | None) -> None:
    import gymnasium as gym
    import numpy as np
    import torch

    sys.path.insert(0, str(ROOT))
    from arcade.envs import CATALOGUE, FRAME_H, FRAME_W, STACK, make
    from arcade.model import ActorCritic
    from arcade.play import load

    spec = CATALOGUE[game]
    checkpoint = checkpoint or latest_checkpoint(game)
    if checkpoint is None:
        raise SystemExit(f"no checkpoint for {game} yet — train it first")
    model, _, blob = load(checkpoint)
    print(f"{spec.title}: playing with {checkpoint.name} "
          f"({blob.get('step', 0):,} steps of training)", flush=True)

    # A human-rendered env draws its own window; the wrapped copy is what the
    # policy reads. Both step together so the picture matches the decision.
    shown = gym.make(spec.env_id, render_mode="human", **spec.kwargs)
    wrapped = make(spec)
    try:
        for episode in range(episodes):
            obs, _ = wrapped.reset(seed=1000 + episode)
            shown.reset(seed=1000 + episode)
            total = 0.0
            for _ in range(6000):
                stacked = torch.from_numpy(np.asarray(obs, dtype=np.uint8)[None])
                action, _, _ = model.act(stacked)
                a = int(action[0])
                obs, reward, terminated, truncated, _ = wrapped.step(a)
                # The shown copy may use a different frame skip, so it is stepped
                # the matching number of times rather than once.
                for _ in range(4):
                    _, _, t2, tr2, _ = shown.step(a)
                    if t2 or tr2:
                        break
                total += float(reward)
                if terminated or truncated:
                    break
            print(f"  episode {episode + 1}: {total:.1f}", flush=True)
    finally:
        shown.close()
        wrapped.close()


def play_doom(episodes: int) -> None:
    sys.path.insert(0, str(ROOT / "projects" / "01-doom-pixel-rl"))
    import numpy as np
    import torch
    from doomagent.env import DoomEnv, EnvConfig
    from doomagent.model import ActorCritic

    weights = ROOT / "projects/01-doom-pixel-rl/runs/defend_the_center/policy.pt"
    if not weights.exists():
        raise SystemExit("no DOOM policy on disk yet")
    blob = torch.load(weights, map_location="cpu", weights_only=False)
    model = ActorCritic(tuple(blob["obs_shape"]), blob["n_actions"],
                        width=int(blob.get("width", 1)))
    model.load_state_dict(blob["model"])
    model.eval()
    print("DOOM: playing with the trained policy", flush=True)
    for episode in range(episodes):
        env = DoomEnv(EnvConfig(scenario="defend_the_center", seed=900100 + episode,
                                window=True))
        try:
            obs = env.reset()
            while True:
                action, _, _ = model.act(torch.from_numpy(np.ascontiguousarray(obs[None])),
                                         greedy=True)
                obs, _, done = env.step(int(action[0]))
                time.sleep(0.02)   # the window is for a person, not a benchmark
                if done:
                    break
            print(f"  episode {episode + 1}: {env.episode_return():.0f} kills", flush=True)
        finally:
            env.close()


def play_brogue(steps: int) -> None:
    sys.path.insert(0, str(ROOT / "projects" / "03-brogue-screen-agent"))
    import mss
    from brogueagent.agent import BrogueAgent, observe
    from brogueagent.screen import Decoder
    from brogueagent.window import WindowGone, launch

    app = ROOT / "games/brogue/app/BrogueCE-windows"
    if not (app / "brogue.exe").exists():
        raise SystemExit("Brogue is not downloaded — run scripts/get_brogue.py")
    decoder = Decoder.load()
    agent = BrogueAgent()
    agent.reset()
    print("Brogue: the game window is the agent's only input", flush=True)
    with mss.mss() as sct:
        win = launch(app, seed=int(time.time()) % 100000)
        try:
            for step in range(steps):
                if not win.alive:
                    break
                try:
                    frame = win.grab(sct)
                except WindowGone:
                    break
                key, why = agent.act(observe(frame, decoder))
                win.send(key)
                if step % 50 == 0:
                    print(f"  step {step}: depth {agent.depth + 1}, {why}", flush=True)
                time.sleep(0.06)
        finally:
            win.close()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", required=True)
    ap.add_argument("--episodes", type=int, default=3)
    ap.add_argument("--steps", type=int, default=600, help="brogue only")
    ap.add_argument("--checkpoint", default=None)
    args = ap.parse_args()

    if args.game == "doom":
        play_doom(args.episodes)
    elif args.game == "brogue":
        play_brogue(args.steps)
    else:
        play_arcade(args.game, args.episodes,
                    Path(args.checkpoint) if args.checkpoint else None)


if __name__ == "__main__":
    main()
