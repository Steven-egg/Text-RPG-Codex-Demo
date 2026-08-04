# GUI Runtime Bridge Plan V1

Purpose: active boundary for the existing local GUI runtime bridge. Historical
architecture, endpoint drafts, slice notes, and superseded verification remain
in `archive/gui-runtime-bridge-plan-v1.md`.

## Authority And Mode Boundary

- The live GUI is the primary product entrypoint direction. The secondary CLI
  is named **文字核心版 Text Core**.
- Python and `04_data/data/` remain gameplay authority. Browser JavaScript
  dispatches UIAction payloads and renders returned ScreenModels.
- Static fixtures remain display/test fallback. They do not define live
  gameplay or become portable gameplay data.
- Save/load uses existing Python runtime behavior only. The bridge, browser,
  and portable launcher must not manually edit `save.json` or introduce a save
  migration.
- New live slices still require exact approval. They may extend presentation
  or adapters only within a named boundary; they do not authorize gameplay,
  balance, rewards, unlocks, data/schema, or broad runtime changes.

## Current Live Boundary

Existing live slices include start/load/restart, town and facility shells,
approved dungeon/combat actions, guild reporting, shop consumables,
magic-book learning, all authoritative current-region workshop and synthesis
recipes, and equipment actions from both the workshop and the world-map
inventory preview. Recipe execution consumes exact equipment instances
(including legacy-normalized instances), while special-slot equipment remains
a static equipment reference. Live and static modes share screen interfaces
while keeping their data sources distinct.

The verified integration candidate adds optional `story_beat` presentation to
that boundary:

- The ScreenModel field is optional and valid only with exactly `id`, `kind`,
  `title`, `lines`, `dismiss_label`, and `tone`.
- Kinds are `prologue`, `region_transition`, `boss_before`, `boss_after`, and
  `ending`; tones are `neutral`, `warning`, `victory`, and `ending`.
- Python/data select and populate story beats. The GUI validates and renders
  them, safely no-oping invalid payloads; it does not invent story state or
  fallback gameplay behavior.
- The live presentation points are Start prologue, World Map region
  transition, Dungeon pre-Boss, Combat post-Boss, and ending. Completion order
  is `result close -> boss_after -> ending -> navigation`.
- Story output remains pure text with focus, keyboard, Escape, and modal
  boundaries. The story overlay layer `9999` remains above the SFX toggle layer
  `9000`.

Five muteable procedural micro-SFX cues coexist with the same static/live
interfaces. They have no BGM, binary audio, or autoplay; mute state uses
`element_maze.sfx_muted`, and untrusted synthetic clicks cannot create or
resume audio. Audio failures must remain non-blocking for UIActions,
navigation, and logging.

## Portable And Release Boundary

The Windows portable GUI launcher binds `127.0.0.1`, opens the existing Start
Screen in `mode=live`, and delegates API behavior to the existing runtime
bridge. Packaging does not establish a second gameplay authority.

Portable layout keeps program files under `app/` and referenced GUI images
under `assets-overlay/app/`. The asset builder preserves repository-relative
paths and writes manifest format 1 to
`dist/manifests/assets-manifest.json`; repository originals remain read-only.
These are packaging contracts, not ScreenModel or UIAction responsibilities.

A verified local-validation ZIP exists only as acceptance evidence. It is not
a formal release: `release_ready:false` remains required until a
redistributable runtime is confirmed, complete runtime/dependency licenses are
assembled, and the required `rich` dependency is present.

## Planning Gate For New Bridge Work

Every separately approved bridge slice must state:

1. exact screen and UIAction scope;
2. existing Python runtime functions reused;
3. ScreenModel fields and files allowed to change;
4. static fixture fallback behavior;
5. save/runtime boundaries, verification commands, and stop conditions.

If a proposal changes authority, mode, save behavior, or gameplay scope, stop
for explicit approval instead of extending the existing bridge by inference.

## Acceptance Checkpoint And Remaining Work

- Batch A--C candidate `02aa179` has passed runtime, story/SFX, release asset,
  portable relocation, and localhost/browser verification. It is not `main`.
- `main` remains at `46efeb9` pending independent Gate 3 / final acceptance.
- The only approved closeout action is that independent acceptance; only after
  it passes and the Owner approves may `main` advance ff-only.
- The only release-level blocker recorded here is the runtime/licenses/`rich`
  condition above. This plan does not open new gameplay or GUI feature work.

## History

Read `archive/gui-runtime-bridge-plan-v1.md` only when a task needs historical
architecture, endpoint drafts, or superseded slice notes.
