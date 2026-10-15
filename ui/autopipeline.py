"""Watch the training runs and finish each game the moment it is ready.

Training a game, filming its checkpoints, rebuilding the dashboard data and
re-checking the pages are four commands that always run in that order, so there
is no reason for a person to be the thing that runs them. This waits for each
run's `train_summary.json` to appear, films that game, re-exports, and carries
on to the next one.

    python ui/autopipeline.py --watch

Nothing here starts training; `arcade.train` does that. This only finishes what
training leaves behind, so it is safe to start at any point, including after
everything has already finished.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = ROOT / ".venv" / "Scripts" / "python.exe"
RUNS = ROOT / "runs_arcade"
MEDIA = ROOT / "docs" / "media"


def python() -> str:
    return str(PY) if PY.exists() else sys.executable


def run(args: list[str], label: str) -> bool:
    print(f"\n--- {label}", flush=True)
    proc = subprocess.run([python(), *args], cwd=str(ROOT),
                          env={**__import__("os").environ, "PYTHONUTF8": "1"})
    if proc.returncode != 0:
        print(f"    {label} failed with {proc.returncode}", flush=True)
    return proc.returncode == 0


def trained(game: str) -> bool:
    return (RUNS / game / "train_summary.json").exists()


def filmed(game: str) -> bool:
    return (MEDIA / game / "progress.mp4").exists() and (MEDIA / game / "ladder.json").exists()


def finish(game: str, episodes: int, max_steps: int) -> None:
    run(["-m", "arcade.progress", "--game", game, "--episodes", str(episodes),
         "--max-steps", str(max_steps)], f"filming {game}")
    run(["ui/export_arcade.py"], "exporting arcade data")
    run(["ui/check_page.py"], "checking the pages")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", nargs="*", default=None)
    ap.add_argument("--watch", action="store_true", help="keep waiting for runs to finish")
    ap.add_argument("--episodes", type=int, default=8)
    ap.add_argument("--max-steps", type=int, default=2500)
    ap.add_argument("--poll", type=int, default=60)
    ap.add_argument("--timeout-minutes", type=int, default=360)
    args = ap.parse_args()

    sys.path.insert(0, str(ROOT))
    from arcade.envs import CATALOGUE

    games = args.games or sorted(CATALOGUE)
    deadline = time.time() + args.timeout_minutes * 60
    done: set[str] = set()

    while True:
        for game in games:
            if game in done:
                continue
            if filmed(game):
                print(f"{game}: already filmed", flush=True)
                done.add(game)
                continue
            if trained(game):
                print(f"{game}: training finished, finishing the rest", flush=True)
                finish(game, args.episodes, args.max_steps)
                done.add(game)
        if len(done) == len(games) or not args.watch:
            break
        if time.time() > deadline:
            waiting = [g for g in games if g not in done]
            print(f"\ngave up waiting after {args.timeout_minutes} minutes; "
                  f"still unfinished: {waiting}", flush=True)
            break
        time.sleep(args.poll)

    summary = {}
    for game in games:
        ladder_path = MEDIA / game / "ladder.json"
        if ladder_path.exists():
            ladder = json.loads(ladder_path.read_text())["ladder"]
            first = next((r for r in ladder if r.get("steps") == 0), None)
            summary[game] = {"untrained": first["return_mean"] if first else None,
                             "trained": ladder[-1]["return_mean"],
                             "random": ladder[0]["return_mean"]}
    print("\n" + json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
