# GUI HTML Static Prototype Progress V1

Purpose: handoff note for the current HTML static prototype work. This file records what is already built, what UI decisions were accepted, what remains out of scope, and the recommended next entry point.

Date: 2026-05-19
Status: static prototype progress note
Last updated: 2026-05-22

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

- Loads static fixtures only.
- Renders Guild title/subtitle, receptionist area, task filters, task list, story hint card, task detail, reward summary, condition rows, feedback bar, primary action, back action, and UIAction log.
- Task filters are UI-only: `all`, `ready_to_submit`, `completed`.
- Selecting a task renders its detail, reward, conditions, feedback, and primary action state.
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

- Runtime adapter.
- Real task data adapter.
- Real image or formal NPC asset.
- Final keyboard navigation graph.

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

- Loads static fixtures only.
- Renders top player/resource strip, full-width programmatic map placeholder, route lines, clickable location nodes, right-side location detail drawer, primary confirm action, fixture selector, and UIAction log.
- Top-left menu button opens a left-side main menu drawer.
- Main menu actions log UIAction events only.
- Main menu includes `back_to_start_screen`, which writes UIAction log before navigating back to the Start Screen static prototype.
- Main menu no longer includes `exit_game` / `離開遊戲`; this static-only action duplicated the return-to-title purpose.
- Initial World Map view keeps the detail drawer closed so the map can use the full main width.
- Clicking a map node logs `select_world_location` and opens/updates the right-side detail drawer.
- Unlocked locations allow `confirm_travel`, write the UIAction log, then navigate to the Dungeon Exploration static prototype.
- Locked locations keep the detail panel visible but block `confirm_travel` with a reason.

Accepted World Map decisions:

- Treat the supplied mockups as reference only, not runtime assets.
- Preserve the user-provided menu-open and detail-drawer mockups in `05_assets/gui_references/world_map/`.
- Main menu is opened from the top-left button as a side drawer.
- Keep return-to-title through `back_to_start_screen`; do not keep a separate static-only `exit_game` command in this prototype.
- Selecting a map point updates the right-side information panel.
- Static prototype navigation only; no runtime adapter, no runtime exploration, and no save writes.

Deferred World Map items:

- Real world map art or formal asset pipeline.
- Runtime adapter for location unlocks and travel.
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
- Town Hub `open_facility {"facility_id":"guild"}` logs before navigating to Guild Screen.
- Guild `back_to_town_hub` logs before navigating to Town Hub.
- World Map renders 9 location nodes from static fixtures.
- World Map menu drawer opens and closes.
- World Map selected location updates the right-side detail panel.
- World Map detail panel opens as a right-side drawer and can be closed.
- World Map locked locations block `confirm_travel` with a reason.
- World Map unlocked locations dispatch `confirm_travel` and navigate to Dungeon Exploration static prototype without entering runtime.
- Town Hub `open_world_map` logs before navigating to World Map.
- World Map does not expose a return-to-town control in the current mockup pass.
- Browser console error log was 0 during World Map static navigation checks.
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

## Recommended Next Step

Recommended next session entry:

```text
Review Start Screen alignment and choose the next unfinished static prototype, likely Shop or Synthesis.
```

Scope suggestion:

- Keep all prototypes static.
- Do not connect runtime.
- Do not use mockup/reference images as runtime assets.
- Keep UIAction logging before navigation.
- Preserve Start Screen, World Map, Dungeon Exploration, and Combat Screen as static fixture display only until a runtime adapter is explicitly approved.
- Do not add gameplay logic, new combat formulas, runtime adapters, or save reads/writes.

Alternative next steps:

- Review and refine the Dungeon Exploration static prototype layout before adding a runtime adapter.
- Build the next facility static prototype, likely Shop or Synthesis.
- Add a proper keyboard focus graph for Town Hub and Guild.
- Add a shared prototype shell / fixture loader after Combat Screen exists.
