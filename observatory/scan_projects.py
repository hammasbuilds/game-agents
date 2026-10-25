"""Check the catalogue against the machine and write what is actually true.

    python -m observatory.scan_projects

Four things the panel must not guess:

* whether the launcher is still where the desktop shortcut pointed,
* which repository the project's folder is a checkout of,
* whether that repository is public — a GitHub link to a private repo is a 404
  for everybody except its owner, so it must not be offered as a link,
* whether the published page is actually published. Twelve of these repos look
  like they should have a Pages site; one has one. The rest are checked and
  recorded as having none rather than linked hopefully.

The result is dated, because every line of it is a measurement of this machine
at one moment: a checkout moves, a repo goes public, a launcher is renamed.
"""
from __future__ import annotations

import json
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from observatory.projects import CATALOGUE, LOCAL_IDS, LOCAL_SNAPSHOT, SNAPSHOT, Project


def remote_of(repo_dir: str | None) -> str | None:
    if not repo_dir or not (Path(repo_dir) / ".git").exists():
        return None
    try:
        url = subprocess.run(["git", "-C", repo_dir, "remote", "get-url", "origin"],
                             capture_output=True, text=True, timeout=20).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None
    if not url:
        return None
    return url[:-4] if url.endswith(".git") else url


def visibility_of(remote: str | None) -> str | None:
    """PUBLIC / PRIVATE, straight from GitHub. None when it cannot be asked."""
    if not remote or "github.com" not in remote:
        return None
    slug = remote.split("github.com")[-1].lstrip(":/")
    try:
        out = subprocess.run(["gh", "repo", "view", slug, "--json", "visibility",
                              "-q", ".visibility"],
                             capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    value = out.stdout.strip()
    return value or None


def page_status(url: str | None) -> int | str | None:
    if not url:
        return None
    request = urllib.request.Request(url, method="GET",
                                     headers={"User-Agent": "observatory-scan"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.status
    except urllib.error.HTTPError as exc:
        return exc.code
    except Exception as exc:                      # offline, DNS, timeout
        return type(exc).__name__


def check(project: Project) -> dict:
    launcher = project.launcher
    path = Path(launcher if isinstance(launcher, str) else launcher[0])
    # An argv whose first element is this interpreter is not a file to look for.
    is_file = isinstance(launcher, str) or path.suffix.lower() in (".exe", ".bat",
                                                                   ".cmd", ".pyw")
    remote = remote_of(project.repo_dir)
    visibility = visibility_of(remote)
    row = {
        "launcher_exists": path.exists() if is_file else True,
        "github": remote if visibility == "PUBLIC" else None,
        "visibility": visibility,
        "live_status": page_status(project.live),
    }
    # A private repo gets no link, and the reason is recorded rather than left
    # as an absence someone later reads as "forgot to add it".
    if visibility == "PRIVATE":
        row["github_note"] = "private repository — no public link"
    elif remote is None and project.repo_dir:
        row["github_note"] = "no remote: this checkout has never been pushed"
    return row


def main() -> None:
    rows: dict[str, dict] = {}
    for project in CATALOGUE:
        row = check(project)
        rows[project.id] = row
        flags = []
        if not row["launcher_exists"]:
            flags.append("LAUNCHER MISSING")
        if row["visibility"]:
            flags.append(row["visibility"].lower())
        if row["live_status"]:
            flags.append(f"live {row['live_status']}")
        print(f"  {project.id:<26} {' · '.join(flags) or '—'}", flush=True)

    checked = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    SNAPSHOT.parent.mkdir(parents=True, exist_ok=True)
    # private projects' facts go to the git-ignored file, so a commit never names them
    for path, keep in ((SNAPSHOT, lambda k: k not in LOCAL_IDS), (LOCAL_SNAPSHOT, lambda k: k in LOCAL_IDS)):
        payload = {"checked": checked, "projects": {k: v for k, v in rows.items() if keep(k)}}
        path.write_text(json.dumps(payload, indent=1), encoding="utf-8")
    missing = [k for k, v in rows.items() if not v["launcher_exists"]]
    print(f"\n{len(rows)} projects checked; {len(missing)} launchers missing"
          f"{': ' + ', '.join(missing) if missing else ''}")
    print(f"wrote {SNAPSHOT}")


if __name__ == "__main__":
    main()
