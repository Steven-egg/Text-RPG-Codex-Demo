# Phase 4B Equipment Quality, Affix, Upgrade, and Enchant Specification v1

## Status and Scope

This is a design draft that follows the Phase 4A instance, seed, and legacy
migration contract. It does not approve runtime, data, schema, save, GUI, or
test changes. It does not replace the existing Phase 4A contract.

The goal is to turn one static regional equipment base into a player-readable
equipment progression model without changing the existing B4 baseline.

## Player-Facing Equipment Model

An equipment name may be composed as:

`[quality] [prefix] base equipment [+upgrade] [suffix]`

Examples:

- `普通的鐵劍`
- `精良的敏捷鐵劍 +1`
- `稀有的火焰長劍`
- `史詩的守護者法杖 +3`

The five layers have separate responsibilities:

| Layer | Responsibility |
|---|---|
| Base equipment | The existing static `EQUIPMENT` entry; regional floor, slot, jobs, price, and original stats remain authoritative. |
| Quality | A player-facing strength band: normal, fine, rare, epic, or legendary. It controls the available affix budget and presentation; it is not an extra uncontrolled stat bundle. |
| Prefix | One optional main directional affix, such as agile, guarded, arcane, or a future elemental direction. |
| Upgrade | A separate `+N` progression owned by the relevant workshop. It improves one selected instance and must not replace its base or affixes. |
| Suffix | One optional secondary affix, such as guarding, starry, or a future elemental/utility direction. |

Quality, affixes, upgrades, and enchant services must all obey one total
increment budget. Existing base stats do not spend that budget.

## Randomness With Direction

Phase 4B should be roguelite-style random, not perfectly job-locked.

- Common utility effects may appear on several equipment types.
- Each slot, weapon type, and job has weighted preferences rather than a fully
  closed pool. A staff can rarely receive an unusual physical or poison-related
  direction if that effect is implemented and safe.
- Effects that have no live runtime meaning, violate a first-slice boundary,
  or create a known unsafe combination are hard exclusions.
- Softly mismatched effects are allowed at low weight when they create an
  understandable optional build rather than a dead result.
- One instance has at most one major affix and one minor affix. Affixes from
  the same effect family cannot stack on that instance.

The existing name lexicon is a candidate vocabulary source, not runtime
authority. Before reuse, every word must map to a supported stat/effect,
eligible slots, a family, and a bounded increment.

## First Affix Candidate Set (Design Only)

The first live set should be deliberately smaller than the name lexicon. It
uses only stats already recognised by equipment validation and the current
deterministic equipment audit. Exact values and weights remain unapproved.

| Candidate family | Example player-facing words | Intended slots | Notes |
|---|---|---|---|
| Physical edge | sharp, sturdy | weapon, body | Attack or defense direction, subject to slot legality. |
| Arcane | arcane, starry | weapon, head, accessory | Magic-attack or magic-defense direction. |
| Agile | agile, light | weapon, head, body, accessory | Agility direction. |
| Precise / critical | precise, keen | weapon, head, accessory | Effect accuracy or crit direction. |
| Element ward | fire ward, frost ward, earth ward, thunder ward | head, body, accessory | Resistance only in the first set; not elemental weapon infusion. |
| Expedition utility | lucky, pathfinder | accessory only | Rare-drop or trap-evasion direction, with strict loadout caps. |

The following lexicon concepts remain outside the first set even if their
names are useful inspiration: direct elemental damage, poisoning, healing,
HP/MP regeneration, max-HP/MP adjustments, evasion, blocking, dark resistance,
and every effect that has no current validated equipment stat. They need a
separate combat and balance decision before they become live affixes.

Quality labels should not be copied from the B6 QA profiles. B6 labels and
budgets remain measurement-only. A later implementation may reuse the Chinese
player-facing words `普通`, `精良`, `稀有`, `史詩`, and `傳說`, but must define
their live generation and increment rules separately.

## Equipment Sources and Quality Timing

The first player-facing acquisition model has three distinct routes:

| Route | Player result | Randomness |
|---|---|---|
| Workshop purchase | A fixed regional base item that gives every player a reliable equipment floor. | None. |
| Workshop strengthening | A selected instance receives a fixed `+N` improvement using known materials and cost. | None. |
| Synthesis / enchant service | A recipe creates an equipment instance or adds an allowed affix result in exchange for materials and higher cost. | Controlled random result. |

