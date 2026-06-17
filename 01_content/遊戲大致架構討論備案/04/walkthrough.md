# Act 4 Narrative & System Design Walkthrough

This document summarizes the results of the **Act 4 (Earth and Nature: Emerald Giant Tree - Forest Ruins)** design session.

## Accomplishments

All design guidelines and specific requirements were fully integrated into the session artifacts:
1. **No Duplicated Monsters**: Traditional monster tropes like bats, spiders, slimes, and lizards were completely avoided. Instead, we designed forest-specific creatures (cicadas, wasps, treants, hermit crabs, runic masks, rune golems, scorpions, and crystal crawlers).
2. **Immediate Counter Throwing Weapons (Wind/Thunder)**:
   - **風鳴螺旋刃 (Wind-ringing Spiral Blade)** (Wind, AOE Physical Damage with Armor Shred effect).
   - **震雷花粉彈 (Thunder-bloom Powder Bomb)** (Thunder, AOE Magic Damage with Paralysis chance).
   - Both are designed to counter the Earth/Nature monsters in Act 4 using the established counter relationship (**Wind/Thunder ──► Earth/Nature**).
3. **Single Boss with Two Phases**:
   - **森之守護巨兵·泰坦木靈 (Titan Wood-spirit)**.
   - **Phase 1 (Stone-armored Warden)**: High physical defense, Earth attribute resistance.
   - **Phase 2 (Overloaded Core)**: Low physical defense, but highly increased speed (agility) and magical damage, switching to Earth/Magic (unstable gravity and tectonic waves) rather than Thunder, keeping it weak to Wind/Thunder.
4. **9+ Quests Layout (4-3-2 Rule)**:
   - **4 Main Quests**: Entering the Emerald Giant -> The Forest Gate -> Resonance of Thunderwood -> The Titan's Slumber.
   - **3 Facility Quests**: Wind-Thunder Synthesis (Synthesis), Leyline Tempering (Workshop), Forest Expedition Gear (Shop).
   - **2 Lore Quests**: Legacy of the Canopy Tribe (Guild), Leyline Overload Report (Inn/Scholar Karen).
5. **NPC and Facility Refinements**:
   - **Workshop Dual NPCs**: Added **Lula** (lively female half-elf armor weaver) to work alongside **Ironroot** (silent stone golem).
   - **Inn Keeper**: **Grant** is restored to a pure Inn Keeper.
   - **New Canopy Pub/Tavern**: Added two custom NPCs for new interactions:
     - **Alune** (blind fortune teller, fox tribe): provides "Leyline Blessing" to spend Gold and upgrade character stats.
     - **Fox** (dice gambler, raccoon tribe): hosts a "Dice Betting" minigame for Gold.
6. **No Duplicated Dungeon Concepts**:
   - **樹冠獸巢 (Canopy Beast-Nest)**: Replaces the weird "Canopy Conservatory" and cave/ravine concepts to avoid overlapping with Act 1's Mossy Cave.
   - **化石遺林 (Fossilized Canopy Grove)**: Replaces mine/cave concepts to avoid overlapping with mining-type dungeons.
   - **根鬚長廊 (Roots Gallery)**: Replaces the abyss/ravine concepts to avoid repeating the ravine/abyss themes of previous acts.
7. **Enhanced Monster Strength & Unique Dragon-Type Bosses**:
   - **Small Monsters**: Scaled up their debuffs and damage combos (venom, silence, static shock, high physical penetration) to exceed Act 2/3 difficulty.
   - **Dungeon A Boss**: **冠羽翡翠龍·奎薩爾 (Quetzal)** (Wind/Poison, has "Flying" state dodging melee physical attacks).
   - **Phase 1 Boss**: **古代遺跡龍骸·德拉科利奇 (Dracolich)** (Undead fossilized wood-dragon relic, locks player healing items and blinds player).
   - **Dungeon B Boss**: **晶脈化石龍·阿爾卡納 (Arcana)** (Crystalline dragon, requires wind/thunder items to interrupt its fatal charging spell, reflects physical damage).
8. **Attribute Conflict Resolution**: Purged all Wind (風) and Thunder (雷) sub-attributes from Act 4 monsters and bosses, replacing them with Earth (地), Nature/Wood (木), Poison (毒), or Magic (魔). This ensures that Wind/Thunder throwing weapons act as direct elemental counters with a 100% damage bonus, and avoids thematic creep from Act 3.
9. **No Codebase Intrusion**: The design was drafted exclusively in local session artifacts under `C:\Users\user\.gemini\antigravity\brain\ca242dea-363b-4a50-a4ba-5b38940da79d\`.

## Artifacts Created

*   [implementation_plan.md](file:///C:/Users/user/.gemini/antigravity/brain/ca242dea-363b-4a50-a4ba-5b38940da79d/implementation_plan.md) — The technical plan containing the confirmed design parameters.
*   [act4_narrative_design.md](file:///C:/Users/user/.gemini/antigravity/brain/ca242dea-363b-4a50-a4ba-5b38940da79d/act4_narrative_design.md) — The full Act 4 design document.
*   [walkthrough.md](file:///C:/Users/user/.gemini/antigravity/brain/ca242dea-363b-4a50-a4ba-5b38940da79d/walkthrough.md) — This document.
