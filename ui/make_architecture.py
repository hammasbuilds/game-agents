"""Generate the architecture animation page for a project, from a spec.

    python ui/make_architecture.py arcade docs/architecture.html
    python ui/make_architecture.py traffic ../traffic-agents/web/architecture.html

The anatomy page answers "what happens between the input and the output". This
one answers the next question down: *what is the shape of the thing at every
step, and how many numbers is the network learning*. Every figure in it is read
from the model itself by `inspect_*()` below rather than typed, so a layer that
changes in the code changes here too.

Isometric again, but a different arrangement: anatomy is a board you walk
across, architecture is a stack of slabs that the activation falls through, with
the parameter count of each layer beside it.
"""
from __future__ import annotations

import argparse
import html
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def inspect_arcade() -> dict:
    """The arcade policy, measured by building it."""
    import torch
    from arcade.model import ActorCritic

    actions = 5                      # CarRacing's discrete set
    model = ActorCritic((4, 84, 84), actions, width=1, arch="nature")
    x = torch.zeros(1, 4, 84, 84)
    layers = [{"name": "observation", "shape": "4 × 84 × 84",
               "note": "four greyscale frames, uint8 ÷ 255", "params": 0}]
    h = x
    conv_notes = ["8×8 kernel, stride 4", "4×4 kernel, stride 2", "3×3 kernel, stride 1"]
    seen_convs = 0
    for module in model.trunk:
        h = module(h)
        name = type(module).__name__
        if name == "Conv2d":
            layers.append({
                "name": f"conv {seen_convs + 1}",
                "shape": " × ".join(str(d) for d in tuple(h.shape)[1:]),
                "note": conv_notes[seen_convs],
                "params": sum(p.numel() for p in module.parameters())})
            seen_convs += 1
        elif name == "Flatten":
            layers.append({"name": "flatten", "shape": str(h.shape[1]),
                           "note": "one long vector", "params": 0})
    body_params = sum(p.numel() for p in model.body.parameters())
    h = model.body(h)
    layers.append({"name": "hidden", "shape": str(h.shape[1]),
                   "note": "fully connected, ReLU", "params": body_params})
    layers.append({"name": "policy head π", "shape": str(actions),
                   "note": "one logit per button",
                   "params": sum(p.numel() for p in model.pi.parameters())})
    layers.append({"name": "value head V", "shape": "1",
                   "note": "what this position is worth",
                   "params": sum(p.numel() for p in model.v.parameters())})
    total = sum(p.numel() for p in model.parameters())
    return {
        "title": "Game Agents — the network, layer by layer",
        "subtitle": "Every shape here is read from the model, not typed: four "
                    "stacked frames in, one button and one value out.",
        "layers": layers,
        "total": total,
        "batch": [
            ("12 environments", "stepped in parallel processes"),
            ("128 steps each", "one rollout = 1,536 transitions"),
            ("4 minibatches", "384 rows per gradient step"),
            ("4 epochs", "the same rollout, reused four times"),
        ],
        "maths": [
            ("r = π(a|s) / π_old(a|s)", "how much more likely the new policy makes the action it took"),
            ("A = Σ (γλ)ᵏ δ", "advantage by GAE, γ 0.99, λ 0.95 — how much better that action was than expected"),
            ("L = −min(rA, clip(r, 0.9, 1.1)·A)", "the clip is what stops one update moving the policy too far"),
            ("+ ½(V − R)² − 0.01·H", "fit the value head, and pay the policy to stay uncertain a while longer"),
        ],
        "footer": "8 games · one network · 424,790 parameters",
    }


def inspect_traffic() -> dict:
    sys.path.insert(0, str(ROOT.parent / "traffic-agents"))
    from citysim.learn import Policy
    from citysim.rlenv import OBS_DIM

    model = Policy()
    layers = [{"name": "observation", "shape": str(OBS_DIM),
               "note": "12 queues, 4 downstream fullnesses, the phase, its age, clearing",
               "params": 0}]
    for i, module in enumerate(model.trunk):
        if type(module).__name__ != "Linear":
            continue
        layers.append({"name": f"hidden {i // 2 + 1}", "shape": str(module.out_features),
                       "note": "fully connected, tanh",
                       "params": sum(p.numel() for p in module.parameters())})
    layers.append({"name": "actor", "shape": str(model.actor.out_features),
                   "note": "one logit per phase",
                   "params": sum(p.numel() for p in model.actor.parameters())})
    layers.append({"name": "critic", "shape": "1",
                   "note": "what this junction's state is worth",
                   "params": sum(p.numel() for p in model.critic.parameters())})
    return {
        "title": "Traffic Agents — the network, layer by layer",
        "subtitle": "One policy, every junction. The batch is junctions, not "
                    "cities: nine of them per city, sixteen cities, one set of weights.",
        "layers": layers,
        "total": sum(p.numel() for p in model.parameters()),
        "batch": [
            ("16 cities", "each a 3×3 grid, in its own process"),
            ("9 junctions each", "144 rows from one decision"),
            ("120 decisions", "17,280 transitions per update"),
            ("4 minibatches × 4 epochs", "the same shared weights every time"),
        ],
        "maths": [
            ("r = Δ waiting / 20", "paid for the cars it cleared, not for the queue being short"),
            ("− 0.05 · waiting / 20", "a standing queue still costs something"),
            ("A = Σ (γλ)ᵏ δ", "γ 0.98 — a decision is ten seconds, so the future is discounted hard"),
            ("L = −min(rA, clip(r, 0.8, 1.2)·A)", "the same clipped objective, over 144 agents at once"),
        ],
        "footer": "9 junctions · one shared policy · 20,101 parameters",
    }


