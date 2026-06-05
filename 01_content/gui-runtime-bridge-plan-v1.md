# GUI Runtime Bridge Plan v1

Purpose: plan the path from HTML static prototypes to a local runtime-connected
prototype without blurring project boundaries.

This file is a planning document, not implementation status. Read live files for
current state before making changes.

## 1. Intent

The current GUI work in `07_gui_prototype/` is static by design. It validates
screen layout, interaction feel, navigation, fixtures, and UIAction logging. It
does not connect to Python runtime, read or write `save.json`, or copy gameplay
rules into JavaScript.

The runtime bridge should add a separate live mode where browser clicks dispatch
UIAction payloads to the Python runtime. The Python side remains responsible for
state changes, save/load, validation, and gameplay rules.

Bridge-planning posture: Element Maze is an expandable playable demo, not a
closed demo. Narrow live slices prove and constrain current bridge risk; they do
not seal off future extension points.

## 2. Modes

### Static Prototype Mode

Static prototype mode remains the default for GUI screen work.

- Source: static JSON fixtures under `07_gui_prototype/<screen>/fixtures/`.
- Behavior: render fixture data, validate layout, validate UIAction logging.
- Forbidden: Python runtime connection, `save.json`, runtime/data/schema/combat
  changes, gameplay rule duplication in JavaScript.

### Runtime-Connected Prototype Mode

Runtime-connected prototype mode is opt-in and requires explicit user approval.

- Source: a local Python bridge service that owns runtime state.
- Behavior: browser UIActions call bridge endpoints; bridge mutates state through
  Python runtime helpers and returns screen models.
- Save/load: only through the runtime bridge using existing runtime save/load
  behavior. Do not manually edit `save.json`.
- JavaScript role: dispatch UIAction, render returned screen model, show result
  feedback. JavaScript must not become gameplay SSOT.

## 3. Approved Surfaces After Explicit Runtime Bridge Approval

When the user explicitly approves runtime-connected prototype work, the narrow
implementation surface may include:

- `06_tools/`: local runtime bridge server and bridge smoke helpers.
- `03_engine/engine/`: small action adapter/helper functions that reuse existing
  runtime logic.
- `07_gui_prototype/`: live-mode client and render integration.
- `save.json`: only as an output/input of existing runtime save/load behavior,
  never as direct hand-edited fixture data.

Runtime/data/schema/combat formula changes remain out of scope unless the user
separately approves that exact work after a read-only planning gate.

## 3.1 Current Landed Live Matrix

This matrix is the Task Zone home for live bridge status that should not bloat
`README.md` or `01_content/codex-handoff-short.md`.

For this matrix, `Not opened` means excluded from the current approved slice. It
does not permanently close the system family. Same-family coverage may proceed
later only through a read-only gate, owner-approved exact scope, and reuse of the
existing runtime-authoritative adapter / ScreenModel pattern where appropriate.

