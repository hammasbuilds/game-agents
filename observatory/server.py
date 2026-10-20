"""A small local control panel for the agents.

    python -m observatory.server

Serves the observatory and four actions behind it: start training, stop
training, watch an agent play in a real window, and stop watching. A page opened
straight off disk can show numbers but cannot launch anything, which is the whole
reason this exists.

**What it will and will not do.** It binds to 127.0.0.1 only, so nothing off this
machine can reach it. It accepts a fixed set of actions over a fixed list of
games — there is no path by which a request names a command to run. And every
action requires a token minted at startup and injected into the page it serves:
without it, any website open in the same browser could post to this port and
start jobs, which is a real thing that happens to local servers that assume
loopback means safe.
"""
from __future__ import annotations

import argparse
import json
import os
import secrets
import signal
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
PY = ROOT / ".venv" / "Scripts" / "python.exe"

from observatory import projects                                  # noqa: E402

TOKEN = secrets.token_urlsafe(18)
JOBS: dict[str, dict] = {}
LOCK = threading.Lock()
REGISTRY = HERE / "data" / "jobs.json"


def _alive(pid: int) -> bool:
    """Is this pid still a live python process?

    A bare 'does the pid exist' check is not enough across a restart: pids are
    reused, and adopting a stranger's process because it inherited the number
    would mean the stop button kills something else entirely.
    """
    try:
        out = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             f"(Get-Process -Id {int(pid)} -ErrorAction SilentlyContinue).ProcessName"],
            capture_output=True, text=True, timeout=20).stdout.strip().lower()
        return out.startswith("python")
    except Exception:
        return False


class Adopted:
    """A job this process did not start but is still responsible for."""

    def __init__(self, pid: int):
        self.pid = pid

    def poll(self):
        return None if _alive(self.pid) else 0

    def send_signal(self, _sig):
        self.terminate()

    def terminate(self):
        subprocess.run(["taskkill", "/PID", str(self.pid), "/T", "/F"],
                       capture_output=True)

    kill = terminate

    def wait(self, timeout=None):
        return 0


def save_registry() -> None:
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    with LOCK:
        rows = [{"kind": j["kind"], "game": j["game"], "pid": j["process"].pid,
                 "started": j["started"], "log": j["log"]}
                for j in JOBS.values() if j["process"].poll() is None]
    REGISTRY.write_text(json.dumps(rows, indent=1))


def load_registry() -> None:
    """Re-adopt jobs that outlived the last run of this panel.

    Training is the point of this tool and it takes hours, so closing the window
    must not orphan a run -- and reopening must not pretend nothing is happening.
    """
    try:
        rows = json.loads(REGISTRY.read_text())
    except (OSError, json.JSONDecodeError):
        return
    for row in rows:
        if not _alive(row["pid"]):
            continue
        key = job_key(row["kind"], row["game"])
        JOBS[key] = {"process": Adopted(row["pid"]), "log": row["log"],
                     "started": row["started"], "kind": row["kind"],
                     "game": row["game"], "handle": None, "adopted": True}
        print(f"  adopted {key} (pid {row['pid']}) from the last session", flush=True)


def python() -> str:
    return str(PY) if PY.exists() else sys.executable


# The arcade games are listed by importing the catalogue, which imports ale-py.
# Started with an interpreter that does not have it -- easy to do, this box has
# several -- that import raised inside the request handler, the socket closed
# with no response at all, and the page's own error handling turned a missing
# dependency into an empty job list with nothing said. The failure is now a
# value the page can show.
GAMES_PROBLEM: str | None = None


def known_games() -> list[str]:
    global GAMES_PROBLEM
    sys.path.insert(0, str(ROOT))
    try:
        from arcade.envs import CATALOGUE
    except Exception as exc:
        GAMES_PROBLEM = (f"{type(exc).__name__}: {exc} — this interpreter "
                         f"({sys.executable}) cannot load the arcade games")
        return ["doom", "brogue", "crafter"]
    GAMES_PROBLEM = None
    return sorted(CATALOGUE) + ["doom", "brogue", "crafter"]


def job_key(kind: str, game: str) -> str:
    return f"{kind}:{game}"


# -- the projects on this machine -------------------------------------------
PROJECT_JOBS: dict[str, dict] = {}


