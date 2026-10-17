window.SCOREBOARD = {
 "rows": [
  {
   "project": "01 \u00b7 DOOM",
   "game": "deadly corridor",
   "agent": "PPO (greedy)",
   "baseline": "random",
   "agent_score": 234.34,
   "baseline_score": -22.92,
   "gain": 257.26,
   "bar": 83.68,
   "verdict": "learned",
   "episodes": 20,
   "unit": "reward",
   "protocol": "held-out episodes, same seeds for every agent; final checkpoint"
  },
  {
   "project": "01 \u00b7 DOOM",
   "game": "defend the center",
   "agent": "PPO (greedy)",
   "baseline": "spray",
   "agent_score": 9.8,
   "baseline_score": 1.23,
   "gain": 8.57,
   "bar": 0.61,
   "verdict": "learned",
   "episodes": 30,
   "unit": "kills",
   "protocol": "held-out episodes, same seeds for every agent; final checkpoint"
  },
  {
   "project": "01 \u00b7 DOOM",
   "game": "health gathering",
   "agent": "PPO (greedy)",
   "baseline": "random",
   "agent_score": 1930.4,
   "baseline_score": 380.0,
   "gain": 1550.4,
   "bar": 169.2,
   "verdict": "learned",
   "episodes": 20,
   "unit": "ticks survived",
   "protocol": "held-out episodes, same seeds for every agent; final checkpoint"
  },
  {
   "project": "02 \u00b7 Crafter",
   "game": "Crafter",
   "agent": "planner (no training)",
   "baseline": "random",
   "agent_score": 12.73,
   "baseline_score": 1.13,
   "gain": 11.6,
   "bar": null,
   "verdict": "no error bar",
   "episodes": 10,
   "unit": "Crafter score (%)",
   "protocol": "geometric mean of achievement rates over fixed episodes",
   "note": "no error bar: the Crafter score is a geometric mean over achievement rates, not a mean over episodes",
   "reward": [
    0.9,
    7.9
   ],
   "achievements": [
    5,
    15
   ]
  },
  {
   "project": "03 \u00b7 Brogue",
   "game": "Brogue CE",
   "agent": "explorer (screen-driven)",
   "baseline": "random keystrokes",
   "agent_score": 1.0,
   "baseline_score": 1.33,
   "gain": -0.33,
   "bar": 1.33,
   "verdict": "inside noise",
   "episodes": 6,
   "unit": "descents in 300 keystrokes",
   "protocol": "fixed seeds, same dungeon for both agents",
   "note": "300 keystrokes is a short run: this is a floor on what the agent can do, not a ceiling"
  },
  {
   "project": "04 \u00b7 Walking",
   "game": "Walker2d-v5",
   "agent": "PPO (best checkpoint)",
   "baseline": "untrained network",
   "agent_score": 4497.88,
   "baseline_score": 65.09,
   "gain": 4432.79,
   "bar": 28.42,
   "verdict": "learned",
   "episodes": 12,
   "unit": "return",
   "protocol": "protocol.py \u2014 ladder on 12 selection episodes, winner re-scored on 12 held out",
   "peaked_early": true,
   "decline_after_peak": 857.7
  },
  {
   "project": "arcade",
   "game": "racing",
   "agent": "PPO (best checkpoint)",
   "baseline": "random",
   "agent_score": 632.5,
   "baseline_score": -41.66,
   "gain": 674.16,
   "bar": 185.87,
   "verdict": "learned",
   "episodes": 6,
   "unit": "episode return",
   "protocol": "protocol.py \u2014 ladder on 6 selection episodes, winner re-scored on 6 held out",
   "peaked_early": false,
   "decline_after_peak": null
  }
 ],
 "rounds": [
  {
   "at": "2026-10-17 05:50:23Z",
   "commit": "25d26c5",
   "project": "04 \u00b7 Walking",
   "game": "Walker2d-v5",
   "round": 1,
   "config": {
    "steps": 2000000,
    "envs": 8,
    "rollout": 256,
    "lr": 0.0003,
    "entropy": 0.0
   },
   "best_checkpoint": "ckpt_342.pt",
   "score": 4497.88,
   "se": 14.2,
   "baseline": 65.09,
   "verdict": "learned",
   "note": "peaked at 700k steps, lost 858 by 2M"
  },
  {
   "at": "2026-10-17 05:50:59Z",
   "commit": "25d26c5",
   "project": "01 \u00b7 DOOM",
   "game": "health_gathering",
   "round": 1,
   "config": {
    "steps": 92160,
    "envs": 6,
    "lr": 0.00025,
    "entropy": 0.01,
    "stopped": true
   },
   "score": 310.0,
   "se": null,
   "baseline": 367.2,
   "baseline_agent": "random",
   "verdict": "worse than baseline",
   "note": "stopped at 92k steps: policy entropy had fallen to 0.0017 of a possible 1.10 and the agent scored below a random one. Training log numbers, not a held-out evaluation"
  },
  {
   "at": "2026-10-17 05:50:59Z",
   "commit": "25d26c5",
   "project": "01 \u00b7 DOOM",
   "game": "health_gathering",
   "round": 2,
   "config": {
    "envs": 6,
    "lr": 0.00015,
    "entropy": 0.03,
    "steps": 1199616
   },
   "score": 1930.4,
   "se": 82.11,
   "baseline": 380.0,
   "baseline_agent": "random",
   "verdict": "learned",
   "note": "entropy bonus tripled and learning rate halved after round 1 collapsed"
  },
  {
   "at": "2026-10-17 05:50:59Z",
   "commit": "25d26c5",
   "project": "01 \u00b7 DOOM",
   "game": "defend_the_center",
   "round": 1,
   "config": {
    "envs": 8,
    "lr": 0.00025,
    "entropy": 0.01,
    "steps": 1999872
   },
   "score": 9.8,
   "se": 0.27,
   "baseline": 1.23,
   "baseline_agent": "spray",
   "verdict": "learned",
   "note": null
  },
  {
   "at": "2026-10-17 05:50:59Z",
   "commit": "25d26c5",
   "project": "01 \u00b7 DOOM",
   "game": "deadly_corridor",
   "round": 1,
   "config": {
    "envs": 6,
    "lr": 0.00025,
    "entropy": 0.01,
    "steps": 1199616
   },
   "score": 234.34,
   "se": 37.86,
   "baseline": -22.92,
   "baseline_agent": "random",
   "verdict": "learned",
   "note": "four buttons of the scenario's seven; episodes end in about twenty agent steps"
  },
  {
   "at": "2026-10-17 05:50:59Z",
   "commit": "25d26c5",
   "project": "arcade",
   "game": "racing",
   "round": 1,
   "config": {
    "steps": 414720,
    "envs": 12,
    "lr": 0.00025,
    "entropy": 0.01,
    "stopped": true
   },
   "score": 330.24,
   "se": null,
   "baseline": -48.59,
   "baseline_agent": "untrained",
   "verdict": "learned",
   "note": "peaked at 60k steps (330) and declined to 263 by 419k; run stopped early. Ladder numbers from docs/media/racing/ladder.json"
  },
  {
   "at": "2026-10-17 05:53:17Z",
   "commit": "25d26c5",
   "project": "arcade",
   "game": "racing",
   "round": 1,
   "config": {
    "rescored": true,
    "episodes": "6 selection + 6 held out",
    "note": "same run as the round above"
   },
   "score": 632.5,
   "se": 92.7,
   "baseline": -41.66,
   "baseline_agent": "untrained network",
   "verdict": "learned",
   "note": "correction: the earlier line for this run quoted a film ladder scored on two tracks, which appeared to show a decline from 330 to 263. Under the protocol the same checkpoints rise monotonically to 632.5 \u00b1 92.7. The run itself did not change; the measurement did."
  }
 ]
};