| Slice | Commit | Landed scope | Not opened |
|---|---|---|---|
| Start / load / restart | blessed live bridge cleanup | `start_new_game`, `restart_game`, `load_game`, live entry-state alignment. | Full frontend app shell or save migration. |
| Inn | blessed live bridge cleanup | `rest_at_inn` through Python runtime state. | Broader facility framework. |
| World Map | blessed live bridge cleanup | Runtime-backed route model, `save_game`, shell-only `open_settings`. | Real settings panel or arbitrary town return action. |
| Dungeon / Combat loop | `be6b06c [antig] feat(gui): complete live combat loop feedback` | Travel, exploration step / retreat, combat actions, victory result, route clear / resolved state. | Complete dungeon framework, boss framework, combat formula changes. |
| Guild report | `c2052d4 [antig] feat(gui): add guild clear report live bridge` | Clear report registration and display for eligible unlocked dungeon clears. | Full guild / quest / reputation / achievement system. |
| Guild Quest Turn-in for Synthesis Unlock | `017fa43 [antig] feat(gui): add guild quest synthesis unlock bridge` | Guild live mode shows unlocked existing `QUESTS`; `submit_quest` completes ready turn-ins through existing runtime validation, reward, and unlock behavior. `quest_cave_gathering` unlocks `shop_synthesis_01`. | Full guild / quest framework, new quest data, story inquiry expansion, save/schema/combat changes, full synthesis, generic recipe bridge. |
| Guild x Dungeon Boss Glen Gating | `9ae502b [antig] fix(gui): repair Boss Glen progression bridge` | Special Scorched Mine Boss Glen gate: 18/18 clue sets `boss_glen_sighted`, Guild `accept_boss_glen_investigation` sets `boss_glen_investigation_accepted`, `challenge_boss` opens after acceptance, and `quest_boss_glen` / Blood Map turn-in unlocks Ash Ravine through existing runtime progression. | Full quest framework, story hint framework, generic boss framework, full Act 2 cleanup, data/schema/save/combat changes. |
| Glen Boss flow UX cleanup | `709dc6c [antig] fix(gui): improve dungeon event scrolling and guild story progression hints` | Persistent Guild story hint review cards across Glen / Act 2 guidance states, Blood Map reward key mapping, HP/MP-only dungeon resource strip, semantic dungeon metrics, scrollable auto-bottom event preview, dynamic 3-column action-bar layout, and boss victory exploration events. | Full quest / story / dungeon / storage / workshop frameworks. |
| Ash / Cinder presentation cleanup | current package | Existing Ash Ravine and Cinder Seal Depths progression remains runtime-owned; Guild story hints and Dungeon Exploration boss / narrative labels avoid premature Boss, reward, and follow-on unlock spoilers before the relevant scout reports. Temple static fixture lore copy is softened. | Generic boss / story / dungeon framework, Act 2 cleanup, Temple / Relic gameplay, data/schema/save/combat changes. |
| Combat Skill Button | `4acd04d [antig] feat(gui): add combat skill button live bridge` | `use_skill` routing from existing `learned_skills` and `SKILLS`. | Formal skill framework, target selection, rebalance. |
| Shop Buy Consumable | `ebc1b5e [antig] feat(gui): add shop buy consumable live bridge` | Buy 1 existing travel-shop consumable through server-side validation. | Full shop system, sell, quantity selector, equipment purchase. |
| Magic Shop Learn Book | `b59fe43 [antig] feat(gui): add magic shop learn book live bridge` | Learn 1 existing magic book through server-side validation. | Full magic / skill framework or combat rebalance. |
| Workshop Buy Weapon & Armor | current package | Buy existing weapon & armor; do not auto-equip. | Accessory purchase, sell, quantity selector, full workshop framework. |
| Workshop Equip & Limited Upgrade | current package | Equip weapons and owned non-weapon equipment; upgrade whitelisted recipes (`recipe_iron_sword_plus_1`, `recipe_leather_armor_plus_1`). | Generic equipment management (unequip, comparison), non-whitelisted recipes. |
| Storage Deposit & Withdraw | current package | Town Hub routes to Storage live screen; `storage_screen_model(state)` renders live inventory / storage status / storage contents / capacity; `unlock_storage` checks cost & unlocks; `deposit_item` & `withdraw_item` allow transferring items. | Storage capacity upgrade, full storage system, generic inventory / equipment management, schema/save/combat changes. |
| Town Hub Mira Entry Unlock | `b046b1e [antig] feat(gui): add Mira synthesis entry unlock bridge` | Town Hub synthesis facility node reflects `is_unlocked(state, "shop_synthesis_01")`; locked state points to Guild task `洞窟採集`; unlocked state routes to the existing static synthesis screen. | Full synthesis, recipe bridge, `synthesis_screen_model()`, live loader, `craft_recipe`, recipe / quest / dungeon / schema / save / combat changes. |
| Synthesis Single Recipe Craft | `5dbc742 [antig] feat(gui): add synthesis single recipe craft bridge` | `synthesis_screen` live mode loads a runtime-shaped ScreenModel and dispatches `craft_recipe` for the single whitelisted recipe `recipe_piercing_bundle`, reusing `game.recipe_available(...)` and `game.craft_recipe_message(...)`. | Full synthesis, generic recipe bridge, multi-recipe coverage, base-item upgrades, recipe / quest / dungeon / schema / save / combat changes. |
| Temple / Church lookup bridge | current package | Live-mode loading, promotion requirement preview, moon well pray, fire-mark church bridge and lookup inquiry actions using Python runtime helpers. | Formal class transfer, class specialization gameplay, manual save.json edits. |
| Relic Preview live opening | current package | Altar screen live-mode loading, previewing registered relics (e.g., ash charm) and requirements, attune action placeholder. | Formal relic effects, equipping/obtaining relics, manual save.json edits. |


Latest committed bridge baseline:
`709dc6c [antig] fix(gui): improve dungeon event scrolling and guild story progression hints`.

## 3.2 Reusable Bridge Pattern Audit

Read-only audit, 2026-06-04:

- Governance rule: each facility / system should first use a narrow MVP to prove
  the runtime bridge shape. After that bridge exists, same-family CLI content
  should usually be described as CLI coverage / bridge coverage follow-up, not as
  a fresh MVP for every item, quest, recipe, dungeon, or monster.
- Browser JavaScript remains a UIAction dispatcher and ScreenModel renderer.
  Python runtime / data / save behavior remains gameplay authority.
- A same-family coverage follow-up still needs an owner-approved exact scope, but
  it should prefer extending the existing adapter / ScreenModel pattern over
  creating a parallel gameplay rule.
- Boss Glen clarified the split between same-family bridge coverage and special
  gating MVPs: already bridged dungeon / combat / guild families may surface CLI
  runtime progression naturally, but special clue-to-Guild-to-Boss gates still
  need a small owner-approved gate instead of a generic boss framework.

