# GUI HTML Static Prototype Progress V1

Purpose: handoff note for the current HTML static prototype work. This file records what is already built, what UI decisions were accepted, what remains out of scope, and the recommended next entry point.

Date: 2026-05-19
Status: static prototype progress note
Last updated: 2026-05-25

## Boundary

- Do not modify runtime, data, schema, save, or combat formulas.
- Do not read or write `save.json`.
- Do not connect the Python runtime.
- Do not start a formal asset pipeline.
- Do not treat reference images or mockup candidates as runtime backgrounds.
- Fixtures are display data for GUI validation only, not gameplay SSOT.

## Built Prototypes

```text
07_gui_prototype/
- start_screen/
  - index.html
  - styles.css
  - start-screen.js
  - fixtures/
    - start-empty.json
    - start-has-save.json
- town_hub/
  - index.html
  - styles.css
  - town-hub.js
  - fixtures/
    - town-hub-default.json
    - town-hub-alerts.json
- guild_screen/
  - index.html
  - styles.css
  - guild-screen.js
  - fixtures/
    - guild-default.json
    - guild-quest-ready.json
- synthesis_screen/
  - index.html
  - styles.css
  - synthesis-screen.js
  - fixtures/
    - synthesis-default.json
    - synthesis-constrained.json
- shop_screen/
  - index.html
  - styles.css
  - shop-screen.js
  - fixtures/
    - shop-default.json
    - shop-constrained.json
- workshop_screen/
  - index.html
  - styles.css
  - workshop-screen.js
  - fixtures/
    - workshop-default.json
    - workshop-constrained.json
- storage_screen/
  - index.html
  - styles.css
  - storage-screen.js
  - fixtures/
    - storage-locked.json
    - storage-empty.json
    - storage-filled.json
    - storage-blocked.json
- magic_shop_screen/
  - index.html
  - styles.css
  - magic-shop-screen.js
  - fixtures/
    - magic-shop-default.json
    - magic-shop-discount.json
    - magic-shop-constrained.json
    - magic-shop-learned.json
- world_map/
  - index.html
  - styles.css
  - world-map.js
  - fixtures/
    - world-map-default.json
    - world-map-frontier-alerts.json
- dungeon_exploration/
  - index.html
  - styles.css
  - dungeon-exploration.js
  - fixtures/
    - dungeon-exploration-default.json
    - dungeon-exploration-encounter.json
- combat_screen/
  - index.html
  - styles.css
  - combat-screen.js
  - fixtures/
    - combat-command-default.json
    - combat-danger-state.json
    - combat-result-victory.json
    - combat-result-defeat.json
    - combat-result-retreat.json
```

## Start Screen Prototype

Location:

```text
07_gui_prototype/start_screen/
```

Current behavior:

- Loads static fixtures only.
- Renders the game title, hero copy, centered primary action buttons, fixture selector, and UIAction log.
- The former central save-state / summary information card has been removed.
- No-save fixture aligns with CLI `start_screen_panel(has_save=False)`: only `start_new_game` is offered, labelled as `開始新冒險（New Game）`.
- Has-save fixture aligns with CLI `start_screen_panel(has_save=True)`: `load_game` is offered as `繼續冒險（Continue）`, and `restart_game` is offered as `重新開始（New Game）`.
- `start_new_game` and `restart_game` open an in-screen modal dialog for the CLI `new_game()` data entry step.
- The modal dialog includes adventurer name input, four initial job cards (`劍士`, `法師`, `盜賊`, `牧師`), guidance text, return, and confirm.
- The modal uses a full-screen dark overlay with light blur, blocks background interaction, and closes from the return action or backdrop.
- Confirming the modal writes the final `start_new_game` or `restart_game` UIAction, then navigates to the World Map static prototype.
- `load_game` writes UIAction log before navigating to the World Map static prototype.
- Save presence is fixture data only; the prototype does not read or write `save.json`.

Accepted Start Screen decisions:

- Start Screen V1 is accepted as a minimal entry surface, not a standalone character creation screen.
- Keep Start Screen as a single screen; the adventurer registration step is an overlay modal component, not a new page.
- Keep the central surface focused on primary actions only; do not show character, location, resource, or recent-progress summary cards in the center.
- Treat existing save / no-save states as static fixtures.
- Navigation from Start Screen enters World Map only; no runtime adapter is connected.
- User-provided Start Screen mockups are accepted as panel layout references only, not visual-language requirements and not runtime assets.
- Start Screen reference files live under `05_assets/gui_references/start_screen/`.

Deferred Start Screen items:

- Runtime save detection or save-load adapter.
- Real character creation / `new_game()` adapter.
- Multiple save slots, settings, exit-game handling, or account-login semantics.
- Real title art, animation, video, or formal asset pipeline.

## Town Hub Prototype

Location:

```text
07_gui_prototype/town_hub/
```

Current local preview during this session:

```text
http://127.0.0.1:8765/
```

Current behavior:

- Loads static fixtures only.
- Renders title, subtitle, resource strip, town guidance, facility nodes, navigation, and UIAction log.
- Facility nodes support hover, selected/focus outline, badge, disabled state, and disabled reason.
- Clicking a facility node logs `open_facility`.
- Disabled facility nodes log blocked `open_facility` with a reason.
- World map remains as the only non-facility navigation action.
- UIAction log is visible for prototype debugging.

Accepted Town Hub decisions:

- Remove the right-side selected facility detail panel.
- Facility entry should happen directly from the facility node.
- Remove global actions from Home Town Hub for now.
- Keep only world map navigation in this prototype.
- Keep simple selected/focus outline for keyboard accessibility.
- Do not solve scalable town layout yet.
- Do not solve final directional keyboard navigation yet.

Deferred Town Hub items:

