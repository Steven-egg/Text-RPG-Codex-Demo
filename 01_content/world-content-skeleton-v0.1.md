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

## Regional Map Plan

| Region | Town Count | Dungeon Count | Current Decision |
|---|---:|---:|---|
| Border / Fire demo route | 1 | Existing demo dungeons | Use the existing Border Town only. Do not add an Ash Outpost. |
| Ice region | 1 | 3 | One regional town, two minor dungeons, one main two-phase dungeon. |
| Earth region | 1 | 3 | One regional town, two minor dungeons, one main two-phase dungeon. |
| Thunder region | 1 | 3 | One regional town, two minor dungeons, one main two-phase dungeon. |
| Final region | 0-1 | 3-4 | Optional front-line camp, four-element echo dungeons, final seal core. |

## Reuse Rule

Regional towns reuse the existing facility families whenever possible:

- Guild: local quests, reports, and guidance.
- Inn: rest and local flavor.
- Shop: local consumables and basic countermeasures.
- Workshop: equipment and upgrades.
- Synthesis: element countermeasure recipes.
- Magic Shop: element-relevant books.
- Temple: seal / class / lore preview.
- Storage: shared utility.
- Relic Preview: preview only until formally reopened.

Town identity should mostly come from local data, presentation, and text, not
from creating new systems.

## Current Fire Route Decision

The fire demo route is considered structurally complete for macro-planning:

- Use the existing Border Town as the only fire-route town.
- Do not add a separate Ash Outpost.
- Existing fire-route dungeons cover the current demo path: Moss Cave, Scorched
  Mine, Ash Ravine, and Cinder Seal Depths.
- Future work may polish or extend exact approved surfaces, but this skeleton
  does not reopen fire-route runtime, GUI, or bridge implementation.

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
