# Town Hub Programmatic Layout Plan V1

用途：把 Town Hub visual mockup candidate 與 facility node mapping 轉成可操作 GUI 的 programmatic layout plan。此文件只做 markdown-only planning，不選定 pygame / HTML / Unity，也不啟動正式 asset pipeline。

## 0. Status

```text
screen: town_hub
plan_date: 2026-05-19
status: programmatic_layout_plan_only
implementation_status: not_started
asset_pipeline_status: not_started
```

參考：

- `01_content/gui-town-hub-screen-model-draft.md`
- `01_content/gui-town-hub-ui2-wireframe-draft.md`
- `01_content/gui-town-hub-facility-node-mapping-v1.md`
- `01_content/gui-town-hub-visual-mockup-candidate-review-v1.md`

## 1. Boundary

- 不修改 runtime、data、schema、save 或 combat formula。
- 不讀取或改動 `03_engine/engine/game.py`。
- 不選定 pygame / HTML / Unity / WebView。
- 不啟動正式 asset pipeline。
- 不把 visual mockup candidate 視為 runtime asset。
- 不追求 pixel-perfect 還原 mockup。
- 不把圖中建築或 icon 反推成 gameplay SSOT。
- 不把 facility 內部流程塞入 Town Hub 主畫面。

## 2. Layout Goal

Programmatic GUI 的第一版應先證明 Town Hub 可操作，而不是先追求完整美術。

V1 目標：

- 用程式化 layout 呈現 Town Hub 的主要區塊。
- 用 `facility_nodes` 建立可 focus、可 disabled、可開啟的設施入口。
- 由 render layer 動態輸出所有文字。
- 用 placeholder / simple panel / simple icon role 先驗證操作感。
- 保留未來替換為正式美術資產的空間。

## 3. Layout Zones

建議把畫面拆成六個穩定區塊：

```text
TownHubLayout
- header_title_area
- header_resource_strip_area
- scene_facility_node_area
- bottom_world_map_nav_area
- bottom_town_guidance_area
- bottom_global_actions_area
```

### `header_title_area`

用途：

- 顯示 `title`。
- 顯示 `subtitle`。

規則：

- 文字由 render layer 輸出。
- 不依賴背景圖上的固定牌匾文字。
- 需支援中文長詞換行或縮放。

### `header_resource_strip_area`

用途：

- 顯示輕量資源列。
- 例如 name / job / level / HP / MP / gold / optional guild points。

規則：

- 不顯示完整角色狀態頁。
- 數值全部動態渲染。
- 資源列不應壓過場景與 facility nodes。

### `scene_facility_node_area`

用途：

- 呈現所有 `facility_nodes`。
- 支援 selected / hover / focus / disabled / badge。

規則：

- 每個 node 至少有 icon role、label、short description。
- label 與 description 由 render layer 輸出。
- icon 可輔助辨識，但不能取代文字。
- node 位置使用抽象 anchor，不綁死候選圖像素。

### `bottom_world_map_nav_area`

用途：

- 承接 `open_world_map`。

規則：

- 是 navigation，不是 facility。
- 不混入 facility grid。
- 可放在左下或主導航列中，但 V1 先延續左下語意。

### `bottom_town_guidance_area`

用途：

- 顯示 1-2 行 `town_guidance`。
- 承接主線、補給、可回報、低 HP / 無藥水等提示。

規則：

- 不變成完整 quest tracker。
- 不替代 Guild Screen 任務詳情。
- 優先放補給提醒，避免為旅館 / 商店濫加 badge。

### `bottom_global_actions_area`

用途：

- 暫時承接 `open_character` / `open_inventory`。

規則：

- 這是主 hub 相容入口，不代表最終全域 navigation 已定案。
- 不得和 facility node 混淆。
- 不得放入 `buy_item`、`craft_recipe`、`submit_quest` 等 facility 內部 action。

## 4. Facility Node Layout

建議 V1 先使用 3 層視覺優先級：

```text
primary:
- guild
- workshop

secondary:
- inn
- travel_shop
- synthesis
- magic_shop
- temple
- relic_preview
- storage

navigation:
- world_map
```

建議抽象 anchor：

```text
guild: top_center_guild_hall
inn: left_inn
travel_shop: mid_left_market
workshop: right_workshop_group
synthesis: bottom_left_alchemy
magic_shop: right_arcane_shop
temple: bottom_center_temple
relic_preview: bottom_right_archive
storage: far_bottom_right_depot
world_map: bottom_left_navigation
```

單一 node 的 programmatic shape：