- Direction-key focus graph that follows visual positions.
- Including world map in the same direction-key navigation graph.
- Scalable layout for future facilities such as tavern, weapon shop, armor shop.
- Static fake transition from Town Hub to facility screens.

## Guild Screen Prototype

Location:

```text
07_gui_prototype/guild_screen/
```

Current local preview during this session:

```text
http://127.0.0.1:8766/
```

Current behavior:

- Loads static fixtures by default and supports the approved local live bridge mode.
- Renders Guild title/subtitle, receptionist area, resource strip, task /
  material-sell mode tabs, task filters, task list, story hint card, sellable
  material list, task or material detail, reward / expected-Gold summary,
  conditions / confirmation, feedback bar, primary action, back action, and
  UIAction log.
- Task filters are UI-only: `all`, `ready_to_submit`, `completed`.
- Selecting a task renders its detail, reward, conditions, feedback, and primary action state.
- Material-sell mode lists existing owned Guild-buyback materials, supports
  quantity controls and explicit confirmation, and dispatches
  `sell_guild_material` in live mode.
- Ready tasks dispatch `submit_quest`.
- Missing or completed tasks block the primary action and show/log the unavailable reason.
- Story hint dispatches `open_story_hint`.
- Back action dispatches `back_to_town_hub`.

Accepted Guild decisions:

- Guild Screen V1 is a quest board / unlocked quest browser, not an accept-quest system.
- Do not include `accept_quest` or `active_quests`.
- Story hint is a special interaction card, not a formal quest and not counted by filters.
- Receptionist area belongs on the right side on desktop.
- Receptionist region should be about 1.2x wider than the first pass.
- Receptionist image placeholder uses a fixed `3:4` ratio.
- Long content areas use internal scrolling instead of stretching layout.
- Main task detail region uses a 55% / 45% vertical split:
  - top: task/story main information
  - bottom: reward and condition sections

Deferred Guild items:

- Real image or formal NPC asset.
- Final keyboard navigation graph.
- Guild features beyond the existing report, quest turn-in, Boss Glen,
  fire-mark inquiry, and material-buyback bridge coverage.

## Synthesis Screen Prototype

Location:

```text
07_gui_prototype/synthesis_screen/
```

Current behavior:

- Loads static fixtures only.
- Renders Synthesis title/subtitle, category tabs, recipe list, selected recipe detail, output summary, NPC/workshop presence, requirement/status rows, feedback bar, primary craft action, back action, and UIAction log. The resource strip remains fixture-backed but is hidden in the accepted base layout.
- Category tabs are UI-only: `all`, `equipment`, `battle`, labelled as `全部`, `裝備`, and `戰術道具`.
- Selecting a category dispatches `select_category`, filters the recipe list, and selects the first visible recipe.
- Selecting a recipe dispatches `select_recipe`, then updates detail, output summary, requirements, feedback, and primary action state.
- Default fixture covers a craftable state with four current synthesis recipes: `recipe_fire_cloak`, `recipe_focus_pouch`, `recipe_heat_charm`, and `recipe_piercing_bundle`.
- Constrained fixture covers missing-gold, missing-material, and missing-base-equipment states.
- Enabled `craft_recipe` writes UIAction log and updates static feedback only; it does not consume gold, materials, base equipment, or produce items.
- Disabled `craft_recipe` writes blocked UIAction log with `disabled_reason` and updates static feedback.
- `back_to_town_hub` writes UIAction log before navigating to the Town Hub static prototype.
- Town Hub `open_facility {"facility_id":"synthesis"}` now writes UIAction log before navigating to Synthesis Screen.
- Base layout tuning pass moved Synthesis Screen toward a facility decision layout:
  - the standalone player/resource strip is hidden so it no longer occupies a full row
  - the center recipe detail card is reduced to the core recipe name, category/status, short description, effect, and brief disabled reason
  - requirement rows moved from the right side into the center decision area under the recipe detail
  - the right side is now a larger Mira/NPC portrait presence area with only a small identity label
  - the bottom feedback/action bar remains the primary place for Mira/system guidance and craft availability feedback
  - UIAction Log remains available as a collapsed debug-only panel by default
- Follow-up layout tuning adjusted the center decision area so the upper recipe detail panel is larger than the lower requirement panel, and requirement rows render as full-width strips rather than button-like tiles.
- User review accepted the current Synthesis Screen static prototype base layout on 2026-05-23. Future adjustments are deferred until the formal bridge or UI image/portrait asset insertion reveals a concrete issue.

Accepted Synthesis decisions:

- Synthesis Screen V1 is a Facility list-detail-requirement-confirm-result validation surface.
- Treat fixture values as GUI display data only, not gameplay SSOT.
- Use programmatic HTML/CSS visuals only; existing Synthesis mockups remain reference history, not runtime or prototype backgrounds.
- Keep categories aligned with CLI Synthesis Catalog MVP: all, equipment, and battle/tactical items.
- Keep primary action as static UIAction logging; do not copy runtime synthesis rules into JS.
- Treat the current base layout as settled for prototype purposes; do not keep tuning it unless a later bridge or visual asset integration pass exposes a problem.

Deferred Synthesis items:

- Runtime adapter for `craft_menu()` / recipe state.
- Real inventory, gold, equipment, or save mutation.
- Real NPC art, item icons, material icons, or formal asset pipeline.
- Batch crafting, selling, recipe expansion, or final keyboard focus graph.

## Shop Screen Prototype

Location:

```text
07_gui_prototype/shop_screen/
```

Current behavior:

