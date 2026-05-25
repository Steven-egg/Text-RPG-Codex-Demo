---
name: element-maze-session-ops
description: Project-specific session operations for Element Maze. Use when Codex needs to prepare commit notes, summarize end-of-session status, generate a next-session handoff prompt with the minimum read list, decide whether to continue the current session or start a new one, perform read-only project catch-up, classify HTML static prototype work stages, or enforce GUI static prototype boundaries for this repository.
---

# Element Maze Session Ops

## Core Rule

Treat this skill as a workflow guide, not a project-state snapshot. Always read the live repository files before answering. Do not rely on stale summaries inside this skill for current progress, next steps, or allowed scope.

Default to Traditional Chinese output unless the user asks otherwise.

## Read-Only Catch-Up

Before producing a commit package, handoff prompt, next-session prompt, continuation decision, or status summary, gather current state with read-only commands and files:

1. Run `git status --short`.
2. Read recent commits with `git log --oneline --decorate --date=short --pretty=format:"%h %ad %s" -n 8`.
3. Read `README.md`.
4. Read `01_content/codex-handoff-short.md`.

For GUI static prototype work, also read:

1. `01_content/gui-planning-index.md`.
2. `01_content/gui-html-static-prototype-progress-v1.md`.

For task-specific context, use `01_content/gui-planning-index.md` or the relevant handoff file to decide what to read next. Prefer the minimum necessary extra files. Do not read broad historical files unless the task requires history.

## Permanent Boundaries

Preserve these boundaries unless the user explicitly approves a different scope:

- Do not read or write `save.json`.
- Do not connect the Python runtime for GUI static prototype tasks.
- Do not treat HTML fixtures as gameplay SSOT.
- Do not copy gameplay rules into JavaScript prototypes.
- Do not modify runtime, data, schema, save, or combat formulas for GUI prototype or handoff tasks.
- Do not start a formal asset pipeline.
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

Keep the title conventional and scoped, such as `docs(gui): ...`, `feat(gui): ...`, or `fix(gui): ...`, based on the actual changes.

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
- If continuing, propose only one smallest safe task and require read-only preflight before implementation.
- Do not modify any files during this gate.

### Read-Only Catch-Up Summary

Use when the user asks to catch up, inspect current status, reverse engineer progress, or decide whether a next step is ready.

After read-only catch-up, produce:

- Current status summary.
- Whether the requested next phase is ready.
- The smallest recommended convergence item.
- Any blocking ambiguity or missing approval.

Do not propose implementation as already approved unless the user explicitly asks to start implementation.

### GUI Static Prototype Preflight

Use for Start Screen, Town Hub, Guild, World Map, Dungeon Exploration, Combat Screen, Synthesis Screen, Shop Screen, or other `07_gui_prototype/` tasks.

Always restate these GUI-specific boundaries in the output or plan when relevant:

- Static fixtures only.
- Validate render layer, layout, interaction, and UIAction logging only.
- No Python runtime adapter.
- No `save.json` access.
- No runtime, data, schema, or combat formula changes.
- No formal asset pipeline.
- Reference images and mockups are visual references, not runtime assets.

Before editing or planning an HTML static prototype, run this decision gate:

1. Classify the current work stage.
   - `content mapping`: Align fixture fields, render surfaces, and UIAction meaning. Prioritize what data appears and which actions exist.
   - `layout refinement`: Adjust CSS, spacing, proportions, responsive behavior, and small HTML class structure. Do not change gameplay meaning.
   - `player-facing polish`: Improve readable hierarchy, information density, debug-log visibility, labels, empty states, and user-facing feedback.
   - `reference alignment`: Compare against a mockup/reference for layout weight, panel role, text-safe area, and character or NPC presence only.
2. Declare the allowed surface for this pass.
   - Examples: `styles.css only`, `CSS + fixture display copy`, `render-layer JS only`, or `HTML/CSS/fixture within 07_gui_prototype only`.
   - If the pass is limited to layout, CSS, fixture, or render layer, do not modify runtime, data, schema, save, or combat formulas.
3. Decide whether mockup/reference reading is needed.
   - Read mockups only for `reference alignment` or explicit user review tasks.
   - Use mockups for layout weight, panel role, text-safe area, and character presence.
   - Do not copy mockup text into data, treat the image as a runtime background, or infer gameplay rules from the image.
4. Decide the debug log stance.
   - Player-facing passes should collapse or minimize large debug areas by default.
   - Debug/testing passes may keep UIAction Log visible if it is needed for interaction verification.
   - Never let a large debug log permanently dominate the primary player layout.
5. Decide whether documentation must be updated.
   - Pure CSS/layout micro-tuning usually does not need docs.
   - Update handoff/progress docs when a new screen lands, a baseline is accepted, a navigation route changes, a prototype boundary changes, or verification records need to be preserved.

For a new prototype planning prompt, include the expected layout pattern, fixture names, key UIAction events, navigation target, and verification checklist, but keep final implementation decisions aligned with live planning docs.

### GUI Prototype Server Helper

Use when the user asks how to launch, preview, smoke test, or browser test HTML static prototypes.

Always remind the user to use a local HTTP server rather than `file://`, because fixture `fetch()` calls may fail from direct file URLs.

Standard server root:

```text
C:\Users\User\OneDrive\文字冒險遊戲\07_gui_prototype
```

Standard command:

```powershell
cd C:\Users\User\OneDrive\文字冒險遊戲\07_gui_prototype
python -m http.server 8000
```

If the repo helper exists, prefer telling the user to run:

```powershell
.\start_gui_prototype_server.bat
```

Standard URLs:

- Start Screen: `http://localhost:8000/start_screen/index.html`
- Town Hub: `http://localhost:8000/town_hub/index.html`
- Guild Screen: `http://localhost:8000/guild_screen/index.html`
- World Map: `http://localhost:8000/world_map/index.html`
- Dungeon Exploration: `http://localhost:8000/dungeon_exploration/index.html`
- Combat Screen: `http://localhost:8000/combat_screen/index.html`
- Synthesis Screen: `http://localhost:8000/synthesis_screen/index.html`
- Shop Screen: `http://localhost:8000/shop_screen/index.html`
- Workshop Screen: `http://localhost:8000/workshop_screen/index.html`

When a new prototype screen is added, update this URL list in the project-local skill copy and sync it to the user skill copy.

### Runtime Preflight

Use when the user asks to continue gameplay/runtime work.

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
