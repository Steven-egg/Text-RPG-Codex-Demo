# 《元素迷宮：邊境冒險者》終端機版

Purpose: project-level entry point for the playable Python CLI RPG and its GUI
prototype work. This README should stay compact. Detailed GUI bridge status,
screen-level verification, and historical MVP notes live in Task Zone files.

## Current Stable Capsule

Git / working-tree baseline:

- Latest committed bridge baseline before the current package:
  `017fa43 [antig] feat(gui): add guild quest synthesis unlock bridge`
- Current newest live slice: Storage Unlock & View Live MVP.

Project posture:

- Element Maze is an expandable playable demo, not a closed demo.
- Narrow live MVP boundaries are current-slice risk controls. They preserve
  future extension points, but expansion still requires a new read-only planning
  gate and owner-approved exact scope.

Gameplay/runtime state:

- The project is a playable Python CLI text RPG.
- Act 1 is playable through its main loop.
- Act 2 fire demo content is in runtime data: Ash Ravine, Ash Guardian, supply
  upgrade, Cinder Seal Depths, Cinder Seal Sentinel, and the three fire-mark
  shard inquiry / church lookup closure.
- CLI UI uses a thin Rich `Panel` presentation layer for the core loop. Input,
  data, save behavior, and combat rules remain the runtime authority.
- `v0.2-2` minimal skill-system cleanup is complete, including skill books,
  learned skills, combat skill use, and MP spending.

GUI state:

- `07_gui_prototype/` remains the default GUI static prototype surface.
- Static prototypes exist for Start Screen, Town Hub, Guild, Synthesis, World
  Map, Dungeon Exploration, Combat, Shop, Workshop, Storage, Magic Shop, Inn,
  Temple, and Relic Preview.
- Static prototype work validates render layer, layout, fixture shape,
  navigation, interaction, and UIAction logging only.
- Runtime-connected GUI work is opt-in and limited to the already approved local
  live bridge slices listed below.

Blessed local live bridge coverage:

| Area | Stable live scope |
|---|---|
| Start | `start_new_game`, `restart_game`, `load_game`; live entry copy and no-save / has-save states aligned with static Start Screen. |
| Town Hub | Live resource strip, facility nodes, synthesis entry unlock state, `open_world_map`, and live routing into approved facilities. Town Hub does not expose `save_game`. |
| Synthesis | Single existing recipe craft bridge for `recipe_piercing_bundle` through Python runtime validation and `game.craft_recipe_message(...)`. |
| Inn | `rest_at_inn` deducts 30G and restores HP/MP through Python runtime behavior. |
| World Map | Runtime-backed location / route ScreenModel; main menu keeps `save_game` and shell-only `open_settings`; town return is via town node / detail action. |
| Dungeon / Combat | Approved traversal and combat loop slice, victory / retreat / defeat routing, route clear / resolved state, and Combat Skill Button MVP. |
| Guild | Narrow clear report registration plus existing `QUESTS` turn-in bridge; `quest_cave_gathering` can unlock `shop_synthesis_01`. |
| Shop | Buy exactly one existing travel-shop consumable through Python server-side validation. |
| Magic Shop | Learn one existing magic book through Python server-side validation and existing skill data. |
| Workshop | Buy existing weapon without auto-equip; equip inventory-held weapon-slot items into `equipment.weapon` through `game.equip_item(...)`. |
| Storage | Unlock and view the Town Storage live screen through Python runtime state; deposit / withdraw / capacity upgrade remain closed. |

Storage Unlock & View Live MVP is the current newest live bridge state:

- Town Hub can route to the Storage live screen, which loads a runtime-shaped
  `storage_screen_model(state)`.
- `unlock_storage` checks the existing runtime storage unlock cost, blocks
  insufficient Gold, deducts Gold on success, and sets
  `state["storage_unlocked"] = True`.
- After unlock, the screen displays live inventory, storage status, current
  storage contents, and capacity.
- `deposit_item`, `withdraw_item`, and storage capacity upgrades remain disabled
  with MVP-scope messaging.
- This does not open full storage, item transfer, capacity upgrades, generic
  inventory / equipment management, schema changes, save migration, combat
  formula changes, or manual `save.json` edits.

Guild Quest Turn-in for Synthesis Unlock Live MVP remains the latest guild /
synthesis unlock bridge coverage:

- Guild live mode can show unlocked existing `QUESTS` and submit ready quest
  turn-ins through Python runtime validation.
