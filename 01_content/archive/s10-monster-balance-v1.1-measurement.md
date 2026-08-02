# S10 Monster Balance v1.1 Measurement

## Round 5: Warrior growth and regional cadence

The fixed five-seed probes showed that a single global attack reduction could
not satisfy both targets: 60% of the prior Warrior attack growth preserved
normal encounters but left Thunder/Final Bosses at 6--8 actions, while 20%
put those Bosses at 10--12 but made normal encounters take 6--10 actions.

The applied character-side resolution is deliberately split by encounter
cadence, not enemy stats: Warrior attack growth is 3.0 -> 1.5; Heavy Slash,
Thunder Strike, and Abyss Overlord Slash are 1.25 -> 1.3125, 1.6 -> 2.08, and
2.0 -> 3.6 respectively; normal
Thunder/Final encounters consume their regional strike at two Physical Charge
stacks, while Bosses after Fire retain charge and use direct attacks.  Fire
continues to spend the three-stack charge skill.

| Scenario | Normal/Boss actions (min/median/max) | Wins | Avg final HP | Supplies | Result |
|---|---:|---:|---:|---:|---|
| Fire | 4/5/5; 12/13/14 | 5/5; 5/5 | 98%; 39% | 0.0; 0.2 | target interval |
| Ice | 4/4/5; 13/13/14 | 5/5; 5/5 | 99%; 96% | 0.0; 0.0 | target interval |
| Earth | 4/4/5; 12/12/13 | 5/5; 5/5 | 99%; 96% | 0.0; 0.0 | target interval |
| Thunder | 3/4/5; 10/10/11 | 5/5; 5/5 | 99%; 98% | 0.0; 0.0 | target interval |
| Final | 3/4/5; 11/12/14 | 5/5; 5/5 | 97%; 98% | 0.0; 0.0 | target interval |

The Fire Boss is the survival boundary: the five trials remain victories with
an average 39% final HP and 0.2 configured supply items consumed per trial.
This replaces
the earlier overfast Warrior outcome without monster HP changes, class-based
enemy scaling, or empty actions.

## Round 4: Warrior charge probe and late-Rogue Boss DoT policy

All probes used the fixed five S10 seeds and stdout only.  No probe changed
monster data, introduced job-specific monster HP, or restored a post-table
monster override.

### Warrior

The five Boss rows were 5/5 victories but too fast: Fire 9--10, Ice 8,
Earth 6--8, Thunder 4--6, and Final 5--8 actions.  The normal rows were all
already in the 3--5 target band.  Removing all charge bonus, restoring the
authored per-stack values (0.08 / 0.10 / 0.12 / 0.14 / 0.16), reducing the
charge bonus to 40%, reducing regional skill multipliers to 75%, and never
casting the charged skill were measured as stdout-only variants.  None brought
Thunder and Final Bosses into 10--15 without also taking a normal row outside
its band when base attack was reduced.  No Warrior data or rotation change was
applied: an empty action or Boss-HP adjustment would only pad the measurement,
not correct an actionable combat imbalance.

### Rogue late Bosses

| Policy | Earth Boss | Thunder Boss | Final Boss | Wins | Result |
|---|---:|---:|---:|---:|---|
| Before: bleed then poison whenever available | 5/6 | 4/5 | 5/6 | 5/5 each | overfast |
| After: direct attacks on Earth/Thunder/Final | 11/13/14 | 10/12/12 | 11/12/13 | 5/5 each | target interval |

The before rows averaged 515.8/534.2, 588.4/591.6, and 870.6/1129.4 direct/DoT
damage for Earth, Thunder, and Final respectively.  After the policy, the
corresponding direct/DoT averages are 1050/0, 1180/0, and 2000/0.  The later
Bosses were dying before a second status cycle repaid its setup action, so the
S10 rotation now reserves the complete bleed/poison opener for normal
encounters and uses direct attacks against the Earth, Thunder, and Final
Bosses.  Fire's existing
Rending Spike policy and Ice's status-immunity fallback are unchanged.

## Round 3: character-side sensitivity and Fire Rogue DoT policy

All probes used the fixed five S10 seeds and stdout only. They did not mutate
monster data, introduce job-specific monster HP, or restore a post-table
monster override.

### Mage sensitivity (current values)

| Variant | Boss action ranges (Fire / Ice / Earth / Thunder / Final) | Finding |
|---|---|---|
| Current rotation | 5-6 / 6 / 4 / 3 / 3 | Overfast in every region. |
| No burst | 5-6 / 6 / 4 / 3 / 3-6 | Burst is not the main cause; most fights end before its turn. |
| No elemental counterplay | 7-8 / 6 / 4 / 3-5 / 3-6 | Only Fire changes materially. |
| Restore pre-tail MP costs | 5-6 / 6 / 4 / 3 / 3 | MP costs are not binding in these short fights. |
| Scale all ten Mage rotation spell multipliers to 0.50 | 11-12 / 12 (0/5) / 12 / 9-10 / 10-11 | Tempo improves, but Ice Boss loses all five trials; rejected. |

