# Antigravity Candidate Content Brief v0.1

Purpose: define the candidate-content package that Antigravity may prepare for
future Element Maze regional expansion. This brief is for naming, flavor, short
descriptions, and option generation only. It does not approve runtime data,
schema, registry, validation, save, combat, GUI, bridge, or asset-pipeline work.

Use this file after:

- `01_content/world-content-skeleton-v0.1.md`
- `01_content/regional-data-template-v0.1.md`
- `01_content/regional-data-instantiation-plan-v0.1.md`

## Role Boundary

Antigravity may generate candidate content only.

Allowed:

- Three candidates per requested slot.
- Names and short descriptions.
- Local mood text.
- NPC and facility flavor lines.
- Quest summary options.
- Item, material, recipe, book, monster, Boss, hub, and dungeon naming options.
- Notes about tone, element fit, and reuse risks.

Not allowed:

- Final runtime data.
- Data table insertion.
- Registry wiring.
- Schema changes.
- Validation tool edits.
- Save changes.
- Combat behavior or formulas.
- GUI implementation.
- Bridge behavior.
- Asset generation or asset-pipeline setup.

Codex or a later exact-scope planning gate remains responsible for final
selection, data shaping, validation, and implementation.

## Candidate Package Format

Each candidate slot should use this shape:

```text
slot_id:
  purpose:
  constraints:
  candidate_a:
    name:
    short_description:
    tone_tags:
    why_it_fits:
    risks:
  candidate_b:
    name:
    short_description:
    tone_tags:
    why_it_fits:
    risks:
  candidate_c:
    name:
    short_description:
    tone_tags:
    why_it_fits:
    risks:
  owner_selection:
  notes_for_codex:
```

Candidates should avoid final IDs, prices, quantities, drop rates, combat
numbers, unlock keys, and schema-specific structures unless a later planning
gate explicitly asks for them.

## Region Input Order

Candidate generation should follow the future data instantiation order:

1. Region manifest slots.
2. Hub and dungeon topology.
3. Quest summary and progression flavor.
4. Material and marker-source naming.
5. Monster and Boss naming.
6. Facility flavor.
7. Shop, Magic Shop, Synthesis, Workshop, equipment, and upgrade naming.
8. Optional elite hunt naming.

Do not start with random item lists or monster lists before the region's route
and completion structure are clear.

## Required Candidate Slots Per Region

For Ice, Earth, Thunder, and Final, prepare three candidates for:

- Region hub name and one-sentence hub flavor.
- Minor dungeon A name and short description.
- Minor dungeon B name and short description.
- Main dungeon phase 1 name and short description.
- Main dungeon phase 2 name and short description.
- Five required Guild quest summaries.
- Main supporting NPC names and one-line roles.
- Facility flavor lines for the nine reused facility families.
- 14 normal monster names and short concepts.
- 4 Boss names and short concepts.
- Regional material names for the material slot template.
- Shop goods names.
- Magic book names by job allocation.
- Synthesis recipe names.
- Equipment names.
- Workshop upgrade naming or flavor hooks.

For Fire / Border route, candidates should be limited to legacy interpretation
or future alignment language only. Do not invent Ash Outpost or replace existing
Fire demo data.

## Relic And Marker Candidate Rules

Use the relic model from `regional-data-instantiation-plan-v0.1.md`.

Candidates may name or describe:

- Elemental seal attunement scenes.
- Seal seats, ancient cores, sources, or local proof objects.
- `relic_marker_source` flavor.
- Fire shard interpretation event wording.

Candidates must not define:

- Active relic effects.
- Passive relic effects.
- Stat bonuses.
- Resistance bonuses.
- Skill links.
- Combat formulas.
- Final implementation of Fire shard consumption or conversion.

Relic effects wait until after class identity and promotion planning.

## Regional Mood Inputs

Use these macro moods as constraints.

| Region | Mood Constraint |
|---|---|
| Fire / Border legacy | Ash, scorched stone, sealed furnace ruins, existing Border Town route. |
| Ice | Frost-tide coast, cold sea, broken ice, fog harbor, salt-frost lighthouse. |
| Earth | Forest ring, root network, old quarry, fungal caverns, leyline stone. |
| Thunder | Storm plateau, sky roads, floating stone, conductive channels, lightning towers. |
| Final | Composite front-line endgame zone echoing Fire, Ice, Earth, and Thunder. |

Final candidates should feel like a convergence and war-front, not a fifth
elemental region.

## Output Quality Rules

Good candidates should:

- Be short enough to fit future UI labels.
- Use clear elemental identity without becoming generic.
- Avoid making every local noun a compound of the element name.
- Leave room for later data IDs.
- Avoid locking combat mechanics before a combat planning gate.
- Avoid adding new systems or facilities.
- Respect the existing facility families.

Antigravity should flag any candidate that may imply new mechanics, new schema,
new equipment slots, new town runtime state, or new GUI requirements.

## Recommended Next Step

Before asking Antigravity for content, Codex should prepare a small request
packet that names:

- Target region.
- Slots requested.
- Tone constraints.
- Current forbidden surfaces.
- Whether Fire legacy wording is in scope.

Start with one region or one slot family first, not the full game at once.
