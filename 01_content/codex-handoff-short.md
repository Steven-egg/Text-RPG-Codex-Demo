# Codex Handoff Short

Purpose: compact new-session handoff for Codex. Keep this file short. It should
tell a new session what is stable, what is forbidden, where details live, and
what the next boundary is. Detailed MVP verification belongs in Task Zone docs.

## Stable Baseline

- Work directory: `C:\Users\user\OneDrive\文字冒險遊戲`
- Current branch expectation: `main` aligned with `origin/main`.
- Latest committed bridge baseline:
  `b046b1e [antig] feat(gui): add Mira synthesis entry unlock bridge`
- Current working-tree live slice: Synthesis Single Recipe Craft Live MVP
  (`recipe_piercing_bundle`), pending commit.

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
- Town Hub Mira / 米菈合成屋 Entry Unlock Live MVP is complete in the working
  tree: the Town Hub synthesis node reflects
  `is_unlocked(state, "shop_synthesis_01")` as locked / unlocked.
- Locked 米菈合成屋 points the player to finish the Guild task `洞窟採集`; unlocked
  米菈合成屋 routes to the existing static synthesis screen.
- Synthesis Single Recipe Craft Live MVP is complete in the working tree:
  `synthesis_screen` live mode loads a runtime-shaped ScreenModel and dispatches
  `craft_recipe` for the single whitelisted recipe `recipe_piercing_bundle`.
- Crafting reuses Python runtime authority:
  `game.recipe_available(...)` and `game.craft_recipe_message(...)`.
- This does not mean full inventory / equipment, synthesis, crafting, guild
  quest, multi-recipe, base-item upgrade, or facility systems are complete.

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

The current recorded follow-up candidate is a read-only gate for broader
synthesis coverage, such as deciding whether to iterate more existing Mira
recipe ids. It is not approved for implementation yet.

Any synthesis follow-up must not open full synthesis, a generic recipe bridge,
broad `craft_recipe` coverage, base-item upgrades, recipe / quest / dungeon
changes, schema changes, save changes, or crafting system refactors without a
new owner-approved exact scope.

For docs-only sync, restrict changes to explicitly approved markdown surfaces and
do not touch runtime, JavaScript, data, schema, save, or combat formula.

## Verification Capsule

Latest stable / working-tree verification noted here:

- `06_tools/validate_data.py`: PASS
- `element_maze.py --smoke-test`: PASS
- Workshop bridge smoke: PASS
- Workshop Weapon Equip owner-side manual smoke: purchase does not auto-equip,
  equip does not deduct Gold, old weapon returns to inventory, new weapon becomes
  `equipment.weapon`, and World Map save / reload preserves equipment state.
- Town Hub Mira / 米菈合成屋 Entry Unlock Antigravity-reported checks:
  `element_maze.py --smoke-test` PASS, `06_tools/validate_data.py` PASS, scratch
  `test_synthesis.py` PASS.
- Synthesis Single Recipe Craft Antigravity-reported checks:
  `node --check 07_gui_prototype/synthesis_screen/synthesis-screen.js` PASS,
  `python 06_tools/smoke_test_synthesis_bridge.py` PASS,
  `python 06_tools/validate_data.py` PASS, and
  `python element_maze.py --smoke-test` PASS.
- Owner manual hand test: not run by request.

For future docs-only cleanup, use markdown diff/status checks. Runtime smoke is
not required unless runtime files change.
