# GUI Static Prototype Current State V1

Purpose: compact active SSOT for the static GUI fallback and its shared render
surface. Historical verification and superseded decisions live in
`archive/gui-html-static-prototype-progress-v1.md`.

## Authority Boundary

- `07_gui_prototype/` contains the static prototype and the render layer shared
  with the opt-in live mode.
- Static fixtures are display/test data only. They are not gameplay, story,
  save, reward, unlock, or balance authority.
- Python and `04_data/data/` remain gameplay authority. Browser JavaScript
  renders ScreenModels and dispatches UIActions; it does not reproduce Python
  gameplay rules.
- Static work may cover rendering, layout, fixture shape, navigation,
  interaction, focus handling, and UIAction logging. Runtime behavior,
  `save.json`, data/schema changes, and gameplay formulas remain outside a
  static GUI task.

## Product Direction And Modes

- The live GUI is the primary product entrypoint direction. The secondary CLI
  is named **文字核心版 Text Core**.
- Static mode remains the development fallback for isolated rendering and
  interaction checks. Live mode uses the same screen interfaces and render
  components with ScreenModels returned by the existing Python runtime bridge.
- A live bridge slice does not make fixtures authoritative and does not approve
  generic inventory, equipment, facility, combat, settings, or other gameplay
  expansion.

## Current Shared Surface

The prototype covers Start Screen, Town Hub, Guild, Shop, Workshop, Storage,
Magic Shop, Inn, Temple, Synthesis, World Map, Dungeon Exploration, Combat, and
Relic Preview. Preserve static fallback and UIAction logging when a screen also
supports live mode.

The verified integration candidate adds these shared presentation behaviors:

- A strict six-field `story_beat` renderer: `id`, `kind`, `title`, `lines`,
  `dismiss_label`, and `tone`. Invalid, incomplete, extra-field, or wrongly
  typed payloads safely no-op.
- Five supported beat kinds: `prologue`, `region_transition`, `boss_before`,
  `boss_after`, and `ending`; four tones: `neutral`, `warning`, `victory`, and
  `ending`.
- Static and live screens use the same story renderer for Start prologue,
  World Map region transition, Dungeon pre-Boss, Combat post-Boss, and ending
  presentation. Text is inserted as text, not trusted markup.
- Combat sequencing remains
  `result close -> boss_after -> ending -> navigation`; story focus, keyboard,
  Escape, and modal boundaries prevent underlying interaction.
- Five procedural micro-SFX cues: `ui_click`, `confirm`, `back`, `warning`, and
  `victory`. There is no BGM, loop, binary audio asset, or autoplay.
- The enabled preference is `element_maze.sfx_enabled` (`true` means audible,
  default on); legacy `element_maze.sfx_muted` values migrate once. Untrusted
  synthetic clicks cannot create or resume an `AudioContext`; audio failures
  remain silent and cannot block navigation, actions, or UIAction logging.
- The SFX toggle uses layer `9000`; the story overlay uses `9999`, so the story
  modal remains visually and interactively above the toggle.

## Release Separation

The referenced-image overlay builder and Windows portable builder are offline
release tooling, not browser-runtime responsibilities. The portable GUI
launcher serves the existing live interface and delegates gameplay to the
existing Python bridge; it does not create another browser gameplay engine.

Release assets live only in ignored output below
`dist/assets-overlay/app/<repository-relative-path>`. A local-validation
portable ZIP is not a formal release. Its image manifest is format 1 at
`dist/manifests/assets-manifest.json`, and the package currently remains
`release_ready:false`.

## Acceptance Checkpoint

- The behaviors above are verified on integration candidate `02aa179`; that
  commit is not `main`.
- `main` remains at `46efeb9` pending independent Gate 3 / final acceptance and
  Owner-approved ff-only promotion.
- Do not add a new GUI feature from this status document. New work still needs
  an exact approved surface and must preserve the static/live authority
  boundary.

## History

Read `archive/gui-html-static-prototype-progress-v1.md` only when a task needs
old screen-by-screen verification, DOM/console results, viewport checks, or a
superseded decision.
