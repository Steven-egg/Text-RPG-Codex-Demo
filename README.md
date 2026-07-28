# Element Maze

Compact entry point for the playable Element Maze RPG, its primary live GUI,
the secondary CLI, and the release boundaries. Detailed decisions and focused
contracts live under `01_content/`.

## Acceptance Status

- The verified Batch A--C integration candidate is
  `02aa179ef8f9259b56369e3998cb7d91ee81ea3d` on
  `codex/s6-wave3-integration`. It has passed runtime, story, SFX, release
  asset, portable-package, and localhost/browser verification.
- `main` and `origin/main` remain at
  `46efeb93a0e98da12bde6c60769af2d303aeeb26`. The candidate is not `main` and
  must not be described as promoted until an independent Gate 3 / final
  acceptance passes and the Owner approves an ff-only promotion.
- The GUI is the primary product entrypoint. The secondary CLI is named
  **文字核心版 Text Core**.
- Python and `04_data/data/` remain gameplay authority. Browser JavaScript,
  static fixtures, the portable launcher, and release builders do not define
  gameplay rules.

## Landed Candidate Capsule

- The playable scope remains sealed: Fire, Ice, Earth, Thunder, and Final;
  four core jobs; eight formal promotion routes; four elemental seals; and the
  Final Boss.
- Optional `story_beat` presentation uses exactly six fields: `id`, `kind`,
  `title`, `lines`, `dismiss_label`, and `tone`. Kinds are `prologue`,
  `region_transition`, `boss_before`, `boss_after`, and `ending`; tones are
  `neutral`, `warning`, `victory`, and `ending`.
- The GUI safely ignores invalid story payloads and presents prologue, region
  transitions, before/after Boss beats, and the ending. Combat completion
  preserves `result close -> boss_after -> ending -> navigation`.
- Five muteable procedural micro-SFX cues are available without BGM, binary
  audio, or autoplay. Mute state uses `element_maze.sfx_muted`; untrusted
  synthetic clicks cannot create or resume an `AudioContext`.
- The release-only image builder writes referenced images to
  `dist/assets-overlay/app/<repository-relative-path>` and writes manifest
  format 1 to `dist/manifests/assets-manifest.json`. The verified candidate
  included 196 images, excluded 47 `OLD` images and 6 unreferenced images, and
  did not overwrite repository originals.
- The Windows portable builder keeps `app/` and `assets-overlay/app/`
  separate, launches the existing live GUI/runtime bridge, and also exposes
  **文字核心版 Text Core**. A local-validation ZIP has passed relocation
  checks, but it is not a formal release.
- Formal publication remains blocked with `release_ready:false`: the runtime
  has not been confirmed redistributable, complete runtime/dependency licenses
  are not assembled, and the required `rich` dependency is absent from the
  validated local runtime.

## Run

Do not depend on the synced `.venv` when it is unhealthy. Set the interpreter
for the active worktree explicitly:

```powershell
$mazePython = 'C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
```

Primary live GUI:

```powershell
& $mazePython -B .\06_tools\gui_runtime_bridge.py
```

Open `http://127.0.0.1:8010/start_screen/index.html?mode=live`. Use localhost,
not `file://`.

Secondary CLI (**文字核心版 Text Core**):

```powershell
& $mazePython .\element_maze.py
```

`run-game.bat` remains a CLI convenience entry when its local Python
environment is healthy. `save.json` is runtime output and must not be edited
manually.

For static-only GUI work, read
`.codex/skills/element-maze-gui-static-prototype/SKILL.md`, start
`start_gui_prototype_server.bat`, and preserve fixture fallback and UIAction
logging.

## Verification Routes

Gameplay/runtime baseline:

```powershell
& $mazePython 06_tools\validate_data.py
& $mazePython element_maze.py --smoke-test
& $mazePython 06_tools\test_job_growth_points.py
& $mazePython 06_tools\test_promotion_contracts.py
& $mazePython 06_tools\test_dungeon_defeat_contract.py
& $mazePython 06_tools\smoke_test_combat_bridge.py
& $mazePython 06_tools\test_combat_balance_report.py
```

Story and GUI SFX focused checks:

```powershell
& $mazePython 06_tools\test_story_beats.py
node 06_tools/test_gui_story_beats.mjs
node 06_tools/test_gui_sfx.mjs
```

Release-only referenced assets:

```powershell
& $mazePython 06_tools\test_release_assets.py
& $mazePython 06_tools\build_release_assets.py --dry-run
& $mazePython 06_tools\build_release_assets.py --output dist\assets-overlay --manifest dist\manifests\assets-manifest.json
& $mazePython 06_tools\build_release_assets.py --verify --output dist\assets-overlay --manifest dist\manifests\assets-manifest.json
```

Windows portable focused verification:

```powershell
& $mazePython 06_tools\test_windows_portable.py
```

Documentation/change hygiene:

```powershell
git diff --check
```

Build and verify commands, runtime requirements, and formal-release conditions
are defined in `01_content/windows-portable-release-v1.md`. Supplying a
machine-local runtime without `--redistributable-runtime` creates ignored
local-validation output with `release_ready:false`; that ZIP must not be
published or described as release-ready.

The combat balance phase-0 report remains diagnostic only; its numbers do not
authorize tuning:

```powershell
& $mazePython 06_tools\test_combat_balance.py --phase0
```

## Project Structure

- `element_maze.py`: **文字核心版 Text Core** entrypoint.
- `01_content/`: current decisions, handoff, plans, and archived history.
- `02_schema/`: data contracts.
- `03_engine/engine/game.py`: CLI lifecycle, combat, main loop, and
  compatibility re-exports.
- `03_engine/engine/facilities.py`: town facility CLI domain.
- `03_engine/engine/dungeon.py`: dungeon menu, exploration, events, Boss gate,
  clear handoff, and defeat handling.
- `03_engine/engine/state.py`: durable defaults and shared state helpers.
- `04_data/data/`: runtime data SSOT.
- `06_tools/`: bridge, validators, focused tests, and release builders.
- `07_gui_prototype/`: static fallback surfaces and the live GUI render layer.

## Document Routing

- Short Codex handoff: `01_content/codex-handoff-short.md`
- GUI live bridge: `01_content/gui-runtime-bridge-plan-v1.md`
- GUI static state: `01_content/gui-static-current-state-v1.md`
- Release asset contract: `01_content/release-asset-policy-v1.md`
- Windows portable contract: `01_content/windows-portable-release-v1.md`
- Maintenance closure: `01_content/maintenance-closure-v1.md`
- Job growth decision: `01_content/proposed-job-growth-points-v1.md`
- Historical task and architecture notes: `01_content/archive/`

## Fixed Boundaries

- Do not treat HTML fixtures, JavaScript, the portable launcher, or release
  output as gameplay SSOT or copy Python gameplay rules into them.
- Balance is closed. Only a reproducible issue that affects normal completion
  or a job's play experience can authorize a minimal maintenance fix.
- Growth SSOT is `04_data/data/jobs.py`. Warrior remains the frozen exception
  at 13.50 points per level (`attack = 1.5`); Mage, Rogue, and Cleric remain at
  15.00.
- Do not expand storage capacity, facilities, assets, classes, saves, rewards,
  unlocks, or gameplay scope without separate exact approval.
- Preserve `game.py` compatibility re-exports while the GUI bridge and tools
  still import through `game.*`.
- The only approved next step for this integration candidate is an independent
  Gate 3 / final acceptance. Only after Owner approval may `main` be advanced
  ff-only.
