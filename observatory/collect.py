"""Gather the state of every agent and every training run into one snapshot.

The dashboard in `docs/` is for a visitor: finished work, best foot forward. This
is the other thing — the view you want while runs are going: what is running,
how fast, how far along, when it will finish, and above all **whether it is
actually learning**.

That last question is the reason this exists rather than a log tail. Boxing
trained for 56 minutes and produced a curve that rose from −0.25 to 2.55, which
reads as progress until you score the untrained network and find it already at
2.12. So every run here is judged against two things it is easy to skip: the
untrained network, and the spread of its own evaluation. A run whose improvement
is smaller than its own error bars is reported as `inside noise`, not as a win.

    python -m observatory.collect              # one snapshot
    python -m observatory.collect --watch 30   # keep it fresh every 30 seconds
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "observatory" / "data"
STALE_AFTER = 300  # seconds without a log write before a running job looks stuck


def read(path: Path):
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None


def age_seconds(path: Path) -> float | None:
    try:
        return time.time() - path.stat().st_mtime
    except OSError:
        return None


def tail(path: Path, lines: int = 12) -> list[str]:
    try:
        text = path.read_text(errors="replace").splitlines()
    except OSError:
        return []
    return [line for line in text[-lines:] if line.strip()]


def thin(history: list[dict], keep: int = 120) -> list[dict]:
    rows = [r for r in history if r.get("return_mean") is not None]
    if not rows:
        return []
    stride = max(1, len(rows) // keep)
    out = rows[::stride]
    if out[-1] is not rows[-1]:
        out.append(rows[-1])
    return [{"steps": r["steps"], "return": round(r["return_mean"], 3),
             "entropy": r.get("entropy"), "sps": r.get("sps"),
             "value_loss": r.get("value_loss")} for r in out]


@dataclass
class Verdict:
    """What the numbers support saying about a run."""

    label: str
    detail: str


def judge(ladder: list[dict] | None) -> Verdict | None:
    """Did this run learn anything the evaluation can actually see?

    The comparison is the trained checkpoint against the untrained one, and the
    bar is the two spreads added: if the gain is smaller than that, the ladder
    cannot tell them apart and neither can we.
    """
    if not ladder:
        return None
    untrained = next((r for r in ladder if r.get("steps") == 0), None)
    trained = ladder[-1]
    if untrained is None or trained is untrained:
        return None
    gain = trained["return_mean"] - untrained["return_mean"]
    noise = (untrained.get("return_std") or 0) + (trained.get("return_std") or 0)
    episodes = trained.get("episodes") or 0
    if gain > noise:
        return Verdict("learned", f"{gain:+.1f} against a combined spread of {noise:.1f} "
                                  f"over {episodes} episodes")
    if gain > 0:
        return Verdict("inside noise", f"{gain:+.1f} is smaller than the combined spread "
                                       f"of {noise:.1f}, so the run cannot claim it")
    return Verdict("no gain", f"{gain:+.1f} against the untrained network over "
                              f"{episodes} episodes")


def arcade_runs() -> list[dict]:
    import sys
    sys.path.insert(0, str(ROOT))
    from arcade.envs import CATALOGUE

    runs = []
    for key, game in CATALOGUE.items():
        run_dir = ROOT / "runs_arcade" / key
        history = read(run_dir / "history.json") or []
        summary = read(run_dir / "train_summary.json")
        checkpoints = read(run_dir / "checkpoints.json") or []
        ladder_blob = read(ROOT / "docs" / "media" / key / "ladder.json")
        ladder = (ladder_blob or {}).get("ladder")
        logs = sorted(ROOT.glob(f"runs_arcade/train_{key}*.log")) + \
            sorted(ROOT.glob("runs_arcade/train_all.log"))
        log = logs[0] if logs else None
        last = history[-1] if history else None

        total = (summary or {}).get("steps")
        if not total and last:
            # Mid-run: the budget is in the trainer, so infer from the log line.
            total = None
        state = "finished" if summary else ("running" if history else "not started")
        idle = age_seconds(run_dir / "history.json") if history else None
        if state == "running" and idle is not None and idle > STALE_AFTER:
            state = "stalled"

        eta = None
        if state == "running" and last and last.get("sps"):
            budget = {"boxing": 2_000_000, "platformer": 2_000_000,
                      "racing": 1_200_000, "pingpong": 2_000_000}.get(key)
            if budget and last["steps"] < budget:
                eta = round((budget - last["steps"]) / last["sps"] / 60, 1)

        runs.append({
            "kind": "arcade",
            "key": key,
            "title": game.title,
            "env_id": game.env_id,
            "blurb": game.blurb,
            "state": state,
            "steps": last["steps"] if last else 0,
            "updates": len(history),
            "sps": last.get("sps") if last else None,
            "return_now": round(last["return_mean"], 2) if last and last.get("return_mean") is not None else None,
            "entropy_now": last.get("entropy") if last else None,
            "wall_minutes": round(summary["wall_seconds"] / 60, 1) if summary else None,
            "params": (summary or {}).get("params"),
            "eta_minutes": eta,
            "seconds_since_update": round(idle) if idle is not None else None,
            "checkpoints": [{"tag": c["tag"], "steps": c["steps"]} for c in checkpoints],
            "curve": thin(history),
            "ladder": ladder,
            "verdict": (lambda v: {"label": v.label, "detail": v.detail} if v else None)(judge(ladder)),
            "clips": sorted(p.name for p in (ROOT / "docs" / "media" / key).glob("*.mp4"))
            if (ROOT / "docs" / "media" / key).exists() else [],
            "log_tail": tail(log) if log else [],
        })
    return runs


def project_runs() -> list[dict]:
    """The three hand-built agents, which are scored rather than trained on a curve."""
    out = []

    doom_eval = read(ROOT / "projects/01-doom-pixel-rl/runs/defend_the_center/eval.json")
    doom_train = read(ROOT / "projects/01-doom-pixel-rl/runs/defend_the_center/train_summary.json")
    if doom_eval or doom_train:
        rows = (doom_eval or {}).get("rows", [])
        best = max((r["return_mean"] for r in rows if r["agent"].startswith("ppo")), default=None)
        floor = next((r["return_mean"] for r in rows if r["agent"] == "spray"), None)
        out.append({
            "kind": "project", "key": "doom", "title": "DOOM from pixels",
            "env_id": "ViZDoom defend_the_center", "state": "finished",
            "headline": f"{best:.2f} kills" if best is not None else None,
            "baseline": f"{floor:.2f} scripted" if floor is not None else None,
            "detail": f"{(doom_train or {}).get('steps', 0):,} steps, "
                      f"{round((doom_train or {}).get('wall_seconds', 0) / 60)} min CPU",
            "rows": [{"agent": r["agent"], "mean": r["return_mean"], "std": r["return_std"]}
                     for r in rows],
        })

    crafter = read(ROOT / "projects/02-crafter-planner/runs/ab_new.json") or \
        read(ROOT / "projects/02-crafter-planner/runs/eval_all.json")
    if crafter:
        rows = crafter if isinstance(crafter, list) else [crafter]
        planner = next((r for r in rows if r.get("agent") == "planner"), rows[0])
        out.append({
            "kind": "project", "key": "crafter", "title": "Crafter planner",
            "env_id": "Crafter", "state": "finished",
            "headline": f"{planner['score']}% score",
            "baseline": "1.13% random",
            "detail": f"{planner['distinct_achievements']}/22 achievements over "
                      f"{planner['episodes']} episodes, no training at all",
            "rows": [{"agent": r["agent"], "mean": r["score"], "std": None} for r in rows],
        })

    brogue = read(ROOT / "projects/03-brogue-screen-agent/runs/play_long.json")
    if brogue:
        rows = []
        for agent in brogue.get("agents", []):
            eps = agent.get("episodes", [])
            if eps:
                mean = sum(e["descents"] for e in eps) / len(eps)
                rows.append({"agent": agent["agent"], "mean": round(mean, 2), "std": None})
        explorer = next((r for r in rows if r["agent"] == "explorer"), None)
        random_row = next((r for r in rows if r["agent"] == "random"), None)
        out.append({
            "kind": "project", "key": "brogue", "title": "Brogue, screen-driven",
            "env_id": "Brogue CE", "state": "finished",
            "headline": f"{explorer['mean']} descents/game" if explorer else None,
            "baseline": f"{random_row['mean']} random keys" if random_row else None,
            "detail": "screenshots in, keystrokes out, no API",
            "rows": rows,
        })
    return out


def machine() -> dict:
    """What the box is doing, so a slow run has somewhere to point."""
    info = {"cpu_percent": None, "python_processes": None, "gpu": None}
    try:
        out = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "(Get-Counter '\\Processor(_Total)\\% Processor Time').CounterSamples.CookedValue; "
             "(Get-Process python -ErrorAction SilentlyContinue).Count"],
            capture_output=True, text=True, timeout=30).stdout.split()
        if out:
            info["cpu_percent"] = round(float(out[0]), 1)
        if len(out) > 1:
            info["python_processes"] = int(out[1])
    except Exception:
        pass
    try:
        gpu = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.used,memory.total,utilization.gpu",
             "--format=csv,noheader"], capture_output=True, text=True, timeout=30).stdout.strip()
        if gpu:
            name, used, total, util = [p.strip() for p in gpu.split(",")]
            info["gpu"] = {"name": name, "memory_used": used, "memory_total": total,
                           "utilisation": util}
    except Exception:
        pass
    return info


def snapshot() -> dict:
    return {
        "taken_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ"),
        "arcade": arcade_runs(),
        "projects": project_runs(),
        "machine": machine(),
    }


def write(data: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "snapshot.json").write_text(json.dumps(data, indent=1))
    (OUT / "snapshot.js").write_text("window.SNAPSHOT = " + json.dumps(data, indent=1) + ";\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--watch", type=int, default=0, metavar="SECONDS",
                    help="keep refreshing the snapshot this often")
    args = ap.parse_args()
    while True:
        data = snapshot()
        write(data)
        running = [r["key"] for r in data["arcade"] if r["state"] in ("running", "stalled")]
        print(f"{data['taken_at']}  arcade={len(data['arcade'])} "
              f"projects={len(data['projects'])} running={running or 'none'}", flush=True)
        if not args.watch:
            return
        time.sleep(args.watch)


if __name__ == "__main__":
    main()
