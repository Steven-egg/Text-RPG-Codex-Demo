---
name: element-maze-session-ops
description: Project-specific session operations for Element Maze. Use when Codex needs commit notes, status summaries, next-session handoff prompts, continuation gates, read-only catch-up, Git packaging, startup governance, or runtime planning gates. For GUI static prototype boundaries, load element-maze-gui-static-prototype.
---

# Element Maze Session Ops

## Core Rule

Treat this skill as a workflow guide, not a project-state snapshot. Always read the live repository files before answering. Do not rely on stale summaries inside this skill for current progress, next steps, or allowed scope.

Default to Traditional Chinese output unless the user asks otherwise.

## Read-Only Catch-Up

At new session startup, first follow `AGENTS.md` and `01_content/agent-startup-reading-list.md`:

- Default startup reads only the Hot Zone and the current Codex skill.
- Task Zone files are read only when the explicit task needs them.
- Cold Zone files are not bulk-loaded at startup.
- Do not reopen settled GUI decisions based on older historical files.

Full read-only catch-up is conditional, not required for every ordinary task.
Use full catch-up before producing any of these:

- commit package or commit summary
- handoff prompt or next-session prompt
- status summary or drift audit
- continuation decision after high context usage or long time since sync
- runtime/data/schema/save/combat planning gate

Full catch-up means gather current state with read-only commands and Hot Zone files:

1. Run `git status --short`.
2. Read recent commits with `git log --oneline --decorate --date=short --pretty=format:"%h %ad %s" -n 8`.
3. Read `AGENTS.md`.
4. Read `01_content/agent-startup-reading-list.md`.
5. Read `README.md`.
6. Read `01_content/codex-handoff-short.md`.
7. Read this skill file.

For ordinary GUI static sprint work, do not default to full catch-up. Read only:

1. `.codex/skills/element-maze-gui-static-prototype/SKILL.md`.
2. The relevant `07_gui_prototype/<screen>/` files for the touched screen(s).
3. Targeted handoff/progress sections only when screen-level detail, verification history, drift audit, or task routing needs them.

For GUI planning, drift audit, or task routing, read `01_content/gui-planning-index.md` only as a Task Zone index. Do not full-load `gui-static-current-state-v1.md`, `gui-planning-index.md`, or the archived progress log at every startup. Prefer the minimum necessary extra files. Do not read broad historical files unless the task requires history.

## Planning, Reporting, And Next Steps

Default to read-only analysis before planning, reviewing, restructuring skills or
docs, or touching runtime, bridge, schema, save, combat, data, or other
cross-system surfaces. Present the proposed slice and wait for explicit approval
before implementation.

For an already-approved GUI static sprint, do not stop for every small HTML/CSS,
fixture, render-layer JS, static navigation, or UIAction logging edit inside the
declared sprint surface. Keep moving within the approved sprint and surface only
new risks or scope changes.

Report only the boundaries relevant to the current task. Do not append a fixed
"no stage / commit / push" note unless the task involves Git, commit packaging,
handoff, or the user asks for it.

Verification is guidance, not ceremony. Suggest checks that fit the risk and
blast radius. Reserve strict verification gates for runtime, bridge, data,
schema, save, combat, and cross-system changes; use smaller checks for docs and
GUI static prototype edits.

After finishing a task, suggest useful next steps when they help the user choose
a path. Distinguish same-phase continuation from cross-phase escalation, and do
not start a new phase or broaden implementation without user approval.

For Codex sessions, if the next task is likely to require broad reading,
multi-zone work, or high context usage, briefly say so and let the user decide
whether to continue, split, or defer. Do not apply this as an Antigravity policy.

## Permanent Boundaries

Preserve these boundaries unless the user explicitly approves a different scope:

- Do not read or write `save.json`.
- Do not connect the Python runtime for GUI static prototype tasks.
- Do not treat HTML fixtures as gameplay SSOT.
- Do not copy gameplay rules into JavaScript prototypes.
- Do not modify runtime, data, schema, save, or combat formulas for GUI prototype or handoff tasks.
- Do not start a formal asset pipeline.
- For HTML static prototypes, use fixtures only to validate render layer, layout, interaction, navigation flow, and UIAction logging.
- Do not treat reference images or mockups as runtime assets.
- Do not commit, push, stage, or create branches unless the user explicitly asks.
- Do not make the skill duplicate project status that already lives in `README.md`, `codex-handoff-short.md`, or planning index files.

