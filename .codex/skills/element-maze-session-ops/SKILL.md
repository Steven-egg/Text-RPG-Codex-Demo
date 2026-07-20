---
name: element-maze-session-ops
description: Lightweight session operations for Element Maze: current status, handoff, Git packaging, and task-focused project orientation.
---

# Element Maze Session Ops

Use this skill only for status summaries, handoffs, continuation decisions,
commit packaging, or other session-operation requests. It is not required for
ordinary implementation work.

## Working Principle

Read the smallest set of live repository files needed for the task. Do not
perform a fixed startup reading sequence or load project history by default.
Default to Traditional Chinese unless the user asks otherwise.

## Status And Handoff

When the user asks for current status, a handoff, or a continuation decision,
inspect the current Git state and the files relevant to that request. Summarize
the stable state, the active work, useful next steps, and any uncertainty that
cannot be resolved from the repository.

## Execution

For implementation requests, act within the user’s stated scope: inspect,
edit, verify, and report the result. Do not require a separate planning round
or a pre-implementation approval gate. Use a proportionate check suited to the
change.

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
- Relevant task notes, if any.
- Next-step candidates.
- The smallest recommended next convergence item.

The prompt should be self-contained but compact. Put concrete paths and exact current boundaries in it.

### Session Continuation Gate

Use when the user mentions context usage percentage, context compression risk, whether to continue the current session, or whether to start a new session.

After read-only catch-up when needed, decide:

- Continue current session if the next task is very small, the relevant files were recently read, and the allowed surface is narrow.
- Recommend a new session if context usage is high, the next task requires broad reading, the workflow is changing, or the current session has just completed a stable convergence item.
- If recommending a new session, produce a compact next-session prompt with the minimum read list and current boundaries.
- If continuing, state the next useful task and proceed when the user has asked for implementation.

### Read-Only Catch-Up Summary

Use when the user asks to catch up, inspect current status, reverse engineer progress, or decide whether a next step is ready.

After read-only catch-up, produce:

- Current status summary.
- Whether the requested next phase is ready.
- The smallest recommended convergence item.
- Any blocking ambiguity or missing approval.

When implementation is requested, proceed directly within the stated scope.

### GUI Static Prototype Tasks

Use `.codex/skills/element-maze-gui-static-prototype/SKILL.md` for all `07_gui_prototype/` planning, preview, edit, URL, fixture, UIAction logging, and GUI drift-boundary details.

This session ops skill should not duplicate landed screen progress, server URL lists, or screen-level GUI decisions.

### Runtime Preflight

Use when the user asks to continue gameplay/runtime work.

For runtime work, inspect the relevant implementation, make the requested
change, and run proportionate verification.

## Output Style

Be concise and operational. Prefer the user's project vocabulary: `static prototype`, `fixtures`, `UIAction logging`, `handoff`, `最小讀取清單`, `下一步邊界`, and `最小收斂項目`.

When producing prompts for a future session, make them copy-paste ready and include the user's workspace path if known: `C:\Users\User\OneDrive\文字冒險遊戲`.
