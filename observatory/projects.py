"""Every project on this machine, with the one command that starts it.

The desktop is where these used to live: twenty-seven shortcuts, each a .bat
that finds an interpreter, starts a local server and opens a browser. This is
the same set, reachable from the panel, with the three things a shortcut cannot
give you — whether it is actually answering, where its repository is, and
whether anything is published.

Two rules shape the code:

**A request names an id, never a command.** The catalogue below is the only
source of anything that gets executed. A POST says `{"project": "studyloop"}`
and the launcher comes from here, so there is no path by which the page — or a
website that found this port — supplies a path to run.

**A port answering is not proof the project is up.** Ports collide on this
machine: StudyLoop and the pak-law demo both want 8765. So "something is
answering on 8765" is reported as exactly that, and only a process this panel
started is reported as started by this panel.

`port_conflicts()` is what surfaces these, and it found the traffic panel
sitting on 8781 beside the PsyReason studio -- both launchers really do bind it,
so whichever started second simply failed to come up. The traffic panel is the
one this session owns, so the traffic panel is the one that moved, to 8822:
a port claimed by nothing in this catalogue, nothing in the Launchpad registry
and no .bat under the studios tree.
"""
from __future__ import annotations

import json
import socket
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[0]
SNAPSHOT = HERE / "data" / "projects.json"
JOB_FILE = HERE / "data" / "project_jobs.json"

DESKTOP = Path.home() / "Desktop"
MY_PROJECTS = DESKTOP / "My Projects"
DEMOS = Path("D:/github/_demos")
DATASETS = Path("C:/d drive data/ai generated datasets")
STUDIOS = DATASETS / "Ai generated datasets"


@dataclass
class Project:
    """One launchable thing.

    `launcher` is either a path to the .bat/.cmd the desktop shortcut pointed at,
    or an argv list for the projects that are started by a module rather than a
    script. `port` is the port its own launcher chose — read out of the launcher,
    not guessed — and `None` for the two that open a window instead of a page.
    """

    id: str
    name: str
    group: str
    blurb: str
    launcher: str | list[str]
    cwd: str | None = None
    port: int | None = None
    repo_dir: str | None = None
    kind: str = "web"                 # web | desktop
    live: str | None = None           # a published page, if there is one
    pages: dict[str, str] = field(default_factory=dict)   # label -> url
    io_hint: str | None = None        # what the project takes in and gives back
    private: bool = False