def project_rows() -> list[dict]:
    """Every project, with what is true about it right now.

    The status is deliberately three-valued rather than a boolean. "Started from
    here and answering" is a different fact from "something is answering on that
    port", and on this machine they come apart: five ports are claimed by two
    projects each, so a page that painted a green dot for an answering port would
    cheerfully report StudyLoop as up while the pak-law demo holds 8765.
    """
    verified = projects.snapshot()
    conflicts = projects.port_conflicts()
    rows = []
    for project in projects.CATALOGUE:
        row = projects.as_dict(project, verified)
        job = PROJECT_JOBS.get(project.id)
        ours = bool(job and job["process"].poll() is None)
        answering = projects.port_answering(project.port)
        row.update({
            "started_here": ours,
            "pid": job["process"].pid if ours else None,
            "seconds": round(time.time() - job["started"]) if ours else None,
            "port_answering": answering,
            "status": ("running" if ours and answering else
                       "starting" if ours else
                       "port in use" if answering else "stopped"),
            "shares_port_with": [i for i in conflicts.get(project.port or 0, [])
                                 if i != project.id],
            "log": job["log"] if job else None,
        })
        rows.append(row)
    return rows


def save_project_registry() -> None:
    rows = [{"id": pid, "pid": j["process"].pid, "started": j["started"],
             "log": j["log"]}
            for pid, j in PROJECT_JOBS.items() if j["process"].poll() is None]
    projects.JOB_FILE.parent.mkdir(parents=True, exist_ok=True)
    projects.JOB_FILE.write_text(json.dumps(rows, indent=1))


def load_project_registry() -> None:
    """Re-adopt project servers this panel started before it was last closed."""
    try:
        rows = json.loads(projects.JOB_FILE.read_text())
    except (OSError, json.JSONDecodeError):
        return
    for row in rows:
        if row["id"] not in projects.BY_ID or not _alive(row["pid"]):
            continue
        PROJECT_JOBS[row["id"]] = {"process": Adopted(row["pid"]),
                                   "started": row["started"], "log": row["log"],
                                   "adopted": True}
        print(f"  adopted project {row['id']} (pid {row['pid']})", flush=True)


def start_project(project_id: str) -> dict:
    """Start one project, exactly as its desktop shortcut would.

    The launcher comes from the catalogue; the request only names which row. A
    .bat gets its own console window, which is how these have always been run and
    means closing that window still stops the server.
    """
    project = projects.BY_ID.get(project_id)
    if project is None:
        return {"ok": False, "error": f"unknown project {project_id!r}"}
    existing = PROJECT_JOBS.get(project_id)
    if existing and existing["process"].poll() is None:
        return {"ok": False, "error": f"{project.name} was already started from here",
                "url": project_url(project)}
    if projects.port_answering(project.port):
        # Something already has the port. A second server on the same port fails
        # inside the launcher's own console window, where nobody sees it.
        others = [i for i in projects.port_conflicts().get(project.port, [])
                  if i != project_id]
        extra = f" (also claimed by {', '.join(others)})" if others else ""
        return {"ok": False,
                "error": f"port {project.port} is already answering{extra}; open it, "
                         f"or stop whatever is on it first",
                "url": project_url(project)}

    launcher = project.launcher
    if isinstance(launcher, str):
        path = Path(launcher)
        if not path.exists():
            return {"ok": False, "error": f"the launcher has moved: {launcher}"}
        args = ["cmd", "/c", str(path)]
        cwd = project.cwd or str(path.parent)
    else:
        args = list(launcher)
        cwd = project.cwd or str(ROOT)

    log = HERE / "logs" / f"project_{project_id}.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    handle = open(log, "a", encoding="utf-8")
    handle.write(f"\n=== {project_id} started "
                 f"{datetime.now(timezone.utc):%Y-%m-%d %H:%M:%SZ} ===\n")
    handle.flush()
    env = {**os.environ, "PYTHONUTF8": "1"}
    creation = 0
    if os.name == "nt":
        creation = subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NEW_PROCESS_GROUP
    try:
        process = subprocess.Popen(args, cwd=cwd, env=env, creationflags=creation)
    except OSError as exc:
        handle.close()
        return {"ok": False, "error": f"could not start it: {exc}"}
    PROJECT_JOBS[project_id] = {"process": process, "started": time.time(),
                                "log": str(log), "handle": handle}
    save_project_registry()
    return {"ok": True, "pid": process.pid, "url": project_url(project),
            "kind": project.kind}


