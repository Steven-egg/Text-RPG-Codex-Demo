# GUI HTML Static Prototype Progress V1

Purpose: handoff note for the current HTML static prototype work. This file records what is already built, what UI decisions were accepted, what remains out of scope, and the recommended next entry point.

Date: 2026-05-19
Status: static prototype progress note

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
- Unlocked locations allow `confirm_travel`, which only logs the UIAction and does not start exploration.
- Locked locations keep the detail panel visible but block `confirm_travel` with a reason.

Accepted World Map decisions:

- Treat the supplied mockups as reference only, not runtime assets.
- Preserve the user-provided menu-open and detail-drawer mockups in `05_assets/gui_references/world_map/`.
- Main menu is opened from the top-left button as a side drawer.
- Selecting a map point updates the right-side information panel.
- Static prototype navigation only; no runtime adapter and no exploration flow.

Deferred World Map items:

- Real world map art or formal asset pipeline.
- Runtime adapter for location unlocks and travel.
- Final animation for the side drawer.
- Keyboard focus graph for map nodes.

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
- World Map unlocked locations dispatch `confirm_travel` without entering runtime.
- Town Hub `open_world_map` logs before navigating to World Map.
- World Map does not expose a return-to-town control in the current mockup pass.
- Browser console error log was 0 during World Map static navigation checks.

## Recommended Next Step

Recommended next session entry:

```text
Review and refine the World Map static prototype, then decide the next facility or travel detail screen.
```

Scope suggestion:

- Keep all prototypes static.
- Do not connect runtime.
- Do not use mockup/reference images as runtime assets.
- Keep UIAction logging before navigation.
- Refine World Map detail data, node placement, drawer behavior, and route readability before adding any runtime adapter.

Alternative next steps:

- Build the next facility static prototype, likely Shop or Synthesis.
- Add a proper keyboard focus graph for Town Hub and Guild.
- Add a shared prototype shell / fixture loader after one more screen exists.