| System | Current reusable state | Hardcoded risk | Coverage direction |
|---|---|---|---|
| Shop / travel shop | `buy_item` validates against existing `SHOP_INVENTORY["travel"]` and item data, but the current live ScreenModel lists a fixed consumable subset and `buy_item` still rejects non-consumables. | Medium. Bridge exists for travel consumable purchase, but battle items / accessories are not yet natural GUI coverage. | Extend the ScreenModel to iterate travel inventory and explicitly decide which existing item kinds are in scope. Do not make one MVP per item. |
| Workshop | Weapon & armor buy reads `SHOP_INVENTORY`; `equip_equipment` and `equip_weapon` reuse `game.equip_item(...)`; upgrades support whitelisted recipes. | Low to medium. Weapon, armor, and whitelisted upgrades are reusable; comparison, unequip, and non-whitelisted upgrades remain closed. | Add more recipe ids as coverage. Generic equipment management (unequip, comparison) needs its own planning gate. |
| Magic shop | `learn_magic_book` validates `MAGIC_BOOKS`, `SKILLS`, job, level, gold, materials, and learned state server-side. ScreenModel still uses a fixed book id list. | Low to medium. Mutation action is reusable; presentation list is narrower than CLI data. | Iterate `MAGIC_BOOKS` in the model before adding more books. No one-book-per-MVP pattern is needed. |
| World map / dungeon / exploration / combat | World Map iterates `DUNGEONS` and runtime unlocks; `confirm_travel`, `advance_step`, combat, retreat, route clear, item rows, and skill rows are shared flow pieces. | Medium. Multiple dungeons can route through the bridge, but complete dungeon events, boss framework, and combat formula changes remain closed. | Treat existing dungeons as coverage follow-up unless the task opens boss / special event behavior. |
| Guild | Current GUI bridge includes dungeon clear report registration from `DUNGEONS`; `017fa43` adds existing `QUESTS` turn-in / reward / unlock coverage for ready quests, validated by `quest_cave_gathering` unlocking `shop_synthesis_01`. | Medium. The turn-in adapter reuses runtime helpers, but this is not a generic guild framework, reputation system, achievement system, or story inquiry bridge. | Treat additional existing `QUESTS` turn-in coverage as same-family coverage follow-up only after an owner-approved exact scope. New quest data, story inquiry, reputation, or broad framework work still needs its own gate. |
| Synthesis / crafting | Town Hub entry unlock is committed. `5dbc742` adds one whitelisted `craft_recipe` path for `recipe_piercing_bundle` and reuses `game.recipe_available(...)` plus `game.craft_recipe_message(...)`. ScreenModel and live loader are deliberately single-recipe. | High for full crafting. The bridge proves one action path, but full synthesis, base-item recipes, and broad recipe iteration remain closed. | Next coverage should start with a read-only gate before iterating more existing Mira recipe ids. Base-item upgrades require a separate gate. |
| Storage | Opens Town Hub routing, live Storage ScreenModel, `unlock_storage`, `deposit_item`, and `withdraw_item` against existing runtime storage state. Capacity upgrades remain disabled. | Low to medium. Storage unlock, view, and deposit / withdraw transfer are now bridged; capacity upgrade behavior remains closed. | Treat capacity upgrade as a separate read-only gate. Do not let deposit / withdraw imply generic inventory or slot management. |
| Inventory / backpack / equipment | World Map utility preview reads runtime inventory plus currently equipped equipment. Workshop can equip weapons and owned non-weapon equipment through approved bridge actions. | Medium. Display is reusable; equipment mutation remains workshop-scoped and does not include unequip / comparison / generic management. | More item display is coverage; generic unequip / comparison / slot management requires its own gate. |
| Bestiary | Preview reads runtime `state["bestiary"]` and monster data, so more registered monsters naturally display. | Low. Mostly a summary presentation surface. | Add detail / filtering as coverage work, not one-monster MVPs. |

Explicit exceptions that are not yet fully bridged system families:

- Guild features beyond existing `QUESTS` turn-in / reward / unlock coverage
  and the current Boss Glen investigation gate.
- Generic boss / story-hint progression beyond the narrow Boss Glen special
  gating bridge.
- Full Act 2 progression cleanup beyond Ash Ravine / fire-demo content naturally
  surfaced through existing CLI runtime progression.
- Complete crafting / synthesis beyond the single whitelisted
  `recipe_piercing_bundle` craft path.
- Complete storage beyond deposit/withdraw, including capacity upgrade behavior.
- Generic equipment management beyond approved workshop equip actions.

Future coverage queue after Phase A close:

Phase B is the second-priority facility coverage track, not an approved
implementation batch:

1. Synthesis existing Mira recipes coverage.
2. Shop travel inventory coverage.
3. Magic Shop `MAGIC_BOOKS` coverage.
4. Workshop upgrade coverage.

For Phase B, owner manual testing may be batched after 2-3 small slices, but each
slice still needs a read-only planning gate, a narrow exact scope, and the
runtime-authoritative ScreenModel / UIAction pattern. Do not turn the batch plan
into a generic facility framework or broad data/schema/save/combat change.

Phase C convenience work is deferred and remains closed for now:

1. Guild material sell.
2. Inventory / equipment management.
3. Storage capacity upgrade.
4. Bestiary detail / filtering.
5. Settings panel.

Phase C items require their own later read-only gate and owner-approved exact
scope. They are not opened by Phase B facility coverage notes.

Town Hub Mira and Synthesis result after this audit:

- Town Hub Mira / 米菈合成屋 Entry Unlock Live MVP has landed in
  `b046b1e [antig] feat(gui): add Mira synthesis entry unlock bridge`.
- Scope is only the Town Hub synthesis facility node reflecting
  `is_unlocked(state, "shop_synthesis_01")` as locked / unlocked.
- Synthesis Single Recipe Craft Live MVP has landed in
  `5dbc742 [antig] feat(gui): add synthesis single recipe craft bridge`.
- Scope is only `recipe_piercing_bundle` on `synthesis_screen`, with
  `craft_recipe` whitelisted to that recipe id.
- Python runtime remains gameplay authority through `game.recipe_available(...)`
  and `game.craft_recipe_message(...)`.
- This slice must not add or modify recipes, quests, dungeons, schema, save
  behavior, combat formulas, or the crafting system.
- Next synthesis follow-up candidate is a read-only gate for broader synthesis
  coverage, such as deciding whether to iterate more existing Mira recipe ids.

## 4. Bridge Shape

Recommended local-only architecture:

```text
browser UIAction
  -> runtime-client.js
  -> localhost bridge API
  -> Python action dispatcher
  -> existing engine/state helpers
  -> in-memory state
  -> optional save_game/load_game
  -> screen model JSON response
```

The bridge should be local development tooling, not a production server.

Suggested endpoints:

- `GET /api/session`
  - Returns bridge health, whether save exists, and current player summary if a
    state is loaded.
