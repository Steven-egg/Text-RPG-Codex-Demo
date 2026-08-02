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
or task-specific files only when they help answer or complete the user's
current request. Do not load a fixed Hot Zone by default.

## 3. GUI Static Prototype Route

Current GUI work lives in `07_gui_prototype/`.

For GUI work, load the current agent's GUI prototype skill and the relevant
screen files. Consult planning material when it materially helps the task.

## 4. Runtime-Connected Prototype Exception

For runtime-connected work, consult the bridge plan when it is relevant to the
implementation.

## 5. Autonomous Work By Phase

Read the live files that are useful for the task, then complete the requested
outcome as one coherent piece of work. Make normal implementation decisions
without a planning or approval checkpoint.

### Feedback Maintenance

For user-reported sound, translation, presentation, usability, runtime, or
reproducible gameplay issues, own the complete focused fix: diagnose, edit all
necessary supporting files, verify it proportionately, and update the relevant
current documentation when it changes the maintained behaviour.

### Documentation And Repository Hygiene

Keep the active documentation surface small and useful. Consolidate overlapping
documents, move completed work and historical handoffs to `01_content/archive/`,
move unapproved future work to `01_content/blueprints/`, and delete files fully
superseded by the current source of truth. Preserve a recoverable Git history:
make moves explicit and leave a concise retirement note or commit message when
it improves later recovery.

### Feature Work

Once the user names the desired feature or outcome, decide the ordinary
technical details and implement all necessary local changes, including focused
tests, fixtures, and documentation. Keep the implementation aligned with the
existing Python/data gameplay authority.

### Release Work

Build, package, inspect, and verify release candidates autonomously. Treat the
decision to publish externally, promote a branch, or declare a formal release
as an Owner decision after the supporting evidence is ready.

## 6. Decision Rule

Do not split ordinary work into planning, approval, or micro-task phases merely
to report progress. Create phases only for real dependencies, independent
acceptance boundaries, or a checkpoint requested by the user. State reasonable
assumptions and proceed; request direction only when it would change the
requested product outcome or require an external decision.
