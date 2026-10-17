# 04 — A robot learns to walk

MuJoCo, PPO with a Gaussian policy, on a laptop CPU. The demonstration is the
same one the rest of this repository uses: the untrained network and the trained
one, same episode, side by side.

```bash
python -m walker.train --env Walker2d-v5 --steps 2000000
python film.py --env Walker2d-v5 --seed 3
```

## Why this one is different from everything else here

Every other agent in this repository chooses between a handful of buttons. A
MuJoCo robot has no buttons: an action is a torque for each of its six joints,
six real numbers at once, and a softmax has nothing to say about that. So the
actor outputs a mean per joint and carries one learned standard deviation per
joint, and the log probability of an action is the sum over joints.

Two other things continuous control needs that pixel control does not:

* **Observations are normalised from a running estimate.** Joint angles sit in
  [-1, 1] and velocities reach double digits. A network fed the raw vector
  spends its first thousand updates learning the scale of its own inputs.
* **That estimate travels in the checkpoint.** A policy restored without its
  normaliser is reading its inputs in different units from the ones it trained
  on, and the result looks exactly like a policy that has forgotten how to walk.

## What the agent sees, and what the camera sees

Nothing. They share nothing: the policy reads a 17-number state vector, the
camera renders at whatever size it is asked for. That separation is the thing
the DOOM project had to be rebuilt to get — there, the recording was being taken
from the agent's own 160×120 training buffer, which is why those films looked
like 1996 while the game underneath did not.

## Results

1,998,848 steps in 43 minutes on a laptop CPU, 11,085
parameters, 4,239 episodes of experience.

| checkpoint | steps | return | ± se | episode length |
|---|---:|---:|---:|---:|
| ckpt_000 | 0 | 65 | 0.6 | 89 |
| ckpt_049 | 100,352 | 430 | 0.8 | 185 |
| ckpt_146 | 299,008 | 883 | 28.1 | 268 |
| ckpt_342 | 700,416 | 4,494 | 11.5 | 1000 |
| ckpt_634 | 1,298,432 | 4,242 | 243.8 | 949 |
| ckpt_976 | 1,998,848 | 3,637 | 392.8 | 784 |

*Scored on 12 selection episodes, the same ones for every row.*

The best checkpoint is **ckpt_342** at
700,416 steps. Re-scored on 12 held-out episodes it
returns **4,498 ± 14.2**, against
**65.1 ± 0.5** for the same network before any
training: learned, +4,433 against a bar of 28.4.

**The run peaked in the middle and got worse.** It reached its best at
700,416 steps and lost 858 return by the end of
training. That is why the scoring here picks a checkpoint instead of taking the
last one, and why choosing it uses a different set of episodes from the ones the
chosen checkpoint is reported on — picking the highest scorer and then quoting
that same score reports the winner's luck as its skill.

The film shows the chosen checkpoint, not the final file on disk.
