"""Collect every project's results and sample frames into docs/ for the dashboard.

    python ui/export.py

The dashboard is a static page so that it works from a GitHub Pages URL with no
server and no build step. Everything it shows is produced here, from the same
run artefacts the READMEs quote, so the page cannot drift into claiming a number
no run produced: if a result is missing, the card says so rather than showing a
stale one.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MEDIA = DOCS / "media"
DATA = DOCS / "data"


def read_json(path: Path):
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None


# -- media ----------------------------------------------------------------
def doom_frames(count: int = 6) -> list[str]:
    """A strip of what the DOOM policy actually sees, and the frame beside it."""
    sys.path.insert(0, str(ROOT / "projects" / "01-doom-pixel-rl"))
    try:
        import torch
        from doomagent.env import DoomEnv, EnvConfig
        from doomagent.model import ActorCritic
    except ImportError:
        return []
    weights = ROOT / "projects" / "01-doom-pixel-rl" / "runs" / "defend_the_center" / "policy.pt"
    if not weights.exists():
        return []
    blob = torch.load(weights, map_location="cpu", weights_only=False)
    model = ActorCritic(tuple(blob["obs_shape"]), blob["n_actions"])
    model.load_state_dict(blob["model"])
    model.eval()

    env = DoomEnv(EnvConfig(scenario="defend_the_center", seed=900001))
    out = []
    try:
        obs = env.reset()
        shots = []
        for step in range(260):
            action, _, _ = model.act(torch.from_numpy(np.ascontiguousarray(obs[None])),
                                     greedy=True)
            if step % 30 == 0 and len(shots) < count:
                state = env.game.get_state()
                if state is not None:
                    shots.append(np.transpose(state.screen_buffer, (1, 2, 0)).copy())
            obs, _, done = env.step(int(action[0]))
            if done:
                break
        for i, shot in enumerate(shots):
            path = MEDIA / f"doom_{i}.png"
            Image.fromarray(shot).resize((320, 240), Image.NEAREST).save(path)
            out.append(path.name)
    finally:
        env.close()
    return out


def crafter_frames(count: int = 6) -> tuple[list[str], list[str]]:
    """Frames from a planner episode, plus what the decoder made of each."""
    sys.path.insert(0, str(ROOT / "projects" / "02-crafter-planner"))
    try:
        import crafter
        from crafteragent.agent import PlannerAgent
    except ImportError:
        return [], []
    env = crafter.Env(seed=500, length=400)
    frame = env.reset()
    agent = PlannerAgent()
    agent.reset()
    frames, decoded = [], []
    for step in range(300):
        action = agent.act(frame)
        if step % 45 == 0 and len(frames) < count:
            path = MEDIA / f"crafter_{len(frames)}.png"
            Image.fromarray(frame).resize((256, 256), Image.NEAREST).save(path)
            frames.append(path.name)
            grid = agent.perceiver(frame).grid_names()
            decoded.append("\n".join(
                " ".join(str(grid[x, y]).split("+")[0][:4].ljust(4)
                         for x in range(grid.shape[0]))
                for y in range(grid.shape[1])))
        frame, _, done, _ = env.step(action)
        if done:
            break
    return frames, decoded


def crafter_episode(steps: int = 90, every: int = 2) -> dict:
    """A short episode kept frame by frame, with the goal chosen at each one.

    This is what the planner looks like from the inside: the dashboard steps
    through it, so the goal ladder can be watched switching from "collect wood"
    to "shelter" as the light goes.
    """
    sys.path.insert(0, str(ROOT / "projects" / "02-crafter-planner"))
    try:
        import crafter
        from crafteragent.agent import PlannerAgent
    except ImportError:
        return {}
    env = crafter.Env(seed=502, length=steps + 2)
    frame = env.reset()
    agent = PlannerAgent()
    agent.reset()
    out = {"frames": [], "goals": [], "daylight": [], "inventory": [], "step": []}
    for step in range(steps):
        action = agent.act(frame)
        if step % every == 0:
            name = f"ep_{len(out['frames']):03d}.png"
            Image.fromarray(frame).resize((128, 128), Image.NEAREST).save(MEDIA / name)
            inv = {k: v for k, v in agent.inventory.items() if v and k not in
                   ("health", "food", "drink", "energy")}
            out["frames"].append(name)
            out["goals"].append(agent.chosen)
            out["daylight"].append(round(agent.perceiver.daylight_now, 2))
            out["inventory"].append(inv)
            out["step"].append(step)
        frame, _, done, _ = env.step(action)
        if done:
            break
    return out


def brogue_frames(count: int = 4) -> list[str]:
    captured = sorted((ROOT / "projects" / "03-brogue-screen-agent" / "runs" / "frames")
                      .glob("*.png"))
    out = []
    for i, src in enumerate(captured[::max(1, len(captured) // count)][:count]):
        path = MEDIA / f"brogue_{i}.png"
        Image.open(src).resize((606, 378), Image.LANCZOS).save(path)
        out.append(path.name)
    return out


# -- results --------------------------------------------------------------
def collect() -> dict:
    doom_eval = read_json(ROOT / "projects/01-doom-pixel-rl/runs/defend_the_center/eval.json")
    doom_hist = read_json(ROOT / "projects/01-doom-pixel-rl/runs/defend_the_center/history.json")
    doom_train = read_json(ROOT / "projects/01-doom-pixel-rl/runs/defend_the_center/train_summary.json")
    kaggle = read_json(ROOT / "projects/01-doom-pixel-rl/runs_kaggle/width_comparison.json")
    crafter_eval = read_json(ROOT / "projects/02-crafter-planner/runs/eval_all.json")
    crafter_perc = read_json(ROOT / "projects/02-crafter-planner/runs/perception.json")
    ab_head = read_json(ROOT / "projects/02-crafter-planner/runs/ab_head.json")
    ab_new = read_json(ROOT / "projects/02-crafter-planner/runs/ab_new.json")
    brogue_play = read_json(ROOT / "projects/03-brogue-screen-agent/runs/play.json")
    brogue_explorer = read_json(ROOT / "projects/03-brogue-screen-agent/runs/play_explorer.json")

    curve = []
    if doom_hist:
        for row in doom_hist:
            if row.get("return_mean") is not None:
                curve.append({"steps": row["steps"], "return": round(row["return_mean"], 2)})

    return {
        "generated": subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                                    capture_output=True, text=True).stdout.strip(),
        "doom": {"eval": doom_eval, "curve": curve[::2], "training": doom_train,
                 "kaggle": kaggle},
        "crafter": {"eval": crafter_eval, "perception": crafter_perc,
                    "ab": {"head": ab_head, "new": ab_new}},
        "brogue": {"play": brogue_play, "explorer": brogue_explorer},
    }


def main() -> None:
    MEDIA.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)

    media = {"doom": [], "crafter": [], "crafter_decoded": [], "brogue": []}
    try:
        media["doom"] = doom_frames()
    except Exception as exc:                      # a missing game must not stop the page
        print(f"doom frames skipped: {exc}")
    try:
        media["crafter"], media["crafter_decoded"] = crafter_frames()
    except Exception as exc:
        print(f"crafter frames skipped: {exc}")
    try:
        payload_episode = crafter_episode()
    except Exception as exc:
        payload_episode = {}
        print(f"crafter episode skipped: {exc}")
    try:
        media["brogue"] = brogue_frames()
    except Exception as exc:
        print(f"brogue frames skipped: {exc}")

    payload = collect()
    payload["media"] = media
    payload["episode"] = payload_episode
    payload["iterations"] = read_json(DATA / "iterations.json")
    payload["clips"] = sorted(p.name for p in MEDIA.glob("clip_*"))
    (DATA / "results.json").write_text(json.dumps(payload, indent=1))
    # The same payload as a script, so the page also works when opened straight
    # off disk: fetch() of a local JSON file is blocked by the browser, and a
    # dashboard that only renders behind a web server is one more thing to run.
    (DATA / "results.js").write_text(
        "window.RESULTS = " + json.dumps(payload, indent=1) + ";\n")
    print(f"wrote {DATA / 'results.json'} and results.js")
    for key, names in media.items():
        if key != "crafter_decoded":
            print(f"  {key}: {len(names)} frames")


if __name__ == "__main__":
    main()
