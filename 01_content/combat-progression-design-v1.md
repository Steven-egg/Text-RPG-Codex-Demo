# Combat Progression Design v1

Purpose: record the owner-approved player-side combat direction, landed
checkpoints, and the boundaries for later implementation gates. This remains a
planning SSOT, not blanket approval for further runtime or monster changes.

## Current Checkpoint

- `43cfc67` finalizes the current regional balance diagnostics after the
  attribute/status foundation, player-content, and relic-passive slices.
- The deterministic harness measures representative four-job profiles,
  support windows, tactical strategies, deterministic equipment floors, and
  role-aware Boss diagnostics. It remains a measurement tool, not a blanket
  balance verdict or production enemy-AI model.
- The approved narrow balance slice adjusted Fire Cinder Seal Sentinel attack,
  Final Demon King HP/attack/defense/magic defense, and Cinder Mark direct
  elemental-magic amplification. It did not alter job growth, promotion
  preview, affix runtime, special slots, elemental infusion, GUI, or saves.

## Quality Equipment Checkpoint — 2026-07-26

This checkpoint records the owner direction and landed four-job quality slice.
It is the current bridge from the completed player-content baseline to the
next measurement gate; it does not approve a new monster or promotion slice.

### North Star And Boundaries

- Four jobs should clear the five regions through distinct, viable strategies.
  Quality equipment is a bounded build direction, not a replacement for job
  skills, relic choices, or supplies.
- Quality keeps one shared contract: Normal is unaffixed; Fine/Rare use a
  fixed major affix; Epic/Legendary add that pattern's fixed minor affix;
  values use `1.00 / 1.15 / 1.35 / 1.60` multipliers.  Synthesis weights,
  Boss-quality mapping, sale multipliers, v3 migration, and no-retro-roll
  rules are shared by all four jobs.
- `special` remains outside quality.  No new free-form rerolls, independent
  `+N`, elemental weapon infusion, or a second parallel counter system are
  part of this slice.

### Landed Four-Job Quality Direction

- Boss routes are no longer job-gated: all four jobs can challenge eligible
  five-region Bosses and receive a quality instance from their legal regional
  candidate pool.  Fire uses the untagged starting/Fire equipment pool.
- Warrior weapons have two fixed patterns.  Both add `+4` percentage points
  per Physical Charge stack to charge-consuming skills; Epic+ then chooses
  either a `+1` charge cap or a 25% chance for one extra Charge after a normal
  attack.  The cap uses floor-after-quality-scaling and may reach the new cap
  on that attack.
- Mage weapons retain `magic_attack` as their common major direction.  Epic+
  chooses either direct elemental magic `+6%` or weapon magic defense `+1`.
  The elemental effect excludes neutral magic, DoT, fixed battle items, and
  physical damage; it adds with direct-magic relic bonuses before the existing
  Cinder Mark multiplier.
- Warrior/Mage head, body, and accessory patterns remain defensive: physical
  guard or magic guard plus a region-aware resistance minor.  Ice/Earth/
  Thunder receive `+5` to their matching resistance; Final receives `+2` to
  each elemental resistance.
- Rogue's head pseudo-offhand exception and Cleric's existing DoT, regeneration,
  and fixed-item boundaries remain unchanged.

### Next Balance Gate

1. Build a non-S10 measurement harness using fixed seeds, identical base items
   and patterns across Fine/Rare/Epic/Legendary, then run all four jobs against
   five-region Boss paths.
2. Compare no-supply, conservative HP/MP, throwable-output, and legal mixed
   supply strategies.  Never use retired `item_potion_m`; record survival,
   turns, final HP/MP, supply use, and adjacent-quality monotonicity.
3. Adjust player affix values first if the measurement identifies a narrow
   problem.  Then make a first unpromoted monster pass for regional/Boss
   HP/attack/defense/magic defense, element, race distribution, and existing
   status effectiveness.
4. Plan promotion before final monster numbers are frozen; implement it after
   that first monster baseline; then run a final late-game/Final-Boss pass.

### Owner Decisions Needed Before Numeric Sign-Off

- Define per-region and Boss success bands: survival rate, expected turns,
  permitted supply use, and whether role-specific risk profiles are intended.
