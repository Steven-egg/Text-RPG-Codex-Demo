# Codex Handoff Short

Purpose: compact new-session handoff for Codex. Keep this file short. It should
tell a new session what is stable, what is forbidden, where details live, and
what the next boundary is. Detailed MVP verification belongs in Task Zone docs.

## Stable Baseline

- Work directory: `C:\Users\user\OneDrive\文字冒險遊戲`
- Current branch expectation: `main` aligned with `origin/main`.
- Latest committed bridge baseline before the current working-tree package:
  `9ae502b [antig] fix(gui): repair Boss Glen progression bridge`
- Current working-tree live slice: Glen Boss flow UX cleanup and dungeon text presentation.

Project state:

- Python CLI runtime remains the playable game and gameplay authority.
- Act 1 is playable; Act 2 fire demo runtime content has landed through the fire
  shard / guild inquiry / church lookup closure.
- GUI static prototype exists under `07_gui_prototype/` and remains static by
  default.
- A local runtime-connected GUI bridge exists only for explicitly approved
  blessed slices.
- Element Maze is an expandable playable demo, not a closed demo. Narrow slice /
  MVP language controls current-round risk; it does not close future extension
  points.

Current newest GUI live state:

- Scorched Mine Boss Glen Progression Deadlock Fix is complete in the current
  working tree: Scorched Mine 18/18 sets `boss_glen_sighted`; Guild can accept
  the investigation through `accept_boss_glen_investigation`, setting
  `boss_glen_investigation_accepted`; returning to Scorched Mine 18/18 then
  enables `challenge_boss` for Boss Glen.
- The intended flow is clue first, Guild acceptance second, formal Blood Map
  task third, Boss challenge fourth, Blood Map turn-in fifth, and Ash Ravine /
  Act 2 entry unlock through existing runtime progression.
- Owner manual hand test confirmed the Boss challenge deadlock is removed, Blood
  Map can be reported after defeating Glen, Ash Ravine can unlock and clear, and
  later CLI fire-demo progression can surface through the live bridge.
- Known follow-up observations are player-facing UX / wording cleanup only:
  after accepting the investigation the Guild main-story area says no current
  clue, quest rewards expose internal keys such as `second_act_preview`,
  `unlock_act_2`, and `unlock_ash_ravine`, Dungeon Exploration bottom button
  layout should be checked if more Boss challenge buttons appear, and Ash Ravine
  / later fire-shard prompts may need less open-ended wording.
- Treat Ash Ravine and later cave / fire-shard visibility as coverage
  observation from existing CLI runtime progression, not as scope drift or an
  approval for full Act 2 cleanup.
- Storage Deposit & Withdraw Live MVP is complete in the current package: Town Hub can route to the Storage live screen, `storage_screen_model(state)` renders live storage state, `unlock_storage` can unlock the storage through Python runtime state, and `deposit_item` / `withdraw_item` allow transferring items.
- The validated path is: low Gold blocks unlock, sufficient Gold deducts the existing runtime storage unlock cost, sets `state["storage_unlocked"] = True`, and returns an updated Storage ScreenModel showing inventory, storage status, storage contents, and capacity.
- `deposit_item` and `withdraw_item` successfully transfer items between player inventory and storage while enforcing capacity limits.
- Storage capacity upgrades remain disabled in this slice with MVP-scope messaging.
- Guild Quest Turn-in for Synthesis Unlock Live MVP is complete: Guild live mode
  shows unlocked existing `QUESTS`, and `submit_quest` can complete ready quest
  turn-ins through existing runtime validation and reward / unlock behavior.
- The validated path is `quest_cave_gathering`: turn in `mat_moss_fiber x3` and
  `mat_cracked_stone x2`, receive the existing quest reward, and unlock
  `shop_synthesis_01`.
- Dungeon clear report semantics remain separate: first-clear rewards still
  happen at route clear, and later Guild report registration only records /
  displays report status.
- Workshop Armor Buy, Equip & Limited Upgrade Live MVP is complete: Workshop can buy existing weapon-shop weapons and armor-shop armor, equip weapons and owned non-weapon equipment through approved bridge actions, and upgrade whitelisted recipes (`recipe_iron_sword_plus_1`, `recipe_leather_armor_plus_1`). Buying does not auto-equip.
- Town Hub Mira / 米菈合成屋 Entry Unlock Live MVP is complete: the Town Hub
  synthesis node reflects
  `is_unlocked(state, "shop_synthesis_01")` as locked / unlocked.
- Locked 米菈合成屋 points the player to finish the Guild task `洞窟採集`; unlocked
  米菈合成屋 routes to the existing static synthesis screen.