```text
TownFacilityNodeView
- bounds / anchor
- icon_role
- label
- short_description
- enabled
- disabled_reason
- badge_slot
- focus_state
- action: open_facility
- payload.facility_id
```

## 5. Focus Order

V1 應支援鍵盤 / controller / mouse hover 的共同模型。

建議 focus order：

```text
guild
inn
travel_shop
workshop
synthesis
magic_shop
temple
relic_preview
storage
open_world_map
open_character
open_inventory
```

備註：

- focus order 不必完全等於畫面座標，但應可預期。
- `world_map` 排在 facility nodes 之後，避免玩家誤以為它是設施。
- `open_character` / `open_inventory` 排在最後，因為目前只是相容 global actions。
- selected state 不寫入 save。

## 6. Action Dispatch Boundary

Town Hub 只 dispatch 高層 action：

```text
open_facility
open_world_map
open_character
open_inventory
back
```

不得在 Town Hub 主畫面 dispatch：

- `buy_item`
- `learn_magic`
- `upgrade_equipment`
- `craft_recipe`
- `submit_quest`
- `sell_material`
- `rest_inn`
- `deposit_item`
- `withdraw_item`

這些屬於 facility screen 或後續 facility flow。

## 7. Disabled State Rules

disabled state 應由 model 提供，不由視覺圖推導。

V1 最小規則：

- `synthesis` 可顯示 `未解鎖` status。
- `storage` 可顯示 `未開啟` status。
- 其他設施預設 enabled，除非現有 runtime 已有明確限制。

disabled reason 呈現策略：

- node 上只放短 status badge。
- 完整原因放在 selected node detail 或 `town_guidance`。
- 不因 disabled state 改 gameplay unlock rule。

## 8. Badge Render Rules

badge 由 render layer 疊加，不使用 candidate 圖中的 icon plaque 當 badge。

最小 badge 優先順序：

```text
guild:
1. 火印線索
2. 可回報

synthesis:
1. 未解鎖

temple:
1. 火印查閱 / 橋接提示

storage:
1. 未開啟
```

規則：

- 每個 node 預設最多一個 badge。
- 多個狀態時依 priority 選最高者。
- 補給提醒優先放 `town_guidance`，不硬加旅館與商店 badge。
- 不新增 notification center。

## 9. Workshop Handling

Programmatic GUI V1 建議採：

```text
visible_node: workshop
visual_group: workshop
on_open:
- show second-level choice, or
- enter a workshop facility screen with iron / armor tabs
```

這樣可保留候選圖的單一大型工坊語意，也不丟失 `iron_workshop` / `armor_workshop` runtime 分流。

暫不建議在 Town Hub 主畫面直接鋪兩個獨立大型工坊 node，除非後續 layout 測試證明不擁擠。

## 10. Programmatic-First Guardrails

此 plan 仍符合 Programmatic GUI → Asset-driven 原則。

守則：

- 先用程式化 layout 驗證資訊與操作。
- 背景可先用 placeholder / flat color / simple scene block。
- icon 可先用 simple symbol 或文字 icon role。
- 所有文字由 render layer 動態輸出。
- hover / focus / selected / disabled / badge 都由程式狀態控制。
- 等可操作 GUI 穩定後，再決定正式 asset 需求。

避免：

- 為了貼合 mockup 像素去扭曲 layout。
- 為了美術圖增刪 runtime facility。
- 把 candidate 圖直接當背景進 runtime。
- 在 programmatic GUI 還沒穩時切正式素材。

## 11. Minimum Interactive Prototype Scope

未來若進入 implementation，最小可操作 Town Hub prototype 應只需要：

- render title / subtitle。
- render resource strip。
- render facility nodes。
- support keyboard / mouse selection。
- show selected node guidance。
- show disabled state for locked node。
- show one badge for guild or synthesis。
- dispatch `open_facility` with `facility_id` payload。
- dispatch `open_world_map`。
- keep character / inventory as temporary global actions。

仍不需要：

- formal background asset。
- final icon set。
- animation。
- facility inner screens。
- asset registry runtime integration。

## 12. Recommended Next Step

下一步建議先做 reference governance：

1. 決定是否把 candidate 複製到 `05_assets/gui_references/town_hub/`。
2. 若複製，只標為 `visual_mockup_candidate` / `reference`。
3. 不把它接入 runtime。
4. 不啟動正式 asset pipeline。

完成 reference 收納後，再進入 GUI framework 選型討論，或先針對 pygame / HTML 各寫一份 implementation tradeoff note。

