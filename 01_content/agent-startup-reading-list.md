# Agent Startup Reading List - Element Maze

Purpose: keep new Codex and Antigravity sessions aligned without loading broad
history. This file defines loading zones only; it is not a project-status log.

Default rule: read the Hot Zone, then stop. Task Zone files are opened only when
the current task explicitly needs them. Cold Zone files are not loaded unless the
owner names them or the task cannot be handled without that history.

## 1. Hot Zone

New session minimum read order:

1. `AGENTS.md`
   - Shared entry route and cross-agent governance.
2. `01_content/agent-startup-reading-list.md`
   - This loading-zone guide.
3. Current agent skill
   - Codex: `.codex/skills/element-maze-session-ops/SKILL.md`
   - Antigravity: `.antigravity/skills/element-maze-session-governance/SKILL.md`
4. `README.md`
   - Compact project entry, current stable capsule, run/verify basics, SSOT
     boundaries.
5. `01_content/codex-handoff-short.md`
   - Short new-session handoff: latest stable point, current prohibitions,
     next-step boundary, and Task Zone routing.

For GUI static prototype tasks, also read the current agent's GUI static
prototype skill:

- Codex: `.codex/skills/element-maze-gui-static-prototype/SKILL.md`
- Antigravity: `.antigravity/skills/element-maze-gui-static-prototype/SKILL.md`

Do not read `01_content/gui-html-static-prototype-progress-v1.md` or
`01_content/gui-planning-index.md` during ordinary startup unless the task needs
GUI screen-level detail, GUI planning, drift audit, or task routing.

## 2. Task Zone

Open these only for matching tasks.

### GUI static prototype

- `01_content/gui-html-static-prototype-progress-v1.md`
  - Current static prototype handoff and screen-level verification. Read targeted
    sections only.
- `01_content/gui-planning-index.md`
  - GUI document lifecycle, planning routing, drift audit, and archive candidate
    index.
- `01_content/ui-flow-blueprint.md`
  - CLI thin-layer to GUI flow mapping.
- `01_content/gui-screen-map.md`
  - Screen, ScreenModel, and UIAction map.
- `07_gui_prototype/<screen>/`
  - Read only the relevant screen's HTML/CSS/render-layer JS/fixtures.

### GUI runtime bridge

- `01_content/gui-runtime-bridge-plan-v1.md`
  - Runtime-connected prototype plan, approved surfaces, and landed live-slice
    status notes.
- `01_content/gui-runtime-bridge-preflight-v1.md`
  - Read only when a bridge preflight or runtime-connected planning task requires
    it.
- `01_content/gui-bridge-vertical-slice-contract-audit-v1.md`
  - Read only for bridge contract audits.

Runtime-connected prototype work is not implied by static prototype approval.
When the owner approves runtime-connected scope, first read the runtime bridge
plan and stop at a read-only planning gate before implementation.

### Runtime / data / schema / combat

For gameplay, runtime, data, schema, save, combat, economy, inventory, or bridge
work, start with a read-only planning gate. Do not edit files until the owner
approves the exact surface.

## 3. Cold Zone

Cold Zone files are historical, long-form, or broad planning documents. Do not
load them during ordinary startup.

Examples:

- `01_content/game-design.md`
- `01_content/game-architecture.md`
- `01_content/full-act-structure.md`
- `01_content/act-2-content-plan.md`
- `01_content/combat-growth-layering-plan.md`
- `01_content/codex-session-snapshot.md`
- `01_content/demo-playtest-notes.md`
- `01_content/gui-implementation-platform-tradeoff.md`

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
- Do not modify runtime, data, schema, save, or combat formulas from a docs or GUI
  prototype task.
- Do not treat HTML fixtures as gameplay SSOT.
- Do not connect Python runtime for static prototype work.
- Do not stage, commit, push, create branches, or archive files unless explicitly
  asked.
