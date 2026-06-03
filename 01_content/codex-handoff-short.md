# Codex Handoff Short

Purpose: compact new-session handoff for Codex. Keep this file short. It should
tell a new session what is stable, what is forbidden, where details live, and
what the next boundary is. Detailed MVP verification belongs in Task Zone docs.

## Stable Baseline

- Work directory: `C:\Users\user\OneDrive\文字冒險遊戲`
- Current branch expectation: `main` aligned with `origin/main`.
- Latest docs sync: `a20d912 [codex] docs(gui): sync workshop weapon equip bridge handoff`
- Latest feature commit: `6abe303 [antig] feat(gui): add workshop weapon equip bridge & align backpack presentation`
- Previous stable docs point: `3792099 docs(gui): sync workshop buy weapon bridge handoff`

Project state:

- Python CLI runtime remains the playable game and gameplay authority.
- Act 1 is playable; Act 2 fire demo runtime content has landed through the fire
  shard / guild inquiry / church lookup closure.
- GUI static prototype exists under `07_gui_prototype/` and remains static by
  default.
- A local runtime-connected GUI bridge exists only for explicitly approved
  blessed slices.

Current newest GUI live state:

- Workshop Buy Weapon Live MVP is complete: Workshop can buy existing weapon-shop
  weapons, and buying does not auto-equip.
- Workshop Weapon Equip Live MVP is complete: Workshop "owned equipment" can equip
  inventory-held weapon-slot items into `equipment.weapon`.
- `equip_weapon` validation and mutation happen Python server-side and reuse
  `game.equip_item(state, item_id, quiet=True)`.
- World Map / main inventory overlay presentation is aligned with inventory
  equipment plus currently equipped equipment.
- This does not mean the full inventory / equipment system is complete.

## Hot Zone Startup Order

Use the startup list as the source of truth. Minimum Codex startup read order:

1. `AGENTS.md`
2. `01_content/agent-startup-reading-list.md`
3. `.codex/skills/element-maze-session-ops/SKILL.md`
4. `README.md`
5. `01_content/codex-handoff-short.md`

Read Task Zone docs only when the current task needs them. Do not load Cold Zone
files during ordinary startup.

## Task Zone Routing

- GUI live bridge details and landed MVP status notes:
  `01_content/gui-runtime-bridge-plan-v1.md`
- GUI static prototype screen-level progress and verification:
  `01_content/gui-html-static-prototype-progress-v1.md`
- GUI planning / document lifecycle / archive candidate routing:
  `01_content/gui-planning-index.md`
- GUI runtime bridge approval route:
  read `01_content/gui-runtime-bridge-plan-v1.md` and stop at a read-only planning
  gate before implementation.
- GUI static prototype work:
  read `.codex/skills/element-maze-gui-static-prototype/SKILL.md` and the
  relevant `07_gui_prototype/<screen>/` files only.

## Explicitly Not Open

- Full inventory / equipment management.
- Armor, accessory, special-slot, unequip, comparison, upgrade expansion, or
  generic workshop framework.
- Full shop, magic shop, storage, synthesis, guild, quest, boss, dungeon, magic,
  skill, target-selection, or facility framework.
- Save migration, data/schema changes, combat formula changes, stat rebalance, or
  manual `save.json` edits.
- Formal asset pipeline or reference/mockup images as runtime assets.
- Runtime or GUI feature implementation without a new owner-approved exact scope.

## Next-Step Boundary

No next implementation is pre-approved.

The current recorded candidate is Combat / Field Item Use MVP: let already owned
consumables be used through existing runtime authority and return HP / MP /
inventory updates to the GUI live ScreenModel. This is only a candidate and still
requires a single-slice read-only planning gate.

For docs-only sync, restrict changes to explicitly approved markdown surfaces and
do not touch runtime, JavaScript, data, schema, save, or combat formula.

## Verification Capsule

Latest stable verification before this cleanup included:

- `06_tools/validate_data.py`: PASS
- `element_maze.py --smoke-test`: PASS
- Workshop bridge smoke: PASS
- Workshop Weapon Equip owner-side manual smoke: purchase does not auto-equip,
  equip does not deduct Gold, old weapon returns to inventory, new weapon becomes
  `equipment.weapon`, and World Map save / reload preserves equipment state.

For future docs-only cleanup, use markdown diff/status checks. Runtime smoke is
not required unless runtime files change.
