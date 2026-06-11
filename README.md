# 《元素迷宮：邊境冒險者》終端機版

Purpose: project-level entry point for the playable Python CLI RPG and its GUI
prototype work. This README should stay compact. Detailed GUI bridge status,
screen-level verification, and historical MVP notes live in Task Zone files.

## Current Stable Capsule

Git baseline:

- Latest stable checkpoint:
  `ad42c0e [owner] feat(gui): merge storage and workshop facility skins`
- Latest committed bridge baseline:
  `2ecca91 [antig] feat(gui): add Guild material sell bridge and fix Shop layout`
- Basic facility CLI-parity bridge coverage is complete through the existing
  Guild material-buyback behavior. See `git status --short` before editing.

Maintainability Checkpoint:
- Shared `resource_strip` has been moved to `gui_presentation.py`.
- The following facility ScreenModels have been extracted from `gui_actions.py`:
  - Shop, Magic Shop, Workshop, Storage, Synthesis, Temple, Relic Preview, Guild.
- Action dispatching, validation, and mutation are retained in `gui_actions.py`.
- Exploration/Combat, World Map/Town Hub, and Inn are temporarily not subject to further micro-extraction to avoid complexity.

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
- Shop + Magic Shop GUI Layout Normalization V0.5 first CSS-only checkpoint is
  complete through `c7729df`.
- Current facility planning has returned to a family-level
  Mockup-to-HTML shell baseline. AI facility hero images provide scene, NPC,
  lighting, and atmosphere; HTML/CSS/JS provides all UI and interaction; Python
  runtime remains gameplay authority.
- The owner has retired and removed `08_experiments/` after the facility
  skinning exploration completed. Its accepted results now live in the formal
  `07_gui_prototype/` screens; the old lab and merge-back route is historical,
  not a current work path.
- Future minor facility visual adjustments should target the formal prototype
  path directly after exact-scope approval. Use a short-lived feature branch for
  uncertain or multi-file work; do not recreate an experiment copy unless an
  explicit isolation need cannot be served by a branch.
- `01_content/facilities-visual-integration-spec-v0.1.md` is a paused Draft
  comparison reference. It does not authorize visual implementation.

Blessed local live bridge coverage:

| Area | Stable live scope |
|---|---|
| Start | `start_new_game`, `restart_game`, `load_game`; live entry copy and no-save / has-save states aligned with static Start Screen. |
| Town Hub | Live resource strip, facility nodes, synthesis entry unlock state, `open_world_map`, and live routing into approved facilities. Town Hub does not expose `save_game`. |
| Synthesis | Craft coverage for the four existing Mira recipes through Python runtime validation and `game.craft_recipe_message(...)`. |
| Inn | `rest_at_inn` deducts 30G and restores HP/MP through Python runtime behavior. |
| World Map | Runtime-backed location / route ScreenModel; main menu keeps `save_game` and shell-only `open_settings`; town return is via town node / detail action. |
| Dungeon / Combat | Approved traversal and combat loop slice, victory / retreat / defeat routing, route clear / resolved state, and Combat Skill Button MVP. |
| Guild | Clear report registration, existing `QUESTS` turn-ins, Boss Glen investigation, three-shard fire-mark inquiry, and existing `GUILD_MATERIAL_BUY_PRICES` material sell coverage with Python-side quantity / eligibility / transaction validation. |
| Guild x Dungeon Boss Glen | Special gating bridge plus UX cleanup: Scorched Mine 18/18 records `boss_glen_sighted`, Guild accepts `boss_glen_investigation_accepted`, Boss Glen challenge opens only after investigation acceptance, persistent Guild story hint cards guide Glen / Act 2 steps, and `quest_boss_glen` / Blood Map turn-in unlocks Ash Ravine through existing runtime progression. |
| Ash / Cinder presentation cleanup | Ash Ravine and Cinder Seal Depths use existing runtime progression while GUI copy avoids premature Boss / reward / unlock spoilers before the matching scout reports; owner hand test confirmed the progression flow reaches the Temple / Church handoff. |
| Shop | Data-driven coverage for all nine existing `SHOP_INVENTORY["travel"]` entries; purchases remain quantity-one, and accessories go to the backpack without auto-equip. |
| Magic Shop | Data-driven coverage for all existing `MAGIC_BOOKS`; learning remains server-validated, and debuff books follow the CLI special-magic category. |
| Workshop | Buy weapon & armor without auto-equip; equip weapons and owned non-weapon equipment; upgrade whitelisted recipes (`recipe_iron_sword_plus_1`, `recipe_leather_armor_plus_1`). |
| Storage | Unlock, view, and deposit / withdraw items through Python runtime state; storage capacity upgrades remain closed. |
| Temple | Live-mode loading, promotion requirement preview, moon well pray, fire-mark church bridge and lookup inquiry actions using Python runtime helpers. |
| Relic Preview | Altar screen live-mode loading, previewing registered relics (e.g., ash charm) and requirements, attune action placeholder. Formal relic effects remain closed. |


