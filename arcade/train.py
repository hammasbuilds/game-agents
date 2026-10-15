"""Train one game from the arcade.

    python -m arcade.train --game boxing --steps 2000000 --envs 12
    python -m arcade.train --all

Checkpoints are written from step 0, so the before-and-after video exists the
moment training ends.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .envs import CATALOGUE
from .ppo import PPOConfig, train

ROOT = Path(__file__).resolve().parents[1]

# How long each game needs to show something a viewer can see, measured by
# throughput on this machine rather than guessed: the racing game runs at a
# quarter of the Atari pace because every agent step is four physics steps and a
# render.
BUDGET = {"boxing": 2_000_000, "platformer": 2_000_000, "racing": 800_000}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--game", choices=sorted(CATALOGUE))
    ap.add_argument("--all", action="store_true", help="train every game in turn")
    ap.add_argument("--steps", type=int, default=None)
    ap.add_argument("--envs", type=int, default=12)
    ap.add_argument("--width", type=int, default=1)
    ap.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    if not args.game and not args.all:
        ap.error("pass --game or --all")
    games = sorted(CATALOGUE) if args.all else [args.game]

    for key in games:
        game = CATALOGUE[key]
        steps = args.steps or BUDGET.get(key, 1_000_000)
        out = ROOT / "runs_arcade" / key
        cfg = PPOConfig(total_steps=steps, n_envs=args.envs, width=args.width,
                        device=args.device)
        print(f"\n=== {game.title} ({game.env_id}) : {steps:,} steps on "
              f"{args.envs} envs -> {out}", flush=True)
        summary = train(game, cfg, out, seed=args.seed)
        print(json.dumps({k: v for k, v in summary.items() if k != "checkpoints"},
                         indent=1))


if __name__ == "__main__":
    main()
