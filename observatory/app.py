"""Game Playing AI Agents as a desktop application.

    python -m observatory.app

Same page, same control server, in a window of its own: no browser, no address
to remember, no token to carry. The server still runs — it is what launches and
stops the runs — but it is started inside this process on a free port and bound
to loopback, and the window is pointed at it.

**Closing the window does not stop your training.** Runs are separate processes
and are written to a registry on disk, so the next launch adopts whatever is
still going rather than pretending the machine is idle. That is the whole reason
this is worth being an application rather than a page: a training run outlives
the thing you were watching it with.
"""
from __future__ import annotations

import argparse
import socket
import sys
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def free_port(preferred: int = 8777) -> int:
    for port in (preferred, 0):
        with socket.socket() as sock:
            try:
                sock.bind(("127.0.0.1", port))
                return sock.getsockname()[1]
            except OSError:
                continue
    raise RuntimeError("no port available")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=0, help="0 picks a free one")
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--height", type=int, default=880)
    ap.add_argument("--browser", action="store_true",
                    help="open in the default browser instead of a window")
    args = ap.parse_args()

    sys.path.insert(0, str(ROOT))
    from observatory import server as control

    port = args.port or free_port()
    control.load_registry()
    # Project servers started from the panel outlive the window too, and a panel
    # that forgot them would offer to start a second one on the same port.
    control.load_project_registry()
    threading.Thread(target=control.refresh_snapshot, daemon=True).start()
    httpd = ThreadingHTTPServer(("127.0.0.1", port), control.Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{port}/"
    print(f"control server on {url}")

    if args.browser:
        import webbrowser
        webbrowser.open(url)
        print("press Ctrl+C to stop the panel; any runs you started keep going")
        try:
            threading.Event().wait()
        except KeyboardInterrupt:
            pass
        return

    try:
        import webview
    except ImportError:
        raise SystemExit("pywebview is not installed: pip install pywebview, "
                         "or pass --browser")

    webview.create_window("Game Playing AI Agents", url,
                          width=args.width, height=args.height,
                          min_size=(900, 620), background_color="#0a0c10")
    # Closing the window ends this process; the runs it started are their own
    # processes and carry on, which is what the registry is for.
    webview.start()
    print("window closed; any runs you started are still going")


if __name__ == "__main__":
    main()