- Loads static fixtures only.
- Renders Shop title/subtitle, category tabs, item list, selected item detail, shopkeeper presence, price / owned / stock display, feedback bar, primary buy action, back action, and UIAction log.
- Default fixture covers purchasable travel shop items such as consumables, tactical items, and accessories.
- Constrained fixture covers blocked purchase states such as missing gold, locked stock, or unavailable items.
- Selecting a category dispatches `select_category`; selecting an item dispatches `select_item`.
- Enabled `buy_item` writes UIAction log and static feedback only; it does not consume gold, change inventory, or update stock.
- Disabled `buy_item` writes blocked UIAction log with `disabled_reason` and static feedback.
- `back_to_town_hub` writes UIAction log before navigating to the Town Hub static prototype.
- Town Hub `open_facility {"facility_id":"travel_shop"}` routes to `../shop_screen/index.html`.

Accepted Shop decisions:

- Shop Screen V1 is a Facility list-detail-price-confirm-feedback validation surface.
- Treat fixture values as GUI display data only, not gameplay SSOT.
- Keep primary action as static UIAction logging; do not copy runtime shop rules into JS.
- Keep category meaning aligned with CLI Travel Shop Catalog MVP: all goods, consumables, tactical items, and accessories.

Deferred Shop items:

- Shop sell, generic quantity selection, economy tuning, or broader Shop runtime
  behavior beyond the landed travel-inventory purchase coverage.
- Shop live extra top spacing from the unused `resource_strip` was corrected in
  `2ecca91`. Shopkeeper naming / copy alignment remains presentation polish only.
- Batch buying, final shop economy tuning, item icons, NPC art, or formal asset pipeline.
- Final keyboard focus graph.

## Workshop Screen Prototype

Location:

```text
07_gui_prototype/workshop_screen/
```

Current behavior:

- Supports static fixture fallback and approved live mode for Workshop Buy Weapon Live MVP.
- Static mode renders Workshop title/subtitle, player/equipment summary, buy and upgrade tabs, equipment or recipe list, selected detail, requirement/status rows, feedback, primary action, back action, and UIAction log.
- Live mode loads a runtime-shaped workshop ScreenModel and currently exposes weapon purchase only; `armors` and `upgrades` are intentionally empty for the MVP.
- Default fixture covers a normal warrior-like state with enough gold/materials for buying or upgrading.
- Constrained fixture covers low-gold, missing-material, job-restricted, and locked/unavailable states.
- Selecting a tab dispatches `select_tab`; selecting equipment dispatches `select_item`; selecting an upgrade recipe dispatches `select_recipe`.
- In static mode, enabled `buy_equipment` and `upgrade_equipment` write UIAction log and static feedback only; they do not consume gold/materials, change equipment, or mutate inventory.
- In live mode, `buy_equipment` dispatches to Python server-side gameplay authority and renders the returned ScreenModel.
- Blocked states write `blocked_action` with the intended action and reason.
- `back_to_town_hub` writes UIAction log before navigating to the Town Hub static prototype.
- Town Hub `open_facility {"facility_id":"workshop"}` routes to `../workshop_screen/index.html`.

Accepted Workshop decisions:

- Workshop Screen V1 is a Facility buy/upgrade-detail-requirement-confirm-feedback validation surface.
- Treat fixture values as GUI display data only, not gameplay SSOT.
- Keep static primary actions as UIAction logging; in live mode, JavaScript dispatches UIAction payloads and renders returned ScreenModels only.
- Python remains gameplay authority for live weapon purchase validation, Gold deduction, and inventory mutation.
- Keep the prototype focused on equipment purchase and upgrade readability, not economy or data changes.

Deferred Workshop items:

- Armor sales, upgrade execution, equipment changing / GUI equipment management, and broader inventory-equipment workflows.
- Workshop stat label localization / presentation polish, such as `accuracy +3`.
- Any broader workshop / equipment / shop framework work.
- Real equipment icons, blacksmith/NPC art, animation, or formal asset pipeline.
- Final keyboard focus graph.

## Storage Screen Prototype

Location:

```text
07_gui_prototype/storage_screen/
```

Current behavior:

- Loads static fixtures only.
- Renders Storage title/subtitle, player resources, capacity bar ("容量: N / 10") with status badge, left Backpack item list with category tabs, right Warehouse list showing exactly 10 slots (occupied rows, empty slots `[ 空置保管欄位 ]`, locked placeholders `🔒 保管欄位鎖定`), center Transfer Action Panel, feedback atmospheric bar, primary/secondary action buttons, and UIAction log.
- Supports four JSON fixtures: `storage-locked.json` (unopened state), `storage-empty.json` (unlocked but empty), `storage-filled.json` (normal storage usage), and `storage-blocked.json` (low-gold or key item storage block details).
- Clicking Backpack list row logs `select_inventory_item` and opens center panel for simulated "deposit" transfer.
- Clicking Warehouse list row logs `select_storage_item` and opens center panel for simulated "withdraw" transfer.
- Center panel combines selected item name, usage description, transfer mode badge ("存入倉庫 ➔" or "🠔 取出背包"), quantity stepper controls (`-`, `+`, `MAX` buttons), and the primary "確認轉移/存入/取出" confirm button.
- Bottom primary action buttons are dynamic: triggers simulated `unlock_storage` (500G) when locked, or shows disabled `upgrade_storage` (disabled placeholder) when unlocked.
- Bottom feedback bar acts as the main JRPG receptionist dialogue interface: prints receptionist Noah's custom welcomes, guidelines, and warning feedbacks.
- Back action dispatches `back_to_town_hub` and returns to Town Hub static prototype.

Accepted Storage decisions:

- Storage Screen V1 is a JRPG 3-Column Dual-List horizontal transfer panel, not an in-backpack menu.
- Keep the middle column clean by removing redundant NPC avatars or duplicate grids; NPC portrait assets and roles are completely unified under the bottom feedback bar interface.
- Warehouse items must always render exactly 10 slots (visual cap matching JRPG constraints), cleanly displaying populated, empty placeholder, and locked rows.
- Quantity adjustment must utilize stepper buttons (`-`, `+`, `MAX`) directly in the center detail panel, rather than popover overlays.

