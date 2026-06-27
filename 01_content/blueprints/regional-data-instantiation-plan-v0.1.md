# Regional Data Instantiation Plan v0.1

Purpose: planning bridge between the macro world skeleton and future formal
runtime data work. This file records the intended expansion order for Ice,
Earth, Thunder, and Final regional content. It does not approve runtime, data,
schema, save, combat, GUI, bridge, or asset-pipeline implementation.

Use this file after:

- `01_content/world-content-skeleton-v0.1.md`
- `01_content/blueprints/regional-data-template-v0.1.md`

## Core Approach

Use a hybrid instantiation route:

1. Define a data-ready region manifest first.
2. Instantiate future data in ordered layers.
3. Keep candidate naming, prose, art direction, and runtime implementation in
   separate later gates.

The region manifest should describe required slots and dependencies, not final
names, prices, quantities, effects, drop rates, formulas, or schema changes.

## Region Manifest Contract

Each future region manifest should reserve these planning slots:

- `region_id`
- `region_role`
- `element_identity`
- `hub_presentation`
- `dungeon_slots`
- `quest_slots`
- `progression_markers`
- `material_slots`
- `monster_slots`
- `boss_slots`
- `facility_slots`
- `shop_goods_slots`
- `magic_book_slots`
- `synthesis_recipe_slots`
- `equipment_slots`
- `workshop_upgrade_slots`
- `optional_elite_slot`
- `required_flags`
- `validation_notes`

Ice, Earth, and Thunder are future elemental expansion regions. Final is a
composite endgame region and should not be treated as a fifth core element.

## Fire Legacy Reference

The existing Fire / Border route is a read-only legacy reference, not the
standard pattern for future regions.

- Use the existing Border Town only.
- Do not add Ash Outpost as part of this plan.
- Existing fire-mark shards are demo-era relic clues / prologue evidence.
- Future Ice, Earth, and Thunder regions should not copy the shard collection
  and synthesis pattern.

Preferred future alignment path:

- A later Fire interpretation event may use the existing fire-mark shards as
  prerequisites to resolve the Fire relic marker.
- That event would align Fire with later full-seal regions at the progression
  layer.
- Whether the existing shards are preserved, converted, consumed, archived, or
  kept as memorabilia is deferred to a later exact-scope data / save planning
  gate.

## Relic And Marker Model

Use three separate layers so relic planning does not collapse into ordinary
item drops.

| Layer | Meaning | Notes |
|---|---|---|
| Relic / seal | Narrative concept: elemental acknowledgement, attunement, or region completion. | Not a normal reward item. |
| Relic marker | Progression / unlock state used by future gates. | Used for region completion, Final access, and facility unlock containers. |
| `relic_marker_source` | Optional proof object, echo, core remnant, or narrative carrier. | May support recovery from progression bugs, flavor display, sale value, or memorial use. |

For Ice, Earth, and Thunder, the relic marker should live in the progression /
unlock layer. It should not be treated as a quest reward, ordinary material, or
Boss drop.

Final should use analogous final resolution markers and ending flags rather
than a fifth elemental relic marker.

Relic effects are intentionally deferred until after class identity and
promotion planning. Active effects, passive effects, stat bonuses, resistance
effects, skill links, combat formulas, and UI presentation require a later
Relic effects planning gate.

## Relic Marker Source Rule

Each elemental region should reserve a `relic_marker_source` slot by default,
but it may be replaced by a story flag when a pure attunement event fits better.

Default interpretation:

1. The player defeats the main dungeon phase 2 Boss.
2. A post-Boss scene, seal seat, ancient core, or elemental source responds.
3. The region's relic marker is resolved in progression state.
4. A `relic_marker_source` may be granted, displayed, checked, or retained as
   proof, but it is not the relic itself.

Validation rule:

- Every regional relic marker must have at least one reliable source condition:
  Boss flag, clear flag, story flag, or marker source.
- A relic marker must not depend only on common materials that can be acquired
  before the intended story point.

## Layered Instantiation Order

Future data planning should instantiate layers in this order.

### 1. Region Manifest Layer

Create the data-ready manifest for each planned region:

- Fire read-only legacy reference.
- Ice expansion manifest.
- Earth expansion manifest.
- Thunder expansion manifest.
- Final composite endgame manifest.

### 2. Topology Layer

Define each region's structural graph:

- One hub or front-line camp presentation context.
- Two minor dungeons.
- One main dungeon split into phase 1 and phase 2.
- Five required Guild quest slots.