Guild x Dungeon Boss Glen live bridge state:

- The bridge uses two narrow runtime flags: `boss_glen_sighted` when Scorched
  Mine 18/18 reveals the strong presence, and
  `boss_glen_investigation_accepted` when the Guild accepts the investigation.
- Dungeon Exploration only discovers the clue; Guild turns that clue into the
  formal `quest_boss_glen` / Blood Map task and unlocks Boss Glen challenge.
- Owner manual hand test confirmed the deadlock is removed: the first Scorched
  Mine clear blocks direct Boss challenge with a Guild-facing hint, Guild can
  accept the investigation, returning to 18/18 opens Boss Glen combat, Blood Map
  can be reported after victory, and Ash Ravine / later CLI progression appears
  through the existing runtime bridge.
- `709dc6c` landed the player-facing UX cleanup: Guild story hints remain
  reviewable across Glen / Act 2 guidance states, Blood Map reward unlock keys
  render as player-facing labels, Dungeon Exploration keeps HP/MP in the resource
  strip while run Gold stays in current-run rewards, the dungeon event list can
  scroll and auto-scrolls to the newest event, and the action bar supports stable
  Boss / leave button placement.
- The Ash Ravine / Cinder Seal Depths presentation cleanup keeps the existing
  CLI runtime progression intact while making Guild and Dungeon Exploration
  wording less spoiler-like before scout reports are complete. Owner manual hand
  test confirmed Ash Ravine first clear, scout turn-in, Ash Boss, supply-line
  upgrade, Cinder Depths unlock, Cinder scout / Boss path, and Temple / Church
  handoff all progress through the bridge.
- Known MVP observation: Ash Ravine and Cinder Seal Depths currently share some
  fire-demo materials, so later scout turn-ins can be ready immediately. This is
  existing CLI MVP content/data reuse, not a regression in the presentation
  cleanup.
- This does not open a full quest framework, story hint framework, generic boss
  framework, full Act 2 progression cleanup, schema changes, save migration,
  combat formula changes, or manual `save.json` work.

Storage Deposit & Withdraw Live MVP remains part of the current live bridge
package:

- Town Hub can route to the Storage live screen, which loads a runtime-shaped `storage_screen_model(state)`.
- `unlock_storage` checks the existing runtime storage unlock cost, blocks insufficient Gold, deducts Gold on success, and sets `state["storage_unlocked"] = True`.
- After unlock, the screen displays live inventory, storage status, storage contents, and capacity.
- `deposit_item` and `withdraw_item` allow transferring items between player inventory and storage, enforcing runtime constraints and capacity limits.
- Storage capacity upgrades remain disabled with MVP-scope messaging.
- This does not open full storage system, capacity upgrades, generic inventory / equipment management, schema changes, save migration, combat formula changes, or manual `save.json` edits.

Workshop Armor Buy, Equip & Limited Upgrade Live MVP is included in the current
package:

- Workshop can buy existing weapon-shop weapons and armor-shop armor through
  `buy_equipment`; buying still does not auto-equip.
- Workshop can equip weapons and owned non-weapon equipment through approved
  bridge actions that reuse `game.equip_item(...)` and runtime slot data.
- `upgrade_equipment` is limited to existing whitelisted workshop recipes:
  `recipe_iron_sword_plus_1` and `recipe_leather_armor_plus_1`.
- This does not open accessory purchase, sell, generic unequip / comparison,
  non-whitelisted upgrades, full workshop, full synthesis, new equipment data,
  schema changes, save migration, combat formula changes, or manual `save.json`
  edits.

Guild Quest Turn-in and fire-mark inquiry coverage are included in the current
package:

- Guild live mode can show unlocked existing `QUESTS` and submit ready quest
  turn-ins through Python runtime validation.
- `quest_cave_gathering` turn-in consumes existing materials, grants existing
  quest rewards, and unlocks `shop_synthesis_01` through existing runtime unlock
  behavior.
- Dungeon clear report semantics remain separate: first-clear rewards still
  happen at route clear, and Guild report registration only records/display
  report status.
