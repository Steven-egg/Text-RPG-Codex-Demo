# Element Maze

Purpose: compact project entry point for the playable Python CLI RPG, GUI
prototype, and current-game content planning. Detailed bridge status,
screen-level verification, and historical MVP notes live in Task Zone files.

## Current Stable Capsule

- Latest committed checkpoint:
  `c44ddb7 2026-07-19 feat(equipment): add unaffixed instance lifecycle baseline`.
- Active OneDrive worktree (not yet committed): B4B-2 adds three fixed static
  affixes (`major_sharp`, `minor_agile`, `minor_fire_ward`), detached resolver
  increments, and side-effect-free comparison views. B4B-3a renders those
  views in the CLI equipment summary and comparison panel. This remains outside
  random rolls, quality, `+N`, drops, shops, synthesis, GUI, and save work.
- Combat Progression v1 foundation, player-content, relic-passive, and balance
  slices are landed and covered by deterministic validation. The balance tools
  keep B4 as the canonical gameplay baseline; B5/B6 remain QA overlays.
- Element Maze already has a playable five-region mainline: Border / Fire, Ice,
  Earth, Thunder, and Final. The current runtime inventory reports 21 dungeon
  entries, 28 quests, 20 bosses, and 93 monsters. Treat this as the content
  foundation for a small complete RPG; future expansion is optional rather than
  a prerequisite for the existing route.
- The Python CLI runtime remains the gameplay authority.
- The CLI mainline has runtime data and progression scaffolding through Final.
- The Fire route is in runtime data and bridge coverage, including Ash
  Ravine, Cinder Seal Depths, three fire-mark shards, Guild / Temple / Church
  lookup closure, and Boss rule parity for Glen, Ash Guardian, and Cinder Seal
  Sentinel.
- Ice, Earth, Thunder, and Final display naming passes are complete in runtime
  data for dungeons, monsters, bosses, materials / key proofs, and quest title /
  description text.
- Relic v1 is complete as a four-element seal enshrinement flow: Fire, Ice,
  Earth, and Thunder have true seal key items, enshrined flags, validated Relic
  metadata, CLI placement behavior, and GUI bridge compatibility for
  `attune_relic`.
- Fire now consumes the three fire-mark shards at the Relic table after the
  Guild / Temple lookup closure, creates and enshrines the Fire seal, and
  unlocks Ice. Ice, Earth, and Thunder source items convert to true seals
  with their selected passive choices applied to stat and combat behavior.
- Final access is gated by all four enshrined elemental seals, not by Thunder Q5
  alone.
- `06_tools/naming_inventory_report.py` is a read-only naming inventory helper
  for duplicate display names and lightweight term-shape checks.
- Final display naming keeps `魔王城` as the region-facing target and reveals
  `災禍邪神 阿巴頓` as the final boss display identity.
- Each enshrined relic now offers a selectable passive choice, saved through
  the existing state flow and applied to the relevant stat or combat path.
  Additional relic systems remain separate future planning gates.
- Owner-approved player-side combat direction now lives in
  `01_content/combat-progression-design-v1.md`. It records the landed combat
  baseline and the boundaries for any later, separately approved slice.
- Basic facility CLI-parity bridge coverage is complete through Guild material
  buyback.
- The maintainability checkpoint is stable: shared GUI presentation helpers and
  facility ScreenModel extraction are in place; town facility CLI behavior now
  lives in `03_engine/engine/facilities.py`, pure payment / quest helper logic
  lives in `03_engine/engine/state.py`, and `game.py` keeps facade re-exports
  for GUI bridge compatibility.
- GUI finalized asset links are stable: combat monster runtime/live coverage is
  verified at 93/93, `mon_earth_bark_shell` renders in live GUI combat, combat
  backgrounds are organized by region, and facility backgrounds use the shared
  `07_gui_prototype/shared/facility-backgrounds.js` helper.
- Facility CSS convergence is landed: shop / guild facility
  background sizing now uses a facility background token alias with `cover`
  fallback for cross-viewport edge safety, shop / magic shop / synthesis
  typography is tokenized locally, and the facility-family short-viewport CSS
  convergence pass has Antigravity-reported Chrome Headless visual verification
  for shop, guild, magic shop, and synthesis.
- World Map localization and preview mapping are converged: player-facing map
  copy uses Traditional Chinese, while runtime IDs remain stable; live models
  and static fixtures provide data-driven preview image paths for towns,
  dungeons, and Main Dungeon phases through Final.

See `git status --short` before editing. The workspace may contain owner-side
document cleanup or archive changes.

## Content Skeleton

Current macro route and content planning lives in:

- `01_content/world-content-skeleton-v0.1.md`

Current macro decisions:

- Four core content elements: Fire, Ice, Earth, Thunder.
- Final region is a composite endgame zone, not a fifth core element.
- The existing Fire route uses the existing Border Town only; do not add an
  Ash Outpost.
- Ice / Earth / Thunder regions each default to one regional town and three
  dungeons: two minor dungeons plus one main two-phase dungeon.
- Current display naming coverage is complete through Final.
- Four-seal Relic v1 is landed as a progression / Final-gating layer with one
  selectable passive choice per enshrined relic; it does not open broad new
  facility systems.
- This skeleton does not approve runtime, data, schema, save, GUI, bridge,
  combat, class, relic, or asset-pipeline implementation.

## GUI State

- `07_gui_prototype/` remains the default GUI static prototype surface.
- Static prototype work validates render layer, layout, fixture shape,
  navigation, interaction, and UIAction logging only.