Deferred Storage items:

- Real storage expansion or vault upgrades beyond level 1.
- Runtime state updates mapping back to `save.json`.
- Automatic item categorization beyond basic tabs.
- Keyboard navigation focus grid for transfer columns.

## Magic Shop Screen Prototype

Location:

```text
07_gui_prototype/magic_shop_screen/
```

Current behavior:

- Static mode loads fixtures only; live mode now has a narrow runtime bridge handoff for `learn_magic_book`.
- Renders Magic Shop title/subtitle, left-side Spellbook list with categories, center Scroll Detail card with item/gold requirements, right-side Eve's NPC Observatory portrait card, bottom feedback atmospheric bar, primary buy/learn action, back action, and UIAction log.
- Category tabs are aligned with the CLI Magic Shop Catalog MVP: `全部`, `攻擊魔法`, `恢復魔法`, `輔助魔法`, `特殊魔法`.
- Spellbook rows render status badges dynamically: `已學會` (gold), `可學習` (green), `等級不足` (red/gray), `素材不足` (red/gray).
- Selecting a spellbook details its spell name, MP cost, job requirements, level conditions, and price.
- If `quest_magic_crystal` is completed, book spark price drops by 50G (150G -> 100G) and prints custom Eve welcome text.
- In static fixture mode, enabled `learn_magic_book` writes UIAction log and static feedback only; it does not subtract gold/materials or learn active runtime skills.
- In live mode, `b59fe43 [antig] feat(gui): add magic shop learn book live bridge` dispatches `learn_magic_book` through the runtime bridge, renders the returned ScreenModel, and preserves static fixture fallback.
- Bottom feedback bar acts as Eve's communication channel (e.g. `伊芙：「願星辰指引你的靈魂，冒險者。」`).
- Back action dispatches `back_to_town_hub` and returns to Town Hub.

Accepted Magic Shop decisions:

- Magic Shop Screen V1 is a Facility Spellbook list-detail-requirement-learn validation surface.
- Keep color accent unified under a high-fidelity magenta/purple arcane theme (`var(--accent-magenta)`).
- Renders requirements as full-width strip rows under the detail panel, complying with Synthesis Screen layout structure.
- Renders Eve's illustration inside a dedicated right-hand portrait area with a standard JRPG aspect ratio.

Deferred Magic Shop items:

- Complete magic shop system, formal magic / skill framework, target selection, combat formula / skill rebalance, generic facility framework, and broader inventory / equipment / shop system.
- Real spellbook/magic icons or observatory background animations.
- Selling magic books, multiple spell slots, or advanced magic schools.

## World Map Prototype

Location:

```text
07_gui_prototype/world_map/
```

Reference images:

```text
05_assets/gui_references/world_map/world_map_visual_reference_v1_user_mockup_menu_open.png
05_assets/gui_references/world_map/world_map_visual_reference_v1_user_mockup_detail_drawer.png
```

Current behavior:

- Supports the existing static fixture mode and approved live bridge mode; the
  fullscreen presentation pass does not change runtime authority or action
  semantics.
- Renders a fullscreen desktop map stage using the screen-local
  `assets/world-map-environment-v01.jpg` environment image.
- Uses a floating top-left menu control and floating player/resource HUD over the
  map rather than reserving a separate top layout row.
- Uses simplified location emblems with hover / selected labels. Existing route
  rendering remains in the prototype layer but is visually hidden in the
  current presentation.
- Keeps the fixture selector and UIAction Log available only when `?debug=1` is
  present; normal player-facing URLs hide the prototype debug panel.
- Top-left menu button opens a left-side main menu drawer.
- In static mode, main menu actions log UIAction events without runtime
  mutation.
- Main menu includes `back_to_start_screen`, which writes UIAction log before
  navigating back to the Start Screen static prototype.
- Main menu no longer includes `exit_game` / `離開遊戲`; this static-only action duplicated the return-to-title purpose.
- Initial World Map view keeps the detail drawer closed so the map can use the full main width.
- Clicking a map node logs `select_world_location` and opens/updates the right-side detail drawer.
- In static mode, unlocked locations allow `confirm_travel`, write the UIAction
  log, then navigate to the Dungeon Exploration static prototype.
- Locked locations keep the detail panel visible but block `confirm_travel` with
  a reason in both presentation modes.

Accepted World Map decisions:

- Treat the supplied mockups as reference only, not runtime assets.
- Preserve the user-provided menu-open and detail-drawer mockups in `05_assets/gui_references/world_map/`.
- Treat `07_gui_prototype/world_map/assets/world-map-environment-v01.jpg` as a
  screen-local prototype presentation asset. It does not open a formal asset
  pipeline or become runtime/gameplay authority.
- Use the map as the fullscreen desktop stage, with dynamic HUD, location nodes,
  drawers, text, and interactions rendered by HTML/CSS/JS above it.
- Hide prototype debug controls from normal player-facing URLs and expose them
  through `?debug=1`.
- Main menu is opened from the top-left button as a side drawer.
- Keep return-to-title through `back_to_start_screen`; do not keep a separate static-only `exit_game` command in this prototype.
- Selecting a map point updates the right-side information panel.
- The presentation checkpoint does not change existing static/live bridge
  actions, runtime validation, save behavior, or gameplay authority.

World Map static-mode main menu read-only classification:

- Keep as current static prototype navigation:
  - `back_to_start_screen`: keep as the accepted return-to-title path; it writes UIAction log before navigating to Start Screen.
- Keep as semantic GUI actions, but only as fake interactions in the current static prototype:
  - `view_status`: CLI already has character/status meaning, but no GUI Status Screen or runtime adapter is connected yet.
  - `open_inventory`: CLI already has inventory/equipment meaning, but no GUI Inventory Screen or runtime adapter is connected yet.
  - `open_bestiary`: CLI already has bestiary meaning, but no GUI Bestiary Screen or runtime adapter is connected yet.
  - `save_game`: static prototype may show/log the action or a blocked state, but must not read or write `save.json`.
  - `open_settings`: static prototype may show/log the action, but no formal Settings Screen exists yet.
