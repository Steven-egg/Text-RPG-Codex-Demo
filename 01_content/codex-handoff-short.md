# Codex Handoff Short

Purpose: compact handoff for continuing Codex work. Read live files before
editing; this document identifies the current boundary, not gameplay SSOT.

## Current State

- Work directory: `C:\Users\user\OneDrive\文字冒險遊戲`
- Current committed checkpoint:
  `9a61eab 2026-07-15 [codex] feat(combat): complete progression and relic passive slices`.
- `main` is ahead of `origin/main` by one commit. Do not push without explicit
  owner approval.
- The working tree is intentionally uncommitted. Do not stage, commit, create
  a branch, push, or archive unless explicitly requested. LF-to-CRLF warnings
  are known and must not be cleaned up opportunistically.
- README was not synchronized in this combat pass; treat it as potentially
  stale and report any drift rather than updating it without approval.

## Landed Working-Tree Combat State

- The player physical-defense buff is single-pass: `get_stats()` owns the
  player-side modifier and enemy damage does not apply it again. The value-model
  audit checks Final Warrior baseline damage 43 and `defense_up` damage 15 with
  zero single-pass delta.
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

## Next Boundary

No further gameplay implementation is pre-approved. The next task is a
read-only combat-balance planning gate. Keep the following work separate:

1. Measure Quickstep, Cinder Mark, and Froststep over three-, six-, and
   ten-turn windows, including their action and MP break-even.
2. Audit deterministic regional equipment budgets by region, job, and slot;
   do not treat the B6 affix overlay as player-facing equipment rules.
3. Define four-job, milestone-level, region/Boss target bands and the missing
   enemy-survival-pressure measurements before tuning monster values.

Only after those gates should the owner consider narrow support-book changes,
equipment-data tuning, relic numeric tuning, or monster HP/attack/defense/
magic-defense/resistance/status tuning. Do not combine this core-balance work
with preview-only promotion/class-transfer or affix/save work.

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