- `fire_mark_guild_inquiry` reuses
  `game.can_ask_fire_mark_guild_inquiry(...)` and
  `game.fire_mark_guild_inquiry(...)`; it keeps the three shards and enables the
  existing Guild -> Temple -> Church lookup progression without manually setting
  the prerequisite flag.
- This does not open a full guild / quest framework, new quest data, schema
  changes, save migration, combat formula changes, generic story inquiries, or
  generic sell beyond the existing Guild material-buyback behavior.

Phase B facility coverage landed in `eed7b4b`:

- `synthesis_screen` live mode loads a runtime-shaped ScreenModel and dispatches
  `craft_recipe` for the four existing Mira recipes:
  `recipe_fire_cloak`, `recipe_focus_pouch`, `recipe_heat_charm`, and
  `recipe_piercing_bundle`.
- Python runtime remains gameplay authority through `game.recipe_available(...)`
  and `game.craft_recipe_message(...)`.
- Shop iterates the existing travel inventory, and Magic Shop iterates existing
  `MAGIC_BOOKS`; neither adds new data or a generic facility framework.
- This does not open arbitrary recipes, new items or magic books, Shop sell,
  equipment sell, generic quantity selectors, generic inventory / equipment
  management, schema changes, save changes, combat formula changes, or crafting
  system refactors.

Guild Material Sell bridge landed in `2ecca91`:

- Guild live mode provides task / material-sell modes and lists only owned
  materials registered in the existing CLI `GUILD_MATERIAL_BUY_PRICES`.
- `sell_guild_material` validates item eligibility, positive integer quantity,
  owned quantity, and confirmation in Python before removing materials and
  adding the existing buyback total to Gold.
- The Guild ScreenModel refreshes material rows and resources after each sale.
  Shop live layout spacing and Guild task-list scrolling were also corrected.
- This does not open Shop sell, equipment sell, key/story-item sell, generic
  sell, economy rebalance, or generic inventory / equipment management.

Temple and Relic Altar Live MVP is included in the current package:

- Town Hub can route to Temple and Relic Altar live screens.
- Temple live screen loads a runtime-shaped `temple_screen_model(state)`. It previews job promotion requirements based on the database and checks if they are satisfied. Moon well pray deducts 30G and returns live state/message feedback.
- `fire_mark_church_bridge` and `fire_mark_church_lookup` actions are triggered by inquiry buttons when their respective runtime prerequisites (`should_show_fire_mark_church_bridge(state)` and `should_show_fire_mark_church_lookup(state)`) are met. They directly call Python gameplay helpers to modify story flags.
- The current package supplies the missing Guild-side prerequisite through
  `fire_mark_guild_inquiry`, so the live progression reaches Temple naturally.
- Relic Altar live screen loads a runtime-shaped `relic_preview_screen_model(state)`. It previews registered relics (like the ash charm) and lists their unlock requirements. Attuning a relic dispatches `attune_relic` action returning preview-only messages.
- This does not open formal class transfer, class specialization gameplay, formal relic system, relic effects, equipping/obtaining relics, or manual `save.json` edits.

Task Zone routing:

- Facility-family Mockup-to-HTML responsibility and configuration baseline:
  `01_content/gui-facility-shell-baseline-v0.1.md`
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

- God File / Maintainability Checkpoint is sufficiently converged.
- Endless ScreenModel micro-extraction is not recommended.
- Shop + Magic Shop GUI Layout Normalization V0.5 first CSS-only checkpoint is
  complete through `c7729df`.
- Facility skinning exploration is complete through the accepted formal
  prototype state. `08_experiments/` has been retired and removed by the owner.
- Facilities visual integration review is paused at
  `01_content/facilities-visual-integration-spec-v0.1.md`; no comparison
  candidate or CSS adjustment is currently approved.
- No additional image generation, HTML/CSS implementation, runtime work, or
  asset pipeline is pre-approved by this docs sync.
- Phase C convenience candidates, runtime/data/schema/save/combat remain deferred.

The next implementation target is not pre-approved. Basic facility CLI-parity
bridge coverage is complete through the existing Guild material-buyback
behavior.

Remaining Phase C convenience candidates are deferred:

1. Inventory / equipment management.
2. Storage capacity upgrade.
3. Bestiary detail / filtering.
4. Settings panel.

Phase C is not current work. Storage capacity upgrades, generic inventory
management, generic equipment management, non-whitelisted workshop upgrades, and
full workshop expansion remain closed until a later read-only planning gate and
owner-approved exact scope.

Before any runtime, data, schema, save, combat, or broader GUI live bridge work,
start with a single-slice read-only planning gate. For ordinary static prototype
work, use the GUI static prototype skill and only the relevant screen files.