def openable_urls() -> set[str]:
    """Every address the panel is allowed to hand to a browser.

    The desktop window has no address bar and no tabs, so a link in it has to be
    opened by this process instead. That turns "open a link" into "run a browser
    on a string from a web page", which is only safe if the string cannot be
    anything the page likes: the set is built from the catalogue, so a request
    can pick one of these and nothing else.
    """
    urls: set[str] = set()
    for project in projects.CATALOGUE:
        if project.port:
            urls.add(f"http://127.0.0.1:{project.port}/")
        if project.live:
            urls.add(project.live)
        urls.update(project.pages.values())
    verified = projects.snapshot().get("projects", {})
    for row in verified.values():
        if row.get("github"):
            urls.add(row["github"])
    return urls


def open_url(url: str) -> dict:
    allowed = openable_urls()
    if url not in allowed:
        return {"ok": False, "error": "that address is not one of this panel's links"}
    import webbrowser
    return {"ok": bool(webbrowser.open(url)), "url": url}


def project_url(project) -> str | None:
    return f"http://127.0.0.1:{project.port}/" if project.port else None


def stop_project(project_id: str) -> dict:
    project = projects.BY_ID.get(project_id)
    if project is None:
        return {"ok": False, "error": f"unknown project {project_id!r}"}
    job = PROJECT_JOBS.get(project_id)
    if not job or job["process"].poll() is not None:
        if projects.port_answering(project.port):
            return {"ok": False,
                    "error": f"something is answering on {project.port}, but this "
                             f"panel did not start it, so this panel will not kill "
                             f"it — close its own window"}
        return {"ok": False, "error": f"{project.name} is not running"}
    process = job["process"]
    try:
        # The launcher is a .bat holding a server: killing the shell alone leaves
        # the server behind, so the whole tree goes.
        subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                       capture_output=True, timeout=25)
        process.wait(timeout=10)
    except Exception:
        try:
            process.kill()
        except Exception:
            pass
    finally:
        try:
            if job.get("handle"):
                job["handle"].close()
        except Exception:
            pass
    PROJECT_JOBS.pop(project_id, None)
    save_project_registry()
    return {"ok": True, "stopped": project_id}


# Every training knob the panel may set, with the range it may set it to. The
# panel sends values, never flags: nothing a request contains becomes part of a
# command except as the value of a switch named here, and anything outside its
# range is refused rather than clamped, so a typo is visible instead of silently
# becoming a different experiment.
TRAIN_SCHEMA = {
    "steps": {"flag": "--steps", "type": int, "min": 10_000, "max": 50_000_000,
              "label": "training steps"},
    "envs": {"flag": "--envs", "type": int, "min": 1, "max": 32,
             "label": "parallel games"},
    "arch": {"flag": "--arch", "type": str, "choices": ("nature", "impala", "small"),
             "label": "architecture"},
    "width": {"flag": "--width", "type": int, "min": 1, "max": 8,
              "label": "channel multiplier"},
    "lr": {"flag": "--lr", "type": float, "min": 1e-6, "max": 1e-2,
           "label": "learning rate"},
    "entropy": {"flag": "--entropy", "type": float, "min": 0.0, "max": 0.2,
                "label": "entropy bonus"},
    "rollout": {"flag": "--rollout", "type": int, "min": 16, "max": 1024,
                "label": "rollout length"},
    "epochs": {"flag": "--epochs", "type": int, "min": 1, "max": 16,
               "label": "epochs per batch"},
    "minibatches": {"flag": "--minibatches", "type": int, "min": 1, "max": 32,
                    "label": "minibatches"},
    "lr_schedule": {"flag": "--lr-schedule", "type": str,
                    "choices": ("linear", "constant", "cosine", "warmup_cosine"),
                    "label": "lr schedule"},
    "device": {"flag": "--device", "type": str, "choices": ("auto", "cpu", "cuda"),
               "label": "device"},
    "seed": {"flag": "--seed", "type": int, "min": 0, "max": 10_000_000, "label": "seed"},
}


