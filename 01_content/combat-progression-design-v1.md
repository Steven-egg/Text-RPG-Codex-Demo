# Combat Progression Design v1

Purpose: record the owner-approved player-side combat direction before a later
runtime/data/schema implementation gate. This is a planning SSOT, not
implementation approval and not a monster-balance table.

## Current Checkpoint

- `45cbbad` landed the attribute and status-effect rework.
- The current combat-planning slice sets `Sanctified Decay` and `Regeneration`
  to five turns and adds the deterministic
  `06_tools/test_combat_balance.py` harness.
- The harness measures representative four-job profiles. It is a player-output
  and action-cost tool; it does not yet simulate enemy survival pressure.
- Monster values remain the final balancing layer. Do not rebalance monsters
  until the player systems below are implemented and measured.

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
| Fire | direct damage +5%; physical lifesteal 5%; critical damage +15% | all elemental resistance +3% |
| Ice | magic damage +5%; maximum MP +10%; magic defense +10% | all elemental resistance +3% |
| Earth | maximum HP +10%; regeneration/healing +10%; damage-over-time +10% | all elemental resistance +3% |
| Thunder | agility +5; critical chance +5%; effect accuracy +10% | all elemental resistance +3% |

- Fire's lifesteal applies only to direct physical damage.
- Direct-damage bonuses exclude bleeding, poison, and Cleric magic
  damage-over-time; Earth owns the damage-over-time bonus.
- Selecting the shared choice on all four relics grants +12% all elemental
  resistance: meaningful in Final without replacing regional accessories.

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

After player systems land, use the balance harness at levels 10, 18, 25, 32,
and 40 with representative equipment. Only if monster tuning cannot meet the
target fight bands should job base/growth/every-three values be revisited.

## Future Implementation Gates

Implementation must be sliced and separately approved:

1. Combat foundation: monster race data/validation, status-damage handling,
   and Warrior Physical Charge plus focused unit checks.
2. Player content: regional equipment, Rogue offhands/Workshop upgrades,
   Mage books, Cleric mixed-stat weapons, and battle items.
3. Relic passives: data contract, durable selection state, Temple selection /
   free respec flow, stat and combat integration, and save compatibility.
4. Balance: harness profiles at milestone levels, job-growth review only if
   needed, then monster HP/attack/defense/magic-defense/resistance/status
   tuning.

Do not combine these gates into one implementation pass.