## Workflow Selection

Use the workflow that matches the request.

### Commit Package

Use when the user asks for commit content, commit message, commit summary, or text to paste into commit and push.

After read-only catch-up, produce:

- Suggested commit title.
- Commit body with the main behavioral or documentation changes.
- Changed files summary from git status or diff inspection when available.
- Verification performed.
- Not run / residual risk.
- Explicit note that no commit or push was performed unless it actually was.

When the user asks for commit content, prefer a single paste-ready commit block: subject on the first line, a blank line, then the body. Include `Changed files:` and `Verification:` sections when useful for future agent catch-up. Keep commit text in clear English unless the user asks otherwise.

Keep the title conventional and scoped, such as `docs(gui): ...`, `feat(gui): ...`, or `fix(gui): ...`, based on the actual changes. When Codex creates a commit, the subject must start with `[codex]`, for example `[codex] docs(governance): sync skill startup rules`. Commits produced by Antigravity use `[antig]`. Do not expand this into a large commit convention.

### Next-Session Prompt

Use when the user asks for a new conversation prompt, handoff prompt, continuation prompt, minimum read list, or session memory transfer.

After read-only catch-up, produce a paste-ready prompt containing:

- Work directory.
- Current stable state.
- Git state and latest relevant commit.
- Minimum required read list.
- Task-specific extra read list, if any.
- Current restrictions and forbidden actions.
- Next-step candidates.
- The smallest recommended next convergence item.

The prompt should be self-contained but compact. Put concrete paths and exact current boundaries in it.

### Session Continuation Gate

Use when the user mentions context usage percentage, context compression risk, whether to continue the current session, or whether to start a new session.

After read-only catch-up when needed, decide:

- Continue current session if the next task is very small, the relevant files were recently read, and the allowed surface is narrow.
- Recommend a new session if context usage is high, the next task requires broad reading, the workflow is changing, or the current session has just completed a stable convergence item.
- If recommending a new session, produce a compact next-session prompt with the minimum read list and current boundaries.
- If continuing, propose only one smallest safe task. Runtime/data/schema/save/combat work still requires a read-only preflight; GUI static sprint work follows the GUI skill's sprint preflight.
- Do not modify any files during this gate.

### Read-Only Catch-Up Summary

Use when the user asks to catch up, inspect current status, reverse engineer progress, or decide whether a next step is ready.

After read-only catch-up, produce:

- Current status summary.
- Whether the requested next phase is ready.
- The smallest recommended convergence item.
- Any blocking ambiguity or missing approval.

Do not propose implementation as already approved unless the user explicitly asks to start implementation.

### GUI Static Prototype Tasks

Use `.codex/skills/element-maze-gui-static-prototype/SKILL.md` for all `07_gui_prototype/` planning, preview, edit, URL, fixture, UIAction logging, and GUI drift-boundary details.

This session ops skill should not duplicate landed screen progress, server URL lists, or screen-level GUI decisions. Keep this file focused on startup governance, handoff, Git packaging, context gates, catch-up conditions, and runtime planning gates.

### Runtime Preflight

Use when the user asks to continue gameplay/runtime work.

For high-risk tasks involving schema, save, combat, engine flow, inventory, economy, or cross-system changes, the first round must be read-only planning. Do not edit files in that first round. Report affected files, risk, smallest safe slice, validation plan, and whether a higher reasoning model is needed.

Do a read-only boundary check first. Identify:

- The exact proposed slice.
- Files likely to be touched.
- Forbidden adjacent systems.
- Validation commands.
- Whether the task needs explicit user approval before edits.

Do not start runtime implementation from this skill alone.

## Output Style

Be concise and operational. Prefer the user's project vocabulary: `static prototype`, `fixtures`, `UIAction logging`, `handoff`, `最小讀取清單`, `下一步邊界`, and `最小收斂項目`.

When producing prompts for a future session, make them copy-paste ready and include the user's workspace path if known: `C:\Users\User\OneDrive\文字冒險遊戲`.
