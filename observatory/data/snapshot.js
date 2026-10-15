window.SNAPSHOT = {
 "taken_at": "2026-10-15 04:27:02Z",
 "arcade": [
  {
   "kind": "arcade",
   "key": "racing",
   "title": "Car racing",
   "env_id": "CarRacing-v3",
   "blurb": "Top-down racing. The agent sees the track and steers; an untrained one spins on the grass, a trained one follows the road.",
   "state": "not started",
   "steps": 0,
   "updates": 0,
   "sps": null,
   "return_now": null,
   "entropy_now": null,
   "wall_minutes": null,
   "params": null,
   "eta_minutes": null,
   "seconds_since_update": null,
   "checkpoints": [],
   "curve": [],
   "ladder": null,
   "verdict": null,
   "clips": [],
   "log_tail": [
    "=== Car racing (CarRacing-v3) : 1,200,000 steps on 12 envs -> D:\\github\\game-agents\\runs_arcade\\racing",
    "checkpoint 000 at step 0 (untrained) -> ckpt_000.pt"
   ]
  },
  {
   "kind": "arcade",
   "key": "boxing",
   "title": "Boxing",
   "env_id": "ALE/Boxing-v5",
   "blurb": "Hand to hand. Score is punches landed minus punches taken, so it runs from -100 to +100 and reads at a glance.",
   "state": "finished",
   "steps": 1999872,
   "updates": 1302,
   "sps": 591.2,
   "return_now": 2.55,
   "entropy_now": 2.7859,
   "wall_minutes": 56.4,
   "params": 428131,
   "eta_minutes": null,
   "seconds_since_update": 3636,
   "checkpoints": [
    {
     "tag": "000",
     "steps": 0
    },
    {
     "tag": "005",
     "steps": 99840
    },
    {
     "tag": "015",
     "steps": 299520
    },
    {
     "tag": "035",
     "steps": 700416
    },
    {
     "tag": "065",
     "steps": 1299456
    },
    {
     "tag": "100",
     "steps": 1999872
    }
   ],
   "curve": [
    {
     "steps": 21504,
     "return": -0.25,
     "entropy": 2.8788,
     "sps": 489.3,
     "value_loss": 0.1287
    },
    {
     "steps": 36864,
     "return": -0.25,
     "entropy": 2.8327,
     "sps": 530.7,
     "value_loss": 0.302
    },
    {
     "steps": 52224,
     "return": -0.25,
     "entropy": 2.8459,
     "sps": 544.6,
     "value_loss": 0.1975
    },
    {
     "steps": 67584,
     "return": 0.806,
     "entropy": 2.8273,
     "sps": 559.1,
     "value_loss": 0.2379
    },
    {
     "steps": 82944,
     "return": 0.806,
     "entropy": 2.8135,
     "sps": 569.5,
     "value_loss": 0.3458
    },
    {
     "steps": 98304,
     "return": 1.438,
     "entropy": 2.8205,
     "sps": 574.2,
     "value_loss": 0.2982
    },
    {
     "steps": 113664,
     "return": 1.2,
     "entropy": 2.7974,
     "sps": 578.5,
     "value_loss": 0.316
    },
    {
     "steps": 129024,
     "return": 1.306,
     "entropy": 2.7812,
     "sps": 581.4,
     "value_loss": 0.2047
    },
    {
     "steps": 144384,
     "return": 1.306,
     "entropy": 2.7341,
     "sps": 581.2,
     "value_loss": 0.2162
    },
    {
     "steps": 159744,
     "return": 1.333,
     "entropy": 2.7327,
     "sps": 581.1,
     "value_loss": 0.2844
    },
    {
     "steps": 175104,
     "return": 1.219,
     "entropy": 2.8034,
     "sps": 581.6,
     "value_loss": 0.2209
    },
    {
     "steps": 190464,
     "return": 1.219,
     "entropy": 2.7733,
     "sps": 581.5,
     "value_loss": 0.3205
    },
    {
     "steps": 205824,
     "return": 1.47,
     "entropy": 2.7735,
     "sps": 583.3,
     "value_loss": 0.3195
    },
    {
     "steps": 221184,
     "return": 1.51,
     "entropy": 2.6876,
     "sps": 586.6,
     "value_loss": 0.1257
    },
    {
     "steps": 236544,
     "return": 1.27,
     "entropy": 2.738,
     "sps": 588.9,
     "value_loss": 0.1682
    },
    {
     "steps": 251904,
     "return": 1.27,
     "entropy": 2.7656,
     "sps": 590.4,
     "value_loss": 0.1295
    },
    {
     "steps": 267264,
     "return": 0.99,
     "entropy": 2.7884,
     "sps": 590.0,
     "value_loss": 0.2375
    },
    {
     "steps": 282624,
     "return": 1.32,
     "entropy": 2.751,
     "sps": 589.3,
     "value_loss": 0.2282
    },
    {
     "steps": 297984,
     "return": 1.32,
     "entropy": 2.7225,
     "sps": 589.9,
     "value_loss": 0.2271
    },
    {
     "steps": 313344,
     "return": 1.29,
     "entropy": 2.6688,
     "sps": 591.3,
     "value_loss": 0.2011
    },
    {
     "steps": 328704,
     "return": 1.16,
     "entropy": 2.6692,
     "sps": 593.0,
     "value_loss": 0.2949
    },
    {
     "steps": 344064,
     "return": 1.11,
     "entropy": 2.5881,
     "sps": 592.6,
     "value_loss": 0.2718
    },
    {
     "steps": 359424,
     "return": 1.11,
     "entropy": 2.6234,
     "sps": 589.8,
     "value_loss": 0.2437
    },
    {
     "steps": 374784,
     "return": 1.41,
     "entropy": 2.6042,
     "sps": 589.1,
     "value_loss": 0.2924
    },
    {
     "steps": 390144,
     "return": 1.28,
     "entropy": 2.4969,
     "sps": 589.5,
     "value_loss": 0.0844
    },
    {
     "steps": 405504,
     "return": 1.28,
     "entropy": 2.5961,
     "sps": 590.8,
     "value_loss": 0.1921
    },
    {
     "steps": 420864,
     "return": 1.33,
     "entropy": 2.5849,
     "sps": 591.6,
     "value_loss": 0.2495
    },
    {
     "steps": 436224,
     "return": 1.81,
     "entropy": 2.5591,
     "sps": 592.2,
     "value_loss": 0.2533
    },
    {
     "steps": 451584,
     "return": 1.96,
     "entropy": 2.5369,
     "sps": 592.8,
     "value_loss": 0.166
    },
    {
     "steps": 466944,
     "return": 1.96,
     "entropy": 2.7051,
     "sps": 593.7,
     "value_loss": 0.2714
    },
    {
     "steps": 482304,
     "return": 1.85,
     "entropy": 2.6793,
     "sps": 595.4,
     "value_loss": 0.2736
    },
    {
     "steps": 497664,
     "return": 1.79,
     "entropy": 2.418,
     "sps": 596.1,
     "value_loss": 0.2213
    },
    {
     "steps": 513024,
     "return": 1.7,
     "entropy": 2.5545,
     "sps": 596.8,
     "value_loss": 0.2316
    },
    {
     "steps": 528384,
     "return": 1.95,
     "entropy": 2.5504,
     "sps": 597.5,
     "value_loss": 0.1618
    },
    {
     "steps": 543744,
     "return": 1.27,
     "entropy": 2.635,
     "sps": 598.5,
     "value_loss": 0.3143
    },
    {
     "steps": 559104,
     "return": 1.12,
     "entropy": 2.6728,
     "sps": 598.8,
     "value_loss": 0.2823
    },
    {
     "steps": 574464,
     "return": 1.12,
     "entropy": 2.6971,
     "sps": 600.0,
     "value_loss": 0.3882
    },
    {
     "steps": 589824,
     "return": 1.37,
     "entropy": 2.7369,
     "sps": 601.4,
     "value_loss": 0.3337
    },
    {
     "steps": 605184,
     "return": 1.33,
     "entropy": 2.7175,
     "sps": 602.2,
     "value_loss": 0.2129
    },
    {
     "steps": 620544,
     "return": 1.23,
     "entropy": 2.7783,
     "sps": 603.3,
     "value_loss": 0.1892
    },
    {
     "steps": 635904,
     "return": 1.23,
     "entropy": 2.7844,
     "sps": 604.6,
     "value_loss": 0.2776
    },
    {
     "steps": 651264,
     "return": 1.22,
     "entropy": 2.7825,
     "sps": 605.9,
     "value_loss": 0.2972
    },
    {
     "steps": 666624,
     "return": 1.17,
     "entropy": 2.7525,
     "sps": 605.9,
     "value_loss": 0.3185
    },
    {
     "steps": 681984,
     "return": 1.17,
     "entropy": 2.7796,
     "sps": 606.6,
     "value_loss": 0.2463
    },
    {
     "steps": 697344,
     "return": 1.51,
     "entropy": 2.7936,
     "sps": 606.7,
     "value_loss": 0.2421
    },
    {
     "steps": 712704,
     "return": 1.6,
     "entropy": 2.8504,
     "sps": 607.0,
     "value_loss": 0.2195
    },
    {
     "steps": 728064,
     "return": 1.8,
     "entropy": 2.8711,
     "sps": 607.5,
     "value_loss": 0.1932
    },
    {
     "steps": 743424,
     "return": 1.8,
     "entropy": 2.8726,
     "sps": 608.5,
     "value_loss": 0.1502
    },
    {
     "steps": 758784,
     "return": 2.02,
     "entropy": 2.8472,
     "sps": 609.3,
     "value_loss": 0.4067
    },
    {
     "steps": 774144,
     "return": 2.23,
     "entropy": 2.8312,
     "sps": 609.6,
     "value_loss": 0.2005
    },
    {
     "steps": 789504,
     "return": 2.23,
     "entropy": 2.7974,
     "sps": 610.3,
     "value_loss": 0.361
    },
    {
     "steps": 804864,
     "return": 2.01,
     "entropy": 2.7562,
     "sps": 610.7,
     "value_loss": 0.2801
    },
    {
     "steps": 820224,
     "return": 1.6,
     "entropy": 2.7154,
     "sps": 611.0,
     "value_loss": 0.2595
    },
    {
     "steps": 835584,
     "return": 1.57,
     "entropy": 2.7792,
     "sps": 611.1,
     "value_loss": 0.3886
    },
    {
     "steps": 850944,
     "return": 1.57,
     "entropy": 2.8101,
     "sps": 611.2,
     "value_loss": 0.2787
    },
    {
     "steps": 866304,
     "return": 1.32,
     "entropy": 2.8545,
     "sps": 611.4,
     "value_loss": 0.2233
    },
    {
     "steps": 881664,
     "return": 1.33,
     "entropy": 2.8278,
     "sps": 611.8,
     "value_loss": 0.2275
    },
    {
     "steps": 897024,
     "return": 1.33,
     "entropy": 2.8694,
     "sps": 611.8,
     "value_loss": 0.2855
    },
    {
     "steps": 912384,
     "return": 1.53,
     "entropy": 2.791,
     "sps": 611.4,
     "value_loss": 0.3294
    },
    {
     "steps": 927744,
     "return": 1.76,
     "entropy": 2.8135,
     "sps": 611.2,
     "value_loss": 0.8159
    },
    {
     "steps": 943104,
     "return": 1.61,
     "entropy": 2.8236,
     "sps": 610.9,
     "value_loss": 0.319
    },
    {
     "steps": 958464,
     "return": 1.61,
     "entropy": 2.8494,
     "sps": 610.6,
     "value_loss": 0.2067
    },
    {
     "steps": 973824,
     "return": 1.17,
     "entropy": 2.8373,
     "sps": 610.3,
     "value_loss": 0.2757
    },
    {
     "steps": 989184,
     "return": 1.57,
     "entropy": 2.8288,
     "sps": 609.8,
     "value_loss": 0.3442
    },
    {
     "steps": 1004544,
     "return": 1.57,
     "entropy": 2.798,
     "sps": 609.6,
     "value_loss": 0.3891
    },
    {
     "steps": 1019904,
     "return": 1.98,
     "entropy": 2.7752,
     "sps": 609.3,
     "value_loss": 0.3628
    },
    {
     "steps": 1035264,
     "return": 1.79,
     "entropy": 2.763,
     "sps": 609.0,
     "value_loss": 0.35
    },
    {
     "steps": 1050624,
     "return": 2.05,
     "entropy": 2.7462,
     "sps": 608.6,
     "value_loss": 0.3142
    },
    {
     "steps": 1065984,
     "return": 2.05,
     "entropy": 2.7236,
     "sps": 608.4,
     "value_loss": 0.2958
    },
    {
     "steps": 1081344,
     "return": 1.77,
     "entropy": 2.6161,
     "sps": 607.9,
     "value_loss": 0.7735
    },
    {
     "steps": 1096704,
     "return": 1.03,
     "entropy": 2.696,
     "sps": 607.5,
     "value_loss": 0.3651
    },
    {
     "steps": 1112064,
     "return": 1.2,
     "entropy": 2.6607,
     "sps": 606.3,
     "value_loss": 0.2459
    },
    {
     "steps": 1127424,
     "return": 1.2,
     "entropy": 2.6068,
     "sps": 605.5,
     "value_loss": 0.3394
    },
    {
     "steps": 1142784,
     "return": 1.49,
     "entropy": 2.6208,
     "sps": 605.2,
     "value_loss": 0.1783
    },
    {
     "steps": 1158144,
     "return": 1.67,
     "entropy": 2.5304,
     "sps": 605.0,
     "value_loss": 0.6452
    },
    {
     "steps": 1173504,
     "return": 1.67,
     "entropy": 2.5797,
     "sps": 604.8,
     "value_loss": 0.2153
    },
    {
     "steps": 1188864,
     "return": 1.67,
     "entropy": 2.5491,
     "sps": 604.5,
     "value_loss": 0.3224
    },
    {
     "steps": 1204224,
     "return": 1.58,
     "entropy": 2.5151,
     "sps": 604.5,
     "value_loss": 0.3946
    },
    {
     "steps": 1219584,
     "return": 1.14,
     "entropy": 2.5187,
     "sps": 604.3,
     "value_loss": 0.2263
    },
    {
     "steps": 1234944,
     "return": 1.14,
     "entropy": 2.6339,
     "sps": 604.1,
     "value_loss": 0.3324
    },
    {
     "steps": 1250304,
     "return": 1.01,
     "entropy": 2.6535,
     "sps": 603.8,
     "value_loss": 0.2558
    },
    {
     "steps": 1265664,
     "return": 1.01,
     "entropy": 2.5048,
     "sps": 603.6,
     "value_loss": 0.4102
    },
    {
     "steps": 1281024,
     "return": 1.01,
     "entropy": 2.7142,
     "sps": 603.5,
     "value_loss": 0.3088
    },
    {
     "steps": 1296384,
     "return": 0.83,
     "entropy": 2.7498,
     "sps": 603.3,
     "value_loss": 0.2845
    },
    {
     "steps": 1311744,
     "return": 0.59,
     "entropy": 2.7103,
     "sps": 603.1,
     "value_loss": 0.274
    },
    {
     "steps": 1327104,
     "return": 0.14,
     "entropy": 2.6837,
     "sps": 603.0,
     "value_loss": 0.2744
    },
    {
     "steps": 1342464,
     "return": 0.14,
     "entropy": 2.7796,
     "sps": 602.9,
     "value_loss": 0.333
    },
    {
     "steps": 1357824,
     "return": 0.29,
     "entropy": 2.7807,
     "sps": 602.7,
     "value_loss": 0.2494
    },
    {
     "steps": 1373184,
     "return": 0.06,
     "entropy": 2.7866,
     "sps": 602.6,
     "value_loss": 0.2763
    },
    {
     "steps": 1388544,
     "return": 0.06,
     "entropy": 2.8415,
     "sps": 602.3,
     "value_loss": 0.2369
    },
    {
     "steps": 1403904,
     "return": 0.22,
     "entropy": 2.7994,
     "sps": 602.2,
     "value_loss": 0.2297
    },
    {
     "steps": 1419264,
     "return": 0.55,
     "entropy": 2.832,
     "sps": 602.1,
     "value_loss": 0.1608
    },
    {
     "steps": 1434624,
     "return": 0.83,
     "entropy": 2.8471,
     "sps": 602.0,
     "value_loss": 0.4138
    },
    {
     "steps": 1449984,
     "return": 0.83,
     "entropy": 2.82,
     "sps": 601.8,
     "value_loss": 0.2725
    },
    {
     "steps": 1465344,
     "return": 1.11,
     "entropy": 2.8155,
     "sps": 601.6,
     "value_loss": 0.3473
    },
    {
     "steps": 1480704,
     "return": 1.34,
     "entropy": 2.7854,
     "sps": 601.4,
     "value_loss": 0.3204
    },
    {
     "steps": 1496064,
     "return": 1.34,
     "entropy": 2.7614,
     "sps": 601.2,
     "value_loss": 0.286
    },
    {
     "steps": 1511424,
     "return": 1.43,
     "entropy": 2.7573,
     "sps": 599.6,
     "value_loss": 0.2637
    },
    {
     "steps": 1526784,
     "return": 1.35,
     "entropy": 2.8531,
     "sps": 597.1,
     "value_loss": 0.2137
    },
    {
     "steps": 1542144,
     "return": 1.3,
     "entropy": 2.8405,
     "sps": 594.6,
     "value_loss": 0.224
    },
    {
     "steps": 1557504,
     "return": 1.3,
     "entropy": 2.8079,
     "sps": 593.1,
     "value_loss": 0.259
    },
    {
     "steps": 1572864,
     "return": 1.01,
     "entropy": 2.8549,
     "sps": 592.8,
     "value_loss": 0.3019
    },
    {
     "steps": 1588224,
     "return": 1.24,
     "entropy": 2.8456,
     "sps": 592.7,
     "value_loss": 0.2321
    },
    {
     "steps": 1603584,
     "return": 1.33,
     "entropy": 2.8459,
     "sps": 592.7,
     "value_loss": 0.2919
    },
    {
     "steps": 1618944,
     "return": 1.45,
     "entropy": 2.8326,
     "sps": 592.6,
     "value_loss": 0.2521
    },
    {
     "steps": 1634304,
     "return": 1.38,
     "entropy": 2.8427,
     "sps": 592.6,
     "value_loss": 0.2596
    },
    {
     "steps": 1649664,
     "return": 1.42,
     "entropy": 2.81,
     "sps": 592.6,
     "value_loss": 0.2523
    },
    {
     "steps": 1665024,
     "return": 1.42,
     "entropy": 2.8419,
     "sps": 592.5,
     "value_loss": 0.2078
    },
    {
     "steps": 1680384,
     "return": 1.39,
     "entropy": 2.8382,
     "sps": 592.5,
     "value_loss": 0.3232
    },
    {
     "steps": 1695744,
     "return": 1.43,
     "entropy": 2.8512,
     "sps": 592.4,
     "value_loss": 0.2518
    },
    {
     "steps": 1711104,
     "return": 1.59,
     "entropy": 2.7465,
     "sps": 592.4,
     "value_loss": 0.5505
    },
    {
     "steps": 1726464,
     "return": 1.59,
     "entropy": 2.6579,
     "sps": 592.4,
     "value_loss": 0.2925
    },
    {
     "steps": 1741824,
     "return": 2.19,
     "entropy": 2.7974,
     "sps": 592.3,
     "value_loss": 0.2333
    },
    {
     "steps": 1757184,
     "return": 1.92,
     "entropy": 2.7982,
     "sps": 592.3,
     "value_loss": 0.3214
    },
    {
     "steps": 1772544,
     "return": 1.92,
     "entropy": 2.7543,
     "sps": 592.2,
     "value_loss": 0.2428
    },
    {
     "steps": 1787904,
     "return": 1.91,
     "entropy": 2.7845,
     "sps": 592.2,
     "value_loss": 0.311
    },
    {
     "steps": 1803264,
     "return": 2.15,
     "entropy": 2.7977,
     "sps": 592.1,
     "value_loss": 0.1676
    },
    {
     "steps": 1818624,
     "return": 2.57,
     "entropy": 2.7629,
     "sps": 592.0,
     "value_loss": 0.2742
    },
    {
     "steps": 1833984,
     "return": 2.57,
     "entropy": 2.7725,
     "sps": 592.0,
     "value_loss": 0.2356
    },
    {
     "steps": 1849344,
     "return": 2.67,
     "entropy": 2.729,
     "sps": 591.9,
     "value_loss": 0.3138
    },
    {
     "steps": 1864704,
     "return": 2.71,
     "entropy": 2.7063,
     "sps": 591.8,
     "value_loss": 0.413
    },
    {
     "steps": 1880064,
     "return": 2.71,
     "entropy": 2.7748,
     "sps": 591.8,
     "value_loss": 0.2013
    },
    {
     "steps": 1895424,
     "return": 3.14,
     "entropy": 2.7992,
     "sps": 591.7,
     "value_loss": 0.2991
    },
    {
     "steps": 1910784,
     "return": 2.79,
     "entropy": 2.7401,
     "sps": 591.7,
     "value_loss": 0.4491
    },
    {
     "steps": 1926144,
     "return": 3.14,
     "entropy": 2.694,
     "sps": 591.6,
     "value_loss": 0.3824
    },
    {
     "steps": 1941504,
     "return": 3.14,
     "entropy": 2.7704,
     "sps": 591.5,
     "value_loss": 0.2897
    },
    {
     "steps": 1956864,
     "return": 3.06,
     "entropy": 2.7863,
     "sps": 591.4,
     "value_loss": 0.3618
    },
    {
     "steps": 1972224,
     "return": 2.56,
     "entropy": 2.7916,
     "sps": 591.3,
     "value_loss": 0.2435
    },
    {
     "steps": 1987584,
     "return": 2.56,
     "entropy": 2.7879,
     "sps": 591.2,
     "value_loss": 0.618
    },
    {
     "steps": 1999872,
     "return": 2.55,
     "entropy": 2.7859,
     "sps": 591.2,
     "value_loss": 0.3122
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
   "verdict": {
    "label": "no gain",
    "detail": "-0.5 against the untrained network over 8 episodes"
   },
   "clips": [
    "progress.mp4",
    "step_000.mp4",
    "step_035.mp4",
    "step_100.mp4"
   ],
   "log_tail": [
    "  File \"C:\\Users\\dell\\AppData\\Roaming\\uv\\python\\cpython-3.12-windows-x86_64-none\\Lib\\multiprocessing\\connection.py\", line 337, in _recv_bytes",
    "    raise EOFError",
    "  File \"D:\\github\\game-agents\\arcade\\vec.py\", line 46, in _worker",
    "    cmd, data = remote.recv()",
    "                ^^^^^^^^^^^^^",
    "EOFError",
    "  File \"C:\\Users\\dell\\AppData\\Roaming\\uv\\python\\cpython-3.12-windows-x86_64-none\\Lib\\multiprocessing\\connection.py\", line 250, in recv",
    "    buf = self._recv_bytes()",
    "          ^^^^^^^^^^^^^^^^^^",
    "  File \"C:\\Users\\dell\\AppData\\Roaming\\uv\\python\\cpython-3.12-windows-x86_64-none\\Lib\\multiprocessing\\connection.py\", line 337, in _recv_bytes",
    "    raise EOFError",
    "EOFError"
   ]
  },
  {
   "kind": "arcade",
   "key": "platformer",
   "title": "Platformer",
   "env_id": "ALE/Kangaroo-v5",
   "blurb": "Climb the ladders, punch the monkeys, reach the top. The legal stand-in for Mario: a platformer with ROMs that ship licensed.",
   "state": "not started",
   "steps": 0,
   "updates": 0,
   "sps": null,
   "return_now": null,
   "entropy_now": null,
   "wall_minutes": null,
   "params": null,
   "eta_minutes": null,
   "seconds_since_update": null,
   "checkpoints": [],
   "curve": [],
   "ladder": null,
   "verdict": null,
   "clips": [],
   "log_tail": [
    "  File \"C:\\Users\\dell\\AppData\\Roaming\\uv\\python\\cpython-3.12-windows-x86_64-none\\Lib\\multiprocessing\\connection.py\", line 337, in _recv_bytes",
    "    raise EOFError",
    "  File \"D:\\github\\game-agents\\arcade\\vec.py\", line 46, in _worker",
    "    cmd, data = remote.recv()",
    "                ^^^^^^^^^^^^^",
    "EOFError",
    "  File \"C:\\Users\\dell\\AppData\\Roaming\\uv\\python\\cpython-3.12-windows-x86_64-none\\Lib\\multiprocessing\\connection.py\", line 250, in recv",
    "    buf = self._recv_bytes()",
    "          ^^^^^^^^^^^^^^^^^^",
    "  File \"C:\\Users\\dell\\AppData\\Roaming\\uv\\python\\cpython-3.12-windows-x86_64-none\\Lib\\multiprocessing\\connection.py\", line 337, in _recv_bytes",
    "    raise EOFError",
    "EOFError"
   ]
  },
  {
   "kind": "arcade",
   "key": "pingpong",
   "title": "Table tennis",
   "env_id": "ALE/Pong-v5",
   "blurb": "Score runs from -21 to +21, so there is nowhere for a weak agent to hide: it starts losing every rally and ends winning them.",
   "state": "finished",
   "steps": 1999872,
   "updates": 1302,
   "sps": 559.8,
   "return_now": -14.4,
   "entropy_now": 1.2063,
   "wall_minutes": 59.6,
   "params": 425047,
   "eta_minutes": null,
   "seconds_since_update": 22,
   "checkpoints": [
    {
     "tag": "000",
     "steps": 0
    },
    {
     "tag": "005",
     "steps": 99840
    },
    {
     "tag": "015",
     "steps": 299520
    },
    {
     "tag": "035",
     "steps": 700416
    },
    {
     "tag": "065",
     "steps": 1299456
    },
    {
     "tag": "100",
     "steps": 1999872
    }
   ],
   "curve": [
    {
     "steps": 9216,
     "return": -21.0,
     "entropy": 1.7761,
     "sps": 398.7,
     "value_loss": 0.0629
    },
    {
     "steps": 24576,
     "return": -20.417,
     "entropy": 1.7731,
     "sps": 442.8,
     "value_loss": 0.0564
    },
    {
     "steps": 39936,
     "return": -20.575,
     "entropy": 1.7696,
     "sps": 441.8,
     "value_loss": 0.0564
    },
    {
     "steps": 55296,
     "return": -20.474,
     "entropy": 1.6244,
     "sps": 442.5,
     "value_loss": 0.0338
    },
    {
     "steps": 70656,
     "return": -20.411,
     "entropy": 1.6949,
     "sps": 443.5,
     "value_loss": 0.0176
    },
    {
     "steps": 86016,
     "return": -20.441,
     "entropy": 1.6918,
     "sps": 441.8,
     "value_loss": 0.0365
    },
    {
     "steps": 101376,
     "return": -20.39,
     "entropy": 1.7333,
     "sps": 442.3,
     "value_loss": 0.0357
    },
    {
     "steps": 116736,
     "return": -20.44,
     "entropy": 1.7586,
     "sps": 443.6,
     "value_loss": 0.0318
    },
    {
     "steps": 132096,
     "return": -20.41,
     "entropy": 1.7244,
     "sps": 445.2,
     "value_loss": 0.0274
    },
    {
     "steps": 147456,
     "return": -20.46,
     "entropy": 1.7312,
     "sps": 446.2,
     "value_loss": 0.0438
    },
    {
     "steps": 162816,
     "return": -20.47,
     "entropy": 1.7493,
     "sps": 446.8,
     "value_loss": 0.0541
    },
    {
     "steps": 178176,
     "return": -20.45,
     "entropy": 1.737,
     "sps": 446.5,
     "value_loss": 0.0339
    },
    {
     "steps": 193536,
     "return": -20.43,
     "entropy": 1.6911,
     "sps": 446.5,
     "value_loss": 0.0365
    },
    {
     "steps": 208896,
     "return": -20.39,
     "entropy": 1.6341,
     "sps": 446.5,
     "value_loss": 0.0244
    },
    {
     "steps": 224256,
     "return": -20.39,
     "entropy": 1.6632,
     "sps": 446.5,
     "value_loss": 0.0262
    },
    {
     "steps": 239616,
     "return": -20.36,
     "entropy": 1.7018,
     "sps": 446.2,
     "value_loss": 0.0286
    },
    {
     "steps": 254976,
     "return": -20.33,
     "entropy": 1.7002,
     "sps": 446.0,
     "value_loss": 0.0405
    },
    {
     "steps": 270336,
     "return": -20.35,
     "entropy": 1.7011,
     "sps": 446.0,
     "value_loss": 0.0344
    },
    {
     "steps": 285696,
     "return": -20.39,
     "entropy": 1.719,
     "sps": 445.9,
     "value_loss": 0.0286
    },
    {
     "steps": 301056,
     "return": -20.4,
     "entropy": 1.6915,
     "sps": 445.5,
     "value_loss": 0.0258
    },
    {
     "steps": 316416,
     "return": -20.35,
     "entropy": 1.7093,
     "sps": 445.1,
     "value_loss": 0.0415
    },
    {
     "steps": 331776,
     "return": -20.28,
     "entropy": 1.7234,
     "sps": 444.6,
     "value_loss": 0.0246
    },
    {
     "steps": 347136,
     "return": -20.33,
     "entropy": 1.7535,
     "sps": 443.4,
     "value_loss": 0.0375
    },
    {
     "steps": 362496,
     "return": -20.34,
     "entropy": 1.7712,
     "sps": 447.2,
     "value_loss": 0.044
    },
    {
     "steps": 377856,
     "return": -20.24,
     "entropy": 1.7705,
     "sps": 451.3,
     "value_loss": 0.0414
    },
    {
     "steps": 393216,
     "return": -20.2,
     "entropy": 1.7251,
     "sps": 452.9,
     "value_loss": 0.0404
    },
    {
     "steps": 408576,
     "return": -20.22,
     "entropy": 1.7148,
     "sps": 455.3,
     "value_loss": 0.0375
    },
    {
     "steps": 423936,
     "return": -20.28,
     "entropy": 1.7203,
     "sps": 458.8,
     "value_loss": 0.0311
    },
    {
     "steps": 439296,
     "return": -20.24,
     "entropy": 1.6832,
     "sps": 462.4,
     "value_loss": 0.0233
    },
    {
     "steps": 454656,
     "return": -20.28,
     "entropy": 1.6919,
     "sps": 465.9,
     "value_loss": 0.0277
    },
    {
     "steps": 470016,
     "return": -20.41,
     "entropy": 1.6998,
     "sps": 469.3,
     "value_loss": 0.0224
    },
    {
     "steps": 485376,
     "return": -20.39,
     "entropy": 1.7305,
     "sps": 472.6,
     "value_loss": 0.0352
    },
    {
     "steps": 500736,
     "return": -20.4,
     "entropy": 1.7018,
     "sps": 475.9,
     "value_loss": 0.0271
    },
    {
     "steps": 516096,
     "return": -20.34,
     "entropy": 1.7362,
     "sps": 478.8,
     "value_loss": 0.0258
    },
    {
     "steps": 531456,
     "return": -20.26,
     "entropy": 1.6811,
     "sps": 481.6,
     "value_loss": 0.0219
    },
    {
     "steps": 546816,
     "return": -20.2,
     "entropy": 1.6628,
     "sps": 484.4,
     "value_loss": 0.0173
    },
    {
     "steps": 562176,
     "return": -20.16,
     "entropy": 1.7046,
     "sps": 486.9,
     "value_loss": 0.027
    },
    {
     "steps": 577536,
     "return": -20.13,
     "entropy": 1.6829,
     "sps": 489.5,
     "value_loss": 0.0336
    },
    {
     "steps": 592896,
     "return": -20.08,
     "entropy": 1.6886,
     "sps": 491.7,
     "value_loss": 0.047
    },
    {
     "steps": 608256,
     "return": -20.02,
     "entropy": 1.6655,
     "sps": 494.1,
     "value_loss": 0.0402
    },
    {
     "steps": 623616,
     "return": -19.98,
     "entropy": 1.6708,
     "sps": 496.3,
     "value_loss": 0.0284
    },
    {
     "steps": 638976,
     "return": -19.99,
     "entropy": 1.7033,
     "sps": 498.5,
     "value_loss": 0.0293
    },
    {
     "steps": 654336,
     "return": -19.87,
     "entropy": 1.7122,
     "sps": 500.4,
     "value_loss": 0.0297
    },
    {
     "steps": 669696,
     "return": -19.94,
     "entropy": 1.7092,
     "sps": 502.4,
     "value_loss": 0.0321
    },
    {
     "steps": 685056,
     "return": -19.93,
     "entropy": 1.6851,
     "sps": 504.1,
     "value_loss": 0.0537
    },
    {
     "steps": 700416,
     "return": -19.97,
     "entropy": 1.6829,
     "sps": 505.8,
     "value_loss": 0.0359
    },
    {
     "steps": 715776,
     "return": -20.0,
     "entropy": 1.6946,
     "sps": 507.5,
     "value_loss": 0.0426
    },
    {
     "steps": 731136,
     "return": -19.96,
     "entropy": 1.6555,
     "sps": 509.0,
     "value_loss": 0.031
    },
    {
     "steps": 746496,
     "return": -19.81,
     "entropy": 1.6226,
     "sps": 510.6,
     "value_loss": 0.0318
    },
    {
     "steps": 761856,
     "return": -19.74,
     "entropy": 1.572,
     "sps": 512.2,
     "value_loss": 0.0421
    },
    {
     "steps": 777216,
     "return": -19.58,
     "entropy": 1.5608,
     "sps": 513.7,
     "value_loss": 0.0388
    },
    {
     "steps": 792576,
     "return": -19.39,
     "entropy": 1.4888,
     "sps": 515.2,
     "value_loss": 0.0383
    },
    {
     "steps": 807936,
     "return": -19.31,
     "entropy": 1.5124,
     "sps": 516.7,
     "value_loss": 0.0462
    },
    {
     "steps": 823296,
     "return": -19.15,
     "entropy": 1.468,
     "sps": 518.1,
     "value_loss": 0.0463
    },
    {
     "steps": 838656,
     "return": -19.02,
     "entropy": 1.4757,
     "sps": 519.4,
     "value_loss": 0.0495
    },
    {
     "steps": 854016,
     "return": -18.94,
     "entropy": 1.4523,
     "sps": 520.8,
     "value_loss": 0.0405
    },
    {
     "steps": 869376,
     "return": -18.85,
     "entropy": 1.4305,
     "sps": 522.0,
     "value_loss": 0.0406
    },
    {
     "steps": 884736,
     "return": -18.72,
     "entropy": 1.4935,
     "sps": 523.3,
     "value_loss": 0.0418
    },
    {
     "steps": 900096,
     "return": -18.65,
     "entropy": 1.4854,
     "sps": 524.5,
     "value_loss": 0.059
    },
    {
     "steps": 915456,
     "return": -18.43,
     "entropy": 1.5374,
     "sps": 525.7,
     "value_loss": 0.0424
    },
    {
     "steps": 930816,
     "return": -18.3,
     "entropy": 1.4978,
     "sps": 526.8,
     "value_loss": 0.0327
    },
    {
     "steps": 946176,
     "return": -18.22,
     "entropy": 1.4949,
     "sps": 528.0,
     "value_loss": 0.0443
    },
    {
     "steps": 961536,
     "return": -18.0,
     "entropy": 1.4593,
     "sps": 529.0,
     "value_loss": 0.0406
    },
    {
     "steps": 976896,
     "return": -17.88,
     "entropy": 1.4315,
     "sps": 530.1,
     "value_loss": 0.0466
    },
    {
     "steps": 992256,
     "return": -17.73,
     "entropy": 1.4018,
     "sps": 531.2,
     "value_loss": 0.045
    },
    {
     "steps": 1007616,
     "return": -17.65,
     "entropy": 1.3434,
     "sps": 531.9,
     "value_loss": 0.0439
    },
    {
     "steps": 1022976,
     "return": -17.59,
     "entropy": 1.3698,
     "sps": 532.8,
     "value_loss": 0.0504
    },
    {
     "steps": 1038336,
     "return": -17.29,
     "entropy": 1.4073,
     "sps": 533.8,
     "value_loss": 0.0335
    },
    {
     "steps": 1053696,
     "return": -17.14,
     "entropy": 1.3019,
     "sps": 534.7,
     "value_loss": 0.0448
    },
    {
     "steps": 1069056,
     "return": -16.8,
     "entropy": 1.3264,
     "sps": 535.5,
     "value_loss": 0.0352
    },
    {
     "steps": 1084416,
     "return": -16.74,
     "entropy": 1.3583,
     "sps": 536.3,
     "value_loss": 0.0365
    },
    {
     "steps": 1099776,
     "return": -16.53,
     "entropy": 1.3002,
     "sps": 537.1,
     "value_loss": 0.0292
    },
    {
     "steps": 1115136,
     "return": -16.39,
     "entropy": 1.2518,
     "sps": 537.9,
     "value_loss": 0.0388
    },
    {
     "steps": 1130496,
     "return": -16.4,
     "entropy": 1.1634,
     "sps": 538.7,
     "value_loss": 0.0315
    },
    {
     "steps": 1145856,
     "return": -16.25,
     "entropy": 1.2223,
     "sps": 539.4,
     "value_loss": 0.0412
    },
    {
     "steps": 1161216,
     "return": -16.12,
     "entropy": 1.2491,
     "sps": 540.2,
     "value_loss": 0.0307
    },
    {
     "steps": 1176576,
     "return": -16.06,
     "entropy": 1.253,
     "sps": 541.0,
     "value_loss": 0.0372
    },
    {
     "steps": 1191936,
     "return": -15.78,
     "entropy": 1.2453,
     "sps": 541.6,
     "value_loss": 0.0454
    },
    {
     "steps": 1207296,
     "return": -15.64,
     "entropy": 1.2286,
     "sps": 542.1,
     "value_loss": 0.045
    },
    {
     "steps": 1222656,
     "return": -15.48,
     "entropy": 1.2137,
     "sps": 542.8,
     "value_loss": 0.0507
    },
    {
     "steps": 1238016,
     "return": -15.19,
     "entropy": 1.2256,
     "sps": 543.4,
     "value_loss": 0.0396
    },
    {
     "steps": 1253376,
     "return": -15.06,
     "entropy": 1.1942,
     "sps": 544.0,
     "value_loss": 0.03
    },
    {
     "steps": 1268736,
     "return": -15.1,
     "entropy": 1.1628,
     "sps": 544.7,
     "value_loss": 0.044
    },
    {
     "steps": 1284096,
     "return": -14.87,
     "entropy": 1.1028,
     "sps": 545.3,
     "value_loss": 0.0323
    },
    {
     "steps": 1299456,
     "return": -14.84,
     "entropy": 1.0655,
     "sps": 545.9,
     "value_loss": 0.0415
    },
    {
     "steps": 1314816,
     "return": -14.55,
     "entropy": 1.0496,
     "sps": 546.4,
     "value_loss": 0.0353
    },
    {
     "steps": 1330176,
     "return": -14.47,
     "entropy": 1.0815,
     "sps": 547.1,
     "value_loss": 0.0393
    },
    {
     "steps": 1345536,
     "return": -14.34,
     "entropy": 1.1257,
     "sps": 547.6,
     "value_loss": 0.0327
    },
    {
     "steps": 1360896,
     "return": -14.32,
     "entropy": 1.1102,
     "sps": 548.0,
     "value_loss": 0.0414
    },
    {
     "steps": 1376256,
     "return": -13.91,
     "entropy": 1.1264,
     "sps": 548.5,
     "value_loss": 0.0334
    },
    {
     "steps": 1391616,
     "return": -14.11,
     "entropy": 1.1865,
     "sps": 549.1,
     "value_loss": 0.0358
    },
    {
     "steps": 1406976,
     "return": -14.16,
     "entropy": 1.2405,
     "sps": 549.8,
     "value_loss": 0.0422
    },
    {
     "steps": 1422336,
     "return": -14.29,
     "entropy": 1.2117,
     "sps": 550.3,
     "value_loss": 0.0345
    },
    {
     "steps": 1437696,
     "return": -14.29,
     "entropy": 1.1981,
     "sps": 550.8,
     "value_loss": 0.0373
    },
    {
     "steps": 1453056,
     "return": -14.43,
     "entropy": 1.2522,
     "sps": 551.3,
     "value_loss": 0.0251
    },
    {
     "steps": 1468416,
     "return": -14.63,
     "entropy": 1.2795,
     "sps": 551.9,
     "value_loss": 0.0388
    },
    {
     "steps": 1483776,
     "return": -14.84,
     "entropy": 1.2111,
     "sps": 552.3,
     "value_loss": 0.0342
    },
    {
     "steps": 1499136,
     "return": -14.82,
     "entropy": 1.2084,
     "sps": 552.8,
     "value_loss": 0.0254
    },
    {
     "steps": 1514496,
     "return": -14.99,
     "entropy": 1.2168,
     "sps": 553.3,
     "value_loss": 0.0291
    },
    {
     "steps": 1529856,
     "return": -15.26,
     "entropy": 1.2151,
     "sps": 553.3,
     "value_loss": 0.0289
    },
    {
     "steps": 1545216,
     "return": -15.2,
     "entropy": 1.2632,
     "sps": 553.7,
     "value_loss": 0.02
    },
    {
     "steps": 1560576,
     "return": -15.29,
     "entropy": 1.2884,
     "sps": 554.2,
     "value_loss": 0.0338
    },
    {
     "steps": 1575936,
     "return": -15.46,
     "entropy": 1.3088,
     "sps": 554.7,
     "value_loss": 0.0246
    },
    {
     "steps": 1591296,
     "return": -15.55,
     "entropy": 1.2926,
     "sps": 555.0,
     "value_loss": 0.039
    },
    {
     "steps": 1606656,
     "return": -15.65,
     "entropy": 1.2829,
     "sps": 555.5,
     "value_loss": 0.0294
    },
    {
     "steps": 1622016,
     "return": -15.37,
     "entropy": 1.1949,
     "sps": 555.9,
     "value_loss": 0.0403
    },
    {
     "steps": 1637376,
     "return": -15.37,
     "entropy": 1.2328,
     "sps": 556.4,
     "value_loss": 0.0339
    },
    {
     "steps": 1652736,
     "return": -15.28,
     "entropy": 1.1601,
     "sps": 556.9,
     "value_loss": 0.0263
    },
    {
     "steps": 1668096,
     "return": -15.51,
     "entropy": 1.1411,
     "sps": 557.4,
     "value_loss": 0.0389
    },
    {
     "steps": 1683456,
     "return": -15.6,
     "entropy": 1.2072,
     "sps": 558.1,
     "value_loss": 0.0422
    },
    {
     "steps": 1698816,
     "return": -15.44,
     "entropy": 1.1783,
     "sps": 558.7,
     "value_loss": 0.0305
    },
    {
     "steps": 1714176,
     "return": -15.22,
     "entropy": 1.2069,
     "sps": 559.1,
     "value_loss": 0.0358
    },
    {
     "steps": 1729536,
     "return": -15.24,
     "entropy": 1.0932,
     "sps": 559.6,
     "value_loss": 0.0354
    },
    {
     "steps": 1744896,
     "return": -14.96,
     "entropy": 1.0725,
     "sps": 559.1,
     "value_loss": 0.0412
    },
    {
     "steps": 1760256,
     "return": -14.94,
     "entropy": 1.0267,
     "sps": 559.3,
     "value_loss": 0.0283
    },
    {
     "steps": 1775616,
     "return": -14.6,
     "entropy": 1.1552,
     "sps": 559.7,
     "value_loss": 0.0287
    },
    {
     "steps": 1790976,
     "return": -14.52,
     "entropy": 1.1781,
     "sps": 559.7,
     "value_loss": 0.0237
    },
    {
     "steps": 1806336,
     "return": -14.53,
     "entropy": 1.127,
     "sps": 559.5,
     "value_loss": 0.033
    },
    {
     "steps": 1821696,
     "return": -14.1,
     "entropy": 1.1329,
     "sps": 559.4,
     "value_loss": 0.0248
    },
    {
     "steps": 1837056,
     "return": -14.45,
     "entropy": 1.1391,
     "sps": 559.5,
     "value_loss": 0.0266
    },
    {
     "steps": 1852416,
     "return": -14.5,
     "entropy": 1.1362,
     "sps": 559.6,
     "value_loss": 0.0258
    },
    {
     "steps": 1867776,
     "return": -14.29,
     "entropy": 1.1969,
     "sps": 559.6,
     "value_loss": 0.0372
    },
    {
     "steps": 1883136,
     "return": -14.3,
     "entropy": 1.2164,
     "sps": 560.0,
     "value_loss": 0.0369
    },
    {
     "steps": 1898496,
     "return": -14.17,
     "entropy": 1.2066,
     "sps": 560.2,
     "value_loss": 0.0312
    },
    {
     "steps": 1913856,
     "return": -14.14,
     "entropy": 1.2241,
     "sps": 560.3,
     "value_loss": 0.0417
    },
    {
     "steps": 1929216,
     "return": -14.18,
     "entropy": 1.2141,
     "sps": 560.5,
     "value_loss": 0.025
    },
    {
     "steps": 1944576,
     "return": -14.35,
     "entropy": 1.1985,
     "sps": 560.5,
     "value_loss": 0.0339
    },
    {
     "steps": 1959936,
     "return": -14.28,
     "entropy": 1.2001,
     "sps": 560.1,
     "value_loss": 0.034
    },
    {
     "steps": 1975296,
     "return": -14.4,
     "entropy": 1.212,
     "sps": 560.1,
     "value_loss": 0.0252
    },
    {
     "steps": 1990656,
     "return": -14.34,
     "entropy": 1.2221,
     "sps": 560.0,
     "value_loss": 0.0498
    },
    {
     "steps": 1999872,
     "return": -14.4,
     "entropy": 1.2063,
     "sps": 559.8,
     "value_loss": 0.0307
    }
   ],
   "ladder": null,
   "verdict": null,
   "clips": [],
   "log_tail": [
    "{",
    " \"game\": \"pingpong\",",
    " \"env_id\": \"ALE/Pong-v5\",",
    " \"updates\": 1302,",
    " \"steps\": 1999872,",
    " \"wall_seconds\": 3574.1,",
    " \"final_return_mean\": -14.4,",
    " \"params\": 425047,",
    " \"width\": 1,",
    " \"device\": \"cpu\",",
    " \"envs\": 12",
    "}"
   ]
  }
 ],
 "projects": [
  {
   "kind": "project",
   "key": "doom",
   "title": "DOOM from pixels",
   "env_id": "ViZDoom defend_the_center",
   "state": "finished",
   "headline": "9.80 kills",
   "baseline": "1.23 scripted",
   "detail": "1,999,872 steps, 59 min CPU",
   "rows": [
    {
     "agent": "random",
     "mean": 0.0,
     "std": 0.91
    },
    {
     "agent": "spray",
     "mean": 1.23,
     "std": 0.82
    },
    {
     "agent": "ppo-greedy",
     "mean": 9.8,
     "std": 1.47
    },
    {
     "agent": "ppo-sampled",
     "mean": 9.23,
     "std": 1.33
    }
   ]
  },
  {
   "kind": "project",
   "key": "crafter",
   "title": "Crafter planner",
   "env_id": "Crafter",
   "state": "finished",
   "headline": "12.55% score",
   "baseline": "1.13% random",
   "detail": "15/22 achievements over 30 episodes, no training at all",
   "rows": [
    {
     "agent": "planner",
     "mean": 12.55,
     "std": null
    }
   ]
  },
  {
   "kind": "project",
   "key": "brogue",
   "title": "Brogue, screen-driven",
   "env_id": "Brogue CE",
   "state": "finished",
   "headline": "4.5 descents/game",
   "baseline": "0.25 random keys",
   "detail": "screenshots in, keystrokes out, no API",
   "rows": [
    {
     "agent": "random",
     "mean": 0.25,
     "std": null
    },
    {
     "agent": "explorer",
     "mean": 4.5,
     "std": null
    }
   ]
  }
 ],
 "machine": {
  "cpu_percent": 97.9,
  "python_processes": 48,
  "gpu": {
   "name": "Quadro RTX 5000",
   "memory_used": "14029 MiB",
   "memory_total": "16384 MiB",
   "utilisation": "91 %"
  }
 }
};