The first uniform 50% proposal was rejected, then re-tested as a single Mage
core rebalance: base HP 80 -> 110, base DEF 5 -> 12, normal rotation spells
set to 47% of their former multipliers, and the two Earth counter-spells set
to 33% (the minimum that keeps Thunder Boss at 5/5). Final Mage outcomes are:

| Scenario | Normal/Boss actions (min/median/max) | Wins | Result |
|---|---:|---:|---|
| Fire | 3/4/4; 12/12/13 | 5/5; 5/5 | target interval |
| Ice | 4/5/5; 14/15/15 | 5/5; 5/5 | target interval |
| Earth | 4/4/4; 12/13/13 | 5/5; 5/5 | target interval |
| Thunder | 5/5/5; 13/13/13 | 5/5; 5/5 | target interval |
| Final | 4/4/4; 11/11/12 | 5/5; 5/5 | target interval |

This keeps all Mage rows inside the fixed 3-5 normal and 10-15 Boss bands
without changing monster data or using job-specific monster scaling.

### Fire endgame Rogue

| Policy | Wins | Actions (min/median/max) | Avg direct / DoT damage | Avg supply items | Result |
|---|---:|---:|---:|---:|---|
| Existing normal-only fallback against construct immunity | 5/5 | 18/19/20 | 520 / 0 | 2.4 | outside target |
| One `item_rending_spike`, opening application | 5/5 | 15/17/17 | 405 / 90 | 3.0 | still slow |
| Two `item_rending_spike`, opening plus DoT refresh | 5/5 | 11/12/13 | 290 / 180 | 2.6 | target interval |

Applied the third policy only to the Fire Boss Rogue supply override and Rogue
rotation. The construct still rejects bleed and poison; the Rogue uses its
legal class-only rending supply at opening and expiry, then resumes normal
attacks. Other jobs retain the Fire profile's original `item_armor_piercer`.
This is an explicit player-side loadout/rotation policy, not a monster HP or
stat adjustment.

## Scope

S10 keeps fixed monster data in `04_data/data/monsters.py`.  Regional equipment,
relic counts, supply profiles, and the five fixed seeds remain the only dynamic
conditions.  No runtime class-specific monster HP scaling is used.

## Round 1: fixed monster-table starting values

Applied the requested S10 values (including removal of the post-declaration
monster HP mutation).  The main survival exception was Fire endgame Rogue:

| Scenario / job | Boss ATK | Wins | Actions (min/median/max) | Avg supply items | Avg final HP % | Diagnosis |
|---|---:|---:|---|---:|---:|---|
| Fire endgame / Rogue | 26 | 0/5 | 13/14/14 | 0.0 | 0.00 | survival_insufficient; not_all_victories |

The raw rows showed that the Rogue had the legal `boss_standard` inventory but
its rotation never selected a recovery item.  This is a player-side policy
issue, rather than a reason to add class-specific boss HP.

## Round 2: minimal survival policy correction

| Change | Before | After | Reason |
|---|---|---|---|
| Boss recovery selection | Cleric-only hard-coded item selection; non-Clerics did not consume configured recovery supplies | All jobs may select an available configured HP/MP recovery item below 25% HP / below 4 MP | Make the existing S10 supply profile a real player-side condition without changing enemy behavior by job |
| `boss_cinder_seal_sentinel` ATK | 26 | 24 | The permitted two-point reduction converts the Fire Rogue from 0/5 deaths to five wins after supply timing is enabled |

| Scenario / job | Boss ATK | Wins | Actions (min/median/max) | Avg supply items | Avg final HP % | Diagnosis |
|---|---:|---:|---|---:|---:|---|
| Fire endgame / Rogue | 24 | 5/5 | 18/19/20 | 2.4 | 41.05 | outside_target_interval |

The survival failure is resolved, but the Rogue is now over the 10–15 Boss
action target.  It remains explicitly not passed; the next adjustment should
improve Rogue Boss damage/DoT efficiency or potion timing, not further reduce
the Boss's HP globally.

## Final round observations

- All five seeds now win for every S10 row.
- The target interval is reached by all four Fire/Ice/Earth normal-class rows
  except the explicitly diagnosed fast/slow cases, and by the Cleric and Ice
  Rogue Boss rows.
- Mage normals and most Mage/Warrior/Rogue Boss rows still report
  `overfast_kill`; Thunder and Final Bosses are especially short.  These remain
  character/loadout/rotation investigation items, not a reason to add hidden
  monster overrides.
- Final-entry Cleric, Ice/Thunder-entry Rogue, and Thunder-entry Cleric remain
  above the normal 3–5 action target.
