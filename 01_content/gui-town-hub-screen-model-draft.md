# Town Hub Screen Model Draft

用途：整理 Town Hub V1 的 ScreenModel 與 UIAction 邊界，承接目前 `town_menu()` 的 runtime 角色與使用者提供的城鎮場景式 mockup。此文件只做 GUI planning，不代表已實作 GUI，也不代表已選定 render 技術。

## 0. 當前邊界

- 不修改 runtime、data、schema、save 或 combat formula。
- 不重構 `03_engine/engine/game.py`。
- 不選定 pygame / HTML / Unity / WebView。
- 不啟動正式 asset pipeline。
- 不把 reference image 視為 runtime asset。
- 不把 mockup 圖內文字當作資料來源；所有 title、label、badge、hint 與 action text 都必須由 render layer 動態輸出。
- 不重開 Guild Screen V1 的任務 filter、story hint 或 primary action 語意。

## 1. Town Hub V1 定位

Town Hub V1 是「艾爾姆城鎮的設施入口 hub」。它負責讓玩家看見目前可前往的城鎮設施、少量高價值狀態與下一步方向，但不處理各 facility 的內部流程。

目前 runtime 參考：

- `main_loop(state)`：目前 CLI 主選單入口，包含返回城鎮、進入迷宮、背包、存檔等。
- `town_menu(state)`：目前 Town Hub 的最直接參考，列出城鎮設施並呼叫對應 facility。
- `dungeon_menu(state)`：目前迷宮目的地選擇，未來應由 World Map 承接，不屬於 Town Hub 內部。

Town Hub V1 的畫面角色：

- 顯示「艾爾姆城鎮」場景。
- 以建築或場景熱點呈現 facility entry。
- 提供返回 World Map 的明確入口。
- 顯示玩家資源與下一步提示，但不讓資訊層壓過場景。
- 點選 facility 後進入對應 Facility Screen 或目前 runtime 既有流程。

## 2. Visual Reference 吸收方式

使用者提供的 reference：

```text
05_assets/gui_references/town_hub/town_hub_visual_reference_v1_user_mockup.png
```

此圖目前作為 Town Hub 的 visual reference / user mockup，不是最終 layout，也不是 runtime asset。

已採納的結構方向：

- 主畫面是艾爾姆城鎮場景，而不是純 panel list。
- facility 以建築入口呈現，例如工會、旅館、工坊、商店、米菈合成屋、聖物調查所。
- 上方保留 town title 與 subtitle。
- 左下保留 `open_world_map` 入口。
- 每個入口可有 icon、label 與一句短描述。

mockup 尚未明確呈現但 ScreenModel 應保留的資訊層：

- `player_summary` / `resource_strip`：角色、等級、HP/MP、金幣等輕量摘要。
- `town_guidance`：主線提示、可交付任務、旅館或補給提醒。
- 少量高價值 `facility_badges`：只標示會影響玩家決策的狀態。

## 3. ScreenModel 草案

```text
TownHubScreenModel
- screen_id
- title
- subtitle
- scene
- player_summary
- resource_strip
- town_guidance
- facility_nodes
- selected_facility_id
- global_actions
- result_message
```

建議欄位語意：

- `screen_id`：固定為 `town_hub`。
- `title`：例如 `艾爾姆城鎮`。
- `subtitle`：例如 `冒險者的據點與補給中心`。
- `scene`：描述城鎮場景與 reference path，不包含動態文字。
- `player_summary`：單行玩家摘要，可對應目前 `player_summary_line(state)`。
- `resource_strip`：資源列，可對應目前 `player_resource_lines(state)` 的輕量版本。
- `town_guidance`：1-2 條高價值提示，可對應目前 `next_step_hint(state)` / `town_hint_lines(state)`。
- `facility_nodes`：場景中的可互動建築或入口，不預設為純列表。
- `selected_facility_id`：目前 focus / hover / keyboard selection，不應寫入 save。
- `global_actions`：城鎮層級 action，例如返回世界地圖、角色、背包。
- `result_message`：從 facility 返回後的短回饋，V1 可選。

## 4. Facility Node 草案

`facility_nodes` 比 `facility_rows` 更適合 Town Hub，因為目前採用場景式建築入口，而不是純表格或清單。若未來需要跨 render layer 的更中性命名，也可評估 `facility_entries`；本 draft 暫用 `facility_nodes`。

```text
TownFacilityNode
- facility_id
- label
- description
- visual_group
- visual_anchor
- icon_role
- enabled
- disabled_reason
- badges
- primary_action
- payload
```

欄位語意：

- `facility_id`：穩定 id，例如 `guild`、`inn`、`travel_shop`。
- `label`：動態顯示名稱，例如 `工會委託所`。
- `description`：一句用途提示，例如 `接受與回報任務`。
- `visual_group`：視覺分組，例如 `workshop` 可同時承接鐵刃與堅甲工坊。
- `visual_anchor`：抽象位置語意，例如 `center_castle`、`left_inn`，不綁死像素座標。
- `icon_role`：語意 icon，例如 `guild`、`bed`、`hammer`、`shop`、`alchemy`。
- `enabled`：此入口是否可進入。
- `disabled_reason`：不可進入原因，例如合成屋尚未解鎖。
- `badges`：少量狀態或通知。
- `primary_action`：通常為 `open_facility`。
- `payload`：action 所需參數，例如 `{ facility_id: "guild" }`。

