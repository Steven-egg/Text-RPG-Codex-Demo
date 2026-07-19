# Combat Items, Support Skills, and Equipment Affixes — Construction Plan v1

## Purpose

Establish a staged route for three linked combat systems:

1. consumables and thrown battle items;
2. the practical value of support magic books;
3. repeatable-run equipment affixes.

This is a planning document, not an approval to alter gameplay data, runtime,
schema, or saves. Each implementation phase needs a separate owner approval
for its exact file surface.

## Current Implementation Checkpoint

- The five-group expedition supply contract is landed: sustain HP 3, emergency
  HP 1, MP, one selected throwable type (up to 2), and escape. Antidote remains
  outside those five groups.
- Regional HP/MP recovery is landed with fixed-or-percent formulas, and MP
  recovery remains a once-per-player-turn free action.
- `item_armor_piercer` is now a fixed-power physical throwable (90), uses enemy
  physical defense, and applies three turns of defense-down. It no longer uses
  enemy maximum-HP percentage damage.
- Fire/Ice/Earth/Thunder fixed-power (45) throwables are landed. They use the
  existing elemental-counter multiplier only, do not scale with job stats, and
  do not add monster elemental-resistance data.
- All damaging throwables consume a full player turn. No damaging throwable may
  be a free action.
- Phase 0 v2 measurement is landed in the two existing balance tools. It emits
  stdout-only records for opening-pair and finisher-only policies; B4 remains
  canonical and B5/B6 remain overlays.
- Quickstep and Froststep are landed as passive triggers with replacement
  priority. Cinder Mark remains MP 9 for five turns; its direct
  elemental-magic amplification is 50% after the fixed-window evidence.
- The deterministic equipment audit now emits 100 region × job × slot baseline
  records and keeps baseline budgets separate from affix-cap accounting. No
  affix increment, item generation, save contract, special-slot expansion, or
  elemental-infusion runtime behavior was added.
- Phase 4A now defines the instance, seed, and legacy-migration contract only.
  It does not approve an affix generator, runtime migration, or save-file
  operation.

## Design Decisions Already Chosen

- Recovery effects use a fixed floor or a maximum-resource percentage,
  whichever is larger. Examples:
  - small HP recovery: `max(30 HP, 30% max HP)`;
  - medium HP recovery: `max(70 HP, 45% max HP)`;
  - emergency HP recovery: `max(120 HP, 60% max HP)`;
  - focus drop: `max(12 MP, 30% max MP)`.
- A run has five supply groups: three sustain HP, one emergency HP, job-limited
  MP, up to two copies of one selected throwable type, and one escape item.
- Damage items are either physical throwables or elemental throwables.
  Elemental items use elemental advantage and resistance but must not scale from
  a job's `magic_attack`; this keeps them useful to every job.
- Region equipment remains the deterministic floor for balance measurement.
  Random affixes are optional variation on top of that floor, not a replacement.
- Unaffixed weapons remain physical for normal attacks. A single elemental
  infusion affix may change normal attacks and weapon follow-ups to one element;
  it must not overwrite an active skill's declared element.

## Current Findings and Constraints

- The historical B4 Boss QA kit remains a comparison only. Phase 0 v2 now also
  measures legal supply selections with explicit throwable timing policy.
- Opening-pair throwable use usually loses value to the two action costs;
  finisher-only use is currently the stronger measured policy. This is not a
  gameplay rule or a balance verdict.
- The dedicated support-window probes measure Quickstep, Cinder Mark, and
  Froststep independently of the core B4 rotation. The Cinder 50% adjustment
  is the minimum single-field correction that makes Ice/Earth/Thunder
  three-turn output repay positively; Final is outside its core-element scope.
- B6 affixes are QA-only, in-memory sensitivity overlays. They are not item
  generation, random drops, a schema contract, or save-compatible state.
- B4 Final now completes 5/5 for every job after the approved narrow Final
  Boss tuning. This is evidence for the measured profile, not a universal
  balance verdict; Boss action and final-HP bands remain diagnostics.

## Construction Sequence

### Phase 0 — Item and Support-Skill Measurement Gate (completed)