- `POST /api/session/new`
  - Payload: `{ "name": "...", "job_id": "..." }`.
  - Creates runtime state through `create_state`.
- `POST /api/session/load`
  - Loads existing runtime save through `load_game`.
- `POST /api/save`
  - Persists current state through `save_game`.
- `GET /api/screen/<screen_id>`
  - Returns a live screen model shaped close to existing fixtures.
- `POST /api/action`
  - Payload: `{ "action_id": "...", "payload": {...}, "screen_id": "..." }`.
  - Dispatches a whitelisted action and returns `{ ok, message, state_summary,
    screen_model }`.

## 5. Phases

### Phase 0 - Governance And Static Readiness

- Keep existing static prototype mode intact.
- Let Antigravity add static prototype screens for Inn, Temple, and Relic Preview
  without treating those files as drift.
- Use stable action ids in those static screens so the bridge can map them later.

Recommended static screen folders:

- `07_gui_prototype/inn_screen/`
- `07_gui_prototype/temple_screen/`
- `07_gui_prototype/relic_preview_screen/`

### Phase 1 - Start, Load, Save

Goal: prove the browser can talk to the runtime and save through Python.

Live actions:

- `start_new_game`
- `restart_game`
- `load_game`
- `save_game`

Live screens:

- Start Screen
- World Map summary
- Town Hub summary/navigation

This phase should not touch combat, data, schema, or save migration.

### Phase 2 - Inn As First Mutating Facility

Goal: prove a simple facility action mutates runtime state and can be saved.

Live action:

- `rest_at_inn`
  - Payload: `{ "service_id": "overnight_rest", "cost": 30 }`.
  - Runtime effect: deduct gold, restore HP/MP to current max values.

The inn is the best first facility because it has a small, visible state change:
gold down, HP/MP restored.

### Phase 3 - Town Facilities With Existing Mutators

Map current GUI UIActions to Python runtime helpers:

- `buy_item` -> travel shop purchase helper.
- `buy_equipment` -> workshop equipment purchase helper.
- `equip_weapon` -> workshop weapon equip helper.
- `upgrade_equipment` -> recipe craft helper.
- `craft_recipe` -> recipe craft helper.
- `learn_magic_book` -> magic shop learn helper.
- `unlock_storage` -> storage unlock helper.
- `deposit_item` -> storage deposit helper.
- `withdraw_item` -> storage withdraw helper.
- `report_dungeon_clear` -> guild clear report registration helper for the
  narrow Guild Report MVP only.
- `submit_quest` -> existing `QUESTS` turn-in adapter for the narrow Guild Quest
  Turn-in for Synthesis Unlock MVP.
- `accept_boss_glen_investigation` -> narrow Boss Glen story-hint action that
  records Guild acceptance of the Scorched Mine clue and opens the formal Blood
  Map / Boss challenge gate.
- `challenge_boss` -> narrow dungeon-end Boss entry action for approved Boss
  gates; Boss combat and victory resolution remain Python runtime owned.

Where CLI functions currently prompt for input, add small non-interactive helper
functions instead of simulating CLI input.

Status note, 2026-06-01:

- A narrow Guild Report / Dungeon Clear Reward MVP has landed through
  `c2052d4 [antig] feat(gui): add guild clear report live bridge`.
- Completed coverage is limited to Town Hub -> Guild live routing, a runtime-shaped
  Guild ScreenModel for unlocked dungeon clear / report status, and report
  registration when the player's current guild task state, unlock conditions, and
  dungeon clear state make that report available.
- The report action only sets `state.flags["guild_reported_<dungeon_id>"] = True`
  to register / display report status. First-clear reward timing remains at route
  clear; Guild report does not reissue clear reward or move reward timing.
- Static fixture fallback remains available, and story hint is only a hidden
  placeholder in this MVP.
- This status note does not approve a complete guild system, formal quest
  framework, reputation, achievement, data/schema changes, save migration, combat
  formula changes, or any broader facility family bridge.

Status note, 2026-06-04:

- A narrow Guild Quest Turn-in for Synthesis Unlock MVP has landed through
  `017fa43 [antig] feat(gui): add guild quest synthesis unlock bridge`.
- Completed coverage is limited to Guild live routing already established by the
  Guild Report MVP, a runtime-shaped Guild ScreenModel for unlocked existing
  `QUESTS`, and `submit_quest` for ready quest turn-ins.
- The validated path is `quest_cave_gathering`: submit
  `mat_moss_fiber x3` and `mat_cracked_stone x2`, receive the existing quest
  reward, and unlock `shop_synthesis_01` through existing runtime unlock
  behavior.
- Python runtime remains gameplay authority through `game.quest_ready(...)`,
  `game.pay_items(...)`, reward application, `game.add_item(...)`, and
  `game.unlock(...)`. Browser JavaScript continues to dispatch UIAction payloads
  and render returned ScreenModels.
- Dungeon clear report semantics remain separate. First-clear rewards still
  happen at route clear, and Guild report registration only records / displays
  report status.
- Antigravity-reported verification passed:
  `python 06_tools/smoke_test_guild_quest_bridge.py`,
  `python 06_tools/validate_data.py`,
  `python element_maze.py --smoke-test`,
  `python 06_tools/smoke_test_synthesis_bridge.py`,
  `python 06_tools/smoke_test_workshop_bridge.py`, and
  `python 06_tools/smoke_test_magic_shop_bridge.py`.
- Owner manual hand test passed: locked synthesis before quest completion,
  unlocked synthesis after Guild quest turn-in, save/load persistence for
  unlocked state, new-game locked state, and old completed save unlocked state.
