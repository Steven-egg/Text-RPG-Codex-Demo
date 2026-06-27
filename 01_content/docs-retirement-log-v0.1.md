# 01_content 文檔退役與物理存檔審計日誌 v0.1

本文件記錄了為減少 `01_content/` 目錄中的認知負擔與歷史規劃噪聲，所執行的全面「物理規檔（Physical Archiving）」審計。此操作將所有非當前專注核心的歷史文檔與設計稿，物理移至 `01_content/archive/` 子目錄中。

> [!IMPORTANT]
> - 本誌所列檔案均已物理搬移至 `archive/` 目錄。
> - 所有搬移的檔案皆已在 Git 歷史中安全記錄，未來若需檢索或還原，可隨時透過 Git 歷史找回。
> - 本誌不包含 `01_content/blueprints/` 內之活躍藍圖與規約檔案（藍圖並非退役檔案，僅作非侵入性分類隔離）。

---

## 物理存檔清單與審計分類

以下為搬移至 `archive/` 目錄的 41 個檔案之完整審計資訊，按文檔類型分組呈報：

### 1. 舊世界/地圖設計與交接文檔 (World / Map / Handoff Docs)

| 歸檔檔案路徑 (Archived Path) | 生命週期狀態 (Status) | 歸檔原因 (Reason) | 當前替代 SSOT / 活躍路徑 | 刪除安全說明 (Deletion Safety) | Git 歷史註記 |
|---|---|---|---|---|---|
| `archive/act-2-content-plan.md` | superseded | 早期 Act 2 火區 demo 的詳細執行規劃，其關卡與劇情邏輯已完全融入 Python 代碼。 | `world-content-skeleton-v0.1.md` | owner 同意後可安全物理刪除 | 歷史版本可隨時從 git 還原 |
| `archive/earth-world-map-brief-v0.1.md` | superseded | Earth 區世界地圖規劃細節已大致沉澱於數據和宏觀骨架，且其地圖相關的視覺資產請求將直接列入未來的 Earth 區資產清冊。 | `world-content-skeleton-v0.1.md` 及正式的資產清冊表 | 待資產清冊架構穩定後可物理刪除 | 歷史版本可隨時從 git 還原 |
| `archive/thunder-world-map-brief-v0.1.md` | superseded | Thunder 區世界地圖規劃細節已移至宏觀骨架，後續應併入相應的資產清單。 | `world-content-skeleton-v0.1.md` | owner 同意後可安全物理刪除 | 歷史版本可隨時從 git 還原 |
| `archive/final-world-map-brief-v0.1.md` | superseded | Final 終極區域世界地圖規劃細節已移至宏觀骨架，後續應併入相應的資產清單。 | `world-content-skeleton-v0.1.md` | owner 同意後可安全物理刪除 | 歷史版本可隨時從 git 還原 |
| `archive/ice-playable-skeleton-handoff-v0.1.md` | historical | 記錄 Ice 區 v0.1 CLI 骨架完成時的交接文檔，該功能目前已完整合併入 main 分支，相關的實作內容與測試數據皆已沉澱為代碼。 | `README.md` (capsule 狀態說明) 與實作代碼 | owner 同意後可安全物理刪除 | 歷史版本可隨時從 git 還原 |
| `archive/ice-region-branching-handoff-v0.1.md` | historical | Ice v0.1 分支開發時的對接說明，記錄了臨時的分支選擇和生成提示，現已完全無用。 | 無（階段任務已結束） | owner 同意後可安全物理刪除 | 歷史版本可隨時從 git 還原 |
| `archive/ui-art-prep-brief-v0.1.md` | superseded | 舊的 UI 美術準備簡報，其視覺基調與資產類別規劃已整合併入正式的資產生產清冊。 | `asset-production-inventory-v0.1.md` | 待資產清冊創建並確認後可物理刪除 | 歷史版本可隨時從 git 還原 |
| `archive/antigravity-candidate-content-brief-v0.1.md` | retired | 該文件規範了 Antigravity 產出候選名稱與文本的格式包，但現行區域內容多已直接於數據層成形，此指引過於冗長且流於純設計層，容易造成概念雜訊。 | `world-content-skeleton-v0.1.md` 及代碼 | owner 同意後可安全物理刪除 | 歷史版本可隨時從 git 還原 |