**Goal:** create evidence before changing gameplay.

Measure, with deterministic seeds and no repository report artifacts:

- no-item, legal-standard-kit, and item-sensitivity Boss runs;
- effective HP/MP restored per consumed slot;
- throwable contribution to victory, actions, and final HP;
- support-book break-even against the action that would otherwise be used;
- three, six, and ten-turn windows for Quickstep, Cinder Mark, and Froststep.

The report must distinguish player/job variation from region/monster variation.
It must not use B5 promotion or B6 affix overlays as canonical gameplay.

**Likely measurement surface:**

- `06_tools/test_combat_balance.py`
- `06_tools/test_combat_balance_report.py`
- a new stdout-only helper under `06_tools/`, only if the two existing tools
  cannot express the comparisons cleanly.

**Approval gate:** owner approves the exact measurement file surface before
any tool edits. No gameplay behavior changes in this phase.

### Phase 1 — Consumable Contract and Data Slice (completed)

**Goal:** turn the selected standard kit into a real, explainable player rule.

Define for each item:

- category: recovery, physical throwable, elemental throwable, cleanse, escape;
- floor-or-percent effect formula;
- carry-slot cost and per-run limit;
- eligible regions, unlock path, price, crafting/drop source;
- Boss legality and any per-battle limit;
- damage type, element if any, duration, and target stat interaction.

Initial tactical catalogue should stay deliberately small:

- armor piercer: physical utility throwable; fixed regional-tier damage plus
  short defense-down, with no target-maximum-HP percentage;
- one elemental throwable for each core element, introduced only where its
  counterplay has a clear regional purpose;
- antidote/cleanse and escape as non-DPS utility.

**Landed supporting surface:**

- `04_data/data/items.py`
- `03_engine/engine/game.py`
- `03_engine/engine/state.py`
- `02_schema/item.schema.md` if a new data field is needed
- targeted validation and combat tests under `06_tools/`

**Forbidden adjacent changes:** monster stats, player growth, equipment values,
relic values, promotion overlays, B6 rules, GUI, and save migration.

### Phase 2 — Support Magic-Book Value Slice (completed)

**Goal:** every purchasable support book has a visible tactical use and a
measured break-even.

Use Phase 0 evidence to choose one minimal correction per ineffective book:

- Quickstep/Froststep: improve the payoff of agility or add one narrow,
  player-visible benefit; do not add unrelated damage systems.
- Cinder Mark: ensure a fire-oriented follow-up window can repay its casting
  turn and MP, without making it mandatory for all casters.

The desired outcome is situational value, not automatic rotation dominance.

Completed outcome: Quickstep/Froststep use the existing passive-trigger path
with replacement priority. Cinder Mark retains its MP 9 and five-turn duration,
but raises direct elemental-magic damage by 50%.

**Landed supporting surface:**

- `04_data/data/skills.py`
- `03_engine/engine/game.py` and/or `03_engine/engine/state.py` only if the
  chosen effect cannot use existing hooks
- corresponding `02_schema/skill.schema.md` only if fields change
- targeted tests under `06_tools/`

**Forbidden adjacent changes:** item economy beyond Phase 1, monster tuning,
job growth, relic values, equipment values, GUI, and saves.

### Phase 3 — Deterministic Equipment Baseline Audit (completed)

**Goal:** define a stable stat budget before allowing randomization.

For each region × job × slot, record:

- expected base stat range;
- permitted stat families by slot;
- intended trade-offs, such as attack versus agility or defense;
- one explicit special-effect budget for pseudo-offhand follow-ups;
- element-infusion eligibility and its opportunity cost.

This phase treats existing B6 weights and caps only as QA accounting. They must
not silently become formal player-facing item rules.

**Likely planning/read-only surface:**

- `04_data/data/items.py`
- `02_schema/equipment.schema.md`
- `06_tools/test_combat_balance.py`
- `06_tools/test_combat_balance_report.py`

**Completed outcome:** the 100-record ledger exposes the live deterministic
floor, permitted slot families, pseudo-offhand effect budget, and unallocated
element-infusion opportunity cost. Baseline values that exceed legacy affix caps
are reported separately, not treated as affix-rule violations.

