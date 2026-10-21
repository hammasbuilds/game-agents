"""Copy the shared trainer, film code and protocol into game-playing-agents.

    python scripts/sync_shared.py --check     # say what has drifted, change nothing
    python scripts/sync_shared.py             # copy, and say what changed

game-playing-agents presents the same eight runs as eight readable folders, and
to be runnable it carries a copy of `arcade/`, `film/` and `protocol.py`. A copy
drifts: within a day of making it, three files there were a version behind,
because `obs_shape()` learned to ask the game and `VecArcade` stopped assuming
84x84 here and not there. Nothing broke loudly -- the older copy still imported
and still trained -- which is exactly why it needed a command rather than
good intentions.

This is the one direction that is ever correct: game-agents is where the shared
code is edited, and game-playing-agents receives it. Anything edited only in the
copy is reported as a difference and then overwritten, so it does not survive
unnoticed.
"""
from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIBLING = ROOT.parent / "game-playing-agents"

SHARED = ["protocol.py", "film/__init__.py", "film/record.py"] + [
    f"arcade/{name}" for name in (
        "__init__.py", "README.md", "crafter_env.py", "envs.py", "evaluate.py",
        "model.py", "play.py", "ppo.py", "progress.py", "reel.py", "sweep.py",
        "train.py", "vec.py")]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="report drift and exit non-zero, without copying")
    ap.add_argument("--into", default=str(SIBLING))
    args = ap.parse_args()

    into = Path(args.into)
    if not into.is_dir():
        raise SystemExit(f"{into} is not a directory")

    same, drifted, absent = [], [], []
    for rel in SHARED:
        source = ROOT / rel
        if not source.exists():
            raise SystemExit(f"{source} is missing from this repository")
        target = into / rel
        if not target.exists():
            absent.append(rel)
        elif filecmp.cmp(source, target, shallow=False):
            same.append(rel)
        else:
            drifted.append(rel)

    for rel in drifted:
        print(f"  differs  {rel}")
    for rel in absent:
        print(f"  missing  {rel}")
    print(f"\n{len(same)} identical, {len(drifted)} different, {len(absent)} missing")

    if args.check:
        if drifted or absent:
            print("\nRun without --check to copy them over.")
            sys.exit(1)
        print("the copy matches this repository")
        return

    for rel in drifted + absent:
        target = into / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, target)
    print(f"copied {len(drifted) + len(absent)} file(s) into {into}"
          if drifted or absent else "nothing to copy")


if __name__ == "__main__":
    main()
