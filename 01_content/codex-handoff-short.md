# Codex Handoff Short

Purpose: compact new-session handoff for Codex. Keep this file short. It should
tell a new session what is stable, what is forbidden, where details live, and
what the next boundary is. Detailed MVP verification belongs in Task Zone docs.

## Stable Baseline

- Work directory: `C:\Users\user\OneDrive\文字冒險遊戲`
- Current branch expectation: `main` aligned with `origin/main`.
- Latest stable checkpoint:
  `c7729df [antig] fix(gui): normalize shop family layout`
- Latest committed bridge baseline:
  `2ecca91 [antig] feat(gui): add Guild material sell bridge and fix Shop layout`
- Basic facility CLI-parity bridge coverage is complete through the existing
  Guild material-buyback behavior.

- Maintainability Checkpoint:
  - Shared `resource_strip` has been moved to `gui_presentation.py`.
  - The following facility ScreenModels have been extracted from `gui_actions.py`:
    - Shop, Magic Shop, Workshop, Storage, Synthesis, Temple, Relic Preview, Guild.
  - Action dispatching, validation, and mutation are retained in `gui_actions.py`.
  - Exploration/Combat, World Map/Town Hub, and Inn are temporarily not subject to further micro-extraction to avoid complexity.

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

Current facility-family planning state:

- Shop + Magic Shop GUI Layout Normalization V0.5 first CSS-only checkpoint is
  complete through `c7729df`.
- The active Mockup-to-HTML model is family-level:
  AI facility hero image supplies scene / NPC / lighting / atmosphere;
  HTML/CSS/JS supplies panels / text / lists / controls / interaction;
  Python runtime supplies gameplay state, validation, and results.
- `08_experiments/mockup_to_html/bg-npc.png` and
  `08_experiments/mockup_to_html/code_artifact.html` are approved reference
  examples for that responsibility split. They are not runtime assets or a
  formal asset pipeline.
- `01_content/gui-facility-shell-baseline-v0.1.md` is the current facility-family
  planning baseline.
- The Shop single-screen readiness checklist and mockup brief are paused. Do not
  resume Shop skinning or generate another Shop candidate without explicit owner
  approval.
- Owner-approved isolated Shop Skinning Lab v0.2.2 exists under
  `08_experiments/mockup_to_html/shop_skinning_lab/` as a fixture-only,
  player-facing visual baseline. It is not runtime source, not a formal
  `07_gui_prototype/shop_screen/` replacement, and not a formal asset pipeline.
- Future lab-only skinning should read the lab `README.md`,
  `shop-skinning-process-note-v1.md`, and local lab files first. Do not reload
  broad GUI/runtime docs unless the task explicitly asks for resync,
  merge-back, runtime bridge, or formal prototype work.

Current newest GUI live state:

- Phase B facility coverage landed in `eed7b4b`:
  Synthesis supports the four existing Mira recipes; Shop iterates all nine
  existing travel-shop entries; Magic Shop iterates all existing `MAGIC_BOOKS`
  and aligns debuff books with the CLI special-magic category.
- Shop accessory purchases go to the backpack without auto-equip. Shop,
  Synthesis, and Magic Shop remain existing-data coverage, not generic facility
  frameworks.
- The missing fire-mark Guild inquiry bridge is closed:
  `fire_mark_guild_inquiry` reuses the CLI prerequisite and mutation helpers,
  keeps all three shards, sets `fire_mark_guild_inquiry_done`, and lets the
  Temple bridge appear naturally without manually setting the flag.
- Guild material sell landed in `2ecca91`: Guild live mode provides task /
  material-sell modes, lists only owned entries registered in
  `GUILD_MATERIAL_BUY_PRICES`, and dispatches `sell_guild_material`. Python
  validates eligibility, positive integer quantity, owned quantity, and
  confirmation before removing materials and adding the existing buyback total
  to Gold. This does not open Shop sell, equipment sell, or generic sell.
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
- Synthesis existing Mira recipe coverage is complete:
  `synthesis_screen` live mode loads a runtime-shaped ScreenModel and dispatches
  `craft_recipe` for `recipe_fire_cloak`, `recipe_focus_pouch`,
  `recipe_heat_charm`, and `recipe_piercing_bundle`.
- Crafting reuses Python runtime authority:
  `game.recipe_available(...)` and `game.craft_recipe_message(...)`.
- This does not mean full inventory / equipment, storage capacity upgrade,
  arbitrary synthesis, crafting, guild quest, story hint, generic boss, full
  Act 2, sell, or facility systems are complete.
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

- Facility-family Mockup-to-HTML responsibility and configuration baseline:
  `01_content/gui-facility-shell-baseline-v0.1.md`
