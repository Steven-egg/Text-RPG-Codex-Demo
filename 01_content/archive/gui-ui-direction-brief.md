# GUI 導向 UI 總體規劃 Brief

用途：定義未來第一階段 GUI vertical slice 的方向，供新 session 先讀。此文件只做 UI 規劃，不代表已開始 GUI 實作，也不選定 pygame、HTML、Unity 或任何正式技術方案。

## 0. 當前邊界

- 不修改 runtime、data、schema、save 或 combat formula。
- 不重構 `03_engine/engine/game.py`。
- 不實作 GUI，不啟動 dev server，不生成圖片。
- 不選定 pygame / HTML / Unity / WebView 等 render 技術。
- 不建立正式 asset pipeline、prompt builder 或 asset registry。
- 不把目前 CLI `input()` / `print()` menu 視為最終架構。
- 目前 CLI / Rich panel 是 playable reference；未來 GUI 應抽象成 ScreenModel / UIAction 後再接不同 render layer。

## 1. 第一階段 GUI Vertical Slice 畫面範圍

第一階段 GUI vertical slice 的目標不是覆蓋所有系統，而是把核心循環整理成一條可視覺化、可互動、可反覆驗證的最小閉環：

```text
Start
→ World Map
→ Town Hub
→ Facility
→ World Map
→ Exploration
→ Combat
→ Result / Reward
→ Exploration or World Map / Town Hub
```

### Start Screen

目的：建立遊戲入口與存檔選擇的第一印象。

第一階段包含：
- 遊戲標題與最小進入選項。
- 有存檔時顯示「載入進度 / 重新開始」。
- 無存檔時顯示「開始新冒險」。
- 可顯示角色摘要或最近進度，但不得依賴圖片內文字。

不包含：
- 角色創建流程重做。
- 全螢幕動畫、影片、複雜背景素材。

### World Map Screen

目的：作為正式 GUI 的中樞，承接城鎮與探索兩種主要目的地。

第一階段包含：
- 目前主線目標。
- 角色摘要：職業、等級、HP/MP、金幣、關鍵狀態。
- 可進入的城鎮與迷宮節點。
- 迷宮可用 / 不可用原因、推薦等級、Boss / gate 狀態。

不包含：
- 自由拖曳大地圖。
- 多區域世界探索。
- 動態天候、路線動畫或大量地圖素材。

### Town Hub Screen

目的：把城鎮設施整理成 GUI 可點選的 hub，而不是沿用單層數字選單。

第一階段包含：
- 城鎮設施入口：工會、旅人小鋪、工坊、米菈合成屋、星燈魔法商店、旅館、倉庫、轉職神殿 / 聖物調查 preview。
- 每個設施的用途提示與可交付 / 可處理狀態。
- 玩家資源摘要與下一步推薦。

不包含：
- 城鎮自由行走。
- NPC 對話系統重做。
- 所有設施都做完整 GUI 詳情。

### Facility Screen：Synthesis / Shop 類設施

目的：先驗證最有代表性的 list-detail-confirm-result 模式，作為之後商店、工坊、魔法書、合成屋共用模板。

第一階段優先對象：
- 米菈合成屋 Synthesis Screen。
- 旅人小鋪 Shop Screen 可作第二候選。

第一階段包含：
- 分類 tab。
- 項目列表。
- 詳情區。
- 條件 / 持有 / 價格 / 素材狀態。
- 確認 action。
- 成功或失敗結果提示。

不包含：
- 新增配方、商品、價格、批量購買或賣出規則。
- 新增素材圖示 pipeline。
- 把所有 facility 一次做完。

### Exploration Screen

目的：呈現單一路線步數制探索，保留目前 CLI 核心節奏。

第一階段包含：
- 迷宮名稱、目前步數、總步數。
- 玩家 HP/MP 與本趟收益摘要。
- 當前事件：素材、遭遇、Boss gate、撤退、通關提示。
- 主要 action：前進、撤退、查看簡短狀態。

不包含：
- 格子地圖、自由移動、碰撞或即時探索。
- 新事件系統。
- 新迷宮規則。

### Combat Screen

目的：服務回合決策，不把完整戰鬥過程擠在主畫面。

第一階段包含：
- 玩家 HP/MP、狀態、可用指令。
- 敵人 HP、屬性、狀態。
- 回合數與上一動短摘要。
- 指令：攻擊、防禦、技能、道具、逃跑。
- 可開啟 Battle Log，但主畫面只保留決策所需資訊。

不包含：
- 新 combat formula。
- 多目標戰鬥重做。
- 動畫系統或特效 pipeline。

