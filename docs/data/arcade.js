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
   "trained": true,
   "summary": {
    "game": "boxing",
    "env_id": "ALE/Boxing-v5",
    "updates": 1302,
    "steps": 1999872,
    "wall_seconds": 3383.7,
    "final_return_mean": 2.55,
    "params": 428131,
    "width": 1,
    "device": "cpu",
    "envs": 12,
    "checkpoints": [
     {
      "tag": "000",
      "update": 0,
      "steps": 0,
      "path": "ckpt_000.pt",
      "return_mean": null
     },
     {
      "tag": "005",
      "update": 65,
      "steps": 99840,
      "path": "ckpt_005.pt",
      "return_mean": 1.4375
     },
     {
      "tag": "015",
      "update": 195,
      "steps": 299520,
      "path": "ckpt_015.pt",
      "return_mean": 1.29
     },
     {
      "tag": "035",
      "update": 456,
      "steps": 700416,
      "path": "ckpt_035.pt",
      "return_mean": 1.51
     },
     {
      "tag": "065",
      "update": 846,
      "steps": 1299456,
      "path": "ckpt_065.pt",
      "return_mean": 0.83
     },
     {
      "tag": "100",
      "update": 1302,
      "steps": 1999872,
      "path": "ckpt_100.pt",
      "return_mean": 2.55
     }
    ]
   },
   "curve": [
    {
     "steps": 26112,
     "return": -0.25,
     "entropy": 2.8647,
     "length": 1782.25,
     "sps": 509.6
    },
    {
     "steps": 38400,
     "return": -0.25,
     "entropy": 2.8313,
     "length": 1782.25,
     "sps": 532.1
    },
    {
     "steps": 50688,
     "return": -0.25,
     "entropy": 2.8466,
     "length": 1782.125,
     "sps": 545.5
    },
    {
     "steps": 62976,
     "return": -0.25,
     "entropy": 2.8098,
     "length": 1782.125,
     "sps": 554.7
    },
    {
     "steps": 75264,
     "return": 0.8055555555555556,
     "entropy": 2.8351,
     "length": 1782.2222222222222,
     "sps": 566.0
    },
    {
     "steps": 87552,
     "return": 1.4375,
     "entropy": 2.8286,
     "length": 1782.0208333333333,
     "sps": 571.9
    },
    {
     "steps": 99840,
     "return": 1.4375,
     "entropy": 2.7981,
     "length": 1782.0208333333333,
     "sps": 575.0
    },
    {
     "steps": 112128,
     "return": 1.2,
     "entropy": 2.7902,
     "length": 1782.0333333333333,
     "sps": 578.3
    },
    {
     "steps": 124416,
     "return": 1.2,
     "entropy": 2.7571,
     "length": 1782.0333333333333,
     "sps": 581.1
    },
    {
     "steps": 136704,
     "return": 1.3055555555555556,
     "entropy": 2.7603,
     "length": 1782.1805555555557,
     "sps": 582.9
    },
    {
     "steps": 148992,
     "return": 1.3055555555555556,
     "entropy": 2.6773,
     "length": 1782.1805555555557,
     "sps": 581.5
    },
    {
     "steps": 161280,
     "return": 1.3333333333333333,
     "entropy": 2.7265,
     "length": 1782.202380952381,
     "sps": 581.0
    },
    {
     "steps": 173568,
     "return": 1.21875,
     "entropy": 2.8072,
     "length": 1782.2083333333333,
     "sps": 580.8
    },
    {
     "steps": 185856,
     "return": 1.21875,
     "entropy": 2.826,
     "length": 1782.2083333333333,
     "sps": 582.3
    },
    {
     "steps": 198144,
     "return": 1.47,
     "entropy": 2.768,
     "length": 1782.32,
     "sps": 581.2
    },
    {
     "steps": 210432,
     "return": 1.47,
     "entropy": 2.7453,
     "length": 1782.32,
     "sps": 584.3
    },
    {
     "steps": 222720,
     "return": 1.51,
     "entropy": 2.6891,
     "length": 1782.22,
     "sps": 586.5
    },
    {
     "steps": 235008,
     "return": 1.51,
     "entropy": 2.7072,
     "length": 1782.22,
     "sps": 588.4
    },
    {
     "steps": 247296,
     "return": 1.27,
     "entropy": 2.7796,
     "length": 1782.1,
     "sps": 590.3
    },
    {
     "steps": 259584,
     "return": 0.99,
     "entropy": 2.7726,
     "length": 1782.03,
     "sps": 590.4
    },
    {
     "steps": 271872,
     "return": 0.99,
     "entropy": 2.7801,
     "length": 1782.03,
     "sps": 589.5
    },
    {
     "steps": 284160,
     "return": 1.32,
     "entropy": 2.778,
     "length": 1781.92,
     "sps": 589.8
    },
    {
     "steps": 296448,
     "return": 1.32,
     "entropy": 2.7378,
     "length": 1781.92,
     "sps": 590.4
    },
    {
     "steps": 308736,
     "return": 1.29,
     "entropy": 2.6981,
     "length": 1781.76,
     "sps": 590.7
    },
    {
     "steps": 321024,
     "return": 1.16,
     "entropy": 2.6857,
     "length": 1781.56,
     "sps": 592.1
    },
    {
     "steps": 333312,
     "return": 1.16,
     "entropy": 2.6843,
     "length": 1781.56,
     "sps": 592.9
    },
    {
     "steps": 345600,
     "return": 1.11,
     "entropy": 2.5832,
     "length": 1781.41,
     "sps": 592.9
    },
    {
     "steps": 357888,
     "return": 1.11,
     "entropy": 2.6338,
     "length": 1781.41,
     "sps": 590.2
    },
    {
     "steps": 370176,
     "return": 1.41,
     "entropy": 2.6132,
     "length": 1781.46,
     "sps": 589.6
    },
    {
     "steps": 382464,
     "return": 1.41,
     "entropy": 2.5999,
     "length": 1781.46,
     "sps": 589.8
    },
    {
     "steps": 394752,
     "return": 1.28,
     "entropy": 2.5879,
     "length": 1781.41,
     "sps": 589.9
    },
    {
     "steps": 407040,
     "return": 1.33,
     "entropy": 2.561,
     "length": 1781.37,
     "sps": 591.0
    },
    {
     "steps": 419328,
     "return": 1.33,
     "entropy": 2.554,
     "length": 1781.37,
     "sps": 591.6
    },
    {
     "steps": 431616,
     "return": 1.81,
     "entropy": 2.6238,
     "length": 1781.32,
     "sps": 592.2
    },
    {
     "steps": 443904,
     "return": 1.81,
     "entropy": 2.5874,
     "length": 1781.32,
     "sps": 592.6
    },
    {
     "steps": 456192,
     "return": 1.96,
     "entropy": 2.6482,
     "length": 1781.37,
     "sps": 593.2
    },
    {
     "steps": 468480,
     "return": 1.96,
     "entropy": 2.715,
     "length": 1781.37,
     "sps": 593.8
    },
    {
     "steps": 480768,
     "return": 1.85,
     "entropy": 2.6603,
     "length": 1781.5,
     "sps": 595.2
    },
    {
     "steps": 493056,
     "return": 1.79,
     "entropy": 2.498,
     "length": 1781.56,
     "sps": 596.3
    },
    {
     "steps": 505344,
     "return": 1.79,
     "entropy": 2.4695,
     "length": 1781.56,
     "sps": 596.7
    },
    {
     "steps": 517632,
     "return": 1.95,
     "entropy": 2.6073,
     "length": 1781.56,
     "sps": 597.3
    },
    {
     "steps": 529920,
     "return": 1.95,
     "entropy": 2.5781,
     "length": 1781.56,
     "sps": 597.8
    },
    {
     "steps": 542208,
     "return": 1.27,
     "entropy": 2.6265,
     "length": 1781.58,
     "sps": 598.2
    },
    {
     "steps": 554496,
     "return": 1.27,
     "entropy": 2.716,
     "length": 1781.58,
     "sps": 598.6
    },
    {
     "steps": 566784,
     "return": 1.12,
     "entropy": 2.6646,
     "length": 1781.6,
     "sps": 599.5
    },
    {
     "steps": 579072,
     "return": 1.37,
     "entropy": 2.7402,
     "length": 1781.77,
     "sps": 600.6
    },
    {
     "steps": 591360,
     "return": 1.37,
     "entropy": 2.7016,
     "length": 1781.77,
     "sps": 601.6
    },
    {
     "steps": 603648,
     "return": 1.33,
     "entropy": 2.6617,
     "length": 1781.73,
     "sps": 602.2
    },
    {
     "steps": 615936,
     "return": 1.33,
     "entropy": 2.7652,
     "length": 1781.73,
     "sps": 603.1
    },
    {
     "steps": 628224,
     "return": 1.23,
     "entropy": 2.826,
     "length": 1781.85,
     "sps": 604.1
    },
    {
     "steps": 640512,
     "return": 1.23,
     "entropy": 2.7691,
     "length": 1781.85,
     "sps": 605.0
    },
    {
     "steps": 652800,
     "return": 1.22,
     "entropy": 2.8062,
     "length": 1781.86,
     "sps": 605.8
    },
    {
     "steps": 665088,
     "return": 1.17,
     "entropy": 2.7298,
     "length": 1781.7,
     "sps": 606.0
    },
    {
     "steps": 677376,
     "return": 1.17,
     "entropy": 2.7371,
     "length": 1781.7,
     "sps": 606.2
    },
    {
     "steps": 689664,
     "return": 1.51,
     "entropy": 2.7663,
     "length": 1781.63,
     "sps": 606.7
    },
    {
     "steps": 701952,
     "return": 1.51,
     "entropy": 2.7903,
     "length": 1781.63,
     "sps": 606.9
    },
    {
     "steps": 714240,
     "return": 1.6,
     "entropy": 2.8627,
     "length": 1781.51,
     "sps": 607.1
    },
    {
     "steps": 726528,
     "return": 1.6,
     "entropy": 2.8638,
     "length": 1781.51,
     "sps": 607.8
    },
    {
     "steps": 738816,
     "return": 1.8,
     "entropy": 2.8654,
     "length": 1781.44,
     "sps": 608.1
    },
    {
     "steps": 751104,
     "return": 2.02,
     "entropy": 2.8628,
     "length": 1781.27,
     "sps": 608.8
    },
    {
     "steps": 763392,
     "return": 2.02,
     "entropy": 2.8385,
     "length": 1781.27,
     "sps": 609.4
    },
    {
     "steps": 775680,
     "return": 2.23,
     "entropy": 2.8178,
     "length": 1781.27,
     "sps": 609.6
    },
    {
     "steps": 787968,
     "return": 2.23,
     "entropy": 2.7762,
     "length": 1781.27,
     "sps": 610.1
    },
    {
     "steps": 800256,
     "return": 2.01,
     "entropy": 2.7712,
     "length": 1781.18,
     "sps": 610.6
    },
    {
     "steps": 812544,
     "return": 1.7,
     "entropy": 2.7729,
     "length": 1781.19,
     "sps": 610.6
    },
    {
     "steps": 824832,
     "return": 1.6,
     "entropy": 2.7099,
     "length": 1781.15,
     "sps": 611.1
    },
    {
     "steps": 837120,
     "return": 1.57,
     "entropy": 2.7269,
     "length": 1781.19,
     "sps": 611.2
    },
    {
     "steps": 849408,
     "return": 1.57,
     "entropy": 2.8079,
     "length": 1781.19,
     "sps": 611.3
    },
    {
     "steps": 861696,
     "return": 1.32,
     "entropy": 2.833,
     "length": 1781.27,
     "sps": 611.1
    },
    {
     "steps": 873984,
     "return": 1.32,
     "entropy": 2.8299,
     "length": 1781.27,
     "sps": 611.4
    },
    {
     "steps": 886272,
     "return": 1.33,
     "entropy": 2.8423,
     "length": 1781.39,
     "sps": 611.8
    },
    {
     "steps": 898560,
     "return": 1.53,
     "entropy": 2.8667,
     "length": 1781.31,
     "sps": 611.7
    },
    {
     "steps": 910848,
     "return": 1.53,
     "entropy": 2.8291,
     "length": 1781.31,
     "sps": 611.4
    },
    {
     "steps": 923136,
     "return": 1.76,
     "entropy": 2.7864,
     "length": 1781.46,
     "sps": 611.3
    },
    {
     "steps": 935424,
     "return": 1.76,
     "entropy": 2.825,
     "length": 1781.46,
     "sps": 611.2
    },
    {
     "steps": 947712,
     "return": 1.61,
     "entropy": 2.8436,
     "length": 1781.66,
     "sps": 610.9
    },
    {
     "steps": 960000,
     "return": 1.61,
     "entropy": 2.818,
     "length": 1781.66,
     "sps": 610.6
    },
    {
     "steps": 972288,
     "return": 1.17,
     "entropy": 2.8427,
     "length": 1781.9,
     "sps": 610.2
    },
    {
     "steps": 984576,
     "return": 1.57,
     "entropy": 2.8494,
     "length": 1781.86,
     "sps": 609.9
    },
    {
     "steps": 996864,
     "return": 1.57,
     "entropy": 2.8239,
     "length": 1781.86,
     "sps": 609.7
    },
    {
     "steps": 1009152,
     "return": 1.98,
     "entropy": 2.7967,
     "length": 1781.91,
     "sps": 609.5
    },
    {
     "steps": 1021440,
     "return": 1.98,
     "entropy": 2.7704,
     "length": 1781.91,
     "sps": 609.3
    },
    {
     "steps": 1033728,
     "return": 1.79,
     "entropy": 2.7534,
     "length": 1781.79,
     "sps": 609.1
    },
    {
     "steps": 1046016,
     "return": 1.79,
     "entropy": 2.7193,
     "length": 1781.79,
     "sps": 608.7
    },
    {
     "steps": 1058304,
     "return": 2.05,
     "entropy": 2.7579,
     "length": 1781.87,
     "sps": 608.4
    },
    {
     "steps": 1070592,
     "return": 1.77,
     "entropy": 2.6043,
     "length": 1781.91,
     "sps": 608.2
    },
    {
     "steps": 1082880,
     "return": 1.77,
     "entropy": 2.6306,
     "length": 1781.91,
     "sps": 608.0
    },
    {
     "steps": 1095168,
     "return": 1.03,
     "entropy": 2.6658,
     "length": 1781.87,
     "sps": 607.6
    },
    {
     "steps": 1107456,
     "return": 1.03,
     "entropy": 2.6553,
     "length": 1781.87,
     "sps": 607.1
    },
    {
     "steps": 1119744,
     "return": 1.2,
     "entropy": 2.6351,
     "length": 1781.8,
     "sps": 605.8
    },
    {
     "steps": 1132032,
     "return": 1.2,
     "entropy": 2.6129,
     "length": 1781.8,
     "sps": 605.4
    },
    {
     "steps": 1144320,
     "return": 1.49,
     "entropy": 2.6502,
     "length": 1781.55,
     "sps": 605.2
    },
    {
     "steps": 1156608,
     "return": 1.67,
     "entropy": 2.5532,
     "length": 1781.67,
     "sps": 605.0
    },
    {
     "steps": 1168896,
     "return": 1.67,
     "entropy": 2.521,
     "length": 1781.67,
     "sps": 604.8
    },
    {
     "steps": 1181184,
     "return": 1.67,
     "entropy": 2.5255,
     "length": 1781.82,
     "sps": 604.6
    },
    {
     "steps": 1193472,
     "return": 1.67,
     "entropy": 2.5616,
     "length": 1781.82,
     "sps": 604.5
    },
    {
     "steps": 1205760,
     "return": 1.58,
     "entropy": 2.5401,
     "length": 1781.91,
     "sps": 604.5
    },
    {
     "steps": 1218048,
     "return": 1.58,
     "entropy": 2.7224,
     "length": 1781.91,
     "sps": 604.3
    },
    {
     "steps": 1230336,
     "return": 1.14,
     "entropy": 2.6036,
     "length": 1781.76,
     "sps": 604.1
    },
    {
     "steps": 1242624,
     "return": 1.01,
     "entropy": 2.342,
     "length": 1781.78,
     "sps": 603.9
    },
    {
     "steps": 1254912,
     "return": 1.01,
     "entropy": 2.68,
     "length": 1781.78,
     "sps": 603.8
    },
    {
     "steps": 1267200,
     "return": 1.01,
     "entropy": 2.5781,
     "length": 1781.83,
     "sps": 603.6
    },
    {
     "steps": 1279488,
     "return": 1.01,
     "entropy": 2.6757,
     "length": 1781.83,
     "sps": 603.5
    },
    {
     "steps": 1291776,
     "return": 0.83,
     "entropy": 2.6476,
     "length": 1781.68,
     "sps": 603.3
    },
    {
     "steps": 1304064,
     "return": 0.62,
     "entropy": 2.7447,
     "length": 1781.64,
     "sps": 603.1
    },
    {
     "steps": 1316352,
     "return": 0.59,
     "entropy": 2.7136,
     "length": 1781.68,
     "sps": 603.2
    },
    {
     "steps": 1328640,
     "return": 0.14,
     "entropy": 2.6536,
     "length": 1781.34,
     "sps": 603.0
    },
    {
     "steps": 1340928,
     "return": 0.14,
     "entropy": 2.7675,
     "length": 1781.34,
     "sps": 602.9
    },
    {
     "steps": 1353216,
     "return": 0.29,
     "entropy": 2.8108,
     "length": 1781.35,
     "sps": 602.7
    },
    {
     "steps": 1365504,
     "return": 0.29,
     "entropy": 2.8108,
     "length": 1781.35,
     "sps": 602.7
    },
    {
     "steps": 1377792,
     "return": 0.06,
     "entropy": 2.8025,
     "length": 1781.4,
     "sps": 602.5
    },
    {
     "steps": 1390080,
     "return": 0.22,
     "entropy": 2.8318,
     "length": 1781.34,
     "sps": 602.3
    },
    {
     "steps": 1402368,
     "return": 0.22,
     "entropy": 2.8313,
     "length": 1781.34,
     "sps": 602.2
    },
    {
     "steps": 1414656,
     "return": 0.55,
     "entropy": 2.8092,
     "length": 1781.44,
     "sps": 602.1
    },
    {
     "steps": 1426944,
     "return": 0.55,
     "entropy": 2.7937,
     "length": 1781.44,
     "sps": 602.1
    },
    {
     "steps": 1439232,
     "return": 0.83,
     "entropy": 2.8062,
     "length": 1781.46,
     "sps": 602.0
    },
    {
     "steps": 1451520,
     "return": 0.83,
     "entropy": 2.8061,
     "length": 1781.46,
     "sps": 601.8
    },
    {
     "steps": 1463808,
     "return": 1.11,
     "entropy": 2.8055,
     "length": 1781.6,
     "sps": 601.6
    },
    {
     "steps": 1476096,
     "return": 1.34,
     "entropy": 2.8372,
     "length": 1781.87,
     "sps": 601.5
    },
    {
     "steps": 1488384,
     "return": 1.34,
     "entropy": 2.7637,
     "length": 1781.87,
     "sps": 601.3
    },
    {
     "steps": 1500672,
     "return": 1.43,
     "entropy": 2.7448,
     "length": 1782.0,
     "sps": 601.1
    },
    {
     "steps": 1512960,
     "return": 1.43,
     "entropy": 2.7471,
     "length": 1782.0,
     "sps": 599.4
    },
    {
     "steps": 1525248,
     "return": 1.35,
     "entropy": 2.8612,
     "length": 1782.07,
     "sps": 597.3
    },
    {
     "steps": 1537536,
     "return": 1.35,
     "entropy": 2.8318,
     "length": 1782.07,
     "sps": 595.3
    },
    {
     "steps": 1549824,
     "return": 1.3,
     "entropy": 2.8419,
     "length": 1781.9,
     "sps": 593.4
    },
    {
     "steps": 1562112,
     "return": 1.01,
     "entropy": 2.859,
     "length": 1782.05,
     "sps": 592.9
    },
    {
     "steps": 1574400,
     "return": 1.01,
     "entropy": 2.8625,
     "length": 1782.05,
     "sps": 592.8
    },
    {
     "steps": 1586688,
     "return": 1.24,
     "entropy": 2.8535,
     "length": 1782.09,
     "sps": 592.7
    },
    {
     "steps": 1598976,
     "return": 1.24,
     "entropy": 2.8479,
     "length": 1782.09,
     "sps": 592.7
    },
    {
     "steps": 1611264,
     "return": 1.45,
     "entropy": 2.8333,
     "length": 1782.02,
     "sps": 592.7
    },
    {
     "steps": 1623552,
     "return": 1.45,
     "entropy": 2.8374,
     "length": 1782.02,
     "sps": 592.7
    },
    {
     "steps": 1635840,
     "return": 1.38,
     "entropy": 2.8278,
     "length": 1782.11,
     "sps": 592.6
    },
    {
     "steps": 1648128,
     "return": 1.42,
     "entropy": 2.829,
     "length": 1782.07,
     "sps": 592.6
    },
    {
     "steps": 1660416,
     "return": 1.42,
     "entropy": 2.7727,
     "length": 1782.07,
     "sps": 592.5
    },
    {
     "steps": 1672704,
     "return": 1.39,
     "entropy": 2.8189,
     "length": 1782.08,
     "sps": 592.5
    },
    {
     "steps": 1684992,
     "return": 1.39,
     "entropy": 2.8045,
     "length": 1782.08,
     "sps": 592.5
    },
    {
     "steps": 1697280,
     "return": 1.43,
     "entropy": 2.8385,
     "length": 1781.86,
     "sps": 592.4
    },
    {
     "steps": 1709568,
     "return": 1.43,
     "entropy": 2.751,
     "length": 1781.86,
     "sps": 592.4
    },
    {
     "steps": 1721856,
     "return": 1.59,
     "entropy": 2.7367,
     "length": 1781.93,
     "sps": 592.4
    },
    {
     "steps": 1734144,
     "return": 2.19,
     "entropy": 2.7516,
     "length": 1781.89,
     "sps": 592.4
    },
    {
     "steps": 1746432,
     "return": 2.19,
     "entropy": 2.7164,
     "length": 1781.89,
     "sps": 592.3
    },
    {
     "steps": 1758720,
     "return": 1.92,
     "entropy": 2.7793,
     "length": 1781.93,
     "sps": 592.3
    },
    {
     "steps": 1771008,
     "return": 1.92,
     "entropy": 2.7327,
     "length": 1781.93,
     "sps": 592.2
    },
    {
     "steps": 1783296,
     "return": 1.91,
     "entropy": 2.7898,
     "length": 1781.97,
     "sps": 592.1
    },
    {
     "steps": 1795584,
     "return": 1.83,
     "entropy": 2.7587,
     "length": 1781.97,
     "sps": 592.1
    },
    {
     "steps": 1807872,
     "return": 2.15,
     "entropy": 2.7621,
     "length": 1781.94,
     "sps": 592.1
    },
    {
     "steps": 1820160,
     "return": 2.57,
     "entropy": 2.6937,
     "length": 1781.94,
     "sps": 592.0
    },
    {
     "steps": 1832448,
     "return": 2.57,
     "entropy": 2.7689,
     "length": 1781.94,
     "sps": 592.0
    },
    {
     "steps": 1844736,
     "return": 2.67,
     "entropy": 2.7798,
     "length": 1781.98,
     "sps": 591.9
    },
    {
     "steps": 1857024,
     "return": 2.67,
     "entropy": 2.7687,
     "length": 1781.98,
     "sps": 591.9
    },
    {
     "steps": 1869312,
     "return": 2.71,
     "entropy": 2.7752,
     "length": 1782.03,
     "sps": 591.8
    },
    {
     "steps": 1881600,
     "return": 3.17,
     "entropy": 2.738,
     "length": 1782.0,
     "sps": 591.8
    },
    {
     "steps": 1893888,
     "return": 3.14,
     "entropy": 2.7539,
     "length": 1781.92,
     "sps": 591.7
    },
    {
     "steps": 1906176,
     "return": 2.79,
     "entropy": 2.7462,
     "length": 1781.86,
     "sps": 591.7
    },
    {
     "steps": 1918464,
     "return": 2.79,
     "entropy": 2.7919,
     "length": 1781.86,
     "sps": 591.6
    },
    {
     "steps": 1930752,
     "return": 3.14,
     "entropy": 2.7309,
     "length": 1781.97,
     "sps": 591.6
    },
    {
     "steps": 1943040,
     "return": 3.14,
     "entropy": 2.7933,
     "length": 1781.97,
     "sps": 591.5
    },
    {
     "steps": 1955328,
     "return": 3.06,
     "entropy": 2.7871,
     "length": 1781.84,
     "sps": 591.4
    },
    {
     "steps": 1967616,
     "return": 2.56,
     "entropy": 2.807,
     "length": 1781.75,
     "sps": 591.4
    },
    {
     "steps": 1979904,
     "return": 2.56,
     "entropy": 2.7858,
     "length": 1781.75,
     "sps": 591.3
    },
    {
     "steps": 1992192,
     "return": 2.55,
     "entropy": 2.7708,
     "length": 1781.72,
     "sps": 591.2
    },
    {
     "steps": 1999872,
     "return": 2.55,
     "entropy": 2.7859,
     "length": 1781.72,
     "sps": 591.2
    }
   ],
   "ladder": [
    {
     "tag": "random",
     "steps": null,
     "episodes": 8,
     "return_mean": 0.5,
     "return_std": 5.83,
     "return_min": -10.0,
     "return_max": 7.0,
     "length_mean": 1782.0,
     "returns": [
      -4.0,
      6.0,
      -3.0,
      -10.0,
      5.0,
      1.0,
      2.0,
      7.0
     ]
    },
    {
     "tag": "000",
     "steps": 0,
     "episodes": 8,
     "return_mean": 2.12,
     "return_std": 3.27,
     "return_min": -1.0,
     "return_max": 9.0,
     "length_mean": 1782.0,
     "returns": [
      0.0,
      -1.0,
      4.0,
      3.0,
      9.0,
      0.0,
      0.0,
      2.0
     ]
    },
    {
     "tag": "005",
     "steps": 99840,
     "episodes": 8,
     "return_mean": 3.0,
     "return_std": 4.41,
     "return_min": -2.0,
     "return_max": 12.0,
     "length_mean": 1782.0,
     "returns": [
      3.0,
      -1.0,
      5.0,
      0.0,
      3.0,
      12.0,
      4.0,
      -2.0
     ]
    },
    {
     "tag": "015",
     "steps": 299520,
     "episodes": 8,
     "return_mean": -3.5,
     "return_std": 8.4,
     "return_min": -14.0,
     "return_max": 9.0,
     "length_mean": 1782.0,
     "returns": [
      -14.0,
      -3.0,
      9.0,
      4.0,
      -11.0,
      3.0,
      -12.0,
      -4.0
     ]
    },
    {
     "tag": "035",
     "steps": 700416,
     "episodes": 8,
     "return_mean": 2.12,
     "return_std": 6.31,
     "return_min": -6.0,
     "return_max": 12.0,
     "length_mean": 1782.0,
     "returns": [
      3.0,
      8.0,
      0.0,
      -6.0,
      -6.0,
      12.0,
      1.0,
      5.0
     ]
    },
    {
     "tag": "065",
     "steps": 1299456,
     "episodes": 8,
     "return_mean": -2.12,
     "return_std": 5.0,
     "return_min": -13.0,
     "return_max": 4.0,
     "length_mean": 1782.0,
     "returns": [
      -4.0,
      -2.0,
      1.0,
      4.0,
      -2.0,
      -13.0,
      -1.0,
      0.0
     ]
    },
    {
     "tag": "100",
     "steps": 1999872,
     "episodes": 8,
     "return_mean": 1.62,
     "return_std": 3.5,
     "return_min": -2.0,
     "return_max": 9.0,
     "length_mean": 1782.0,
     "returns": [
      0.0,
      0.0,
      4.0,
      1.0,
      9.0,
      2.0,
      -2.0,
      -1.0
     ]
    }
   ],
   "evaluation_seeds": [
    50000,
    50001,
    50002,
    50003,
    50004,
    50005,
    50006,
    50007
   ],
   "clips": [
    "progress.mp4",
    "step_000.mp4",
    "step_035.mp4",
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
  },
  "pingpong": {
   "key": "pingpong",
   "title": "Table tennis",
   "blurb": "Score runs from -21 to +21, so there is nowhere for a weak agent to hide: it starts losing every rally and ends winning them.",
   "env_id": "ALE/Pong-v5",
   "trained": false,
   "summary": null,
   "curve": [
    {
     "steps": 9216,
     "return": -21.0,
     "entropy": 1.7761,
     "length": 759.0,
     "sps": 398.7
    },
    {
     "steps": 10752,
     "return": -20.875,
     "entropy": 1.7657,
     "length": 837.125,
     "sps": 414.9
    },
    {
     "steps": 12288,
     "return": -20.6,
     "entropy": 1.7646,
     "length": 864.2,
     "sps": 428.6
    },
    {
     "steps": 13824,
     "return": -20.454545454545453,
     "entropy": 1.7651,
     "length": 885.4545454545455,
     "sps": 440.5
    },
    {
     "steps": 15360,
     "return": -20.333333333333332,
     "entropy": 1.7676,
     "length": 908.6666666666666,
     "sps": 450.9
    },
    {
     "steps": 16896,
     "return": -20.333333333333332,
     "entropy": 1.767,
     "length": 908.6666666666666,
     "sps": 452.3
    },
    {
     "steps": 18432,
     "return": -20.333333333333332,
     "entropy": 1.7695,
     "length": 908.6666666666666,
     "sps": 451.1
    },
    {
     "steps": 19968,
     "return": -20.428571428571427,
     "entropy": 1.7724,
     "length": 891.1428571428571,
     "sps": 449.4
    },
    {
     "steps": 21504,
     "return": -20.55,
     "entropy": 1.766,
     "length": 872.75,
     "sps": 445.5
    },
    {
     "steps": 23040,
     "return": -20.40909090909091,
     "entropy": 1.766,
     "length": 885.3636363636364,
     "sps": 443.1
    },
    {
     "steps": 24576,
     "return": -20.416666666666668,
     "entropy": 1.7731,
     "length": 880.5833333333334,
     "sps": 442.8
    },
    {
     "steps": 26112,
     "return": -20.416666666666668,
     "entropy": 1.767,
     "length": 880.5833333333334,
     "sps": 443.5
    },
    {
     "steps": 27648,
     "return": -20.416666666666668,
     "entropy": 1.7554,
     "length": 880.5833333333334,
     "sps": 442.6
    },
    {
     "steps": 29184,
     "return": -20.44,
     "entropy": 1.7653,
     "length": 875.92,
     "sps": 443.9
    },
    {
     "steps": 30720,
     "return": -20.517241379310345,
     "entropy": 1.7709,
     "length": 864.6896551724138,
     "sps": 443.1
    },
    {
     "steps": 32256,
     "return": -20.558823529411764,
     "entropy": 1.7725,
     "length": 862.3235294117648,
     "sps": 442.1
    },
    {
     "steps": 33792,
     "return": -20.542857142857144,
     "entropy": 1.7785,
     "length": 861.7142857142857,
     "sps": 442.0
    },
    {
     "steps": 35328,
     "return": -20.52777777777778,
     "entropy": 1.7807,
     "length": 862.6111111111111,
     "sps": 442.3
    },
    {
     "steps": 36864,
     "return": -20.52777777777778,
     "entropy": 1.7795,
     "length": 862.6111111111111,
     "sps": 442.1
    },
    {
     "steps": 38400,
     "return": -20.54054054054054,
     "entropy": 1.7723,
     "length": 860.5135135135135,
     "sps": 441.8
    },
    {
     "steps": 39936,
     "return": -20.575,
     "entropy": 1.7696,
     "length": 857.3,
     "sps": 441.8
    },
    {
     "steps": 41472,
     "return": -20.5609756097561,
     "entropy": 1.7617,
     "length": 856.780487804878,
     "sps": 442.1
    },
    {
     "steps": 43008,
     "return": -20.545454545454547,
     "entropy": 1.757,
     "length": 859.4090909090909,
     "sps": 442.6
    },
    {
     "steps": 44544,
     "return": -20.51063829787234,
     "entropy": 1.7541,
     "length": 867.6808510638298,
     "sps": 443.1
    },
    {
     "steps": 46080,
     "return": -20.520833333333332,
     "entropy": 1.7275,
     "length": 869.9166666666666,
     "sps": 443.0
    },
    {
     "steps": 47616,
     "return": -20.520833333333332,
     "entropy": 1.7064,
     "length": 869.9166666666666,
     "sps": 443.6
    },
    {
     "steps": 49152,
     "return": -20.53061224489796,
     "entropy": 1.6821,
     "length": 869.4897959183673,
     "sps": 443.1
    },
    {
     "steps": 50688,
     "return": -20.50980392156863,
     "entropy": 1.6784,
     "length": 871.7254901960785,
     "sps": 442.9
    },
    {
     "steps": 52224,
     "return": -20.51923076923077,
     "entropy": 1.6413,
     "length": 873.5769230769231,
     "sps": 442.6
    },
    {
     "steps": 53760,
     "return": -20.464285714285715,
     "entropy": 1.6431,
     "length": 877.4642857142857,
     "sps": 441.9
    },
    {
     "steps": 55296,
     "return": -20.473684210526315,
     "entropy": 1.6244,
     "length": 876.8421052631579,
     "sps": 442.5
    },
    {
     "steps": 56832,
     "return": -20.45,
     "entropy": 1.6586,
     "length": 880.95,
     "sps": 442.0
    },
    {
     "steps": 58368,
     "return": -20.45,
     "entropy": 1.6845,
     "length": 880.95,
     "sps": 442.0
    },
    {
     "steps": 59904,
     "return": -20.442622950819672,
     "entropy": 1.6882,
     "length": 880.1803278688525,
     "sps": 443.2
    },
    {
     "steps": 61440,
     "return": -20.442622950819672,
     "entropy": 1.6865,
     "length": 880.1803278688525,
     "sps": 443.4
    },
    {
     "steps": 62976,
     "return": -20.41269841269841,
     "entropy": 1.6956,
     "length": 883.4920634920635,
     "sps": 442.9
    },
    {
     "steps": 64512,
     "return": -20.40909090909091,
     "entropy": 1.6888,
     "length": 884.9848484848485,
     "sps": 443.3
    },
    {
     "steps": 66048,
     "return": -20.422535211267604,
     "entropy": 1.7147,
     "length": 887.0,
     "sps": 443.7
    },
    {
     "steps": 67584,
     "return": -20.40277777777778,
     "entropy": 1.6973,
     "length": 888.25,
     "sps": 443.2
    },
    {
     "steps": 69120,
     "return": -20.410958904109588,
     "entropy": 1.6709,
     "length": 886.7808219178082,
     "sps": 443.5
    },
    {
     "steps": 70656,
     "return": -20.410958904109588,
     "entropy": 1.6949,
     "length": 886.7808219178082,
     "sps": 443.5
    },
    {
     "steps": 72192,
     "return": -20.41891891891892,
     "entropy": 1.702,
     "length": 885.9054054054054,
     "sps": 443.5
    },
    {
     "steps": 73728,
     "return": -20.428571428571427,
     "entropy": 1.694,
     "length": 883.922077922078,
     "sps": 443.7
    },
    {
     "steps": 75264,
     "return": -20.430379746835442,
     "entropy": 1.6782,
     "length": 883.2025316455696,
     "sps": 443.6
    },
    {
     "steps": 76800,
     "return": -20.428571428571427,
     "entropy": 1.6745,
     "length": 880.9642857142857,
     "sps": 443.9
    },
    {
     "steps": 78336,
     "return": -20.428571428571427,
     "entropy": 1.6356,
     "length": 880.9642857142857,
     "sps": 442.3
    },
    {
     "steps": 79872,
     "return": -20.435294117647057,
     "entropy": 1.6748,
     "length": 880.6470588235294,
     "sps": 441.8
    },
    {
     "steps": 81408,
     "return": -20.430232558139537,
     "entropy": 1.657,
     "length": 880.1860465116279,
     "sps": 441.9
    },
    {
     "steps": 82944,
     "return": -20.42528735632184,
     "entropy": 1.6796,
     "length": 879.7126436781609,
     "sps": 442.5
    },
    {
     "steps": 84480,
     "return": -20.426966292134832,
     "entropy": 1.705,
     "length": 879.2134831460675,
     "sps": 442.0
    },
    {
     "steps": 86016,
     "return": -20.440860215053764,
     "entropy": 1.6918,
     "length": 878.3870967741935,
     "sps": 441.8
    },
    {
     "steps": 87552,
     "return": -20.431578947368422,
     "entropy": 1.6742,
     "length": 878.421052631579,
     "sps": 442.5
    },
    {
     "steps": 89088,
     "return": -20.422680412371133,
     "entropy": 1.6764,
     "length": 878.8144329896908,
     "sps": 442.3
    },
    {
     "steps": 90624,
     "return": -20.422680412371133,
     "entropy": 1.6873,
     "length": 878.8144329896908,
     "sps": 442.5
    },
    {
     "steps": 92160,
     "return": -20.428571428571427,
     "entropy": 1.6929,
     "length": 878.6938775510204,
     "sps": 442.7
    },
    {
     "steps": 93696,
     "return": -20.434343434343436,
     "entropy": 1.7025,
     "length": 878.1414141414141,
     "sps": 442.9
    },
    {
     "steps": 95232,
     "return": -20.43,
     "entropy": 1.7172,
     "length": 880.18,
     "sps": 442.9
    },
    {
     "steps": 96768,
     "return": -20.41,
     "entropy": 1.7349,
     "length": 879.71,
     "sps": 442.6
    },
    {
     "steps": 98304,
     "return": -20.41,
     "entropy": 1.7321,
     "length": 879.71,
     "sps": 442.8
    },
    {
     "steps": 99840,
     "return": -20.39,
     "entropy": 1.727,
     "length": 882.55,
     "sps": 442.8
    },
    {
     "steps": 101376,
     "return": -20.39,
     "entropy": 1.7333,
     "length": 882.58,
     "sps": 442.3
    },
    {
     "steps": 102912,
     "return": -20.41,
     "entropy": 1.7202,
     "length": 880.81,
     "sps": 442.8
    },
    {
     "steps": 104448,
     "return": -20.43,
     "entropy": 1.7354,
     "length": 877.59,
     "sps": 442.7
    },
    {
     "steps": 105984,
     "return": -20.44,
     "entropy": 1.7485,
     "length": 878.44,
     "sps": 442.9
    },
    {
     "steps": 107520,
     "return": -20.43,
     "entropy": 1.7526,
     "length": 880.71,
     "sps": 443.2
    },
    {
     "steps": 109056,
     "return": -20.43,
     "entropy": 1.7632,
     "length": 880.71,
     "sps": 443.4
    },
    {
     "steps": 110592,
     "return": -20.42,
     "entropy": 1.7698,
     "length": 884.41,
     "sps": 443.5
    },
    {
     "steps": 112128,
     "return": -20.43,
     "entropy": 1.7619,
     "length": 882.61,
     "sps": 443.5
    },
    {
     "steps": 113664,
     "return": -20.43,
     "entropy": 1.7669,
     "length": 887.3,
     "sps": 444.0
    },
    {
     "steps": 115200,
     "return": -20.43,
     "entropy": 1.758,
     "length": 888.55,
     "sps": 443.8
    },
    {
     "steps": 116736,
     "return": -20.44,
     "entropy": 1.7586,
     "length": 890.97,
     "sps": 443.6
    },
    {
     "steps": 118272,
     "return": -20.44,
     "entropy": 1.761,
     "length": 892.8,
     "sps": 444.1
    },
    {
     "steps": 119808,
     "return": -20.44,
     "entropy": 1.7548,
     "length": 893.56,
     "sps": 444.0
    },
    {
     "steps": 121344,
     "return": -20.43,
     "entropy": 1.753,
     "length": 893.44,
     "sps": 444.4
    },
    {
     "steps": 122880,
     "return": -20.43,
     "entropy": 1.7567,
     "length": 893.44,
     "sps": 444.7
    },
    {
     "steps": 124416,
     "return": -20.42,
     "entropy": 1.7629,
     "length": 894.7,
     "sps": 444.7
    },
    {
     "steps": 125952,
     "return": -20.43,
     "entropy": 1.7541,
     "length": 896.99,
     "sps": 444.9
    },
    {
     "steps": 127488,
     "return": -20.43,
     "entropy": 1.7465,
     "length": 900.31,
     "sps": 445.2
    },
    {
     "steps": 129024,
     "return": -20.41,
     "entropy": 1.7378,
     "length": 902.71,
     "sps": 445.2
    },
    {
     "steps": 130560,
     "return": -20.41,
     "entropy": 1.7355,
     "length": 902.71,
     "sps": 445.0
    },
    {
     "steps": 132096,
     "return": -20.41,
     "entropy": 1.7244,
     "length": 901.46,
     "sps": 445.2
    },
    {
     "steps": 133632,
     "return": -20.41,
     "entropy": 1.7363,
     "length": 902.21,
     "sps": 445.7
    },
    {
     "steps": 135168,
     "return": -20.42,
     "entropy": 1.7229,
     "length": 900.56,
     "sps": 445.8
    },
    {
     "steps": 136704,
     "return": -20.43,
     "entropy": 1.7329,
     "length": 899.34,
     "sps": 445.6
    },
    {
     "steps": 138240,
     "return": -20.42,
     "entropy": 1.7323,
     "length": 897.49,
     "sps": 445.4
    },
    {
     "steps": 139776,
     "return": -20.42,
     "entropy": 1.7377,
     "length": 896.44,
     "sps": 445.6
    },
    {
     "steps": 141312,
     "return": -20.42,
     "entropy": 1.7407,
     "length": 899.14,
     "sps": 445.6
    },
    {
     "steps": 142848,
     "return": -20.42,
     "entropy": 1.7445,
     "length": 899.14,
     "sps": 445.6
    },
    {
     "steps": 144384,
     "return": -20.44,
     "entropy": 1.722,
     "length": 898.05,
     "sps": 445.7
    },
    {
     "steps": 145920,
     "return": -20.44,
     "entropy": 1.7255,
     "length": 898.05,
     "sps": 445.9
    },
    {
     "steps": 147456,
     "return": -20.46,
     "entropy": 1.7312,
     "length": 895.87,
     "sps": 446.2
    },
    {
     "steps": 148992,
     "return": -20.46,
     "entropy": 1.7121,
     "length": 895.58,
     "sps": 446.3
    },
    {
     "steps": 150528,
     "return": -20.49,
     "entropy": 1.7089,
     "length": 891.14,
     "sps": 446.3
    },
    {
     "steps": 152064,
     "return": -20.49,
     "entropy": 1.709,
     "length": 891.14,
     "sps": 446.3
    },
    {
     "steps": 153600,
     "return": -20.47,
     "entropy": 1.7021,
     "length": 894.0,
     "sps": 446.1
    },
    {
     "steps": 155136,
     "return": -20.47,
     "entropy": 1.7209,
     "length": 894.36,
     "sps": 446.0
    },
    {
     "steps": 156672,
     "return": -20.48,
     "entropy": 1.7421,
     "length": 894.21,
     "sps": 446.3
    },
    {
     "steps": 158208,
     "return": -20.46,
     "entropy": 1.7481,
     "length": 893.56,
     "sps": 446.3
    },
    {
     "steps": 159744,
     "return": -20.47,
     "entropy": 1.7508,
     "length": 893.08,
     "sps": 446.1
    },
    {
     "steps": 161280,
     "return": -20.48,
     "entropy": 1.7545,
     "length": 893.49,
     "sps": 446.6
    },
    {
     "steps": 162816,
     "return": -20.47,
     "entropy": 1.7493,
     "length": 893.6,
     "sps": 446.8
    },
    {
     "steps": 164352,
     "return": -20.48,
     "entropy": 1.7415,
     "length": 893.71,
     "sps": 446.9
    },
    {
     "steps": 165888,
     "return": -20.46,
     "entropy": 1.7196,
     "length": 895.03,
     "sps": 447.1
    },
    {
     "steps": 167424,
     "return": -20.47,
     "entropy": 1.7292,
     "length": 894.85,
     "sps": 447.1
    },
    {
     "steps": 168960,
     "return": -20.45,
     "entropy": 1.7193,
     "length": 896.4,
     "sps": 447.1
    },
    {
     "steps": 170496,
     "return": -20.46,
     "entropy": 1.7005,
     "length": 898.47,
     "sps": 446.9
    },
    {
     "steps": 172032,
     "return": -20.47,
     "entropy": 1.7181,
     "length": 900.82,
     "sps": 446.8
    },
    {
     "steps": 173568,
     "return": -20.44,
     "entropy": 1.7235,
     "length": 905.58,
     "sps": 447.1
    },
    {
     "steps": 175104,
     "return": -20.44,
     "entropy": 1.741,
     "length": 906.54,
     "sps": 447.0
    },
    {
     "steps": 176640,
     "return": -20.44,
     "entropy": 1.7299,
     "length": 904.88,
     "sps": 446.7
    },
    {
     "steps": 178176,
     "return": -20.45,
     "entropy": 1.737,
     "length": 903.88,
     "sps": 446.5
    },
    {
     "steps": 179712,
     "return": -20.46,
     "entropy": 1.7511,
     "length": 903.37,
     "sps": 446.4
    },
    {
     "steps": 181248,
     "return": -20.46,
     "entropy": 1.7611,
     "length": 903.85,
     "sps": 446.7
    },
    {
     "steps": 182784,
     "return": -20.45,
     "entropy": 1.7579,
     "length": 903.83,
     "sps": 446.7
    },
    {
     "steps": 184320,
     "return": -20.43,
     "entropy": 1.7584,
     "length": 905.7,
     "sps": 446.5
    },
    {
     "steps": 185856,
     "return": -20.42,
     "entropy": 1.751,
     "length": 905.27,
     "sps": 446.6
    },
    {
     "steps": 187392,
     "return": -20.41,
     "entropy": 1.731,
     "length": 910.86,
     "sps": 446.5
    },
    {
     "steps": 188928,
     "return": -20.42,
     "entropy": 1.706,
     "length": 910.31,
     "sps": 446.5
    },
    {
     "steps": 190464,
     "return": -20.43,
     "entropy": 1.7025,
     "length": 906.58,
     "sps": 446.6
    },
    {
     "steps": 192000,
     "return": -20.43,
     "entropy": 1.6756,
     "length": 905.52,
     "sps": 446.5
    },
    {
     "steps": 193536,
     "return": -20.43,
     "entropy": 1.6911,
     "length": 906.09,
     "sps": 446.5
    },
    {
     "steps": 195072,
     "return": -20.44,
     "entropy": 1.6985,
     "length": 904.62,
     "sps": 446.4
    },
    {
     "steps": 196608,
     "return": -20.42,
     "entropy": 1.6721,
     "length": 905.94,
     "sps": 446.4
    },
    {
     "steps": 198144,
     "return": -20.42,
     "entropy": 1.6726,
     "length": 906.52,
     "sps": 446.6
    },
    {
     "steps": 199680,
     "return": -20.4,
     "entropy": 1.6907,
     "length": 904.66,
     "sps": 446.5
    },
    {
     "steps": 201216,
     "return": -20.4,
     "entropy": 1.7012,
     "length": 902.84,
     "sps": 446.5
    },
    {
     "steps": 202752,
     "return": -20.41,
     "entropy": 1.7004,
     "length": 900.75,
     "sps": 446.3
    },
    {
     "steps": 204288,
     "return": -20.41,
     "entropy": 1.6756,
     "length": 900.75,
     "sps": 446.4
    },
    {
     "steps": 205824,
     "return": -20.39,
     "entropy": 1.651,
     "length": 898.75,
     "sps": 446.6
    },
    {
     "steps": 207360,
     "return": -20.39,
     "entropy": 1.6538,
     "length": 899.04,
     "sps": 446.6
    },
    {
     "steps": 208896,
     "return": -20.39,
     "entropy": 1.6341,
     "length": 898.04,
     "sps": 446.5
    },
    {
     "steps": 210432,
     "return": -20.39,
     "entropy": 1.6537,
     "length": 899.35,
     "sps": 446.6
    },
    {
     "steps": 211968,
     "return": -20.4,
     "entropy": 1.672,
     "length": 898.99,
     "sps": 446.5
    },
    {
     "steps": 213504,
     "return": -20.4,
     "entropy": 1.6669,
     "length": 897.2,
     "sps": 446.5
    },
    {
     "steps": 215040,
     "return": -20.4,
     "entropy": 1.6474,
     "length": 894.85,
     "sps": 446.4
    },
    {
     "steps": 216576,
     "return": -20.41,
     "entropy": 1.6236,
     "length": 892.99,
     "sps": 446.5
    },
    {
     "steps": 218112,
     "return": -20.41,
     "entropy": 1.6067,
     "length": 891.7,
     "sps": 446.4
    },
    {
     "steps": 219648,
     "return": -20.4,
     "entropy": 1.6398,
     "length": 893.34,
     "sps": 446.3
    },
    {
     "steps": 221184,
     "return": -20.4,
     "entropy": 1.6502,
     "length": 893.06,
     "sps": 446.3
    },
    {
     "steps": 222720,
     "return": -20.39,
     "entropy": 1.6718,
     "length": 894.88,
     "sps": 446.5
    },
    {
     "steps": 224256,
     "return": -20.39,
     "entropy": 1.6632,
     "length": 894.88,
     "sps": 446.5
    },
    {
     "steps": 225792,
     "return": -20.4,
     "entropy": 1.6792,
     "length": 893.82,
     "sps": 446.5
    },
    {
     "steps": 227328,
     "return": -20.4,
     "entropy": 1.6613,
     "length": 895.13,
     "sps": 446.5
    },
    {
     "steps": 228864,
     "return": -20.38,
     "entropy": 1.6736,
     "length": 897.72,
     "sps": 446.6
    },
    {
     "steps": 230400,
     "return": -20.38,
     "entropy": 1.683,
     "length": 897.72,
     "sps": 446.5
    },
    {
     "steps": 231936,
     "return": -20.37,
     "entropy": 1.6864,
     "length": 898.03,
     "sps": 446.4
    },
    {
     "steps": 233472,
     "return": -20.38,
     "entropy": 1.6854,
     "length": 898.34,
     "sps": 446.4
    },
    {
     "steps": 235008,
     "return": -20.37,
     "entropy": 1.6979,
     "length": 898.41,
     "sps": 446.5
    },
    {
     "steps": 236544,
     "return": -20.37,
     "entropy": 1.6963,
     "length": 898.41,
     "sps": 446.3
    },
    {
     "steps": 238080,
     "return": -20.37,
     "entropy": 1.7104,
     "length": 898.33,
     "sps": 446.3
    },
    {
     "steps": 239616,
     "return": -20.36,
     "entropy": 1.7018,
     "length": 902.21,
     "sps": 446.2
    },
    {
     "steps": 241152,
     "return": -20.36,
     "entropy": 1.7141,
     "length": 902.22,
     "sps": 446.2
    },
    {
     "steps": 242688,
     "return": -20.35,
     "entropy": 1.7187,
     "length": 899.2,
     "sps": 446.1
    },
    {
     "steps": 244224,
     "return": -20.36,
     "entropy": 1.7286,
     "length": 899.57,
     "sps": 446.0
    },
    {
     "steps": 245760,
     "return": -20.33,
     "entropy": 1.7259,
     "length": 902.6,
     "sps": 446.0
    },
    {
     "steps": 247296,
     "return": -20.33,
     "entropy": 1.7324,
     "length": 904.4,
     "sps": 445.8
    },
    {
     "steps": 248832,
     "return": -20.34,
     "entropy": 1.7382,
     "length": 904.14,
     "sps": 445.8
    },
    {
     "steps": 250368,
     "return": -20.33,
     "entropy": 1.747,
     "length": 904.57,
     "sps": 445.8
    },
    {
     "steps": 251904,
     "return": -20.33,
     "entropy": 1.7399,
     "length": 906.07,
     "sps": 445.8
    },
    {
     "steps": 253440,
     "return": -20.33,
     "entropy": 1.716,
     "length": 905.72,
     "sps": 445.9
    },
    {
     "steps": 254976,
     "return": -20.33,
     "entropy": 1.7002,
     "length": 907.89,
     "sps": 446.0
    },
    {
     "steps": 256512,
     "return": -20.32,
     "entropy": 1.708,
     "length": 909.8,
     "sps": 446.0
    },
    {
     "steps": 258048,
     "return": -20.3,
     "entropy": 1.6919,
     "length": 914.07,
     "sps": 446.0
    },
    {
     "steps": 259584,
     "return": -20.32,
     "entropy": 1.6942,
     "length": 912.21,
     "sps": 446.0
    },
    {
     "steps": 261120,
     "return": -20.31,
     "entropy": 1.6966,
     "length": 913.69,
     "sps": 446.1
    },
    {
     "steps": 262656,
     "return": -20.31,
     "entropy": 1.6882,
     "length": 911.36,
     "sps": 446.1
    },
    {
     "steps": 264192,
     "return": -20.34,
     "entropy": 1.6726,
     "length": 909.89,
     "sps": 446.1
    },
    {
     "steps": 265728,
     "return": -20.34,
     "entropy": 1.697,
     "length": 908.8,
     "sps": 446.1
    },
    {
     "steps": 267264,
     "return": -20.35,
     "entropy": 1.721,
     "length": 908.53,
     "sps": 446.2
    },
    {
     "steps": 268800,
     "return": -20.35,
     "entropy": 1.6977,
     "length": 908.53,
     "sps": 446.1
    },
    {
     "steps": 270336,
     "return": -20.35,
     "entropy": 1.7011,
     "length": 908.18,
     "sps": 446.0
    },
    {
     "steps": 271872,
     "return": -20.37,
     "entropy": 1.711,
     "length": 907.45,
     "sps": 446.0
    },
    {
     "steps": 273408,
     "return": -20.39,
     "entropy": 1.7116,
     "length": 905.06,
     "sps": 446.1
    },
    {
     "steps": 274944,
     "return": -20.39,
     "entropy": 1.6931,
     "length": 905.06,
     "sps": 446.1
    },
    {
     "steps": 276480,
     "return": -20.4,
     "entropy": 1.7064,
     "length": 904.76,
     "sps": 446.1
    },
    {
     "steps": 278016,
     "return": -20.42,
     "entropy": 1.6999,
     "length": 901.6,
     "sps": 445.9
    },
    {
     "steps": 279552,
     "return": -20.4,
     "entropy": 1.7165,
     "length": 901.64,
     "sps": 446.0
    },
    {
     "steps": 281088,
     "return": -20.4,
     "entropy": 1.7295,
     "length": 901.68,
     "sps": 445.9
    },
    {
     "steps": 282624,
     "return": -20.39,
     "entropy": 1.7185,
     "length": 905.99,
     "sps": 445.9
    },
    {
     "steps": 284160,
     "return": -20.39,
     "entropy": 1.714,
     "length": 905.99,
     "sps": 445.8
    },
    {
     "steps": 285696,
     "return": -20.39,
     "entropy": 1.719,
     "length": 908.53,
     "sps": 445.9
    },
    {
     "steps": 287232,
     "return": -20.41,
     "entropy": 1.7144,
     "length": 909.64,
     "sps": 445.6
    },
    {
     "steps": 288768,
     "return": -20.41,
     "entropy": 1.7327,
     "length": 908.73,
     "sps": 445.6
    },
    {
     "steps": 290304,
     "return": -20.41,
     "entropy": 1.7339,
     "length": 908.73,
     "sps": 445.7
    },
    {
     "steps": 291840,
     "return": -20.41,
     "entropy": 1.7385,
     "length": 908.73,
     "sps": 445.7
    },
    {
     "steps": 293376,
     "return": -20.42,
     "entropy": 1.742,
     "length": 911.71,
     "sps": 445.6
    },
    {
     "steps": 294912,
     "return": -20.43,
     "entropy": 1.7405,
     "length": 912.09,
     "sps": 445.5
    },
    {
     "steps": 296448,
     "return": -20.43,
     "entropy": 1.7368,
     "length": 911.93,
     "sps": 445.7
    },
    {
     "steps": 297984,
     "return": -20.43,
     "entropy": 1.7289,
     "length": 913.07,
     "sps": 445.7
    },
    {
     "steps": 299520,
     "return": -20.42,
     "entropy": 1.7114,
     "length": 913.08,
     "sps": 445.7
    },
    {
     "steps": 301056,
     "return": -20.4,
     "entropy": 1.6915,
     "length": 918.13,
     "sps": 445.5
    },
    {
     "steps": 302592,
     "return": -20.39,
     "entropy": 1.6712,
     "length": 921.24,
     "sps": 445.4
    },
    {
     "steps": 304128,
     "return": -20.37,
     "entropy": 1.6416,
     "length": 920.73,
     "sps": 445.5
    },
    {
     "steps": 305664,
     "return": -20.35,
     "entropy": 1.6723,
     "length": 922.69,
     "sps": 445.5
    },
    {
     "steps": 307200,
     "return": -20.36,
     "entropy": 1.6708,
     "length": 923.17,
     "sps": 445.5
    },
    {
     "steps": 308736,
     "return": -20.34,
     "entropy": 1.669,
     "length": 924.13,
     "sps": 445.4
    },
    {
     "steps": 310272,
     "return": -20.34,
     "entropy": 1.6845,
     "length": 922.94,
     "sps": 445.3
    },
    {
     "steps": 311808,
     "return": -20.34,
     "entropy": 1.708,
     "length": 922.94,
     "sps": 445.5
    },
    {
     "steps": 313344,
     "return": -20.34,
     "entropy": 1.7041,
     "length": 922.36,
     "sps": 445.5
    },
    {
     "steps": 314880,
     "return": -20.33,
     "entropy": 1.688,
     "length": 923.76,
     "sps": 445.4
    },
    {
     "steps": 316416,
     "return": -20.35,
     "entropy": 1.7093,
     "length": 922.3,
     "sps": 445.1
    },
    {
     "steps": 317952,
     "return": -20.32,
     "entropy": 1.6967,
     "length": 926.64,
     "sps": 445.1
    },
    {
     "steps": 319488,
     "return": -20.3,
     "entropy": 1.7169,
     "length": 929.54,
     "sps": 444.9
    },
    {
     "steps": 321024,
     "return": -20.29,
     "entropy": 1.7303,
     "length": 929.74,
     "sps": 444.7
    },
    {
     "steps": 322560,
     "return": -20.31,
     "entropy": 1.7427,
     "length": 931.96,
     "sps": 444.6
    },
    {
     "steps": 324096,
     "return": -20.31,
     "entropy": 1.7485,
     "length": 931.96,
     "sps": 444.3
    },
    {
     "steps": 325632,
     "return": -20.32,
     "entropy": 1.7474,
     "length": 931.41,
     "sps": 444.1
    },
    {
     "steps": 327168,
     "return": -20.3,
     "entropy": 1.7413,
     "length": 932.71,
     "sps": 444.1
    },
    {
     "steps": 328704,
     "return": -20.3,
     "entropy": 1.7365,
     "length": 932.59,
     "sps": 443.9
    },
    {
     "steps": 330240,
     "return": -20.29,
     "entropy": 1.7351,
     "length": 933.61,
     "sps": 444.2
    },
    {
     "steps": 331776,
     "return": -20.28,
     "entropy": 1.7234,
     "length": 935.38,
     "sps": 444.6
    },
    {
     "steps": 333312,
     "return": -20.31,
     "entropy": 1.7373,
     "length": 934.25,
     "sps": 444.9
    },
    {
     "steps": 334848,
     "return": -20.33,
     "entropy": 1.7276,
     "length": 935.58,
     "sps": 445.2
    },
    {
     "steps": 336384,
     "return": -20.35,
     "entropy": 1.7297,
     "length": 935.29,
     "sps": 445.5
    },
    {
     "steps": 337920,
     "return": -20.33,
     "entropy": 1.7405,
     "length": 938.26,
     "sps": 443.6
    },
    {
     "steps": 339456,
     "return": -20.33,
     "entropy": 1.7396,
     "length": 938.26,
     "sps": 442.0
    },
    {
     "steps": 340992,
     "return": -20.33,
     "entropy": 1.7446,
     "length": 935.5,
     "sps": 442.2
    },
    {
     "steps": 342528,
     "return": -20.34,
     "entropy": 1.7492,
     "length": 935.57,
     "sps": 442.5
    },
    {
     "steps": 344064,
     "return": -20.34,
     "entropy": 1.7558,
     "length": 934.59,
     "sps": 442.8
    },
    {
     "steps": 345600,
     "return": -20.32,
     "entropy": 1.7591,
     "length": 934.27,
     "sps": 443.1
    },
    {
     "steps": 347136,
     "return": -20.33,
     "entropy": 1.7535,
     "length": 931.99,
     "sps": 443.4
    },
    {
     "steps": 348672,
     "return": -20.33,
     "entropy": 1.759,
     "length": 932.68,
     "sps": 443.7
    },
    {
     "steps": 350208,
     "return": -20.33,
     "entropy": 1.7662,
     "length": 932.68,
     "sps": 444.2
    },
    {
     "steps": 351744,
     "return": -20.35,
     "entropy": 1.7691,
     "length": 929.13,
     "sps": 444.6
    },
    {
     "steps": 353280,
     "return": -20.36,
     "entropy": 1.7678,
     "length": 931.87,
     "sps": 445.0
    }
   ],
   "ladder": null,
   "evaluation_seeds": null,
   "clips": [],
   "gifs": [],
   "progress": null
  }
 }
};
