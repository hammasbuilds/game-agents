"""The evaluation protocol every project in this repository is scored by.

Three rules, written once here instead of four times badly:

**1. The last checkpoint is not the trained agent.** Both long runs in this
repository peaked in the middle and got worse: the walker reached 4,502 at
700k steps and finished at 3,550 by 2M; racing peaked at 60k and declined for
the next 360k. Reporting the final checkpoint is reporting whichever point
training happened to stop at.

**2. Choosing the best checkpoint is itself a measurement, so it needs its own
seeds.** Picking the highest scorer on a set of episodes and then quoting that
same score is selection bias — with six checkpoints and noisy episodes, the
winner is partly the luckiest. So the ladder is scored on `SELECT_SEEDS`, the
winner is re-scored on the disjoint `REPORT_SEEDS`, and the reported number is
the second one.

**3. A gain is a gain only if it is bigger than the uncertainty of the
difference.** Two standard errors of the difference, not two standard
deviations: with eight episodes a hundred-point gap in a racing score can be
nothing at all.

Nothing here knows what a game is. A project supplies a callable that plays N
episodes from a seed list and returns the returns; everything else is shared.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable, Sequence

import numpy as np

# Disjoint on purpose. Selection and reporting must not share an episode.
SELECT_SEEDS = tuple(range(2_000, 2_020))
REPORT_SEEDS = tuple(range(9_000, 9_020))


@dataclass
class Score:
    """What N episodes of one agent came to."""

    returns: list[float]
    seeds: list[int] = field(default_factory=list)
    lengths: list[float] = field(default_factory=list)

    @property
    def n(self) -> int:
        return len(self.returns)

    @property
    def mean(self) -> float:
        return float(np.mean(self.returns)) if self.returns else float("nan")

    @property
    def std(self) -> float:
        return float(np.std(self.returns, ddof=1)) if self.n > 1 else 0.0

    @property
    def se(self) -> float:
        """Standard error: how far the *mean* is likely to be from the truth.

        This, not the standard deviation, is what a comparison of means is
        allowed to use. An earlier version of this repository compared two means
        against the sum of their standard deviations and called real learning
        noise.
        """
        return self.std / np.sqrt(self.n) if self.n > 1 else 0.0

    def as_dict(self) -> dict:
        return {
            "episodes": self.n,
            "return_mean": round(self.mean, 2),
            "return_std": round(self.std, 2),
            "return_se": round(self.se, 2),
            "return_min": round(float(np.min(self.returns)), 2) if self.returns else None,
            "return_max": round(float(np.max(self.returns)), 2) if self.returns else None,
            "steps_mean": round(float(np.mean(self.lengths)), 1) if self.lengths else None,
            "seeds": list(self.seeds),
            "returns": [round(float(r), 2) for r in self.returns],
        }


def verdict(challenger: Score, baseline: Score, challenger_name: str = "trained",
            baseline_name: str = "untrained") -> dict:
    """Did the challenger beat the baseline by more than the measurement can explain?"""
    gain = challenger.mean - baseline.mean
    bar = 2 * float(np.hypot(challenger.se, baseline.se))
    if gain > bar:
        label = "learned"
    elif gain < -bar:
        label = f"worse than {baseline_name}"
    else:
        label = "inside noise"
    return {
        "challenger": challenger_name, "baseline": baseline_name,
        "challenger_mean": round(challenger.mean, 2),
        "baseline_mean": round(baseline.mean, 2),
        "gain": round(gain, 2), "bar": round(bar, 2), "label": label,
        "episodes": challenger.n,
    }


def _log(message: str) -> None:
    """Print, flushed. Scoring a ladder takes minutes and its output is usually
    redirected to a file, where an unflushed print means the log stays empty
    until the run ends and there is no way to tell it apart from a hang."""
    print(message, flush=True)


def score_ladder(checkpoints: Sequence, play: Callable[[object, Iterable[int]], Score],
                 select_seeds: Sequence[int] = SELECT_SEEDS,
                 report_seeds: Sequence[int] = REPORT_SEEDS,
                 log=_log) -> dict:
    """Score every checkpoint, pick the best, and re-score it on fresh episodes.

    `checkpoints` is any sequence of (label, handle) pairs, oldest first;
    `play(handle, seeds)` returns a Score. The first checkpoint is treated as the
    untrained baseline, which is why every training run here keeps one.
    """
    rows = []
    for label, handle in checkpoints:
        score = play(handle, select_seeds)
        rows.append({"checkpoint": label, **score.as_dict()})
        log(f"  {str(label):<16} return {score.mean:>9.1f} ± {score.se:>6.1f} "
            f"over {score.n} selection episodes")

    best_index = int(np.argmax([r["return_mean"] for r in rows]))
    best_label, best_handle = checkpoints[best_index]
    first_label, first_handle = checkpoints[0]

    # The two numbers that get quoted are measured on episodes no checkpoint was
    # chosen on.
    best_report = play(best_handle, report_seeds)
    first_report = play(first_handle, report_seeds)
    log(f"\n  best on selection episodes: {best_label}")
    log(f"  re-scored on {len(report_seeds)} held-out episodes: "
        f"{best_report.mean:.1f} ± {best_report.se:.1f} "
        f"(untrained {first_report.mean:.1f} ± {first_report.se:.1f})")

    out = {
        "select_seeds": list(select_seeds),
        "report_seeds": list(report_seeds),
        "ladder": rows,
        "best": {"checkpoint": best_label, **best_report.as_dict()},
        "untrained": {"checkpoint": first_label, **first_report.as_dict()},
        "final": rows[-1],
        "verdict": verdict(best_report, first_report),
    }
    # Whether training should have stopped earlier is a fact about the run, and
    # it is the one a "final checkpoint" report hides.
    out["peaked_early"] = bool(best_index < len(rows) - 1)
    if out["peaked_early"]:
        drop = rows[best_index]["return_mean"] - rows[-1]["return_mean"]
        out["decline_after_peak"] = round(drop, 2)
        log(f"  peaked at {best_label} and declined {drop:.1f} by the end of training")
    return out


# -- the record of rounds ----------------------------------------------------
def record_round(entry: dict, path=None) -> None:
    """Append one scored round to the repository's round log.

    A single result says what an agent does; the log says what *trying again*
    did, which is the only way to tell a real improvement from a seed. Each line
    carries the configuration that produced it, so a round that beat the last
    one can be repeated rather than admired.

    Appending, never rewriting: a round whose numbers came out badly stays in
    the file. The whole value of the log is that it contains the attempts that
    did not work.
    """
    import json
    import subprocess
    from datetime import datetime, timezone
    from pathlib import Path

    root = Path(__file__).resolve().parent
    path = Path(path) if path else root / "docs" / "data" / "rounds.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=root,
                                capture_output=True, text=True, timeout=20).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        commit = None
    row = {"at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ"),
           "commit": commit or None, **entry}
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row) + chr(10))
