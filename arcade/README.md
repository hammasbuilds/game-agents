# The arcade — one network, three games, and the gap between step 1 and the last step

Three visual games, one training stack, and a deliberate output: a video in which
the **untrained network and the trained one play the same level at the same
time**. The point of this half of the repository is not a leaderboard number. It
is being able to see what learning did.

| game | what it is | why it is here |
|---|---|---|
| **Car racing** | Gymnasium `CarRacing-v3`, discrete actions | the improvement is visible without reading a score: an untrained car spins on the grass, a trained one follows the road |
| **Boxing** | `ALE/Boxing-v5` | hand to hand; the score is punches landed minus punches taken, so it runs from −100 to +100 |
| **Platformer** | `ALE/Kangaroo-v5` | climb, punch, reach the top — the legal stand-in for Mario, since `ale-py` ships its ROMs under licence and NES ROMs are not mine to distribute |

Nothing here needs a ROM you have to find yourself, and nothing is specialised to
one game: every one is reduced to a stack of four 84×84 greyscale frames and
learned by the same network with the same PPO.

## The thing this is built around

**Checkpoints are written from step 0** — before a single gradient step — and
then at 5%, 15%, 35%, 65% and 100% of training. That is not bookkeeping. A
before-and-after comparison only exists if somebody saved the "before", and the
untrained network is the most useful baseline there is: it is the same
architecture, the same observation, the same action set, with nothing learned.

`arcade/progress.py` then does two things with those files:

1. **Scores every checkpoint on the same evaluation levels.** Same seeds for all
   of them, so the climb is like for like rather than a tour of different levels.
   A random-key policy is scored on those levels too, as the floor.
2. **Films them playing the same seed**, and lays the clips out side by side into
   one autoplaying video, each panel labelled with how long that network had
   trained and what it scored.

```bash
python -m arcade.train --all --envs 12      # trains every game, saving checkpoints
python -m arcade.progress --game boxing     # ladder + side-by-side film
python ui/export_arcade.py                  # feed it to the dashboard
```

Results land in `docs/media/<game>/` and appear on the dashboard as a card per
game; the card is a button to that game's own page.

## Two details that are easy to get wrong

**The untrained agent is filmed sampling, not taking the argmax.** A freshly
initialised policy is nearly uniform, and its argmax is one arbitrary action
repeated forever — a car that drives into a wall and stays there. That looks like
a broken program rather than like an untrained agent, and it would make the
"before" side of every comparison dishonest in the flattering direction.

**CarRacing's first fifty frames are a camera zoom** in which the car is a few
pixels across on an empty field. They are skipped before the episode is handed
over, because training on them teaches the policy to act on a picture it will
never see again. The reward collected during the skip is kept, so the episode
score still means what the game says it means.

## Cost

Everything runs on the CPU — the GPU on this machine belongs to another job. The
rollout, not the gradient, is the bottleneck in all three games, which is the
same thing the DOOM project found and the Kaggle notebook measured: four times
the network width costs 2% of the throughput.
