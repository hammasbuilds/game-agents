"""One table of every result in the repository, with how each was measured.

    python -m ui.scoreboard

Each project writes its own `eval.json` and each has its own units — kills,
ticks survived, metres of road, Crafter score. A reader cannot compare those
numbers and should not try. What they can compare is the *shape* of each claim:
what the agent was measured against, over how many episodes, and whether the gap
is bigger than the uncertainty of the difference.

So this collects one row per agent and records, per row, which protocol produced
it. Rows scored under `protocol.py` say so and carry their selection and
reporting seed counts; rows from an earlier evaluation say that instead of
pretending otherwise.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

DATA = ROOT / "docs" / "data"


def read(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def bar_verdict(gain: float, bar: float, baseline_label: str = "the baseline") -> str:
    if gain > bar:
        return "learned"
    if gain < -bar:
        return f"worse than {baseline_label}"
    return "inside noise"


def row(project, game, agent, baseline, agent_mean, baseline_mean, se_a, se_b,
        episodes, unit, protocol, note=None, **extra) -> dict:
    gain = agent_mean - baseline_mean
    # A missing error bar is not a bar of zero. Treating it as zero makes every
    # gap clear it, which is the denominator doing the work: the Crafter score
    # is a geometric mean over achievement rates and has no standard error, so
    # its row says that instead of claiming a win it cannot support.
    measurable = se_a is not None and se_b is not None
    bar = 2 * float(np.hypot(se_a, se_b)) if measurable else None
    out = {
        "project": project, "game": game, "agent": agent, "baseline": baseline,
        "agent_score": round(float(agent_mean), 2),
        "baseline_score": round(float(baseline_mean), 2),
        "gain": round(gain, 2), "bar": round(bar, 2) if measurable else None,
        "verdict": bar_verdict(gain, bar, baseline) if measurable else "no error bar",
        "episodes": episodes, "unit": unit, "protocol": protocol,
    }
    if note:
        out["note"] = note
    out.update(extra)
    return out


def collect() -> list[dict]:
    rows: list[dict] = []

    # -- DOOM: one row per scenario -----------------------------------------
    for run_dir in sorted((ROOT / "projects/01-doom-pixel-rl/runs").glob("*")):
        data = read(run_dir / "eval.json")
        if not data or "rows" not in data:
            continue
        by_agent = {r["agent"]: r for r in data["rows"]}
        ppo = by_agent.get("ppo-greedy")
        if not ppo:
            continue
        baselines = [r for name, r in by_agent.items() if "ppo" not in name]
        if not baselines:
            continue
        best = max(baselines, key=lambda r: r["return_mean"])
        se = lambda r: r["return_std"] / np.sqrt(r["episodes"])
        rows.append(row(
            "01 · DOOM", run_dir.name.replace("_", " "), "PPO (greedy)", best["agent"],
            ppo["return_mean"], best["return_mean"], se(ppo), se(best),
            ppo["episodes"],
            {"defend_the_center": "kills", "health_gathering": "ticks survived"}
            .get(run_dir.name, "reward"),
            "held-out episodes, same seeds for every agent; final checkpoint"))

    # -- Crafter -------------------------------------------------------------
    crafter = read(ROOT / "projects/02-crafter-planner/runs/eval_all.json")
    if crafter:
        agents = {a["agent"]: a for a in crafter}
        planner, random_agent = agents.get("planner"), agents.get("random")
        if planner and random_agent:
            # The Crafter score is the official metric: the geometric mean of
            # achievement success rates. It is not a mean over episodes, so it
            # has no standard error, and saying so is better than inventing one.
            rows.append(row(
                "02 · Crafter", "Crafter", "planner (no training)", "random",
                planner["score"], random_agent["score"], None, None,
                planner["episodes"], "Crafter score (%)",
                "geometric mean of achievement rates over fixed episodes",
                note="no error bar: the Crafter score is a geometric mean over "
                     "achievement rates, not a mean over episodes",
                reward=[random_agent["reward_mean"], planner["reward_mean"]],
                achievements=[random_agent["distinct_achievements"],
                              planner["distinct_achievements"]]))

    # -- Brogue --------------------------------------------------------------
    # Two files, because the explorer was re-run on its own later. The random
    # agent only exists in the first one, and a comparison needs both -- so the
    # agents are merged, newest wins, rather than reading whichever file happens
    # to be named first.
    by_name = {}
    for name in ("play.json", "play_explorer.json"):
        data = read(ROOT / "projects/03-brogue-screen-agent/runs" / name)
        for agent in (data or {}).get("agents", []):
            by_name[agent["agent"]] = agent
    if by_name:
        explorer, random_agent = by_name.get("explorer"), by_name.get("random")
        if explorer and random_agent:
            def descents(agent):
                values = [float(e["descents"]) for e in agent["episodes"]]
                return float(np.mean(values)), float(np.std(values, ddof=1) /
                                                     np.sqrt(len(values))) if len(values) > 1 else 0.0
            a_mean, a_se = descents(explorer)
            b_mean, b_se = descents(random_agent)
            rows.append(row(
                "03 · Brogue", "Brogue CE", "explorer (screen-driven)", "random keystrokes",
                a_mean, b_mean, a_se, b_se, len(explorer["episodes"]),
                "descents in 300 keystrokes",
                "fixed seeds, same dungeon for both agents",
                note="300 keystrokes is a short run: this is a floor on what the "
                     "agent can do, not a ceiling"))

    # -- the walking robot ---------------------------------------------------
    for run_dir in sorted((ROOT / "projects/04-mujoco-walk/runs").glob("*")):
        data = read(run_dir / "eval.json")
        if not data or "verdict" not in data:
            continue
        v, best, untrained = data["verdict"], data["best"], data["untrained"]
        rows.append(row(
            "04 · Walking", data.get("env_id", run_dir.name), "PPO (best checkpoint)",
            "untrained network", best["return_mean"], untrained["return_mean"],
            best["return_se"], untrained["return_se"], best["episodes"], "return",
            f"protocol.py — ladder on {len(data['select_seeds'])} selection episodes, "
            f"winner re-scored on {len(data['report_seeds'])} held out",
            peaked_early=data.get("peaked_early"),
            decline_after_peak=data.get("decline_after_peak")))

    # -- the arcade ----------------------------------------------------------
    for run_dir in sorted((ROOT / "runs_arcade").glob("*")):
        data = read(run_dir / "eval.json")
        if not data or "verdict" not in data:
            continue
        v, best, untrained = data["verdict"], data["best"], data["untrained"]
        rows.append(row(
            "arcade", data.get("game", run_dir.name), "PPO (best checkpoint)",
            untrained["checkpoint"].replace(".pt", ""),
            best["return_mean"], untrained["return_mean"],
            best["return_se"], untrained["return_se"], best["episodes"], "episode return",
            f"protocol.py — ladder on {len(data['select_seeds'])} selection episodes, "
            f"winner re-scored on {len(data['report_seeds'])} held out",
            peaked_early=data.get("peaked_early"),
            decline_after_peak=data.get("decline_after_peak")))

    return rows


def rounds() -> list[dict]:
    """The round log, oldest first.

    It is a .jsonl because it is only ever appended to: a round whose numbers
    came out badly stays in the file, and that is the whole point of keeping it.
    """
    path = DATA / "rounds.jsonl"
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def main() -> None:
    rows = collect()
    DATA.mkdir(parents=True, exist_ok=True)
    payload = {"rows": rows, "rounds": rounds()}
    (DATA / "scoreboard.json").write_text(json.dumps(payload, indent=1), encoding="utf-8")
    (DATA / "scoreboard.js").write_text(
        "window.SCOREBOARD = " + json.dumps(payload, indent=1) + ";\n", encoding="utf-8")

    width = max((len(r["project"]) for r in rows), default=10)
    for r in rows:
        print(f"  {r['project']:<{width}}  {r['game']:<20} "
              f"{r['agent_score']:>10,.2f} vs {r['baseline_score']:>9,.2f} "
              f"{r['unit']:<16} {r['verdict']}")
    print(f"\n{len(rows)} rows and {len(payload['rounds'])} rounds -> "
          f"{(DATA / 'scoreboard.json').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
