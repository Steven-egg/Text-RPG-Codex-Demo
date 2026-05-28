---
name: element-maze-gui-static-prototype
description: Project-specific GUI static prototype boundaries for Element Maze. Use when Codex plans, reviews, previews, or edits 07_gui_prototype HTML static prototype work, server URLs, fixture boundaries, UIAction logging, or GUI drift control.
---

# Element Maze GUI Static Prototype

## Core Rule

This skill is the source for GUI static prototype boundaries. It is not a progress
log. For current screen details, read targeted sections of
`01_content/gui-html-static-prototype-progress-v1.md` only when the task needs them.

Default to Traditional Chinese output unless the user asks otherwise.

## Current Scope

GUI static prototypes live in:

```text
07_gui_prototype/
```

This skill is not the project status SSOT. Current landed screens, planned
screens, and detailed progress live in README / handoff / GUI planning or
progress docs. Read those only when the task needs current screen status or drift
context.

## Allowed Surface

For GUI static prototype tasks, allowed work is limited to:

- static fixtures
- render layer behavior
- layout and responsive behavior
- interaction feeling
- static navigation flow
- UIAction logging
- browser or syntax verification of the prototype layer

HTML fixtures are display data for GUI validation only. They are not gameplay SSOT.

## GUI Static Sprint Mode

Use this mode when the user asks for a GUI static prototype sprint, screen pass,
review fix pass, layout pass, fixture pass, UIAction logging pass, navigation
pass, or browser verification pass inside `07_gui_prototype/`.

At the start of each session or sprint, do one sprint preflight:

1. Name the touched screen(s) or route family.
2. Declare the allowed static surface, such as HTML/CSS/render-layer JS/fixtures,
   static navigation, UIAction logging, and browser or syntax verification within
   `07_gui_prototype/`.
3. Restate that the sprint excludes Python runtime, `save.json`, runtime, data,
   schema, save migration, combat formula, JS gameplay authority, and formal asset
   pipeline work.
4. Read the relevant screen files. Read targeted handoff/progress sections only
   when screen-level detail, verification history, drift audit, or task routing
   needs them.

After sprint preflight, the agent may make a sequence of small related static
prototype edits without repeating the preflight for every CSS rule, fixture row,
button, navigation link, or UIAction log adjustment.

Allowed sprint edits include:

- adding or editing HTML/CSS inside `07_gui_prototype/`
- render-layer JavaScript that only renders fixture/live-shaped screen models or
  dispatches prototype UIAction events
- static JSON fixtures
- static navigation flow
- UIAction logging
- browser verification and syntax checks for the prototype layer

Start a new preflight when the task changes screen family, changes mode, asks for
runtime/live bridge work, or touches anything outside the declared static surface.

## Forbidden Drift

For GUI static prototype tasks, do not:

- connect to the Python runtime
- read or write `save.json`
- modify runtime, data, schema, save, or combat formulas
- copy gameplay rules into JavaScript prototypes
- treat reference images or mockup candidates as runtime assets
- start a formal asset pipeline
- infer gameplay changes from mockup text or screenshots
- refactor `03_engine/engine/game.py`

## Runtime-Connected Prototype Exception

Runtime-connected prototype work is a separate opt-in mode, not ordinary static
prototype work. Use it only when the user explicitly approves that exact scope.

Before implementation, read:

```text
01_content/gui-runtime-bridge-plan-v1.md
```

Then stop at a read-only planning gate and identify the exact slice, touched
files, validation commands, and forbidden adjacent systems.

When approved, the narrow implementation surface may include:

- `06_tools/`: local runtime bridge server or bridge smoke helpers.
- `03_engine/engine/`: small action adapter/helper functions that reuse existing
  runtime logic.
- `07_gui_prototype/`: live-mode client or render integration.
- `save.json`: only through existing runtime save/load behavior, never by manual
  editing or fixture-style writes.

Keep JavaScript out of gameplay authority. In live mode, JavaScript dispatches
UIAction payloads and renders returned screen models; Python remains responsible
for state changes, save/load, validation, and gameplay rules.

Runtime, data, schema, save migration, and combat formula changes remain
forbidden unless separately approved after a read-only planning gate.

## Server Helper

Use a local HTTP server. Do not open prototype pages with `file://`, because fixture
`fetch()` calls may fail.

Preferred launcher from the repository root:

```powershell
.\start_gui_prototype_server.bat
```

Server root:

```text
07_gui_prototype/
```

Screen URL pattern:

```text
http://localhost:8000/<screen_folder>/index.html
```

## Preflight Gate

For a one-off GUI prototype task outside a declared sprint:

1. Name the screen or route being touched.
2. Declare the allowed surface, such as `CSS only`, `fixture only`, `render-layer JS
   only`, or `HTML/CSS/fixture within 07_gui_prototype only`.
3. Restate that no Python runtime, `save.json`, runtime, data, schema, save, combat
   formula, or formal asset pipeline work is included.
4. Read only the relevant screen files and targeted handoff sections needed for that
   screen.

For GUI Static Sprint Mode, run the sprint preflight once per session or sprint
instead of repeating this gate for each small edit.

## Verification Stance

Use the smallest fitting verification:

- JSON fixture parse checks for fixture edits.
- JavaScript syntax checks for render-layer edits.
- Browser checks for layout, interaction, navigation, and UIAction logging.

Treat these checks as guidance for choosing a fitting confidence level, not as a
mandatory gate for every small static edit. Avoid turning ordinary CSS, fixture,
copy, or UIAction logging tweaks into a full verification matrix unless the risk
or user request calls for it.

Do not run runtime validation for GUI-only prototype edits unless the task separately
touches runtime, which should require a separate read-only planning gate first.
