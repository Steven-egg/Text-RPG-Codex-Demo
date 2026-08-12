# GUI static prototype guidance

Applies to `07_gui_prototype/`. Read relevant screen files first and use
Traditional Chinese unless the user asks otherwise.

## Scope

- With explicit approval for a GUI static sprint, make consecutive small edits
  within the named screen, route, or screen family: HTML/CSS, static fixtures,
  render-layer JavaScript, static navigation, UIAction logging, and responsive
  behavior.
- Fixtures and JavaScript exist only for prototype display and interaction;
  they are not gameplay authority.
- Do not connect to the Python runtime, read/write `save.json`, change runtime,
  data, schema, save, or combat formulas, copy gameplay rules into JavaScript,
  start a formal asset pipeline, or refactor `03_engine/engine/game.py`.
- A static-sprint approval never authorizes runtime bridge work. For explicitly
  approved runtime-connected work, follow the root `AGENTS.md` planning gate.

## Working and verification

- Read targeted progress or planning sections only when screen-level history is
  needed; do not load broad logs or unrelated files by default.
- Use the smallest fitting check: JSON fixture parsing, JavaScript syntax, or
  browser verification for layout, interaction, navigation, UIAction logging,
  and fixture loading.
- Use a local HTTP server for fixture-fetching pages, not `file://`. The helper
  is `start_gui_prototype_server.bat`; serve from `07_gui_prototype/` and use
  `http://localhost:8000/<screen_folder>/index.html`.
- After implementation, report modified files, checks performed, and any
  deferred items or relevant boundary.
