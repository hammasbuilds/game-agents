"""Assemble the per-game repository from this one.

    python -m ui.build_showcase --out ../game-playing-agents

`game-agents` is organised the way it was built: a shared arcade package, four
one-off projects, a protocol, a recorder. That is the right shape to work in and
the wrong shape to read. This writes the same work out as one folder per game,
numbered, each with its own README, its short demonstration and its comparison
still, so a reader can open folder 01 and see one game from end to end.

Every number in the generated READMEs is read from a run artefact — eval.json,
train_summary.json — and never typed here. A game whose evaluation has not been
run yet says so rather than carrying a stale figure.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


@dataclass
class Game:
    folder: str
    title: str
    game: str
    source: str                   # where the game itself comes from
    method: str
    code: list[str] = field(default_factory=list)   # paths copied from this repo
    eval_path: str | None = None
    train_path: str | None = None
    commands: list[str] = field(default_factory=list)
    notes: str = ""
    shared: bool = False          # runs on the shared arcade package


GAMES = [
    Game(folder="01-doom", title="DOOM, from pixels", game="DOOM (Freedoom data)",
         source="`vizdoom` on PyPI, which embeds the engine and ships Freedoom",
         method="PPO written out rather than imported, trained from raw frames on CPU",
         code=["projects/01-doom-pixel-rl"],
         eval_path="projects/01-doom-pixel-rl/runs/defend_the_center/eval.json",
         train_path="projects/01-doom-pixel-rl/runs/defend_the_center/train_summary.json",
         commands=["python -m doomagent.train --scenario defend_the_center",
                   "python evaluate.py --scenario defend_the_center --episodes 30",
                   "python film.py --scenario defend_the_center --resolution 640x480"],
         notes="Three maps, not one: defend the center, health gathering and "
               "deadly corridor. One map cannot tell *learned DOOM* from "
               "*learned one room*."),
    Game(folder="02-crafter", title="Crafter, planned", game="Crafter",
         source="`crafter` on PyPI",
         method="tile decoding into a map, then a goal ladder — no training at all",
         code=["projects/02-crafter-planner"],
         commands=["python evaluate.py --agent all --episodes 20",
                   "python film.py --seed 11 --length 350"],
         notes="The agent has no weights. It reads the 64×64 frame into a grid "
               "of named tiles and chooses a goal; the comparison is against a "
               "random agent on the same seed."),
    Game(folder="03-brogue", title="Brogue, through the screen", game="Brogue CE",
         source="the GPL release, fetched by `scripts/get_brogue.py`",
         method="screenshots in, keystrokes out — no API, no memory reading",
         code=["projects/03-brogue-screen-agent"],
         commands=["python play.py --seeds 1 2 3 4 5 --steps 300 --agent explorer",
                   "python film.py --seed 1"],
         notes="The one honest failure in the set: over 300 keystrokes the "
               "explorer does not descend more often than random keystrokes do."),
    Game(folder="04-walker", title="A robot learns to walk", game="MuJoCo Walker2d",
         source="`mujoco` and `gymnasium` on PyPI",
         method="PPO with a Gaussian policy — an action is a torque per joint",
         code=["projects/04-mujoco-walk"],
         eval_path="projects/04-mujoco-walk/runs/walker2d/eval.json",
         train_path="projects/04-mujoco-walk/runs/walker2d/train_summary.json",
         commands=["python -m walker.train --env Walker2d-v5 --steps 2000000",
                   "python evaluate.py --episodes 20",
                   "python film.py --seed 3"],
         notes="The only agent here whose actions are not buttons."),
    Game(folder="05-racing", title="Car racing", game="CarRacing-v3 (Box2D)",
         source="`gymnasium[box2d]` on PyPI",
         method="the shared arcade PPO: 84×84 greyscale, four stacked frames",
         eval_path="runs_arcade/racing/eval.json", shared=True,
         commands=["python -m arcade.train --game racing --steps 900000",
                   "python -m arcade.evaluate --game racing --episodes 12",
                   "python -m arcade.progress --game racing"]),
    Game(folder="06-boxing", title="Boxing (retired)", game="Atari 2600 Boxing",
         source="ROMs shipped under licence with `ale-py`",
         method="the shared arcade PPO", eval_path="runs_arcade/boxing/eval.json",
         shared=True,
         commands=["python -m arcade.train --game boxing",
                   "python -m arcade.evaluate --game boxing --episodes 20"],
         notes="Retired from the showcase for how the console looks at demo "
               "size, not for how the agent did. Its numbers are here."),
    Game(folder="07-kangaroo", title="Kangaroo (retired)", game="Atari 2600 Kangaroo",
         source="ROMs shipped under licence with `ale-py`",
         method="the shared arcade PPO", eval_path="runs_arcade/platformer/eval.json",
         shared=True,
         commands=["python -m arcade.train --game platformer",
                   "python -m arcade.evaluate --game platformer --episodes 20"],
         notes="A hard-exploration game: the reward needs a ladder climb and a "
               "punch in sequence, which random play almost never completes."),
    Game(folder="08-pong", title="Table tennis (retired)", game="Atari 2600 Pong",
         source="ROMs shipped under licence with `ale-py`",
         method="the shared arcade PPO", eval_path="runs_arcade/pingpong/eval.json",
         shared=True,
         commands=["python -m arcade.train --game pingpong",
                   "python -m arcade.evaluate --game pingpong --episodes 20"]),
]

SHARED = ["protocol.py", "film", "arcade", "requirements.txt"]


def read(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def scoreboard_row(game: Game) -> dict | None:
    """Crafter and Brogue keep their results in their own shapes.

    Neither is a checkpoint ladder — one trains nothing at all, the other is
    scored on descents per run — so the scoreboard already knows how to read
    them, and this asks it rather than parsing them a second time.
    """
    from ui.scoreboard import collect
    want = {"02-crafter": "02 · Crafter", "03-brogue": "03 · Brogue"}.get(game.folder)
    if not want:
        return None
    for row in collect():
        if row["project"] == want:
            return row
    return None


def result_lines(game: Game) -> tuple[str, str]:
    row = scoreboard_row(game)
    if row:
        bar = ("no error bar — " + row.get("note", "") if row["bar"] is None
               else f"a bar of {row['bar']:.2f}")
        extra = ""
        if row.get("achievements"):
            before, after = row["achievements"]
            extra = (os.linesep + f"Achievements unlocked: **{after}** against "
                     f"{before} for the random agent." + os.linesep)
        block = f"""### Result

