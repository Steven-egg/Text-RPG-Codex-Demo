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

For GUI static prototype tasks, also read the current agent's GUI static prototype
skill. Read detailed GUI progress only when the task needs screen-level detail.

## 3. GUI Static Prototype Boundary

Current GUI work lives in `07_gui_prototype/`.

Landed static prototype screens:

1. Start Screen
2. Town Hub
3. Guild Screen
4. Synthesis Screen
5. Shop Screen
6. Workshop Screen
7. Storage Screen
8. Magic Shop Screen
9. World Map
10. Dungeon Exploration
11. Combat Screen

Allowed GUI prototype work:

- static fixtures
- render layer validation
- layout validation
- interaction validation
- navigation flow validation
- UIAction logging validation

Forbidden for GUI prototype work:

- Python runtime connection
- reading or writing `save.json`
- runtime, data, schema, save, or combat formula changes
- copying gameplay rules into JavaScript
- formal asset pipeline work
- treating reference images or mockup candidates as runtime assets

## 4. Reading Discipline

Do not full-load `01_content/gui-html-static-prototype-progress-v1.md` at every
startup. It is the detailed GUI handoff and verification log; read targeted sections
when a GUI task requires them.

Do not full-load `01_content/gui-planning-index.md` at every startup. It is a Task
Zone navigation index; read it only for GUI planning, drift audit, or task routing.

Do not load Cold Zone files unless the user explicitly names them.

## 5. Change Discipline

Do not modify `README.md`, `01_content/`, `07_gui_prototype/`, runtime, data,
schema, or save files unless the user explicitly approves that exact surface.

Do not stage, commit, push, create branches, or archive files unless explicitly asked.

Runtime/data/schema/save/combat work must stop at a read-only planning gate first.
