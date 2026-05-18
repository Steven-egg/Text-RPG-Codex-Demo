# GUI Guild Screen Model Draft

用途：把已採納的 Guild Screen visual baseline 收斂成 Guild Screen V1 的 ScreenModel / row model / UIAction 規格。此文件只做 GUI 規劃，不代表已實作 GUI，也不修改 runtime。

## 0. 邊界

- 不修改 runtime、data、schema、save、combat formula。
- 不重構 `03_engine/engine/game.py`。
- 不選定 pygame / HTML / Unity / WebView 或其他 GUI 技術。
- 不建立正式 asset pipeline。
- 不生成新圖片。
- 不移動 reference image。
- 不新增任務、報酬、工會積分、任務歷史或工會管理系統。
- 不新增「接任務」流程、不新增 `active_quests`，也不把解鎖任務改成需接取後才進行。
- 不把工會素材收購納入 Guild Screen V1 主視覺；素材收購未來若需要，應另作 Guild Buyback / Exchange 類型畫面。
- 不把 Guild Screen baseline 圖直接視為 runtime asset。
- 不把任何固定文字畫死在圖片裡；任務名稱、描述、條件、報酬、狀態、feedback、action label 都必須由 render layer 動態輸出。

## 1. 來源與定位

主要來源文件：

- `01_content/gui-planning-index.md`
- `01_content/gui-ui-direction-brief.md`
- `01_content/gui-screen-map.md`
- `01_content/ui-flow-blueprint.md`
- `01_content/gui-facility-screen-template.md`
- `01_content/gui-guild-screen-visual-baseline.md`
- `01_content/gui-asset-registry-draft.md`

參考圖：

```text
05_assets/gui_references/guild_screen/guild_screen_visual_baseline_v1_user_reference.png
```

Guild Screen V1 的定位是：

```text
Adventurers' Guild / Quest Board
冒險者工會 / 委託板
```

V1 正式語意：

- 已解鎖委託瀏覽。
- 查看任務需求與報酬。
- 條件滿足時提交 / 回報任務。
- 持有三枚火印碎片後，顯示向諾亞詢問的主線入口。

V1 不包含：

- 接任務系統。
- `active_quests` 或任務接取狀態。
- 可接任務 / 進行中任務這類任務生命週期 tab。
- `category_tabs` 命名與分類模型。
- 工會素材收購主畫面。
- 完整工會管理、工會歷史、工會聲望或批量回報。

## 2. Screen Flow

Guild Screen 屬於 Flow A 的 Facility Screen 變體。

```text
Town Hub Screen
→ Guild Screen
→ Town Hub Screen
```

V1 不做工會內多層路由，不做 `category_tabs`，也不做 `sections` / `selected_section_id`。V1 可保留 `task_filters` 作為 UI-only 篩選，三枚火印碎片後的詢問入口以 `story_hint_card` 處理；若 layout 受限，可降級為特殊互動列。

## 3. Model 目標

`GuildScreenModel` V1 應回答：

- 目前有哪些已解鎖委託可瀏覽？
- 目前套用哪個 UI-only filter？
- 是否有可顯示的主線詢問入口？
- 目前選中的任務是什麼？
- 選中任務的標題、委託人與描述是什麼？
- 選中任務的回報條件目前是否滿足？
- 選中任務的報酬是什麼？
- 工會接待員或系統應提示什麼？
- 右下單一主要 action 應是 `submit_quest`、`open_story_hint` 還是 `unavailable`？

此 model 應可被 CLI / Rich wireframe、未來 GUI 點擊或觸控共用；輸入方式不可寫死在 model 內。

## 4. GuildScreenModel V1

建議欄位：

```text
GuildScreenModel
- screen_id
- facility_id
- title
- subtitle
- visual_baseline_id
- npc
- player_summary
- task_filters
- selected_filter_id
- task_rows
- story_hint_card
- selected_task_id
- task_detail
- reward_summary
- condition_rows
- feedback_message
- primary_action
- secondary_actions
- empty_state
```

欄位說明：

