# GUI Screen Map Draft

用途：記錄從目前 CLI / Rich playable reference 轉向 GUI-oriented vertical slice 的 screen map、UI action 與分階段策略。此文件只做規劃；目前已存在的 GUI work 是 `07_gui_prototype/` HTML static prototype，不代表正式 runtime GUI 或 runtime adapter。

## 1. UI 三階段策略

三階段共用同一套 Screen Map、ScreenModel 與 UIAction；差異只在 render / presentation layer。

### Phase UI-1：Home Hub / Main Menu 文字式 UI

- 最接近目前 CLI panel 行為。
- 以文字、選單與簡單狀態資訊為主。
- 可由目前 CLI / Rich 或未來 HTML / Pygame 初版呈現。
- 目標是整理 screen flow、ScreenModel 與 UIAction。
- 不追求美術、不追求正式地圖、不處理素材風格。

### Phase UI-2：HTML Static Fixture Prototype

- 用 HTML/CSS/JS render layer、static fixtures、靜態 navigation 與 UIAction logging 組裝畫面。
- 目標是驗證 screen layout、資訊分區、選取狀態、操作回饋與 prototype navigation。
- 不接 Python runtime，不讀寫 `save.json`，不把 gameplay rules 複製進 JS。
- 不處理正式美術 asset pipeline。
- 不要求每個場景有正式背景圖。
- 不先建立嚴格 prompt / schema / style bible。

### Phase UI-3：最終 GUI 視覺版本

- 接近正式遊戲畫面。
- 使用完整背景圖、建築圖、角色圖、icon 與 UI skin。
- 需要 asset request schema、prompt builder、asset registry 與 style bible。
- 此階段屬後期，不應現在直接實作。

## 2. 正式 Flow 草案

### Flow A：城鎮與功能介面

```text
Start Screen
→ World Map Screen
→ Town Hub Screen
→ Facility Screen
   - Shop Screen
   - Guild Screen
   - Forge Screen
   - Synthesis Screen
   - Inn Screen
   - Storage Screen
→ Town Hub Screen
→ World Map Screen
```

### Flow B：探索與戰鬥介面

```text
Start Screen
→ World Map Screen
→ Exploration Screen
   - Step forward
   - Event / material / battle / boss trigger
→ Combat Screen
→ Combat Result overlay
→ Exploration Screen
→ Dungeon Clear / Retreat / Defeat Result
→ World Map Screen or Town Hub Screen
```

World Map 是正式 UI 的中樞。Town Hub 與 Dungeon / Exploration 是從 World Map 進入的兩種目的地。

## 3. Screen Map

| Screen | Purpose | 現有 CLI 參考 | 優先級 |
|---|---|---|---|
| Start Screen | 開始新冒險、讀取進度 | `start_screen_panel()` | static prototype 已落地 |
| World Map Screen | 選擇目的地、查看主線目標與角色摘要 | `main_loop()` + `dungeon_menu()` 概念拆分 | static prototype 已落地 |
| Town Hub Screen | 場景式 facility hub，點選建築入口進入城鎮設施 | `town_menu()` | static prototype 已落地 |
| Guild Screen | 任務列表、交付、素材收購、主線線索 | `guild_menu()` | static prototype 已落地 |
| Shop Screen | 商品分類、列表、詳情、購買 | `travel_shop()` | static prototype 已落地 |
| Forge / Workshop Screen | 購買裝備、強化裝備、查看本店裝備 | `workshop_catalog()` | static prototype 已落地 |
| Synthesis Screen | 配方分類、列表、詳情、合成 | `craft_menu()` | static prototype 已落地 |
| Inn Screen | 休息確認與資源回復 | `rest_inn()` | 低 |
| Storage Screen | 存入、取出、查看容量 | `storage_menu()` | static prototype 已落地 |
| Magic Shop Screen | 購買與學習技能書 | `magic_shop_catalog()` | static prototype 已落地 |
| Exploration Screen | 單一路線步數制探索、事件與撤退 | `explore_dungeon()` | static prototype 已落地 |
| Combat Screen | 回合制戰鬥決策與戰鬥紀錄 | `combat()` | static prototype 已落地 |
| Result Screen | 結果概念；Combat Result 目前整合為 Combat Screen overlay | 多處 `render_panel()` | 概念保留 |

