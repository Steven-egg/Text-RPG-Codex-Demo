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

The current landed screen set has 11 static prototypes:

1. Start Screen: `start_screen/`
2. Town Hub: `town_hub/`
3. Guild Screen: `guild_screen/`
4. Synthesis Screen: `synthesis_screen/`
5. Shop Screen: `shop_screen/`
6. Workshop Screen: `workshop_screen/`
7. Storage Screen: `storage_screen/`
8. Magic Shop Screen: `magic_shop_screen/`
9. World Map: `world_map/`
10. Dungeon Exploration: `dungeon_exploration/`
11. Combat Screen: `combat_screen/`

Treat Synthesis, Shop, Workshop, Storage, and Magic Shop static prototype v1 as
landed. Do not list them as unfinished candidates unless live files or the user say so.

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

Standard URLs:

- Start Screen: `http://localhost:8000/start_screen/index.html`
- Town Hub: `http://localhost:8000/town_hub/index.html`
- Guild Screen: `http://localhost:8000/guild_screen/index.html`
- Synthesis Screen: `http://localhost:8000/synthesis_screen/index.html`
- Shop Screen: `http://localhost:8000/shop_screen/index.html`
- Workshop Screen: `http://localhost:8000/workshop_screen/index.html`
- Storage Screen: `http://localhost:8000/storage_screen/index.html`
- Magic Shop Screen: `http://localhost:8000/magic_shop_screen/index.html`
- World Map: `http://localhost:8000/world_map/index.html`
- Dungeon Exploration: `http://localhost:8000/dungeon_exploration/index.html`
- Combat Screen: `http://localhost:8000/combat_screen/index.html`

## Preflight Gate

Before planning or editing a GUI prototype task:

1. Name the screen or route being touched.
2. Declare the allowed surface, such as `CSS only`, `fixture only`, `render-layer JS
   only`, or `HTML/CSS/fixture within 07_gui_prototype only`.
3. Restate that no Python runtime, `save.json`, runtime, data, schema, save, combat
   formula, or formal asset pipeline work is included.
4. Read only the relevant screen files and targeted handoff sections needed for that
   screen.

## Verification Stance

Use the smallest fitting verification:

- JSON fixture parse checks for fixture edits.
- JavaScript syntax checks for render-layer edits.
- Browser checks for layout, interaction, navigation, and UIAction logging.

Do not run runtime validation for GUI-only prototype edits unless the task separately
touches runtime, which should require a separate read-only planning gate first.