---

### 2. 舊系統與協作歷史文檔 (System / Collaboration / Historical Background)

| 歸檔檔案路徑 (Archived Path) | 生命週期狀態 (Status) | 歸檔原因 (Reason) | 當前替代 SSOT / 活躍路徑 | 刪除安全說明 (Deletion Safety) | Git 歷史註記 |
|---|---|---|---|---|---|
| `archive/codex-antigravity-collaboration-workflow-v0.1.md` | retired | 舊版的 AI 協作工作流規範，其核心控制和防漂移原則已融入 `AGENTS.md`。 | `AGENTS.md` (session 路由規則) | owner 同意後可安全物理刪除 | 歷史版本可隨時從 git 還原 |
| `archive/codex-session-snapshot.md` | retired | 早期代碼整合階段的會話快照日誌，已被最新的 `task.md` 與交接文檔取代，屬於歷史殘留。 | `task.md` 與 `codex-handoff-short.md` | owner 同意後可安全物理刪除 | 歷史版本可隨時從 git 還原 |
| `archive/combat-growth-layering-plan.md` | conditional historical | 戰鬥數值成長與階層化規劃。目前雖無運行時實作，但其內含的設計思路未來可能有參考價值，因此物理存檔以供日後備查。 | `world-content-baselines-v0.1.md` (部分宏觀層面) | 建議保留於 archive 中作歷史參考 | 歷史版本可隨時從 git 還原 |
| `archive/demo-playtest-notes.md` | historical | 火區 demo 的舊測試反饋記錄，相關問題已在代碼與數據層中修復。 | 無（問題已解決） | owner 同意後可安全物理刪除 | 歷史版本可隨時從 git 還原 |
| `archive/facility-npc-display-baseline-v0.1.md` | superseded | 舊的設施與 NPC 顯示基準，相關的資料對應與顯示邏輯已被運行時數據覆蓋。 | `04_data/data/display_names.py` | owner 同意後可安全物理刪除 | 歷史版本可隨時從 git 還原 |
| `archive/game-architecture.md` | historical | 舊版遊戲架構設計背景文檔，屬於早期技術預研，目前的架構已沉澱在 `03_engine/` 中。 | `README.md` 中的項目結構說明 | 建議保留於 archive 中作歷史參考 | 歷史版本可隨時從 git 還原 |
| `archive/gui-implementation-platform-tradeoff.md` | historical | 平台方案評估與折衷背景文件（Pygame / HTML 選擇分析），不影響當前靜態原型開發。 | 無（已定案使用 HTML/CSS 靜態原型） | 建議保留於 archive 中作歷史參考 | 歷史版本可隨時從 git 還原 |
| `archive/gui-post-bridge-roadmap-v0.5.md` | retired | 舊的網橋開發路線圖，多數功能已在 integration/bridge 階段實現並進入 stable 狀態。 | `gui-runtime-bridge-plan-v1.md` | owner 同意後可安全物理刪除 | 歷史版本可隨時從 git 還原 |

---

### 3. 舊 GUI 介面規格與設計文檔 (GUI Mockups / Checklists / Wireframes - Town Hub Focus)

本組文檔為城鎮中心（Town Hub）開發過程中各個階段的 UI/UX 線框圖、排版計劃、視覺 Prompt 草案以及對應的審查清單。這些檔案已不再活躍修改，但當需要重新微調 `07_gui_prototype/town_hub/` 介面時，仍可作為非常有用的佈局與定位邏輯參考，故予以物理存檔。

