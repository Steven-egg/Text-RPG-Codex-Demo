# Codex Handoff Short

Purpose: compact handoff for continuing Codex work. Read live files before
editing; this document identifies the current boundary, not gameplay SSOT.

## Current State

- Work directory: `C:\Users\user\OneDrive\文字冒險遊戲`
- Current committed checkpoint:
  `c44ddb7 2026-07-19 feat(equipment): add unaffixed instance lifecycle baseline`.
- Inspect `git status --short` before editing. Do not stage, commit, create a
  branch, push, or archive unless explicitly requested. Known LF-to-CRLF
  warnings must not be cleaned up opportunistically.
- Runtime content scope: the five-region mainline is present in data and engine
  flow, not merely a future skeleton. The current inventory reports 21 dungeon
  entries, 28 quests, 20 bosses, and 93 monsters. Do not describe the project
  as needing its Fire / Ice / Earth / Thunder / Final route built from scratch.

## Active OneDrive Worktree

- B4B-2 is implemented but uncommitted: non-special equipment instances may
  resolve the fixed static affixes `major_sharp` (attack +1), `minor_agile`
  (agility +1), and `minor_fire_ward` (fire resist +5). Resolver output stays
  detached; invalid IDs, tiers, and slots do not apply increments.
- B4B-3a is implemented but uncommitted: the CLI equipment summary uses
  effective stats, while the comparison panel renders major/minor affix views
  and incompatibility reasons. No acquisition source, rolling, quality, `+N`,
  shop, synthesis, drop, GUI, or save behavior was added.
- Run `06_tools/test_equipment_affix_resolution.py`,
  `06_tools/test_equipment_cli_affix_presentation.py`,
  `06_tools/test_equipment_instance_lifecycle.py`, and
  `06_tools/test_equipment_reference_adapter.py` before the next equipment
  slice. The shared OneDrive worktree carries these uncommitted changes to the
  other machine; still inspect `git status --short` there before editing.

## Landed Combat State

- The player physical-defense buff is single-pass: `get_stats()` owns the
  player-side modifier and enemy damage does not apply it again. The value-model
  audit keeps a zero single-pass delta. The Final Warrior sample is now
  floor-clamped at damage 1, so it checks consistency rather than the size of
  that defense gain.
- Expedition supplies have five groups: sustain HP (3), emergency HP (1), MP,
  throwable, and escape. Unused supplies are not pre-deducted. Antidote keeps
  its existing combat rule outside the five groups.
- Regional HP/MP potions use their dedicated slots and fixed-or-percent recovery
  formulas. MP recovery remains free but is limited to once per player turn.
- Battle throwables are landed with CLI and live-GUI parity:
  `item_armor_piercer` is physical fixed-power 90 plus three turns of defense
  down; Fire/Ice/Earth/Thunder throwables use fixed power 45 and the existing
  elemental-counter multiplier only. A run selects one throwable type and can
  carry at most two.
- Role-specific tactical throwables are also landed: Cleric-only
  `item_sanctified_ash_vial` deals a fixed 20 hit and refreshes five turns of
  Sanctified Erosion at 15 fixed damage per tick; Warrior/Rogue-only
  `item_rending_spike` deals a fixed 25 hit and refreshes five turns of
  Rending Wound at 18 fixed defense-ignoring damage per tick. Both use a full
  player turn, occupy the existing throwable slot, and may coexist with their
  intended non-item damage-over-time effects.
- All damaging throwables consume a full player turn. They must never become
  free actions; only MP recovery remains a free action.
- Current element throwables do not scale from job attack/magic attack, defense,
  criticals, or direct-damage relic effects. No monster elemental-resistance
  data contract was added.
- Bleed and Poison now use race-aware tick damage: `effective` is 1.25x,
  `normal` is 1.0x, and `ineffective` remains blocked before application.
  The multiplier applies only to those two physical status ticks, before the
  existing relic damage-over-time bonus; it does not affect Rending Wound,
  Sanctified Erosion, Cleric magic damage-over-time, direct hits, or status
  application chance.
- Quickstep and Froststep are passive triggers with replacement priority;
  Froststep replaces the Rogue pursuit trigger when its higher-priority
  condition applies. Cinder Mark remains MP 9 for five turns and increases
  direct elemental-magic damage by 50%.
- The deterministic equipment audit now emits 100 region × job × slot baseline
  ledger records. It reports deterministic budgets and affix-cap overages
  separately; no affix increment, special-slot expansion, or elemental
  infusion runtime contract was added.
- Fire Cinder Seal Sentinel attack is 28. Final Demon King values are HP 2400,
  attack 135, defense 75, and magic defense 110. B4 Final now completes 5/5
  for all four jobs. Boss action and final-HP bands are role-specific
  diagnostics, not hard balance gates.

## Measurement State

- B4 remains the canonical gameplay baseline. B3 compares relics only; B5/B6
  remain QA overlays and must not become player-facing baseline rules.
- `06_tools/test_combat_balance.py --phase0` is stdout-only Phase 0 v2
  measurement. It compares no item, historical B4 QA kit, and legal two-item
  physical/elemental kits with `opening_pair` and `finisher_only` policies.
- Measurement result: opening two throwables usually loses value to action cost.
  Finisher-only use modestly outperforms no-item runs. This is evidence about
  timing, not a balance verdict or approval to change item values.
- `--tactical-strategy` is the current fixed-seed, stdout-only comparison for
  no throwable, existing throwable, and tactical throwable policies. Cleric
  Sanctified Erosion is clearly positive against both comparison groups;
  Warrior Rending Wound's fixed first-turn policy is currently negative because
  it disrupts the Physical Charge rhythm; Rogue gains limited Fire-region value
  but does not yet outperform the existing armor-piercing throwable overall.
  Mage correctly remains `not_applicable`.
- The tactical harness records live Cleric DoT state keys and paired five-turn
  damage, HP, and MP deltas. Its report verifies 300-record coverage, pairing,
  CSV/JSON parity, reproducibility, and global data/RNG non-mutation.
- The support-window probes show the Cinder 50% adjustment is the minimum
  single-field correction that makes Ice/Earth/Thunder three-turn output
  repay positively; Final has no matching core-element Cinder scenario.

## Next Boundary

No further gameplay implementation is pre-approved. The completed support-book
measurement, deterministic equipment audit, role-aware Boss diagnostics, and
narrow monster tuning must not imply approval for job growth, formal promotion,
affix/save work, special-slot expansion, elemental infusion, GUI, or further
combat changes. Start any future exact slice with a read-only planning gate.

The next planning direction is to turn the existing role, promotion-preview,
equipment-affix, and monster data into one implementable progression-and-balance
chain: settle the current uncommitted gameplay baseline, define a minimal formal
promotion contract, then adjust player and monster values with deterministic
measurement. Do not restart five-region content planning.

## Minimum Read List

1. `AGENTS.md`
2. `01_content/agent-startup-reading-list.md`
3. `.codex/skills/element-maze-session-ops/SKILL.md`
4. `README.md`
5. this file
6. `01_content/world-content-skeleton-v0.1.md`
7. `01_content/combat-progression-design-v1.md`
8. `01_content/combat-items-affixes-construction-plan-v1.md`

For the next planning gate also inspect the live combat/item surfaces named by
the plan. Never manually read or edit `save.json`.
