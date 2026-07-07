# Codex Handoff Short

Purpose: compact new-session handoff for Codex. Keep this file short. It should
tell a new session what is stable, what is forbidden, where details live, and
what the next boundary is.

## Stable State

- Work directory: `C:\Users\user\OneDrive\文字冒險遊戲`
- Latest local checkpoint recorded for this handoff:
  `029c10b 2026-06-30 [antig] refactor(runtime): extract dungeon domain`.
- For the full stable capsule details (CLI runtime authority, Relic v1
  flow, naming passes, and bridge parity), see [README.md](../README.md#current-stable-capsule).
- Phase 3 facilities extraction is landed: town facility CLI behavior now lives
  in `03_engine/engine/facilities.py`, pure payment / quest helpers live in
  `03_engine/engine/state.py`, and `game.py` keeps facade re-exports for GUI
  bridge compatibility.
- Note: Element Maze is an expandable playable demo, not a closed demo.
  Narrow MVP language controls current-round risk; it does not close
  future extension points.

See `git status --short` before editing. There may be owner-side docs/archive
cleanup in the worktree.

## Hot Zone Startup

Minimum Codex startup read order:

1. `AGENTS.md`
2. `01_content/agent-startup-reading-list.md`
3. `.codex/skills/element-maze-session-ops/SKILL.md`
4. `README.md`
5. `01_content/codex-handoff-short.md`
6. `01_content/world-content-skeleton-v0.1.md`

For GUI static prototype tasks, also read:

- `.codex/skills/element-maze-gui-static-prototype/SKILL.md`

For monster asset candidate generation, also read:

- `C:\Users\User\.codex\skills\.system\imagegen\SKILL.md`
- `04_data/data/monsters.py`
- `04_data/data/dungeons.py`
- `01_content/blueprints/naming-lexicon-v0.1.md`

Read Task Zone docs only when the current task needs them. Do not load Cold Zone
files during ordinary startup.

## Current Content Planning

Macro content skeleton:

- `01_content/world-content-skeleton-v0.1.md`

Current decisions:

- For the full content decisions (core elements, region town/dungeon
  counts, and relic progression boundaries), see [README.md](../README.md#content-skeleton).
- This is planning only. It does not approve runtime, data, schema, save, GUI,
  bridge, combat, class, relic, or asset-pipeline work.

## Current Asset Candidate Status

Monster image generation is complete and owner-finalized. This is not runtime,
data, schema, save, combat, bridge, or formal asset-pipeline approval.

- Combat monster assets now live under:
  `07_gui_prototype/combat_screen/assets/monsters/{fire,ice,earth,thunder,final}/`
- The old raw / transparent monster folders were removed or superseded.
- `fire/` is the formal replacement for the old transparent Fire / demo assets.
- No further monster image generation is planned.
- `OLD/` folders and source / check files are owner-side asset history; do not
  link, delete, move, or clean them unless the owner approves that exact asset
  surface.
- Next smallest GUI step: update `07_gui_prototype/combat_screen/combat-screen.js`
  imageSrc mappings to point at the finalized element folders. This remains
  static prototype display-layer work only.

## Task Zone Routing

- Task coordination board:
  `../task.md`
- World content detailed baselines:
  `01_content/world-content-baselines-v0.1.md`
- GUI live bridge details and landed MVP status notes:
  `01_content/gui-runtime-bridge-plan-v1.md`
- GUI static prototype screen-level progress and verification:
  `01_content/gui-html-static-prototype-progress-v1.md`
- GUI planning / document lifecycle / archive candidate routing:
  `01_content/gui-planning-index.md`
- Facility-family Mockup-to-HTML responsibility baseline:
  `01_content/blueprints/gui-facility-shell-baseline-v0.1.md`
- Runtime bridge approval route:
  read `01_content/gui-runtime-bridge-plan-v1.md` and stop at a read-only
  planning gate before implementation.
- GUI static prototype work:
  read `.codex/skills/element-maze-gui-static-prototype/SKILL.md` and only the
  relevant `07_gui_prototype/<screen>/` files.
- Content-design background:
  `01_content/blueprints/game-design.md`, `01_content/blueprints/full-act-structure.md`, and
  `01_content/archive/act-2-content-plan.md` are Cold / Task Zone references. Open them
  only for named content-design or history tasks.

## Explicitly Not Open

Interpretation rule: `Explicitly Not Open` means not approved in the current
slice. It is not a permanent ban or demo freeze.

- Runtime/data/schema/save/combat changes.
- Manual `save.json` work.
- New quest data or broad quest framework changes.
- Full inventory / equipment management.
- Storage capacity upgrade.
- Shop sell, equipment sell, generic sell, generic unequip, comparison, or
  generic workshop framework.
- New or expanded shop, magic shop, synthesis, guild, quest, boss, dungeon,
  magic, skill, target-selection, or facility gameplay framework beyond the
  landed extraction.
- Formal class transfer, class specialization gameplay, relic effects, endgame
  systems, or formal settings persistence.
- GUI bridge expansion, new GUI image generation, or formal asset pipeline.

## Next-Step Boundary

No implementation is pre-approved.

Small safe next steps:

- link finalized combat monster images in the GUI static prototype after exact
  `07_gui_prototype/combat_screen/combat-screen.js` approval
- produce a `dungeon.py` domain extraction read-only planning gate
- produce a dead-code cleanup gate for the unused legacy `buy_menu`
- produce an AI tooling / validation pipeline audit for future small tools
- refine `01_content/world-content-skeleton-v0.1.md`
- keep Hot Zone docs short and move historical detail to Task / Cold Zone
- produce a read-only planning gate for one exact future slice

For docs-only sync, restrict changes to explicitly approved markdown surfaces and
do not touch runtime, JavaScript, data, schema, save, or combat formulas.

For future runtime/data/schema/save/combat or broader GUI live bridge work, start
with a single-slice read-only planning gate and name the exact files likely to be
touched.

## Verification

Latest detailed verification history lives in Task Zone files. For docs-only
cleanup, status/diff review is enough. Runtime smoke is required only when
runtime, data, schema, save, combat, or bridge behavior changes.

Latest facilities extraction checkpoint verification:

- `python 06_tools\validate_data.py`
- `python element_maze.py --smoke-test`
- all current `06_tools\smoke_test_*.py` bridge smoke tests
- `python 06_tools\smoke_test_temple_bridge.py`
- `git diff --check`

Manual owner playtest after `56731f1` confirmed Demon King defeat completes
Final Q5, grants Guild reputation +500, shows the ending panel and
`MAIN STORY CLEAR` panel, then returns to the title screen.