# Starting points per architecture, offered by the panel when the model changes.
# They are suggestions the form fills in, not rules: the wider trunks are slower
# per step and more easily destabilised early, so they start with a gentler rate
# and a warm-up, while the small one can afford more parallel games.
PRESETS = {
    "nature": {"lr": 0.00025, "entropy": 0.01, "envs": 12, "rollout": 128,
               "epochs": 4, "minibatches": 4, "lr_schedule": "linear", "width": 1},
    "impala": {"lr": 0.00015, "entropy": 0.01, "envs": 8, "rollout": 256,
               "epochs": 3, "minibatches": 8, "lr_schedule": "warmup_cosine", "width": 1},
    "small": {"lr": 0.0004, "entropy": 0.015, "envs": 16, "rollout": 128,
              "epochs": 4, "minibatches": 4, "lr_schedule": "linear", "width": 1},
}

SWEEPABLE = ("lr", "entropy", "arch", "width", "rollout", "epochs",
             "minibatches", "envs", "seed", "lr_schedule")


def build_train_args(config: dict) -> tuple[list[str], dict, str | None]:
    """Turn a config from the panel into command-line switches, or refuse it."""
    args: list[str] = []
    used: dict = {}
    for key, value in (config or {}).items():
        rule = TRAIN_SCHEMA.get(key)
        if rule is None:
            return [], {}, f"{key!r} is not a setting this panel knows"
        if value is None or value == "":
            continue
        try:
            typed = rule["type"](value)
        except (TypeError, ValueError):
            return [], {}, f"{rule['label']} must be a {rule['type'].__name__}"
        if "choices" in rule and typed not in rule["choices"]:
            return [], {}, f"{rule['label']} must be one of {', '.join(rule['choices'])}"
        if "min" in rule and typed < rule["min"]:
            return [], {}, f"{rule['label']} must be at least {rule['min']}"
        if "max" in rule and typed > rule["max"]:
            return [], {}, f"{rule['label']} must be at most {rule['max']}"
        args += [rule["flag"], str(typed)]
        used[key] = typed

    # Minibatches have to divide the batch, or PPO silently trains on ragged
    # slices and the last one is a different size every update.
    envs, rollout, minibatches = used.get("envs"), used.get("rollout"), used.get("minibatches")
    if envs and rollout and minibatches:
        if (envs * rollout) % minibatches:
            return [], {}, (f"{envs} games x {rollout} steps is {envs * rollout}, "
                            f"which {minibatches} minibatches do not divide evenly")
    return args, used, None


def start_job(kind: str, game: str, config: dict | None = None) -> dict:
    """Launch one job, refusing to start a second of the same kind for a game."""
    if game not in known_games():
        return {"ok": False, "error": f"unknown game {game!r}"}
    key = job_key(kind, game)
    with LOCK:
        live = JOBS.get(key)
        if live and live["process"].poll() is None:
            return {"ok": False, "error": f"{kind} is already running for {game}"}

        if kind == "train":
            if game in ("doom", "brogue", "crafter"):
                return {"ok": False,
                        "error": f"{game} is not one of the arcade runs; it has its own trainer"}
            used = {}
            extra, used, problem = build_train_args(config or {})
            if problem:
                return {"ok": False, "error": problem}
            # Each launch gets its own run directory. The trainer refuses to
            # write into one that already holds checkpoints -- it let an earlier
            # run's untrained checkpoint be overwritten silently -- so a panel
            # that always used runs_arcade/<game> could only ever start the
            # first run of a game, and would fail from the second onwards with
            # the error buried in a log file.
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            out_dir = ROOT / "runs_arcade" / f"{game}_{stamp}"
            args = [python(), "-m", "arcade.train", "--game", game,
                    "--out", str(out_dir)]
            if "--envs" not in extra:
                args += ["--envs", "12"]
            args += extra
            used["out"] = out_dir.name
            log = ROOT / "runs_arcade" / f"train_{game}_{stamp}.log"
        elif kind == "play":
            used = {}
            args = [python(), "-m", "observatory.live", "--game", game]
            log = HERE / "logs" / f"play_{game}.log"
        else:
            return {"ok": False, "error": f"unknown action {kind!r}"}

        log.parent.mkdir(parents=True, exist_ok=True)
        handle = open(log, "a", encoding="utf-8")
        handle.write(f"\n=== {kind} {game} started "
                     f"{datetime.now(timezone.utc):%Y-%m-%d %H:%M:%SZ} ===\n")
        handle.flush()
        env = {**os.environ, "PYTHONUTF8": "1"}
        creation = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
        process = subprocess.Popen(args, cwd=str(ROOT), stdout=handle,
                                   stderr=subprocess.STDOUT, env=env,
                                   creationflags=creation)
        JOBS[key] = {"process": process, "log": str(log), "started": time.time(),
                     "kind": kind, "game": game, "handle": handle,
                     "config": used if kind == "train" else {}}
    save_registry()
    return {"ok": True, "pid": process.pid, "log": str(log),
            "config": used if kind == "train" else {}}