- Owner exploratory bridge-loop hand test later confirmed that runtime can
  progress to 焦石礦坑, 焦石礦坑 exploration report can complete and appear in
  Guild as completed, Mira synthesis unlock works, `recipe_piercing_bundle` can
  be crafted, and the crafted battle item can be used in combat. This is only
  supplementary verification for the Guild / Synthesis unlock loop.
- This status note does not approve a full guild / quest framework, new quest
  data, story inquiry expansion, reputation / achievement systems, schema
  changes, save migration, combat formula changes, full synthesis, generic
  recipe bridge, multi-recipe synthesis coverage, base-item upgrades, boss /
  血跡地圖 progression, more quests, a combat item system, or crafting system
  refactors.

Status note, 2026-06-05:

- A narrow Scorched Mine Boss Glen Progression Deadlock Fix landed in
  `9ae502b [antig] fix(gui): repair Boss Glen progression bridge`.
- Completed coverage is limited to the Guild x Dungeon special gate for
  `boss_glen`: Scorched Mine 18/18 records `boss_glen_sighted`, Guild
  `accept_boss_glen_investigation` records
  `boss_glen_investigation_accepted`, `challenge_boss` becomes available only
  after Guild acceptance, Boss victory records existing defeat / loot state, and
  `quest_boss_glen` / Blood Map turn-in unlocks Ash Ravine / Act 2 entry through
  existing runtime progression.
- Python runtime remains gameplay authority. The bridge uses existing state,
  flags, quest validation, combat start / victory resolution, item rewards, and
  unlock behavior; Browser JavaScript continues to dispatch UIAction payloads
  and render returned ScreenModels.
- Owner manual hand test confirmed: first Scorched Mine 18/18 cannot directly
  challenge Glen and points back to Guild, Guild accepts the investigation,
  returning to 18/18 opens Boss Glen combat, Blood Map can be reported after
  victory, Ash Ravine unlocks and can clear, later Ash Ravine Boss / fire-shard
  visibility follows existing CLI runtime progression, and supply-line upgrade
  turn-in / medium potion unlock still works.
- Recorded follow-up observations are player-facing UX / wording coverage only:
  post-investigation Guild guidance, internal unlock keys in quest rewards,
  Dungeon Exploration bottom button layout when Boss challenge actions appear,
  and Ash Ravine / later fire-demo prompt wording.
- This status note does not approve a full quest framework, full story hint
  framework, generic boss framework, full Act 2 progression cleanup, new quest
  data, data/schema/save migration, combat formula changes, Temple / Relic /
  class transfer work, full storage, full workshop, or manual `save.json` edits.

Status note, 2026-06-05:

- Glen Boss flow UX cleanup landed in
  `709dc6c [antig] fix(gui): improve dungeon event scrolling and guild story progression hints`.
- Completed coverage is limited to player-facing bridge presentation around the
  already-approved Glen flow: persistent Guild story hint review cards for Glen
  and follow-on Act 2 guidance states, player-facing unlock labels for Blood Map
  reward display, HP/MP-only Dungeon Exploration resource strip with run Gold
  kept in current-run rewards, scrollable auto-bottom dungeon event preview,
  dynamic three-column action-bar layout, and boss victory exploration event
  presentation.
- Python runtime remains gameplay authority for flags, boss availability,
  quest-ready state, rewards, inventory, combat results, and route clear state.
  Browser JavaScript continues to render ScreenModels and dispatch UIActions.
- Antigravity-reported verification passed:
  `python 06_tools/smoke_test_progression_bridge.py`,
  `python element_maze.py --smoke-test`, and
  `python 06_tools/validate_data.py`.
- This status note does not approve a generic boss framework, full quest
  framework, full story hint framework, full dungeon framework, full Act 2
  progression cleanup, data/schema/save migration, combat formula changes,
  Temple / Relic / class transfer work, equipment / workshop expansion, full
  storage, or manual `save.json` edits.

Status note, 2026-06-05:

- Ash Ravine / Cinder Seal Depths GUI presentation cleanup is implemented in the
  current package. Completed coverage is limited to player-facing wording in
  `gui_actions.py`: Dungeon Exploration now uses progression-aware Boss /
  narrative labels, and Guild story hint cards avoid premature Boss, reward, and
  follow-on unlock spoilers before the relevant scout reports. The Temple static
  fixture fire-mark lore copy is also softened.
- Python runtime remains gameplay authority for quest completion, Boss
  availability, flags, rewards, unlocks, inventory, combat results, and route
  clear state. Browser JavaScript continues to render returned ScreenModels and
  dispatch UIActions only.
- Owner manual hand test confirmed: Ash Ravine first clear reaches a non-Boss
  terminal state, Guild scout turn-in updates the guidance and opens the Ash
  Boss path, Ash Boss victory unlocks follow-on supply-line guidance,
  supply-line turn-in unlocks Cinder Seal Depths, the Cinder scout / Boss path
  completes, and the flow reaches the Temple / Church handoff.
- Known MVP observation: Ash Ravine and Cinder Seal Depths currently share some
  fire-demo materials, so later scout turn-ins can be ready immediately. This is
  existing CLI MVP content/data reuse, not a regression in this presentation
  cleanup.
- This status note does not approve a generic boss framework, full quest
  framework, full story hint framework, full dungeon framework, full Act 2
  progression cleanup, data/schema/save migration, combat formula changes,
  Temple / Relic / class transfer gameplay, formal relic work, or manual
  `save.json` edits.

Status note, 2026-06-04:

