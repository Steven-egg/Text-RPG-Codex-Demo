# World Content Baselines v0.1

Purpose: Detailed content baseline specifications moved from the Hot Zone content skeleton to control startup reading bulk.
This document is for planning only; it does NOT represent implementation approval.
For the macro structure and core design, see [world-content-skeleton-v0.1.md](world-content-skeleton-v0.1.md).

> [!IMPORTANT]
> The specifications in this document are planning baselines only. They do not approve any runtime, data, schema, save, GUI, bridge, combat, class, relic, or asset-pipeline implementation.

---

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

---

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

---

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

---

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

---

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

---

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
- Relic Preview: seal inspection / enshrinement surface. The landed relic
  passive choices use the existing Temple/state flow; broader relic systems
  remain deferred.

Town identity should mostly come from local data, presentation, and text, not
from creating new systems.

---

## Relic Baseline

Relic completion is not a pure key-item layer. The landed passive-choice system
is intentionally bounded; it does not authorize broader active relic systems.

Current landed interpretation: as of `43cfc67`, Relic v1 implements true Fire,
Ice, Earth, and Thunder seal key items, source-to-seal conversion, enshrined
flags, Final gating, and one selectable passive choice per enshrined relic. The
choice is saved through the existing state flow and applied to its relevant
stat or combat path.

For Fire, Ice, Earth, and Thunder, each completed relic is planned as:

- A main-story key for next-region access and Final-region gating.
- A region-completion marker.
- A facility-unlock container for later local Shop, Magic Shop, Synthesis,
  Workshop, Temple, or guidance unlock timing.

Additional relic systems are intentionally deferred to a later planning gate.
That gate must explicitly cover runtime, data, schema, save compatibility,
combat behavior, UI presentation, and smoke tests before adding any new active,
passive, stat, resistance, skill, or combat effect beyond the landed choices.

---

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

---

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

---

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

---

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

---

## Current Fire Route Decision

The fire demo route is considered structurally complete for macro-planning:

- Use the existing Border Town as the only fire-route town.
- Do not add a separate Ash Outpost.
- Existing fire-route dungeons cover the current demo path: Moss Cave, Scorched
  Mine, Ash Ravine, and Cinder Seal Depths.
- Future work may polish or extend exact approved surfaces, but this skeleton
  does not reopen fire-route runtime, GUI, or bridge implementation.
