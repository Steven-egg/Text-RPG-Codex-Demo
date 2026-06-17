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
| Final region | 1 | 3 | One front-line camp, two minor dungeons, one final main two-phase dungeon. |

## Regional Quest And Dungeon Baseline

Future Ice, Earth, Thunder, and Final regions use the same reusable content
shape: one regional town or front-line camp, two minor dungeons, and one main
two-phase dungeon.

Each region has five quest slots:

- Quest 1: minor dungeon A.
- Quest 2: minor dungeon B.
- Quest 3: main dungeon phase 1.
- Quest 4: main dungeon phase 2.
- Quest 5: return / resolution quest. In the Final region, this is the final
  boss defeat and main ending quest.

Baseline dungeon scale:

| Dungeon Slot | Exploration Turns | Normal Enemy Types | Boss Count |
|---|---:|---:|---:|
| Minor dungeon A | 15 | 4 | 1 |
| Minor dungeon B | 15 | 4 | 1 |
| Main dungeon phase 1 | 12 | 3 | 1 |
| Main dungeon phase 2 | 12 | 3 | 1 |

Per region baseline total: 54 exploration turns, 14 normal enemy types, and 4
bosses. Final region follows the same dungeon scale; its final phase boss is the
main ending boss.

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

## Regional Shop Baseline

Future regional towns extend the existing Shop / travel inventory pattern with
small local additions instead of new shop systems.

Each Ice, Earth, and Thunder regional town adds four Shop goods:

- One HP recovery consumable.
- One MP recovery consumable.
- One local resistance accessory.
- One battle item.

The Final front-line camp adds three high-end supplies:

- One high-end HP recovery consumable.
- One high-end MP recovery consumable.
- One high-end combined HP / MP / abnormal-status recovery consumable.

Exact item names, numbers, prices, effects, and unlock timing are intentionally
left for later data planning.

## Regional Equipment And Upgrade Baseline

Future regional towns extend the existing weapon / armor shop and Workshop
patterns with fixed equipment slots instead of new equipment systems.

Each Ice, Earth, Thunder, and Final town adds seven equipment entries:

- Four job weapons, one for each current job.
- Two shared armor pieces.
- One role-leaning armor piece.

Resistance accessories from the Shop baseline are counted as Shop / travel
goods, not as weapon / armor shop equipment.

Upgrade targets stay limited so equipment data does not expand too quickly:

- Ice, Earth, and Thunder each select four upgrade targets: two job weapons, one
  shared armor piece, and one role-leaning armor piece.
- Final may select six upgrade targets as endgame loadout consolidation: four
  final job weapons and two final shared armor pieces.

Rogue pseudo-offhand equipment keeps the current data shape: it remains
head-slot, role-leaning armor unless a later exact-scope runtime / schema /
state / UI plan explicitly opens a real offhand slot. If a regional
role-leaning armor item is a Rogue head-slot pseudo-offhand item, it is
automatically eligible as that region's role-leaning armor upgrade target. This
keeps the Rogue identity without adding extra per-region equipment count.

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