- Future handling:
  - Status, inventory/equipment, bestiary, settings, and save all need a formal screen and/or runtime adapter before doing real work.
  - `exit_game` should not be reintroduced into the World Map static prototype; `back_to_start_screen` replaces the duplicate static-only return-to-title purpose.

Deferred World Map items:

- Formal World Map asset pipeline or additional environment / location art set.
- Expansion beyond the existing approved World Map live bridge.
- Final animation for the side drawer.
- Keyboard focus graph for map nodes.

## Dungeon Exploration Prototype

Location:

```text
07_gui_prototype/dungeon_exploration/
```

Current local preview during this session:

```text
http://127.0.0.1:8767/dungeon_exploration/index.html
```

Reference image:

```text
05_assets/gui_references/dungeon_exploration_screen/dungeon_exploration_visual_reference_v1_user_mockup_main.png
```

Current behavior:

- Loads static fixtures only.
- Renders a compact title/subtitle header, HP/MP resource strip, enlarged dungeon scene placeholder, left-side dungeon summary overlay, right-side exploration status panel, narrative message, bottom action bar, fixture selector, and UIAction log.
- The right-side exploration status panel is CLI-aligned: current step meter, three compact status chips, current-run reward summary, and the latest event only.
- The visible bottom action bar only shows CLI exploration actions: advance and retreat.
- Default fixture covers ordinary step-based exploration in Ash Valley.
- Fixed Encounter Preview fixture covers a static prototype-only dangerous step without presenting a strong pre-encounter confirmation UI.
- `advance_step` and `retreat` only write UIAction log and update the prototype feedback message.
- `retreat` writes UIAction log, updates the prototype feedback message, then navigates back to the World Map static prototype.
- In the Fixed Encounter Preview fixture, `advance_step` with prototype-only `encounter_hint` writes UIAction log, then navigates to `../combat_screen/index.html`.

Accepted Dungeon Exploration decisions:

- Treat the supplied dungeon exploration mockup as visual/layout reference only, not a runtime asset.
- Use a programmatic scene placeholder instead of the reference image as a background.
- Keep the central dungeon scene as the main stage.
- Keep the current step, HP/MP, current-run rewards, latest event, and narrative text rendered by the prototype layer.
- Do not show total money, a full inventory list, exploration-time inventory/status actions, or return-to-world-map as Dungeon Exploration commands until the CLI supports those commitments.
- Do not implement random events, real step advancement, reward calculation, combat trigger logic, or runtime adapters.
- Treat Fixed Encounter Preview as test fixture data only; the final gameplay expectation remains random encounter logic inside the future runtime flow.

Deferred Dungeon Exploration items:

- Runtime adapter for dungeon state.
- Real dungeon background art or formal asset pipeline.
- Final keyboard focus graph for exploration actions.

## Combat Screen Prototype

Location:

```text
07_gui_prototype/combat_screen/
```

Current local preview during this session:

```text
http://127.0.0.1:8767/combat_screen/index.html
```

Reference image:

```text
05_assets/gui_references/combat_screen/combat_screen_visual_reference_v1_user_mockup_command.png
```

Current behavior:

- Loads static fixtures only.
- Renders a compact title/subtitle header, combat resource strip, enlarged battlefield placeholder, top enemy HUD, lower-left player HUD, right-side Battle Log panel, bottom command bar, fixture selector, and UIAction log.
- Default command fixture covers a normal player decision state.
- Danger fixture covers low HP/MP, disabled skill submenu items, and a longer Battle Log.
- Victory / Defeat / Retreat Result Preview fixtures cover static prototype-only terminal combat states.
- `basic_attack`, `open_skill_menu`, `open_item_menu`, `use_skill`, `use_item`, `defend`, and `retreat` only write UIAction log and update prototype feedback.
- Result Preview fixture actions may include `opens_result: true`; those actions write UIAction log, then open the in-screen Combat Result overlay.
- The bottom command bar is a single battle-action row: attack, skill, item, defend, and flee.
- Skill and item commands open an in-screen floating popover submenu; submenu selection records static `use_skill` / `use_item` UIAction only.
- The skill/item popover has no internal return button; pressing the active Skill or Item command a second time closes the popover.
- The submenu does not occupy layout flow: wide layout anchors it above the command row, while stacked/narrow layout keeps it near the command controls without covering Battle Log or pushing the command bar.
- Combat Result is integrated as a central terminal overlay inside Combat Screen, not a separate prototype page.
- When the Result overlay is open, the command bar remains visible but disabled; the overlay has no close/back-to-combat action.
- Result overlay next actions write UIAction log before navigating: victory/retreat return to Dungeon Exploration, defeat returns to Town Hub.
- Result overlay no longer repeats the next-step navigation as a result row; the bottom overlay button is the sole next-step control.
- Result overlay result rows stay limited to direct battle/result data; defeat and retreat previews do not include extra static-only status/carryover explanation rows.
- The command bar no longer includes `view_battle_log` or `back_to_exploration`.
- The Combat Screen no longer shows gold in the top combat resource strip.
- The Combat Screen no longer shows the separate round card, previous-action summary card, enemy detail panel, or player detail panel.
- The Combat Screen fixtures no longer depend on unused `round`, player item/effect summary, enemy weakness/intent/threat, or standalone last-action fields.
- The Battle Log has a side-panel expand/collapse control and is not a bottom command.
- Desktop mockup-alignment pass moved Combat Screen toward a HUD-over-battlefield composition:
  - the battlefield placeholder is now the full main stage rather than a card in a page grid
  - compact prototype header sits as a top HUD overlay
  - the former top-left resource strip was removed; only a small round chip remains above the enemy HUD
  - enemy focus HUD is top-centered
  - player focus and Battle Log render as left/right floating panels
  - the five bottom commands render as a larger command deck over the lower battlefield area
  - UIAction Log remains available as a compact prototype/debug panel below the main stage