- Synthesis Single Recipe Craft Live MVP is complete:
  `synthesis_screen` live mode loads a runtime-shaped ScreenModel and dispatches
  `craft_recipe` for the single whitelisted recipe `recipe_piercing_bundle`.
- Crafting reuses Python runtime authority:
  `game.recipe_available(...)` and `game.craft_recipe_message(...)`.
- This does not mean full inventory / equipment, storage capacity upgrade,
  synthesis, crafting, guild quest, story hint, generic boss, full Act 2,
  multi-recipe, base-item upgrade, or facility systems are complete.

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

Interpretation rule: `Explicitly Not Open` means not approved in the current
slice. It is not a permanent ban or demo freeze. Future extension points may be
reopened through a read-only planning gate and owner-approved exact scope.

- Full inventory / equipment management.
- Accessory purchase, sell, generic unequip, comparison, non-whitelisted upgrade
  expansion, or generic workshop framework.
- Full shop, magic shop, storage capacity upgrade, synthesis, guild,
  quest, boss, dungeon, magic, skill, target-selection, or facility framework.
- New quest data, schema changes, broad quest framework changes, or story inquiry
  expansion beyond existing runtime `QUESTS` turn-in coverage.
- Save migration, data/schema changes, combat formula changes, stat rebalance, or
  manual `save.json` edits.
- Formal asset pipeline or reference/mockup images as runtime assets.
- Runtime or GUI feature implementation without a new owner-approved exact scope.

## Next-Step Boundary

No next implementation is pre-approved.

The current recorded Boss Glen follow-ups are coverage-oriented UX observations,
not approved implementation: post-investigation Guild guidance, player-facing
reward wording for unlock keys, Dungeon Exploration bottom button layout for
future Boss actions, and later Ash Ravine / fire-shard prompt wording.

Broader synthesis coverage remains a possible future read-only gate, such as
deciding whether to iterate more existing Mira recipe ids. It is not approved
for implementation yet.

Any synthesis follow-up must not open full synthesis, a generic recipe bridge,
broad `craft_recipe` coverage, base-item upgrades, recipe / quest / dungeon
changes, schema changes, save changes, or crafting system refactors without a
new owner-approved exact scope.

Any Storage / Workshop follow-up must start with a new read-only gate and
explicit owner approval. Do not open storage capacity upgrades, generic inventory
/ equipment management, non-whitelisted upgrades, full workshop, schema changes,
save migration, combat formula changes, or manual `save.json` work.

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
- Guild Quest Turn-in for Synthesis Unlock Antigravity-reported checks:
  `python 06_tools/smoke_test_guild_quest_bridge.py` PASS,
  `python 06_tools/validate_data.py` PASS,
  `python element_maze.py --smoke-test` PASS,
  `python 06_tools/smoke_test_synthesis_bridge.py` PASS,
  `python 06_tools/smoke_test_workshop_bridge.py` PASS, and
  `python 06_tools/smoke_test_magic_shop_bridge.py` PASS.
- Owner manual hand test: locked synthesis before quest completion, unlocked
  synthesis after Guild quest turn-in, save/load persistence for unlocked state,
  new-game locked state, and old completed save unlocked state all PASS.
- Storage Deposit & Withdraw / Workshop Armor & Upgrade Antigravity-reported
  checks: `git diff --check` PASS,
  `python 06_tools/smoke_test_storage_bridge.py` PASS,
  `python 06_tools/smoke_test_workshop_bridge.py` PASS,
  `python 06_tools/validate_data.py` PASS,
  `python element_maze.py --smoke-test` PASS,
  `node --check 07_gui_prototype/storage_screen/storage-screen.js` PASS, and
  `node --check 07_gui_prototype/workshop_screen/workshop-screen.js` PASS.
- Owner exploratory bridge-loop hand test: runtime can progress to 焦石礦坑,
  焦石礦坑 exploration report can complete and appears in Guild as completed,
  Mira synthesis unlock works, `recipe_piercing_bundle` can be crafted, and the
  crafted battle item can be used in combat. This is only supplementary
  verification for the Guild / Synthesis unlock loop; it does not open Boss,
  血跡地圖, more quests, more recipes, full synthesis, or a combat item system.

- Boss Glen progression owner manual hand test: first Scorched Mine 18/18 blocks
  direct Boss challenge and points back to Guild, Guild accepts the investigation,
  returning to 18/18 starts Boss Glen combat, Blood Map can be reported after
  victory, Ash Ravine unlocks and can clear, later Ash Ravine Boss / fire-shard
  visibility follows existing CLI runtime progression, and supply-line upgrade
  turn-in / medium potion unlock still works.

For future docs-only cleanup, use markdown diff/status checks. Runtime smoke is
not required unless runtime files change.