### Result / Reward Screen

目的：把戰鬥、探索、合成、購買、任務交付的結果集中成可讀、可返回的回饋畫面。

第一階段包含：
- 成功 / 失敗 / 撤退 / 戰敗 / 通關狀態。
- 金幣、EXP、素材、道具、關鍵 unlock。
- 下一步 action：返回探索、回城、回世界地圖、查看詳情。
- Battle Log 或事件摘要入口。

不包含：
- 成就系統。
- 大量獎勵動畫。
- 新掉落規則。

## 2. 視覺方向高層定調

### 遊戲整體感覺

《元素迷宮：邊境冒險者》的 GUI 應該像「溫暖但危險的邊境冒險」：城鎮有手作、營地、工坊與旅人補給的生活感；迷宮有潮濕石壁、焦黑岩層、灰燼火光與古老印記的危險感。整體應保持清楚、可讀、可反覆操作，不走單純炫技或厚重到壓過資訊的方向。

第一階段視覺重點：
- 讓玩家一眼知道目前在哪裡。
- 讓主要 action 明確可選。
- 讓資源、條件、風險、回饋可被快速掃讀。
- 讓世界觀透過材質、色彩、icon 與小型場景提示出現，而不是靠大段說明文字。

### 主要 UI 語彙

推薦語彙：
- 地圖節點：World Map 用節點與狀態標記表達地點。
- Hub 入口：Town Hub 用設施入口與狀態 badge 表達可處理事件。
- List + Detail：Shop、Synthesis、Forge、Magic Book 優先使用分類、列表、詳情、確認、結果。
- Status Strip：玩家資源與關鍵狀態用穩定位置呈現。
- Action Bar：當前可做的語意 action 集中放置。
- Log Drawer / Log Panel：戰鬥與探索完整紀錄收納在可開啟區域，不干擾主決策。
- Disabled Reason：不可用 action 必須顯示原因，例如等級不足、素材不足、任務未完成。

避免語彙：
- 把所有東西做成單層按鈕牆。
- 把 CLI 數字選單直接搬成 GUI。
- 為了看起來像 GUI 而增加不必要流程。

### 色彩與材質方向

色彩方向：
- 城鎮：暖木、鐵灰、羊皮紙、布料、黃銅、柔和燈火。
- 迷宮：苔綠、濕石、焦黑、熔岩橙、灰燼紅、暗紫作少量魔法點綴。
- 魔法：星燈藍、晶粉、冷白光，用於技能、魔法書與特殊狀態。
- 危險 / Boss / gate：深紅、焦橙、黑鐵，但只用於警示與重點。
- 成功 / 可製作 / 可交付：穩定綠或金色點綴。
- 不可用 / 缺素材：低飽和灰、暗紅或斜線狀態，不只靠顏色判斷。

材質方向：
- 面板可參考羊皮紙、木框、鐵鉚釘、石板、布標籤，但必須保持文字清晰。
- icon 可使用線性或半填色符號，重點是語意穩定，而不是每個物品都先有精緻插畫。
- 背景圖只服務地點氛圍，不應遮住資訊層。

### 角色、場景、Icon、面板使用原則

角色：
- NPC 或玩家角色圖可以用於設施與劇情氣氛，但第一階段不是必需。
- 角色圖不可承載動態資訊，例如價格、任務狀態、可交付條件。
- 同一 NPC 的剪影、色調與服裝語彙應穩定，避免每個畫面像不同遊戲。

場景：
- Start、World Map、Town Hub、Facility、Exploration 可有場景背景或局部背景。
- 背景應提供地點辨識與情緒，不應把關鍵操作藏在畫面內。
- 迷宮背景可重複使用同一套氣氛圖，不需要每個事件都有新圖。

Icon：
- icon 優先表達類別與狀態：補給、素材、裝備、魔法、任務、Boss、gate、金幣、HP/MP。
- icon 必須搭配文字或 tooltip，不可成為唯一資訊來源。
- 第一階段應先定義 icon 語意清單，再決定是否需要正式素材。

面板：
- 面板是資訊分區，不是把文字做進圖片。
- 同類畫面應共用資訊層級：標題、摘要、列表、詳情、行動、結果。
- 重要狀態應有固定位置，避免每個 screen 重新學一次。

### 不能畫死在圖片裡的文字

以下文字必須由 render layer 動態輸出，不可烘在背景圖或裝飾圖片內：