def start_sweep(game: str, param: str, values: list, steps: int, envs: int,
                episodes: int) -> dict:
    """Queue one training run per value, one after another."""
    if game not in known_games():
        return {"ok": False, "error": f"unknown game {game!r}"}
    if param not in SWEEPABLE:
        return {"ok": False, "error": f"{param!r} cannot be swept"}
    cleaned = [str(v).strip() for v in values if str(v).strip()]
    if len(cleaned) < 2:
        return {"ok": False, "error": "a sweep needs at least two values to compare"}
    if len(cleaned) > 6:
        return {"ok": False, "error": "six arms is the most this will queue at once"}
    # Each value has to survive the same check a single run's value would.
    for value in cleaned:
        _, _, problem = build_train_args({param: value})
        if problem:
            return {"ok": False, "error": problem}
    if not (10_000 <= steps <= 20_000_000):
        return {"ok": False, "error": "steps per arm must be between 10,000 and 20,000,000"}

    key = job_key("sweep", game)
    with LOCK:
        live = JOBS.get(key)
        if live and live["process"].poll() is None:
            return {"ok": False, "error": f"a sweep is already running for {game}"}
        log = ROOT / "runs_arcade" / f"sweep_{game}_{param}.log"
        log.parent.mkdir(parents=True, exist_ok=True)
        handle = open(log, "a", encoding="utf-8")
        args = [python(), "-m", "arcade.sweep", "--game", game, "--param", param,
                "--values", ",".join(cleaned), "--steps", str(int(steps)),
                "--envs", str(int(envs)), "--episodes", str(int(episodes))]
        env = {**os.environ, "PYTHONUTF8": "1"}
        creation = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
        process = subprocess.Popen(args, cwd=str(ROOT), stdout=handle,
                                   stderr=subprocess.STDOUT, env=env,
                                   creationflags=creation)
        JOBS[key] = {"process": process, "log": str(log), "started": time.time(),
                     "kind": "sweep", "game": game, "handle": handle,
                     "config": {"param": param, "values": cleaned, "steps": steps}}
    save_registry()
    return {"ok": True, "pid": process.pid, "arms": cleaned}


def stop_job(kind: str, game: str) -> dict:
    key = job_key(kind, game)
    with LOCK:
        job = JOBS.get(key)
        if not job or job["process"].poll() is not None:
            return {"ok": False, "error": f"no {kind} running for {game}"}
        process = job["process"]
        # Ask first, insist second: a training run that is killed outright leaves
        # its worker processes orphaned and holding the game's shared memory.
        try:
            if os.name == "nt":
                process.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                process.terminate()
            process.wait(timeout=12)
        except Exception:
            process.kill()
        finally:
            try:
                if job.get("handle"):
                    job["handle"].close()
            except Exception:
                pass
    save_registry()
    return {"ok": True, "stopped": key}


def job_status() -> list[dict]:
    out = []
    with LOCK:
        for key, job in list(JOBS.items()):
            running = job["process"].poll() is None
            out.append({"key": key, "kind": job["kind"], "game": job["game"],
                        "running": running, "pid": job["process"].pid,
                        "seconds": round(time.time() - job["started"]),
                        "adopted": bool(job.get("adopted")),
                        "config": job.get("config") or {}, "log": job["log"]})
    return out


def refresh_snapshot() -> None:
    """Keep the data the page reads current, in this process rather than another.

    Running the collector as a separate long-lived process meant it served a
    snapshot built from the code it had imported at startup; doing it here keeps
    one thing responsible for one thing.
    """
    sys.path.insert(0, str(ROOT))
    while True:
        try:
            from observatory import collect
            import importlib
            importlib.reload(collect)
            collect.write(collect.snapshot())
        except Exception as exc:
            print(f"snapshot failed: {type(exc).__name__}: {exc}", flush=True)
        time.sleep(20)


