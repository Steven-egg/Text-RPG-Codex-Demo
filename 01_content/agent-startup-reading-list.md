# Agent Startup Reading List - Element Maze

Purpose: keep new Codex and Antigravity sessions aligned without loading broad
history. This file defines loading zones only; it is not a project-status log.

Default rule: read the Hot Zone, then stop. Task Zone files are opened only when
the current task explicitly needs them. Cold Zone files are not loaded unless
the owner names them or the task cannot be handled without that history.

## 1. Hot Zone

New session minimum read order:

1. `AGENTS.md`
   - Shared Codex / Antigravity governance route.
2. `01_content/agent-startup-reading-list.md`
   - This loading-zone guide.
3. Current agent skill
   - Codex: `.codex/skills/element-maze-session-ops/SKILL.md`
   - Antigravity: `.antigravity/skills/element-maze-session-governance/SKILL.md`
4. `README.md`
   - Compact project entry, current stable capsule, run/verify basics, SSOT
     boundaries.
5. `01_content/codex-handoff-short.md`
   - Short new-session handoff: stable state, prohibitions, Task Zone routing,
     and next boundary.
6. `01_content/world-content-skeleton-v0.1.md`
   - Current macro route: the implemented Fire / Ice / Earth / Thunder / Final
     mainline shape, regional map mood, town/dungeon count decisions, and
     no-implementation boundary.

For GUI static prototype tasks, also read the current agent's GUI static
prototype skill:

- Codex: `.codex/skills/element-maze-gui-static-prototype/SKILL.md`
- Antigravity: `.antigravity/skills/element-maze-gui-static-prototype/SKILL.md`

Do not read `01_content/gui-static-current-state-v1.md`,
`01_content/gui-runtime-bridge-plan-v1.md`, or
`01_content/gui-planning-index.md` during ordinary startup unless the task needs
screen-level detail, bridge planning, GUI planning, drift audit, document
lifecycle, or task routing.

## 2. Task Zone

Open these only for matching tasks.

### Archived Task-Chain Record

- `01_content/archive/task.md`
  - Historical weekend / weekday task-chain board for docs drift control, asset inventory, and runtime slimming coordination. Open only when historical task-chain context is explicitly needed; do not treat it as current project status.

### World / Content Planning

- `01_content/world-content-skeleton-v0.1.md`
  - Hot Zone macro skeleton and current content-count decisions.
- `01_content/world-content-baselines-v0.1.md`
  - Task Zone detailed content baseline specifications for jobs, promotions, quests, and facilities.
- `01_content/combat-progression-design-v1.md`
  - Owner-approved player-side combat progression planning: job roles,
    equipment direction, race-aware statuses, relic passive choices, expected
    level bands, and the future implementation order. Read for combat,
    equipment, relic, growth, or monster-balance planning.
- `01_content/blueprints/regional-data-template-v0.1.md`
  - Task Zone template for reusable region data slots, ID naming, material
    timing, quest turn-in safety, and candidate-content handoff.
- `01_content/blueprints/game-design.md`
  - Content-design SSOT; open for named gameplay/content-design questions.
- `01_content/blueprints/full-act-structure.md`
  - Five-act long-term skeleton; open for act routing or long-form planning.
- `01_content/archive/act-2-content-plan.md`
  - Act 2 fire-demo detail and history; open only when Act 2 detail matters.
- `04_data/data/*.py`
  - Runtime data SSOT; read during runtime/data planning gates, not ordinary
    docs cleanup.
- `02_schema/*.schema.md`
  - Data contracts; read only when schema/data validation matters.

### GUI Static Prototype

- `01_content/gui-static-current-state-v1.md`
  - Compact current static prototype state and boundaries. Read only when the
    task needs GUI status.
- `01_content/gui-planning-index.md`
  - GUI document lifecycle, planning routing, drift audit, and archive candidate
    index.
- `01_content/blueprints/ui-flow-blueprint.md`
  - CLI thin-layer to GUI flow mapping.
- `01_content/blueprints/gui-screen-map.md`
  - Screen, ScreenModel, and UIAction map.
- `07_gui_prototype/<screen>/`
  - Read only the relevant screen's HTML/CSS/render-layer JS/fixtures.

### GUI Runtime Bridge

- `01_content/gui-runtime-bridge-plan-v1.md`
  - Compact runtime-connected prototype boundary and planning gate.
- `01_content/archive/gui-html-static-prototype-progress-v1.md`
  - Historical static prototype verification log; read only for named history
    or verification-trace work.
- `01_content/blueprints/gui-runtime-bridge-preflight-v1.md`
  - Read only when a bridge preflight or runtime-connected planning task
    requires it.
- `01_content/blueprints/gui-bridge-vertical-slice-contract-audit-v1.md`
  - Read only for bridge contract audits.

Runtime-connected prototype work is not implied by static prototype approval.
When the owner approves runtime-connected scope, first read the runtime bridge
plan and stop at a read-only planning gate before implementation.

### Runtime / Data / Schema / Combat

For gameplay, runtime, data, schema, save, combat, economy, inventory, or bridge
work, start with a read-only planning gate. Do not edit files until the owner
approves the exact surface.

## 3. Cold Zone

Cold Zone files are historical, long-form, or broad planning documents. Do not
load them during ordinary startup.

Examples:

- `01_content/archive/game-architecture.md`
- `01_content/archive/combat-growth-layering-plan.md`
- `01_content/archive/codex-session-snapshot.md`
- `01_content/archive/demo-playtest-notes.md`
- `01_content/archive/gui-implementation-platform-tradeoff.md`
- retired or superseded GUI prompt / mockup / wireframe docs listed in
  `01_content/gui-planning-index.md`
- long-form old backup folders or archive packages under `01_content/`

If Hot Zone status conflicts with current git or current files, report the drift
and use targeted read-only checks. Do not load broad Cold Zone history just to
reconstruct old decisions.

## 4. Archive Candidates

Archive candidates are no longer listed in this Hot Zone startup file. Their
logical lifecycle and routing live in `01_content/gui-planning-index.md`.

Do not physically move, delete, or archive files unless the owner explicitly
approves that exact docs surface and operation.

## 5. Change Discipline

- Do not read or write `save.json`.
- Do not modify runtime, data, schema, save, or combat formulas from a docs or
  GUI prototype task.
- Do not treat HTML fixtures as gameplay SSOT.
- Do not connect Python runtime for static prototype work.
- Do not stage, commit, push, create branches, or archive files unless
  explicitly asked.
- Keep Hot Zone docs compact. Move detailed verification, historical MVP notes,
  and screen-level records into Task / Cold Zone files.
