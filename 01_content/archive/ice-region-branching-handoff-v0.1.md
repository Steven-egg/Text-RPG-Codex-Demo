# Ice Region Branching Handoff v0.1

Purpose: record the current Ice region planning checkpoint and prepare two
separate next-session routes: one for placeholder image generation, and one for
quest / CLI expansion planning. This is a Task Zone handoff. It does not approve
runtime, data, schema, save, combat, GUI static prototype, bridge, or formal
asset-pipeline implementation.

## Current Checkpoint

- Latest actual git checkpoint observed during this handoff:
  `703ff24 2026-06-19 [codex] docs(content): add collaboration and NPC display baselines`.
- `README.md` and `01_content/codex-handoff-short.md` may still mention the
  older `5c0dfad` checkpoint. Treat current git as authoritative.
- Worktree was clean before this docs handoff file was created.
- Antigravity is no longer the default generator for regional expansion content.
  Current preferred flow is owner + Codex planning first, with Antigravity kept
  as optional support for later naming or wording variants.
- `regional_dungeon_image_spine` is accepted as a chat-level v0 baseline:
  Ice / Earth / Thunder / Final each have two minor dungeon slots and one
  two-phase main dungeon slot.
- `ice_content_spine` exists as a chat-level v0 candidate only. It needs a
  clean v1 pass before image generation.

## Ice Spine Clean v1 Decisions

Keep:

- Ice is a frost-tide coast / cold sea / fog harbor / broken ice region.
- Ice's core content conflict is a seal anomaly, handled only as narrative and
  planning placeholder.
- Ice uses one presentation hub, two minor dungeon slots, one two-phase main
  dungeon, five Guild quest slots, and nine reused facility families.
- Guild quest slots stay at narrative-purpose level only.
- Facility content stays at lightweight function / atmosphere level only.

Remove or avoid:

- Do not put a distant lighthouse silhouette in the Ice town hub image brief.
  It pulls the composition into a far landscape and can shrink facility
  buildings.
- Do not use far landmark focal points in town hub generation prompts.
- Do not make the town hub a scenic vista. Facility entrances must remain large,
  readable, and useful for future overlay / interaction planning.
- Do not create NPC names, quest IDs, turn-ins, rewards, flags, unlock keys,
  item names, recipe names, material names, monster names, or formal dungeon
  names in the clean v1 pass.

Lighthouse handling:

- The salt-frost lighthouse may remain a world-map, lore, or dungeon-background
  motif later.
- It should not appear as a far focal point in the Ice town hub image brief.
- It is not a facility, dungeon, quest hook, runtime object, or new map system.

Seal / relic handling:

- Use the `regional-data-instantiation-plan-v0.1.md` separation:
  relic / seal as narrative concept, relic marker as later progression layer,
  and `relic_marker_source` as possible future proof / echo / core-remnant
  planning slot.
- For the Ice clean v1 pass, the seal is only a narrative placeholder.
- Do not define active effects, passive effects, stat bonuses, resistance
  bonuses, skill links, formal flags, unlock keys, source item names, or Boss
  drops.

## Branch A Prompt - Placeholder Image Route

```text
Work directory: C:\Users\User\OneDrive\文字冒險遊戲

請先遵守 AGENTS.md 與 Codex session ops。這是 Ice town hub placeholder image
candidate route，不是 runtime / data / schema / save / combat / bridge / formal
asset-pipeline task。

Minimum read:
1. AGENTS.md
2. 01_content/agent-startup-reading-list.md
3. .codex/skills/element-maze-session-ops/SKILL.md
4. README.md
5. 01_content/codex-handoff-short.md
6. 01_content/world-content-skeleton-v0.1.md
7. 01_content/ui-art-prep-brief-v0.1.md
8. 01_content/ice-region-branching-handoff-v0.1.md

Also inspect visual anchors from 07_gui_prototype before image work:
- 07_gui_prototype/town_hub/assets/town-hub-environment-v01.jpg
- 07_gui_prototype/world_map/assets/world-map-environment-v01.jpg
- relevant dungeon / facility assets only if needed for style continuity

Task:
1. Produce `ice_content_spine_clean_v1` in chat first, based on
   01_content/ice-region-branching-handoff-v0.1.md.
2. Produce an Ice town hub image brief that is friendly to image generation.
3. Generate only placeholder / candidate image output after the brief is clear.

Hard constraints:
- Do not edit repo files unless I explicitly approve the exact file path.
- Do not edit 07_gui_prototype.
- Do not start a formal asset pipeline.
- Do not create registry entries or final asset manifests.
- Do not touch runtime, data, schema, save, combat, GUI bridge, or JS.
- Do not include a distant lighthouse silhouette in the Ice town hub image.
- Do not include far landmark focal points that pull the camera away.
- Keep facility buildings large, readable, and similar in scale to the current
  demo town hub.
- All text, labels, icons, badges, resources, and UI chrome are future render
  layer concerns; do not bake readable UI text into the image.

Target style:
- Continue the existing stylized JRPG / Japanese-leaning 3D fantasy direction
  visible in 07_gui_prototype assets.
- The Ice hub should feel like a wet, cold harbor town with warm indoor light,
  snow-dusted roofs, fog, windbreaks, wet stone, and clear facility entrances.
- It should not become a distant landscape, hard-realistic western fantasy,
  flat cartoon, chibi, sci-fi, or a new gameplay map.

Output expected:
- `ice_content_spine_clean_v1`
- `ice_town_hub_image_brief_v1`
- one or more placeholder candidate images, if image generation is available
  and stays outside repo-tracked implementation surfaces
```

