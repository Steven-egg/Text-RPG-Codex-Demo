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

As of `56731f1`, the Ice, Earth, Thunder, and Final CLI playable skeletons have
landed as traversal and progression scaffolds. This means the required quest,
dungeon, boss, and ending flow can be exercised in the CLI, but it does not mean
regional content, naming, encounter texture, reward balance, dialogue, or final
polish are complete.

Future work should peel these layers deliberately, starting from the smallest
approved slice and keeping runtime, data, schema, save, combat, GUI bridge, and
asset-pipeline changes behind the matching read-only planning gate.

## Job Identity Baseline

The four current jobs should differ by combat rhythm and problem-solving role,
not only by raw damage numbers.

| Job | Baseline Identity |
|---|---|
| Mage | Element counterplay and magic burst damage. Mage should feel strongest when exploiting elemental weakness, with MP pressure as the main limiter. |
| Warrior | Defense, reliable basic attacks, and a small set of physical skill damage boosts. Warrior should feel stable and durable rather than tricky. |
| Rogue | Physical offense, special-attack bonus damage, conditional spikes, and a small amount of status application through skills. Rogue should feel fast and opportunistic. |
| Cleric | Regeneration, recovery, protection, damage over time, and thrown / battle-item damage support. Cleric should win longer fights through sustain and pressure, not pure burst. |

Exact skill names, formulas, status chances, item-scaling rules, and combat
numbers are intentionally left for later combat / data planning.

## Promotion Baseline

Formal-version promotion planning starts with one promotion tier. Each current
base job has two promotion directions:

| Base Job | Direction A | Direction B |
|---|---|---|
| Mage | Element burst. | Magic control / multi-element response. |
| Warrior | Defense / guarding. | Basic attack / physical skill offense. |
| Rogue | Critical burst. | Status / special-attack interaction. |
| Cleric | Recovery / protection. | Damage over time / item support. |

Promotion implementation is intentionally undecided. This skeleton does not
choose whether promotions are expressed through stat growth changes, new skills,
skill replacement, passive title effects, equipment permissions, or mixed
mechanics. That decision requires a later read-only planning gate covering
runtime, data, schema, save compatibility, combat validation, and smoke tests.

## Regional Map Plan

| Region | Town Count | Dungeon Count | Current Decision |
|---|---:|---:|---|
| Border / Fire demo route | 1 | Existing demo dungeons | Use the existing Border Town only. Do not add an Ash Outpost. |
| Ice region | 1 | 3 | One regional town, two minor dungeons, one main two-phase dungeon. |
| Earth region | 1 | 3 | One regional town, two minor dungeons, one main two-phase dungeon. |
| Thunder region | 1 | 3 | One regional town, two minor dungeons, one main two-phase dungeon. |
| Final region | 1 | 3 | One front-line camp, two minor dungeons, one final main three-phase dungeon. |

Detailed region-level data template planning lives in:

- `01_content/regional-data-template-v0.1.md`

That Task Zone file defines reusable data slots, ID naming rules, region hub
presentation boundaries, material timing, quest turn-in safety, Synthesis /
Workshop timing, and Antigravity candidate-content handoff. This Hot Zone file
keeps only the macro content skeleton.

## Regional Quest And Dungeon Baseline

Ice, Earth, Thunder, and Final regions use the same reusable content shape: one
regional town or front-line camp, two minor dungeons, and one main dungeon. Ice,
Earth, and Thunder use two main phases by default; Final may use a longer
three-phase main dungeon for ending escalation.

Each region has five quest slots:

- Quest 1: minor dungeon A.
- Quest 2: minor dungeon B.
- Quest 3: main dungeon phase 1.
- Quest 4: main dungeon phase 2.
- Quest 5: return / resolution quest. In the Final region, this is the final
  boss defeat and main ending quest.

Regional Guild quest types stay templated:

| Quest Slot | Default Guild Quest Type |
|---|---|
| Quest 1 | Scout / first survey for minor dungeon A. |
| Quest 2 | Gathering / hunt task for minor dungeon B. |
| Quest 3 | Anomaly investigation / entrance unlock for main dungeon phase 1. |
| Quest 4 | Seal breach / boss hunt for main dungeon phase 2. |
| Quest 5 | Report / interpretation / next-region handoff. Final region uses this slot for the Demon King defeat and ending resolution. |

Exact NPCs, materials, rewards, dialogue, and quest text are intentionally left
for later data planning.

Baseline dungeon scale:

| Dungeon Slot | Exploration Turns | Normal Enemy Types | Boss Count |
|---|---:|---:|---:|
| Minor dungeon A | 15 | 4 | 1 |
| Minor dungeon B | 15 | 4 | 1 |
| Main dungeon phase 1 | 12 | 3 | 1 |
| Main dungeon phase 2 | 12 | 3 | 1 |

