# Agent Startup Reading List - Text-RPG-Codex-Demo

為了降低新 Session 的 Token 膨脹壓力，防止 Agent 讀入過多歷史文件而導致上下文認知混亂（Drift），特制定此 Agent 啟動讀取清單。
後續所有在新 Session 中啟動的 Agent，在未獲得使用者特別指示前，**必須嚴格遵循本載入規則，嚴禁進行全專案目錄檔案掃描或主動加載冷區檔案**。

---

## 1. 文件載入分區規則 (Loading Zones)

### 🔴 Hot Zone (新 Session 啟動必讀 - 核心治理與進度)
*每次新對話/Session 開始時，Agent 必須主動加載且僅加載以下 5 個核心文件，以快速對齊專案現況與治理邊界：*

1. [README.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/README.md)
   - *用途*：確認專案結構、啟動方式、SSOT 規則與最新進度摘要。
2. [01_content/codex-handoff-short.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/codex-handoff-short.md)
   - *用途*：確認最新穩定狀態、已完成的 MVP 項目與下一步清晰的施工邊界。
3. [01_content/gui-html-static-prototype-progress-v1.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/gui-html-static-prototype-progress-v1.md)
   - *用途*：確認當前 GUI HTML 原型的最新進度、已定案設施畫面與驗證紀錄。
4. 專案內目前有效的 `SKILL.md`
   - Codex：`.codex/skills/element-maze-session-ops/SKILL.md`
   - Antigravity：`.antigravity/skills/element-maze-session-governance/SKILL.md`
   - *用途*：依目前 agent 工具環境載入專案本機專屬的協作與治理規範、指令匯報格式與嚴格禁止事項；不要把 Codex / Antigravity skill 混用成同一份狀態來源。
5. [01_content/agent-startup-reading-list.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/agent-startup-reading-list.md) *(本檔案)*
   - *用途*：本載入指南，用於約束載入範圍。

---

### 🟡 Task Zone (依任務選讀 - 特定開發任務加載)
*僅在進行與該主題相關的開發或規劃任務時，才允許依需讀取，平常啟動時不主動讀取：*

* **GUI 目標與架構關聯任務**：
  - [gui-planning-index.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/gui-planning-index.md) (GUI 規劃總索引)
  - [ui-flow-blueprint.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/ui-flow-blueprint.md) (UI 流程藍圖)
  - [gui-screen-map.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/gui-screen-map.md) (GUI 畫面地圖)
* **具體畫面實作與調整任務**：
  - 僅加載對應設施的 HTML/CSS/JS 代碼，例如當前在處理 Workshop 任務時，只讀取 `07_gui_prototype/workshop_screen/` 下的檔案。

---

### 🔵 Cold Zone (降權不讀 - 歷史願景大文件)
*以下為歷史大文件、系統規劃書、或是已定案的長期願景文件。**除非使用者在對話中特別指名要求讀取，否則啟動時一律降權、不主動加載**以節省 Context 空間：*

- [act-2-content-plan.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/act-2-content-plan.md) (第二幕內容規劃)
- [full-act-structure.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/full-act-structure.md) (全幕次結構規劃)
- [game-architecture.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/game-architecture.md) (遊戲架構)
- [game-design.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/game-design.md) (遊戲設計)
- [combat-growth-layering-plan.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/combat-growth-layering-plan.md) (戰鬥與成長分層規劃)
- [codex-session-snapshot.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/codex-session-snapshot.md) (歷史對話 Snapshot 紀錄)
- [demo-playtest-notes.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/demo-playtest-notes.md) (遊玩測試回饋與待優化筆記)
- [gui-implementation-platform-tradeoff.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/gui-implementation-platform-tradeoff.md) (GUI 實作平台技術評估取捨)

---

## 2. Archive Candidates (已定案設施的歷史草案歸檔候選)

下列 **23 個檔案** 屬於早期設計、線框圖草案、評審檢核表或 Prompt 草擬文件。由於 Town Hub、Guild、Synthesis 等設施的靜態原型已定案並進入穩定階段，**這些文件均已失去時效性，標記為未來可移入 archive 目錄的歸檔候選**。

> [!NOTE]
> 治理政策：為了避免檔案遺失或路徑中斷，本階段**嚴禁在硬碟上進行實體搬移或刪除檔案動作**，僅在文件中進行邏輯分類標記，待未來啟動正式文件整理輪時一次性處理。

> [!NOTE]
> 若 Hot Zone 文件與最新 commit 或現有目錄狀態出現落差，新 Session 應先回報 drift 風險，並以 read-only 方式確認差異；不得直接讀取 Cold Zone 大文件來「補歷史」。

1. [gui-asset-registry-draft.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/gui-asset-registry-draft.md)
2. [gui-asset-request-schema.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/gui-asset-request-schema.md)
3. [gui-facility-screen-template.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/gui-facility-screen-template.md)
4. [gui-facility-synthesis-mockup-request.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/gui-facility-synthesis-mockup-request.md)
5. [gui-facility-synthesis-prompt-draft.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/gui-facility-synthesis-prompt-draft.md)
6. [gui-facility-synthesis-v2-prompt-draft.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/gui-facility-synthesis-v2-prompt-draft.md)
7. [gui-guild-screen-model-draft.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/gui-guild-screen-model-draft.md)
8. [gui-guild-screen-review-checklist.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/gui-guild-screen-review-checklist.md)
9. [gui-guild-screen-visual-baseline.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/gui-guild-screen-visual-baseline.md)
10. [gui-html-town-hub-fixture-spec.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/gui-html-town-hub-fixture-spec.md)
11. [gui-html-town-hub-prototype-plan.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/gui-html-town-hub-prototype-plan.md)
12. [gui-town-hub-facility-node-mapping-v1.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/gui-town-hub-facility-node-mapping-v1.md)
13. [gui-town-hub-mockup-review-v1.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/gui-town-hub-mockup-review-v1.md)
14. [gui-town-hub-programmatic-layout-plan-v1.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/gui-town-hub-programmatic-layout-plan-v1.md)
15. [gui-town-hub-review-checklist.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/gui-town-hub-review-checklist.md)
16. [gui-town-hub-screen-model-draft.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/gui-town-hub-screen-model-draft.md)
17. [gui-town-hub-ui2-wireframe-draft.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/gui-town-hub-ui2-wireframe-draft.md)
18. [gui-town-hub-ui2-wireframe-review-v1.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/gui-town-hub-ui2-wireframe-review-v1.md)
19. [gui-town-hub-visual-mockup-candidate-review-v1.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/gui-town-hub-visual-mockup-candidate-review-v1.md)
20. [gui-town-hub-visual-mockup-prompt-draft.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/gui-town-hub-visual-mockup-prompt-draft.md)
21. [gui-town-hub-visual-mockup-prompt-review-v1.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/gui-town-hub-visual-mockup-prompt-review-v1.md)
22. [gui-town-hub-wireframe-plan.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/gui-town-hub-wireframe-plan.md)
23. [gui-ui-direction-brief.md](file:///c:/Users/user/OneDrive/文字冒險遊戲/01_content/gui-ui-direction-brief.md)
