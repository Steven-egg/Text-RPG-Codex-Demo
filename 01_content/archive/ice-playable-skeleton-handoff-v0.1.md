# Ice Playable Skeleton Handoff v0.1

Purpose: record the Ice CLI playable skeleton checkpoint after the first owner
playtest. This is a Task Zone handoff and test note. It does not approve new
runtime, data, schema, save, combat, GUI static prototype, bridge, relic-effect,
or asset-pipeline implementation.

## Current Checkpoint

- Latest gameplay commit: `f3a3314 2026-06-20 [codex] feat(content): add Ice playable skeleton`.
- Latest environment commit observed after the gameplay checkpoint:
  `5565eb8 2026-06-20 [codex] docs(env): document local Python venv setup`.
- Owner-side untracked visual references remain outside the committed runtime
  slice:
  - `05_assets/gui_references/ice-town-hub-placeholder-candidate-v01.png`
  - `05_assets/gui_references/ice-world-map-placeholder-candidate-v01.png`
- These reference images are read-only visual guides and are not gameplay SSOT.
- The first Ice CLI skeleton playtest reached Q5 completion successfully.

## Implemented Shape

Ice v0.1 follows the clone-first route:

- Runtime/data content uses four playable blocks:
  - `dungeon_ice_minor_a`
  - `dungeon_ice_minor_b`
  - `dungeon_ice_main_phase_1`
  - `dungeon_ice_main_phase_2`
- Player-facing dungeon presentation remains three locations:
  - `幽帆沉船`
  - `霜根岩窟`
  - `霜鐵古城`
- The main dungeon is represented as two runtime phases:
  - `霜鐵古城 - 斷階外城`
  - `霜鐵古城 - 終印宮殿`
- No relic active/passive/stat/combat effect is implemented.

## Quest And Dungeon Mapping

| Quest | Role | Runtime Target | Main Condition | Unlock / Outcome |
|---|---|---|---|---|
| Q1 `quest_ice_minor_a` | Minor A survey | `幽帆沉船` | turn in `mat_ice_saltcloth` and `mat_ice_wreck_plank` | unlocks `霜根岩窟` |
| Q2 `quest_ice_minor_b` | Minor B anomaly check | `霜根岩窟` | turn in `mat_ice_frostroot` and `mat_ice_blue_stone` | unlocks main phase 1 |
| Q3 `quest_ice_main_phase_1` | Main phase 1 Boss task | `霜鐵古城 - 斷階外城` | flag `ice_outer_gatewarden_defeated` | unlocks main phase 2 |
| Q4 `quest_ice_main_phase_2` | Main phase 2 / deep seal task | `霜鐵古城 - 終印宮殿` | flag `ice_final_boss_defeated` | sets `ice_relic_marker_resolved`; grants marker source |
| Q5 `quest_ice_return_handoff` | Return / closure / handoff | no new dungeon | flag `ice_relic_marker_resolved` | unlocks `unlock_earth_region_preview` placeholder |

Minor A and Minor B Bosses are intentionally not required by Q1 / Q2:

- `boss_ice_wreck_captain`
- `boss_ice_frostroot_keeper`

The player can challenge them at the dungeon end as optional direct Boss fights
within the required route.

## Owner Playtest Notes

The first CLI playtest suggests the expansion succeeded at the skeleton level:

- Ice content became reachable after the Fire route.
- Ice dungeons can be entered and cleared.
- Normal encounters, Boss encounters, rewards, and Guild turn-ins function.
- Q1 through Q5 can be completed.
- The final Boss grants `Ice Relic Marker Source`.
- Q5 can be completed after Q4 as a closure task.

Observed placeholder / follow-up issues:

- Town presentation is still the existing town shell.
- Some guidance still routes through existing Fire-route or old NPC context,
  including references like finding Sion.
- Ice text remains mixed Chinese / English placeholder copy.
- Q5 currently has no substantive event; it is a direct closure turn-in.
- Main phase 2 can appear as the same player-facing main dungeon, but CLI copy
  still needs later polish to make the phase transition feel intentional.

These are accepted v0.1 skeleton limitations, not blockers for the gameplay
checkpoint.

## Q5 Interpretation

Q5 is a closure and handoff slot, not a combat task.

Current v0.1 function:

- Confirms the Ice region was reported back to the Guild.
- Provides a clean completion marker after Q4.
- Opens `unlock_earth_region_preview` as a next-region placeholder.
- Reserves the future story event position for Sion / Guild / Ice seal
  interpretation / next-map direction.

Future polish may turn Q5 into a real report scene or handoff event, but this
requires a later exact-scope runtime / text planning gate.

## Verification Recorded

Before the gameplay commit, Codex ran:

```powershell
python 06_tools/validate_data.py
python element_maze.py --smoke-test
python 06_tools/smoke_test_progression_bridge.py
python 06_tools/smoke_test_combat_bridge.py
```

The local environment used the bundled Codex Python because `python` was not on
PATH in that session. The command intent remains the standard validation set.

Owner then manually committed the gameplay slice as:

```text
f3a3314 [codex] feat(content): add Ice playable skeleton
```

## Recommended Next Session Route

Recommended next convergence item:

1. Start a new Codex session.
2. Do a read-only catch-up from the Hot Zone.
3. Read this handoff.
4. Decide whether the next CLI expansion target is:
   - Earth playable skeleton preflight, or
   - Ice v0.2 Chinese naming / text cleanup preflight.

If the goal is to finish the CLI dungeon universe quickly, prefer:

```text
Earth playable skeleton preflight
```

Use the Ice v0.1 pattern as the template:

- two minor dungeons
- one two-phase main dungeon
- five Guild quests
- minor Bosses optional
- Q3/Q4 Boss-gated
- Q5 closure / next-region placeholder

Implementation is still not pre-approved. Any Earth / Thunder / Final runtime,
data, schema, combat, save, or bridge work must begin with a read-only preflight
that names exact files and validation commands.

## Boundaries

- Do not read or write `save.json` manually.
- Do not modify runtime/data/schema/save/combat from this handoff alone.
- Do not treat GUI reference images or static fixtures as gameplay SSOT.
- Do not start formal image, monster-art, Boss-art, or asset-pipeline work from
  this document.
- Do not implement relic effects from the Ice marker source.
- Do not mix environment-governance commits with gameplay/data commits.