Quality is determined when an equipment instance is created by its applicable
route. A workshop's fixed item is always `普通 +0`; a synthesis recipe initially
produces only `精良` or `稀有` results. Strengthening changes `+N`, not quality.

This keeps workshop gear as a dependable baseline while making synthesis the
first optional roguelite pursuit. A later, separately approved "ascension" or
"breakthrough" system may allow a quality increase after a material milestone.
It must not be implicitly coupled to every `+N` step, because that would force
an unnecessary fixed mapping such as `+3 = rare`.

## Equipment Comparison Contract

Before any random acquisition route is exposed to players, the runtime needs
one reusable, side-effect-free comparison result for a candidate instance and
the currently equipped item in the same slot. This is a gameplay presentation
contract, not a CLI-only developer tool.

The comparison must report at least:

- base name, quality, affixes, and `+N` for both sides;
- every relevant supported stat as before, after, and signed delta;
- absent versus gained versus replaced affix/family information;
- job and slot compatibility, including a clear reason when the candidate
  cannot be equipped;
- no mutation to the candidate, equipped instance, `EQUIPMENT`, or state.

CLI purchase, synthesis, inventory, and equip confirmation screens will render
this shared result before the action. A future GUI consumes the same result;
GUI presentation is not part of the first runtime slice. Automated tests use
the same contract to verify numerical deltas and independence, rather than
creating a second AI-only comparison tool.

## Facility Roles

| Facility | Future role |
|---|---|
| Weapon / armor workshops | Strengthen a selected equipment instance from `+N` to `+(N+1)` using defined materials and cost. |
| Synthesis / enchant service | Add, replace, or alter a permitted affix on a selected instance. The exact player choice versus random result remains a later decision. |
| Drops and shops | May later create new instances at a defined quality/affix result. They are outside the first runtime slice. |

An upgrade or enchant always targets one instance, never the global
`EQUIPMENT` entry and never every copy of the same base item.

## Special Slot Decision

The current `special` slot is an adventure-support / badge slot, not a combat
equipment slot:

- `special_trial_badge` grants guild-point gain.
- `special_focus_pouch` grants one focus item at dungeon entry.

For this phase it remains outside quality, affix, upgrade, and enchant rules.
Its future presentation may be renamed from "special" to "badge" or
"adventure gear". It is not currently a promotion-title slot, accessory
replacement, offhand, or combat-affix carrier.

This is a frozen boundary for the first three Phase 4B slices: existing and
new special-slot items remain badge/adventure gear, not generated equipment.

## Phased Implementation Direction

1. Preserve the Phase 4A instance and legacy-migration foundation, with no
   affix retro-roll for existing equipment.
2. Add a bounded quality and affix data contract for supported combat stats
   only; preserve unaffixed B4 parity.
3. Add CLI display and one safe equipment-generation source after separate
   approval.
4. Add workshop `+N` strengthening as a separate instance-targeted slice, with
   an initial maximum of `+3`.
5. Add synthesis/enchant actions as a separate slice after their player-choice
   and reroll rules are approved.
6. Consider drops, shop generation, elemental infusion, GUI, and special-slot
   changes only in later approvals.

## Decisions Still Needed Before Runtime Work

- Whether synthesis/enchantment is deterministic choice, weighted random,
  reroll, or a mixture of those models.
- Whether and how a later ascension/breakthrough system can raise quality
  without tying quality mechanically to every `+N` step.
- Which effects are supported in the first affix set, including whether any
  DOT-related effect is allowed at all.
- The exact quality-to-budget table and per-slot / loadout increment caps.
- The user-visible Chinese terms and final name ordering for quality, prefixes,
  suffixes, and `+N`.

## Permanent Boundaries

- Static `EQUIPMENT` remains the deterministic regional base and is never
  mutated for a player copy.
- B4 remains canonical. B5 and B6 remain QA overlays and do not generate live
  equipment.
- No first-slice special-slot changes, head-slot pseudo-offhand changes,
  elemental infusion, new shops/drops, GUI work, promotion work, job growth,
  or monster-stat changes.
- No manual read, write, creation, or overwrite of `save.json`.