| 歸檔檔案路徑 (Archived Path) | 生命週期狀態 (Status) | 歸檔原因 (Reason) | 當前替代 SSOT / 活躍路徑 | 刪除安全說明 (Deletion Safety) | Git 歷史註記 |
|---|---|---|---|---|---|
| `archive/gui-html-town-hub-fixture-spec.md` | historical | 早期 Town Hub 靜態夾具與 Mockup 的技術規格說明。 | `07_gui_prototype/town_hub/` 實作 | 建議保留於 archive 中作歷史參考 | 歷史版本可隨時從 git 還原 |
| `archive/gui-html-town-hub-prototype-plan.md` | historical | Town Hub 靜態原型的製作與流程串接計劃。 | `gui-html-static-prototype-progress-v1.md` | 建議保留於 archive 中作歷史參考 | 歷史版本可隨時從 git 還原 |
| `archive/gui-town-hub-facility-node-mapping-v1.md` | superseded | 舊版城鎮設施節點映射圖，相關的座標與節點配置已被 HTML 靜態原型所吸收。 | `07_gui_prototype/town_hub/` 實作 | owner 同意後可安全物理刪除 | 歷史版本可隨時從 git 還原 |
| `archive/gui-town-hub-mockup-review-v1.md` | historical | 第一代城鎮中心 Mockup 評審紀錄與調整要求。 | `gui-html-static-prototype-progress-v1.md` | owner 同意後可安全物理刪除 | 歷史版本可隨時從 git 還原 |
| `archive/gui-town-hub-programmatic-layout-plan-v1.md` | superseded | Town Hub 網格佈局與程序排版計劃，已被 Flex/Grid CSS 實作取代。 | `07_gui_prototype/town_hub/index.css` | owner 同意後可安全物理刪除 | 歷史版本可隨時從 git 還原 |
| `archive/gui-town-hub-review-checklist.md` | historical | Town Hub 介面整合與排版檢核清單。 | `gui-html-static-prototype-progress-v1.md` | owner 同意後可安全物理刪除 | 歷史版本可隨時從 git 還原 |
| `archive/gui-town-hub-screen-model-draft.md` | superseded | Town Hub ScreenModel 數據結構草稿，已融入運行時網橋模型。 | `03_engine/` 網橋與顯示模組 | owner 同意後可安全物理刪除 | 歷史版本可隨時從 git 還原 |
| `archive/gui-town-hub-ui2-wireframe-draft.md` | historical | Town Hub UI2.0 線框圖設計稿（含詳細版面規劃）。 | `07_gui_prototype/town_hub/` 實作 | 建議保留於 archive 中作歷史參考 | 歷史版本可隨時從 git 還原 |
| `archive/gui-town-hub-ui2-wireframe-review-v1.md` | historical | Town Hub UI2.0 線框圖評審與修改意見。 | `07_gui_prototype/town_hub/` 實作 | owner 同意後可安全物理刪除 | 歷史版本可隨時從 git 還原 |
| `archive/gui-town-hub-visual-mockup-candidate-review-v1.md` | historical | 舊版 Town Hub 視覺候選圖之評審意見。 | `07_gui_prototype/town_hub/assets/` | owner 同意後可安全物理刪除 | 歷史版本可隨時從 git 還原 |
| `archive/gui-town-hub-visual-mockup-prompt-draft.md` | superseded | 舊版 Town Hub AI 繪圖 Prompt 提示詞草稿。 | `asset-production-inventory-v0.1.md` (新 Prompt 清冊) | owner 同意後可安全物理刪除 | 歷史版本可隨時從 git 還原 |
| `archive/gui-town-hub-visual-mockup-prompt-review-v1.md` | historical | 舊版 Town Hub 繪圖 Prompt 的優化與微調評估。 | `asset-production-inventory-v0.1.md` (新 Prompt 清冊) | owner 同意後可安全物理刪除 | 歷史版本可隨時從 git 還原 |
| `archive/gui-town-hub-wireframe-plan.md` | historical | Town Hub 早期線框圖排版構思與佈局草案。 | `07_gui_prototype/town_hub/` 實作 | 建議保留於 archive 中作歷史參考 | 歷史版本可隨時從 git 還原 |

---

### 4. 舊 GUI 介面規格與設計文檔 (GUI Mockups / Checklists / Wireframes - Other Facilities Focus)

本組文檔為公會（Guild）、煉金（Synthesis）、商店（Shop）、道具管理等其他核心設施介面在原型製作階段的草稿、技術模板或檢核表。物理搬移至 `archive/` 可排除核心文件干擾，同時在修改這些畫面時仍保留技術回溯價值。

