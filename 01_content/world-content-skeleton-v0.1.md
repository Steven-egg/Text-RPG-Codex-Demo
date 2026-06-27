# World Content Skeleton v0.1

Purpose: Hot Zone content skeleton for future formal-version expansion. This file
captures the current macro structure only. It does not approve runtime, data,
schema, save, GUI, bridge, combat, class, relic, or asset-pipeline work.

## Core Decision

Element Maze uses four core content elements:

| Element | Map Mood | Notes |
|---|---|---|
| Fire | Ash, scorched stone, lava seams, sealed furnace ruins | Current demo fire route is already represented by the existing Border Town path. |
| Ice | Frost-tide coast, cold sea, broken ice, fog harbor, salt-frost lighthouse | Not just glacier; it should feel coastal, wet, and distant. |
| Earth | Forest ring, root network, old quarry, fungal caverns, leyline stone | Nature is folded into Earth: roots, poison, moss, stone, and ancient growth. |
| Thunder | Storm plateau, sky roads, floating stone, conductive channels, lightning towers | Water can appear as conductive terrain, but Thunder remains the core identity. |

The final map is not a fifth core element. It is a composite endgame zone that
tests and echoes the four elements.

## Current Runtime Interpretation

In the stable CLI skeleton (established in early integration phases), the Ice,
Earth, Thunder, and Final playable scaffolds have landed as traversal and
progression scaffolds, display naming is complete through Final, and Relic v1
has landed as a four-element seal enshrinement flow.
This means the required quest, dungeon, boss, ending, elemental seal placement,
and Final-gate flow can be exercised in the CLI, but it does not mean regional
content, encounter texture, reward balance, dialogue, map routing, town hub
presentation, or final polish are complete.

Relic v1 is a progression and Final-gating layer only. Fire, Ice, Earth, and
Thunder have true seal key items and enshrined flags. Final unlock now depends
on all four enshrined elemental seals. Relic v1 does not add active effects,
passive effects, stat bonuses, resistance, skill links, or combat behavior.

Future work should peel these layers deliberately, starting from the smallest
approved slice and keeping runtime, data, schema, save, combat, GUI bridge, and
asset-pipeline changes behind the matching read-only planning gate.

## Detailed Content Baselines

To control startup reading bulk for the Hot Zone, the detailed specifications for job identities, promotions, quests, dungeons, hunts, reputation, reuse rules, relics, shops, magic shops, synthesis, equipment, and fire-route decisions have been moved to:

- [world-content-baselines-v0.1.md](world-content-baselines-v0.1.md)

These baselines are for planning only and do not constitute implementation approval.

---

## Regional Map Plan

| Region | Town Count | Dungeon Count | Current Decision |
|---|---:|---:|---|
| Border / Fire demo route | 1 | Existing demo dungeons | Use the existing Border Town only. Do not add an Ash Outpost. |
| Ice region | 1 | 3 | One regional town, two minor dungeons, one main two-phase dungeon. |
| Earth region | 1 | 3 | One regional town, two minor dungeons, one main two-phase dungeon. |
| Thunder region | 1 | 3 | One regional town, two minor dungeons, one main two-phase dungeon. |
| Final region | 1 | 3 | One front-line camp, two minor dungeons, one final main three-phase dungeon. |

Detailed region-level data template planning lives in:

- `01_content/blueprints/regional-data-template-v0.1.md`

That Task Zone file defines reusable data slots, ID naming rules, region hub
presentation boundaries, material timing, quest turn-in safety, Synthesis /
Workshop timing, and Antigravity candidate-content handoff. This Hot Zone file
keeps only the macro content skeleton.

---

## Boundaries

This document is a planning index, not implementation approval.

Do not infer approval for:

- new runtime data entries
- schema changes
- save migration or manual `save.json` work
- combat formula changes
- new GUI screens or bridge behavior
- formal class transfer, relic effects, or endgame systems
- asset generation or a formal asset pipeline

Before implementing any part of this skeleton, start with the smallest matching
read-only planning gate and name the exact files to be touched.