- A narrow Storage Deposit & Withdraw Live MVP is included in the current package.
- Completed coverage includes Town Hub -> Storage live routing, a runtime-shaped `storage_screen_model(state)` for live inventory / storage status / storage contents / capacity display, `unlock_storage` for opening the storage, and `deposit_item` / `withdraw_item` for transferring items between inventory and storage.
- Python runtime remains gameplay authority: the bridge uses the existing runtime storage unlock cost, blocks low Gold, deducts Gold on success, sets `state["storage_unlocked"] = True`, and validates deposit / withdraw requests against capacity limits and inventory quantities. Browser JavaScript dispatches UIAction payloads and renders returned ScreenModels.
- Storage capacity upgrades remain disabled in this MVP with explicit scope messaging.
- Antigravity-reported verification passed:
  `python 06_tools/smoke_test_storage_bridge.py`,
  `python 06_tools/validate_data.py`,
  `python element_maze.py --smoke-test`,
  `python 06_tools/smoke_test_guild_quest_bridge.py`,
  `python 06_tools/smoke_test_synthesis_bridge.py`,
  `python 06_tools/smoke_test_workshop_bridge.py`, and
  `python 06_tools/smoke_test_magic_shop_bridge.py`.
- Owner manual hand test passed: Storage screen opens in live mode, 500G unlock flow works, and after unlock the screen shows live inventory, storage status, and capacity. Item deposit and withdraw transfer work correctly.
- This status note does not approve capacity upgrade, a full storage system, generic inventory / equipment management, schema changes, save migration, combat formula changes, or manual `save.json` edits.

Status note, 2026-06-04:

- A narrow Workshop Armor Buy, Equip & Limited Upgrade Live MVP is included in the current package.
- Completed coverage is built on the previous weapon buy/equip bridge. It allows buying armor from `SHOP_INVENTORY["armor"]` via `buy_equipment` (without auto-equip), equipping owned non-weapon equipment via `equip_equipment` (reusing `game.equip_item(state, item_id, quiet=True)` and runtime slot data), and upgrading whitelisted recipes (`recipe_iron_sword_plus_1`, `recipe_leather_armor_plus_1`) via `upgrade_equipment`.
- Python server-side remains gameplay authority. Buying, equipping, and upgrading actions are validated against inventory, gold, job, and recipe unlock states.
- Upgrading consumes base equipment and required materials, deducts gold, and inserts the upgraded equipment into the player's inventory.
- This status note does not approve accessory buy, sell, generic equipment unequip, comparison, non-whitelisted upgrades, new recipes, new equipment data, save migration, schema changes, or manual `save.json` edits.


Status note, 2026-06-02:

- A narrow Shop Buy Consumable MVP has landed through
  `ebc1b5e [antig] feat(gui): add shop buy consumable live bridge`.
- Completed coverage is limited to Town Hub -> Shop live routing, a
  runtime-shaped Shop ScreenModel for travel shop consumables, and `buy_item`
  for purchasing exactly 1 consumable at a time.
- The action is limited to existing `SHOP_INVENTORY["travel"]` entries whose
  `ITEMS` data has `kind == "consumable"`. Existing unlock / availability rules
  still apply.
- Python server-side remains gameplay authority: it validates that `item_id`
  exists, belongs to the travel shop, is a consumable, is available / unlocked,
  and that Gold is sufficient. Insufficient Gold returns 409 blocked. Gold
  deduction and inventory increment happen server-side.
- Browser JavaScript only dispatches UIAction payloads through `runtimeClient`
  and renders the returned ScreenModel. Static fixture fallback and UIAction
  logging remain available.
- One owner-side Mage-route regression smoke confirmed Start -> Town -> Guild ->
  Shop -> Potion purchase -> World Map -> Dungeon -> Combat, including the
  existing item-use flow, without an obvious routing regression.
- This status note does not approve a complete shop system, equipment purchase,
  sell, quantity selector, complete inventory UI, shared Shop / Workshop /
  Magic Shop abstraction, generic facility framework, data/schema changes, save
  migration, combat formula changes, or any broader facility family bridge.

Status note, 2026-06-02:

- A narrow Magic Shop Learn Magic Book MVP has landed through
  `b59fe43 [antig] feat(gui): add magic shop learn book live bridge`.
- Completed coverage is limited to Town Hub -> Magic Shop live routing, a
  runtime-shaped Magic Shop ScreenModel for existing magic books, and
  `learn_magic_book` for learning one existing magic book at a time.
- The action is limited to existing `MAGIC_BOOKS` entries and their existing
  `SKILLS` references. No new magic books, skills, recipes, conditions, quests,
  items, or rules are added by this MVP.
- Python server-side remains gameplay authority: it validates that `book_id`
  exists, the referenced skill exists in `SKILLS`, the player's job is allowed,
  level is sufficient, Gold is sufficient, required materials are present, and
  the skill is not already learned. Blocked job / level / Gold / material /
  already learned states return blocked responses.
- On success, the bridge deducts Gold using the existing magic book price helper,
  pays required materials through existing runtime item payment behavior, and
  appends the referenced `skill_id` to `state["learned_skills"]`.
- Browser JavaScript only dispatches UIAction payloads through `runtimeClient`
  and renders the returned ScreenModel. Static fixture fallback and UIAction
  logging remain available.
- Owner-side smoke confirmed a CLI Mage Lv2 save can be picked up by the GUI
  live bridge; Town Hub -> Magic Shop live route works; book spark can be
  learned with Gold / materials / learned state updated; learned books disable
  their action; Rogue can learn an in-class book; out-of-class or unmet
  condition books are blocked; and the existing Combat Skill Button bridge can
  read and cast Spark after learning. The combat check is only a regression
  smoke, not completion of full Magic / Skill / Combat systems.
