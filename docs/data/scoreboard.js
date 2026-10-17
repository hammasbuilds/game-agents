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
  }
 ]
};