Per region baseline total for Ice, Earth, and Thunder: 54 exploration turns, 14
normal enemy types, and 4 bosses. Final region may exceed this baseline with an
ending escalation phase; the landed CLI skeleton uses a three-phase final main
dungeon whose final phase boss is the main ending boss.

## Optional Elite Hunt Baseline

Optional elite hunts are the default optional challenge layer. They are not part
of each region's five required quest slots.

After the four elemental relics / seals are completed, the Guild may publish one
optional elite hunt for each of the four elemental regions. Each hunt points to
one existing dungeon in that region and enables a low-rate optional elite
encounter there.

Elite hunt rewards stay bounded:

- The elite encounter drops a rare synthesis material intended for Final-region
  crafting.
- The rare synthesis material should be guaranteed after defeating the elite, so
  the player does not need to roll both encounter chance and drop chance.
- Guild turn-in rewards should focus on guild points / reputation.
- Gold rewards should stay small to moderate as supply compensation.
- EXP rewards should be absent or very small.
- Direct endgame equipment, relic effects, or overpowered rewards are not part
  of this baseline.

Final-region synthesis may later use these rare materials for endgame recipes.
Exact elite IDs, dungeons, encounter rates, material IDs, reward numbers, and
recipe outputs are intentionally left for later data planning.

## Guild Reputation Baseline

Guild points should be treated as cumulative reputation / rank progress, not as
a spendable currency. Main-story progression should not be hard-gated by guild
point totals.

Main-story progression should continue to use concrete progress keys:

- Completed required quests.
- Cleared required dungeons.
- Defeated required bosses.
- Completed elemental relics / seals.
- Required story flags.

Guild reputation is best used for optional and support-layer gates:

- Optional elite hunts.
- High-rank Guild requests.
- Advanced local facility availability, such as selected Shop, Magic Shop,
  Synthesis, Workshop, Temple, or guidance unlocks.
- Town / Guild recognition text.

Guild reputation gate implementation belongs to the progression / facility
unlock stage. It should be planned after relic key and region-completion flags
are defined, and before or alongside later promotion implementation and
elemental combat formula expansion. Exact ranks, thresholds, unlock keys,
screen presentation, validation, and smoke tests are intentionally left for that
later read-only planning gate.

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

## Relic Baseline

Relic completion should not be treated as a pure key item, but this skeleton
does not define active or passive relic effects yet.

For Fire, Ice, Earth, and Thunder, each completed relic is planned as:

- A main-story key for next-region access and Final-region gating.
- A region-completion marker.
- A facility-unlock container for later local Shop, Magic Shop, Synthesis,
  Workshop, Temple, or guidance unlock timing.

Concrete relic effects are intentionally deferred to a later Relic effects
planning gate. That gate must explicitly cover runtime, data, schema, save
compatibility, combat behavior, UI presentation, and smoke tests before any
active, passive, stat, resistance, skill, or combat effect is implemented.

## Regional Shop Baseline

Future regional towns extend the existing Shop / travel inventory pattern with
small local additions instead of new shop systems.

Each Ice, Earth, and Thunder regional town adds three Shop goods:

- One HP recovery consumable.
- One MP recovery consumable.
- One local resistance accessory.

The Final front-line camp adds three high-end supplies:

- One high-end HP recovery consumable.
- One high-end MP recovery consumable.
- One high-end combined HP / MP / abnormal-status recovery consumable.

Exact item names, numbers, prices, effects, and unlock timing are intentionally
left for later data planning.

## Regional Magic Shop Baseline

Future regional Magic Shops favor Mage and Cleric growth while still giving
Warrior and Rogue one local book each. Do not use cross-job tactical books as
the default expansion pattern.

Each Ice, Earth, Thunder, and Final town adds six magic books:

- Two Mage books.
- Two Cleric books.
- One Warrior book.
- One Rogue book.

Exact book names, skill effects, MP costs, prices, unlock timing, and combat
numbers are intentionally left for later data planning.

## Regional Synthesis Baseline

Future regional Synthesis additions handle battle-item crafting and resistance
accessory upgrades. This keeps Shop focused on consumables and base resistance
accessories while Synthesis handles crafted countermeasures.

Each Ice, Earth, and Thunder regional town adds two synthesis recipes:

- One local battle-item recipe.
- One local resistance-accessory upgrade recipe.

The Final front-line camp adds four synthesis recipes:

- One endgame battle-item recipe.
- One endgame resistance-accessory upgrade recipe.
- Two expensive attribute-boost recipes for endgame material and gold sinks.

Exact recipe names, materials, prices, output quantities, stat effects, and
unlock timing are intentionally left for later data planning.

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