| Field | 說明 |
|---|---|
| `screen_id` | 固定為 `facility_guild_screen`。 |
| `facility_id` | 固定為 `guild` 或未來資料層對應 id。 |
| `title` | 動態標題，例如 `冒險者工會 / 委託板`。 |
| `subtitle` | 短提示，例如接待員引導或目前委託板狀態。 |
| `visual_baseline_id` | 對應 `gui_guild_screen_visual_baseline_v1`，只作 reference 追蹤。 |
| `npc` | 接待員 / 工會角色呈現資訊，不承載任務條件。 |
| `player_summary` | 可選玩家摘要；V1 不應放過多資源槽。 |
| `task_filters` | UI-only 任務篩選器，不寫入 save/state。 |
| `selected_filter_id` | 目前套用的 UI-only filter。 |
| `task_rows` | 套用 filter 後顯示的已解鎖任務列表 row。 |
| `story_hint_card` | 可選；三枚火印碎片後的諾亞詢問入口。 |
| `selected_task_id` | 目前選中的任務 id；只指向任務，不指向 filter。 |
| `task_detail` | 中央任務詳情。 |
| `reward_summary` | 中央中段報酬摘要。 |
| `condition_rows` | 中央下方任務達成 / 回報條件檢查表。 |
| `feedback_message` | 底部 NPC guidance / operation feedback。 |
| `primary_action` | 右下單一主要 action。 |
| `secondary_actions` | 返回 Town Hub 等次要 action。 |
| `empty_state` | 無任務或無選取時的顯示狀態。 |

V1 明確不使用：

- `category_tabs`
- `selected_category_id`
- `sections`
- `selected_section_id`

## 5. Task Filters V1

Guild Screen V1 可保留 `task_filters`，但它們只作為 UI-only filter，不代表 gameplay state，也不寫入 save/state/schema。

建議 filter：

```text
GuildTaskFilter
- id
- label
- count
- selected
- enabled
```

| Filter ID | Label | 推導方式 |
|---|---|---|
| `all` | 全部委託 | `quest_unlocked(state, quest_id)` |
| `ready_to_submit` | 可回報 | `quest_unlocked(state, quest_id)` 且 `quest_ready(state, quest_id)` |
| `completed` | 已完成 | `quest_unlocked(state, quest_id)` 且 `quest_id in state["completed_quests"]` |

原則：

- 目前 runtime 沒有任務接取流程，只有「已解鎖且未完成 / 可回報 / 已完成」的狀態。
- `可接任務`、`進行中任務` 會暗示不存在的 `active_quests`。
- `task_filters` 只決定哪些 `task_rows` 顯示，不改變任務規則。
- `count` 可由同一批已解鎖任務 row 即時計算。
- 不使用 `category_tabs` 命名，避免誤解成任務資料分類或玩法狀態。
- 三枚火印碎片後的諾亞詢問是特殊互動入口，不進入 filter，也不升級成完整主線 tab。

V1 呈現方式：

- 頂部或左側顯示 `全部委託 / 可回報 / 已完成` filter。
- `task_rows` 顯示套用 `selected_filter_id` 後的任務列。
- 若 `can_ask_fire_mark_guild_inquiry(state)` 成立，顯示 `story_hint_card`；若 layout 受限，可降級為任務列表附近的特殊互動列。

## 6. GuildTaskRow V1

左側列表只服務掃描，不承載完整描述或完整報酬。

```text
GuildTaskRow
- task_id
- title
- giver
- status
- status_label
- status_icon_id
- selected
- enabled
- disabled_reason
- sort_key
```

欄位說明：

| Field | 說明 |
|---|---|
| `task_id` | 任務 id。 |
| `title` | 任務名稱，動態文字。 |
| `giver` | 委託人，例如 `諾亞`、`伊芙`、`拉比`。 |
| `status` | V1 任務狀態。 |
| `status_label` | 顯示用短狀態，例如 `可回報`、`條件不足`、`已完成`。 |
| `status_icon_id` | 狀態 icon 語意 id，不是圖片路徑。 |
| `selected` | 是否為目前選取 row。 |
| `enabled` | 是否可選取查看詳情；V1 的已解鎖任務通常可選。 |
| `disabled_reason` | 不可選原因；V1 多數情境可為空。 |
| `sort_key` | 排序用，不顯示給玩家。 |

