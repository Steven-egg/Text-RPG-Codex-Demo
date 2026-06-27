# Facility NPC Display Baseline v0.1

Purpose: define the display-name baseline for facility presenters before future
regional NPC generation. This is a Task Zone planning document. It does not
approve runtime, data, schema, save, GUI, bridge, combat, or asset-pipeline
implementation.

Use this file with:

- `01_content/codex-antigravity-collaboration-workflow-v0.1.md`
- `01_content/antigravity-candidate-content-brief-v0.1.md`
- `01_content/world-content-skeleton-v0.1.md`

## Authority Rule

NPC display names are player-facing presentation, not gameplay authority.

Authority order for NPC display naming:

1. Owner-approved GUI portrait and dialogue name.
2. Stable GUI ScreenModel or fixture presenter.
3. Runtime / CLI feedback speaker.
4. Older design docs and legacy CLI names.
5. Antigravity candidate names.

If GUI display identity and early CLI naming conflict, prefer the GUI display
identity for future presentation planning. Keep the older CLI name as
`legacy_name` until a later exact-scope sync task updates implementation.

Do not change `facility_id` from this document. Facility IDs remain system
anchors, while NPC names are display presentation.

## Baseline Table

| Facility | Facility ID | Display canon | Legacy / support names | Status | Notes |
|---|---|---|---|---|---|
| Adventurer Guild | `guild` | 莉娜 | 諾亞 | split presenter / senior liaison | 莉娜 is the GUI board presenter. 諾亞 remains a guild senior / story liaison and existing quest-giver legacy name. |
| Inn | `inn` | 莉莉 | Lily | stable | GUI and fixture identity are aligned. |
| Travel Shop | `travel_shop` | 特里 | 拉比 | stable with legacy drift | 特里 is the shop presenter. 拉比 is older shop-related CLI / design wording and should not guide new regional NPC names. |
| Workshop | `workshop` | 葛雷 / 布琳 | Grey / Bryn | dual presenter | Workshop may use two presenters: 葛雷 for weapons / offensive upgrades, 布琳 for armor / defensive upgrades. |
| Synthesis | `synthesis` | 米菈 | 米拉 / Mira | stable spelling baseline | Use 米菈 as the Chinese display spelling. |
| Magic Shop | `magic_shop` | 伊芙 | Eve | stable | Magic Shop presenter and magic-book guide. |
| Temple | `temple` | 艾莉希亞 | 賽恩 | owner-approved GUI canon, legacy drift | 艾莉希亞 is the future display canon. 賽恩 is an early CLI / runtime legacy name until a later sync task. |
| Storage | `storage` | 諾亞 | Noah | guild-linked utility presenter | Treat 諾亞 as a Guild storage liaison, not a separate storage-only character archetype. |
| Relic Preview | `relic_preview` | none | none | facility voice | Use facility voice, record text, altar echo, or preview copy. Do not add a named NPC by default. |

## Facility Role Boundaries

Guild:

- Allowed: local quests, quest reports, guild guidance, guild recognition text.
- Do not imply: recruitable party members, new exploration systems, or new
  guild-management mechanics.

Inn:

- Allowed: rest, local flavor, rumors, town atmosphere.
- Do not imply: quest unlocks, dungeon unlocks, hot-spring buffs, frostbite
  curing, or new rest bonus systems.

Travel Shop:

- Allowed: consumables, basic countermeasures, local supply flavor.
- Do not imply: new sell systems, price formulas, formal item IDs, or
  per-region shop mechanics beyond the approved shop slot plan.

Workshop:

- Allowed: weapons, armor, upgrades, material-flavor explanations.
- Do not imply: new equipment slots, salvage minigames, repair durability, or
  offhand systems.

Synthesis:

- Allowed: battle-item and resistance-countermeasure recipe flavor.
- Do not imply: final recipes, prices, quantities, effects, or formula changes.

Magic Shop:

- Allowed: element-relevant books, study flavor, school / tome atmosphere.
- Do not imply: skill formulas, MP costs, final book IDs, or class-system
  changes.

Temple:

- Allowed: seal lore, class / promotion preview, faith and regional-history
  flavor.
- Do not imply: relic active effects, passive effects, stat bonuses,
  resistance bonuses, skill links, or formal unlock keys.

Storage:

- Allowed: shared utility, storage availability flavor, guild-linked handling.
- Do not imply: capacity upgrades, new storage tiers, or independent storage
  economy.

Relic Preview:

- Allowed: preview-only relic / seal copy, record text, altar echo, marker
  display language.
- Do not imply: player obtains a relic, relic effects are active, or a named
  NPC controls relic progression.

## Regional NPC Generation Rule

Antigravity should not invent facility roles from character concepts first.
Generate regional NPCs from facility anchors.

For each regional candidate NPC, require:

```text
npc_slot:
  facility_anchor:
  base_display_canon:
  regional_local_face:
  name_candidate:
  allowed_dialogue_scope:
  must_not_imply:
  relationship_to_existing_presenter:
  risks:
```

Regional local faces may be:

- a local representative of the same facility family;
- a temporary contact who reports through the facility;
- flavor-only local staff who do not add new services.

Regional local faces must not replace demo display canon unless the owner
explicitly approves a future region-specific presentation plan.

## Current Naming Decisions

- Temple display canon is `艾莉希亞`.
- `賽恩` remains a legacy name until a later exact-scope sync task.
- Synthesis Chinese display spelling is `米菈`.
- Relic Preview has no named NPC by default.

## Future Sync Boundary

This document only defines display baseline and generation guidance.

Later CLI / GUI / runtime synchronization requires a read-only implementation
gate that names exact files and checks. Likely surfaces include GUI fixtures,
ScreenModel presenters, CLI narrative speakers, quest giver text, and feedback
messages.

Do not start that synchronization from this document alone.
