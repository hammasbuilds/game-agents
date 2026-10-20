"""Every demonstration film in the repository, listed from the directory.

The panel used to show one film per arcade game, named from the arcade
catalogue. That misses more than it shows: DOOM is played on three maps, the
walking robot is not an arcade game at all, and Brogue's demonstration is built
from stored frames rather than a run. Naming them in code also means a film
recorded later never appears until somebody edits a list.

So the films are found on disk and matched to what is known about them. A film
with no entry here still appears, with its filename as its title — missing from
the panel is worse than appearing plainly.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "docs" / "media"


@dataclass(frozen=True)
class Demo:
    key: str                  # how the page addresses it
    title: str
    game: str
    project: str
    detail: str               # what the film actually shows
    path: str                 # relative to docs/media


# What is known about each film. The key is the path under docs/media, so a new
# recording in a known folder gets its description automatically.
KNOWN: dict[str, tuple[str, str, str, str]] = {
    "doom/defend_the_center_640x480.mp4": (
        "DOOM — defend the center", "ViZDoom (Freedoom)", "01 · DOOM from pixels",
        "untrained and trained on the same map, filmed at 640×480 while the agent "
        "sees 60×80 greyscale"),
    "doom/health_gathering_640x480.mp4": (
        "DOOM — health gathering", "ViZDoom (Freedoom)", "01 · DOOM from pixels",
        "the floor is acid: untrained 348 ticks, trained 1,884 of a possible 2,100"),
    "doom/deadly_corridor_640x480.mp4": (
        "DOOM — deadly corridor", "ViZDoom (Freedoom)", "01 · DOOM from pixels",
        "three episodes end to end, because each one is over in about twenty "
        "agent steps"),
    "crafter/planner_vs_random.mp4": (
        "Crafter — planner vs random", "Crafter", "02 · Crafter, planned",
        "same seed, 512×512: random unlocks 3 achievements, the planner 12, and "
        "it trains nothing"),
    "brogue/seed1.mp4": (
        "Brogue — what the agent reads", "Brogue CE", "03 · Brogue through the screen",
        "the window beside the decoded dungeon: every lit cell named from a glyph "
        "atlas, ? where the decoder is unsure"),
    "walker/walker2d.mp4": (
        "Walker2d — a robot learns to walk", "MuJoCo Walker2d", "04 · Walking",
        "the untrained network and the chosen checkpoint, same episode; the camera "
        "tracks the robot"),
    "racing/progress.mp4": (
        "Car racing — the ladder", "CarRacing-v3", "arcade",
        "untrained, 180k and 419k steps driving the same track at the same moment"),
    "boxing/progress.mp4": (
        "Boxing — the ladder (retired)", "Atari 2600 Boxing", "arcade · retired",
        "kept for its numbers: the trained agent gained nothing over its untrained "
        "checkpoint"),
    "platformer/progress.mp4": (
        "Kangaroo — the ladder (retired)", "Atari 2600 Kangaroo", "arcade · retired",
        "kept for its numbers: it ended worse than untrained, collapsed onto one "
        "button"),
    "pingpong/progress.mp4": (
        "Table tennis — the ladder (retired)", "Atari 2600 Pong", "arcade · retired",
        "from losing every rally to winning them"),
    # The first recordings, kept because the README still links one of them and
    # because "superseded" is a fact worth showing rather than a file to hide.
    "clip_doom.mp4": (
        "DOOM — first recording (superseded)", "ViZDoom (Freedoom)", "01 · DOOM from pixels",
        "320×240, taken from the agent's own training buffer — the reason the "
        "films were rebuilt"),
    "clip_crafter.mp4": (
        "Crafter — first recording (superseded)", "Crafter", "02 · Crafter, planned",
        "256×256, one agent, no comparison"),
    "clip_brogue.mp4": (
        "Brogue — first recording", "Brogue CE", "03 · Brogue through the screen",
        "a plain screen capture of one run, before the decode was shown beside it"),
    "anatomy/game-agents.mp4": (
        "How it works — one frame to one verdict", "all eight", "the whole repository",
        "the isometric walk-through: a frame shrunk to what the agent sees, through "
        "the network, into a ladder of checkpoints and out as a scored verdict"),
    "anatomy/game-agents-architecture.mp4": (
        "The network, layer by layer", "all eight", "the whole repository",
        "every tensor shape and parameter count read from the model: 95% of the "
        "424,790 parameters are in one hidden layer"),
    "reel.mp4": (
        "The reel", "all four arcade games", "arcade",
        "every arcade game in one strip"),
}

# Films that are a step of a ladder rather than a demonstration of their own.
SKIP_PREFIXES = ("step_",)


def demos() -> list[Demo]:
    out: list[Demo] = []
    if not MEDIA.exists():
        return out
    for path in sorted(MEDIA.rglob("*.mp4")):
        relative = path.relative_to(MEDIA).as_posix()
        if any(path.name.startswith(prefix) for prefix in SKIP_PREFIXES):
            continue
        known = KNOWN.get(relative)
        if known:
            title, game, project, detail = known
        else:
            title, game, project = path.stem.replace("_", " "), "", "unlisted"
            detail = "no description for this film yet"
        out.append(Demo(key=relative, title=title, game=game, project=project,
                        detail=detail, path=relative))
    # Known films first, in the order they are described; anything else after.
    order = list(KNOWN)
    out.sort(key=lambda d: (order.index(d.key) if d.key in order else len(order), d.key))
    return out


def as_dicts() -> list[dict]:
    rows = []
    for demo in demos():
        file = MEDIA / demo.path
        gif = file.with_suffix(".gif")
        rows.append({
            "key": demo.key, "title": demo.title, "game": demo.game,
            "project": demo.project, "detail": demo.detail,
            # The panel serves /docs from the repository root.
            "url": f"/docs/media/{demo.path}",
            "gif": f"/docs/media/{gif.relative_to(MEDIA).as_posix()}"
                   if gif.exists() else None,
            "megabytes": round(file.stat().st_size / 1e6, 1),
        })
    return rows