- This status note does not approve a complete magic shop system, formal magic
  or skill framework, target selection, combat formula or skill rebalance,
  generic facility framework, broader inventory / equipment / shop system,
  data/schema changes, save migration, or any broader facility family bridge.

Status note, 2026-06-03:

- A narrow Workshop Buy Weapon MVP has landed through
  `2d99d7e [antig] feat(gui): add workshop buy weapon live bridge MVP`.
- Completed coverage is limited to Town Hub -> Workshop live routing, a
  runtime-shaped Workshop ScreenModel for existing `SHOP_INVENTORY["weapon"]`
  entries, and `buy_equipment` for purchasing exactly one existing weapon at a
  time.
- The action is limited to existing `EQUIPMENT` entries sold through the weapon
  shop. Python server-side validates equipment existence, weapon-shop
  availability, player job compatibility, and sufficient Gold before deducting
  Gold and adding the weapon to inventory.
- Buying a weapon intentionally does not auto-equip it. Equipment changes require
  a separate approved equip action.
- Browser JavaScript only dispatches UIAction payloads through `runtimeClient`
  and renders the returned ScreenModel. Static fixture fallback and UIAction
  logging remain available.
- This status note does not approve armor purchase, accessory purchase, sell,
  quantity selection, upgrade flow expansion, full workshop system, full
  inventory / equipment management, data/schema changes, save migration, combat
  formula changes, stat rebalance, or any broader facility family bridge.

Status note, 2026-06-03:

- A narrow Workshop Weapon Equip MVP has landed through
  `6abe303 [antig] feat(gui): add workshop weapon equip bridge & align backpack presentation`.
- Completed coverage is limited to Workshop live routing already established by
  the buy weapon MVP, a runtime-shaped Workshop ScreenModel for weapon catalog
  and owned weapon display, and `equip_weapon` for equipping an inventory-held
  weapon into `state["equipment"]["weapon"]`.
- `buy_equipment` still does not auto-equip. Equipping happens only when the
  browser dispatches `equip_weapon` from the Workshop "owned equipment" surface.
- Python server-side remains gameplay authority: it validates that `item_id`
  exists in `EQUIPMENT`, that the item uses the `weapon` slot, that the player
  has the weapon in inventory, that the player's job can use it, and that the
  same weapon is not already equipped. Successful equip reuses
  `game.equip_item(state, item_id, quiet=True)`.
- Workshop owned aggregation and the World Map backpack / equipment overlay now
  display inventory equipment plus currently equipped equipment with same-item
  counts merged and equipped items marked. This is presentation alignment, not a
  complete inventory UI.
- Owner-side smoke confirmed purchase does not auto-equip, equipping does not
  deduct Gold, the old weapon returns to inventory, the new weapon becomes
  `equipment.weapon`, and save/load through World Map preserves equipment and
  backpack state.
- This status note does not approve armor, accessory, special-slot management,
  unequip, equipment comparison, upgrade flow expansion, complete inventory /
  equipment management, data/schema changes, save migration, combat formula
  changes, stat rebalance, or any broader facility family bridge.

Status note, 2026-06-04:

- A narrow Synthesis Single Recipe Craft Live MVP has landed through
  `5dbc742 [antig] feat(gui): add synthesis single recipe craft bridge`.
- Completed coverage is limited to Town Hub -> Synthesis live routing already
  established by the Mira entry unlock MVP, a runtime-shaped
  `synthesis_screen_model(state)` for one recipe, and `craft_recipe` for the
  single whitelisted recipe `recipe_piercing_bundle`.
- The action rejects non-whitelisted recipes, checks runtime recipe unlock state
  with `game.recipe_available(...)`, and performs the actual gold / material /
  output mutation through existing `game.craft_recipe_message(...)`.
- Browser JavaScript only loads the live ScreenModel, dispatches UIAction payloads
  through `runtimeClient`, renders returned ScreenModels, and keeps fixture
  fallback / UIAction logging available.
- Antigravity-reported verification passed:
  `node --check 07_gui_prototype/synthesis_screen/synthesis-screen.js`,
  `python 06_tools/smoke_test_synthesis_bridge.py`,
  `python 06_tools/validate_data.py`, and
  `python element_maze.py --smoke-test`.
- Owner manual hand test was intentionally not run for this slice.
- This status note does not approve complete synthesis, generic recipe bridge,
  multi-recipe coverage, base-item upgrades, recipe / quest / dungeon changes,
  data/schema changes, save migration, combat formula changes, or crafting
  system refactors.

Status note, 2026-06-05:

- A narrow Temple & Relic Altar Live MVP is included in the current package.
- Completed coverage includes live routing from Town Hub, live screen model generation for Temple and Relic Altar, and action dispatches for `temple_pray`, `fire_mark_church_bridge`, `fire_mark_church_lookup`, and `attune_relic`.
- Python gameplay rules remain the authority. `fire_mark_church_bridge` and `fire_mark_church_lookup` calls existing game helpers to mutate story flags on the backend and return story text to the client. Promotion previews check database conditions against live player state.
- Relic Altar previews `relic_ash_charm` and requirements, displaying it as unlocked when `unlock_ash_ravine` is unlocked in state. Attuning dispatches a preview-only action.
- Antigravity-reported verification passed:
  `python 06_tools/smoke_test_temple_bridge.py`,
  `python 06_tools/validate_data.py`, and
  `python element_maze.py --smoke-test`.