- Confirm the final Charge bonus/cap/extra-gain values and the cap rounding
  rule; confirm Mage elemental percentage and the defensive-affix scale.
- Confirm the Final resistance split, seed list/sample count, acceptable
  quality deltas, and the escalation order when player and monster changes
  could both solve a measured gap.
- Define promotion's timing and power budget before the final monster pass.

## Locked Combat Roles

| Job | Combat identity |
|---|---|
| Warrior | Normal attacks build Physical Charge. Physical skills consume it for Boss-oriented burst. No counterattack system. |
| Mage | Elemental burst. Weapons provide magic attack; magic-book skills provide element, MP cost, and damage multiplier. |
| Rogue | Highest sustained physical DPS through a main weapon, head-slot pseudo-offhand, criticals, and race-aware status effects. |
| Cleric | Long-fight mixed damage: magic damage-over-time, regeneration, basic attacks, and battle items. |

### Warrior: Physical Charge

- A normal attack gains one `Physical Charge`, up to three stacks.
- Charge does not decay during that combat and is cleared when combat ends.
- A physical skill consumes all Charge stacks.
- Each physical skill owns `charge_bonus_per_stack`; planned progression is
  `8% / 10% / 12% / 14% / 16%` for the starting, Ice, Earth, Thunder, and
  Final skill tiers. Three Final stacks therefore add 48% to that skill.
- Regional weapons raise normal equipment stats; they do not own the Charge
  multiplier. Rare battle items may lower enemy physical defense.

### Mage: Magic Books

- Every regional Mage inventory provides two books: one MP-efficient mainstay
  spell and one high-MP, high-multiplier burst spell.
- Mage weapons increase `magic_attack` only; they have no additional weapon
  trigger in the first implementation.
- Elemental weakness remains the source of counterplay. Do not add a second
  weapon-only weakness multiplier.

### Rogue: Main Weapon, Offhand, and Statuses

- Main weapons supply the primary attack value plus critical chance and/or
  critical-damage support.
- Head-slot pseudo-offhands supply smaller secondary damage and chance-based
  effects. Normal attacks use the offhand follow-up; skills apply their own
  status effects.
- A new regional offhand is gained in Ice, Earth, Thunder, and Final, and each
  may receive a small Workshop upgrade. Older offhands remain selectable for
  their tactical effect.

| Offhand stage | Intended specialty |
|---|---|
| Initial sleeve blade | Establishes the offhand follow-up pattern. |
| Ice | Bleeding. |
| Earth | Poison. |
| Thunder | Lifesteal. |
| Final | Higher secondary damage; stronger follow-up against a bleeding or poisoned target. |

#### Races and Physical Statuses

Monsters need one mandatory race tag: `beast`, `humanoid`, `plant`,
`construct`, `spirit`, or `aberration`.

| Race | Bleed | Poison |
|---|---|---|
| beast | effective | normal |
| humanoid | effective | normal |
| plant | ineffective | effective |
| construct | ineffective | ineffective |
| spirit | ineffective | ineffective |
| aberration | normal | effective |

`effective` Bleed and Poison ticks deal `1.25x` damage; `normal` deals `1.0x`;
`ineffective` remains unappliable (and therefore deals `0x`). This multiplier
applies only to those two physical status ticks, before the existing relic
damage-over-time bonus. It does not affect Rending Wound, Sanctified Erosion,
Cleric magic damage-over-time, direct hits, or status application chance.

- Bleeding lasts three turns; poison lasts five turns.
- Both use a separate status-damage path that ignores physical defense.
- An ineffective status cannot be applied. Existing effect accuracy and the
  target's physical-status resistance still control successful application
  where the status is valid.
- Construct and spirit encounters are intentional Rogue pressure points;
  direct damage, armor-piercing items, and other jobs remain their answers.

### Cleric: Sustain and Battle Items

- Cleric has lower direct physical attack than Warrior and wins long fights by
  combining magic damage-over-time, regeneration, basic attacks, and items.
- Cleric weapons provide both `attack` and `magic_attack`, with magic attack as
  the larger contribution.
- A regional Cleric weapon may strengthen the Cleric magic damage-over-time
  while regeneration is active; this is the only planned Cleric weapon trigger.