### Phase 4 — Affix and Replayability Design Gate

**Goal:** specify optional seeded variety without invalidating region balance.

Model each generated item as:

`deterministic regional base + optional one major affix + optional one minor affix`.

Examples of bounded affix families:

- major: elemental infusion, sharp (+attack), arcane (+magic attack), guarded
  (+defense/magic defense);
- minor: agile, precise, critical, or one-element resistance.

Rules:

- never roll multiple elemental infusions on one item;
- preserve job and slot legality;
- stay inside the regional base item's approved power envelope;
- use one run seed so a restarted run is reproducible;
- expose the generated result to UI only after a stable runtime contract exists.

**Likely implementation surface, pending a separate high-risk approval:**

- item data/schema
- generation and state runtime
- save compatibility/migration path
- validation, deterministic tests, and balance harness
- later GUI display surfaces only after runtime behavior is stable

This phase must begin with a read-only save/schema preflight. It is not covered
by approval for Phases 0–3.

### Phase 4A — Instance, Seed, And Migration Contract (approved design)

Phase 4A defines the contract only. It does not add an affix generator, alter
combat output, create item data, or migrate a real save file.

The runtime contract is intentionally instance-based: static `EQUIPMENT` stays
the deterministic regional base, while each generated copy has an
`equipment_instance` record. Inventory and equipped slots will ultimately hold
an instance reference for equipment, so multiple copies of the same base item
can carry different affixes without mutating global data.

The target state fields are:

- `state_version`: the migration contract version; absent legacy state is v1.
- `run_seed`: a persisted non-negative integer. The same seed plus the same
  equipment-generation order must reproduce the same affix results.
- `affix_roll_counter`: incremented only when an equipment instance is rolled.
- `equipment_instances`: `instance_id -> {base_item_id, generation_version,
  roll_index, major_affix_id | None, minor_affix_id | None}`.

Migration must convert every legacy inventory or equipped equipment id into a
distinct, unaffixed instance (`generation_version: 0`) before any new roll. It
must preserve quantities, job legality, equipped slot, and current HP/MP; it
must never retroactively roll an affix for an existing item. Static consumables,
materials, keys, and storage entries remain count-based IDs in the first pass.

The first runtime vertical slice must exclude `special`, head-slot pseudo-offhand
effect changes, elemental infusion, new shops/drops, GUI, and any save-file
manual operation. A later elemental-infusion slice may use the instance
contract, but must not overwrite a skill's declared element.

Affix caps apply to affix increments only. Existing deterministic baseline
stats, including baseline values already above legacy QA caps, are not affix
violations. One instance may have at most one major and one minor affix; the
two IDs must be distinct families, and no first-slice affix may change an
existing `normal_attack_followup` payload.

Required implementation tests after a separate approval: identical
seed/order reproducibility, legacy-state normalization, duplicate-base-item
independence, slot/job legality, no global `EQUIPMENT` mutation, cap accounting,
and unchanged unaffixed B4 results. B6 remains an in-memory QA overlay and does
not become the runtime generator.

## Required Validation Per Implemented Slice

Run the smallest relevant checks, then the cross-system checks when runtime or
data changes are approved:

```powershell
& '<bundled-python>' 06_tools/validate_data.py
& '<bundled-python>' 06_tools/test_combat_progression_foundation.py
& '<bundled-python>' 06_tools/test_combat_balance_report.py
```

For balance slices, also run deterministic B4 comparisons using stdout or TEMP
only. Do not create CSV/JSON artifacts in the repository. B3 may compare relic
impact; B5 and B6 remain sensitivity overlays, never canonical baselines.

## Next Approval Boundary

Phase 4A contract design is complete. No Phase 4B runtime implementation target
is pre-approved: instance resolution, migration, deterministic rolling, and
CLI presentation require a separate high-risk approval. Elemental infusion,
special-slot behavior, pseudo-offhand effect changes, GUI, and save-file
operations remain outside that future slice. Preserve B4 as the canonical
baseline while keeping B5/B6 as QA overlays.