V1 暫不放：

- `category_id`
- `location_label`
- `recommended_level`
- 任務類型欄位
- 長摘要或完整條件

左側 row 不應包含：

- 任務長描述。
- 完整報酬清單。
- 完整條件表。
- 多個 action。

## 7. Task Status V1

建議狀態值：

| Status | 意義 | 常見 primary action |
|---|---|---|
| `ready_to_submit` | 條件已滿足，可回報 | `submit_quest` |
| `requirements_missing` | 已解鎖但條件不足 | `unavailable` |
| `completed` | 已完成 | `unavailable` |
| `story_hint` | 主線詢問或特殊提示 | `open_story_hint` |

注意：

- V1 不使用 `available`，避免暗示「可接任務」。
- V1 不使用 `active`，避免暗示 `active_quests` 或接取流程。
- V1 不使用 `ready_to_turn_in`，改用較貼近目前 runtime 的 `ready_to_submit`。
- 已完成任務仍可保留在列表中，方便確認進度，但 primary action 應為 `unavailable`。
- `story_hint` 不對應 quest completion 規則，不應被當成正式任務狀態。

## 8. GuildTaskDetail V1

中央上方任務詳情區。

```text
GuildTaskDetail
- task_id
- title
- giver
- description
- status_label
- related_unlocks
- notes
```

欄位說明：

| Field | 說明 |
|---|---|
| `title` | 任務名稱，來自 `QUESTS[quest_id]["title"]`。 |
| `giver` | 委託人，來自 `QUESTS[quest_id]["giver"]`。 |
| `description` | 任務描述，來自 `QUESTS[quest_id]["desc"]`。 |
| `status_label` | 可回報、條件不足、已完成或主線線索。 |
| `related_unlocks` | 可選；來自 `QUESTS[quest_id]["unlocks"]` 的 raw / readable 摘要。 |
| `notes` | 可選；例如 V1 對 story hint 的短說明。 |

V1 延後，不納入欄位：

- `task_type`
- `location_label`
- `recommended_level`
- 由迷宮或 Boss 推導出的風險提示

限制：

- 不把完整條件表塞進 description。
- 不把報酬與條件混在同一段長文字。
- 不為了顯示地點、等級或類型新增 adapter mapping。
- 不把任何欄位畫死在背景圖中。

## 9. GuildRewardSummary V1

中央中段報酬摘要區。

```text
GuildRewardSummary
- gold
- guild_points
- items
- unlocks
- notes
```

```text
GuildRewardItem
- item_id
- label
- quantity
- icon_id
```

欄位原則：

- `gold`、`items`、`guild_points` 應直接由 `QUESTS[quest_id]["reward"]` 產生。
- `guild_points` 對應目前 runtime 的工會積分，不使用 `reputation` 命名。
- `unlocks` 可先顯示 raw / readable 摘要；若需要完整人類可讀分類，應另做 adapter，不在 V1 強求。
- V1 不新增正式工會聲望系統。
- 報酬摘要不承載回報條件。
- 沒有報酬時應顯示可讀 empty state，而不是隱藏區塊造成 layout 跳動。

## 10. GuildConditionRow V1

中央下方任務達成 / 回報條件檢查表。

```text
GuildConditionRow
- id
- condition_type
- label
- required_value
- current_value
- status
- status_icon_id
- disabled_reason
- source
```

V1 `condition_type`：

| Type | 用途 |
|---|---|
| `turn_in_item` | 回報素材、物品或裝備。 |
| `flag_set` | `flag:xxx` 條件，例如 Boss 擊敗 flag。 |
| `none` | 任務沒有交付需求。 |

V1 `status`：

| Status | 意義 |
|---|---|
| `met` | 已滿足。 |
| `missing` | 未滿足。 |
| `not_applicable` | 此任務不需要該條件。 |

row 顯示應支援：

```text
條件類型 icon
→ 條件名稱
→ 需求數量 / 目前持有數或目前狀態
→ 狀態 marker
```

限制：