def docs_path(path: str) -> str | None:
    """Where a /docs/... request maps to on disk, or None if it is not one.

    The page is served out of observatory/ and asks for the films at
    docs/media/..., where the dashboard keeps them. Served from here that was a
    404 for every clip on the overview -- quietly, because a card with no film
    falls back to a label rather than complaining.

    It is a function rather than a method so the path handling can be tested
    without a live socket, and so the one rule that matters -- nothing outside
    docs/ is reachable through this prefix -- is in one readable place.
    """
    clean = path.split("?", 1)[0].split("#", 1)[0]
    if not clean.startswith("/docs/"):
        return None
    base = (ROOT / "docs").resolve()
    target = (base / clean[len("/docs/"):].lstrip("/")).resolve()
    try:
        target.relative_to(base)
    except ValueError:
        return None
    return str(target)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(HERE), **kwargs)

    def translate_path(self, path):
        """Serve /docs/... from the repository, not from this folder."""
        return docs_path(path) or super().translate_path(path)

    def log_message(self, fmt, *args):  # quieter than the default
        if "/api/" in (self.path or ""):
            print(f"  {self.command} {self.path}", flush=True)

    # -- plumbing ---------------------------------------------------------
    def _json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _authorised(self) -> bool:
        return self.headers.get("X-Obs-Token") == TOKEN

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/jobs":
            schema = {k: {kk: (list(vv) if isinstance(vv, tuple) else vv)
                          for kk, vv in rule.items() if kk != "type"}
                      for k, rule in TRAIN_SCHEMA.items()}
            for key, rule in TRAIN_SCHEMA.items():
                schema[key]["kind"] = rule["type"].__name__
            games = known_games()
            return self._json({"jobs": job_status(), "games": games,
                               "schema": schema, "presets": PRESETS,
                               "sweepable": list(SWEEPABLE),
                               "problem": GAMES_PROBLEM})
        if path == "/api/demos":
            from observatory import demos as demo_index
            import importlib
            importlib.reload(demo_index)      # a film recorded since startup counts
            return self._json({"demos": demo_index.as_dicts()})
        if path == "/api/projects":
            return self._json({"projects": project_rows(),
                               "groups": projects.GROUPS,
                               "conflicts": {str(k): v for k, v
                                             in projects.port_conflicts().items()}})
        if path in ("/", "/index.html"):
            # The token is handed to the page it is meant for, and only that
            # page: another origin cannot read this response.
            html = (HERE / "index.html").read_text(encoding="utf-8")
            html = html.replace("</head>",
                                f'<script>window.OBS_TOKEN = "{TOKEN}";</script></head>')
            body = html.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        return super().do_GET()

    def do_POST(self):
        path = urlparse(self.path).path
        if not path.startswith("/api/"):
            return self._json({"ok": False, "error": "not found"}, 404)
        if not self._authorised():
            return self._json({"ok": False, "error": "bad or missing token"}, 403)
        length = int(self.headers.get("Content-Length") or 0)
        try:
            payload = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            return self._json({"ok": False, "error": "bad json"}, 400)
        game = str(payload.get("game", ""))

        if path == "/api/train/start":
            return self._json(start_job("train", game, payload.get("config") or {}))
        if path == "/api/train/stop":
            return self._json(stop_job("train", game))
        if path == "/api/play/start":
            return self._json(start_job("play", game))
        if path == "/api/play/stop":
            return self._json(stop_job("play", game))
        if path == "/api/sweep/start":
            return self._json(start_sweep(
                game, str(payload.get("param", "lr")),
                payload.get("values") or [],
                int(payload.get("steps") or 300_000),
                int(payload.get("envs") or 12),
                int(payload.get("episodes") or 5)))
        if path == "/api/open":
            return self._json(open_url(str(payload.get("url", ""))))
        if path == "/api/projects/start":
            return self._json(start_project(str(payload.get("project", ""))))
        if path == "/api/projects/stop":
            return self._json(stop_project(str(payload.get("project", ""))))
        if path == "/api/sweep/stop":
            return self._json(stop_job("sweep", game))
        return self._json({"ok": False, "error": "unknown action"}, 404)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8777)
    ap.add_argument("--open", action="store_true", help="open the page in a browser")
    args = ap.parse_args()

    load_registry()
    load_project_registry()
    threading.Thread(target=refresh_snapshot, daemon=True).start()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    url = f"http://127.0.0.1:{args.port}/"
    print(f"Game Playing AI Agents — control panel on {url}")
    print("bound to loopback only; actions need the token this page is given")
    if args.open:
        import webbrowser
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopping; any jobs started from here keep running")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
