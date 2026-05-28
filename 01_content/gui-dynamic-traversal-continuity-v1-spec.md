# GUI Dynamic Traversal Continuity v1 Spec

Purpose: record the agreed UX and implementation contract for the next
runtime-connected GUI traversal slice. This is a specification, not an
implementation status log.

## 1. Status

This direction has user approval as a planning and specification target.
It does not by itself approve runtime implementation, staging, committing, or
packaging.

Runtime-connected GUI work remains opt-in. Before implementation, do a narrow
read-only preflight and confirm the exact slice.

## 2. Core Direction

The GUI live mode should follow the existing CLI traversal semantics and the
static prototype UX shell.

- CLI / Rich remains the gameplay behavior reference.
- HTML static prototype remains the RPG UX shell reference.
- Python runtime remains the authority for state, combat, rewards, save/load,
  validation, and gameplay rules.
- JavaScript dispatches UIAction payloads and renders returned screen models.
- JavaScript must not copy gameplay rules.
- Static fixture mode must remain usable.
- Do not manually read, write, or edit `save.json`.
- Avoid changing `03_engine/engine/game.py` for this slice.

The preferred long-term shape is:

```text
static UX shell
  + live ScreenModel from Python bridge
  + UIAction dispatch from browser
  + CLI-aligned traversal semantics
```

## 3. Player Mental Model

The player is exploring a dungeon. Combat is an event inside that traversal, not
an independent stage that resets the whole adventure.

Therefore, victory and combat retreat should preserve the sense that the player
is still inside the same dungeon run. Defeat is the exceptional case that breaks
the traversal and sends the player back to town.

## 4. Traversal Flow Contract

| Source screen | Event | Destination | Meaning |
| --- | --- | --- | --- |
| `world_map` | `confirm_travel` | `dungeon_exploration` | Enter the selected dungeon traversal. |
| `dungeon_exploration` | `retreat` | `world_map` | Leave the current dungeon traversal. |
| `dungeon_exploration` | `advance_step` encounter | `combat_screen` | Start combat as part of the same traversal. |
| `combat_screen` | victory result next action | `dungeon_exploration` | Combat resolved; continue the same traversal. |
| `combat_screen` | successful combat retreat result next action | `dungeon_exploration` | Escaped combat; continue the same traversal. |
| `combat_screen` | failed combat retreat | `combat_screen` | Enemy still acts; combat continues. |
| `combat_screen` | defeat result next action | `town_hub` | Traversal is broken; return by rescue / defeat flow. |

`combat_screen` retreat means leaving combat. It does not mean leaving the
dungeon. The dungeon-level decision to leave belongs to `dungeon_exploration`.

## 5. Exploration State Contract

Live exploration should preserve one active traversal session while the player is
inside a dungeon.

Minimum state to preserve:

- `dungeon_id`
- current step / route progress, following CLI behavior
- run rewards / current run log
- recent events
- last narrative message
- whether exploration is currently free to advance or waiting for combat result

When returning from combat victory or successful combat retreat:

- clear the active combat state
- restore exploration status to exploring
- append a short event line to the exploration event log
- keep the same dungeon traversal context
- do not route directly to Town Hub

Step progression must follow current CLI semantics. Do not create GUI-only step
rules.

## 6. Combat Result Overlay Contract

Victory and retreat overlays should keep the static prototype's continuity:

```text
Combat
  -> Result Overlay
  -> Return Exploration
```

Defeat should remain the run-breaking result:

```text
Combat
  -> Defeat Overlay
  -> Return Town Hub
```

Recommended `result_overlay.next_action` shape:

- Victory:
  - `action_id`: `return_to_exploration`
  - label: `返回探索`
  - route: `../dungeon_exploration/index.html?mode=live`
- Successful combat retreat:
  - `action_id`: `return_to_exploration`
  - label: `返回探索`
  - route: `../dungeon_exploration/index.html?mode=live`
