# UI Art Prep Brief v0.1

Purpose: define future preparation work for UI images, regional visual mood, and
visual asset candidates. This brief is planning only. It does not approve GUI
static prototype edits, image generation, runtime bridge work, formal asset
pipeline setup, data changes, schema changes, save changes, or combat changes.

Use this file after:

- `01_content/world-content-skeleton-v0.1.md`
- `01_content/regional-data-template-v0.1.md`
- `01_content/regional-data-instantiation-plan-v0.1.md`

## Core Boundary

This brief prepares future art direction and candidate asset needs.

Allowed at this stage:

- Identify which screens may eventually need images.
- Define region mood constraints.
- List candidate asset categories.
- Separate early visual candidates from later asset-pipeline work.
- Record what must be decided before actual image generation or production.

Not allowed at this stage:

- Generate final images.
- Edit `07_gui_prototype/`.
- Open GUI static sprint work.
- Connect runtime bridge behavior.
- Create asset registry entries.
- Add formal asset folders or pipeline scripts.
- Modify runtime data, schema, save, or combat.

## Screen Areas That May Need Visual Assets

Future UI work may eventually need images or visual treatments for:

- Region hub / town presentation.
- Dungeon entry and dungeon exploration state.
- Boss encounter presentation.
- Normal monster presentation.
- Optional elite hunt presentation.
- Guild quest listing and quest detail.
- Shop, Magic Shop, Synthesis, Workshop, Temple, Storage, Inn, and Relic
  Preview facility shells.
- Item, material, equipment, recipe, and book icons.
- Relic / seal state presentation.
- Final region gate and ending resolution.

This list is not approval to edit GUI screens. It is a planning checklist for
future static prototype or asset-pipeline gates.

## Regional Mood Baseline

| Region | Visual Mood |
|---|---|
| Fire / Border legacy | Ash, scorched stone, low furnace glow, sealed ruin heat, frontier town wear. |
| Ice | Frost-tide coast, cold sea, salt fog, broken ice, lighthouse silhouettes, wet stone. |
| Earth | Root networks, old quarry faces, moss, fungal caverns, leyline stone, ancient growth. |
| Thunder | Storm plateau, sky roads, floating stone, conductive rails, lightning towers, charged mist. |
| Final | Front-line camp, fractured convergence, four-element echoes, siege tension, endgame scale. |

Final should not introduce a fifth elemental palette. It should visually combine
or stress-test the four established element moods.

## Candidate Asset Categories

Prepare candidates before final production for:

- Region hub background direction.
- Dungeon background direction.
- Main Boss silhouette or portrait direction.
- Optional elite silhouette direction.
- Normal monster icon or portrait direction.
- Facility header or backdrop direction.
- NPC bust or portrait direction.
- Item and material icon families.
- Magic book icon family.
- Recipe and synthesis icon family.
- Equipment icon family.
- Relic / seal emblem direction.
- Final gate and ending image direction.

At candidate stage, prefer mood boards, descriptions, references, or prompt
drafts over final generated assets.

## Early Candidate Priority

The first useful visual candidates are:

1. One mood direction per region.
2. One hub background direction per region.
3. One dungeon visual identity per dungeon slot family.
4. One relic / seal emblem direction per element.
5. One shared icon style direction for items, materials, books, recipes, and
   equipment.

Boss portraits, NPC portraits, and full monster sets should wait until the
regional route and candidate content names are more stable.

## What To Leave For GUI Static Prototype

Leave these decisions for a later approved GUI static prototype sprint:

- Exact screen placement.
- HTML / CSS implementation.
- Fixture shape changes.
- UIAction logging.
- Static navigation changes.
- Responsive layout verification.
- Browser screenshot verification.

Static prototype assets should remain references or placeholders unless the
owner approves the exact `07_gui_prototype/` surface.

## What To Leave For Asset Pipeline

Leave these decisions for a later formal asset-pipeline gate:

- Final asset folder structure.
- Export formats and sizes.
- Naming convention for actual image files.
- Licensing and source tracking.
- Compression and optimization.
- Runtime or GUI asset registry.
- Replacement rules for placeholder art.
- Validation tools for missing assets.

No formal asset pipeline starts from this brief.

## Relationship To Antigravity

Antigravity may later provide visual candidate wording, mood options, and prompt
drafts, but not final assets or implementation.

If paired with the candidate-content brief, Antigravity should first generate
content names and short descriptions, then prepare visual candidate directions
that match the selected tone.

## Recommended Next Step

Before visual production, choose one of these planning slices:

- Regional mood board brief for Ice only.
- Shared icon style direction for item / material / book / recipe icons.
- Relic / seal emblem direction for Fire, Ice, Earth, and Thunder.
- Final front-line camp mood exploration.

Do not generate or place images until an exact art or GUI surface is approved.
