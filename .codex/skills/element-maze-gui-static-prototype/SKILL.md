---
name: element-maze-gui-static-prototype
description: Task-focused GUI guidance for Element Maze. Use when Codex plans, reviews, previews, or edits prototype screens, runtime-connected UI, server URLs, fixtures, or UIAction logging.
---

# Element Maze GUI Static Prototype

## Core Rule

This skill provides task-focused GUI guidance. Read current screen details only
when they help complete the task.

Default to Traditional Chinese output unless the user asks otherwise.

## Current Scope

GUI static prototypes live in:

```text
07_gui_prototype/
```

This skill is not the project status SSOT. Current static GUI state lives in
`01_content/gui-static-current-state-v1.md`; historical verification lives in
`01_content/archive/gui-html-static-prototype-progress-v1.md`. Read the current
state only when the task needs status, and read the archive only for named
historical or verification-trace work.

## GUI Static Sprint Mode

Use this mode when the user asks for a GUI static prototype sprint, screen pass,
review fix pass, layout pass, fixture pass, UIAction logging pass, navigation
pass, or browser verification pass inside `07_gui_prototype/`.

Read the relevant screen and supporting files, then implement the requested
change directly. A sprint may cover HTML, CSS, JavaScript, fixtures, static
navigation, UIAction logging, and runtime-connected UI when those are part of
the task. Do not require a preflight, a fixed declaration of scope, or a
separate approval round before editing.

Use the appropriate existing source of truth for the task: fixtures for display
states, and runtime code or data for live behavior. Keep frontend and backend
responsibilities clear where that makes the implementation easier to maintain.

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

### Codex Local Server Check

For a Codex-managed localhost check, do not use `Get-NetTCPConnection` as the
preflight: its Windows CIM query can be denied by the Codex sandbox even when
the server is healthy. Start the intended local server, then verify the exact
page or API URL with an HTTP request and require a `200` response. This is a
Codex environment diagnostic rule, not a project runtime requirement.

- Static prototype: `http://127.0.0.1:8000/<screen_folder>/index.html`
- Runtime bridge:
  `http://127.0.0.1:8010/<screen_folder>/index.html?mode=live`

## Verification Stance

Use the smallest fitting verification:

- JSON fixture parse checks for fixture edits.
- JavaScript syntax checks for render-layer edits.
- Browser checks for layout, interaction, navigation, and UIAction logging.

Treat these checks as guidance for choosing a fitting confidence level, not as a
mandatory gate for every small static edit. Avoid turning ordinary CSS, fixture,
copy, or UIAction logging tweaks into a full verification matrix unless the risk
or user request calls for it.

Run runtime validation when the task touches runtime; otherwise use the smallest
check that meaningfully verifies the requested GUI change.