| agent | {row['unit']} |
|---|---:|
| {row['baseline']} | {row['baseline_score']:,.2f} |
| **{row['agent']}** | **{row['agent_score']:,.2f}** |

*{row['episodes']} episodes, {row['protocol']}.*
{extra}
Gain **{row['gain']:+,.2f}** against {bar} — {row['verdict']}.
"""
        return (f"**{row['agent_score']:,.2f}** vs {row['baseline_score']:,.2f} "
                f"{row['unit']} — {row['verdict']}"), block

    """A one-line result for the index, and a block for the game's own README."""
    if not game.eval_path:
        return ("not scored under the protocol", "")
    data = read(ROOT / game.eval_path)
    if not data:
        return ("evaluation not run yet", "")

    # Two shapes of eval.json live in this repository: the protocol's, and the
    # older per-agent table DOOM writes. Both are real results; neither is
    # reshaped here to look like the other.
    if "verdict" in data and "best" in data:
        v, best, untrained = data["verdict"], data["best"], data["untrained"]
        rows = "\n".join(
            f"| {r['checkpoint'].replace('.pt', '')} | "
            f"{'—' if r.get('steps') is None else format(r['steps'], ',')} | "
            f"{r['return_mean']:,.2f} | {r['return_se']:.2f} |"
            for r in data["ladder"])
        block = f"""### Result

| checkpoint | steps | return | ± se |
|---|---:|---:|---:|
{rows}

*Scored on {len(data['select_seeds'])} selection episodes, the same ones for every row.*

Best: **{best['checkpoint'].replace('.pt', '')}**, re-scored on {len(data['report_seeds'])} held-out episodes: **{best['return_mean']:,.2f} ± {best['return_se']:.2f}** against **{untrained['return_mean']:,.2f} ± {untrained['return_se']:.2f}** untrained — {v['label']}, {v['gain']:+,.2f} against a bar of {v['bar']:.2f}.
"""
        if data.get("peaked_early"):
            block += (f"\nThis run peaked in the middle: it lost "
                      f"{data['decline_after_peak']:,.0f} return between its best "
                      f"checkpoint and the end of training.\n")
        summary = (f"**{best['return_mean']:,.0f}** vs {untrained['return_mean']:,.0f} "
                   f"untrained — {v['label']}")
        return summary, block

    if "rows" in data:
        import numpy as np
        by_agent = {r["agent"]: r for r in data["rows"]}
        ppo = by_agent.get("ppo-greedy")
        others = [r for n, r in by_agent.items() if "ppo" not in n]
        best = max(others, key=lambda r: r["return_mean"])
        se = lambda r: r["return_std"] / np.sqrt(r["episodes"])
        gain = ppo["return_mean"] - best["return_mean"]
        bar = 2 * float(np.hypot(se(ppo), se(best)))
        rows = "\n".join(
            f"| {r['agent']} | {r['return_mean']:,.2f} | {r['return_std']:.2f} | "
            f"{r['return_min']:,.1f} | {r['return_max']:,.1f} |"
            for r in data["rows"])
        block = f"""### Result

| agent | mean | sd | min | max |
|---|---:|---:|---:|---:|
{rows}

*{ppo['episodes']} held-out episodes, the same maps for every agent.*

Against the better baseline ({best['agent']}): **{gain:+,.2f}** with a bar of
**{bar:.2f}** — {"learned" if gain > bar else "inside noise"}.
"""
        return (f"**{ppo['return_mean']:,.2f}** vs {best['return_mean']:,.2f} "
                f"({best['agent']}) — {'learned' if gain > bar else 'inside noise'}"), block

    return ("evaluation not run yet", "")