| 歸檔檔案路徑 (Archived Path) | 生命週期狀態 (Status) | 歸檔原因 (Reason) | 當前替代 SSOT / 活躍路徑 | 刪除安全說明 (Deletion Safety) | Git 歷史註記 |
|---|---|---|---|---|---|
| `archive/gui-facility-screen-template.md` | historical | 設施畫面的 ScreenModel 與 UIAction 配置模板，技術參考用。 | `blueprints/gui-screen-map.md` | 建議保留於 archive 中作歷史參考 | 歷史版本可隨時從 git 還原 |
| `archive/gui-facility-synthesis-mockup-request.md` | historical | 煉金設施的視覺要求與控制項定義。 | `07_gui_prototype/synthesis/` 實作 | 建議保留於 archive 中作歷史參考 | 歷史版本可隨時從 git 還原 |
| `archive/gui-facility-synthesis-prompt-draft.md` | superseded | 早期煉金設施背景 AI 繪圖 Prompt。 | `asset-production-inventory-v0.1.md` (新 Prompt 清冊) | owner 同意後可安全物理刪除 | 歷史版本可隨時從 git 還原 |
| `archive/gui-facility-synthesis-v2-prompt-draft.md` | superseded | 煉金設施背景 AI 繪圖 Prompt 第二版優化稿。 | `asset-production-inventory-v0.1.md` (新 Prompt 清冊) | owner 同意後可安全物理刪除 | 歷史版本可隨時從 git 還原 |
| `archive/gui-guild-screen-model-draft.md` | superseded | 公會畫面的資料傳輸結構草案，目前已在網橋穩定運作。 | `03_engine/` 及公會網橋代碼 | owner 同意後可安全物理刪除 | 歷史版本可隨時從 git 還原 |
| `archive/gui-guild-screen-review-checklist.md` | historical | 公會介面（Guild Screen）細節審查與實作確認清冊。 | `gui-html-static-prototype-progress-v1.md` | owner 同意後可安全物理刪除 | 歷史版本可隨時從 git 還原 |
| `archive/gui-guild-screen-visual-baseline.md` | historical | 公會介面的初始排版與視覺標準線。 | `07_gui_prototype/guild/` 實作 | 建議保留於 archive 中作歷史參考 | 歷史版本可隨時從 git 還原 |
| `archive/gui-shop-mockup-brief-v0.1.md` | historical | 舊版商店 Mockup 與界面配置規劃。 | `07_gui_prototype/shop/` 實作 | 建議保留於 archive 中作歷史參考 | 歷史版本可隨時從 git 還原 |
| `archive/gui-shop-skinning-lab-readiness-checklist-v0.1.md` | historical | 商店皮膚探索實驗準備清單，相關實驗結果已被吸收。 | `07_gui_prototype/shop/` 實作 | owner 同意後可安全物理刪除 | 歷史版本可隨時從 git 還原 |
| `archive/gui-ui-direction-brief.md` | historical | 早期 GUI 視覺設計方向簡報，記錄了初始風格定調。 | `blueprints/gui-family-classification-visual-token-audit-v0.1.md` | 建議保留於 archive 中作歷史參考 | 歷史版本可隨時從 git 還原 |
| `archive/gui-asset-registry-draft.md` | superseded | 早期的 GUI 資產註冊表草稿。現已被正式資產清冊與運行時註冊表完全取代。 | `asset-production-inventory-v0.1.md` 及 `04_data/data/registry.py` | owner 同意後可安全物理刪除 | 歷史版本可隨時從 git 還原 |
| `archive/gui-asset-request-schema.md` | superseded | 舊的 GUI 資產請求結構規劃，定義了複雜的格式。在目前的輕量化開發下已無保留必要。 | `asset-production-inventory-v0.1.md` | owner 同意後可安全物理刪除 | 歷史版本可隨時從 git 還原 |

---

## 審計結論與後續步驟

1. **物理搬移完成**: 所有 41 個檔案均已搬移至 `archive/`，排除了根目錄的雜訊。
2. **安全歸檔原則**: 本日誌保證了每個檔案的去向與歷史價值皆有跡可循，在 owner 同意進行物理刪除前，暫時安全保留在 `archive/` 目錄中。