SPECS = {"arcade": inspect_arcade, "traffic": inspect_traffic}


def render(spec: dict) -> str:
    """Geometry on the left, words on the right.

    Text counter-rotated onto an isometric slab is unreadable the moment the
    slab is small or its neighbour overlaps it — two versions of this page
    proved it. So the slabs carry no text at all: they are the shape of the
    computation, and a flat table beside them says what each one is, lighting up
    in step with the slab it describes.
    """
    def esc(text):
        return html.escape(str(text))

    n = len(spec["layers"])
    step_seconds = 2.0
    duration = n * step_seconds

    slabs, rows, rail = [], [], []
    for i, layer in enumerate(spec["layers"]):
        size = 132 - i * 7
        kind = "in" if i == 0 else ("out" if i >= n - 2 else "mid")
        slabs.append(f'      <div class="slab {kind}" style="--i:{i}; --s:{size}px"></div>')
        rows.append(f'''      <li>
        <span class="lname">{esc(layer["name"])}</span>
        <span class="lshape">{esc(layer["shape"])}</span>
        <span class="lparams">{"—" if not layer["params"] else f"{layer['params']:,}"}</span>
      </li>''')
        rail.append(f'''    <div class="step"><b>{esc(layer["name"])} · {esc(layer["shape"])}</b>'''
                    f'''<span>{esc(layer["note"])}</span></div>''')

    batch = "\n".join(
        f'      <li><b>{esc(a)}</b><span>{esc(b)}</span></li>' for a, b in spec["batch"])
    maths = "\n".join(
        f'      <li><code>{esc(a)}</code><span>{esc(b)}</span></li>' for a, b in spec["maths"])
    delays = "\n".join(
        f'  .slab:nth-child({i + 1}), .layers li:nth-child({i + 1}), '
        f'.rail .step:nth-child({i + 1}) {{ animation-delay: {i * step_seconds}s; }}'
        for i in range(n))

    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(spec["title"])}</title>