- Cleric damage-over-time and a battle-item damage-over-time may coexist.
- Reusing the same class of battle-item damage-over-time refreshes it rather
  than stacking it. One-shot battle items deal fixed immediate damage and do
  not scale with attack, magic attack, or criticals.
- Cleric damage-over-time and regeneration both last five turns.

## Equipment Direction

Each Ice, Earth, Thunder, and Final region is planned to provide:

- four main weapons, one per job;
- four body armors: Warrior heavy armor, Mage light robe/magic-defense armor,
  Rogue light armor, and Cleric medium holy robe;
- one Rogue head-slot pseudo-offhand;
- one shared elemental-resistance accessory.

Armor and accessories are stat-only in the first pass. Combat behaviors stay
concentrated in job skills, Rogue offhands, and the Cleric weapon/skill link.

## Relic Passive Choices

Each of the four enshrined relics offers four choices. The player selects one
per relic at the Temple and may respec there for free. Four active choices are
possible after all relics are enshrined.

| Relic | Themed choices | Shared choice |
|---|---|---|
| Fire | direct damage +8%; physical lifesteal 7%; critical damage +20% | all elemental resistance +5% |
| Ice | direct magic damage +8%; maximum MP +15%; magic defense +15% | all elemental resistance +5% |
| Earth | maximum HP +15%; regeneration/healing +15%; damage-over-time +15% | all elemental resistance +5% |
| Thunder | direct physical damage +8%; critical chance +8%; effect accuracy +15% | all elemental resistance +5% |

- Fire's lifesteal applies only to direct physical damage.
- `direct damage` means normal attacks and skill hits that deal damage
  immediately, including physical and magic damage, but excluding all
  periodic damage-over-time ticks.
- Direct-damage bonuses exclude bleeding, poison, and Cleric magic
  damage-over-time; Earth owns the damage-over-time bonus.
- Ice keeps the existing `magic_defense` stat rather than adding a new generic
  damage-reduction formula. A future balance gate may reconsider that choice.
- Thunder intentionally replaces the previous weak agility option with direct
  physical damage; the current game has no speed/initiative layer that makes a
  small agility bonus a meaningful relic choice.
- Selecting the shared choice on all four relics grants +20% all elemental
  resistance. This is a generalist defensive route; it will be measured only
  in the later balance phase.

### Relic Choice Intent

- Fire is the general direct-output relic. All jobs can use direct damage;
  Swordfighter and Rogue gain additional physical sustain or critical value.
- Ice is the Mage-first relic, with Cleric as a secondary user through magic
  output, MP, and magic defense.
- Earth is the sustain relic: Cleric favors regeneration/healing and magic
  damage-over-time, Rogue can favor physical status damage-over-time, and all
  jobs can take maximum HP or the shared resistance option.
- Thunder is the Rogue-first critical/status relic and a Swordfighter
  secondary relic through direct physical damage and critical chance.

## Progression and Balance Order

The current linear job growth model remains in place: per-level growth plus
the existing every-three-level bonus. Do not introduce late-game stat-curve
acceleration at this stage.

| Region | Expected player level | Boss ceiling |
|---|---:|---:|
| Fire | 1–10 | 12 |
| Ice | 10–18 | 20 |
| Earth | 18–25 | 27 |
| Thunder | 25–32 | 34 |
| Final | 32–40 | 43 |

The current regional baseline has been measured at the representative level
bands and tuned through the approved narrow monster/data slice. Job
base/growth/every-three values remain unchanged; reconsidering them requires a
new read-only planning gate with evidence that further narrow tuning cannot
meet the intended fight bands.

## Completed Gates And Next Boundary

The following separately approved slices are landed: combat foundation;
regional player content and tactical items; relic passive selection, persistence,
and application; and the current balance measurement / narrow monster-tuning
pass. B4 Final completes 5/5 for each job, while Boss action and final-HP bands
remain role-specific diagnostics rather than hard gates.

No next combat implementation target is pre-approved. Any future job-growth,
promotion, affix, special-slot, elemental-infusion, relic-system, save, GUI, or
additional monster-tuning proposal must begin with its own read-only planning
gate and must not be combined with an unrelated slice.