CATALOGUE: list[Project] = [
    # -- this repo ------------------------------------------------------------
    Project(
        id="game-agents",
        name="Game agents — dashboard",
        group="Game agents",
        blurb="The public dashboard for the four arcade games and the three "
              "desktop games, served from this checkout.",
        launcher=[sys.executable, "-m", "http.server", "8779", "--bind", "127.0.0.1",
                  "--directory", "docs"],
        cwd=str(ROOT),
        port=8779,
        repo_dir=str(ROOT),
        live="https://hammasbuilds.github.io/game-agents/",
        pages={"analytics": "https://hammasbuilds.github.io/game-agents/analytics.html",
               "demo videos": "https://hammasbuilds.github.io/game-agents/index.html#media",
               "Kaggle notebook": "https://www.kaggle.com/code/hammasbuilds/game-agents-ppo-arcade"},
        io_hint="in: a game and a checkpoint · out: score per checkpoint, films of "
                "the first and last",
    ),
    Project(
        id="traffic-agents",
        name="Traffic agents — live city",
        group="Traffic",
        blurb="A 3x3 grid of signalised junctions, four controllers, and a "
              "head-to-head race on identical arrivals.",
        launcher=[sys.executable, "-m", "web.server", "--port", "8822"],
        cwd="D:/github/traffic-agents",
        port=8822,
        repo_dir="D:/github/traffic-agents",
        io_hint="in: grid size, demand, controller · out: delay, throughput, "
                "per-phase reasoning at any junction",
    ),

    # -- the five packages, through their demonstration front ends ------------
    Project(id="urdunlp", name="urdunlp — Urdu NLP", group="Packages",
            blurb="Urdu normalisation, transliteration and tokenising, in a page.",
            launcher=str(MY_PROJECTS / "1 - urdunlp (Urdu NLP).bat"),
            port=8771, repo_dir="D:/github/urdu-nlp-toolkit",
            io_hint="in: Urdu or Roman text · out: normalised text, transliteration, tokens"),
    Project(id="suite-auditor", name="suite-auditor", group="Packages",
            blurb="Finds the tests in a suite that cannot fail.",
            launcher=str(MY_PROJECTS / "2 - suite-auditor (test-suite audit).bat"),
            port=8773, repo_dir="D:/github/suite-auditor",
            io_hint="in: a Python package · out: assertion-free and tautological tests"),
    Project(id="assay-drift", name="assay-drift", group="Packages",
            blurb="PCR primers against a drifting viral genome.",
            launcher=str(MY_PROJECTS / "3 - assay-drift (PCR assay drift).bat"),
            port=8772, repo_dir="D:/github/assay-drift",
            io_hint="in: an assay and a sequence · out: mismatches, position, verdict"),
    Project(id="blast-radius", name="blast-radius", group="Packages",
            blurb="What a dependency upgrade actually touches.",
            launcher=str(MY_PROJECTS / "4 - blast-radius (upgrade impact).bat"),
            port=8774, repo_dir="D:/github/blast-radius",
            io_hint="in: a repo and a package bump · out: the call sites that change"),
    Project(id="flake-detective", name="flake-detective", group="Packages",
            blurb="Separates flaky tests from broken ones by re-running them.",
            launcher=str(MY_PROJECTS / "5 - flake-detective (flaky tests).bat"),
            port=8775, repo_dir="D:/github/flake-detective",
            io_hint="in: a suite and a repeat count · out: flake rate per test"),

    # -- the MCP servers and the lab, through their demos ---------------------
    Project(id="agent-tools", name="Agent tools (agentic-ai-lab)", group="Packages",
            blurb="The eleven tool packages behind the lab, in one page.",
            launcher=str(DEMOS / "agenttools" / "start.cmd"),
            port=8785, repo_dir="D:/github/agentic-ai-lab",
            io_hint="in: a tool and its arguments · out: the tool's real output"),
    Project(id="paklaw", name="Pakistan law MCP", group="Packages",
            blurb="Statute lookup over a bundled corpus, no network.",
            launcher=str(DEMOS / "paklaw" / "start.cmd"),
            port=8765, repo_dir="D:/github/pak-law-assistant",
            io_hint="in: a legal question · out: the section, quoted, with its citation"),
    Project(id="repo-recon", name="Repo recon MCP", group="Packages",
            blurb="Six read-only tools for reading an unfamiliar repository.",
            launcher=str(DEMOS / "reporecon" / "start.cmd"),
            port=8766, repo_dir="D:/github/repo-recon",
            io_hint="in: a checkout · out: entry points, hot files, test map"),

    # -- the three products ---------------------------------------------------
    Project(id="studyloop", name="StudyLoop", group="Products",
            blurb="Spaced repetition over your own notes.",
            launcher="D:/github/studyloop/run.bat", port=8765,
            repo_dir="D:/github/studyloop",
            live="https://studyloop-iota.vercel.app",
            io_hint="in: notes or a PDF · out: cards, a schedule, a daily queue"),
    Project(id="analyst-in-a-box", name="Analyst-in-a-Box", group="Products",
            blurb="A table in, a written analysis out.",
            launcher="D:/github/analyst-in-a-box/run.bat", port=8780,
            repo_dir="D:/github/analyst-in-a-box",
            live="https://analyst-in-a-box-bay.vercel.app",
            io_hint="in: a CSV · out: charts, findings, and the SQL behind them"),
    Project(id="llm-control-room", name="LLM Control Room", group="Products",
            blurb="What the local models are doing, and what they cost.",
            launcher="D:/github/llm-control-room/run.bat", port=8790,
            repo_dir="D:/github/llm-control-room",
            live="https://llm-control-room.vercel.app",
            io_hint="in: a prompt and a model · out: latency, tokens, cost, a log"),
    Project(id="job-radar", name="job-radar", group="Products",
            blurb="Non-GPU job and company hunting, filtered hard.",
            launcher="D:/github/job-radar/run-job-radar.bat", port=8000,
            repo_dir="D:/github/job-radar", private=True,
            io_hint="in: a search · out: the few postings that survive the filters"),

    # -- research, all private ------------------------------------------------
    Project(id="trial-by-ai", name="Trial by AI", group="Research",
            blurb="The courtroom game. Private, and staying private.",
            launcher="D:/the dock/TrialByAI.bat", port=8000,
            repo_dir="D:/the dock", private=True,
            io_hint="in: your questions to a witness · out: a verdict and a score"),
    Project(id="psyscreen", name="PsyScreen", group="Research",
            blurb="The psychological assessment app.",
            launcher="D:/psychological assessment app/psyreason-app/PsyScreen.bat",
            port=8010, repo_dir="D:/psychological assessment app/psyreason-app",
            private=True,
            io_hint="in: an instrument and answers · out: scored scales and a report"),
    Project(id="dalil", name="DALIL", group="Research",
            blurb="The Urdu legal reasoning model, in a browser.",
            launcher="D:/22 Ai genefrted dataset 22/dalil/DALIL.bat", port=8731,
            repo_dir="D:/22 Ai genefrted dataset 22/dalil", private=True,
            io_hint="in: an Urdu legal question · out: the model's reasoning and answer"),
    Project(id="scholarcritic", name="ScholarCritic", group="Research",
            blurb="Reviews a protocol and says what is wrong with it.",
            launcher=str(DATASETS / "10-scholarcritic" / "ScholarCritic.bat"),
            port=8020, repo_dir=None, private=True,
            io_hint="in: a method section · out: the flaws it finds, with reasons"),
    Project(id="research-lab", name="Research Lab", group="Research",
            blurb="The GPU queue and the research projects, as a desktop window.",
            launcher=["D:/the dock/.venv/Scripts/pythonw.exe",
                      "D:/pending research work/_desktop/research_lab.pyw"],
            cwd="D:/pending research work/_desktop", kind="desktop", private=True,
            io_hint="in: a job · out: the queue, and what the GPU is doing"),

    # -- the ten dataset studios ---------------------------------------------
    *[Project(id=f"studio-{slug}", name=f"{label} studio", group="Dataset studios",
              blurb=f"Browse and search the {label} dataset.",
              launcher=str(STUDIOS / folder / bat), port=port, private=True,
              io_hint="in: a filter or a row id · out: the example, its label and its check")
      for slug, label, folder, bat, port in (
          ("psyreason", "PsyReason", "01-psyreason", "PsyReason-Studio.bat", 8781),
          ("contradiction-ledger", "Contradiction Ledger", "02-contradiction-ledger",
           "ContradictionLedger-Studio.bat", 8782),
          ("witnessdrift", "WitnessDrift", "03-witnessdrift", "WitnessDrift-Studio.bat", 8783),
          ("fraudtrail", "FraudTrail", "04-fraudtrail", "FraudTrail.bat", 8792),
          ("timelineforge", "TimelineForge", "05-timelineforge", "TimelineForge-Studio.bat", 8785),
          ("deescalate", "DeEscalate", "06-deescalate", "DeEscalate-Studio.bat", 8786),
          ("urdu-legal-reason", "Urdu Legal Reason", "07-urdu-legal-reason",
           "UrduLegalReason-Studio.bat", 8787),
          ("interrogation-logic", "Interrogation Logic", "08-interrogation-logic",
           "InterrogationLogic-Studio.bat", 8788),
          ("protocolcheck", "ProtocolCheck", "09-protocolcheck", "ProtocolCheck.bat", 8791),
      )],
    Project(id="studio-scholarcritic", name="ScholarCritic data studio",
            group="Dataset studios",
            blurb="Browse and search the ScholarCritic dataset — 271,755 rows, five tasks.",
            launcher=str(DATASETS / "10-scholarcritic" / "ScholarCriticData-Studio.bat"),
            port=8790, private=True,
            io_hint="in: a task and a filter · out: the example and its verified label"),
]