## 5. Runtime 對照

| Facility node | Runtime 參考 | V1 顯示定位 | Badge 原則 |
|---|---|---|---|
| `guild` | `guild_menu(state)` | 工會委託所 / 接受與回報任務 | 可回報、火印線索 |
| `inn` | `rest_inn(state)` | 旅館 / 休息恢復 HP/MP | 預設不加，必要時只提示可休息 |
| `iron_workshop` | `iron_workshop(state)` | 鐵刃工坊 / 武器購買與強化 | 預設不加 |
| `armor_workshop` | `armor_workshop(state)` | 堅甲工坊 / 防具購買與強化 | 預設不加 |
| `travel_shop` | `travel_shop(state)` | 旅人小鋪 / 補給與特殊道具 | 預設不加，缺藥水可放在 town guidance |
| `synthesis` | `craft_menu(...)` | 米菈合成屋 / 素材合成與轉換 | 未解鎖 |
| `magic_shop` | `magic_shop(state)` | 星燈魔法商店 / 學習永久技能 | 預設不加 |
| `temple` | `temple(state)` | 轉職神殿 / 轉職與火印查閱 preview | 火印查閱可用時可提示 |
| `relic_preview` | `relic_preview_menu(state)` | 聖物調查 / 未開放聖物線索 | 預設不加或標示 preview |
| `storage` | `storage_menu(state)` | 倉庫 / 非關鍵物品存取 | 未開啟可作狀態 badge |
| `world_map` | future World Map | 返回世界地圖 | navigation，不是 facility |

注意：mockup 可把鐵刃 / 堅甲工坊視覺上合併為同一個「工坊」建築，但 ScreenModel 不應因此丟失 runtime 目前存在的兩個入口。可用 `visual_group: workshop` 讓 render layer 決定呈現成一個建築加二級選擇，或兩個相鄰入口。

## 6. Badge 規則

Town Hub badge 只服務決策，不服務視覺熱鬧。

建議 badge 型別：

```text
FacilityBadge
- badge_id
- label
- kind
- priority
- source
```

- `kind: notification`：有新事情需要處理，例如工會可回報、火印線索。
- `kind: status`：入口狀態，例如合成屋未解鎖、倉庫未開啟。

V1 badge 原則：

- 工會最多可顯示高價值通知：`可回報`、`火印線索`。
- 合成屋可顯示狀態：`未解鎖`。
- 轉職神殿可在火印橋接或查閱可用時顯示提示，但不要展開正式轉職或火印流程。
- 其他設施若沒有強必要，預設不加 badge。
- 不建立完整通知中心、不記錄通知已讀、不新增 notification schema。

可直接對應的來源：

- `ready_quest_titles(state)`：工會可回報。
- `can_ask_fire_mark_guild_inquiry(state)`：工會火印線索。
- `is_unlocked(state, "shop_synthesis_01")`：合成屋是否解鎖。
- `should_show_fire_mark_church_bridge(state)` / `should_show_fire_mark_church_lookup(state)`：神殿火印提示。
- `state["storage_unlocked"]`：倉庫是否開啟。

## 7. UIAction 草案

Town Hub V1 應使用語意 action，不綁定滑鼠、鍵盤或觸控。

```text
TownHubAction
- open_facility
- open_world_map
- open_character
- open_inventory
- back
```

`open_facility` payload 範例：

```text
UIActionItem
- action_id: open_facility
- label: 前往工會
- enabled: true
- disabled_reason: null
- payload:
    facility_id: guild
```

V1 不需要新增 `buy_item`、`craft_recipe`、`submit_quest` 等 facility 內部 action。這些仍屬於各 Facility Screen 或 Guild Screen。

## 8. 可直接取得與應延後

可直接由現有 state / runtime 取得：

- 玩家摘要：`player_summary_line(state)`。
- 玩家資源：`player_resource_lines(state)`。
- 城鎮提示：`next_step_hint(state)`、`town_hint_lines(state)`。
- 工會可回報：`ready_quest_titles(state)`。
- 工會火印線索：`can_ask_fire_mark_guild_inquiry(state)`。
- 合成屋解鎖：`is_unlocked(state, "shop_synthesis_01")`。
- 倉庫狀態：`state["storage_unlocked"]`、`storage_kind_count(state)`、`STORAGE_CAPACITY`。
- 旅館狀態：`state["gold"]`、`state["current_hp"]`、`state["current_mp"]`、`get_stats(state)`。

應先延後：

- 每個商店商品是否可買的完整聚合。
- 每個工坊裝備是否可強化的完整聚合。
- 每本魔法書是否可學的完整聚合。
- 每張合成配方是否可製作的完整聚合。
- Guild Screen 的 task filter、task rows、primary action 與 story hint 細節。
- 工會素材收購 / Exchange 類畫面。
- World Map node model。
- 正式 icon、背景、layout 座標與 asset pipeline。

## 9. V1 不做事項

- 不做城鎮自由行走。
- 不做 NPC 對話系統重做。
- 不做所有 facility 的內部 GUI。
- 不做大型通知系統。
- 不新增 save 欄位保存 hover、focus 或 selected facility。
- 不因 mockup 刪除 runtime 目前已有的設施入口。
- 不因 mockup 新增 runtime 未開放的 gameplay。
- 不把 `main_loop()` / `town_menu()` 重構為正式 screen router。

