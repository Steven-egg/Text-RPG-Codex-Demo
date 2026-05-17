# GUI Screen Map Draft

用途：記錄從目前 CLI / Rich prototype 轉向 GUI-oriented vertical slice 前的 screen map、UI action 與分階段策略。此文件只做規劃，不代表已開始 GUI 實作。

## 1. UI 三階段策略

三階段共用同一套 Screen Map、ScreenModel 與 UIAction；差異只在 render / presentation layer。

### Phase UI-1：Home Hub / Main Menu 文字式 UI

- 最接近目前 CLI panel 行為。
- 以文字、選單與簡單狀態資訊為主。
- 可由目前 CLI / Rich 或未來 HTML / Pygame 初版呈現。
- 目標是整理 screen flow、ScreenModel 與 UIAction。
- 不追求美術、不追求正式地圖、不處理素材風格。

### Phase UI-2：CLI / Rich 風格 Wireframe

- 用框線、區塊、簡單圖示與選取狀態組裝畫面。
- 類似低成本 GUI wireframe。
- 目標是驗證 screen layout、資訊分區、選取狀態與操作回饋。
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
→ Combat Result
→ Exploration Screen
→ Dungeon Clear / Retreat / Defeat Result
→ World Map Screen or Town Hub Screen
```

World Map 是正式 UI 的中樞。Town Hub 與 Dungeon / Exploration 是從 World Map 進入的兩種目的地。

## 3. Screen Map

| Screen | Purpose | 現有 CLI 參考 | 優先級 |
|---|---|---|---|
| Start Screen | 開始新冒險、讀取進度 | `start_screen_panel()` | 已有 CLI MVP |
| World Map Screen | 選擇目的地、查看主線目標與角色摘要 | `main_loop()` + `dungeon_menu()` 概念拆分 | 高 |
| Town Hub Screen | 點選城鎮設施 | `town_menu()` | 高 |
| Guild Screen | 任務列表、交付、素材收購、主線線索 | `guild_menu()` | 中 |
| Shop Screen | 商品分類、列表、詳情、購買 | `travel_shop()` | 中 |
| Forge Screen | 購買裝備、強化裝備、查看本店裝備 | `workshop_catalog()` | 中 |
| Synthesis Screen | 配方分類、列表、詳情、合成 | `craft_menu()` | 最高 |
| Inn Screen | 休息確認與資源回復 | `rest_inn()` | 低 |
| Storage Screen | 存入、取出、查看容量 | `storage_menu()` | 低 |
| Exploration Screen | 單一路線步數制探索、事件與撤退 | `explore_dungeon()` | 中 |
| Combat Screen | 回合制戰鬥決策與戰鬥紀錄 | `combat()` | 中後 |
| Result Screen | 戰鬥、探索、任務或合成結果 | 多處 `render_panel()` | 中 |

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

- `open_world_map`
- `open_town`
- `select_destination`
- `enter_dungeon`
- `open_facility`

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

## 6. 第一個實驗對象

建議先以米菈合成屋作第一個 ScreenModel / UIAction 實驗。

原因：

- 已有分類：全部 / 裝備 / 戰術道具。
- 已有列表、詳情、狀態與確認流程。
- 副作用清楚：扣金幣、扣素材、消耗基底裝備、取得產出。
- 可抽出通用模式：`category → item list → detail → confirm → result`。
- 風險低於戰鬥、背包、工會。

第一個實驗目標不應是 GUI，而是把現有合成屋拆成：

```text
build_synthesis_screen_model(state, selected_category, selected_recipe)
handle_synthesis_action(state, action)
render_with_cli_adapter(screen_model)
```

實作前仍需先 read-only 評估，不要直接重構 `game.py`。

## 7. 近期不要做

- 不直接選 pygame / HTML。
- 不建立新 GUI framework。
- 不啟動正式美術 asset pipeline。
- 不建立 prompt builder / asset registry / style bible。
- 不把目前 `input()` / `print()` menu 視為最終架構。
- 不繼續大範圍 CLI-only catalog polish。
- 不重構整個 `03_engine/engine/game.py`。
- 不改 save、schema、data 或 combat formula。

## 8. 下一步建議

1. Read-only 對照 `craft_menu()` / `craft_recipe_list_menu()`。
2. 文件化 Synthesis ScreenModel 欄位。
3. 文件化 Synthesis UIAction 列表。
4. 再決定是否做最小 runtime 實驗：只抽「畫面模型建構函式」，不改合成規則。
5. 成功後再評估 Shop Screen 是否沿用同一 pattern。
