# Act 5 Narrative & System Design Proposal (World Leylines Core / Final Chapter)

This plan outlines the design of **Act 5: Final Chapter (Ultimate Dungeon - Core of World Leylines / World Maze)**.
The proposal includes the final state of Elm Town (featuring the Arena with 20 contenders and the Nameless King champion), Tier-3 Class Specializations with corresponding class-specific ultimate weapons, a 3-stage main final dungeon, a 3-phase final Boss, and ultimate battle items.

## User Review Required

> [!IMPORTANT]
> - All proposed changes are strictly **read-only** in this session and will not modify any files in the project repository `C:\Users\user\OneDrive\文字冒險遊戲`.
> - The detailed design is saved in the session-local artifact `act5_narrative_design.md` once this plan is approved.
> - This plan establishes the narrative guidelines, battle rules, and final game closure before any future runtime implementation.

## Design Decisions (Confirmed & Updated)

1. **小鎮新增設施「競技場 (Arena)」**：
   - 增加戰前熱身與挑戰，NPC 為「大劍雷格 (Regg the Greatsword)」。
   - **新增 20 名選手天梯名冊**，分為青銅、白銀、黃金、白金四個梯隊與最終冠軍。
   - 最終第 1 名為**「戰神化身·無名王者」**，具有大劍與符文法術姿態切換。
   - **冠軍獎勵**：擊敗無名王者後重鑄獎盃，獲得主角當前三階職業特化的**唯一神降專屬神兵**（共 8 把，如劍聖的「無極天刃·萬華鏡」、影刺客的「幽影深淵雙刃」等）。

2. **第三階轉職 (Tier-3 Class Specialization)**：
   - 轉職限制為達到 Lv 30 且通過競技場試煉，並在教堂消耗 3x 神諭星砂。
   - 四大初始職業均有雙特化分歧，並引入終極奧義技能以抗衡 Boss 滅世傷害。

3. **終焉地城三階段 (3-Stage Dungeon)**：
   - 終焉迷宮細分為三階段：混沌碎裂長廊（火/冰）、元素湮滅裂隙（雷/地）與萬宿源流核心（魔/混沌）。

4. **最終 Boss 三階段 (3-Phase Boss)**：
   - **Phase 1 (萬宿吸聚形態)**：元素屏障輪轉弱點機制。
   - **Phase 2 (星能爆發形態)**：複合雙元素屬性與重力防禦削弱。
   - **Phase 3 (崩解奇點形態)**：防禦降 50%、敏捷提 150%、5回合奇點湮滅致命傷害倒計時。

## Proposed Changes

No changes will be made to the project repository.
The following session-local design documents are created/modified in this session:
*   #### [MODIFY] [act5_narrative_design.md](file:///C:/Users/user/.gemini/antigravity/brain/5af09798-de92-4c76-8541-15d09f8b4339/act5_narrative_design.md)
*   #### [MODIFY] [implementation_plan.md](file:///C:/Users/user/.gemini/antigravity/brain/5af09798-de92-4c76-8541-15d09f8b4339/implementation_plan.md)

## Verification Plan

### Manual Verification
- Review the updated design document for consistency with `README.md` and `full-act-structure.md` constraints.
- Verify that the Arena 20-contender progression, champion reward system, Tier-3 Class Specializations, 3-stage Main Dungeon, and 3-phase final Boss mechanics fit the 1v1 combat engine.
- Verify that all elements are integrated and balanced across the three stages and boss phases.
