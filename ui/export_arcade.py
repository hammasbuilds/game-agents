"""Collect every arcade training run into one file the dashboard can read.

Keeps the same rule as the rest of the site: the page shows what a run produced,
and where a run has not happened yet the card says so rather than showing a
number from somewhere else.

    python ui/export_arcade.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "runs_arcade"
MEDIA = ROOT / "docs" / "media"
DATA = ROOT / "docs" / "data"


def read(path: Path):
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None


def thin(history: list[dict], keep: int = 160) -> list[dict]:
    """A curve for a chart does not need every update."""
    if not history:
        return []
    stride = max(1, len(history) // keep)
    rows = history[::stride]
    if rows[-1] is not history[-1]:
        rows.append(history[-1])
    return [{"steps": r["steps"], "return": r["return_mean"],
             "entropy": r.get("entropy"), "length": r.get("length_mean"),
             "sps": r.get("sps")} for r in rows if r.get("return_mean") is not None]


def main() -> None:
    import sys
    sys.path.insert(0, str(ROOT))
    from arcade.envs import CATALOGUE

    games = {}
    for key, game in CATALOGUE.items():
        run = RUNS / key
        media = MEDIA / key
        history = read(run / "history.json") or []
        summary = read(run / "train_summary.json")
        ladder = read(media / "ladder.json")
        clips = sorted(p.name for p in media.glob("*.mp4")) if media.exists() else []
        gifs = sorted(p.name for p in media.glob("*.gif")) if media.exists() else []
        # A run that was stopped early but produced a scored ladder has results
        # worth showing; calling it 'training' hides them behind a placeholder.
        if summary:
            state = "trained"
        elif ladder:
            state = "stopped early"
        elif history:
            state = "training"
        else:
            state = "not started"
        games[key] = {
            "key": key,
            "state": state,
            "title": game.title,
            "blurb": game.blurb,
            "env_id": game.env_id,
            "trained": bool(summary) or bool(ladder),
            "summary": summary,
            "curve": thin(history),
            "ladder": (ladder or {}).get("ladder"),
            "evaluation_seeds": (ladder or {}).get("evaluation_seeds"),
            "clips": clips,
            "gifs": gifs,
            "progress": "progress.mp4" if "progress.mp4" in clips else None,
        }
        print(f"{key:<11} {state:<13} updates={len(history):>5} "
              f"ladder={'yes' if ladder else 'no':<4} clips={len(clips)}")

    DATA.mkdir(parents=True, exist_ok=True)
    payload = {"games": games}
    (DATA / "arcade.json").write_text(json.dumps(payload, indent=1))
    (DATA / "arcade.js").write_text("window.ARCADE = " + json.dumps(payload, indent=1) + ";\n")
    print(f"\nwrote {(DATA / 'arcade.json').relative_to(ROOT)} and arcade.js")


if __name__ == "__main__":
    main()