## 4. UIAction 草案

Action 應描述遊戲語意，不綁定鍵盤、滑鼠或觸控。

通用 action：

- `confirm`
- `cancel`
- `back`
- `open_detail`
- `close_detail`
- `select_category`
- `select_item`
- `next_tab`
- `previous_tab`
- `open_character`
- `open_inventory`
- `save_game`
- `exit_game`

World Map / Town action：

- `back_to_start_screen`
- `open_world_map`
- `open_town`
- `select_destination`
- `enter_dungeon`
- `open_facility`

Town Hub 目前仍可保留 `open_character` / `open_inventory` 作為現階段主 hub 相容入口；最終是否屬於全域導航，待後續 navigation model 再定。

World Map static prototype 目前不使用 `exit_game`。回到標題以 `back_to_start_screen` 表示，並先寫入 UIAction log 再導向 Start Screen static prototype；`view_status`、`open_inventory`、`open_bestiary`、`save_game` 與 `open_settings` 在 World Map drawer 中只作語意展示與 UIAction logging，不接 runtime、不讀寫 `save.json`。

Facility action：

- `buy_item`
- `learn_magic`
- `upgrade_equipment`
- `craft_recipe`
- `submit_quest`
- `sell_material`
- `rest_inn`
- `deposit_item`
- `withdraw_item`

Exploration / Combat action：

- `advance_step`
- `retreat`
- `basic_attack`
- `defend`
- `open_skill_menu`
- `use_skill`
- `open_item_menu`
- `use_item`
- `choose_target`
- `view_battle_log`

## 5. ScreenModel 草案

ScreenModel 先以資料結構描述畫面，不指定 render 技術。

建議最小欄位：

```text
ScreenModel
- screen_id
- title
- subtitle
- player_summary
- objective
- sections
- selected_id
- actions
- result_message
```

Action item 建議欄位：

```text
UIActionItem
- action_id
- label
- description
- enabled
- disabled_reason
- payload
```

List row 建議欄位：

```text
ListRow
- id
- title
- category
- status
- summary
- owned_count
- price
- detail
```

Town Hub V1 補充摘要：

```text
TownHubScreenModel
- resource_strip
- town_guidance
- facility_nodes
- selected_facility_id
- global_actions
```

Town Hub 採場景式 hub，不以純列表作為主要結構。`facility_nodes` 承接工會、旅館、工坊、商店、合成屋、魔法商店、轉職神殿、聖物調查與倉庫等建築入口；badge 只保留少量高價值提示，例如工會可回報、火印線索、合成屋未解鎖。完整規格見 `01_content/archive/gui-town-hub-screen-model-draft.md`。

## 6. 後續實驗對象

Start Screen、Town Hub、Guild、Synthesis、World Map、Dungeon Exploration、Combat、Shop、Workshop、Storage、Magic Shop static prototype 都已落地。後續實驗對象應由使用者指定單一小切片，並先做 read-only preflight。

較安全的候選：

- Inn Screen static prototype
- Town Hub / Guild 的 keyboard focus graph
- 單一既有畫面小幅 polish
- shared prototype shell / fixture loader（僅列為後續候選，不要實作）

任何後續 UI-2 工作仍只驗證 static fixtures、render layer、layout、interaction、navigation flow 與 UIAction logging；不接 runtime、不讀寫 save、不啟動正式 asset pipeline。

## 7. 近期不要做

- 不把 HTML static prototype 視為正式 GUI app 或 runtime adapter。
- 不建立新 GUI framework。
- 不啟動正式美術 asset pipeline。
- 不建立 prompt builder / asset registry / style bible。
- 不把目前 `input()` / `print()` menu 視為最終架構。
- 不繼續大範圍 CLI-only catalog polish。
- 不重構整個 `03_engine/engine/game.py`。
- 不改 save、schema、data 或 combat formula。

## 8. 下一步建議

1. 先維持 HTML static prototype 邊界，由使用者指定單一小切片。
2. 若是 GUI 任務，先做 Task Zone read-only preflight，再決定是否進行 docs-only 或 prototype-only 小修。
3. Synthesis / Shop / Workshop / Storage / Magic Shop static prototype v1 都已落地，不再列為未完成候選。
4. 暫不接 runtime、不讀寫 save、不生成新圖、不啟動正式 asset pipeline。