- The battlefield placeholder gained additional programmatic depth/silhouette treatment; no reference/mockup image is used as a runtime or prototype background asset.

Accepted Combat Screen decisions:

- Treat the supplied combat mockup as visual/layout reference only, not a runtime asset.
- Keep the battlefield as the main visual stage.
- Keep enemy name, enemy HP, round count, player HP/MP, command labels, submenu labels, and Battle Log text rendered by the prototype layer.
- Battle Log remains readable in a side panel and does not cover the command controls.
- Per review, Battle Log stays as a side display panel but is not a bottom command.
- Do not implement damage calculation, enemy turn advancement, flee checks, animations, effects, runtime adapters, or combat formulas.
- Treat skill and item submenus as static fixture display only; selecting an entry does not consume MP/items, change HP, or advance turns.
- Treat Combat Result overlay data as fixture display only; it does not calculate, award, consume, save, or resolve combat.

Deferred Combat Screen items:

- Runtime adapter for combat state.
- Real combat background/enemy art or formal asset pipeline.
- Target selection and final keyboard focus graph.

## Verification Notes

Validated during this session:

- Start Screen fixtures parse as UTF-8 JSON.
- Start Screen JS and World Map JS pass syntax check with the bundled Node.js runtime.
- Start Screen no-save fixture renders only `start_new_game`.
- Start Screen has-save fixture renders `load_game` and `restart_game`.
- Start Screen central surface renders only primary action buttons and no longer renders the save-state / summary information card.
- Start Screen no-save `start_new_game` opens the adventurer registration modal.
- Start Screen has-save `restart_game` opens the adventurer registration modal.
- Start Screen modal renders name input, four initial job cards, return, and confirm actions.
- Start Screen modal closes from return and backdrop.
- Start Screen modal confirm writes `start_new_game` / `restart_game` UIAction and navigates to World Map static prototype.
- Start Screen `load_game` logs before navigating to World Map static prototype.
- World Map `back_to_start_screen` menu action logs before navigating to Start Screen static prototype.
- World Map main menu fixtures no longer contain `exit_game` / `離開遊戲`.
- Town Hub fixtures parse as UTF-8 JSON.
- Guild fixtures parse as UTF-8 JSON.
- Town Hub renders 9 facility nodes.
- Town Hub world map logs `open_world_map`.
- Town Hub disabled nodes log blocked actions.
- Guild default fixture renders filters, task rows, detail, rewards, conditions, feedback, and primary action.
- Guild quest-ready fixture renders story hint and dispatches `open_story_hint`.
- Guild ready tasks dispatch `submit_quest`.
- Guild unavailable states block primary action with a reason.
- Guild right-side receptionist layout and 55/45 detail split were accepted by the user.
- Guild material-sell mode landed in `2ecca91`: task / sell tabs, registered
  material rows, quantity controls, expected Gold, explicit confirmation, live
  `sell_guild_material` dispatch, and refreshed ScreenModel rendering.
- Guild task-list internal scrolling was restored in `2ecca91`.
- Town Hub `open_facility {"facility_id":"guild"}` logs before navigating to Guild Screen.
- Guild `back_to_town_hub` logs before navigating to Town Hub.
- World Map fullscreen presentation checkpoint landed in `e12cab6`: the
  screen-local environment image fills the desktop stage, the menu and
  player/resource HUD float over the map, location nodes use simplified hover /
  selected presentation, and the debug panel is hidden unless `?debug=1` is
  present.
- World Map renders 9 location nodes from static fixtures.
- World Map menu drawer opens and closes.
- World Map selected location updates the right-side detail panel.
- World Map detail panel opens as a right-side drawer and can be closed.
- World Map locked locations block `confirm_travel` with a reason.
- World Map unlocked locations dispatch `confirm_travel` and navigate to Dungeon Exploration static prototype without entering runtime.
- Town Hub `open_world_map` logs before navigating to World Map.
- World Map town-node detail action provides the existing return-to-town path.
- Browser console error log was 0 during World Map static navigation checks.
- World Map JavaScript syntax check passed for the `e12cab6` presentation
  checkpoint, and owner visual review accepted the current fullscreen World Map
  adjustment.
- Dungeon Exploration fixtures parse as UTF-8 JSON.
- Dungeon Exploration JS and World Map JS pass syntax check with the bundled Node.js runtime.
- Dungeon Exploration default fixture renders 2 visible action buttons, Ash Valley location data, step meter, compact current-run rewards, latest event preview, and UIAction log.
- Dungeon Exploration default fixture dispatches `advance_step` and updates the narrative feedback message without changing fixture state.
- Dungeon Exploration Fixed Encounter Preview fixture renders 2 visible action buttons: `advance_step` and `retreat`.
- Dungeon Exploration Fixed Encounter Preview fixture `advance_step` logs before navigating to Combat Screen static prototype.
- World Map `confirm_travel` logs before navigating to Dungeon Exploration static prototype.
- Browser console error log was 0 during Dungeon Exploration static checks.
- Dungeon Exploration browser DOM check confirmed left dungeon overlay, right exploration status panel, bottom action row, and 591px desktop stage height.
- Dungeon Exploration browser DOM check confirmed the red-marked bottom actions are no longer visible, the action row width is constrained to the left command area, and the green-marked right panel is summarized.
- Dungeon Exploration browser DOM check confirmed the CLI-aligned surface: HP/MP only in the resource strip, no `1957G`, no item summary panel, no inventory/status/world-map commands, no strong encounter prompt wording, current-run rewards, latest event, and advance/retreat only.
- Dungeon Exploration Fixed Encounter Preview fixture browser check confirmed `advance_step` still navigates to `../combat_screen/index.html`.
- Dungeon Exploration `retreat` action browser check confirmed navigation to `../world_map/index.html` from both Default Exploration and Fixed Encounter Preview fixtures.
- Dungeon Exploration visual tune-up confirmed the fixture selector labels the combat-transition fixture as `Fixed Encounter Preview`.
- Dungeon Exploration screenshot capture in the in-app browser timed out after layout and interaction checks; DOM and console checks were still completed.
- Glen Boss flow UX cleanup landed in `709dc6c`: Dungeon Exploration live mode
  keeps HP/MP-only resource-strip presentation, renders the full event preview
  list with vertical scrolling and auto-scroll-to-bottom behavior, and supports a
  three-column action row so Boss challenge and leave/retreat actions keep stable
  placement.