- This status note does not approve formal class transfer, class specialization gameplay, formal relic system, relic effects, equipping/obtaining relics, or manual `save.json` edits.


### Phase 4 - Temple And Relic Preview

Temple should avoid changing story flags merely because the screen opens.

Live actions:

- `view_promotion_preview`
- `advance_church_story`
- `fire_mark_church_bridge`
- `fire_mark_church_lookup`

Relic Preview should remain preview-first until relic gameplay is explicitly
approved.

Live actions:

- `view_relic_preview`
- `select_relic_preview`

### Phase 5 - Exploration And Combat

Exploration and combat are last because current CLI flow is blocking and
turn-based.

Expected actions:

- `confirm_travel`
- `advance_step`
- `retreat`
- `basic_attack`
- `defend`
- `open_skill_menu`
- `use_skill`
- `open_item_menu`
- `use_item`

This phase should introduce explicit runtime session state for exploration/combat
turns rather than trying to drive the CLI input loop from the browser.

Status note, 2026-06-01:

- A narrow traversal and combat loop slice has landed through
  `be6b06c [antig] feat(gui): complete live combat loop feedback`.
- Completed coverage is limited to World Map `confirm_travel`, Dungeon
  Exploration `advance_step` / `retreat`, Combat `basic_attack` / `defend` /
  supported `use_item` / `retreat`, victory result overlay feedback, return to
  Dungeon Exploration, minimal route clear / resolved state, and leaving the
  dungeon back to World Map.
- Victory result overlay now reports EXP, gold, drops, bestiary status, and
  level-up feedback. Defeat and retreat routing remain aligned with the approved
  traversal semantics.
- First-clear guild reward timing remains owned by the route clear moment; later
  Guild report registration only displays / records report status.
- This status note does not approve a complete skill system, inventory /
  equipment interaction, facility family, generic boss framework, complete
  dungeon event framework, combat formula changes, data/schema changes, or save
  migration.

Status note, 2026-06-02:

- A narrow Combat Skill Button Live MVP has landed through
  `4acd04d [antig] feat(gui): add combat skill button live bridge`.
- Completed coverage is limited to GUI live bridge `use_skill` routing and a
  Combat ScreenModel `skill_menu` generated from `state["learned_skills"]` and
  the existing `SKILLS` table.
- Skill button enabled / disabled state is derived from current MP, learned
  skill state, and whether combat has ended.
- Python server-side remains gameplay authority: it validates that `skill_id`
  is learned, the skill exists in the existing `SKILLS`, and MP is sufficient.
  Insufficient MP returns 409 blocked, and MP deduction happens server-side.
- Skill damage / heal / buff / debuff behavior reuses existing runtime behavior
  and data. Browser JavaScript only dispatches UIAction payloads and renders the
  returned ScreenModel.
- One Rogue / Assassin-route E2E manual test pass confirmed live bridge entry,
  combat entry, Rogue / Assassin skill usage, MP consumption, skill blocking
  after MP depletion, EXP gain through skill combat, level-up HP/MP refill,
  return to Dungeon Exploration, and later routing to World Map / Town Hub /
  Guild / Inn / Save without an obvious routing regression. Warrior, Mage,
  Priest, and other class skill branches remain pending for follow-up manual
  tests.
- This status note does not approve a complete GUI runtime, formal skill system,
  skill framework, target selection, skill rebalancing, large combat refactor,
  `game.py` changes, data/schema changes, save migration, or combat formula
  changes.

## 6. Action Contract

Each live action should have:

- stable `action_id`
- explicit payload schema
- server-side validation
- deterministic success/failure response
- returned state summary for resource strips
- returned screen model or next route suggestion
- UIAction log entry in the browser

Do not trust fixture `enabled` flags as runtime authority. The bridge must
validate whether the action is legal against current runtime state.

## 7. Screen Model Contract

Prefer returning JSON shaped close to the existing static fixtures so the render
layer can switch between fixture mode and live mode.

Minimum useful model fields:

- `screen_id`
- player/resource summary
- selected entity id, if applicable
- rows/cards/actions to render
- disabled reasons from runtime validation
- feedback message
- next route or suggested screen id

## 8. Verification Plan

Static mode verification:

- JSON fixture parse checks.
- JavaScript syntax checks.
- Browser checks for layout, navigation, and UIAction logging.

Runtime-connected mode verification:

- Data validation.
- Runtime smoke test.
- Bridge endpoint smoke tests.
- Browser click smoke for one happy path and one blocked path.
- Confirm save/load through runtime behavior, not manual `save.json` editing.

Recommended first live acceptance test:

1. Start a new game from the browser.
2. Reach World Map or Town Hub live summary.
3. Save from the browser.
4. Reload the bridge session from the browser.
5. Confirm player name/job/resources are preserved.

Recommended first mutating facility test:

1. Load a state with partial HP/MP and at least 30G.
2. Open Inn live screen.
3. Click `rest_at_inn`.
4. Confirm gold decreases by 30 and HP/MP are restored.
5. Save and reload to confirm persistence.

## 9. Open Decisions

- Whether live mode is toggled by query string, local setting, or separate server
  root.
- Whether successful mutating actions auto-save or require explicit `save_game`.
- Whether bridge responses should include full screen models every time or only
  patches.
- Whether combat live mode should be deterministic for testability.

Default recommendation:

- Query string or local toggle for live mode.
- Manual save in Phase 1, optional auto-save decision after Inn test.
- Full screen model response until payload size becomes a real issue.
- Deterministic combat test hooks only in bridge smoke tests, not normal play.
