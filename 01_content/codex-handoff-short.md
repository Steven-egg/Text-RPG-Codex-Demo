# Codex Handoff Short

Purpose: compact continuation boundary. Read live files before editing;
Python and `04_data/data/` remain gameplay authority.

## Current Acceptance State

- Verified Batch A--C integration candidate:
  `02aa179ef8f9259b56369e3998cb7d91ee81ea3d` on
  `codex/s6-wave3-integration`.
- `main` and `origin/main` remain at
  `46efeb93a0e98da12bde6c60769af2d303aeeb26`. The candidate has not been
  promoted to `main`.
- The integration branch is pushed and the verified candidate was clean. Its
  37 cumulative changed paths preserve Python/data authority, with no balance,
  save migration, reward, or unlock drift.
- The GUI is the primary product entrypoint. The secondary CLI is named
  **文字核心版 Text Core**.

## Wave State

- **S1 landed:** optional six-field `story_beat` presentation contract under
  Python/data authority: `id`, `kind`, `title`, `lines`, `dismiss_label`, and
  `tone`. Kinds: `prologue`, `region_transition`, `boss_before`, `boss_after`,
  `ending`. Tones: `neutral`, `warning`, `victory`, `ending`.
- **S2 landed:** strict GUI story renderer, invalid-payload safe no-op, pure
  text rendering, keyboard/focus/modal boundaries, and
  `result close -> boss_after -> ending -> navigation`.
- **S3 landed:** five muteable procedural micro-SFX cues with no BGM, binary
  audio, or autoplay. Mute key: `element_maze.sfx_muted`. Synthetic untrusted
  clicks cannot create/resume audio; SFX toggle layer `9000` stays below story
  overlay `9999`.
- **S4 landed:** release-only referenced-image overlay at
  `dist/assets-overlay/app/<repository-relative-path>` with manifest format 1
  at `dist/manifests/assets-manifest.json`. Verified counts: 196 included, 47
  `OLD` excluded, 6 unreferenced excluded. Repository images stay read-only.
- **S5 landed:** Windows portable builder with separate `app/` and
  `assets-overlay/app/`, existing live GUI/runtime bridge as the primary
  entrypoint, and **文字核心版 Text Core** as the secondary entrypoint.

## Gates And Integration

- **Gate 1 complete:** S1 `story_beat` schema and S4 asset manifest/path
  contract were locked before Wave 2.
- **Gate 2 PASS:** S2, S3, and S5 contracts and cross-branch integration order
  were accepted. S5 history includes S4.
- **Batch A--C complete:** S1, S2+S3, and S4+S5 were integrated at `02aa179`.
  S1/S2/S3/S4/S5 exact tips are ancestors. The only path overlap was
  `07_gui_prototype/start_screen/start-screen.js`; Git auto-merged it and
  verification confirmed story wiring, `?debug=1`, and the production cover
  without `frontier`/`data-cover` regression.
- Runtime, story, SFX, assets, portable relocation, and localhost/browser
  checks passed on the candidate. This handoff records that evidence; it does
  not replace an independent final acceptance.

## Release Blocker

Formal publication remains blocked with `release_ready:false`. The validated
ZIP is local-validation output only: runtime redistributability is unconfirmed,
complete runtime/dependency licenses are not assembled, and the required
`rich` dependency is absent from the validated local runtime. Do not publish
or label this artifact as a formal release.

## Frozen Boundaries

- Static fixtures are display/test data only. JavaScript, the portable
  launcher, and release builders are not gameplay or schema authority.
- Balance remains closed. Warrior `growth_points.attack = 1.5` and the
  per-job frozen growth totals remain unchanged.
- Existing save behavior and `save.json` boundaries remain unchanged; never
  edit runtime save output manually.
- Do not use this closeout to add gameplay, rewards, unlocks, facilities,
  storage capacity, balance changes, or a second runtime authority.

## Minimum Read List

1. `AGENTS.md`
2. `.codex/skills/element-maze-session-ops/SKILL.md`
3. `README.md`
4. this file
5. the task-specific live contract or source files

For GUI work, also use
`.codex/skills/element-maze-gui-static-prototype/SKILL.md` and the two current
GUI boundary documents. For release work, read
`release-asset-policy-v1.md` and `windows-portable-release-v1.md`.

## Next Boundary

The only approved next step is an independent **Gate 3 / final acceptance** of
`02aa179`. Do not merge, rebase, cherry-pick, or promote from this handoff.
Only after Gate 3 passes and the Owner explicitly approves promotion may
`main` advance by ff-only; formal release readiness remains a separate blocked
condition.
