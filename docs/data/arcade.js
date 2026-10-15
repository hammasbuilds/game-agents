window.ARCADE = {
 "games": {
  "racing": {
   "key": "racing",
   "title": "Car racing",
   "blurb": "Top-down racing. The agent sees the track and steers; an untrained one spins on the grass, a trained one follows the road.",
   "env_id": "CarRacing-v3",
   "trained": false,
   "summary": null,
   "curve": [],
   "ladder": null,
   "evaluation_seeds": null,
   "clips": [],
   "gifs": [],
   "progress": null
  },
  "boxing": {
   "key": "boxing",
   "title": "Boxing",
   "blurb": "Hand to hand. Score is punches landed minus punches taken, so it runs from -100 to +100 and reads at a glance.",
   "env_id": "ALE/Boxing-v5",
   "trained": false,
   "summary": null,
   "curve": [
    {
     "steps": 21504,
     "return": -0.25,
     "entropy": 2.8788,
     "length": 1782.25,
     "sps": 489.3
    },
    {
     "steps": 23040,
     "return": -0.25,
     "entropy": 2.8729,
     "length": 1782.25,
     "sps": 496.9
    },
    {
     "steps": 24576,
     "return": -0.25,
     "entropy": 2.8664,
     "length": 1782.25,
     "sps": 506.5
    },
    {
     "steps": 26112,
     "return": -0.25,
     "entropy": 2.8647,
     "length": 1782.25,
     "sps": 509.6
    },
    {
     "steps": 27648,
     "return": -0.25,
     "entropy": 2.8466,
     "length": 1782.25,
     "sps": 513.6
    },
    {
     "steps": 29184,
     "return": -0.25,
     "entropy": 2.8432,
     "length": 1782.25,
     "sps": 515.5
    },
    {
     "steps": 30720,
     "return": -0.25,
     "entropy": 2.8233,
     "length": 1782.25,
     "sps": 518.2
    },
    {
     "steps": 32256,
     "return": -0.25,
     "entropy": 2.8118,
     "length": 1782.25,
     "sps": 522.8
    },
    {
     "steps": 33792,
     "return": -0.25,
     "entropy": 2.8294,
     "length": 1782.25,
     "sps": 528.2
    },
    {
     "steps": 35328,
     "return": -0.25,
     "entropy": 2.8318,
     "length": 1782.25,
     "sps": 529.1
    },
    {
     "steps": 36864,
     "return": -0.25,
     "entropy": 2.8327,
     "length": 1782.25,
     "sps": 530.7
    },
    {
     "steps": 38400,
     "return": -0.25,
     "entropy": 2.8313,
     "length": 1782.25,
     "sps": 532.1
    },
    {
     "steps": 39936,
     "return": -0.25,
     "entropy": 2.8528,
     "length": 1782.25,
     "sps": 535.1
    },
    {
     "steps": 41472,
     "return": -0.25,
     "entropy": 2.8413,
     "length": 1782.25,
     "sps": 539.8
    },
    {
     "steps": 43008,
     "return": -0.25,
     "entropy": 2.8661,
     "length": 1782.125,
     "sps": 539.8
    },
    {
     "steps": 44544,
     "return": -0.25,
     "entropy": 2.8646,
     "length": 1782.125,
     "sps": 543.6
    },
    {
     "steps": 46080,
     "return": -0.25,
     "entropy": 2.8443,
     "length": 1782.125,
     "sps": 544.6
    }
   ],
   "ladder": [
    {
     "tag": "random",
     "steps": null,
     "episodes": 1,
     "return_mean": 0.0,
     "return_std": 0.0,
     "return_min": 0.0,
     "return_max": 0.0,
     "length_mean": 150.0,
     "returns": [
      0.0
     ]
    },
    {
     "tag": "000",
     "steps": 0,
     "episodes": 1,
     "return_mean": 0.0,
     "return_std": 0.0,
     "return_min": 0.0,
     "return_max": 0.0,
     "length_mean": 150.0,
     "returns": [
      0.0
     ]
    },
    {
     "tag": "100",
     "steps": 6144,
     "episodes": 1,
     "return_mean": 3.0,
     "return_std": 0.0,
     "return_min": 3.0,
     "return_max": 3.0,
     "length_mean": 150.0,
     "returns": [
      3.0
     ]
    }
   ],
   "evaluation_seeds": [
    50000
   ],
   "clips": [
    "progress.mp4",
    "step_000.mp4",
    "step_100.mp4"
   ],
   "gifs": [
    "progress.gif"
   ],
   "progress": "progress.mp4"
  },
  "platformer": {
   "key": "platformer",
   "title": "Platformer",
   "blurb": "Climb the ladders, punch the monkeys, reach the top. The legal stand-in for Mario: a platformer with ROMs that ship licensed.",
   "env_id": "ALE/Kangaroo-v5",
   "trained": false,
   "summary": null,
   "curve": [],
   "ladder": null,
   "evaluation_seeds": null,
   "clips": [],
   "gifs": [],
   "progress": null
  }
 }
};