- `quest_cave_gathering` turn-in consumes existing materials, grants existing
  quest rewards, and unlocks `shop_synthesis_01` through existing runtime unlock
  behavior.
- Dungeon clear report semantics remain separate: first-clear rewards still
  happen at route clear, and Guild report registration only records/display
  report status.
- This does not open a full guild / quest framework, new quest data, schema
  changes, save migration, combat formula changes, full synthesis, generic
  recipe bridge, multi-recipe synthesis coverage, or base-item upgrades.

Synthesis Single Recipe Craft Live MVP remains the current synthesis craft
coverage:

- `synthesis_screen` live mode loads a runtime-shaped ScreenModel and dispatches
  `craft_recipe`.
- The only allowed recipe is `recipe_piercing_bundle`.
- Python runtime remains gameplay authority through `game.recipe_available(...)`
  and `game.craft_recipe_message(...)`.
- This does not open full synthesis, generic recipe bridge, multi-recipe
  coverage, base-item upgrades, recipe / quest / dungeon changes, schema
  changes, save changes, combat formula changes, or crafting system refactors.

Task Zone routing:

- Live bridge plan and landed MVP status notes:
  `01_content/gui-runtime-bridge-plan-v1.md`
- Static prototype handoff and screen-level verification:
  `01_content/gui-html-static-prototype-progress-v1.md`
- GUI document routing and lifecycle index:
  `01_content/gui-planning-index.md`
- New-session short handoff:
  `01_content/codex-handoff-short.md`

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

Direct smoke and validation:

```powershell
python element_maze.py --smoke-test
python 06_tools\validate_data.py
```

Read-only content inventory:

```powershell
python 06_tools\content_inventory_report.py
python 06_tools\content_inventory_report.py --json
```

GUI static prototype checks are task-specific. Use fixture parsing, JavaScript
syntax checks, and browser checks for the touched screen only. GUI static checks
do not imply gameplay validation.

## Project Structure

- `element_maze.py`: game entry point.
- `01_content/`: content design, handoff, and planning docs.
- `02_schema/`: data contract docs.
- `03_engine/engine/`: runtime flow and gameplay rules.
- `04_data/data/`: runtime data tables.
- `05_assets/`: future/reference asset area.
- `06_tools/`: validation, smoke, bridge helper, and read-only inventory tools.
- `07_gui_prototype/`: HTML static prototype and limited local live bridge render
  surfaces.

## SSOT Rules

- `README.md`: compact project entry and stable capsule.
- `01_content/codex-handoff-short.md`: short new-session handoff.
- `01_content/gui-runtime-bridge-plan-v1.md`: GUI live bridge plan and landed
  live-slice status notes.
- `01_content/gui-html-static-prototype-progress-v1.md`: static prototype
  screen-level handoff and verification.
- `01_content/game-design.md`: content-design SSOT.
- `02_schema/*.schema.md`: data contracts.
- `04_data/data/*.py`: runtime data SSOT.
- `04_data/data/registry.py`: runtime data index and helper id sets.
- `06_tools/validate_data.py`: cross-table validation.
- `06_tools/content_inventory_report.py`: read-only inventory / drift report.
- `save.json`: runtime save output, not design data and not a manual edit target.

## Change Boundaries

- Do not treat HTML fixtures as gameplay SSOT.
- Do not copy gameplay rules into JavaScript prototypes.
- Do not read or write `save.json` manually.
- Do not modify runtime, data, schema, save, or combat formulas as part of GUI
  prototype or handoff work.
- Treat `not opened` / narrow MVP language as current-slice risk control, not as
  a closed-demo statement or permanent ban on future extension points.
- Do not expand a landed narrow live MVP into a full system without a new
  read-only planning gate and explicit owner approval.
- Do not start a formal asset pipeline from reference/mockup images.
- Do not let README, handoff, schema, and runtime data drift out of sync.

## Next-Step Boundary

The next implementation target is not pre-approved. Candidate follow-up currently
recorded for future planning is a read-only gate for broader synthesis coverage,
such as deciding whether to iterate more existing Mira recipe ids.

Storage deposit / withdraw, capacity upgrades, and generic inventory management
are not opened by the Storage Unlock & View MVP; they require a new read-only
planning gate and owner-approved exact scope.

Before any runtime, data, schema, save, combat, or broader GUI live bridge work,
start with a single-slice read-only planning gate. For ordinary static prototype
work, use the GUI static prototype skill and only the relevant screen files.
