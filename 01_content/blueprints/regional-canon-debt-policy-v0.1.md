# Regional Canon And Debt Processing Policy v0.1

Purpose: planning policy for turning the landed CLI playable skeleton into
regional canon, data cleanup, and later system work. This file defines the debt
processing order and slice discipline only. It does not approve runtime, data,
schema, save, GUI, bridge, combat, class, relic, asset-pipeline, or image
generation implementation.

Use this file with:

- `01_content/world-content-skeleton-v0.1.md`
- `01_content/regional-data-template-v0.1.md`
- `01_content/regional-data-instantiation-plan-v0.1.md`

## Core Principle

Element Maze should process expansion debt from outer identity inward:

1. Define regional canon.
2. Derive visual and exploration identity.
3. Derive monsters, bosses, items, quests, and material names.
4. Reflect the selected canon into CLI runtime data.
5. Strengthen registry, schema, validation, and engine boundaries.
6. Revisit class identity, promotion, relic effects, economy, equipment, and
   optional endgame layers after the main route is stable.

The landed CLI skeleton proves that the route can be exercised. It is not final
canon for naming, regional texture, reward balance, encounter identity, UI
structure, class design, relic behavior, or endgame economy.

## Processing Order

### 1. Regional Identity Layer

Start by defining each region's world-map identity and town-hub identity.

This layer answers:

- What does the region look and feel like from the world map?
- What is the local hub or front-line camp's role?
- Which mood words are canon, and which are only temporary reference language?
- Which facilities reuse the existing families, and what local flavor do they
  carry?

Allowed outputs:

- Docs-only canon notes.
- Candidate names, mood boards, reference prompts, or mockup briefs.
- Explicit placeholder lists.

Closed at this layer:

- Runtime data edits.
- GUI static prototype implementation.
- Image generation as final assets.
- Asset-pipeline work.

### 2. Dungeon Exploration Layer

After regional and hub identity are stable, derive dungeon exploration identity.

This layer answers:

- What does each minor dungeon represent in the region?
- What does the main dungeon's phase split mean?
- What is the exploration mood, route pressure, and local hazard fantasy?
- Which current dungeon names are canon candidates and which are placeholders?

Dungeon identity should come before monster and item naming so encounter ecology
and drops grow from place, not from isolated stat blocks.

### 3. Monster And Boss Identity Layer

After dungeon identity is stable, derive normal monster and Boss identity.

This layer answers:

- Which enemies naturally live in each dungeon or phase?
- What does each Boss guard, prove, corrupt, or resolve?
- Which Bosses need special resolution hooks, and which can use generic rules?
- Which current enemy names are placeholders?

Boss uniqueness should not automatically mean scattered hardcode in
`game.py`. Special outcomes should later move toward concentrated progression
or Boss-resolution rules.

### 4. CLI Data Canon Layer

After regional, dungeon, monster, and Boss identity are stable, reflect the
selected canon into CLI data names and text.

This layer includes:

- Dungeons.
- Quests.
- Monsters.
- Bosses.
- Materials.
- Items.
- Equipment.
- Magic books and skills.
- Facility copy.

Data IDs should remain type-first and region-prefixed when new formal data is
planned, following `01_content/regional-data-template-v0.1.md`.

Do not rename large amounts of runtime data without a read-only data planning
gate, because renames may affect registry helpers, schema docs, validation,
smoke tests, bridge contracts, and save compatibility assumptions.

### 5. Engine Boundary Layer

After canon and data naming have a stable target, clean up engine boundaries in
small slices.

Likely slices:

- Boss resolution rules.
- Quest completion and reward rules.
- Region / town / facility navigation context.
- Dungeon visibility and unlock summaries.
- Ending and clear-state presentation.

Preferred direction:

- Keep CLI rendering thin where possible.
- Move progression and resolution rules out of ad hoc menu code.
- Let CLI and future GUI presentation consume shared runtime state or
  ScreenModel-style summaries.

Do not start this layer without a read-only runtime / data / schema planning
gate naming exact files, risks, and validation commands.

### 6. Registry And Schema Layer

Registry and schema work becomes important once regional canon is ready to be
reflected into data.

Registry should serve as:

- Data index.
- ID grouping helper.
- Validation helper.
- Runtime lookup helper.

Registry should not become:

