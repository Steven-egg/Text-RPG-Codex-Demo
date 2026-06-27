# Weekend Task Board: Docs, Asset Inventory, Runtime Slimming

Purpose: let desktop Codex, desktop Antigravity, and the owner continue the
same long task chain without a long spoken handoff.

Start prompt:

```text
Read AGENTS.md Hot Zone first, then read task.md.
Antigravity drafts or implements the next approved slice.
Codex reviews scope, drift risk, diffs, and merge readiness.
The owner decides direction changes and approves any implementation surface.
Do not push. Do not read or write save.json.
```

## Current Owner Intent

- CLI expansion and the local GUI bridge are close to structurally complete.
- Next work should prepare visual assets and reduce future drift risk.
- World / encounter assets can come before late balance work.
- Late balance work is not part of this task chain yet.

Out of scope for the asset phase:

- skill VFX
- class-change character art
- element-counter VFX
- relic active or passive effect visuals
- endgame build visuals
- class specialization visuals
- relic aura visuals

## Priority Order

1. Documentation drift control.
2. Asset production inventory.
3. `game.py` / `gui_actions.py` slimming review.
4. Asset connection strategy.

Do the phases in this order unless the owner changes it.

## Phase 1: Documentation Drift Control

Goal:

- Reduce old-plan drag before broad asset planning.
- Keep Hot Zone short.
- Mark stale or historical material clearly so future reads do not treat it as
  current approval.

Allowed first output:

- A read-only cleanup proposal.
- A list of exact files and sections that should be shortened, moved, or marked
  historical.
- Reasons for each cleanup item.

Preferred Antigravity role:

- Draft the cleanup proposal.
- Do not edit docs until the owner approves exact files.

Preferred Codex role:

- Review whether the proposal protects startup routing and avoids losing useful
  context.
- Check that no Cold Zone history becomes required startup reading.

Implementation requires owner approval for exact doc surfaces.

## Phase 2: Asset Production Inventory

Goal:

- Produce a read-only visual asset inventory aligned to existing runtime ids and
  display names.

In scope:

- monsters
- bosses
- facilities
- dungeon exploration scenes
- combat backgrounds
- region hubs
- town hubs

First suggested slice:

- Border / Fire: baseline audit only (no generation) because the demo route is
  already structurally complete.
- Ice: first production-oriented region.

Roles and Ownership:

- Antigravity: drafts the asset inventory and image request specs.
- Codex: generates image candidates from approved specs.
- Preferred Antigravity role details:
  - Draft the inventory table.
  - Include suggested asset id, source runtime id, display name, image type,
    first slice priority, and notes.
  - Avoid changing runtime, schema, save data, GUI bridge code, or generated
    assets.
- Preferred Codex role details:
  - Review id alignment, missing categories, stale-plan drift, and verify no
    out-of-scope visual types are included.

Closed Visual Types (Out of Scope):

- The following remain closed: skill VFX, class-change art, element-counter VFX,
  relic active/passive visuals, endgame build visuals, class specialization
  visuals, relic aura visuals.

Possible future output file:

- `01_content/asset-production-inventory-v0.1.md`

Do not create that file until the owner approves the docs surface.

## Phase 3: Runtime / Bridge Slimming Review

Goal:

- Review `03_engine/engine/game.py` and `03_engine/engine/gui_actions.py`
  before image connection work makes them longer.

Allowed first output:

- Read-only structure review.
- Candidate extraction points.
- Risk list.
- Proposed smallest implementation slice.

Preferred Antigravity role:

- Draft the structural review or implement an approved small slice.

Preferred Codex role:

- Review behavior risk, save/load implications, smoke coverage, and diff size.

Implementation requires owner approval for the exact runtime files.

## Phase 4: Asset Connection Strategy

Goal:

- Decide how generated images map to stable ids without expanding gameplay
  logic.

Preference:

- Use data-driven references or manifest-style mapping.
- Avoid broad conditional logic in `game.py` or `gui_actions.py`.
- Keep Python runtime as gameplay authority.

Possible future surfaces:

- asset manifest
- GUI render-layer mapping
- static prototype fixtures
- narrowly approved GUI bridge fields

Do not start implementation until Phases 1 to 3 have produced reviewed outputs.

## Fixed Review Pipeline

For every subtask:

1. State the exact surface.
2. Read only the minimum files needed for that surface.
3. Produce a short plan, proposal, or inventory.
4. Codex reviews for drift, scope creep, stale-history influence, and test fit.
5. Owner approves edits before any Hot Zone, Task Zone, runtime, data, schema,
   save, GUI prototype, or GUI bridge file is changed.
6. Run checks that match the touched surface.

Suggested checks:

- Docs only: `git status --short`, targeted diff review, and markdown sanity.
- Runtime or bridge: `python 06_tools/validate_data.py`,
  `python element_maze.py --smoke-test`, targeted smoke tests, and
  `git diff --check`.
- GUI static prototype: syntax check, browser preview when applicable, and
  UIAction logging review when touched.

## Standing Guardrails

- Do not read or write `save.json`.
- Do not push unless the owner explicitly asks.
- Do not treat old Cold Zone plans as current approval.
- Do not connect generated art by adding broad conditional logic to runtime
  files.
- Do not start class balance, class promotion, element formula, relic effect, or
  endgame balance work during this task chain.
- Do not stage, commit, merge, or archive unless the owner asks.

