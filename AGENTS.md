# AGENTS.md

Purpose: shared entry route for Codex and Antigravity sessions in this repository.
This file is governance, not project status. Read live project files for current state.

## 1. Agent Routing

- Codex session ops skill:
  `.codex/skills/element-maze-session-ops/SKILL.md`
- Codex GUI static prototype skill:
  `.codex/skills/element-maze-gui-static-prototype/SKILL.md`
- Antigravity session governance skill:
  `.antigravity/skills/element-maze-session-governance/SKILL.md`
- Antigravity GUI static prototype skill:
  `.antigravity/skills/element-maze-gui-static-prototype/SKILL.md`

Use the skill that matches the current agent. Do not treat one agent's command policy
as automatically valid for the other.

## 2. Startup Order

At the start of a new session, read only the Hot Zone defined in
`01_content/agent-startup-reading-list.md`.

Default startup route:

1. `AGENTS.md`
2. `01_content/agent-startup-reading-list.md`
3. The current agent's session ops/governance skill.
4. `README.md`
5. `01_content/codex-handoff-short.md`
6. `01_content/world-content-skeleton-v0.1.md`

For GUI static prototype tasks, also read the current agent's GUI static prototype
skill. Read detailed GUI progress only when the task needs screen-level detail.

## 3. GUI Static Prototype Route

Current GUI work lives in `07_gui_prototype/`.

For GUI static prototype work, load the current agent's GUI static prototype
skill and follow its GUI Static Sprint Mode rules. The detailed screen list,
current progress, and drift decisions live in README / handoff / planning docs,
not in AGENTS.md.

At this level, static GUI work remains limited to prototype render surfaces:
HTML/CSS/render-layer JS/fixtures, static navigation, UIAction logging, and
browser or syntax verification. It is not runtime gameplay work.

## 4. Runtime-Connected Prototype Exception

Runtime-connected prototype work is not the default GUI prototype mode. It is
allowed only when the user explicitly approves that exact scope.

When approved, first read `01_content/gui-runtime-bridge-plan-v1.md` and stop at
a read-only planning gate before implementation. Static prototype sprint approval
does not imply runtime bridge approval.

## 5. Reading Discipline

Do not full-load `01_content/gui-static-current-state-v1.md` at every startup.
It is the compact active GUI state; read it only when the task needs GUI status.
The historical verification log is
`01_content/archive/gui-html-static-prototype-progress-v1.md` and is not a
normal startup read.

Do not full-load `01_content/gui-planning-index.md` at every startup. It is a Task
Zone navigation index; read it only for GUI planning, drift audit, or task routing.

Do not load Cold Zone files unless the user explicitly names them.

## 6. Change Discipline

Do not modify `README.md`, `01_content/`, `07_gui_prototype/`, runtime, data,
schema, or save files unless the user explicitly approves that exact surface.

Do not stage, commit, push, create branches, or archive files unless explicitly asked.

Runtime/data/schema/save/combat work must stop at a read-only planning gate first.
Never manually read, write, or edit `save.json` unless the user explicitly approves
the exact runtime/save surface and the plan uses existing runtime behavior.
