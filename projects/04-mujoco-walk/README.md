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

Filled in from the run artefacts once training finishes; nothing is typed in
here by hand.
