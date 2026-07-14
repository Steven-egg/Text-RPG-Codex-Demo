# Codex Handoff Short

Purpose: compact handoff for continuing Codex work. Keep current status here;
details belong to their owning SSOT.

## Current State

- Work directory: `C:\Users\User\OneDrive\文字冒險遊戲`
- Latest committed checkpoint:
  `6b75e38 2026-07-12 [codex] feat(combat): add progression balance harness`.
- The working tree contains the owner-verified Combat Progression v1 Slice 1
  implementation: mandatory monster races, race-aware Bleed / Poison,
  defense-bypassing physical status damage, and Swordfighter Physical Charge.
- The same uncommitted slice fixes the live GUI combat bridge so DoT damage
  reduces enemy HP, produces readable localized battle-log rows, and resolves
  victory when DoT defeats an enemy. Focused bridge regression coverage is in
  `06_tools/smoke_test_combat_bridge.py`; foundation coverage is in
  `06_tools/test_combat_progression_foundation.py`.
- Owner manual verification passed for Physical Charge, race immunity, and
  GUI live DoT logging. Automated verification passed: data validation,
  combat foundation checks, combat bridge smoke, and CLI smoke test.
- The owner-approved player-side design is recorded at
  `01_content/combat-progression-design-v1.md`; it is planning only and does
  not authorize the future runtime/data/schema slices.
- Python CLI runtime remains gameplay authority.
- `07_gui_prototype/` remains the default static GUI surface.
- Facility CSS convergence and finalized GUI asset linking are landed.
- World Map now has Traditional Chinese player-facing presentation text and
  data-driven preview image paths for towns, normal dungeons, Main Dungeon
  phases, and static fixture fallback. Runtime IDs remain unchanged.
- The uncommitted Combat Progression v1 player-content work also includes the
  smallest Slice 2 Cleric change: Ice / Earth / Thunder / Final Cleric weapons
  now use mixed attack and magic-attack stats (8/22, 12/30, 16/40, 24/60).
- The uncommitted Rogue Ice pseudo-offhand slice makes the existing
  `armor_rogue_sleeve_blade` normal-attack follow-up data-driven and adds
  `armor_ice_rogue_sleeve_blade` (霜痕袖刃): head-slot Rogue equipment with a
  0.35x follow-up and a 30% Bleed attempt. Data validation, foundation,
  balance harness, CLI smoke, combat bridge, regional facility visibility, and
  magic-shop bridge smoke all passed.
- The next planned gate is Relic Passive v1. Its spec now locks one free-choice
  selection per enshrined relic, direct/DoT terminology, the four thematic
  roles, and the revised +8% / +15% / +20% / +5% values in
  `01_content/combat-progression-design-v1.md`. It remains unimplemented.

## Minimum Read List

1. `AGENTS.md`
2. `01_content/agent-startup-reading-list.md`
3. `.codex/skills/element-maze-session-ops/SKILL.md`
4. `README.md`
5. `01_content/codex-handoff-short.md`
6. `01_content/world-content-skeleton-v0.1.md`

For combat, equipment, relic, growth, or monster-balance work, also read:

- `01_content/combat-progression-design-v1.md`

For static GUI work, also read:

- `.codex/skills/element-maze-gui-static-prototype/SKILL.md`
- `01_content/gui-static-current-state-v1.md`
- only the relevant `07_gui_prototype/<screen>/` files

For runtime-connected GUI work, first read:

- `01_content/gui-runtime-bridge-plan-v1.md`

Then stop at a read-only planning gate.

## Boundaries

- Do not manually read or edit `save.json`.
- Do not modify runtime, data, schema, save, combat formulas, or gameplay
  authority from a static GUI task.
- Do not connect the Python runtime for static prototype work.
- Do not treat fixtures as gameplay SSOT.
- Do not start a formal asset pipeline.
- Do not stage, commit, push, create branches, or archive files unless explicitly
  requested.

## Next Boundary

No implementation target is pre-approved. The smallest next convergence item is
a read-only implementation gate for Relic Passive v1: declarative choice data,
durable `relic_choices` compatibility defaults, existing Temple/relic selection
and free-respec flow, stat/combat integration, and the narrow live relic-preview
bridge surface. Do not implement until the owner approves that exact surface.
Do not broaden it into monster balancing, growth, equipment expansion, battle
items, generic damage reduction, static GUI expansion, or manual save work.

Historical screen progress and verification are archived at:

`01_content/archive/gui-html-static-prototype-progress-v1.md`
