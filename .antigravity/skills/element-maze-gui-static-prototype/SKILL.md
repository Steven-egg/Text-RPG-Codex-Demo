---
name: element-maze-gui-static-prototype
description: Project-specific GUI static prototype boundaries for Element Maze. Use when Antigravity plans, reviews, previews, or edits 07_gui_prototype HTML static prototype work, server URLs, fixture boundaries, UIAction logging, or GUI drift control.
---

# Element Maze GUI Static Prototype

## Core Rule

This skill defines GUI static prototype working habits and boundaries. It is not
a progress log. Current screen state, landed status, detailed verification logs,
and drift decisions belong in README, handoff, progress, and planning docs.

Default to Traditional Chinese output unless the user asks otherwise.

## Current Scope

GUI static prototypes live in:

```text
07_gui_prototype/
```

For current screen folders, landed screens, and detailed status, read live files
or targeted sections of `01_content/gui-html-static-prototype-progress-v1.md`
only when the task needs screen-level detail.

Do not copy or maintain the current landed screen set inside this skill.

## GUI Static Sprint Mode

When the user explicitly approves a GUI static sprint, Antigravity may work
through multiple small static prototype edits inside the approved surface without
asking for approval at every small step.

Run one sprint preflight per session or sprint:

1. Name the screen, route, or screen family being touched.
2. Name the allowed surface, such as `HTML/CSS only`, `fixture only`,
   `render-layer JS only`, or `07_gui_prototype static shell only`.
3. Confirm that runtime, data, schema, save, combat formula, manual `save.json`,
   formal asset pipeline, and JS gameplay authority are out of scope.
4. Read only relevant screen files and targeted handoff/progress sections needed
   for the sprint.

Within that sprint, allowed consecutive work may include:

- HTML/CSS static layout changes
- fixture edits
- render-layer JavaScript for static fixtures
- static navigation flow
- UIAction logging
- localhost browser verification
- syntax or fixture parse checks for the prototype layer

Pause and start a new planning gate if the work crosses into another mode,
another file surface, runtime/live bridge, data/schema/save/combat, formal asset
pipeline, or a materially different screen family.

## Allowed Surface

For GUI static prototype tasks, allowed work is limited to:

- static fixtures
- render layer behavior
- layout and responsive behavior
- interaction feeling
- static navigation flow
- UIAction logging
- browser or syntax verification of the prototype layer

HTML fixtures are display data for GUI validation only. They are not gameplay
SSOT.

## Forbidden Drift

For GUI static prototype tasks, do not:

- connect to the Python runtime
- read, write, or manually edit `save.json`
- modify runtime, data, schema, save, or combat formulas
- copy gameplay rules into JavaScript prototypes
- treat reference images or mockup candidates as runtime assets
- start a formal asset pipeline
- infer gameplay changes from mockup text or screenshots
- refactor `03_engine/engine/game.py`

## Runtime-Connected Prototype Exception

Runtime-connected GUI work is not GUI Static Sprint Mode.

It is allowed only when the user explicitly approves that exact scope. When
approved, first read `01_content/gui-runtime-bridge-plan-v1.md` and stop at a
read-only planning gate before implementation.

Static sprint approval does not imply runtime bridge approval. Python remains
the gameplay authority, and JavaScript must not copy gameplay rules.

## Server Helper

Use a local HTTP server. Do not open prototype pages with `file://`, because
fixture `fetch()` calls may fail.

Antigravity may autonomously start the local prototype server for GUI static
prototype verification:

```powershell
.\start_gui_prototype_server.bat
```

Server root:

```text
07_gui_prototype/
```

URL pattern:

```text
http://localhost:8000/<screen_folder>/index.html
```

Use the relevant screen folder from `07_gui_prototype/` rather than maintaining
a duplicated full URL list in this skill.

## Read Strategy

- Read relevant screen files first.
- Read targeted progress or planning sections only when the task requires
  screen-level status, prior decisions, or drift context.
- Do not full-load GUI progress logs or planning indexes for ordinary sprint
  edits.
- Do not read Cold Zone files unless the user names them or the active task truly
  requires them.

## Verification Stance

Use the smallest fitting verification.

Antigravity may autonomously run local syntax and fixture parse checks, and may
use localhost browser checks to verify layout, interaction, navigation, UIAction
logging, and fixture loading.

Examples:

- JSON fixture parse checks for fixture edits
- JavaScript syntax checks for render-layer edits
- Browser checks for layout, interaction, navigation, UIAction logging, and
  fixture loading

Verification is guidance, not a mandatory gate for every small CSS, HTML,
fixture-text, or docs adjustment. Use stricter gates only when the task touches
runtime, bridge, data, schema, save, combat, or another high-risk surface.

## Reporting

After GUI static prototype implementation, report:

- actual modified files
- concise change summary
- checks performed, if any
- unresolved or intentionally deferred items
- relevant boundaries, especially if `07_gui_prototype/` was or was not touched

Do not report unrelated governance boilerplate.