The Final region follows the same dungeon / quest shape, but its fifth quest is
the Demon King defeat and ending resolution.

### 3. Progression Marker Layer

Define what counts as completing each region before assigning materials or
drops.

Planning slots:

- Dungeon clear flags.
- Boss defeat flags.
- Required story flags.
- Region completion marker.
- Elemental relic marker for Fire, Ice, Earth, and Thunder.
- Final gate requirements.
- Final ending / resolution marker.

This layer comes before material planning so the relic marker is not mistaken
for a material, Boss drop, or quest turn-in reward.

### 4. Quest Objective Safety Layer

Define how each quest avoids early completion.

Every required Guild quest should use at least one target-safe condition:

- A material that only appears in the target dungeon or phase.
- A clear flag.
- A Boss flag.
- A required story flag.
- A resolved marker source where appropriate.

Do not let a quest depend only on region-common materials if those materials can
be collected before the target dungeon is reached.

### 5. Material Economy Layer

Use a revised material planning shape:

```text
6 + marker_source + elite
```

Default slots:

- `region_common`
- `early_local_a`
- `early_local_b`
- `main_local_1`
- `main_local_2`
- `refined_core`
- `relic_marker_source`
- `optional_elite_rare`

`relic_marker_source` replaces the old shard-oriented reading of
`key_or_relic_shard`. It is a proof / narrative carrier, not a standard shard
collection system.

Material and drop planning should serve quests, synthesis, Workshop upgrades,
and optional endgame preparation. It should not define what the relic marker is.

For Final, optional elite rare materials should primarily be interpreted as
inputs or sinks for Final-region synthesis supplied by elemental optional elite
hunts, unless a later plan explicitly opens a Final optional elite.

### 6. Encounter Layer

Define encounter slots after progression and material timing are clear.

Per Ice, Earth, Thunder, and Final region:

- 14 normal enemy types.
- 4 Bosses.
- Optional elite hunt only for elemental regions after all four elemental relic
  markers are complete.

Normal enemies should share the regional material pool. Every normal enemy
should have at least one material drop, but unique material per enemy is not the
default goal.

### 7. Facility Inventory Layer

Define facility content after the core route, flags, and materials are known.

Reusable facility families:

- Guild
- Inn
- Shop
- Workshop
- Synthesis
- Magic Shop
- Temple
- Storage
- Relic Preview

Per Ice, Earth, and Thunder:

- 3 Shop goods: HP item, MP item, local resistance accessory.
- 6 Magic Shop books: Mage 2, Cleric 2, Warrior 1, Rogue 1.
- 2 Synthesis recipes: battle item, resistance accessory upgrade.
- 7 equipment entries.
- 4 Workshop upgrade targets: 2 early and 2 late.

For Final:

- 3 high-end Shop goods.
- 6 Magic Shop books.
- 4 Synthesis recipes.
- 7 equipment entries.
- Up to 6 Workshop upgrade targets.

Exact names, numbers, prices, effects, unlock keys, and formulas remain for
later data planning.

### 8. Validation And Gate Layer

Before any future implementation, prepare a read-only runtime / data / schema
planning gate that names exact files and checks.

Planning checks should cover:

- ID prefix consistency.
- Quest turn-in safety.
- Boss / clear / story flag coverage.
- Relic marker source coverage.
- Drop coverage for normal enemies.
- Recipe material availability timing.
- Workshop early / late material timing.
- Optional elite unlock requirements.
- Final gate requirements.

Implementation remains closed until the owner approves an exact surface.

## Antigravity Boundary

Antigravity may later generate candidate content only. It may provide three
candidates per planned slot for names, short descriptions, NPC flavor, local
mood text, items, materials, recipes, books, monsters, bosses, hubs, and
dungeons.

Antigravity must not produce final runtime data, schema changes, registry
wiring, validation edits, save changes, combat behavior, bridge behavior, GUI
implementation, or asset-pipeline work from this plan.

The candidate-content brief should be a separate document.

## UI And Asset Boundary

This plan may inform future UI art preparation, but it does not open GUI static
prototype work, image generation, bridge expansion, or formal asset-pipeline
work.

Visual mood, screen image needs, and asset candidate planning should be handled
in a separate UI art preparation brief.

## Next Planning Documents

Recommended next documents, if approved later:

- `01_content/archive/antigravity-candidate-content-brief-v0.1.md`
- `01_content/archive/ui-art-prep-brief-v0.1.md`

Do not update existing Hot Zone files from this plan unless the owner approves
that exact docs surface.