- Defeat:
  - `action_id`: `back_to_town_hub`
  - label: `返回城鎮`
  - route: `../town_hub/index.html?mode=live`

The bridge may keep combat result data until the next action is dispatched, but
the next action should be responsible for restoring the appropriate destination
screen model.

## 7. World Map And Dungeon Entrance

World Map should remain the traversal stage, not a simple debug list. The static
prototype's selected-location detail panel is the current UX reference for a
dungeon entrance / confirm travel layer.

Future live mode should reuse that shell:

- select a dungeon on the map
- show dungeon information in the detail / floating panel
- dispatch `confirm_travel`
- enter `dungeon_exploration`

Do not create per-dungeon hardcoded screens for this slice. Prefer shared shell
plus injected ScreenModel content.

## 8. Player-Facing Language

Player-facing live UI should use Traditional Chinese RPG language. Engineering
terms should not appear in the main player UI.

Avoid player-facing phrases such as:

- `Live Combat`
- `Runtime-connected`
- `Python runtime`
- `bridge`
- `fixture preview`
- `live session`

Engineering terms may remain in:

- UIAction log
- debug-only fields
- developer / testing notes

Suggested replacements:

| Engineering phrase | Player-facing phrase |
| --- | --- |
| `Live Combat` | `戰鬥` |
| `Live Dungeon Exploration` | `迷宮探索` |
| `Return to live Town Hub` | `返回城鎮` |
| `Ask the Python runtime to advance exploration.` | `繼續向前探索。` |
| `Runtime-connected combat turn.` | `戰鬥回合進行中。` |

## 9. Expected Implementation Surface

If the user later approves implementation, keep the slice narrow:

- `03_engine/engine/gui_actions.py`
  - adapter/session state
  - ScreenModel shaping
  - UIAction dispatch semantics
  - no gameplay formula rewrite
- `07_gui_prototype/dungeon_exploration/dungeon-exploration.js`
  - render returned live model
  - dispatch exploration actions
  - navigate to returned live routes
- `07_gui_prototype/combat_screen/combat-screen.js`
  - render result overlay
  - dispatch `return_to_exploration` / `back_to_town_hub`
  - navigate to returned live routes

Touch `07_gui_prototype/shared/runtime-client.js` only if route handling requires
it, and keep that change mechanical.

Out of scope unless separately approved:

- `03_engine/engine/game.py`
- data/schema changes
- save migration
- combat formula changes
- full exploration event table
- boss gate / complete dungeon clear
- `use_skill`
- town economy v2
- facility runtime integration

## 10. Verification Plan

Minimum non-browser checks:

- Python syntax check for touched Python.
- JavaScript syntax checks for touched JS.
- Adapter smoke:
  - `confirm_travel -> dungeon_exploration`
  - `advance_step -> combat_screen`
  - combat victory overlay -> `return_to_exploration`
  - successful combat retreat overlay -> `return_to_exploration`
  - defeat overlay -> `back_to_town_hub`
  - exploration retreat -> `world_map`
- HTTP bridge endpoint smoke for the same transitions.
- Static fixture fallback still loads for exploration and combat.

Browser/manual smoke, when tooling or user testing is available:

```text
Start Screen live
  -> demo seed
  -> Town Hub
  -> World Map
  -> confirm travel
  -> Dungeon Exploration
  -> advance step
  -> Combat
  -> Victory or Retreat overlay
  -> Return Exploration
  -> Exploration retreat
  -> World Map
```

Defeat path should separately verify:

```text
Combat defeat overlay
  -> Return Town Hub
```

## 11. Notes For Future Agents

Do not treat this spec as permission to implement broad runtime GUI work. It is
only the agreed direction and a narrow v1 contract for traversal continuity.

If implementing, start with a read-only preflight and report:

- exact files to touch
- exact actions to support
- validation commands
- known unchanged limitations
- whether any current user edits conflict with the slice
