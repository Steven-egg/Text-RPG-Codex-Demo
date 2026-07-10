# GUI Static Prototype Current State V1

Purpose: compact active SSOT for the current HTML static prototype state. Historical
verification and superseded decisions live in
`archive/gui-html-static-prototype-progress-v1.md`.

## Boundary

- `07_gui_prototype/` is the default GUI static prototype surface.
- Static work covers render layer, layout, fixture shape, navigation,
  interaction, and UIAction logging.
- Fixtures are display data only, not gameplay SSOT.
- Do not connect the Python runtime, read or write `save.json`, modify runtime,
  data, schema, save, or combat formulas, or start a formal asset pipeline from
  a static GUI task.
- Runtime-connected GUI remains a separate explicitly approved mode.

## Current Static Surface

The current static prototype route covers these screen families:

- Start Screen and Town Hub
- Guild, Shop, Workshop, Storage, Magic Shop, Inn, Temple, and Synthesis
- World Map, Dungeon Exploration, Combat, and Relic Preview

Preserve static fixture fallback and UIAction logging. Screen-specific details
should be read from the relevant screen files, not copied into this document.

## Current Bridge Boundary

Approved live bridge slices may coexist with static fixtures, but do not imply
full inventory, equipment, facility, combat, settings, or other gameplay-system
expansion. Runtime bridge planning and approved-slice details remain in
`gui-runtime-bridge-plan-v1.md`.

## Current Checkpoint

- Facility-family CSS convergence is landed for the current prototype screens.
- Finalized GUI asset links and the current narrow bridge slices are already
  recorded in `README.md` and the runtime bridge plan.
- No new GUI implementation target is pre-approved; request an exact small
  surface before editing.

## History

For old screen-by-screen verification, Browser / DOM / console results, viewport
checks, and superseded decisions, read the archived progress log only when the
task needs historical context:

`archive/gui-html-static-prototype-progress-v1.md`
