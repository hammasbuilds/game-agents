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


def known_games() -> list[str]:
    sys.path.insert(0, str(ROOT))
    from arcade.envs import CATALOGUE
    return sorted(CATALOGUE) + ["doom", "brogue", "crafter"]


def job_key(kind: str, game: str) -> str:
    return f"{kind}:{game}"


def start_job(kind: str, game: str) -> dict:
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
            args = [python(), "-m", "arcade.train", "--game", game, "--envs", "12"]
            log = ROOT / "runs_arcade" / f"train_{game}.log"
        elif kind == "play":
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
                     "kind": kind, "game": game, "handle": handle}
    save_registry()
    return {"ok": True, "pid": process.pid, "log": str(log)}


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
                        "adopted": bool(job.get("adopted")), "log": job["log"]})
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


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(HERE), **kwargs)

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
            return self._json({"jobs": job_status(), "games": known_games()})
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
            return self._json(start_job("train", game))
        if path == "/api/train/stop":
            return self._json(stop_job("train", game))
        if path == "/api/play/start":
            return self._json(start_job("play", game))
        if path == "/api/play/stop":
            return self._json(stop_job("play", game))
        return self._json({"ok": False, "error": "unknown action"}, 404)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8777)
    ap.add_argument("--open", action="store_true", help="open the page in a browser")
    args = ap.parse_args()

    load_registry()
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