- Paused Shop single-screen planning:
  `01_content/gui-shop-skinning-lab-readiness-checklist-v0.1.md` and
  `01_content/gui-shop-mockup-brief-v0.1.md`; read only when the owner explicitly
  reopens that route.
- Isolated Shop Skinning Lab capsule:
  `08_experiments/mockup_to_html/shop_skinning_lab/README.md` and
  `08_experiments/mockup_to_html/shop_skinning_lab/shop-skinning-process-note-v1.md`;
  read these plus local lab files for owner-approved lab-only skinning. This does
  not reopen formal Shop single-screen skinning or runtime work.
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
- Shop sell, equipment sell, generic sell, generic unequip, comparison,
  non-whitelisted upgrade expansion, or generic workshop framework.
- Full shop, magic shop, storage capacity upgrade, synthesis, guild,
  quest, boss, dungeon, magic, skill, target-selection, or facility framework.
- New quest data, schema changes, broad quest framework changes, or story inquiry
  expansion beyond the existing fire-mark and Boss Glen closures.
- Save migration, data/schema changes, combat formula changes, stat rebalance, or
  manual `save.json` edits.
- Formal asset pipeline or reference/mockup images as runtime assets.
- Runtime or GUI feature implementation without a new owner-approved exact scope.

## Next-Step Boundary

- God File / Maintainability Checkpoint is sufficiently converged.
- Endless ScreenModel micro-extraction is not recommended.
- Shop + Magic Shop GUI Layout Normalization V0.5 first CSS-only checkpoint is
  complete through `c7729df`.
- Current work has returned to the facility-family Mockup-to-HTML shell baseline.
- The next smallest candidate is a markdown-only Facility Family Overlay Zone
  Map V0.1.
- Do not select one facility for skinning, generate an image brief, generate a
  candidate, or implement HTML/CSS without new explicit owner approval.
- Phase C convenience candidates, runtime/data/schema/save/combat remain deferred.

No next implementation is pre-approved. Basic facility CLI-parity bridge
coverage is complete through the existing Guild material-buyback behavior.

The Glen UX cleanup and the narrow Ash / Cinder GUI presentation cleanup are
complete in the current package. Remaining Boss / Act 2 observations are
coverage-oriented only; this does not approve Ash Guardian, Cinder Seal
Sentinel, generic Boss handling, full story hints, Temple / Relic gameplay, or
full Act 2 cleanup beyond the existing bridge presentation work.

Remaining Phase C convenience candidates are deferred:

1. Inventory / equipment management.
2. Storage capacity upgrade.
3. Bestiary detail / filtering.
4. Settings panel.

Any Phase C convenience follow-up must start with a later read-only gate and
explicit owner approval. Do not open storage capacity upgrades, generic
inventory / equipment management, settings, Shop or equipment sell, generic
sell, bestiary detail framework, schema changes, save migration, combat formula
changes, or manual `save.json` work from the current bridge coverage.

For docs-only sync, restrict changes to explicitly approved markdown surfaces and
do not touch runtime, JavaScript, data, schema, save, or combat formula.

## Verification Capsule

Latest stable verification noted here:

- Maintainability checkpoint through `7c23bad`:
  Guild ScreenModel parity and extraction checks PASS.
- Guild material sell bridge Codex recheck after `2ecca91`:
  `smoke_test_guild_material_sell_bridge.py`,
  `smoke_test_guild_quest_bridge.py`, `smoke_test_progression_bridge.py`,
  `smoke_test_fire_mark_guild_bridge.py`, `smoke_test_shop_bridge.py`,
  `validate_data.py`, `element_maze.py --smoke-test`, and Guild JavaScript
  syntax check all PASS.
- Current Phase B + fire-mark inquiry package Codex recheck:
  `smoke_test_fire_mark_guild_bridge.py`, `smoke_test_temple_bridge.py`,
  `smoke_test_shop_bridge.py`, `smoke_test_magic_shop_bridge.py`,
  `smoke_test_synthesis_bridge.py`, `smoke_test_progression_bridge.py`,
  `validate_data.py`, `element_maze.py --smoke-test`, and JavaScript syntax
  checks for Guild, Shop, and Magic Shop all PASS.
- `06_tools/validate_data.py`: PASS
- `element_maze.py --smoke-test`: PASS
- Workshop bridge smoke: PASS
- Workshop Weapon Equip owner-side manual smoke: purchase does not auto-equip,
  equip does not deduct Gold, old weapon returns to inventory, new weapon becomes
  `equipment.weapon`, and World Map save / reload preserves equipment state.
- Town Hub Mira / 米菈合成屋 Entry Unlock Antigravity-reported checks:
  `element_maze.py --smoke-test` PASS, `06_tools/validate_data.py` PASS, scratch
  `test_synthesis.py` PASS.
- Historical Synthesis single-recipe baseline Antigravity-reported checks:
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
