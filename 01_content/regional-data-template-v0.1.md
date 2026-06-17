# Regional Data Template v0.1

Purpose: Task Zone template for turning the formal-version region skeleton into
future runtime data planning. This file defines reusable slots, naming rules,
material timing, and candidate-content handoff only. It does not approve
runtime, data, schema, save, GUI, bridge, combat, class, relic, or asset-pipeline
implementation.

Use this file after `01_content/world-content-skeleton-v0.1.md` when a task needs
region-level data planning detail.

## Region Hub Rule

Regional towns are presentation / context hubs, not formal runtime town
entities.

- Do not create a `town` data table or `town_id` requirement from this template.
- CLI may continue using a single town / facility menu shape.
- GUI may present each region hub with different title, background, NPC flavor,
  and facility copy.
- Regional identity should come from facility flavor, quest data, shop goods,
  recipes, magic books, equipment, and unlock context.

## Data ID Rule

Future formal data IDs should use:

```text
type_prefix + region_prefix + semantic_name
```

Examples:

- `dungeon_ice_*`
- `quest_thunder_*`
- `mat_earth_*`
- `mon_final_*`
- `boss_ice_*`
- `item_thunder_*`
- `acc_earth_*`
- `recipe_final_*`
- `book_ice_*`
- `skill_thunder_*`

This follows the current type-first style used by existing `dungeon_*`,
`quest_*`, `mat_*`, `recipe_*`, `book_*`, and related IDs.

Exact IDs are intentionally left for later data planning.

## Per-Region Slot Template

Ice, Earth, Thunder, and Final share the same region structure:

| Slot | Count / Shape |
|---|---|
| Region hub | 1 presentation / context hub |
| Dungeons | 2 minor dungeons + 1 two-phase main dungeon |
| Guild quests | 5 required quest slots |
| Normal enemy types | 14 per region |
| Bosses | 4 per region |
| Shop goods | 3 per region |
| Magic books | 6 per region |
| Synthesis recipes | 2 per Ice / Earth / Thunder, 4 for Final |
| Equipment entries | 7 per region |
| Upgrade targets | 4 per Ice / Earth / Thunder, 6 for Final |
| Optional elite hunt | 1 per elemental region after all four relics / seals |

Final follows the same slot structure, but its final main boss is the main
ending boss.

## Material Slot Template

Each region uses `6 + key + elite` material planning:

| Slot | Timing / Use |
|---|---|
| `region_common` | Region-wide common material, available early. |
| `early_local_a` | Minor dungeon A local material. |
| `early_local_b` | Minor dungeon B local material. |
| `main_local_1` | Main dungeon phase 1 local material. |
| `main_local_2` | Main dungeon phase 2 local material. |
| `refined_core` | Mid / late refined material for upgrades and stronger recipes. |
| `key_or_relic_shard` | Main-story key / relic shard style item. |
| `optional_elite_rare` | Optional elite rare material for Final-region synthesis. |

Normal enemies should share this material pool rather than each introducing a
unique material. Every normal enemy should have at least one material drop, but
multiple enemies may drop the same material.

Material buyback and economy values are intentionally left for later economy and
data planning.

## Quest Turn-In Safety Rule

Shared material pools must not allow quests to be completed before the target
dungeon is reached.

Every Guild quest turn-in must include at least one of these gates:

- A material that only appears in the target dungeon / phase.
- A clear flag.
- A boss flag.
- A required story flag.

Do not make a quest depend only on common materials that can be gathered earlier
than the quest's target dungeon.

## Synthesis Timing Rule

Regional Synthesis handles crafted countermeasures.

- Battle-item recipes should use early materials so the item can help during the
  region, not only after the region is nearly finished.
- Resistance-accessory upgrade recipes may use mid / late materials.
- Each synthesis recipe should require at least two material types.
- Optional elite rare materials are reserved for Final-region synthesis and
  should not be ordinary early-region recipe inputs.

Exact recipe outputs, material quantities, gold costs, unlock keys, and effects
are intentionally left for later data planning.

## Workshop Timing Rule

Equipment progression uses new regional equipment plus selected upgrades.

- Each region still introduces new equipment as the baseline stage upgrade.
- Workshop upgrades are optional investment paths, not a replacement for new
  regional shop equipment.
- Ice, Earth, and Thunder each split four upgrade targets into two early upgrades
  and two late upgrades.
- Early upgrades should use `region_common`, `early_local_a`, or
  `early_local_b`.
- Late upgrades should use `main_local_1`, `main_local_2`, or `refined_core`.
- Final may use six upgrade targets as endgame loadout consolidation.

This keeps the new-region shop relevant while still giving Workshop meaningful
early and late-region roles.

## Candidate Content Handoff

Antigravity may be used for candidate content generation only.

For each planned slot, Antigravity may provide three candidates for:

- Region hub names and short flavor.
- Dungeon names and short descriptions.
- Boss and monster names.
- NPC names and facility flavor lines.
- Item, equipment, material, recipe, magic book, and skill names.
- Short quest summaries and local mood copy.

Antigravity must not produce final runtime data, registry wiring, schema
changes, validation edits, save changes, combat behavior, bridge behavior, or
GUI implementation from this template.

Final selection, data shaping, validation, and implementation require a later
exact-scope planning gate.

## Boundaries

This template is planning only.

Do not infer approval for:

- New runtime data entries.
- New schema or registry tables.
- `save.json` work.
- Combat formula or elemental weakness implementation.
- Town runtime state or multi-town CLI navigation.
- GUI bridge expansion.
- Final item names, prices, quantities, drop rates, unlock keys, or smoke tests.
