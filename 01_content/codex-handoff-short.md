# Codex Handoff Short

Purpose: compact continuation boundary. Read live files before editing; runtime
data remains the gameplay SSOT.

## Current State

- Work directory: `C:\Users\user\OneDrive\文字冒險遊戲`
- Latest commit: `b542039 wip: backup promotion, balance, quality, and GUI work`
- The worktree contains existing uncommitted WIP across engine, data, tools,
  Temple GUI, and a measurement document. Run `git status --short` first. Do
  not stage, commit, push, reset, archive, or overwrite WIP without explicit
  approval.
- The playable scope is sealed: five-region mainline, four core jobs, eight
  formal promotion routes, four elemental seals, Final Boss, and CLI authority.
  GUI has a static prototype and selected live bridge slices.
- Storage live GUI supports a 500G unlock and deposit/withdraw for 10 non-key
  item types. Capacity upgrades are not open.
- Monster race gameplay remains data-driven by `MONSTER_RACE_RULES` and the
  existing `game.*` consumers. The live combat ScreenModel now exposes the
  enemy race, trait, and readable one-shot state; the Combat Screen renders
  those fields while old static fixtures keep their existing fallback.
- Final S10 remains 200/200 victories across 40 job/scenario rows, with every
  Boss row inside 10--15 actions. The retained normal-row diagnostics are Fire
  Rogue 2/3/3, Ice Rogue 5/5/6, Thunder Rogue 6/6/6, Thunder Cleric 5/6/6,
  and Final Cleric 8/8/8; they do not reopen balance.

## Frozen Decisions

- Balance work is complete. Only a reproducible issue affecting normal
  completion or a job's play experience may trigger a minimal maintenance fix.
  Turns, consumables, quality comparisons, and damage ratios are diagnostic,
  not authorization to tune values.
- Warrior `growth_points.attack = 1.5` is intentional. Warrior totals 13.50
  points per level; Mage, Rogue, and Cleric total 15.00. Do not buff Warrior to
  satisfy the old uniform validator rule.
- `06_tools/validate_data.py`, `06_tools/test_job_growth_points.py`, and
  `01_content/proposed-job-growth-points-v1.md` use the per-job frozen totals.

## Maintainability State

- The handoff assumption that `dungeon.py` was only a future candidate was
  stale. Live code already has `03_engine/engine/dungeon.py`, and `game.py`
  re-exports its public helpers for GUI/tool compatibility.
- Keep `game.py` as CLI orchestrator. Do not remove re-exports, alter gameplay,
  or start `combat.py` extraction without a separate exact-scope approval.
- `dungeon.handle_defeat()` had a reproducible missing-import crash when a
  defeated run contained loot. The minimal import fix and focused regression
  are part of the current maintenance closure.
- Detailed domain inventory, state mutations, bridge dependencies, validation
  matrix, and remaining risks are in
  `01_content/maintenance-closure-v1.md`.

## Minimum Read List

1. `AGENTS.md`
2. `.codex/skills/element-maze-session-ops/SKILL.md`
3. `README.md`
4. this file
5. `01_content/maintenance-closure-v1.md`

For growth work, also read `01_content/proposed-job-growth-points-v1.md`,
`04_data/data/jobs.py`, and `06_tools/validate_data.py`. For GUI work, use the
GUI static prototype skill and live files for the exact screen.

## Next Boundary

No gameplay, balance, GUI bridge, storage-capacity, or engine-extraction slice
is pre-approved. After closure verification, stop and ask the owner whether any
separate hardening work is wanted; do not infer a new implementation round.