## Branch B Prompt - Quest / CLI Expansion Planning Route

```text
Work directory: C:\Users\User\OneDrive\文字冒險遊戲

請先遵守 AGENTS.md 與 Codex session ops。這是 read-only / planning-first
quest and CLI expansion route。不要修改 runtime、data、schema、save、combat、
GUI、bridge、asset pipeline，也不要 stage/commit/push。

Minimum read:
1. AGENTS.md
2. 01_content/agent-startup-reading-list.md
3. .codex/skills/element-maze-session-ops/SKILL.md
4. README.md
5. 01_content/codex-handoff-short.md
6. 01_content/world-content-skeleton-v0.1.md
7. 01_content/regional-data-template-v0.1.md
8. 01_content/regional-data-instantiation-plan-v0.1.md
9. 01_content/ice-region-branching-handoff-v0.1.md

Read-only implementation context to inspect:
- 04_data/data/quests.py
- 04_data/data/dungeons.py
- 04_data/data/materials.py
- 04_data/data/monsters.py
- 04_data/data/registry.py
- 03_engine/engine/game.py targeted sections for quest_unlocked, quest_ready,
  guild hints, boss/story-specific quest logic
- 03_engine/engine/gui_guild_model.py targeted sections if GUI quest model
  implications matter
- 06_tools/validate_data.py quest, dungeon, monster, item/material, and unlock
  validation checks

Task:
Discuss and plan how future Ice Guild quest content should expand from the demo
without pretending a reusable quest pipeline already exists.

Starting facts:
- Existing Fire/demo quests are not fully generic. Data lives in QUESTS, but
  unlock flow, story hints, Boss investigation, Act 2 handoff, and validation
  include Fire/demo-specific logic.
- Ice quest work must start as a read-only planning gate.
- Ice quest slots should remain narrative-purpose level until a reusable
  runtime/data approach is approved.
- Current preferred Ice quest spine:
  Q1 outer coast scout, Q2 local anomaly check, Q3 main route confirmation,
  Q4 deep seal resolution placeholder, Q5 return / handoff.

Questions to answer:
- Which parts of the demo quest flow can be reused as data pattern?
- Which parts are hard-coded or Fire/demo-specific?
- What is the smallest safe reusable quest pipeline slice?
- Which files would likely be touched later, if implementation is approved?
- What validation and smoke checks would be required?
- How should Ice quest slots avoid early completion and avoid common-material
  turn-in hazards?
- How should seal / relic marker placeholders stay separate from quest rewards,
  Boss drops, item drops, and unlock keys?

Do not implement. End with a read-only planning gate containing proposed slice,
likely files, forbidden adjacent systems, validation plan, and open decisions.
```

## Shared Branch Boundaries

- Do not read or write `save.json`.
- Do not modify runtime, data, schema, save, combat, GUI, bridge, or asset
  pipeline without a later exact-scope approval.
- Do not stage, commit, push, create branches, or archive files unless the owner
  explicitly asks.
- Do not treat candidate images, mockups, or HTML fixtures as gameplay SSOT.
- Do not let Ice planning define relic effects, stat bonuses, resistance
  bonuses, skill links, formal flags, unlock keys, or source item names.

