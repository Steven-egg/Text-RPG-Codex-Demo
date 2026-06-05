# Codex Handoff Short

Purpose: compact new-session handoff for Codex. Keep this file short. It should
tell a new session what is stable, what is forbidden, where details live, and
what the next boundary is. Detailed MVP verification belongs in Task Zone docs.

## Stable Baseline

- Work directory: `C:\Users\user\OneDrive\文字冒險遊戲`
- Current branch expectation: `main` aligned with `origin/main`.
- Latest committed bridge baseline:
  `709dc6c [antig] fix(gui): improve dungeon event scrolling and guild story progression hints`

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

- Scorched Mine Boss Glen Progression Deadlock Fix is complete:
  Scorched Mine 18/18 sets `boss_glen_sighted`; Guild can accept
  the investigation through `accept_boss_glen_investigation`, setting
  `boss_glen_investigation_accepted`; returning to Scorched Mine 18/18 then
  enables `challenge_boss` for Boss Glen.
- The intended flow is clue first, Guild acceptance second, formal Blood Map
  task third, Boss challenge fourth, Blood Map turn-in fifth, and Ash Ravine /
  Act 2 entry unlock through existing runtime progression.
- Owner manual hand test confirmed the Boss challenge deadlock is removed, Blood
  Map can be reported after defeating Glen, Ash Ravine can unlock and clear, and
  later CLI fire-demo progression can surface through the live bridge.
- Glen Boss flow UX cleanup is landed in `709dc6c`: the Guild story hint remains
  reviewable after accepting the investigation and after Glen is defeated, Blood
  Map reward unlock keys are mapped to player-facing labels, Dungeon Exploration
  keeps HP/MP in the resource strip while run Gold remains in current-run
  rewards, dungeon events scroll and auto-scroll to the newest event, and the
  action row supports stable Boss / leave button placement.
- Ash Ravine / Cinder Seal Depths GUI presentation cleanup is implemented in the
  current package: Guild story hints and Dungeon Exploration boss / narrative
  copy now lean on existing scout-report progression and avoid premature Boss /
  reward / unlock spoilers. Temple static fixture lore copy is also softened.
- Owner manual hand test confirmed the progression flow works through Ash Ravine
  first clear, scout turn-in, Ash Boss, supply-line upgrade, Cinder Depths
  unlock, Cinder scout / Boss path, and Temple / Church handoff.
- Known MVP observation: Ash Ravine and Cinder Seal Depths currently share some
  fire-demo materials, so a later scout turn-in can be ready immediately. Treat
  this as existing CLI MVP content/data reuse, not as presentation-cleanup drift.
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
- Temple and Relic Altar Live MVP is complete: Town Hub supports live routing to Temple and Relic Altar screens, which load runtime-shaped ScreenModels. Temple dispatches `temple_pray` (paying 30G for temporary blessing), `fire_mark_church_bridge` and `fire_mark_church_lookup` (inquiries updating runtime flags via game helpers when prerequisites are met), and previews promotions. Relic Altar previews registered relics (like ash charm) and requirements, allowing the `attune_relic` placeholder action.
- This does not open formal class transfer, class specialization gameplay, formal relic system, relic effects, equipping/obtaining relics, or manual `save.json` edits.

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

The Glen UX cleanup and the narrow Ash / Cinder GUI presentation cleanup are
complete in the current package. Remaining Boss / Act 2 observations are
coverage-oriented only; this does not approve Ash Guardian, Cinder Seal
Sentinel, generic Boss handling, full story hints, Temple / Relic gameplay, or
full Act 2 cleanup beyond the existing bridge presentation work.

Future Phase B candidate queue, second priority after the Phase A mainline
close:

1. Synthesis existing Mira recipes coverage.
2. Shop travel inventory coverage.
3. Magic Shop `MAGIC_BOOKS` coverage.
4. Workshop upgrade coverage.

Phase B work may be owner-tested in small batches after 2-3 narrow slices, but
each implementation slice still needs its own read-only planning gate and
owner-approved exact scope.

Future Phase C convenience queue is deferred:

1. Guild material sell.
2. Inventory / equipment management.
3. Storage capacity upgrade.
4. Bestiary detail / filtering.
5. Settings panel.

Any synthesis follow-up must not open full synthesis, base-item upgrades, recipe
/ quest / dungeon changes, schema changes, save changes, or crafting system
refactors without a new owner-approved exact scope.

Any Shop / Magic Shop / Workshop follow-up must stay within the approved
single-slice coverage target. Do not open full shop, full magic shop, generic
facility framework, generic equipment management, non-whitelisted upgrades, full
workshop, schema changes, save migration, combat formula changes, or manual
`save.json` work.

Any Phase C convenience follow-up must start with a later read-only gate and
explicit owner approval. Do not open storage capacity upgrades, generic
inventory / equipment management, settings, sell systems, bestiary detail
framework, schema changes, save migration, combat formula changes, or manual
`save.json` work from the current Phase B planning notes.

For docs-only sync, restrict changes to explicitly approved markdown surfaces and
do not touch runtime, JavaScript, data, schema, save, or combat formula.

## Verification Capsule

Latest stable verification noted here:

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
- Glen Boss flow UX cleanup Antigravity-reported checks:
  `python 06_tools/smoke_test_progression_bridge.py` PASS,
  `python element_maze.py --smoke-test` PASS, and
  `python 06_tools/validate_data.py` PASS.
- Ash / Cinder presentation cleanup owner manual hand test: Ash Ravine first
  clear shows a non-Boss terminal state, Guild scout turn-in updates guidance,
  Ash Boss opens and can be defeated, supply-line guidance appears, supply-line
  turn-in unlocks Cinder Depths, Cinder scout / Boss path completes, and the flow
  reaches the Temple / Church handoff. Existing shared fire-demo materials can
  make the next scout turn-in ready immediately; this is a known CLI MVP content
  reuse observation.

For future docs-only cleanup, use markdown diff/status checks. Runtime smoke is
not required unless runtime files change.