BY_ID = {p.id: p for p in CATALOGUE}
GROUPS = ["Game agents", "Traffic", "Packages", "Products", "Research",
          "Dataset studios"]


# -- the facts that have to be checked rather than claimed -------------------
def port_answering(port: int | None, timeout: float = 0.25) -> bool:
    if not port:
        return False
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def port_conflicts() -> dict[int, list[str]]:
    """Ports that more than one project wants.

    Five of them collide on this machine, which matters: open the panel's link
    for StudyLoop while the pak-law demo is serving on 8765 and you get pak-law,
    with nothing anywhere saying so.
    """
    seen: dict[int, list[str]] = {}
    for project in CATALOGUE:
        if project.port:
            seen.setdefault(project.port, []).append(project.id)
    return {port: ids for port, ids in seen.items() if len(ids) > 1}


def snapshot() -> dict:
    """The verified side of the catalogue, written by scan_projects.py."""
    try:
        return json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"checked": None, "projects": {}}


def as_dict(project: Project, verified: dict) -> dict:
    extra = verified.get("projects", {}).get(project.id, {})
    launcher = project.launcher
    return {
        "id": project.id,
        "name": project.name,
        "group": project.group,
        "blurb": project.blurb,
        "kind": project.kind,
        "port": project.port,
        "url": f"http://127.0.0.1:{project.port}/" if project.port else None,
        "io_hint": project.io_hint,
        "private": project.private,
        "live": project.live,
        "pages": project.pages,
        "launcher": launcher if isinstance(launcher, str) else " ".join(launcher),
        # Verified by the scanner: does the launcher exist, what is the repo's
        # remote, is it public, does the published page answer.
        "launcher_exists": extra.get("launcher_exists"),
        "github": extra.get("github"),
        "visibility": extra.get("visibility"),
        "live_status": extra.get("live_status"),
        "repo_dir": project.repo_dir,
        "checked": verified.get("checked"),
    }