- 不應 icon-only。
- 不只靠紅綠色判斷。
- V1 條件來源只讀 `QUESTS[quest_id]["turn_in"]` 與 `state.inventory` / `state.flags`。
- 不在 V1 新增討伐數、探索完成度、前置任務鏈等 adapter 欄位。

## 11. StoryHintCard V1

三枚火印碎片後的諾亞詢問入口優先用特殊提示卡表示，不做成 tab，也不計入 `task_filters`。若 layout 受限，可降級為任務列表附近的特殊互動列。

```text
GuildStoryHintCard
- id
- title
- description
- status
- status_label
- visible
- enabled
- disabled_reason
- primary_action
```

建議固定語意：

- `id`: `story_hint_fire_mark_guild_inquiry`
- `title`: `詢問三枚印記碎片的事情`
- `status`: `story_hint`
- `primary_action`: `open_story_hint`

顯示條件應忠於現有 runtime：

- 玩家持有 `key_fire_mark_shard x3`。
- 尚未設定 `fire_mark_guild_inquiry_done`。

此 row 不應：

- 寫入 `QUESTS`。
- 當成正式任務完成規則。
- 進入 `task_filters`。
- 暗示火印正式合成、啟用或聖物效果已開放。

## 12. Feedback 與 Empty State

底部中央區是 NPC guidance / operation feedback bar。

```text
GuildFeedbackMessage
- tone
- speaker
- text
- related_task_id
- severity
```

建議 `severity`：

- `info`
- `success`
- `warning`
- `error`

常見訊息：

- 接待員提示目前委託板用途。
- 任務尚未完成的原因。
- 任務可回報提示。
- 回報成功。
- 任務已完成。
- 三枚火印碎片可詢問諾亞。

空狀態：

```text
GuildEmptyState
- title
- message
- suggested_action
```

例如：

- 目前沒有可顯示的已解鎖委託。
- 請先前往迷宮取得回報素材。
- 目前沒有可回報的委託。

## 13. Guild UIAction V1

通用 action 仍沿用 `gui-screen-map.md` 的語意，但 V1 只需要最小子集：

- `confirm`
- `cancel`
- `back`
- `open_detail`
- `close_detail`
- `select_item`
- `select_filter`

Guild-specific action：

| Action ID | 用途 | 備註 |
|---|---|---|
| `submit_quest` | 回報任務 | 對應條件已滿足的任務。 |
| `open_story_hint` | 查看主線詢問入口 | 用於三枚火印碎片後詢問諾亞。 |
| `select_filter` | 切換 UI-only 任務篩選 | 不寫入 save/state。 |
| `view_quest_detail` | 查看任務詳情 | 可映射到 `open_detail`。 |
| `view_reward_detail` | 查看報酬詳情 | V1 可不做獨立 action。 |
| `view_condition_detail` | 查看條件說明 | V1 可不做獨立 action。 |
| `back_to_town_hub` | 返回 Town Hub | 可映射到通用 `back`。 |
| `unavailable` | 不可操作狀態 | 用於條件不足、已完成或無選取。 |

V1 明確移除：

- `accept_quest`
- `sell_material`
- `next_tab`
- `previous_tab`

`UIActionItem` 建議欄位：

```text
UIActionItem
- action_id
- label
- description
- enabled
- disabled_reason
- payload
- visual_role
```

`visual_role` 建議值：

- `primary`
- `secondary`
- `list_select`
- `inline`

V1 Guild Screen 右下只應有一個 `primary` action。

## 14. Primary Action V1 決策規則

依選中 row 狀態決定右下 action：

| Selected row status | Primary action | Enabled | Disabled reason |
|---|---|---|---|
| `ready_to_submit` | `submit_quest` | true | none |
| `requirements_missing` | `unavailable` | false | 顯示尚未滿足的條件 |
| `completed` | `unavailable` | false | `這個任務已完成` |
| `story_hint` | `open_story_hint` | true | none |
| 無選取 | `unavailable` | false | `請先選擇委託` |

V1 不存在：

- `accept_quest`
- `available`
- `active`
- `ready_to_turn_in`

## 15. 與目前 CLI 概念的對應

