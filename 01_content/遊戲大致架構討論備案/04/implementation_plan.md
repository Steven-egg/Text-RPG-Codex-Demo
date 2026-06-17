# Act 4 Narrative & System Design Proposal (Earth and Nature)

This plan outlines the design of **Act 4: Earth and Nature (Emerald Giant Tree - Forest Ruins)**.
The proposal includes the town visuals, the 9+ facility NPCs, the 3-dungeon structure, earth-themed monsters and bosses, and new throwing weapons specifically designed to help physical classes (Swordsman/Rogue) handle multiple enemies and counter specific attributes.

## User Review Required

> [!IMPORTANT]
> - All proposed changes are strictly **read-only** in this session and will not modify any files in the project repository `C:\Users\user\OneDrive\文字冒險遊戲`.
> - The detailed design will be saved in the session artifact `act4_narrative_design.md` once this plan is approved.
> - This plan establishes the narrative guidelines and battle items logic before any runtime implementation.

## Design Decisions (Confirmed & Corrected)

1. **屬性克制與道具屬性定位（選定方案 B，屬性修正）**：
   * 本章的群傷投擲道具屬性為 **「風/雷」** 屬性（風鳴螺旋刃、震雷花粉彈）。
   * 為了確保道具能完美克制本章的 **「地/自然」** 屬性魔物，並避免與 Act 3 的風雷主題重複，**本章的所有怪物與首領將被修正為純「地 (Earth)」、「自然/木 (Wood)」、「毒 (Poison)」或「魔 (Magic)」屬性，全面移除風、雷子屬性**。這樣風雷投擲物在戰鬥中才能發揮最大克制傷害。

2. **單首領兩階段機制（屬性修正）**：
   * 本章關底 Boss 為**單一首領（森之守護巨兵·泰坦木靈）**。
   * 第一階段為石甲守護形態（純地屬性）；第二階段為**地脈過載形態**（地/魔屬性，非雷屬性），因吸收過量地脈能量而狂暴，造成高額重力與地震魔法傷害，仍能被風雷道具克制。

3. **設施與 NPC 的結構性調整**：
   * **工坊 (Workshop)**：新增一位女性防具 NPC **「露拉 (Lula)」** 與石巨人 **「鐵根 (Ironroot)」** 共同看守工坊，形成雙人組。
   * **旅館 (Inn)**：**葛嵐特 (Grant)** 回歸純粹的旅館老闆人設，與學者 **凱倫 (Karen)** 均安置於此。
   * **森林酒館 (Canopy Pub/Tavern)**：新增占卜師 **「艾露恩 (Alune)」**（金幣升級屬性）與莊家 **「福克斯 (Fox)」**（骰子小遊戲）。

4. **地城名稱與概念重構（避開重複概念與古木溫室）**：
   * **次要地城 A**：**樹冠獸巢 (Canopy Beast-Nest)**（野生飛禽、巨獸築巢生態，採集樹汁與藤蔓）。
   * **主地城 階段 1**：**根鬚長廊 (Roots Gallery)**（盤根錯節的遺跡地下木質長廊，避開「深淵」字眼）。
   * **次要地城 B**：**化石遺林 (Fossilized Canopy Grove)**（因地脈結晶化而鈣化、石英化的空中巨枝森林，在此採集結晶砂與鋼木，避開「礦坑」字眼）。

5. **怪物強度提升與首領龍系/獨特生物化**：
   * **小怪設計**：技能干擾強度提升，但屬性嚴格限制在地、木、毒、魔。
   * **次要地城 A 首領**：**冠羽翡翠龍·奎薩爾 (Quetzal the Crown-crested Emerald Wyrm)**（地/毒屬性，擁有空中飛行閃避與劇毒孢子風暴機制）。
   * **主地城 階段 1 首領**：**古代遺跡龍骸·德拉科利奇 (Dracolich the Dendro-Wyrm Relic)**（地/魔屬性，古代巨龍的木質骸骨，具備死靈吐息與鎖死藥水、致盲等強力控制）。
   * **次要地城 B 首領**：**晶脈化石龍·阿爾卡納 (Arcana the Lithic Crystal-Drake)**（地/自然屬性，地脈結晶化的石質巨龍，擁有大招蓄力與晶刺反射，需使用風雷投擲物打斷其蓄力）。

## Proposed Changes

No changes to the project repository.
The following session-local design documents will be created/modified:
*   [MODIFY] [act4_narrative_design.md](file:///C:/Users/user/.gemini/antigravity/brain/ca242dea-363b-4a50-a4ba-5b38940da79d/act4_narrative_design.md)
*   [MODIFY] [implementation_plan.md](file:///C:/Users/user/.gemini/antigravity/brain/ca242dea-363b-4a50-a4ba-5b38940da79d/implementation_plan.md)

## Verification Plan

### Manual Verification
- Review the design document for consistency with `narrative_codex.md` constraints.
- Verify that the town facilities (including the new Tavern) and 3 dungeons rules are followed.
- Check that the throwing weapons address the physical classes' combat balance against multiple enemies.
- Verify the 2-phase boss logic fits the 1v1 engine constraint.
- Ensure the terms "洞窟" (cave), "礦坑" (mine), and "裂谷/深淵" (ravine/rift/abyss) are not used for Act 4's new locations.
- Verify that normal monster designs show higher mechanics and bosses are unique dragon-type or fossil dragon beasts.
- Confirm all monsters and bosses in Act 4 do not contain Wind or Thunder sub-attributes, ensuring Wind/Thunder throwables have a 100% counter damage bonus.