- Runtime-connected GUI work is opt-in and limited to already approved local
  live bridge slices.
- GUI monster image generation and finalized asset linking are complete and
  owner-finalized. Combat monster assets now live under
  `07_gui_prototype/combat_screen/assets/monsters/{fire,ice,earth,thunder,final}/`.
  The old raw / transparent monster folders were removed or superseded, and
  `fire/` is the formal replacement for the old transparent Fire / demo assets.
- Combat screen image mappings now point at finalized element folders, including
  `mon_earth_bark_shell`; combat monster runtime/live coverage is verified at
  93/93 with no missing mapped monster image files.
- Combat backgrounds now live under regional background folders, facility
  backgrounds use the shared facility-backgrounds helper, and OLD / source /
  check asset history is preserved as unlinked history only.
- Facility CSS convergence landed in CSS under
  `07_gui_prototype/{shop_screen,guild_screen,magic_shop_screen,synthesis_screen}/`.
  Antigravity reported Chrome Headless browser screenshot / viewport visual
  verification for the facility-family CSS convergence pass.
- World Map now renders localized Traditional Chinese presentation text and
  data-driven per-dungeon / per-phase preview images in both live mode and
  static fixture fallback. Main Dungeon map nodes use their localized shared
  dungeon names rather than English placeholder labels.
- No further monster image generation or asset-linking pass is planned.
- Detailed GUI bridge and screen status lives in Task Zone files, not this
  README.

Task Zone pointers:

- Archived task-chain record:
  `01_content/archive/task.md`
- World content detailed baselines:
  `01_content/world-content-baselines-v0.1.md`
- Combat progression design and implementation order:
  `01_content/combat-progression-design-v1.md`
- GUI live bridge plan and landed live-slice notes:
  `01_content/gui-runtime-bridge-plan-v1.md`
- GUI static prototype handoff and screen verification:
  `01_content/gui-static-current-state-v1.md`
- GUI document routing and lifecycle:
  `01_content/gui-planning-index.md`
- Facility-family responsibility baseline:
  `01_content/blueprints/gui-facility-shell-baseline-v0.1.md`

## How To Run

Recommended Python:

- Python 3.11.x.
- Keep `.venv/` local to each machine. Do not treat it as a synced or shared
  environment.
- Install dependencies from `requirements.txt`.

Create or refresh a local virtual environment:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

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
.\.venv\Scripts\python.exe .\element_maze.py
```

`.venv/` and `.venv*/` are local tooling only and are ignored by git.

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
.\.venv\Scripts\python.exe 06_tools\content_inventory_report.py
.\.venv\Scripts\python.exe 06_tools\content_inventory_report.py --json
.\.venv\Scripts\python.exe 06_tools\naming_inventory_report.py --region final
.\.venv\Scripts\python.exe 06_tools\smoke_test_combat_bridge.py
.\.venv\Scripts\python.exe 06_tools\smoke_test_progression_bridge.py
.\.venv\Scripts\python.exe 06_tools\smoke_test_temple_bridge.py
```

For docs-only cleanup, use markdown/status/diff checks. Runtime smoke is not
required unless runtime, data, schema, save, combat, or bridge behavior changes.

## Project Structure

- `element_maze.py`: game entry point.
- `01_content/`: content design, handoff, startup, and planning docs.
- `02_schema/`: data contract docs.
- `03_engine/engine/`: runtime flow and gameplay rules.
  - `game.py`: CLI lifecycle, save / load, main loop, dungeon and combat flows,
    and compatibility re-exports for extracted domains.
  - `facilities.py`: town facility CLI menus and shared facility actions.
  - `state.py`: durable state defaults, mutation helpers, stat calculation,
    progression checks, and pure state helpers.
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
- `01_content/combat-progression-design-v1.md`: owner-approved player-side
  combat progression design and future implementation order.
- `01_content/gui-runtime-bridge-plan-v1.md`: active GUI live bridge boundary
  and planning gate; historical detail is archived separately.
- `01_content/gui-static-current-state-v1.md`: compact current static prototype
  state and boundaries.
- `01_content/archive/gui-html-static-prototype-progress-v1.md`: historical
  static prototype screen and verification log.
- `01_content/blueprints/game-design.md`: content-design SSOT.
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

- produce a `dungeon.py` domain extraction read-only planning gate
- produce a dead-code cleanup gate for the unused legacy `buy_menu`
- produce an AI tooling / validation pipeline audit for future small tools
- produce a commit package or branch-closure summary for the current facility
  CSS convergence after owner review
- produce a read-only gate for the next exact GUI static CSS slice, such as
  button state tokens or panel / card pattern convergence
- refine `01_content/world-content-skeleton-v0.1.md`
- route old Hot Zone details into Task / Cold Zone
- produce a Hot Zone / branch-closure read-only sync check before future handoff
- produce a read-only implementation gate for one exact future slice
- produce a read-only planning gate for one exact future combat or progression
  slice

Still closed until a later exact-scope approval:

- runtime/data/schema/save/combat changes
- new quest data or broad quest framework work
- generic inventory/equipment, storage capacity, shop sell, generic sell, or
  new / expanded facility gameplay systems beyond the landed extraction
- formal class transfer, relic systems beyond the landed passive choices,
  endgame systems, settings persistence,
  or cross-screen preferences
- new GUI image generation, bridge expansion, or formal asset pipeline work
