# Element Maze

Purpose: compact project entry point for the playable Python CLI RPG, GUI
prototype, and formal-version content planning. Detailed bridge status,
screen-level verification, and historical MVP notes live in Task Zone files.

## Current Stable Capsule

- Latest local checkpoint seen during docs cleanup:
  `5c0dfad [codex] fix(gui): align Inn and Temple dialogue service shell`.
- Element Maze is an expandable playable demo, not a closed demo.
- The Python CLI runtime remains the gameplay authority.
- Act 1 is playable through the main loop.
- Act 2 fire demo content is in runtime data and bridge coverage, including Ash
  Ravine, Cinder Seal Depths, three fire-mark shards, Guild / Temple / Church
  lookup closure, and Boss rule parity for Glen, Ash Guardian, and Cinder Seal
  Sentinel.
- Basic facility CLI-parity bridge coverage is complete through Guild material
  buyback.
- The maintainability checkpoint is stable: shared GUI presentation helpers and
  facility ScreenModel extraction are in place; action dispatch and mutation
  remain in `gui_actions.py`.

See `git status --short` before editing. The workspace may contain owner-side
document cleanup or archive changes.

## Content Skeleton

Current formal-version macro planning lives in:

- `01_content/world-content-skeleton-v0.1.md`

Current macro decisions:

- Four core content elements: Fire, Ice, Earth, Thunder.
- Final region is a composite endgame zone, not a fifth core element.
- The existing fire demo route uses the existing Border Town only; do not add an
  Ash Outpost.
- Future Ice / Earth / Thunder regions each default to one regional town and
  three dungeons: two minor dungeons plus one main two-phase dungeon.
- This skeleton does not approve runtime, data, schema, save, GUI, bridge,
  combat, class, relic, or asset-pipeline implementation.

## GUI State

- `07_gui_prototype/` remains the default GUI static prototype surface.
- Static prototype work validates render layer, layout, fixture shape,
  navigation, interaction, and UIAction logging only.
- Runtime-connected GUI work is opt-in and limited to already approved local
  live bridge slices.
- Detailed GUI bridge and screen status lives in Task Zone files, not this
  README.

Task Zone pointers:

- GUI live bridge plan and landed live-slice notes:
  `01_content/gui-runtime-bridge-plan-v1.md`
- GUI static prototype handoff and screen verification:
  `01_content/gui-html-static-prototype-progress-v1.md`
- GUI document routing and lifecycle:
  `01_content/gui-planning-index.md`
- Facility-family responsibility baseline:
  `01_content/gui-facility-shell-baseline-v0.1.md`

## How To Run

Most local play:

```powershell
.\run-game.bat
```

Direct Python entry:

```powershell
C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe .\element_maze.py
```

With a local virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
python .\element_maze.py
```

`.venv/` is local tooling only and is ignored by git.

## Verification

Standard local check:

```powershell
.\run_checks.bat
```

`run_checks.bat` runs:

```powershell
python 06_tools\validate_data.py
python element_maze.py --smoke-test
```

Useful direct checks:

```powershell
python 06_tools\content_inventory_report.py
python 06_tools\content_inventory_report.py --json
python 06_tools\smoke_test_combat_bridge.py
python 06_tools\smoke_test_progression_bridge.py
```

For docs-only cleanup, use markdown/status/diff checks. Runtime smoke is not
required unless runtime, data, schema, save, combat, or bridge behavior changes.

## Project Structure

- `element_maze.py`: game entry point.
- `01_content/`: content design, handoff, startup, and planning docs.
- `02_schema/`: data contract docs.
- `03_engine/engine/`: runtime flow and gameplay rules.
- `04_data/data/`: runtime data tables.
- `05_assets/`: future/reference asset area.
- `06_tools/`: validation, smoke, bridge helper, and inventory tools.
- `07_gui_prototype/`: HTML static prototype and limited local live bridge
  render surfaces.

## SSOT Rules

- `README.md`: compact project entry.
- `01_content/agent-startup-reading-list.md`: Hot / Task / Cold Zone loading
  rules.
- `01_content/codex-handoff-short.md`: short new-session handoff.
- `01_content/world-content-skeleton-v0.1.md`: current macro content skeleton.
- `01_content/gui-runtime-bridge-plan-v1.md`: GUI live bridge details.
- `01_content/gui-html-static-prototype-progress-v1.md`: static prototype
  screen-level details.
- `01_content/game-design.md`: content-design SSOT.
- `02_schema/*.schema.md`: data contracts.
- `04_data/data/*.py`: runtime data SSOT.
- `04_data/data/registry.py`: runtime data index and helper id sets.
- `06_tools/validate_data.py`: cross-table validation.
- `06_tools/content_inventory_report.py`: read-only inventory / drift report.
- `save.json`: runtime save output, not design data and not a manual edit target.

## Change Boundaries

- Do not read or write `save.json` manually.
- Do not treat HTML fixtures as gameplay SSOT.
- Do not copy gameplay rules into JavaScript prototypes.
- Do not modify runtime, data, schema, save, or combat formulas as part of GUI
  prototype or docs cleanup.
- Do not expand a landed narrow live MVP into a full system without a new
  read-only planning gate and explicit owner approval.
- Do not start a formal asset pipeline from reference/mockup images.
- Do not let README, handoff, schema, runtime data, and Task Zone docs drift out
  of sync.

## Next-Step Boundary

No next implementation target is pre-approved.

Allowed as planning only:

- refine `01_content/world-content-skeleton-v0.1.md`
- route old Hot Zone details into Task / Cold Zone
- produce a read-only implementation gate for one exact future slice

Still closed until a later exact-scope approval:

- runtime/data/schema/save/combat changes
- new quest data or broad quest framework work
- generic inventory/equipment, storage capacity, shop sell, generic sell, or
  full facility systems
- formal class transfer, relic effects, endgame systems, settings persistence,
  or cross-screen preferences
- GUI visual implementation, image generation, bridge expansion, or asset
  pipeline work
