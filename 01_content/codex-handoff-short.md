# Codex Handoff Short

Purpose: compact new-session handoff for Codex. Keep this file short. It should
tell a new session what is stable, what is forbidden, where details live, and
what the next boundary is.

## Stable State

- Work directory: `C:\Users\user\OneDrive\文字冒險遊戲`
- Latest local checkpoint recorded for this handoff:
  `[codex] feat(runtime): add four-seal relic flow`
  (use live `git log` for the exact hash).
- Python CLI runtime remains the playable game and gameplay authority.
- Act 1 is playable; Act 2 fire demo runtime / bridge coverage is complete for
  the current narrow slice.
- Ice, Earth, Thunder, and Final display naming passes are complete in runtime
  data for dungeons, monsters, bosses, materials / key proofs, and quest title /
  description text.
- Relic v1 is complete as a four-element seal enshrinement flow for Fire, Ice,
  Earth, and Thunder.
- Fire consumes the three fire-mark shards at the Relic table after Guild /
  Temple lookup closure, creates and enshrines the Fire seal, and unlocks Ice.
- Ice, Earth, and Thunder source items convert to true seals without combat
  bonuses, and Final unlock now requires all four enshrined elemental seals.
- `06_tools/naming_inventory_report.py` is available as a read-only naming
  inventory helper for duplicate display names and lightweight term-shape
  checks.
- Final display naming keeps `魔王城` as the region-facing target and reveals
  `災禍邪神 阿巴頓` as the final boss display identity.
- Relic resonance, active effects, passive effects, stat bonuses, resistance,
  skill links, and combat behavior remain future runtime / facility planning
  gates.
- GUI static prototype exists under `07_gui_prototype/` and remains static by
  default.
- A local runtime-connected GUI bridge exists only for explicitly approved
  blessed slices.
- Basic facility CLI-parity bridge coverage is complete through Guild material
  buyback.
- Boss Combat Rule Parity is complete for Glen, Ash Guardian, and Cinder Seal
  Sentinel.
- Element Maze is an expandable playable demo, not a closed demo. Narrow MVP
  language controls current-round risk; it does not close future extension
  points.

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

Read Task Zone docs only when the current task needs them. Do not load Cold Zone
files during ordinary startup.

## Current Content Planning

Macro content skeleton:

- `01_content/world-content-skeleton-v0.1.md`

Current decisions:

- Four core content elements: Fire, Ice, Earth, Thunder.
- Final region is a composite endgame zone, not a fifth core element.
- Existing fire demo route uses the existing Border Town only; do not add an
  Ash Outpost.
- Ice / Earth / Thunder regions default to one regional town and three dungeons:
  two minor dungeons plus one main two-phase dungeon.
- Current display naming coverage is complete through Final.
- Four-seal Relic v1 is landed as a progression and Final-gating layer only; it
  does not open relic effects, combat bonuses, or broad facility systems.
- This is planning only. It does not approve runtime, data, schema, save, GUI,
  bridge, combat, class, relic, or asset-pipeline work.

## Task Zone Routing

- GUI live bridge details and landed MVP status notes:
  `01_content/gui-runtime-bridge-plan-v1.md`
- GUI static prototype screen-level progress and verification:
  `01_content/gui-html-static-prototype-progress-v1.md`
- GUI planning / document lifecycle / archive candidate routing:
  `01_content/gui-planning-index.md`
- Facility-family Mockup-to-HTML responsibility baseline:
  `01_content/gui-facility-shell-baseline-v0.1.md`
- Runtime bridge approval route:
  read `01_content/gui-runtime-bridge-plan-v1.md` and stop at a read-only
  planning gate before implementation.
- GUI static prototype work:
  read `.codex/skills/element-maze-gui-static-prototype/SKILL.md` and only the
  relevant `07_gui_prototype/<screen>/` files.
- Content-design background:
  `01_content/game-design.md`, `01_content/full-act-structure.md`, and
  `01_content/act-2-content-plan.md` are Cold / Task Zone references. Open them
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
- Full shop, magic shop, synthesis, guild, quest, boss, dungeon, magic, skill,
  target-selection, or facility framework.
- Formal class transfer, class specialization gameplay, relic effects, endgame
  systems, or formal settings persistence.
- GUI bridge expansion, GUI visual implementation, image generation, or formal
  asset pipeline.

## Next-Step Boundary

No implementation is pre-approved.

Small safe next steps:

- produce a CLI world map / region routing read-only planning gate
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

Latest Relic v1 checkpoint verification:

- `python 06_tools\validate_data.py`
- `python element_maze.py --smoke-test`
- `python 06_tools\smoke_test_temple_bridge.py`
- `git diff --check`

Manual owner playtest after `56731f1` confirmed Demon King defeat completes
Final Q5, grants Guild reputation +500, shows the ending panel and
`MAIN STORY CLEAR` panel, then returns to the title screen.
