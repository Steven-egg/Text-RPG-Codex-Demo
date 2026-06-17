# Act 3 Narrative & System Design Proposal (Wind and Thunder)

This plan outlines the design of **Act 3: Wind and Thunder (Eagle's Nest Fortress - Floating Islands)**.
The proposal includes the town visuals, the 9 facility NPCs, the 3-dungeon structure, storm-themed monsters and bosses, and new throwing weapons specifically designed to help physical classes (Swordsman/Rogue) handle multiple enemies.

## User Review Required

> [!IMPORTANT]
> - All proposed changes are strictly **read-only** in this session and will not modify any files in the project repository `C:\Users\user\OneDrive\文字冒險遊戲`.
> - The detailed design is saved in the session artifact [act3_narrative_design.md](file:///C:/Users/user/.gemini/antigravity/brain/c4821b38-b2e7-4cec-b255-6144be0dab0f/act3_narrative_design.md).
> - This plan establishes the narrative guidelines and battle items logic before any runtime implementation.

## Design Decisions (Resolved)

1. **投擲性輔助道具機制（簡單粗暴群體傷害）**：採用**群體傷害性一次性消耗道具**定位。與前期的降防輔助道具（如破甲鏢捆）互補：
   * **飛空雷鳴彈**：造成高額群體雷屬性魔法傷害。
   * **碎裂風暴匣**：造成高額群體風屬性物理傷害。
2. **雙首領 (Vane & Bolt) 戰鬥機制**：為符合目前 CLI 引擎僅支援 1v1 戰鬥的限制，將雙衛包裝為**單一戰鬥對象怪物 (ID: `boss_vane_and_bolt`)，共享血條與戰鬥面板**。
   * 戰鬥中以「風、雷姿態切換與協同描述」展現雙首領特質。
3. **高空特色怪物 roster 調整**：全面移除了重複且低威脅感的蜘蛛、蝙蝠、史萊姆、蜥蜴與普通甲蟲，改為：
   * **嘯風石窟**：幼風飛龍（龍類）、風切掠隼（禽類）、雲海漂浮鰩（浮游鰩魚）、狂風精靈。
   * **嵐雷天主堂**：雲海嵐狼（狼類）、雷霆元素、迅雷刃豹（豹類）、始源風護衛等。
   * **墜落雷脈**：導能雷豹、雷光穿山獸、雷晶天牛（極具科技與紫色雷晶風格的甲蟲）。
4. **9 大任務配置與掉落對照表 (4-3-2 法則)**：
   * **主線任務 x 4**：修復滑索 -> 擊敗艾瑞克拿圖紙 -> 收集雷脈礦石製成避雷針突破大門雷暴 -> 擊敗雙衛回收風雷印記。
   * **設施鎖定任務 x 3**：解鎖新群傷投擲武器合成（合成屋）、開放裝備強化 +3 階段（工坊）、販售高空禦風/避雷防具（商店）。
   * **世界觀支線 x 2**：失落空騎兵的墓碑（雷德菲爾）、導師艾爾德林的高空日誌（凱倫）。
   * **掉落素材對照表**：細化 8 種空域與雷脈專屬素材的獲取途徑與強化/合成用途。

## Proposed Changes

No changes to the project repository.
The following session-local design document is created:
*   [MODIFY] [act3_narrative_design.md](file:///C:/Users/user/.gemini/antigravity/brain/c4821b38-b2e7-4cec-b255-6144be0dab0f/act3_narrative_design.md)

## Verification Plan

### Manual Verification
- Review the design document for consistency with `narrative_codex.md` constraints.
- Verify that the 9 town facilities and 3 dungeons rules are followed.
- Check that the throwing weapons address the physical classes' combat balance against multiple enemies.
