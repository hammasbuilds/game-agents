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


PROGRESS = re.compile(r"^(u\d+/|checkpoint |=== |\{)")


def tail(path: Path, lines: int = 12) -> list[str]:
    """The last few lines that say something about progress.

    A raw tail shows whatever the process said last, which after a batch is
    killed is a stack trace about a closed pipe -- true, but not what the run
    did. Progress lines are preferred and the raw tail is the fallback.
    """
    try:
        text = [l for l in path.read_text(errors="replace").splitlines() if l.strip()]
    except OSError:
        return []
    progress = [l for l in text if PROGRESS.match(l)]
    return (progress or text)[-lines:]


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

    The comparison is the trained checkpoint against the untrained one. The bar
    is twice the standard error of the difference between the two means -- very
    roughly a 95% interval -- and *not* the sum of the two standard deviations,
    which is what this first did.

    That distinction is the whole correctness of the column. A standard deviation
    describes how much one episode differs from another; the standard error
    describes how well the mean is pinned down, and it shrinks with the square
    root of the episode count. Using the deviations, Pong's +3.4 was declared
    'inside noise' against a bar of 3.9 even though its training curve had
    climbed from -21 to -14 over a hundred episodes. With the standard errors the
    bar is 2.1, and Pong reads as learned while Boxing still reads as no gain --
    which is what the curves say in both cases.
    """
    if not ladder:
        return None
    untrained = next((r for r in ladder if r.get("steps") == 0), None)
    trained = ladder[-1]
    if untrained is None or trained is untrained:
        return None
    gain = trained["return_mean"] - untrained["return_mean"]
    n_a = max(1, untrained.get("episodes") or 1)
    n_b = max(1, trained.get("episodes") or 1)
    se_a = (untrained.get("return_std") or 0) / (n_a ** 0.5)
    se_b = (trained.get("return_std") or 0) / (n_b ** 0.5)
    bar = 2 * ((se_a ** 2 + se_b ** 2) ** 0.5)
    detail = (f"{gain:+.1f} against a bar of {bar:.1f}, which is two standard errors "
              f"of the difference over {n_b} episodes a side")
    if gain > bar:
        return Verdict("learned", detail)
    if gain > 0:
        return Verdict("inside noise", detail + " — too small to claim")
    return Verdict("no gain", detail)


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
        # A run writes history every ten updates, so between launching and its
        # first write there is a window -- minutes, for the slower games -- where
        # the files say "nothing here" and the truth is "warming up". Reporting
        # that as 'not started' is exactly the kind of lie an operational view
        # must not tell, so the log's own freshness is consulted too.
        log_age = age_seconds(log) if log else None
        starting = (log_age is not None and log_age < STALE_AFTER
                    and (run_dir / "ckpt_000.pt").exists())
        if summary:
            state = "finished"
        elif history:
            state = "running"
        elif starting:
            state = "starting"
        else:
            state = "not started"
        idle = age_seconds(run_dir / "history.json") if history else log_age
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
            "media_dir": f"../docs/media/{key}",
            "clips": sorted(p.name for p in (ROOT / "docs" / "media" / key).glob("*.mp4"))
            if (ROOT / "docs" / "media" / key).exists() else [],
            "gifs": sorted(p.name for p in (ROOT / "docs" / "media" / key).glob("*.gif"))
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


def analytics() -> dict:
    """Everything the analytics view needs, read from the same run artefacts.

    This is deliberately not a second copy of the numbers: each entry points at
    the file some run wrote, so a figure here cannot drift away from the run that
    produced it.
    """
    media = ROOT / "docs" / "media"
    doom_eval = read(ROOT / "projects/01-doom-pixel-rl/runs/defend_the_center/eval.json")
    doom_hist = read(ROOT / "projects/01-doom-pixel-rl/runs/defend_the_center/history.json") or []
    crafter_ab = read(ROOT / "projects/02-crafter-planner/runs/ab_new.json")
    crafter_all = read(ROOT / "projects/02-crafter-planner/runs/eval_all.json")
    crafter_perception = read(ROOT / "projects/02-crafter-planner/runs/perception.json")
    brogue_long = read(ROOT / "projects/03-brogue-screen-agent/runs/play_long.json")
    iterations = read(ROOT / "docs" / "data" / "iterations.json")
    kaggle = read(ROOT / "projects/01-doom-pixel-rl/runs_kaggle/width_comparison.json")

    doom_curve = [{"steps": r["steps"], "return": round(r["return_mean"], 2)}
                  for r in doom_hist[::4] if r.get("return_mean") is not None]
    brogue_rows = []
    for agent in (brogue_long or {}).get("agents", []):
        for e in agent.get("episodes", []):
            brogue_rows.append({"agent": agent["agent"], "seed": e["seed"],
                                "descents": e["descents"],
                                "coverage": e.get("coverage_mean"),
                                "health": e.get("health_final")})

    return {
        "doom": {"rows": (doom_eval or {}).get("rows"), "curve": doom_curve, "kaggle": kaggle},
        "crafter": {"ab": crafter_ab, "all": crafter_all, "perception": crafter_perception},
        "brogue": {"episodes": brogue_rows},
        "iterations": iterations,
        "project_clips": sorted(p.name for p in media.glob("clip_*.mp4")) if media.exists() else [],
        "media_dir": "../docs/media",
    }


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
        "analytics": analytics(),
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
        running = [f"{r['key']}:{r['state']}" for r in data["arcade"]
                   if r["state"] in ("running", "starting", "stalled")]
        print(f"{data['taken_at']}  arcade={len(data['arcade'])} "
              f"projects={len(data['projects'])} running={running or 'none'}", flush=True)
        if not args.watch:
            return
        time.sleep(args.watch)


if __name__ == "__main__":
    main()
