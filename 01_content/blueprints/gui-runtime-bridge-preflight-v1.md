# GUI Runtime Bridge Preflight v1

Purpose: define the first implementable runtime bridge slice before any runtime,
prototype, save, or engine files are edited.

This file is a preflight spec. It is not implementation status and does not by
itself approve code changes.

## 1. Implementation Purpose

The implementation goal is to make the browser prototype meaningfully connected
to the Python CLI runtime:

- Browser clicks dispatch stable UIAction payloads.
- Python runtime owns state changes, validation, and save/load.
- JavaScript renders returned screen models and feedback.
- `save.json` is only read or written through runtime save/load behavior.
- Static prototype mode remains available and remains the default for ordinary
  GUI screen work.

The bridge should prove that the prototype is no longer just a disconnected
display layer, without turning JavaScript into a second gameplay rules engine.

## 2. First Slice

Recommended first implementation slice:

1. Start Screen live session actions.
2. World Map live `save_game`.
3. Town Hub live resource summary and navigation model.
4. Inn live `rest_at_inn` as the first mutating facility action.

This slice is intentionally small. It proves the full loop:

```text
browser click -> bridge action -> Python state change -> screen model response -> save/load
```

## 3. Non-Goals For The First Slice

Do not include these in the first implementation:

- Combat or combat formula changes.
- Dungeon exploration state machines.
- Data or schema edits.
- Save migration.
- Manual `save.json` edits.
- Shop, workshop, synthesis, magic shop, storage transactions.
- Temple story flag mutation.
- Relic gameplay activation.
- Asset pipeline work.
- README updates.

## 4. Expected File Surface After Implementation Approval

If the user later approves implementation, the likely narrow file surface is:

- `06_tools/gui_runtime_bridge.py`
  - Local-only HTTP bridge.
  - Owns in-memory runtime state for the browser session.
  - Calls adapter functions and existing save/load helpers.
- `03_engine/engine/gui_actions.py`
  - Small non-interactive action adapter.
  - Reuses existing runtime functions where safe.
  - Does not prompt for CLI input.
- `07_gui_prototype/shared/runtime-client.js`
  - Shared browser client for live mode.
  - Dispatches UIAction payloads to the bridge.
  - Falls back cleanly to static fixture mode when live mode is off or bridge is
    unavailable.
- `07_gui_prototype/start_screen/start-screen.js`
  - Optional minimal live-mode hook for new/load/restart.
- `07_gui_prototype/world_map/world-map.js`
  - Optional minimal live-mode hook for save and live resource strip.
- `07_gui_prototype/town_hub/town-hub.js`
  - Optional minimal live-mode hook for live resource strip/navigation.
- `07_gui_prototype/inn_screen/`
  - If Antigravity has landed a static inn screen, add live-mode hook only.
  - If not landed yet, defer Inn browser wiring until the static screen exists.

Do not modify `README.md` for this slice. README should wait until at least one
live bridge path is working.

## 5. Live Mode Toggle

Default decision:

- Keep static fixture mode as normal page behavior.
- Enable live mode with a query string such as `?mode=live`.
- Optionally persist the selected mode in `sessionStorage` later.

Reasoning:

- Static verification remains stable.
- Live experiments do not surprise static prototype reviewers.
- Browser checks can test both modes explicitly.

## 6. Save Policy

Default decision:

- Phase 1 uses manual save only.
- `save_game` writes through Python runtime save behavior.
- `start_new_game`, `restart_game`, `load_game`, and `rest_at_inn` do not
  auto-save in the first implementation.
- Auto-save can be reconsidered only after the Inn live action is verified.

Rationale:

- The user can see exactly when persistence happens.
- Failed live experiments do not silently overwrite a useful save.
- The first bridge test remains easy to reason about.

## 7. Endpoint Contract

Suggested endpoints for the first slice:

### `GET /api/session`

Response:

```json
{
  "ok": true,
  "save_exists": true,
  "state_loaded": false,
  "state_summary": null
}
```

### `POST /api/session/new`

Payload:

```json
{
  "name": "Adventurer",
  "job_id": "warrior"
}
```

Behavior:

- Validate `job_id`.
- Create state through runtime logic.
- Return Start or Town Hub next route suggestion.
- Do not save automatically in the first slice.

### `POST /api/session/load`

Behavior:

- Load existing runtime save through `load_game`.
- Return failure if no valid save exists.
- Return state summary and next route suggestion.

### `POST /api/save`

Behavior:

- Require loaded runtime state.
- Save through `save_game`.
- Return current state summary.

### `GET /api/screen/<screen_id>`

First supported screen ids:

- `start_screen`
- `world_map`
- `town_hub`
- `inn_screen` only after the static inn screen exists.

Behavior:

- Return a live screen model close to the existing fixture shape.
- Include `state_summary` and action enabled/disabled reasons from Python.

