# GUI Runtime Bridge Plan V1

Purpose: active planning SSOT for the narrow local GUI runtime bridge. Historical
architecture, endpoint drafts, slice notes, and old verification are preserved in
`archive/gui-runtime-bridge-plan-v1.md`.

## Mode Boundary

- HTML static prototype mode remains the default for ordinary GUI work.
- Runtime-connected GUI is opt-in and requires explicit approval for the exact
  slice before implementation.
- Before approved bridge work, stop at a read-only planning gate and name the
  touched files, runtime actions, validation, and forbidden adjacent systems.
- Python remains gameplay authority. Browser JavaScript only dispatches UIAction
  payloads and renders returned ScreenModels.
- Save/load uses existing runtime behavior only; never manually edit `save.json`.

## Approved Surface

After explicit approval, the narrow surface may include:

- `06_tools/` for the local bridge server and smoke helpers.
- `03_engine/engine/` only for small adapters that reuse existing runtime logic.
- `07_gui_prototype/` for live-mode client and render integration.

Runtime, data, schema, save migration, combat formulas, and broad gameplay
framework work remain separate approval gates.

## Current Live Boundary

Existing narrow slices include start/load/restart, the local town and facility
shells, approved dungeon/combat actions, guild reporting, shop consumables,
magic-book learning, and workshop weapon buy/equip coverage. These slices do not
approve generic inventory/equipment management, new facilities, broad combat
systems, or runtime expansion.

For exact current implementation details, inspect the relevant runtime bridge
code and focused smoke helper. Do not use the archived plan as ordinary status.

## Planning Gate

Every new bridge slice must state:

1. exact screen and action scope;
2. existing runtime functions reused;
3. files allowed to change;
4. static fallback behavior;
5. validation commands and stop conditions.

If the slice changes mode or crosses into gameplay authority, pause for explicit
approval instead of extending an existing MVP by inference.

## History

The previous long-form plan is retained at:

`archive/gui-runtime-bridge-plan-v1.md`
