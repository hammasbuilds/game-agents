"""Tests for the control panel's parameter checking.

The panel hands values to a command line. That is exactly the place where a
careless implementation lets a request name a flag, or an out-of-range number
quietly become a different experiment, so the validator gets its own tests.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def build(config):
    from observatory.server import build_train_args
    return build_train_args(config)


def test_a_valid_config_becomes_switches_and_values():
    args, used, problem = build({"steps": 500_000, "envs": 8, "arch": "impala",
                                 "width": 2, "lr": 3e-4})
    assert problem is None
    assert args == ["--steps", "500000", "--envs", "8", "--arch", "impala",
                    "--width", "2", "--lr", "0.0003"]
    assert used["arch"] == "impala"


def test_an_unknown_key_is_refused_rather_than_passed_on():
    """Nothing in a request may become a flag; only values of known switches."""
    _, _, problem = build({"rm": "-rf"})
    assert problem and "not a setting" in problem


def test_out_of_range_is_refused_not_clamped():
    """Clamping would turn a typo into a different experiment that still runs."""
    _, _, problem = build({"lr": 5.0})
    assert problem and "at most" in problem
    _, _, problem = build({"envs": 0})
    assert problem and "at least" in problem


def test_an_unknown_architecture_is_refused():
    _, _, problem = build({"arch": "transformer"})
    assert problem and "nature" in problem


def test_minibatches_must_divide_the_batch():
    """PPO would otherwise train on a ragged last slice every update."""
    _, _, problem = build({"envs": 12, "rollout": 128, "minibatches": 7})
    assert problem and "divide" in problem
    _, _, problem = build({"envs": 12, "rollout": 128, "minibatches": 4})
    assert problem is None


def test_blank_values_are_skipped_so_defaults_survive():
    args, used, problem = build({"steps": 100_000, "width": "", "arch": None})
    assert problem is None
    assert args == ["--steps", "100000"]
    assert "width" not in used


@pytest.mark.parametrize("arch,expected_order", [("small", 1), ("nature", 4), ("impala", 10)])
def test_every_architecture_builds_and_grows_with_width(arch, expected_order):
    """Each named architecture has to be constructible, and `width` has to mean
    the same thing in all of them."""
    sys.path.insert(0, str(ROOT))
    from arcade.model import build as build_model

    narrow = build_model((4, 84, 84), 6, arch=arch, width=1).n_params()
    wide = build_model((4, 84, 84), 6, arch=arch, width=2).n_params()
    assert narrow > 10_000
    assert wide > 2 * narrow         # channels scale in two dimensions at once
    assert narrow // 100_000 <= expected_order


def test_a_checkpoint_without_an_architecture_still_loads():
    """Checkpoints written before architectures existed carry no 'arch'; they are
    all the nature trunk and must not become unloadable."""
    import torch

    from arcade.model import ActorCritic

    blob = {"obs_shape": (4, 84, 84), "n_actions": 6, "width": 1}
    model = ActorCritic(tuple(blob["obs_shape"]), blob["n_actions"],
                        width=blob.get("width", 1), arch=blob.get("arch", "nature"))
    assert model.arch == "nature"
    assert isinstance(model.n_params(), int)
    del torch
