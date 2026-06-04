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

| Slice | Commit | Landed scope | Not opened |
|---|---|---|---|
| Start / load / restart | blessed live bridge cleanup | `start_new_game`, `restart_game`, `load_game`, live entry-state alignment. | Full frontend app shell or save migration. |
| Inn | blessed live bridge cleanup | `rest_at_inn` through Python runtime state. | Broader facility framework. |
| World Map | blessed live bridge cleanup | Runtime-backed route model, `save_game`, shell-only `open_settings`. | Real settings panel or arbitrary town return action. |
| Dungeon / Combat loop | `be6b06c [antig] feat(gui): complete live combat loop feedback` | Travel, exploration step / retreat, combat actions, victory result, route clear / resolved state. | Complete dungeon framework, boss framework, combat formula changes. |
| Guild report | `c2052d4 [antig] feat(gui): add guild clear report live bridge` | Clear report registration and display for eligible unlocked dungeon clears. | Full guild / quest / reputation / achievement system. |
| Combat Skill Button | `4acd04d [antig] feat(gui): add combat skill button live bridge` | `use_skill` routing from existing `learned_skills` and `SKILLS`. | Formal skill framework, target selection, rebalance. |
| Shop Buy Consumable | `ebc1b5e [antig] feat(gui): add shop buy consumable live bridge` | Buy 1 existing travel-shop consumable through server-side validation. | Full shop system, sell, quantity selector, equipment purchase. |
| Magic Shop Learn Book | `b59fe43 [antig] feat(gui): add magic shop learn book live bridge` | Learn 1 existing magic book through server-side validation. | Full magic / skill framework or combat rebalance. |
| Workshop Buy Weapon | `2d99d7e [antig] feat(gui): add workshop buy weapon live bridge MVP` | Buy existing weapon-shop weapons; do not auto-equip. | Armor, upgrades, full workshop framework. |
| Workshop Weapon Equip | `6abe303 [antig] feat(gui): add workshop weapon equip bridge & align backpack presentation` | Equip inventory-held weapon-slot items into `equipment.weapon`; align inventory/equipment presentation. | Full inventory / equipment management, unequip, comparison, stat rebalance. |
| Town Hub Mira Entry Unlock | working tree, pending commit | Town Hub synthesis facility node reflects `is_unlocked(state, "shop_synthesis_01")`; locked state points to Guild task `洞窟採集`; unlocked state routes to the existing static synthesis screen. | Full synthesis, recipe bridge, `synthesis_screen_model()`, live loader, `craft_recipe`, recipe / quest / dungeon / schema / save / combat changes. |

Latest committed docs sync before Town Hub Mira:
`2b8e64d [codex] docs(gui): record reusable bridge audit`.

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

| System | Current reusable state | Hardcoded risk | Coverage direction |
|---|---|---|---|
| Shop / travel shop | `buy_item` validates against existing `SHOP_INVENTORY["travel"]` and item data, but the current live ScreenModel lists a fixed consumable subset and `buy_item` still rejects non-consumables. | Medium. Bridge exists for travel consumable purchase, but battle items / accessories are not yet natural GUI coverage. | Extend the ScreenModel to iterate travel inventory and explicitly decide which existing item kinds are in scope. Do not make one MVP per item. |
| Workshop | Weapon buy reads `SHOP_INVENTORY["weapon"]`; `equip_weapon` reuses `game.equip_item(...)` and runtime equipment state. Armor, upgrades, comparison, unequip, and generic slots remain closed. | Medium. Weapon path is reusable; broader equipment and crafting-upgrade paths are still MVP-scoped gaps. | Add armor buy or upgrade display as separate small gates. Generic equipment management needs its own planning gate. |
| Magic shop | `learn_magic_book` validates `MAGIC_BOOKS`, `SKILLS`, job, level, gold, materials, and learned state server-side. ScreenModel still uses a fixed book id list. | Low to medium. Mutation action is reusable; presentation list is narrower than CLI data. | Iterate `MAGIC_BOOKS` in the model before adding more books. No one-book-per-MVP pattern is needed. |
| World map / dungeon / exploration / combat | World Map iterates `DUNGEONS` and runtime unlocks; `confirm_travel`, `advance_step`, combat, retreat, route clear, item rows, and skill rows are shared flow pieces. | Medium. Multiple dungeons can route through the bridge, but complete dungeon events, boss framework, and combat formula changes remain closed. | Treat existing dungeons as coverage follow-up unless the task opens boss / special event behavior. |
| Guild | Current GUI bridge is dungeon clear report registration from `DUNGEONS`. It does not implement the CLI `QUESTS` turn-in, reward, unlock, or story inquiry system. | High for QUESTS. This is not a generic guild quest bridge yet. | Guild QUESTS coverage needs a separate small MVP gate. Do not bundle it into facility entry or dungeon coverage work. |
| Inventory / backpack / equipment | World Map utility preview reads runtime inventory plus currently equipped equipment. Workshop weapon equip is the only current live equip action. | Medium. Display is reusable; equipment mutation remains weapon/workshop-specific. | More item display is coverage; generic equip / unequip / slot management requires its own gate. |
| Bestiary | Preview reads runtime `state["bestiary"]` and monster data, so more registered monsters naturally display. | Low. Mostly a summary presentation surface. | Add detail / filtering as coverage work, not one-monster MVPs. |

Explicit exceptions that are not yet fully bridged system families:

- Guild `QUESTS` turn-in / reward / unlock flow.
- Complete crafting / synthesis, including `craft_recipe`.
- Generic equipment management beyond workshop weapon equip.

Town Hub Mira result after this audit:

- Town Hub Mira / 米菈合成屋 Entry Unlock Live MVP is complete in the working
  tree and pending commit.
- Scope is only the Town Hub synthesis facility node reflecting
  `is_unlocked(state, "shop_synthesis_01")` as locked / unlocked.
- This slice is not a complete synthesis shop, not a recipe bridge, not a craft
  action, and not a `synthesis_screen_model()` or live loader task.
- It must not add or modify recipes, quests, dungeons, schema, save behavior,
  combat formulas, or the crafting system.
- Next synthesis follow-up candidate is a single existing recipe live bridge MVP,
  or an even smaller read-only gate first; it is not pre-approved.

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
- `submit_quest` / `report_dungeon_clear` -> guild clear report registration helper
  for the narrow Guild Report MVP only.

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
