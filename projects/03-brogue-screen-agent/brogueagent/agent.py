"""A policy that plays Brogue through the screen and the keyboard.

What the agent is allowed to know is the screen. It gets no hooks, no memory
reads and no save-file parsing; the only thing it sends back is keystrokes.

Two deliberate choices shape it:

**Locomotion goes through Brogue's own commands.** `x` auto-explores and `>`
travels to the down staircase. A human plays this way, and it keeps the agent's
job where the interesting decisions are -- when to explore, when to dive, when to
back off and rest -- rather than in re-implementing a pathfinder the game already
has. The agent still has to *decide*, and it still has to read the screen to know
whether the decision worked.

**Health is read from the bar, not from text.** The sidebar draws a coloured bar
whose filled fraction is the player's health. Measuring coloured pixels is exact
and needs no character recognition, which matters because the decoder names
terrain reliably and letters only sometimes.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .screen import MAP_COL0, MAP_ROW0, Screen

WALKABLE = frozenset({".", "\"", ":", ",", "+"})
WALLS = frozenset({"#", "|", "-"})
# Glyphs that are scenery rather than a threat: the agent should not walk into a
# bloodwort stalk expecting a fight.
HARMLESS = frozenset({"ψ", "*", "$", "!", "?", "(", ")", "[", "]", "/", "=", "\""})

DIRECTIONS = {(-1, 0): "left", (1, 0): "right", (0, -1): "up", (0, 1): "down"}
MOVE_KEYS = {"left": "h", "right": "l", "up": "k", "down": "j"}


@dataclass
class Observation:
    """What one frame tells the agent."""

    screen: Screen
    health: float                  # 0..1, from the sidebar bar
    player: tuple[int, int] | None  # map-local (row, col)
    stairs: list[tuple[int, int]]
    threats: list[tuple[int, int]]
    coverage: float                # share of lit map cells the atlas could name


def read_health(frame: np.ndarray) -> float:
    """Filled fraction of the health bar.

    Brogue draws the bar as a solid block behind the word "Health" in the
    sidebar, in the top rows of the screen. The filled part is markedly brighter
    than the empty part, so the fraction is the share of the bar's width whose
    column is bright.
    """
    arr = np.asarray(frame, dtype=np.float32)
    height, width = arr.shape[:2]
    # Grid row 1 of the sidebar, measured rather than guessed: row 1 is purple
    # across its whole width at the start of a game and row 2 is the nutrition
    # bar below it. Brightness does not work here -- the word "Health" is
    # brighter than the bar it sits on -- but the bar's colour is unmistakable.
    band = arr[round(height / 34):round(2 * height / 34), 0:round(0.20 * width)]
    if band.size == 0:
        return 1.0
    purple = (band[..., 0] + band[..., 2] - 2 * band[..., 1]).max(axis=0)
    if purple.max() < 20:          # no bar on screen at all
        return 0.0
    return float((purple > 40).mean())


def observe(frame, decoder) -> Observation:
    screen = decoder(frame)
    grid = screen.map
    rows, cols = grid.shape

    player = None
    stairs, threats = [], []
    lit = named = 0
    for r in range(rows):
        for c in range(cols):
            ch = grid[r, c]
            if ch == " ":
                continue
            lit += 1
            if ch != "?":
                named += 1
            if ch == "@":
                player = (r, c)
            elif ch == ">":
                stairs.append((r, c))
            elif ch.isalpha() and ch not in HARMLESS:
                threats.append((r, c))
    if player is None:
        # The '@' is drawn in white on the player's tile; when it sits on a lit
        # tile the glyph inverts and may not match. Fall back to the brightest
        # cell near the middle of the view rather than losing track of ourselves.
        player = None
    return Observation(screen=screen, health=read_health(frame), player=player,
                       stairs=stairs, threats=threats,
                       coverage=(named / lit if lit else 1.0))


@dataclass
class BrogueAgent:
    """Decide one keystroke from one frame."""

    name: str = "explorer"
    rest_below: float = 0.55        # health fraction under which it stops to rest
    flee_below: float = 0.30
    chosen: str = "start"
    history: list[str] = field(default_factory=list)
    _last_frames: int = 0

    def reset(self) -> None:
        self.history = []
        self._last_frames = 0

    def _adjacent_threat(self, obs: Observation):
        if obs.player is None:
            return None
        pr, pc = obs.player
        for (dc, dr), name in DIRECTIONS.items():
            if (pr + dr, pc + dc) in obs.threats:
                return name
        return None

    def act(self, obs: Observation) -> tuple[str, str]:
        """Return (key, why)."""
        melee = self._adjacent_threat(obs)

        if melee and obs.health > self.flee_below:
            # Walking into a monster is how you attack it in Brogue.
            return MOVE_KEYS[melee], f"attack {melee}"
        if obs.health <= self.flee_below and obs.threats:
            # Outnumbered and hurt: climb back toward the last staircase rather
            # than trading hits. `<` travels to the up stairs.
            return "<", "retreat upstairs"
        if obs.health <= self.rest_below and not obs.threats:
            # `z` rests until something happens; health comes back with it.
            return "z", "rest"
        if obs.threats and obs.health > self.rest_below:
            # Something is visible but not adjacent. Exploring walks toward it,
            # which is what we want: a cleared level is a safer level.
            return "x", "explore toward trouble"
        if obs.stairs:
            return ">", "take the stairs down"
        return "x", "explore"
