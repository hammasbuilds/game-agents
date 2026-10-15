# game-agents

Three AI agents that play three real games you can download, built on a laptop
CPU. One learns from pixels, one plans without learning anything, and one plays
an ordinary Windows program through screenshots and keystrokes.

**[Live dashboard →](https://hammasbuilds.github.io/game-agents/)** ·
**[Analytics →](https://hammasbuilds.github.io/game-agents/analytics.html)** —
every figure on both is read from a run artefact in this repository, not typed in,
and the analytics page marks which differences are inside the noise of their own
measurement.
**[Kaggle notebook →](https://www.kaggle.com/code/muhammadhammas13/does-a-wider-network-help-a-doom-agent)**
— the same DOOM agent on a GPU, asking whether the laptop-sized network was a
compromise or was enough.

They deliberately share no method. The point of three is to show three ways of
getting a machine to play something — and what each one actually costs.

| | | |
|:---:|:---:|:---:|
| ![DOOM](docs/media/clip_doom.gif) | ![Crafter](docs/media/clip_crafter.gif) | ![Brogue](docs/media/clip_brogue.gif) |
| PPO from pixels, 12 kills in this episode | the planner, 8 achievements, no training | screenshots and keystrokes, reached depth 3 |

| project | game | how it plays | result |
|---|---|---|---|
| [01 — DOOM from pixels](projects/01-doom-pixel-rl) | ViZDoom (Freedoom data) | PPO trained from scratch on raw frames, CPU only | **9.80 kills/episode** vs 1.23 for a hand-written baseline, 30 held-out maps |
| [02 — Crafter, planned](projects/02-crafter-planner) | Crafter | tile decoding → map → goal ladder, **no training at all** | **12.73%** Crafter score vs 1.13% random; 15 of 22 achievements |
| [03 — Brogue, through the screen](projects/03-brogue-screen-agent) | Brogue CE | screenshots in, keystrokes out, no API | names 77–94% of the dungeon view, explores and descends |

Every game is free and open: ViZDoom ships Freedoom, Crafter is a pip install,
Brogue CE is a GPL release download. No ROMs, nothing commercial, nothing
patched. The games themselves are not committed — `scripts/get_brogue.py`
fetches Brogue, and the other two are Python packages.

## What each project is really about

**01** is about throughput. Written the obvious way the trainer ran at 153
steps/s while a single environment did 1,305, and four rounds of profiling each
disproved the obvious answer before the instrumented worker gave it up: a worker
sleeping in `recv()` pays a scheduler-tick wake-up on every step, and since
Windows 10 2004 the timer resolution is **per process**, so the fix belongs in
the worker, not the trainer. One line, 5.2×, and a 2M-step run that finishes in
an hour.

**02** is about whether a plan can stand in for a policy. It can, here: a goal
ladder with no weights reaches roughly what a trained world model reports on the
same benchmark. It is also about not cheating — Crafter offers a full semantic
map in its `info` dict, and the planner reads none of it, decoding the 64×64
frame instead at 99.99% tile accuracy (100% in daylight, 99.5% at midnight, where
the game blends in random noise that can only be removed in expectation).

**03** is about the gap between a game that wants to be automated and one that
does not. Brogue has no API, so the agent starts the process, finds the window,
screenshots the client area and posts keystrokes to that window handle — which
means they go to the game and never into whatever else is open. The hard part was
not the agent but the reading: Brogue stretches its 100×34 character grid over
the whole window, so cells are 9.08 × 16.68 pixels and nothing lands on an
integer lattice.

## What it cost to get there

Every number above came after the first version of that project was bad, and the
fixes came from watching, not from tuning. A few that are written up next to the
code they broke:

- A template atlas built the game's own way was **transposed**, because Crafter
  keeps textures in (x, y) and transposes only the finished canvas. 25% of tiles
  wrong, mostly grass read as stone.
- The Crafter planner walked past three trees to reach a cow eleven tiles away,
  because food was at 3/9 and "hungry" outranked "collect wood".
- It then died at step 223 having spent forty steps fleeing zombies **with nine
  unused stone in the inventory**. Three separate bugs stood between it and
  building a wall; the one that took longest to see was that `seal()` re-chose
  the most exposed side every step, and since the zombies moved, the agent turned
  back and forth and never placed a block.
- Having learned to seal itself in, it starved behind its own wall, because
  nothing opened the box again.
- Choosing between two decoders by "whichever matches better" compared cosine
  similarities across a three-channel and a one-channel space, where the smaller
  space always wins. Accuracy fell to 0.6% before the comparison was replaced
  with the sleep screen's exact algebraic signature.

## The dashboard

`docs/` is a static page — no build step, no server, no CDN — served at
[hammasbuilds.github.io/game-agents](https://hammasbuilds.github.io/game-agents/).
`ui/export.py` fills it from the run artefacts each project writes, so a result
the page shows is one some run produced; where a run is missing, the card says so
instead of showing a stale number. `ui/check_page.py` checks the page without
opening a browser: files it references but does not ship, CSS variables used but
never defined, anything loaded from a third party, and numbers typed into the
HTML rather than read from the data.

```bash
python ui/export.py && python ui/check_page.py
```

## Running them

```bash
python -m venv .venv && .venv/Scripts/activate      # or source .venv/bin/activate
pip install -r requirements.txt
pip install torch --index-url https://download.pytorch.org/whl/cpu

cd projects/01-doom-pixel-rl   && python train.py --scenario defend_the_center --steps 2000000
cd projects/02-crafter-planner && python evaluate.py --agent all --episodes 20
cd projects/03-brogue-screen-agent && python ../../scripts/get_brogue.py && python play.py
```

Everything here runs on a CPU. The DOOM run is the longest at under an hour on 12
cores; the other two are minutes.
