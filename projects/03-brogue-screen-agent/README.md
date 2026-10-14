# 03 — Brogue, through the screen and the keyboard

[Brogue CE](https://github.com/tmewett/BrogueCE) is a real desktop roguelike: a
1.7 MB download from its release page, an SDL window, no API of any kind. This
agent plays it the way a person with a screen recorder and a keyboard would.

| | |
|---|---|
| **Input** | screenshots of the game window |
| **Output** | keystrokes posted to that window |
| **Game** | an unmodified `brogue.exe`, downloaded, not rebuilt |
| **Determinism** | `-s <seed>` fixes the dungeon, so two agents get the same ones |

Nothing is hooked, injected or patched. `brogueagent/window.py` starts the
process, finds its window with `EnumWindows`, captures the client area, and
delivers keys with **`PostMessage` to the window handle** rather than
`SendInput` — so the keystrokes go to the game whether or not it has focus, and
never into whatever else is open on the machine.

## Reading the screen

Brogue draws a 100 × 34 character grid. Everything below follows from one fact
that took four attempts to see: **the grid is stretched over the whole client
area and the fit is not integral at any font size**. At `--size 4` the window is
908 × 567, so a cell is 9.08 × 16.68 pixels and the boundaries drift eight pixels
across the screen.

Assuming a 9 × 16 lattice instead produces symptoms that point nowhere near the
cause:

- the decoder finds **1,924 distinct glyph shapes** in a font with about ninety,
  because every cell is sliced in a slightly different place;
- aligning that lattice by looking for quiet seams wanders by up to 18 pixels
  between frames — most of a Brogue screen is black, so nearly every offset
  looks quiet;
- aligning it by *repetition* instead (the right grid draws the same floor glyph
  hundreds of times) is stable horizontally and still ambiguous vertically,
  because the font does not fill its cell.

Cutting on the rounded fractional boundaries and resampling each cell into one
canonical box collapses that to **233 prototypes, of which 121 cover 96% of the
cells on screen**. Matching is colour-blind and polarity-blind, because Brogue
paints the same glyph in a dozen colours and inverts it on lit tiles; only the
shape is stable.

Glyphs are labelled once, by hand, from the contact sheet `build_atlas.py`
writes — about twenty terrain glyphs, which is what a policy navigates on. In
play the agent names **77–94% of the lit cells** in the dungeon view; the rest
decode as `?`, which the policy reads as "something is there" and treats as an
obstacle, so an unlabelled monster is still an obstacle it will not walk through.

The honest limit: this decodes **terrain**, not prose. An earlier attempt to
label every glyph from Brogue's own fixed strings — aligning them by word-length
pattern, so the labelling needs no labels to bootstrap — got the sentences nearly
right ("Hello and welcome, adventurer, to the Dungeons of Doom!") but smeared
votes across neighbouring letters, and is left in `auto_label.py` unfinished
rather than dressed up. Health is therefore read from the **colour of the health
bar**, not from text: an exact measurement that needs no character recognition.

## Result

Four seeded dungeons per agent, 220 keystrokes each. Descents are counted from
the screen — a new level is almost entirely unexplored, so the number of
non-blank map cells collapses when the agent takes a staircase.

*(filled from `runs/play.json`)*

| agent | descents | map cells named | health at end |
|---|---:|---:|---:|
| random keys | | | |
| explorer | | | |

## Files

```
capture_frames.py        record real frames, so decoding can be tuned offline
build_atlas.py           cluster cells into prototypes, write the labelling sheet
auto_label.py            label from Brogue's own strings -- partial, see above
decode_check.py          decode frames and look for strings Brogue always draws
play.py                  play seeded games; reads brogue.exe --scores afterwards
brogueagent/window.py    launch, capture, PostMessage keys
brogueagent/screen.py    fractional cells, prototypes, the grid -> characters
brogueagent/agent.py     the policy, and the health bar
brogueagent/labels.json  prototype index -> character, hand written
```

## Running it

```bash
python ../../scripts/get_brogue.py      # downloads Brogue CE from its releases
python capture_frames.py --seeds 1 2 3 --frames 28
python build_atlas.py --threshold 0.85
python play.py --seeds 11 12 13 14 --steps 220 --agent both
```

A window opens and plays by itself; the keys go to that window only.
