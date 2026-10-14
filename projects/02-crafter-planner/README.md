# 02 — Crafter, planned rather than learned

[Crafter](https://github.com/danijar/crafter) is a 2D survival game with 22
achievements that form a dependency chain: wood before a table, a table before a
pickaxe, a pickaxe before stone, stone and coal and iron before an iron sword.
Agents are normally *trained* on it. This one is not — it has no weights, no
gradients and no reward signal. It reads the screen, keeps a map, and picks a
goal.

| | |
|---|---|
| **Input** | the 64 × 64 × 3 frame, and nothing else |
| **Output** | one of Crafter's 17 actions |
| **Method** | tile decoding → map stitching → an ordered goal ladder → BFS |
| **Training** | none |

## Result

20 episodes, seeds 500–509, step limit 3,000. Crafter's score is the geometric
mean of the per-achievement success rates, which punishes an agent that masters
a few and ignores the rest.

| agent | score | reward | distinct achievements | mean steps survived |
|---|---:|---:|---:|---:|
| random | 1.13% | 0.90 | 5 | 145 |
| forager (wander and press `do`) | 1.25% | 1.70 | 5 | 180 |
| **planner** | **12.73%** | **7.90** | **15** | **255** |

For scale, the numbers published with the benchmark put a trained PPO at ~4.6%
and DreamerV3 at ~14%, with human experts at ~50%.

## It plays from pixels, and here is the number

Crafter hands an agent a full semantic map of the world, the player's position
and the inventory in its `info` dict. None of that reaches the planner. The only
file that touches it is `perception_check.py`, which exists to score the decoder:

```
$ python perception_check.py --episodes 2 --steps 300
 tile accuracy      all 0.9999   day 1.0   dusk 1.0   night 1.0   midnight 0.9947
 inventory slots    1.0
```

Midnight is the only bucket below perfect, and for a reason worth stating: below
half daylight Crafter blends a vignetted field of **random** noise into the view.
The decoder inverts the rest of the lighting exactly — PIL's colour enhance and
the tint are both affine per pixel, so the whole day/night transform is
`observed = M · true + k` with a known 3×3 M — but noise can only be removed in
expectation, so 0.5% of tiles at midnight are read wrong.

Four bugs were found getting there, each one recorded next to the code it broke:

- **The atlas was transposed.** Crafter keeps textures in (x, y) and transposes
  only the finished canvas. Templates built the game's own way are therefore
  rotated relative to the frame. Cost: 25% of tiles, mostly grass read as stone.
- **Digits were matched without the icon behind them.** The HUD draws the count
  *over* the item sprite, so matching the digit against digit-on-black read 5, 6
  and 7 as 4. Templates are whole cells now.
- **A confidence comparison across two feature spaces.** The sleep screen needs a
  one-channel decode and the normal path three; cosine similarity is
  systematically higher in the smaller space, so "whichever matches better"
  picked *sleep* for every frame and dropped accuracy to 0.6%. The sleep overlay
  has an exact algebraic signature instead (R = G, B − R = 8).
- **Deep night read as sleep.** The saturation threshold that preceded that
  signature could not tell them apart.

The agent also works out its own achievements — a pickaxe appearing in the HUD
*is* `make_wood_pickaxe` — rather than reading them from `info`. Over 10
episodes that inference matched the game's own record exactly: **precision 1.0,
recall 1.0**.

## What the traces changed

Every jump in the score came from watching an episode and fixing what it showed,
not from tuning a constant.

| | score | what the trace said |
|---|---:|---|
| first working version | 1.8% | 78% of steps spent exploring, back and forth over the same twenty tiles |
| committed exploration | — | it now covered ground, and died on the first night |
| urgency-ordered goals | 14.1% | it had been walking past three trees to reach a cow eleven tiles away, because food was at 3/9 |
| night shelter | 13.9% | forty steps of `flee`, ten zombies on screen, dead at step 223 **with nine unused stone in the inventory** |

The shelter work is the part worth reading (`crafteragent/shelter.py`). Running
from zombies does not work in Crafter — they move as fast as the player and spawn
ahead of it — but a sealed tile is safe, because they cannot path through stone.
Getting that to actually happen took three fixes, each a bug the score alone
would never have located:

1. `seal()` re-chose the most exposed side every step, and since the zombies
   moved, the agent turned, turned again, and never placed a block. Eight
   episodes ended with 4–9 stone in hand and `steps_sealed = 0`.
2. The plan committed to "go mine more stone" and kept mining for thirty steps
   while seven stone sat in the inventory, because that had been the right answer
   once. Sealing where you stand is now checked every step, not only when the
   plan goes stale.
3. Then it sealed itself in and **starved**, because nothing opened the box
   again. Hence `break_out`: at dawn, or at food 0, mine back out.

## Files

```
evaluate.py              the table above; --agent all
perception_check.py      scores the decoder against the game's own tile map
trace.py                 one episode, step by step, with the goal it chose
diagnose.py              how episodes end, and what the agent was doing last
crafteragent/perceive.py pixels -> tiles, facing, inventory
crafteragent/memory.py   stitches the 9x7 glimpses into a map by dead reckoning
crafteragent/navigate.py BFS, and committed frontier exploration
crafteragent/shelter.py  surviving the night
crafteragent/agent.py    the goal ladder
crafteragent/achievements.py  what it believes it has achieved, from the HUD
```

## Running it

```bash
PYTHONUTF8=1 pip install crafter        # its setup.py reads README as cp1252 on Windows
python evaluate.py --agent all --episodes 20
python perception_check.py --episodes 3
python trace.py --seed 500 --tail 40
```
