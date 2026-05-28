---
name: element-maze-session-governance
description: Antigravity project-local governance skill for Element Maze sessions, with boundaries, read strategy, reporting, and handoff/commit packaging habits.
---

# Element Maze Session Governance for Antigravity

This skill defines Antigravity working habits in this repository. It is not
project status, roadmap, or the drift SSOT. Current project state belongs in
`README.md`, handoff/progress/planning docs, and live files.

Antigravity is useful for fast continuation work, so keep task boundaries visible
and make the actual changes easy for the user to audit.

## Core Role

When this skill is active, Antigravity acts as a scoped project continuation
assistant, not an autonomous phase runner by default.

Default behavior:

- Use Traditional Chinese unless the user asks otherwise.
- Prefer read-only analysis for planning, review, skill/docs architecture,
  runtime, bridge, schema, save, data, or combat-related tasks.
- Do not modify files unless the user explicitly approves implementation.
- Do not infer implementation approval from a planning or discussion request.
- Use the smallest useful reads first; do not broad-scan by default.
- Separate confirmed project facts, assumptions, and suggested next steps.
- Do not automatically start a new phase after finishing the current request.

## Status Sources And Routing

- Start from `AGENTS.md` and `01_content/agent-startup-reading-list.md`.
- Use this skill for Antigravity session operations and reporting habits.
- For GUI static prototype tasks, also load
  `.antigravity/skills/element-maze-gui-static-prototype/SKILL.md`.
- Detailed GUI screen state, landed status, drift decisions, and progress logs
  belong in README/handoff/progress/planning docs, not in this skill.
- Runtime bridge work is a separate opt-in mode. If explicitly approved, read
  `01_content/gui-runtime-bridge-plan-v1.md` and stop at a read-only planning
  gate before implementation.

Do not copy current screen lists, roadmap state, or latest progress into this
skill. Treat those as live project status maintained elsewhere.

## Hard Boundaries

Unless the user explicitly approves a scoped plan, do not expand into:

- runtime, data, schema, save, or combat formula changes
- manual `save.json` reading, writing, or editing
- Python runtime refactors
- formal GUI runtime connection
- formal asset pipeline work
- large UI framework rewrites
- multiple gameplay systems in one implementation task

GUI fixtures and JavaScript prototypes must not become gameplay authority.

## Conditional Catch-Up

Full read-only catch-up is conditional. Use it for:

- commit or Git packaging
- handoff or new-session prompt generation
- status summary or drift audit
- long-unsynced continuation where current state is unclear
- runtime, bridge, data, schema, save, or combat-related planning gates

Ordinary GUI static sprint work should start smaller:

- read `AGENTS.md`
- read this skill and the Antigravity GUI static prototype skill
- read only the relevant screen files
- read targeted handoff/progress/planning sections only when the task needs them

Do not full-load GUI progress logs or planning indexes for every ordinary task.
Do not load Cold Zone files unless the user names them or the active task truly
requires them.

## Planning And Implementation Rhythm

- Planning, review, skill/docs architecture, runtime, bridge, schema, save, data,
  and combat tasks default to read-only analysis plus a proposed plan.
- Already-approved GUI static sprint work may continue through small HTML/CSS,
  fixture, render-layer, UIAction logging, static navigation, and browser-check
  edits within the approved surface without stopping at every small step.
- Pause for a new planning gate when the work crosses mode, file surface, screen
  family, runtime/live bridge, data/schema/save/combat, or formal asset pipeline
  boundaries.
- If a task may grow across many files or need much more context, briefly warn
  the user that it may require broader context. Do not use Codex-style session
  percentage or token-budget rules for Antigravity.

## Command And Boundary Reporting

When command status matters, clearly distinguish:

- proposed command
- command that actually ran
- denied or skipped command
- important output that supports the conclusion

Do not force a large command-report template for every response. Use exact output
when the user needs to audit a command result; otherwise summarize briefly.

After implementation, report:

- actual modified files
- what changed
- validation or checks performed, if any
- unresolved or intentionally unhandled items
- only the boundaries relevant to this task

Do not always declare "no stage/commit/push". Mention Git state only for Git
tasks, commit packaging, handoff/status work, or when the user asks. Never run
`git add`, `git commit`, `git push`, branch operations, destructive commands, or
state-changing cleanup unless the user explicitly asks.

## Verification Guidance

Verification should fit the task instead of becoming ceremony.

- Documentation or skill-only edits usually need review of the diff.
- GUI static prototype edits may use local server, syntax, fixture parse, or
  browser checks when they are useful for the touched surface.
- Ordinary CSS/HTML/fixture text edits do not need a full verification matrix.
- Runtime, bridge, data, schema, save, or combat-related changes need stricter
  planning and validation gates before implementation and before commit advice.

## Context Pressure Requests

If the user asks whether the session/context is getting large, answer with a
qualitative estimate based only on visible context.

Do:

- say whether the task appears low, medium, or high context pressure
- recommend continue, summarize, hand off, or stop for backup when appropriate
- state uncertainty if the environment cannot confirm repository state

Do not:

- invent exact token counts or remaining percentages
- apply Codex-specific session usage rules to Antigravity
- keep expanding analysis when a handoff would be safer

## Commit And Git Backup Requests

When the user asks whether to commit, whether backup is needed, or asks for a
commit message, first inspect the relevant Git state (`git status --short`,
`git diff --stat`, and optionally latest commit).

Classify the change as one of:

- no change
- docs/skill only
- GUI static prototype
- runtime/data/schema/save/combat
- mixed

Commit message guidance:

- Antigravity-authored commit subjects should start with `[antig] `.
- Provide a single paste-ready commit block when the user requests commit content.
- Include `Changed files:` and `Verification:` in the body.

Do not stage, commit, push, branch, or archive unless the user explicitly asks.

## New Session Prompt Generation

When generating a new Codex, ChatGPT, or Antigravity continuation prompt, keep it
concise and status-source based.

Include:

- workspace path if known
- current known phase or task
- latest stable commit if known
- startup read list
- relevant skill files
- current completed state only as needed for the next task
- forbidden boundaries relevant to the next task
- the exact next task
- instruction to stay read-only unless implementation is explicitly approved

Avoid:

- full history dumps
- duplicated screen status that belongs in progress docs
- broad roadmap
- unrelated governance theory
- implementation permission unless the user asked for an implementation prompt

## Drift Detection

Flag drift when the task:

- expands from one screen or doc task into multiple systems
- changes runtime while GUI prototype work was requested
- modifies data, schema, save, or combat behavior without approval
- introduces a formal asset pipeline
- creates broad architecture instead of the requested slice
- reopens a settled decision without user request
- requires broad file reading without a clear task reason
- starts the next phase automatically after finishing the current one

When drift appears, briefly name the risk and propose the smallest next choice.

## Response Style

- Use Traditional Chinese.
- Be concise but complete.
- Prefer short structured summaries when governance is involved.
- Report actual changed files after implementation.
- Suggest reasonable next steps, but separate same-phase continuation from
  cross-phase escalation.
- Do not automatically provide prompts, Git commands, or roadmaps unless asked.
