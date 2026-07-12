# Codex Handoff Short

Purpose: compact handoff for continuing Codex work. Keep current status here;
details belong to their owning SSOT.

## Current State

- Work directory: `C:\Users\User\OneDrive\文字冒險遊戲`
- Latest committed checkpoint:
  `45cbbad 2026-07-12 [codex] feat(combat): rework attributes and status effects`.
- The current combat-planning slice changes Cleric damage-over-time /
  regeneration durations from three to five turns and adds
  `06_tools/test_combat_balance.py` as a deterministic balance harness.
- The owner-approved player-side design is recorded at
  `01_content/combat-progression-design-v1.md`; it is planning only and does
  not authorize the future runtime/data/schema slices.
- Python CLI runtime remains gameplay authority.
- `07_gui_prototype/` remains the default static GUI surface.
- Facility CSS convergence and finalized GUI asset linking are landed.
- World Map now has Traditional Chinese player-facing presentation text and
  data-driven preview image paths for towns, normal dungeons, Main Dungeon
  phases, and static fixture fallback. Runtime IDs remain unchanged.

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
a read-only implementation gate for Combat Progression v1 slice 1: monster race
data/validation, separate status-damage handling, and Warrior Physical Charge.
Do not broaden that gate into equipment, relic, growth, monster balancing, GUI,
or save changes without another exact-scope approval.

Historical screen progress and verification are archived at:

`01_content/archive/gui-html-static-prototype-progress-v1.md`
