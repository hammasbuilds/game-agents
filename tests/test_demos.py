"""The demonstration index: what the panel offers to play.

The panel used to name one film per arcade game in code, which meant DOOM's two
newer maps, the walking robot and Brogue's rebuilt demo were all invisible there
no matter how many times they were recorded.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from observatory import demos as demo_index

ROOT = Path(__file__).resolve().parents[1]


def test_every_film_on_disk_is_offered():
    """Found from the directory, not from a list somebody has to remember."""
    on_disk = {p.relative_to(demo_index.MEDIA).as_posix()
               for p in demo_index.MEDIA.rglob("*.mp4")
               if not p.name.startswith("step_")}
    offered = {d.key for d in demo_index.demos()}
    assert on_disk == offered


def test_ladder_steps_are_not_demonstrations():
    """A single checkpoint playing alone is a step, not a demonstration."""
    keys = {d.key for d in demo_index.demos()}
    assert not any("step_" in key for key in keys)


def test_every_film_has_a_description():
    """An unlisted film still appears, but this catches one before it ships."""
    unlisted = [d.key for d in demo_index.demos() if d.project == "unlisted"]
    assert not unlisted, f"no description for: {unlisted}"


def test_urls_point_at_the_docs_tree_the_panel_serves():
    for row in demo_index.as_dicts():
        assert row["url"].startswith("/docs/media/")
        assert (ROOT / row["url"].lstrip("/")).exists()


def test_sizes_are_real():
    for row in demo_index.as_dicts():
        assert row["megabytes"] > 0


def test_known_entries_name_files_that_exist():
    """A description for a film that is gone is a card that never renders."""
    missing = [key for key in demo_index.KNOWN if not (demo_index.MEDIA / key).exists()]
    assert not missing, f"described but absent: {missing}"
