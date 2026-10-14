"""ViZDoom wrapped down to what a small CPU policy can chew on.

The raw game hands back a 3x240x320 RGB frame 35 times a second. That is far more
pixels than this agent needs and far more decisions than it benefits from, so each
step here holds one action for `frame_skip` tics and returns a stack of the last
`stack` greyscale 60x80 frames.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

import numpy as np
import vizdoom as vzd

# Scenario -> the buttons the agent is allowed to press. Keeping the action set
# minimal matters more on CPU than any network change: every extra button is a
# wider softmax and a longer search for the same behaviour.
ACTION_SETS: dict[str, list[list[int]]] = {
    # basic.cfg declares MOVE_LEFT, MOVE_RIGHT, ATTACK
    "basic": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
    # defend_the_center.cfg declares TURN_LEFT, TURN_RIGHT, ATTACK
    "defend_the_center": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
    # health_gathering.cfg declares MOVE_FORWARD, TURN_LEFT, TURN_RIGHT
    "health_gathering": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
}

H, W = 60, 80


@dataclass
class EnvConfig:
    scenario: str = "defend_the_center"
    frame_skip: int = 4
    stack: int = 4
    seed: int | None = None
    window: bool = False


def _downsample(screen: np.ndarray) -> np.ndarray:
    """3x120x160 uint8 RGB -> 60x80 uint8 greyscale.

    Plain 2x2 box filter and the ITU-R 601 luma weights; cv2 is not a dependency
    of this project and for a 120x160 frame numpy is quicker than the import.
    Staying in uint8 is not a detail: these frames cross a process boundary every
    step, and sending them as float32 made the rollout 2.5x slower than the game.
    """
    rgb = screen.astype(np.float32)
    grey = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
    return grey.reshape(H, 2, W, 2).mean(axis=(1, 3)).astype(np.uint8)


class DoomEnv:
    """Single ViZDoom instance. No gym dependency: step() returns plain tuples."""

    def __init__(self, cfg: EnvConfig):
        self.cfg = cfg
        if cfg.scenario not in ACTION_SETS:
            raise ValueError(f"unknown scenario {cfg.scenario!r}; have {sorted(ACTION_SETS)}")
        game = vzd.DoomGame()
        game.load_config(os.path.join(vzd.scenarios_path, f"{cfg.scenario}.cfg"))
        game.set_screen_resolution(vzd.ScreenResolution.RES_160X120)
        game.set_screen_format(vzd.ScreenFormat.CRCGCB)
        game.set_window_visible(cfg.window)
        if cfg.seed is not None:
            game.set_seed(cfg.seed)
        game.init()
        self.game = game
        self.actions = ACTION_SETS[cfg.scenario]
        self.frames = np.zeros((cfg.stack, H, W), dtype=np.uint8)

    # -- plumbing ---------------------------------------------------------
    @property
    def n_actions(self) -> int:
        return len(self.actions)

    @property
    def obs_shape(self) -> tuple[int, int, int]:
        return (self.cfg.stack, H, W)

    def frame(self) -> np.ndarray:
        """The newest 60x80 uint8 frame. The vectorised trainer sends this across
        the process boundary and keeps the stack on its own side."""
        state = self.game.get_state()
        if state is None:  # episode just finished; the last frame still stands
            return self.frames[-1]
        return _downsample(state.screen_buffer)

    def _observe(self) -> np.ndarray:
        self.frames = np.roll(self.frames, -1, axis=0)
        self.frames[-1] = self.frame()
        return self.frames.copy()

    def reset(self) -> np.ndarray:
        self.game.new_episode()
        self.frames[:] = 0
        return self._observe()

    def step(self, action: int) -> tuple[np.ndarray, float, bool]:
        reward = self.game.make_action(self.actions[action], self.cfg.frame_skip)
        done = self.game.is_episode_finished()
        return self._observe(), float(reward), done

    def episode_return(self) -> float:
        return float(self.game.get_total_reward())

    def close(self) -> None:
        self.game.close()