- A second gameplay database.
- A place for prose canon.
- A dumping ground for progression logic.

Schema should first protect relationships that are easy to break:

- Region ownership.
- Quest prerequisites.
- Dungeon unlock and clear flags.
- Boss-to-dungeon and Boss-to-quest links.
- Progression markers.
- Drop and material availability timing.
- Recipe and Workshop material timing.

Balance details, exact formulas, promotion mechanics, and relic effects can wait
for later schema passes.

### 7. Class, Promotion, Relic, And Balance Layer

Class identity, promotion, relic effects, equipment curve, money curve, item
economy, combat tuning, and reward pacing are tightly coupled.

Do not turn these systems formal before the main regional route has enough canon
and data stability to support meaningful balance decisions.

Recommended order inside this layer:

1. Class role identity and current job rhythm.
2. Equipment and item economy baseline.
3. Relic marker interpretation.
4. Promotion options.
5. Relic active / passive effects.
6. Combat formula and enemy tuning passes.
7. Money, EXP, drop, synthesis, and Workshop balance passes.

Each item here is a separate high-risk planning gate, not a bundled phase.

### 8. Optional Elite And Endgame Layer

Optional elite hunts, rare materials, endgame synthesis treasures, post-clear
crafting, and high-end equipment sinks should be treated as late or DLC-like
content until the main route is stable.

These features may reserve planning slots early, but implementation should wait
until:

- Regional canon is stable.
- Main route quest and Boss identity is stable.
- Class and equipment roles are clearer.
- Money and material economy has a known target.
- Final-region crafting goals are understood.

Elite and rare-drop systems should not be allowed to force premature balance
decisions in the main route.

## Slice Workflow

Each debt slice should follow this sequence:

1. Direction discussion.
2. Docs canon or policy update.
3. Read-only preflight for the exact implementation surface.
4. Small implementation slice after explicit approval.
5. Focused validation.
6. Handoff or Hot Zone note when the result changes future startup context.

Skip directly to implementation only for already-approved narrow docs edits.

## GUI And Visual Policy

GUI, visual references, mockups, and image candidates may help discover regional
identity, but they do not become gameplay SSOT.

Visual work can inform:

- World map mood.
- Town hub composition.
- Dungeon exploration imagery.
- Monster and Boss silhouette direction.
- Facility presentation tone.

Visual work must not independently define:

- Quest completion logic.
- Dungeon unlock logic.
- Boss resolution behavior.
- Runtime data IDs.
- Combat formulas.
- Save compatibility.
- Registry or schema contracts.

Selected canon should be written back into docs first, then reflected into
runtime data only through an approved planning gate.

## CLI And GUI Responsibility Split

The CLI should remain a playable authority-facing runtime surface until a later
explicit decision changes that role.

The GUI should not hide unresolved CLI world-structure debt by implementing a
second world model. If regional maps, town hubs, local Guild views, or dungeon
lists become richer, the preferred direction is:

- Runtime owns progression and availability.
- Shared data / registry / helpers own lookup and grouping.
- CLI presents a simple text version.
- GUI presents a richer visual version.

Different rendering surfaces may exist, but they should not fork the gameplay
logic.

## Priority Rule

When two debts compete, prefer the one that reduces downstream churn.

Higher priority:

- Regional canon before data naming.
- Dungeon identity before monster and item naming.
- Quest readability before reward tuning.
- Progression rule cleanup before GUI bridge expansion.
- Registry / schema guardrails before large data expansions.
- Main route stability before optional elite and endgame sinks.

Lower priority:

- Polishing placeholder rewards before item identities exist.
- Formalizing promotion before class roles and equipment curve are clearer.
- Implementing relic effects before relic markers and class identity stabilize.
- Building DLC-like elite loops before the main route balance target exists.

## Boundaries

This policy does not approve:

- Runtime edits.
- Data edits.
- Schema edits.
- Save migration or manual `save.json` work.
- Combat formula changes.
- GUI static prototype implementation.
- GUI runtime bridge expansion.
- Image generation or formal asset pipeline work.
- Class transfer, promotion, or relic-effect implementation.
- Optional elite, rare-drop, synthesis treasure, or endgame economy
  implementation.

Before implementing any policy-derived slice, run the smallest matching
read-only planning gate and name exact files, risks, and validation commands.
