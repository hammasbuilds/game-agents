"""The project catalogue, checked where it would otherwise lie quietly.

Every one of these corresponds to a way the launcher could mislead: a button
that runs the wrong thing, a link to a repository nobody else can open, a green
status taken from a port somebody else is on, or a request that supplies its own
command.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from observatory import projects, server


def test_ids_are_unique():
    ids = [p.id for p in projects.CATALOGUE]
    assert len(ids) == len(set(ids))


def test_every_group_is_one_of_the_declared_groups():
    for project in projects.CATALOGUE:
        assert project.group in projects.GROUPS, project.id


def test_launchers_are_absolute():
    """A relative launcher runs whatever is in the current directory."""
    for project in projects.CATALOGUE:
        launcher = project.launcher
        first = launcher if isinstance(launcher, str) else launcher[0]
        assert Path(first).is_absolute(), f"{project.id}: {first}"


def test_a_request_cannot_name_a_command():
    """Only ids in the catalogue start anything."""
    out = server.start_project("../../anything.bat")
    assert out["ok"] is False and "unknown project" in out["error"]
    out = server.stop_project("not-a-project")
    assert out["ok"] is False and "unknown project" in out["error"]


def test_port_conflicts_are_found_not_hidden():
    """Five ports on this machine are claimed twice; the panel has to say so.

    If this ever returns nothing, either the ports were separated — good, update
    the test — or the detection broke, and the panel would start telling people
    StudyLoop is running when the pak-law demo has 8765.
    """
    conflicts = projects.port_conflicts()
    assert conflicts, "two projects share a port in the catalogue; this found none"
    for port, ids in conflicts.items():
        assert len(ids) > 1
        for pid in ids:
            assert projects.BY_ID[pid].port == port


def test_status_separates_ours_from_anyones(monkeypatch):
    """A port answering is not the same fact as a project this panel started."""
    monkeypatch.setattr(projects, "port_answering", lambda port, timeout=0.25: True)
    rows = {r["id"]: r for r in server.project_rows()}
    row = rows["studyloop"]
    assert row["port_answering"] is True
    assert row["started_here"] is False
    assert row["status"] == "port in use", "an answering port must not read as running"

    monkeypatch.setattr(projects, "port_answering", lambda port, timeout=0.25: False)
    assert server.project_rows()[0]["status"] == "stopped"


def test_stop_refuses_to_kill_what_it_did_not_start(monkeypatch):
    monkeypatch.setattr(projects, "port_answering", lambda port, timeout=0.25: True)
    out = server.stop_project("studyloop")
    assert out["ok"] is False
    assert "did not start it" in out["error"]


def test_start_refuses_an_occupied_port(monkeypatch):
    monkeypatch.setattr(projects, "port_answering", lambda port, timeout=0.25: True)
    out = server.start_project("urdunlp")
    assert out["ok"] is False
    assert "already answering" in out["error"]
    assert out["url"] == "http://127.0.0.1:8771/"


def test_private_projects_get_no_github_link():
    """A link to a private repository is a 404 for everybody but its owner."""
    verified = projects.snapshot()
    if not verified.get("projects"):
        pytest.skip("no scan on this machine yet: run observatory.scan_projects")
    for project in projects.CATALOGUE:
        row = projects.as_dict(project, verified)
        if row["visibility"] == "PRIVATE":
            assert row["github"] is None, project.id


def test_snapshot_is_dated():
    """Every line of it is a measurement of this machine at one moment."""
    verified = projects.snapshot()
    if not verified.get("projects"):
        pytest.skip("no scan on this machine yet")
    assert verified.get("checked"), "the scan must record when it was taken"


def test_docs_are_served_from_the_repository():
    """The films live in docs/, which is not the directory the page is served from."""
    resolved = server.docs_path("/docs/media/racing/progress.mp4")
    assert Path(resolved) == (server.ROOT / "docs" / "media" / "racing"
                              / "progress.mp4").resolve()
    assert server.docs_path("/data/snapshot.js") is None


def test_docs_prefix_cannot_escape_docs():
    for attempt in ("/docs/../../../Windows/win.ini", "/docs/..%2f..%2fsecrets",
                    "/docs/../observatory/server.py"):
        resolved = server.docs_path(attempt)
        if resolved is not None:
            assert str(Path(resolved)).startswith(
                str((server.ROOT / "docs").resolve())), attempt