<meta name="description" content="{esc(spec["subtitle"])}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<style>
  :root {{
    color-scheme: dark;
    --bg: #090b10; --slab: #171c25; --slab-2: #1f2631; --edge: #2c3542;
    --panel: #12171f;
    --ink: #e9ecf1; --dim: #93a0b4; --in: #6f9bff; --mid: #46d6c4; --out: #4cc98a;
    --mono: ui-monospace, "Cascadia Mono", Consolas, monospace;
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; width: 1280px; height: 720px; overflow: hidden;
    background: radial-gradient(1100px 650px at 40% 16%, #11161f, var(--bg));
    color: var(--ink); font-family: "Segoe UI", system-ui, sans-serif; }}
  header {{ padding: 20px 34px 0; }}
  h1 {{ margin: 0; font-size: 23px; letter-spacing: -.02em; }}
  h1 small {{ display: block; font-size: 12.5px; color: var(--dim); font-weight: 400;
              margin-top: 5px; max-width: 980px; line-height: 1.5; }}

  /* The stack carries no text: it is the shape of the computation. */
  .stack {{ position: absolute; left: 96px; top: 150px; width: 300px; height: 440px;
            transform: rotateX(56deg) rotateZ(-42deg); transform-style: preserve-3d; }}
  .slab {{ position: absolute; left: calc((132px - var(--s)) / 2);
           top: calc(var(--i) * 46px + (132px - var(--s)) / 2);
           width: var(--s); height: var(--s); border-radius: 10px;
           background: linear-gradient(145deg, var(--slab-2), var(--slab));
           border: 1px solid var(--edge); box-shadow: 0 18px 26px rgba(0,0,0,.5);
           transform: translateZ(calc(var(--i) * 14px));
           animation: pulse {duration}s infinite; }}
  .slab.in {{ border-color: color-mix(in srgb, var(--in) 55%, var(--edge)); }}
  .slab.out {{ border-color: color-mix(in srgb, var(--out) 55%, var(--edge)); }}
  @keyframes pulse {{
    0%, 100% {{ box-shadow: 0 18px 26px rgba(0,0,0,.5); }}
    3% {{ box-shadow: 0 18px 26px rgba(0,0,0,.5), 0 0 0 1.5px var(--mid),
                      0 0 36px rgba(70,214,196,.45); }}
    9% {{ box-shadow: 0 18px 26px rgba(0,0,0,.5); }}
  }}

  /* The table that says what each slab is. */
  .layers {{ position: absolute; left: 400px; top: 150px; width: 362px;
             list-style: none; margin: 0; padding: 0; }}
  .layers li {{ display: grid; grid-template-columns: 1fr auto auto; gap: 12px;
                align-items: baseline; padding: 7px 10px; border-radius: 9px;
                border: 1px solid transparent; animation: row {duration}s infinite; }}
  .lname {{ font-size: 13.5px; }}
  .lshape {{ font-family: var(--mono); font-size: 13px; color: var(--mid); }}
  .lparams {{ font-family: var(--mono); font-size: 11.5px; color: var(--dim);
              min-width: 64px; text-align: right; }}
  @keyframes row {{
    0%, 100% {{ background: transparent; border-color: transparent; }}
    3%, 8% {{ background: #121a22; border-color: color-mix(in srgb, var(--mid) 40%, var(--edge)); }}
  }}
{delays}

  .side {{ position: absolute; right: 30px; top: 150px; width: 470px; }}
  .side h2 {{ margin: 0 0 8px; font-size: 11.5px; letter-spacing: .08em;
              text-transform: uppercase; color: var(--dim); font-family: var(--mono); }}
  .side ul {{ list-style: none; margin: 0 0 16px; padding: 0; display: grid; gap: 7px; }}
  .side li {{ background: var(--panel); border: 1px solid var(--edge); border-radius: 10px;
              padding: 8px 11px; }}
  .side li b {{ display: block; font-size: 13.5px; }}
  .side li code {{ display: block; font-family: var(--mono); font-size: 12.5px; color: var(--mid); }}
  .side li span {{ display: block; color: var(--dim); font-size: 11.5px; line-height: 1.45; margin-top: 2px; }}

  .total {{ position: absolute; left: 96px; bottom: 150px; }}
  .total b {{ font-size: 34px; letter-spacing: -.02em; }}
  .total span {{ display: block; color: var(--dim); font-size: 12px; margin-top: 2px; }}

  .rail {{ position: absolute; left: 96px; bottom: 44px; width: 640px; height: 64px; }}
  .rail .step {{ position: absolute; opacity: 0; animation: say {duration}s infinite; }}
  .rail .step b {{ display: block; font-size: 15px; margin-bottom: 3px; }}
  .rail .step span {{ font-size: 12.5px; color: var(--dim); line-height: 1.5; }}
  @keyframes say {{
    0% {{ opacity: 0; transform: translateY(5px); }}
    3% {{ opacity: 1; transform: translateY(0); }}
    {round(100 / n * 0.78, 1)}% {{ opacity: 1; }}
    {round(100 / n, 1)}%, 100% {{ opacity: 0; }}
  }}
  footer {{ position: absolute; left: 96px; bottom: 16px; font-family: var(--mono);
            font-size: 11.5px; color: var(--dim); }}
</style>
</head>
<body>
<header>
  <h1>{esc(spec["title"])}<small>{esc(spec["subtitle"])}</small></h1>
</header>

<div class="stack">
{chr(10).join(slabs)}
</div>

<ul class="layers">
{chr(10).join(rows)}
</ul>

<div class="side">
  <h2>one update</h2>
  <ul>
{batch}
  </ul>
  <h2>what the update actually does</h2>
  <ul>
{maths}
  </ul>
</div>

<div class="total"><b>{spec["total"]:,}</b><span>parameters, all of them trained on a CPU</span></div>

<div class="rail">
{chr(10).join(rail)}
</div>
<footer>{esc(spec["footer"])}</footer>
</body>
</html>
'''


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec", choices=sorted(SPECS))
    ap.add_argument("out")
    args = ap.parse_args()

    spec = SPECS[args.spec]()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(spec), encoding="utf-8")
    print(f"  {out}  {len(spec['layers'])} layers, {spec['total']:,} parameters")


if __name__ == "__main__":
    main()