此文件不要求讀或改 runtime，但 model 可對應現有 CLI 概念：

| GUI model 概念 | 目前 CLI / gameplay 概念 |
|---|---|
| `GuildScreenModel` | `guild_menu()` 的委託瀏覽與火印詢問入口概念 |
| `task_filters` | UI-only 篩選；由已解鎖任務、`quest_ready()` 與 `completed_quests` 推導 |
| `task_rows` | `guild_quest_menu()` 中已解鎖的 `QUESTS` 清單，套用 `selected_filter_id` 後顯示 |
| `story_hint_card` | `can_ask_fire_mark_guild_inquiry(state)` 成立時的詢問入口 |
| `GuildTaskDetail` | `show_or_complete_quest()` 顯示的任務標題、委託人與描述 |
| `GuildConditionRow` | `QUESTS[quest_id]["turn_in"]` + `state.inventory` / `state.flags` |
| `GuildRewardSummary` | `QUESTS[quest_id]["reward"]` 的 gold、items、guild |
| `feedback_message` | 工會接待員提示、條件不足或回報結果 |
| `primary_action` | 回報任務、查看火印詢問或不可操作 |

工會素材收購目前存在於 CLI，但不納入 Guild Screen V1。若未來要 GUI 化，應另開 Guild Buyback / Exchange screen 或 Facility variant。

未來若要做 runtime experiment，應先 read-only 對照 `guild_menu()`，再決定是否只抽 model builder。不要在同一輪改任務規則。

## 16. Dynamic Text Policy

以下內容必須由 render layer 動態輸出：

- screen title、subtitle。
- 任務名稱、委託人、任務描述。
- 報酬名稱、數量、金幣、工會積分。
- 條件名稱、需求數量、目前數量、狀態。
- filter label。
- 火印詢問 card label。
- 接待員提示、feedback、錯誤訊息。
- primary / secondary action label。
- disabled reason。

V1 延後的動態欄位：

- 任務類型。
- 任務地點。
- 建議等級。

可以在圖片中存在：

- 無語意依賴的羊皮紙、木材、黃銅、旗幟、指南針、徽記、櫃台、光影。
- 不需讀取的裝飾性符號。
- 接待員或工會場景，但不得承載動態資訊。

## 17. 第一版 Demo Scope

建議 V1 只做：

- 顯示已解鎖任務列表。
- 顯示 UI-only task filters：全部委託、可回報、已完成。
- 顯示三枚火印碎片後的諾亞詢問 `story_hint_card`。
- 選中任務。
- 顯示任務詳情。
- 顯示報酬摘要。
- 顯示達成 / 回報條件檢查。
- 顯示底部接待員提示。
- 依狀態顯示右下單一主要 action：`submit_quest`、`open_story_hint` 或 `unavailable`。

暫不做：

- 接任務系統。
- `active_quests`。
- `category_tabs` / sections。
- 可接任務 / 進行中任務這類生命週期 tab。
- 任務地點、任務類型、建議等級 adapter。
- 完整工會積分或聲望系統。
- 完整任務歷史。
- 多層工會子頁。
- 複雜篩選與排序。
- 批量回報。
- 任務地圖自由導航。
- 工會素材收購 GUI。
- 正式 runtime implementation。

## 18. Open Questions

- 三枚火印碎片詢問 card 未來是否升級成 Story / Journal Screen？
- 工會素材收購未來是否作為 Guild Buyback / Exchange screen，或併入廣義 Facility template？
- 若未來要顯示 `location_label`、`recommended_level`、`task_type`，應由 quest data 正式提供，還是由獨立 UI adapter mapping 提供？
- 任務完成後是否長期保留在同一列表，或未來另做歷史 / completed view？

## 19. 下一步

建議下一步仍保持 markdown-only：

1. 用此 V1 model 更新 Guild Screen review checklist。
2. 或針對 Guild Screen 做 UI-2 / Rich wireframe 規劃，不選平台、不改 runtime。
3. 若未來要實作，先做最小 `build_guild_screen_model(state, selected_filter_id, selected_task)` 規劃，不改任務規則、不改 save/schema。
