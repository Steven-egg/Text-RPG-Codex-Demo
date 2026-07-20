# AGENTS.md

Purpose: lightweight project entry point for Codex and Antigravity sessions.
Read live files relevant to the current task; this file is not a project-status record.

## 1. Agent Routing

- Codex session ops skill:
  `.codex/skills/element-maze-session-ops/SKILL.md`
- Codex GUI static prototype skill:
  `.codex/skills/element-maze-gui-static-prototype/SKILL.md`
- Antigravity session governance skill:
  `.antigravity/skills/element-maze-session-governance/SKILL.md`
- Antigravity GUI static prototype skill:
  `.antigravity/skills/element-maze-gui-static-prototype/SKILL.md`

Use the matching skill only when the task needs its specialized workflow.

## 2. Startup Order

Start with this file. Read `README.md`, handoff material, planning documents,
or task-specific files only when they help answer or complete the user’s
current request. Do not load a fixed Hot Zone by default.

## 3. GUI Static Prototype Route

Current GUI work lives in `07_gui_prototype/`.

For GUI work, load the current agent's GUI prototype skill and the relevant
screen files. Consult planning material when it materially helps the task.

## 4. Runtime-Connected Prototype Exception

For runtime-connected work, consult the bridge plan when it is relevant to the
implementation.

## 5. Reading Discipline

Read the smallest useful set of files. Avoid broad history unless it is needed
to resolve the current task.

## 6. Change Discipline

Act directly within the user’s requested scope: inspect the relevant files,
make the needed changes, and run proportionate verification. Use planning or
status documents when they help execution, not as a prerequisite to ordinary
work.
