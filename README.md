# Element Maze

Compact entry point for the playable Python CLI RPG, GUI prototype, and live
project boundaries. Detailed decisions and verification live in Task Zone
documents under `01_content/`.

## Current Stable Capsule

- Latest commit: `b542039 wip: backup promotion, balance, quality, and GUI work`.
- The active OneDrive worktree contains uncommitted WIP. Always inspect
  `git status --short`; do not stage, commit, push, reset, or overwrite it
  without explicit approval.
- The playable scope is sealed: Fire, Ice, Earth, Thunder, and Final; four core
  jobs; eight formal promotion routes; four elemental seals; Final Boss; and
  the Python CLI authority. GUI has a static prototype and selected live bridge
  slices.
- Balance is closed. Only a reproducible issue that affects normal completion
  or a job's play experience can authorize a minimal maintenance fix.
  Diagnostic report values do not authorize tuning.
- Growth SSOT is `04_data/data/jobs.py`. Warrior is the frozen exception at
  13.50 points per level (`attack = 1.5`); Mage, Rogue, and Cleric remain at
  15.00. See `01_content/proposed-job-growth-points-v1.md`.
- Storage live GUI supports a 500G unlock and deposit/withdraw for up to 10
  non-key item types. Capacity upgrades are not open.
- Town facilities live in `03_engine/engine/facilities.py`; the dungeon domain
  already lives in `03_engine/engine/dungeon.py`; `game.py` remains the CLI
  orchestrator and compatibility facade for GUI bridge consumers.
- The release-maintenance conclusion, verification matrix, and remaining risks
  live in `01_content/maintenance-closure-v1.md`.

## Run

Do not depend on the currently broken synced `.venv`. Use the bundled Python
runtime for this worktree:

```powershell
$mazePython = 'C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $mazePython .\element_maze.py
```

`run-game.bat` remains the normal convenience entry when its local Python
environment is healthy. `save.json` is runtime output and must not be edited
manually.

## Release Verification

Blocking checks:

```powershell
& $mazePython 06_tools\validate_data.py
& $mazePython element_maze.py --smoke-test
& $mazePython 06_tools\test_job_growth_points.py
& $mazePython 06_tools\test_promotion_contracts.py
& $mazePython 06_tools\test_dungeon_defeat_contract.py
& $mazePython 06_tools\smoke_test_combat_bridge.py
& $mazePython 06_tools\test_combat_balance_report.py
git diff --check
```

Diagnostic only; its numbers are not a balance verdict:

```powershell
& $mazePython 06_tools\test_combat_balance.py --phase0
```

For a GUI static prototype change, first read
`.codex/skills/element-maze-gui-static-prototype/SKILL.md`, run
`start_gui_prototype_server.bat`, and test through localhost rather than
`file://`.

## Project Structure

- `element_maze.py`: game entry point.
- `01_content/`: current decisions, handoff, plans, and archived history.
- `02_schema/`: data contracts.
- `03_engine/engine/game.py`: CLI lifecycle, combat, main loop, and compatibility
  re-exports.
- `03_engine/engine/facilities.py`: town facility CLI domain.
- `03_engine/engine/dungeon.py`: dungeon menu, exploration, events, Boss gate,
  clear handoff, and defeat handling.
- `03_engine/engine/state.py`: durable defaults and shared state helpers.
- `04_data/data/`: runtime data SSOT.
- `06_tools/`: validators, tests, smoke checks, and diagnostic reports.
- `07_gui_prototype/`: static prototype and limited local live bridge surfaces.

## Document Routing

- Current maintenance closure:
  `01_content/maintenance-closure-v1.md`
- Short Codex handoff:
  `01_content/codex-handoff-short.md`
- Job growth decision and node tables:
  `01_content/proposed-job-growth-points-v1.md`
- World content baseline:
  `01_content/world-content-skeleton-v0.1.md`
- Combat progression history and boundaries:
  `01_content/combat-progression-design-v1.md`
- GUI live bridge plan:
  `01_content/gui-runtime-bridge-plan-v1.md`
- GUI static state:
  `01_content/gui-static-current-state-v1.md`
- Historical task and architecture notes:
  `01_content/archive/`

## Fixed Boundaries

- Do not treat HTML fixtures as gameplay SSOT or copy Python gameplay rules
  into JavaScript.
- Do not expand a landed live MVP, storage capacity, facility system, asset
  pipeline, class system, or balance pass without a new exact-scope approval.
- Do not change gameplay, values, saves, or GUI behavior during structural
  extraction.
- Preserve `game.py` re-exports while current GUI bridge and tools still import
  through `game.*`.
- No next implementation target is pre-approved. The next step after this
  closure is an owner decision, not an implied roadmap item.