def game_readme(game: Game, summary: str, block: str) -> str:
    commands = "\n".join(game.commands)
    shared = ("\nThe code is the shared `arcade/` package at the root of this "
              "repository: one network and one PPO across every arcade game, so "
              "the games differ and the method does not.\n" if game.shared else "")
    notes = f"\n{game.notes}\n" if game.notes else ""
    return f"""# {game.title}

**The game:** {game.game} — {game.source}.
**How the agent plays it:** {game.method}.
{notes}{shared}
![comparison](media/comparison.png)

*Untrained on the left, trained on the right, same episode. The labels carry the
scores measured at the resolution being filmed.*

[Eight-second demonstration](media/demo.mp4) · [as a gif](media/demo.gif)

{block}
### Running it

```bash
{commands}
```

Scored under [`protocol.py`](../protocol.py): the checkpoint ladder is scored on
one set of episodes, the best checkpoint is re-scored on a disjoint set, and a
gain counts only if it clears two standard errors of the difference.
"""


def index_readme(rows: list[tuple[Game, str]]) -> str:
    table = "\n".join(
        f"| {i + 1} | [{g.title}]({g.folder}/) | {g.game} | {g.method} | {summary} |"
        for i, (g, summary) in enumerate(rows))
    return f"""# Game playing agents

Eight games, each in its own folder, each with the agent that plays it, a short
demonstration and the numbers. Every game is a real one that was downloaded and
run unmodified — nothing here is a toy written for the occasion — and every
agent was trained on a laptop CPU.

| # | project | game | how it plays | result |
|---|---|---|---|---|
{table}

Open any folder: it has a comparison still, an eight-second clip, the result
with its error bar, and the commands that produced both.

## How every number here is measured

One file, [`protocol.py`](protocol.py), decides what the numbers mean:

1. **The last checkpoint is not the trained agent.** The ladder is scored and a
   checkpoint is chosen — one run here peaked in the middle and got worse.
2. **Choosing is itself a measurement**, so it uses its own episodes. The winner
   is re-scored on a disjoint set, and that second number is the one reported.
   Quoting the score that won the selection reports luck as skill.
3. **A gain counts only above two standard errors of the difference.** A gap
   smaller than its own uncertainty is not a win, and is not written up as one.

That is why a result in this repository is sometimes *inside noise* — the Brogue
agent's, for one. Those rows are printed beside the wins rather than dropped.

## Where the games come from

| game | what it is | where it comes from |
|---|---|---|
| DOOM | the 1993 engine with free Freedoom data | `vizdoom` (pip) |
| Crafter | an open-source survival game, 2021 | `crafter` (pip) |
| Brogue CE | a GPL roguelike, the real Windows build | release download |
| CarRacing | Gymnasium's Box2D racer | `gymnasium[box2d]` (pip) |
| Walker2d | a MuJoCo robot | `mujoco` (pip) |
| Boxing · Kangaroo · Pong | Atari 2600, 1977–1982 | ROMs shipped under licence with `ale-py` |

No commercial ROMs, nothing patched, nothing emulated by hand. The games
themselves are not committed here: each one is a package install or a download.

The three Atari games are kept with their numbers but retired from the
showcase — a 1980 console at 160×210 cannot be made to look good beside a
640×480 DOOM render, however well the agent plays.

Built from [game-agents](https://github.com/hammasbuilds/game-agents), which
holds the same work arranged by machinery rather than by game, plus the live
dashboard and the control panel.
"""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True)
    ap.add_argument("--no-code", action="store_true",
                    help="write the READMEs only, leaving the code alone")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    if not args.no_code:
        for name in SHARED:
            source = ROOT / name
            if not source.exists():
                continue
            target = out / name
            if source.is_dir():
                shutil.copytree(source, target, dirs_exist_ok=True,
                                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            else:
                shutil.copy2(source, target)
            print(f"  shared  {name}")

    index_rows = []
    for game in GAMES:
        folder = out / game.folder
        folder.mkdir(parents=True, exist_ok=True)
        if not args.no_code:
            for path in game.code:
                source = ROOT / path
                if source.exists():
                    shutil.copytree(source, folder, dirs_exist_ok=True,
                                    ignore=shutil.ignore_patterns(
                                        "__pycache__", "*.pyc", "runs", "*.pt",
                                        "*.npz", "_vizdoom*", "*.log"))
        summary, block = result_lines(game)
        (folder / "README.md").write_text(game_readme(game, summary, block),
                                          encoding="utf-8")
        index_rows.append((game, summary))
        print(f"  {game.folder:<12} {summary}")

    (out / "README.md").write_text(index_readme(index_rows), encoding="utf-8")
    print(f"\nwrote {out / 'README.md'}")


if __name__ == "__main__":
    main()
