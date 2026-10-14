# 01 — DOOM from pixels

A policy trained from scratch on raw frames of DOOM, on a CPU, in under an hour.

The game is [ViZDoom](https://github.com/Farama-Foundation/ViZDoom), which embeds
the original DOOM engine and ships the **Freedoom** data files, so nothing
commercial is needed to run it. The agent sees what a player sees — a stack of
four greyscale frames — and presses one of three buttons.

| | |
|---|---|
| **Input** | 4 × 60 × 80 greyscale frames, i.e. the screen, downsampled |
| **Output** | one of `turn left`, `turn right`, `attack` |
| **Learning** | PPO, written out in `doomagent/ppo.py`, 219,476 parameters |
| **Hardware** | CPU only — 12 game processes, no GPU at any point |

## Result

`defend_the_center`: the player stands in the middle of a room, monsters close in
from every side, and the score is kills minus one for dying. 30 held-out
episodes, seeds the policy never trained on, every agent given the same 30 maps:

| agent | mean return | sd | min | max | steps survived |
|---|---:|---:|---:|---:|---:|
| random | 0.00 | 0.91 | −1 | 2 | 78 |
| spray (turn-and-shoot, hand written) | 1.23 | 0.82 | 0 | 2 | 90 |
| **PPO, greedy** | **9.80** | 1.47 | 6 | 12 | 181 |
| PPO, sampled | 9.23 | 1.33 | 7 | 12 | 168 |

It kills about eight more monsters per episode than the scripted baseline and
stays alive twice as long. The worst of its thirty episodes (6) is better than
the best of either baseline (2).

Training: 2,000,000 agent steps (8,000,000 game tics) in **3,531 seconds**, mean
return over the last 100 training episodes rising from 2.0 to 9.5.

```
$ python train.py --scenario defend_the_center --steps 2000000 --envs 12
u10/1302   steps=15360    return=1.99  sps=554  ent=1.01
u390/1302  steps=599040   return=6.23  sps=576  ent=0.34
u970/1302  steps=1489920  return=9.00  sps=589  ent=0.29
u1302/1302 steps=1999872  return=9.50  sps=577  ent=0.24
```

## The thing that made it possible

The first working version trained at **153 steps/s** while a single environment
in the same process ran at 1,305. Four profiling rounds, each disproving the
obvious answer:

1. *The pipes are carrying too much.* Workers were sending float32 frame
   **stacks**; switching to a single uint8 frame cut the payload 16× and changed
   throughput by **nothing**.
2. *The machine is busy.* It was 17% idle, with a GPU job on it that was not
   using the cores.
3. *Windows' 15.6 ms timer.* Raising the timer resolution in the **trainer**
   did nothing either.
4. The instrumented worker finally said it: `env.step` took **13 ms inside a
   worker** and 0.7 ms in the parent, for identical code. A worker sleeps in
   `recv()` between steps, and every wake-up is rounded up to the scheduler tick.
   Since Windows 10 2004 that resolution is **per process**, so the call has to
   be made in the worker, which is the one place the first attempt had not tried.

One `timeBeginPeriod(1)` inside `_worker` took the rollout from 292 to 1,530
steps/s — 5.2×, for a line of code, and the reason the 2M-step run finishes in an
hour instead of six. It is documented in `doomagent/vecenv.py:fine_timer`.

## Files

```
train.py                 train on one scenario
evaluate.py              random / spray / trained, on the same held-out seeds
doomagent/env.py         ViZDoom wrapper: frame skip, greyscale, stacking
doomagent/vecenv.py      worker processes, and the timer-resolution fix
doomagent/ppo.py         PPO: GAE, clipping, annealed lr
doomagent/model.py       conv trunk + policy and value heads
doomagent/baselines.py   the two floors worth beating
```

## Running it

```bash
pip install vizdoom torch --index-url https://download.pytorch.org/whl/cpu
python train.py --scenario defend_the_center --steps 2000000 --envs 12
python evaluate.py --scenario defend_the_center --episodes 30
```

`--scenario` also takes `basic` and `health_gathering`.