- Guild story hint live presentation now keeps Glen / Blood Map / Act 2 guidance
  reviewable across the accepted, Glen-defeated, and follow-on progression
  states; this is ScreenModel presentation coverage, not a full story hint
  framework.
- Glen Boss flow UX cleanup Antigravity-reported checks:
  `python 06_tools/smoke_test_progression_bridge.py` PASS,
  `python element_maze.py --smoke-test` PASS, and
  `python 06_tools/validate_data.py` PASS.
- Combat Screen fixtures parse as UTF-8 JSON.
- Combat Screen JS and Dungeon Exploration JS pass syntax check with the bundled Node.js runtime.
- Combat Screen default fixture renders 5 command buttons, top enemy HUD, lower-left player HUD, right-side Battle Log, and UIAction log.
- Combat Screen default fixture dispatches `basic_attack` and updates command feedback without changing fixture state.
- Combat Screen default fixture opens a floating skill submenu from `open_skill_menu` and logs `use_skill` when a skill row is selected.
- Combat Screen default fixture opens a floating item submenu from `open_item_menu` and logs `use_item` when an item row is selected.
- Combat Screen skill/item popovers no longer show an internal `返回` button; clicking the active command button again closes the popover.
- Combat Screen danger fixture renders disabled skill submenu rows with disabled reasons.
- Combat Screen blocked submenu `use_skill` logs a blocked UIAction with reason.
- Combat Screen command bar does not include `view_battle_log` or `back_to_exploration`.
- Browser console error log was 0 during Combat Screen static checks.
- Combat Screen browser check confirmed no `1957G` in the combat resource strip and no Battle Log or return-to-exploration command in the bottom command bar.
- Combat Screen browser check confirmed the main command bar remains 5 commands and no longer shows the old Fire Mark Slash command as a main command.
- Combat Screen browser layout check confirmed the floating submenu does not overlap the command row or Battle Log on desktop or narrow viewport, and opening/closing it does not increase page height.
- Combat Screen Victory / Defeat / Retreat Result Preview fixtures render 5 command buttons before terminal action selection.
- Combat Screen result preview actions open central Combat Result overlay, disable the command bar, preserve page height, and keep console error/warning count at 0.
- Combat Screen result next actions navigate to the expected static prototype targets: victory/retreat to Dungeon Exploration, defeat to Town Hub.
- Combat Screen Victory / Defeat / Retreat Result Preview fixtures no longer show a duplicated `下一步` row inside `本場結果`; navigation remains on the bottom result action button.
- Combat Screen Defeat / Retreat Result Preview fixtures no longer show extra `角色狀態` or `本趟素材` rows inside `本場結果`.
- Manual review after the latest Combat Screen result and popover polish was reported OK; first Combat Screen mockup-alignment layout tuning pass is now complete, with any remaining work expected to be minor user-review adjustments.
- Combat Screen mockup-alignment layout tuning pass confirmed desktop 1280x720 geometry with no page scroll and no overlap between top HUDs, enemy HUD, player HUD, right Battle Log, bottom command deck, or compact UIAction Log.
- Combat Screen skill and item popover geometry confirmed no overlap with the command row or Battle Log after the mockup-alignment layout pass.
- Combat Screen responsive layout sanity checks confirmed 5 command buttons, no horizontal overflow, and no HUD/footer overlap at 1280x720, 900x900, and 390x844.
- Combat Screen item popover responsive checks confirmed desktop `above-command` placement and tablet/mobile `under-command` placement without command-row or side-panel overlap.
- Combat Screen result overlay geometry confirmed central overlay display, disabled command buttons, and unchanged no-scroll desktop layout after the mockup-alignment layout pass.
- Combat Screen round HUD revision confirmed only one `第 N 回合` chip renders from fixture data; HP/MP/player identity are no longer duplicated in the top HUD area.
- Combat Screen cache-resilience follow-up added CSS/JS query-versioning and reduced all Combat Screen `resource_strip` fixture arrays to the round chip only, so stale script instances cannot keep rendering the removed HP/MP/player top-left block after fixture changes.
- Synthesis Screen fixtures parse as UTF-8 JSON.
- Synthesis Screen JS and Town Hub JS pass syntax check with the available Node.js runtime.
- Synthesis Screen default fixture renders the planned category, recipe, detail, output, requirement, feedback, primary action, and UIAction log data surfaces.
- Synthesis Screen constrained fixture covers disabled craft actions with readable missing-gold, missing-material, and missing-base reasons.
- Town Hub `synthesis` facility now has a static prototype route to `../synthesis_screen/index.html`.
- Browser console error/warning log was 0 during Synthesis Screen static checks.
- Synthesis Screen default fixture browser check confirmed category switching dispatches `select_category`, recipe selection dispatches `select_recipe`, and enabled `craft_recipe` updates static feedback without mutating fixture counts.
- Synthesis Screen constrained fixture browser check confirmed disabled craft action exposes `aria-disabled`, and a forced click writes blocked `craft_recipe` UIAction with `disabled_reason`.
- Synthesis Screen `back_to_town_hub` browser check confirmed navigation to Town Hub static prototype.
- Town Hub `synthesis` facility browser check confirmed navigation to Synthesis Screen static prototype.
- Synthesis Screen responsive layout sanity checks confirmed no horizontal overflow, no major section overlap, and visible recipe/requirement surfaces at 1280x720, 900x900, and 390x844.
- Synthesis Screen base layout tuning pass browser check confirmed the resource strip is hidden, center recipe detail is compact, requirement rows render in the center area, the right side has no requirement rows, NPC role copy is hidden, and UIAction Log is collapsed by default.
- Synthesis Screen base layout tuning pass responsive checks confirmed no horizontal overflow, no major section overlap, hidden resource strip, centered requirement rows, no right-side requirement rows, and collapsed UIAction Log at 1280x720, 900x900, and 390x844.
- Synthesis Screen follow-up layout check confirmed the upper center detail panel is larger than the lower requirement panel, requirement rows render as single-column strip rows, and scrollbar behavior remains local/fallback-only for long lists or unusually long requirement content.
- Synthesis Screen current base layout was accepted by user review on 2026-05-23; future tuning is deferred until formal bridge work or UI image/portrait asset insertion surfaces a specific issue.
- Shop Screen static prototype v1 exists with default and constrained fixtures.
- Shop Screen dispatches `select_category`, `select_item`, `buy_item`, and `back_to_town_hub` as static UIAction events only.
- Town Hub `travel_shop` facility routes to Shop Screen static prototype.
- Shop Screen fixture notes explicitly state that buy action logging does not change player inventory or gold.
- Workshop Screen static prototype v1 exists with default and constrained fixtures.
- Workshop Screen dispatches `select_tab`, `select_item`, `select_recipe`, `buy_equipment`, `upgrade_equipment`, `blocked_action`, and `back_to_town_hub` as static UIAction events only.
- Town Hub `workshop` facility routes to Workshop Screen static prototype.
- Workshop Screen logic treats buy/upgrade success as simulated feedback only and does not mutate runtime SSOT data.
- Workshop Buy Weapon Live MVP landed in `2d99d7e [antig] feat(gui): add workshop buy weapon live bridge MVP`.
- Workshop live route dispatches `buy_equipment` to Python server-side, which validates existing weapon, workshop weapon availability, job compatibility, and Gold before deducting Gold and adding the item to inventory. It does not auto-equip.
- Workshop Weapon Equip Live MVP landed in `6abe303 [antig] feat(gui): add workshop weapon equip bridge & align backpack presentation`.
- Workshop live "owned equipment" surface can dispatch `equip_weapon` for inventory-held weapon slot items only. Python server-side validates weapon slot, inventory possession, job compatibility, and already-equipped state, then reuses `game.equip_item(...)`. Buying still does not auto-equip.
- Workshop owned aggregation and World Map backpack / equipment overlay now align around inventory equipment plus currently equipped equipment, with same-item counts merged and equipped items marked.
- Workshop live mode intentionally returns empty armor and upgrade lists for this MVP; armor, accessory, special-slot, unequip, comparison, upgrade, and full equip-management flows remain deferred.
- Storage Screen static prototype v1 exists with locked, empty, filled, and blocked fixtures.
- Storage Screen dispatches `select_category`, `select_inventory_item`, `select_storage_item`, `set_transfer_quantity`, `deposit_item`, `withdraw_item`, `unlock_storage`, and `back_to_town_hub` as static UIAction events.
- Town Hub `storage` facility node correctly routes to Storage Screen static prototype.
- Storage Screen 10-row capacity bar and visual rendering logic pass browser checks with zero console errors.
- Magic Shop Screen static prototype v1 exists with default, discount, constrained, and learned fixtures.
- Magic Shop Screen dispatches `select_category`, `select_book`, `learn_magic_book`, and `back_to_town_hub` as static UIAction events only.
- Magic Shop Screen live handoff now has a narrow `learn_magic_book` bridge through `b59fe43`; JavaScript dispatches UIAction and renders returned ScreenModel, while static fixtures remain fallback.
- Town Hub `magic_shop` facility node correctly routes to Magic Shop Screen static prototype.
- Magic Shop Screen requirements rendering and Eve's portrait card pass layout checks with zero console errors.
- Facility-family CSS convergence pass has Antigravity-reported Chrome Headless visual verification for Shop, Guild, Magic Shop, and Synthesis at desktop / laptop / short-view viewports, including 1920x1080, 1440x900, and 1366x768. The pass reports no cut-off primary buttons, missing critical text, or lost facility detail content after the CSS-only short-viewport fixes.

## Recommended Next Step

Recommended next session entry:

```text
Treat the current static prototypes and basic facility CLI-parity bridge coverage as landed through `2ecca91`. Start the next session with read-only Hot Zone catch-up, then ask the user to select one small convergence target before implementation.
```

Scope suggestion:

- Keep static fixture fallback intact while respecting already-landed approved
  live bridge slices.
- Do not use mockup/reference images as runtime assets.
- Keep UIAction logging before navigation.
- Preserve static fixture fallback across the existing prototype screens. Do not
  infer generic sell, inventory / equipment management, storage capacity
  upgrade, settings, or broader runtime work from landed bridge coverage.
- Do not add gameplay logic, new combat formulas, new runtime adapters, or save
  reads/writes without a new approved exact scope.

Alternative next steps:

- Read-only audit the remaining GUI planning docs for drift after Shop/Workshop landed.
- Review and refine a single existing static prototype only if the user points to a concrete issue.
- Add a proper keyboard focus graph for Town Hub and Guild.
- Add a shared prototype shell / fixture loader after Combat Screen exists.
