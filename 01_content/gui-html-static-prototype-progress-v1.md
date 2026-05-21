# GUI HTML Static Prototype Progress V1

Purpose: handoff note for the current HTML static prototype work. This file records what is already built, what UI decisions were accepted, what remains out of scope, and the recommended next entry point.

Date: 2026-05-19
Status: static prototype progress note
Last updated: 2026-05-21

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
```

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
- Initial World Map view keeps the detail drawer closed so the map can use the full main width.
- Clicking a map node logs `select_world_location` and opens/updates the right-side detail drawer.
- Unlocked locations allow `confirm_travel`, write the UIAction log, then navigate to the Dungeon Exploration static prototype.
- Locked locations keep the detail panel visible but block `confirm_travel` with a reason.

Accepted World Map decisions:

- Treat the supplied mockups as reference only, not runtime assets.
- Preserve the user-provided menu-open and detail-drawer mockups in `05_assets/gui_references/world_map/`.
- Main menu is opened from the top-left button as a side drawer.
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
- High-risk fixture covers a dangerous exploration step without presenting a strong pre-encounter confirmation UI.
- `advance_step` and `retreat` only write UIAction log and update the prototype feedback message.
- In the high-risk fixture, `advance_step` with `encounter_hint` writes UIAction log, then navigates to `../combat_screen/index.html`.

Accepted Dungeon Exploration decisions:

- Treat the supplied dungeon exploration mockup as visual/layout reference only, not a runtime asset.
- Use a programmatic scene placeholder instead of the reference image as a background.
- Keep the central dungeon scene as the main stage.
- Keep the current step, HP/MP, current-run rewards, latest event, and narrative text rendered by the prototype layer.
- Do not show total money, a full inventory list, exploration-time inventory/status actions, or return-to-world-map as Dungeon Exploration commands until the CLI supports those commitments.
- Do not implement random events, real step advancement, reward calculation, combat trigger logic, or runtime adapters.

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
- Danger fixture covers low HP/MP, a disabled `use_skill` command, and a longer Battle Log.
- `basic_attack`, `open_skill_menu`, `open_item_menu`, `use_skill`, `defend`, and `retreat` only write UIAction log and update prototype feedback.
- The bottom command bar is a single battle-action row: attack, skill or Fire Mark Slash fixture, item, defend, and flee.
- The command bar no longer includes `view_battle_log` or `back_to_exploration`.
- The Combat Screen no longer shows gold in the top combat resource strip.
- The Combat Screen no longer shows the separate round card, previous-action summary card, enemy detail panel, or player detail panel.
- The Battle Log has a side-panel expand/collapse control and is not a bottom command.

Accepted Combat Screen decisions:

- Treat the supplied combat mockup as visual/layout reference only, not a runtime asset.
- Keep the battlefield as the main visual stage.
- Keep enemy name, enemy HP, round count, player HP/MP, command labels, and Battle Log text rendered by the prototype layer.
- Battle Log remains readable in a side panel and does not cover the command controls.
- Per review, Battle Log stays as a side display panel but is not a bottom command.
- Do not implement damage calculation, enemy turn advancement, skill menus, item menus, flee checks, animations, effects, runtime adapters, or combat formulas.

Deferred Combat Screen items:

- Static navigation from combat command/result state to Combat Result Screen after Combat Result Screen exists.
- Runtime adapter for combat state.
- Real combat background/enemy art or formal asset pipeline.
- Skill submenu, item submenu, target selection, and final keyboard focus graph.

## Verification Notes

Validated during this session:

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
- Dungeon Exploration high-risk fixture renders 2 visible action buttons: `advance_step` and `retreat`.
- Dungeon Exploration high-risk fixture `advance_step` logs before navigating to Combat Screen static prototype.
- World Map `confirm_travel` logs before navigating to Dungeon Exploration static prototype.
- Browser console error log was 0 during Dungeon Exploration static checks.
- Dungeon Exploration browser DOM check confirmed left dungeon overlay, right exploration status panel, bottom action row, and 591px desktop stage height.
- Dungeon Exploration browser DOM check confirmed the red-marked bottom actions are no longer visible, the action row width is constrained to the left command area, and the green-marked right panel is summarized.
- Dungeon Exploration browser DOM check confirmed the CLI-aligned surface: HP/MP only in the resource strip, no `1957G`, no item summary panel, no inventory/status/world-map commands, no strong encounter prompt wording, current-run rewards, latest event, and advance/retreat only.
- Dungeon Exploration high-risk fixture browser check confirmed `advance_step` still navigates to `../combat_screen/index.html`.
- Dungeon Exploration screenshot capture in the in-app browser timed out after layout and interaction checks; DOM and console checks were still completed.
- Combat Screen fixtures parse as UTF-8 JSON.
- Combat Screen JS and Dungeon Exploration JS pass syntax check with the bundled Node.js runtime.
- Combat Screen default fixture renders 5 command buttons, top enemy HUD, lower-left player HUD, right-side Battle Log, and UIAction log.
- Combat Screen default fixture dispatches `basic_attack` and updates command feedback without changing fixture state.
- Combat Screen danger fixture renders disabled `use_skill` with disabled reason.
- Combat Screen blocked `use_skill` logs a blocked UIAction with reason.
- Combat Screen command bar does not include `view_battle_log` or `back_to_exploration`.
- Browser console error log was 0 during Combat Screen static checks.
- Combat Screen browser check confirmed no `1957G` in the combat resource strip and no Battle Log or return-to-exploration command in the bottom command bar.

## Recommended Next Step

Recommended next session entry:

```text
Review the CLI-aligned Dungeon Exploration static prototype, then decide whether another visual pass is needed before moving to the next approved screen.
```

Scope suggestion:

- Keep all prototypes static.
- Do not connect runtime.
- Do not use mockup/reference images as runtime assets.
- Keep UIAction logging before navigation.
- Preserve Dungeon Exploration and Combat Screen as static fixture display only until a runtime adapter is explicitly approved.

Alternative next steps:

- Review and refine the Dungeon Exploration static prototype layout before adding a runtime adapter.
- Build the Combat Result Screen static prototype only after explicit approval to move on from Combat Screen.
- Build the next facility static prototype, likely Shop or Synthesis.
- Add a proper keyboard focus graph for Town Hub and Guild.
- Add a shared prototype shell / fixture loader after Combat Screen exists.