- screen title、subtitle、目前地點名稱。
- 所有按鈕、選單、tab、action label。
- 物品、裝備、技能、配方、任務、迷宮、怪物、NPC 名稱。
- 價格、持有數、素材需求、最多可製作次數。
- HP、MP、EXP、金幣、等級、推薦等級、步數。
- 可用 / 不可用原因、gate 條件、Boss 狀態。
- 任務描述、戰鬥摘要、Battle Log、探索事件文字、獎勵文字。
- 錯誤提示、確認提示、返回提示。
- 未來可能本地化、平衡調整或由 data 驅動的任何內容。

可以畫進圖片的內容：
- 無語意依賴的紋理、符號、印記、邊框。
- 不需讀取的裝飾性標牌。
- 背景建築、場景物件、光影與材質。

### 禁止方向與風格漂移風險

禁止方向：
- 不做現代科幻儀表板風。
- 不做過度霓虹、手遊抽卡、滿版特效 UI。
- 不做純黑暗硬核奇幻到難以閱讀。
- 不做所有畫面都同色系的單調 palette。
- 不把文字烘進圖片。
- 不先大量生成角色、場景或 icon。
- 不以單張漂亮 mockup 反推 runtime 架構。
- 不把 pixel art、Q 版、寫實照片、厚塗史詩風混在同一批規格中。

主要風格漂移風險：
- 從「文字冒險 RPG」漂成「自由移動地圖 RPG」。
- 從「ScreenModel / UIAction 共用」漂成「每個畫面各自硬寫互動」。
- 從「資訊清楚」漂成「背景圖很漂亮但按鈕與數值難讀」。
- 從「一個 screen mockup 實驗」漂成「一次生成大量素材」。
- 從「第一階段 GUI vertical slice」漂成「正式 asset pipeline」。

## 3. Screen Map

### Flow A：Start → World Map → Town Hub → Facility

```text
Start Screen
→ World Map Screen
→ Town Hub Screen
→ Facility Screen
   - Synthesis Screen
   - Shop Screen
   - Forge / Magic / Guild / Inn / Storage as later variants
→ Town Hub Screen
→ World Map Screen
```

| Screen | 目的 | 主要資訊 | 主要 action | 目前 CLI reference |
|---|---|---|---|---|
| Start Screen | 進入遊戲、讀取或重新開始 | 標題、存檔狀態、最近進度 | `start_new_game`、`load_game`、`restart_game`、`exit_game` | `start_screen_panel()` |
| World Map Screen | 選擇城鎮或迷宮目的地 | 玩家摘要、主線目標、地點節點、gate / Boss 狀態 | `open_town`、`select_destination`、`enter_dungeon`、`save_game` | `main_loop()` 與 `dungeon_menu()` 概念拆分 |
| Town Hub Screen | 選擇城鎮設施與查看可處理事項 | 玩家資源、設施列表、可交付 / 可購買 / 可休息提示 | `open_facility`、`open_character`、`open_inventory`、`open_world_map` | `town_menu()` |
| Facility Screen | 處理商店、合成、工坊、魔法書等設施互動 | 分類、列表、詳情、條件、價格、持有狀態、結果 | `select_category`、`select_item`、`open_detail`、`confirm`、`back`、設施專用 action | `travel_shop()`、`workshop_catalog()`、`craft_menu()`、魔法書 catalog |

Facility 第一階段以 Synthesis / Shop 類為代表：

| Facility Variant | 目的 | 主要資訊 | 主要 action | 目前 CLI reference |
|---|---|---|---|---|
| Synthesis Screen | 驗證配方 list-detail-confirm-result 模式 | 配方分類、產出、素材、基底裝備、金幣、最多可製作次數 | `craft_recipe`、`confirm`、`back` | `craft_menu()` |
| Shop Screen | 驗證商品分類、詳情與購買模式 | 商品分類、持有數、價格、效果、解鎖狀態 | `buy_item`、`confirm`、`back` | `travel_shop()` |

### Flow B：Start → World Map → Exploration → Combat → Result

```text
Start Screen
→ World Map Screen
→ Exploration Screen
→ Combat Screen
→ Result / Reward Screen
→ Exploration Screen
→ World Map Screen or Town Hub Screen
```