### `POST /api/action`

Payload:

```json
{
  "screen_id": "world_map",
  "action_id": "save_game",
  "payload": {}
}
```

Response:

```json
{
  "ok": true,
  "action_id": "save_game",
  "message": "Saved.",
  "state_summary": {},
  "screen_model": {},
  "next_route": null
}
```

The bridge must reject unknown action ids and invalid payloads.

## 8. First Action Set

### `start_new_game`

Payload:

```json
{
  "name": "Adventurer",
  "job_id": "warrior"
}
```

Runtime behavior:

- Create new state.
- Return state summary and next route.
- Do not save automatically.

Validation:

- `name` may fall back to the runtime default.
- `job_id` must exist in runtime job data.

### `restart_game`

Same payload and behavior as `start_new_game`, but the response message should
make clear that the in-memory browser session was replaced. It should not delete
or overwrite `save.json` unless `save_game` is explicitly called afterward.

### `load_game`

Payload:

```json
{}
```

Runtime behavior:

- Load runtime save into bridge session.
- Return state summary and next route.

Validation:

- Fail if save is missing or invalid.

### `save_game`

Payload:

```json
{}
```

Runtime behavior:

- Save current in-memory state through runtime save behavior.

Validation:

- Fail if no state is loaded.

### `rest_at_inn`

Payload:

```json
{
  "service_id": "overnight_rest",
  "cost": 30
}
```

Runtime behavior:

- Verify current state has enough gold.
- Deduct 30G.
- Restore HP/MP to current max values.
- Return updated state summary and inn screen model.
- Do not save automatically in the first slice.

Validation:

- Reject unknown service id.
- Reject mismatched cost.
- Reject insufficient gold.

## 9. State Summary Shape

Minimum response shape:

```json
{
  "name": "Adventurer",
  "job_id": "warrior",
  "job_label": "Warrior",
  "level": 1,
  "exp": 0,
  "gold": 120,
  "guild_points": 0,
  "hp": {
    "current": 120,
    "max": 120
  },
  "mp": {
    "current": 20,
    "max": 20
  },
  "save_exists": true
}
```

Labels can be generated server-side from runtime data. The browser should not
infer gameplay values.

## 10. Screen Model Defaults

Return full screen models for the first implementation.

Reasoning:

- Easier to debug.
- Easier to keep render code close to existing fixture renderers.
- Avoids early patch/merge complexity.

The response can be optimized later if payload size becomes a real issue.

## 11. Inn Dependency On Antigravity Work

Antigravity may add static prototypes for:

- `inn_screen/`
- `temple_screen/`
- `relic_preview_screen/`

Treat those as planned additions, not drift.

Bridge implementation should only wire `inn_screen/` after the static screen
exists. If the inn screen is not available when implementation starts, finish
Start/Load/Save/Town Hub first and leave Inn wiring as the next bridge slice.

Temple and Relic Preview should not be in the first live implementation:

- Temple can display live preview later, but story flag mutation needs a
  deliberate action and separate validation.
- Relic Preview should remain preview-only until relic gameplay is explicitly
  approved.

## 12. Validation Plan

Before implementation:

- Confirm working tree and current GUI/runtime files.
- Confirm first slice and file surface with the user.

After implementation:

- Run data validation.
- Run runtime smoke test.
- Run bridge endpoint smoke tests:
  - health/session
  - new game success
  - load game blocked when missing/invalid
  - save blocked without state
  - save success with state
  - inn rest success
  - inn rest insufficient gold blocked
- Run JavaScript syntax checks for touched prototype files.
- Run browser smoke in static mode.
- Run browser smoke in live mode.
- Confirm `save.json` is only changed by runtime save behavior.

## 13. Risk Notes

Main risks:

- Accidentally duplicating gameplay rules in JavaScript.
- Driving the CLI input loop instead of creating non-interactive runtime actions.
- Silent save overwrites.
- Letting Temple screen entry mutate story flags.
- Expanding into combat or dungeon state too early.

Mitigation:

- Keep JavaScript to dispatch/render.
- Keep the first slice to session/save/Town Hub/Inn.
- Manual save only.
- Server-side action whitelist and validation.
- No combat or dungeon work in the first bridge implementation.

## 14. Recommended Next Approval Prompt

Use this if the next session is ready to implement:

```text
Approve the first GUI runtime bridge implementation slice only:

- Add a local bridge server under 06_tools/.
- Add a small runtime action adapter under 03_engine/engine/.
- Add shared live-mode browser client under 07_gui_prototype/shared/.
- Wire Start Screen, World Map save, Town Hub live summary, and Inn only if the
  static inn screen exists.
- Keep static fixture mode as default.
- Use manual save only.
- Do not touch README, data, schema, save migration, combat formulas, dungeon
  exploration, or combat.
- Do not manually edit save.json; only runtime save/load may touch it.
```
