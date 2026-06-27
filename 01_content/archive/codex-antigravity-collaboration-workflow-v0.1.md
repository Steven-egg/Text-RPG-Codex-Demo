# Codex / Antigravity Collaboration Workflow v0.1

Purpose: define the working agreement between the owner, Codex, and
Antigravity for future Element Maze planning. This is a Task Zone workflow
reference, not project status and not implementation approval.

Use this file together with:

- `01_content/antigravity-candidate-content-brief-v0.1.md`
- `01_content/regional-data-instantiation-plan-v0.1.md`
- `01_content/world-content-skeleton-v0.1.md`

## Core Roles

The owner is the director and final decision maker.

Owner responsibilities:

- choose the target slice, such as Ice region skeleton, Fire alignment wording,
  or one visual mood packet;
- select, reject, or mix candidate directions;
- explicitly approve any move from planning into implementation;
- decide whether a candidate becomes official planning material.

Codex is the production coordinator and implementation agent.

Codex responsibilities:

- prepare bounded request packets for Antigravity;
- translate owner intent into repo-safe scope and forbidden surfaces;
- review returned candidates for fit, drift risk, and implementation risk;
- turn selected candidates into planning docs or implementation gates;
- implement runtime, data, schema, GUI, bridge, or asset work only after exact
  owner approval;
- run suitable verification for the approved surface.

Antigravity is the candidate-content and writing assistant.

Antigravity responsibilities:

- generate options for named slots only;
- provide names, short descriptions, local mood text, quest summaries, NPC
  flavor, item names, monster concepts, visual prompt drafts, or similar
  candidate material;
- flag any candidate that may imply new mechanics, schema, GUI, combat behavior,
  equipment slots, asset pipeline, or runtime state;
- leave final selection, data shaping, and implementation to the owner and
  Codex.

## Standard Flow

Use this flow for content, story, region, and visual-candidate work.

1. Owner chooses one small target slice.
2. Codex prepares a request packet with the target, slots, tone constraints,
   output format, and forbidden surfaces.
3. Antigravity returns candidate material.
4. Codex reviews the candidate material as non-authoritative input.
5. Owner selects, rejects, or mixes candidate directions.
6. Codex converts the owner-selected direction into one of:
   - a planning-only doc;
   - a read-only implementation gate;
   - a later exact-scope implementation task.

Candidate material is never official runtime data by itself.

## Candidate Rules

Antigravity output should be treated as a proposal packet.

Allowed candidate content:

- three options per requested slot;
- names and short descriptions;
- local mood or flavor text;
- quest summary options;
- NPC, monster, boss, material, item, recipe, book, equipment, hub, dungeon, or
  visual-direction ideas;
- notes about tone fit and reuse risk.

Forbidden candidate content unless a later exact-scope gate explicitly opens it:

- final runtime data;
- registry wiring;
- schema changes;
- validation tool edits;
- save changes or manual `save.json` work;
- combat formulas, combat behavior, stat effects, or relic effects;
- GUI implementation or runtime bridge behavior;
- generated final assets or formal asset-pipeline setup;
- prices, quantities, drop rates, formulas, final IDs, or unlock keys.

## Codex Review Rules

When reviewing an Antigravity packet, Codex should classify each useful result
as one of:

- `candidate`: usable as an option, not selected yet;
- `owner_selected`: selected by the owner but not implemented;
- `planning_input`: safe to carry into a planning doc;
- `needs_rewrite`: tone or structure needs another pass;
- `blocked`: implies a forbidden surface or unclear system change.

Codex should check candidates against:

- current world skeleton and regional count decisions;
- Fire / Border legacy boundaries;
- region manifest and data instantiation order;
- quest objective safety and early-completion risk;
- relic / marker / marker-source separation;
- GUI, bridge, asset, runtime, data, schema, save, and combat boundaries.

## Implementation Gate

Moving from candidate content into implementation requires a separate owner
approval that names the exact surface.

Before implementation, Codex should provide a read-only gate that identifies:

- proposed slice;
- files likely to be touched;
- adjacent systems that remain closed;
- validation commands or review checks;
- residual risks and open decisions.

No candidate packet alone authorizes implementation.

## Ice Region Skeleton Example

For the current Ice region skeleton packet:

- Owner selects Ice as the target region.
- Codex prepares the Antigravity request packet.
- Antigravity generates candidate mood, hub, dungeon, and Guild quest summaries.
- Owner chooses preferred directions.
- Codex reviews and converts selected directions into planning material.

This example does not open runtime, data, schema, save, combat, GUI, bridge, or
asset-pipeline work.