| Screen | 目的 | 主要資訊 | 主要 action | 目前 CLI reference |
|---|---|---|---|---|
| Start Screen | 進入遊戲、讀取或重新開始 | 標題、存檔狀態、最近進度 | `start_new_game`、`load_game`、`restart_game`、`exit_game` | `start_screen_panel()` |
| World Map Screen | 選擇迷宮並理解風險 | 玩家摘要、迷宮列表、推薦等級、步數、Boss / gate 狀態 | `select_destination`、`enter_dungeon`、`open_town` | `dungeon_menu()` 概念拆分 |
| Exploration Screen | 推進步數制探索 | 迷宮、步數、HP/MP、本趟收益、事件摘要 | `advance_step`、`retreat`、`open_inventory`、`open_character` | `explore_dungeon()` |
| Combat Screen | 回合制決策 | 玩家 / 敵人 HP、MP、狀態、回合數、上一動摘要、可用指令 | `basic_attack`、`defend`、`open_skill_menu`、`use_skill`、`open_item_menu`、`use_item`、`retreat`、`view_battle_log` | `combat()` |
| Result / Reward Screen | 集中回饋收益、失敗與解鎖 | EXP、金幣、掉落、素材、關鍵道具、任務進度、Battle Log 入口 | `confirm`、`back_to_exploration`、`return_to_town`、`open_world_map` | 多處 `render_panel()` 結算畫面 |

## 4. UI 三階段策略

三階段共用同一套 ScreenModel / UIAction；差異只在 render layer。

### UI-1：Home Hub / Main Menu 文字式 UI

定位：
- 仍可在目前 CLI / Rich 環境中表現。
- 用文字與簡單 panel 先確認 screen flow、資訊分區、action 語意。
- 目標是讓現有 playable reference 更接近未來 GUI 的畫面職責。

應產出：
- 每個 screen 的 ScreenModel 欄位。
- 每個 screen 的 UIAction 清單。
- list-detail-confirm-result 的最小共用模式。

不應產出：
- GUI framework。
- 正式美術素材。
- 大規模 `game.py` 重構。

### UI-2：CLI / Rich Wireframe

定位：
- 以 Rich panel、框線、區塊、簡單標記、選取狀態模擬 GUI layout。
- 用低成本方式驗證資訊層級、焦點、不可用原因與結果回饋。

應產出：
- 更接近 GUI 的 layout wireframe。
- ScreenModel 到 render adapter 的概念驗證。
- UIAction 與畫面狀態的對照。

不應產出：
- 正式圖片。
- 完整 asset registry。
- 平台選型結論。

### UI-3：最終 GUI 視覺版

定位：
- 接上正式 render layer 後的視覺版本。
- 使用場景背景、角色圖、icon、UI skin 與互動狀態。

進入條件：
- Screen Map 已穩定。
- ScreenModel / UIAction 已能承接至少一個 Facility screen。
- asset request schema 已定義。
- 第一個 screen mockup / prompt 實驗已有結果。
- asset registry 已能追蹤來源、用途、版本與授權 / 生成參數。

不應提前做：
- 在 UI-1 / UI-2 還不穩時直接大量做圖。
- 為單張 mockup 決定整個技術方案。
- 讓視覺稿改寫 gameplay 規則。

## 5. MVP 拆分順序

建議後續按以下順序前進：

1. 先做整體規格。
   - 完成此 GUI UI direction brief。
   - 對齊 `01_content/ui-flow-blueprint.md` 與 `01_content/gui-screen-map.md`。
   - 補齊 screen scope、視覺方向、禁止方向與三階段策略。

2. 再做 asset request schema。
   - 只定義「若未來需要素材，要如何描述」。
   - schema 應包含 asset type、screen、用途、文字是否動態、尺寸比例、透明需求、狀態變體、風格關鍵詞、禁止事項。
   - 此步仍不生成圖片。

3. 再做第一個 screen mockup / prompt 實驗。
   - 優先 Synthesis Screen 或 Start Screen 二選一。
   - 建議 Synthesis Screen：最能驗證分類、列表、詳情、條件、確認、結果。
   - 只做一個 screen，一個方向即可，不一次做完整 asset set。

4. 再建立 asset registry。
   - 用來記錄素材 id、用途 screen、來源、版本、狀態、是否可替換、文字是否動態、prompt / 生成設定。
   - registry 建立前不要大量製圖，避免之後無法管理。

5. 不要一次生成大量圖片。
   - 第一輪最多只做一個 screen mockup 所需的極少量素材。
   - 先驗證資訊可讀性與畫面結構，再決定是否擴張素材。
   - 所有動態文字仍由 render layer 輸出。

## 6. 下一個 Session 建議

若下一個 session 繼續 UI 規劃，最適合做：

1. 讀取 `01_content/gui-ui-direction-brief.md`、`01_content/gui-screen-map.md`、`01_content/ui-flow-blueprint.md`。
2. 新增 asset request schema 草案文件，例如 `01_content/gui-asset-request-schema.md`。
3. 先只定義 schema，不生成圖片，不選平台。
4. 若要做第一個 screen mockup，先選 Synthesis Screen，因為它已有穩定的分類、列表、詳情、條件、確認與結果流程。

