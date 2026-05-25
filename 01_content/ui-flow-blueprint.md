# UI Flow Blueprint

狀態：第一版核心循環規格已落成 CLI thin display layer；Start Screen MVP、Travel Shop Catalog MVP、Workshop Catalog MVP、Magic Shop Catalog MVP、Synthesis Catalog MVP 與 Combat UI Log Separation MVP 已完成。GUI Phase UI-2 目前已改以 `07_gui_prototype/` 的 HTML static fixtures 驗證 screen layout、互動、navigation flow 與 UIAction logging。此文件記錄 UI 架構意圖；實際 runtime 狀態仍以 `README.md` 與 `03_engine/engine` 為準。

## 1. 規劃主軸

採用「流程節點藍圖」反推 UI。既有 CLI 版本的第一版流程為：

開始畫面 → 主選單 → 城鎮整備 → 迷宮選擇 → 迷宮探索 → 戰鬥 → 結算 / 回城

第一版目標不是建立 UI framework，也不是轉向 Unity / HTML UI，而是把既有 CLI 畫面整理成穩定的 panel 職責：

- 入口：品牌標題、存檔狀態與最小進入選項。
- 狀態：玩家或敵我目前狀況。
- 提示：下一步、風險、gate 或不可用原因。
- 行動：保留數字選單輸入。
- 結算：集中顯示收益、損失與解鎖方向。

未來 GUI-oriented flow 暫定拆成兩條：

- Flow A：Start Screen → World Map Screen → Town Hub Screen → Facility Screens。
- Flow B：Start Screen → World Map Screen → Exploration Screen → Combat Screen → Result → 回到 Exploration 或 World Map / Town。

World Map 是正式 UI 的中樞；Town Hub 與 Dungeon / Exploration 是從 World Map 進入的兩種目的地。CLI 目前的主選單可作為 UI-1 reference，但不應被視為最終主畫面架構。

## 2. UI 升級階段

三階段共用同一套 Screen Map、ScreenModel 與 UIAction；差異只在 render / presentation layer。

- Phase UI-1：Home Hub / Main Menu 文字式 UI。最接近目前 CLI panel 行為，用來整理 screen flow、UIAction、ScreenModel，不追求正式美術或素材風格。
- Phase UI-2：HTML static fixture prototype。用 fixture、HTML/CSS/JS render layer、靜態 navigation 與 UIAction logging 驗證 screen layout，不接 Python runtime、不讀寫 `save.json`、不建立正式 asset pipeline。
- Phase UI-3：最終 GUI 視覺版本。使用正式背景圖、角色圖、icon、UI skin，並需要 asset request schema、prompt builder、asset registry 與 style bible；此階段尚未開始。

CLI 數字輸入、Rich wireframe 選取、GUI 點擊與未來觸控都應映射到同一批 UIAction。不要把目前 `input()` / `print()` menu 直接視為最終架構。

## 3. 已落地畫面

- 主選單：顯示角色、HP/MP、金幣與下一步提示。
- 開始畫面：顯示遊戲標題與最小入口選項；有存檔時提供重新開始與載入進度，無存檔時直接開始新冒險。
- 角色狀態：拆成角色狀態、裝備、技能 panel。
- 城鎮整備：顯示角色資源、可交付任務、補給與設施用途。
- 迷宮選擇：顯示推薦等級、步數、屬性、通關狀態、等級判定與 Boss / gate 提示。
- 迷宮探索：每步顯示目前步數、HP/MP 與本趟收益。
- 戰鬥：主畫面每回合顯示回合數、玩家 HP/MP/狀態、敵人 HP/屬性/狀態、上一動短摘要與可用指令；完整動作過程集中到戰後 Battle Log。
- 結算 / 回城：探索完成、撤退、戰敗與戰鬥勝利都集中顯示結果摘要。
- 背包 / 裝備：背包顯示描述與用途線索；裝備管理顯示目前裝備並提供替換選單。
- 旅館：已有專屬 panel 與確認流程，可作為未來城鎮 NPC 畫面的模式參考。
- 城鎮設施：冒險者工會、工坊、商店、魔法書、合成與倉庫已開始比照旅館，使用專屬設施 panel。
- 旅人小鋪：已從共用購買清單改為專屬分類商店流程，顯示全部 / 補給品 / 戰術道具 / 飾品、持有數、價格、商品詳情與購買確認。
- 鐵刃 / 堅甲工坊：已從共用購買 / 強化入口改為專屬 catalog 流程，顯示購買、強化、我的裝備，並在詳情中呈現職業可用性、裝備狀態、基底裝備與素材狀態。
- 星燈魔法商店：已從單層魔法書清單改為專屬 catalog 流程，顯示全部 / 攻擊魔法 / 恢復魔法 / 輔助魔法 / 特殊魔法，並在詳情中呈現技能、MP、職業、等級、金幣與素材條件。
- 米菈合成屋：已從單層配方清單改為專屬 catalog 流程，顯示全部 / 裝備 / 戰術道具，並在詳情中呈現可製作狀態、產出、持有狀態、基底裝備、素材、最多可製作次數、金幣與合成確認。
- 倉庫：城鎮入口已簡化為純倉庫；背包 / 裝備留在主選單作角色整理用途。

## 4. 手動測試後調整

- 迷宮 Boss/gate 提示不再全部集中在提示區，改放在每個迷宮選項上，避免「無 Boss」與「可挑戰 Boss」同時像是同一座迷宮的提示。
- 葛倫已擊敗後會顯示已擊敗，不再顯示尚未滿足挑戰條件。
- 城鎮提示優先顯示主線 / 探索方向，再補旅館與補給提醒。
- 背包補上物品用途，避免只看到名稱與數量卻不知道能做什麼。
- 工會補上自己的任務提示，包含可交付、進行中需求，以及偵查完成後可挑戰 Boss 的狀態。
- 倉庫從背包 / 裝備選單中抽出，成為城鎮內的獨立設施。
- 戰鬥輸出不再讓攻擊、技能、道具、敵人反擊與狀態 tick 直接散落在同一條輸出流；各動作先產生事件文字，再由 combat loop 統一輸出 1-3 行回合摘要與完整 Battle Log。

## 5. 邊界

- 保留既有數字輸入、返回邏輯、save、schema、data 與 combat formula。
- Rich 不可用時仍退回純文字輸出。
- 使用者提供的 UI 草圖先視為探索稿，需映射到流程節點與 panel 職責後再判斷是否落地。
- 後續 UI 只能做小步 CLI 顯示層改善；戰鬥主畫面服務決策，Battle Log 服務回溯，除非另外明確批准新平台或 UI framework。
- 目前 UI-2 已採 HTML static prototype 作驗證路線；這不等於正式 GUI app，也不等於 runtime adapter。
- 下一個合理小切片應由使用者指定，並先做 read-only preflight；Synthesis / Shop / Workshop static prototype v1 已落地，不再作為未完成候選。
