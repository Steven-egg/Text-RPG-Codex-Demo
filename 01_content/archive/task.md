# Archived Weekend / Weekday Task Board: Docs, Asset Inventory, Runtime Slimming

Archived status: this was a cross-session task-chain board for an earlier docs,
asset inventory, and runtime slimming sequence. It is retained for history only.
Do not treat it as the current task board or current project status.

Original purpose: let desktop Codex, desktop Antigravity, and the owner continue
the same long task chain without a long spoken handoff.

Original start prompt, historical:

```text
Read AGENTS.md Hot Zone first. Read `01_content/archive/task.md` only when
historical task-chain context is explicitly needed.
Antigravity drafts or implements the next approved slice.
Codex reviews scope, drift risk, diffs, and merge readiness.
The owner decides direction changes and approves any implementation surface.
Do not push. Do not read or write save.json.
```

Original weekday / cross-machine short prompt, historical:

```text
Read AGENTS.md Hot Zone first. Read `01_content/archive/task.md` only when
historical task-chain context is explicitly needed.
Use live git status/log on this machine; do not trust another machine's local
working tree as current.
Continue only the smallest approved slice.
Runtime/data/schema/save/combat work starts with a read-only planning gate
unless the owner explicitly approved exact implementation files.
Do not read or write save.json. Do not push unless explicitly asked.
```

Current pushed runtime checkpoint:

- `510db7c [antig] refactor(runtime): extract town facilities domain`
- Branch pushed for this checkpoint:
  `antig/facilities-domain-extraction`
- Working-tree note:
  `06_tools/dialogue_templates_demo.py` may exist as an owner-provided local
  scratch/demo note. Do not include it in runtime slimming commits unless the
  owner explicitly approves that exact file.

## Current Owner Intent

- CLI expansion and the local GUI bridge are close to structurally complete.
- Next work should prepare visual assets and reduce future drift risk.
- World / encounter assets can come before late balance work.
- Late balance work is not part of this task chain yet.
- Engine slimming is useful before heavy weekday work on image production,
  class and element balance, relic effects, promotion / class transfer, and
  asset connection, because it reduces read cost and narrows future edit risk.

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
3. `game.py` / `gui_actions.py` slimming review and engine domain split.
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
- Keep `game.py` focused as the CLI game loop / interface orchestrator rather
  than a mixed gameplay, facility, combat, dungeon, and dialogue god file.
- Reduce future read cost for asset mapping, class / element balance, relic
  effects, promotion / class transfer, and GUI bridge review.

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

Current landed status:

- `03_engine/engine/facilities.py` is landed as the town facility CLI domain for
  Guild, shops, workshops, synthesis, magic shop, storage, inn, and
  Temple-facing CLI flows that are not relic-domain logic.
- `03_engine/engine/state.py` now owns pure payment / quest readiness helpers
  used by facilities and GUI bridge models.
- `03_engine/engine/game.py` keeps compatibility re-exports for the extracted
  facility and state helper API, including `iron_workshop` and
  `armor_workshop`.
- Codex merge-readiness review passed after re-review. Validation used:
  `python 06_tools/validate_data.py`, `python element_maze.py --smoke-test`,
  all current `06_tools/smoke_test_*.py` bridge smoke tests, and
  `git diff --check`.

### Phase 3 Architecture Direction

Avoid micro-splitting each shop or facility into tiny files. Prefer domain-sized
modules that keep related CLI/runtime behavior together:

- `game.py`: CLI lifecycle, title / save / load, main loop, high-level routing.
- `facilities.py`: town facility CLI menus and shared facility actions,
  including Guild, shops, workshops, synthesis, magic shop, storage, inn, and
  Temple-facing CLI flows that are not relic-domain logic.
- `dungeon.py`: dungeon menu, exploration loop, weighted events, treasure,
  traps, special events, boss gate / clear handoff, run-log defeat handling.
- `combat.py`: turn-based combat loop, damage formulas, hit / crit / escape,
  player actions, item use in combat, enemy and boss actions, effect ticking.
- `state.py`: durable state defaults, inventory/equipment mutation, unlocks,
  stat calculation, region normalization, pure state helpers.
- `relic.py`: relic / elemental seal progression domain, enshrinement, Final
  gate unlock, and CLI relic preview. Keep separate from generic facilities
  because relic behavior crosses progression, items, and GUI preview.

Preferred slimming order:

1. Landed: dialogue-template foundation and `relic.py` slice.
2. Landed: `facilities.py` town facility domain extraction; preserve existing
   public `game.py` re-exports where GUI bridge code still imports through
   `game`.
   - *Deferred cleanup note*: `buy_menu` appears unused after the newer shop mechanism replaced it; do not delete during first `facilities.py` extraction; revisit as separate dead-code cleanup after extraction and bridge smoke tests pass.
3. Plan `dungeon.py` after facilities, because it touches exploration flow,
   random events, run logs, boss gates, and defeat handling.
4. Plan `combat.py` last, because it is the highest-risk balance and formula
   surface.

Each runtime extraction slice should:

- Start with a read-only planning gate unless the owner explicitly approves the
  exact implementation surface.
- Move behavior without changing gameplay, text, formulas, rewards, save shape,
  or GUI bridge contracts.
- Keep API compatibility through `game.py` re-exports when existing GUI bridge
  modules depend on `game.<function>`.
- Include targeted checks before review: `python 06_tools/validate_data.py`,
  `python element_maze.py --smoke-test`, relevant bridge smoke tests, and
  `git diff --check`.

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
