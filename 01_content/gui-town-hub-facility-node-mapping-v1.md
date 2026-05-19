# Town Hub Facility Node Mapping V1

用途：把第一張 Town Hub visual mockup candidate 中的建築與 UI 區塊，對應到 `TownHubScreenModel.facility_nodes`、navigation 與 global actions。此文件只做 markdown-only planning，不代表已實作 GUI，也不啟動正式 asset pipeline。

## 0. Status

```text
screen: town_hub
mapping_date: 2026-05-19
status: mapping_note_only
candidate_status: visual_mockup_candidate
runtime_status: not_used_by_runtime
```

candidate 目前位置：

```text
C:\Users\user\.codex\generated_images\019e3bba-e6c2-78f0-97e2-59bb0436eaa8\ig_0978a4b347977fd9016a0b9da7c12c8191aa682dbfa91fc510.png
```

## 1. Boundary

- 不修改 runtime、data、schema、save 或 combat formula。
- 不讀取或改動 `03_engine/engine/game.py`。
- 不選定 pygame / HTML / Unity / WebView。
- 不啟動正式 asset pipeline。
- 不把 candidate 視為 runtime asset。
- 不把圖中 icon plaque 視為資料來源。
- 不把圖中建築數量反推為 gameplay 規則。
- 不新增或刪除 runtime facility。
- 不把 hover / focus / selected state 寫入 save。

## 2. Mapping Principle

此 mapping 只建立「視覺入口語意」與 `facility_id` 的對位。正式 GUI 仍應由 programmatic render layer 輸出：

- facility label
- short description
- disabled reason
- badge label
- focus / hover / selected state
- resource strip
- town guidance
- action label

圖中的菱形徽章、盾牌、卷軸、星形與瓶子圖示暫時視為 `icon_role` 或 `visual marker`，不是 `FacilityBadge`。真正 badge 仍由 render layer 依狀態另外疊加。

## 3. Facility Node Mapping

| Visual anchor in candidate | Proposed `facility_id` | Visual role | Runtime / model note | Mapping status |
|---|---|---|---|---|
| Top-center large blue-roof guild hall / castle-like building | `guild` | Main guild entrance | `guild_menu(state)`；承接可回報、火印線索等高價值提示 | clear |
| Left large warm red-roof building | `inn` | Rest / inn entrance | `rest_inn(state)`；補給提醒優先放 town guidance，不預設加 badge | clear |
| Center-left small market building with awning and pouch marker | `travel_shop` | Item / supply shop entrance | `travel_shop(state)`；缺藥水可由 town guidance 提示 | clear |
| Right large smoky industrial building with anvil / armor markers | `workshop` visual group | Workshop building group | 建議採「單一工坊建築 + 二級選擇」；保留 `iron_workshop` / `armor_workshop` runtime 分流 | clear_with_note |
| Bottom-left teal / alchemy building with potion marker and glowing bottles | `synthesis` | Alchemy / crafting entrance | `craft_menu(...)`；可承接合成屋未解鎖 status | clear_with_note |
| Right purple arcane building with star marker | `magic_shop` | Magic shop entrance | `magic_shop(state)`；與 synthesis 的視覺分工清楚 | clear |
| Bottom-center chapel / spire building with star marker | `temple` | Temple / vocation / fire-mark lookup entrance | `temple(state)`；可承接火印橋接或查閱提示 | clear |
| Bottom-right round dome archive / scroll marker building | `relic_preview` | Relic research / archive entrance | `relic_preview_menu(state)`；維持 preview / future growth 語意 | clear |
| Far bottom-right small depot with crates / chest marker | `storage` | Storage / warehouse entrance | `storage_menu(state)`；可承接未開啟 status badge | clear |

## 4. Navigation And Global Areas

| Visual anchor in candidate | Proposed action / model field | Role | Notes |
|---|---|---|---|
| Top-left empty ornate panel | `title` / `subtitle` safe area | Dynamic title area | 只作為 safe area，不烘文字 |
| Top-right horizontal ornate strip with resource icons | `resource_strip` safe area | Dynamic resource strip | 可承接 name / job / level / HP / MP / gold / optional guild points |
| Bottom-center empty ornate panel | `town_guidance` safe area | Dynamic guidance | 承接 1-2 行主線、補給、可回報提示 |
| Bottom-left compass panel | `open_world_map` | Navigation entry | 是 navigation，不是 facility node |
| Bottom-right shield panel | `open_character` / `open_inventory` temporary global actions | Current hub compatibility actions | 暫時承接 global actions；未定為最終 navigation |

## 5. Recommended Programmatic Interpretation

建議 Programmatic GUI 不照抄 candidate 的像素，而是抽成下列 layout zones：

```text
TownHubLayout
- header_title_area
- header_resource_strip_area
- scene_facility_node_area
- bottom_world_map_nav_area
- bottom_town_guidance_area
- bottom_global_actions_area
```

`facility_nodes` 可使用抽象 anchor，而不是固定座標：

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

## 6. Workshop Strategy

candidate 的工坊是一個很強的單一大型建築，因此目前建議：

```text
visual_group: workshop
primary visible node: workshop
secondary choices:
- iron_workshop
- armor_workshop
```

這表示 programmatic GUI 可以先讓玩家選中 `workshop`，再用 selected detail、popover 或下一層 facility screen 承接鐵刃 / 堅甲分流。若未來要改成雙入口，這張圖右側工坊已有 anvil / armor 兩個視覺 marker，可支援相鄰 sub-node。

## 7. Badge Placement Rules

candidate 已有很多 icon plaque，為避免語意混淆：

- icon plaque = facility marker / `icon_role`
- status badge = render layer 額外疊加
- notification badge = render layer 額外疊加

建議 badge slots：

| Facility | Badge slot note |
|---|---|
| `guild` | 建築入口或 guild marker 旁，顯示 `火印線索` 或 `可回報` |
| `synthesis` | alchemy entrance 旁，顯示 `未解鎖` |
| `temple` | temple entrance 旁，顯示火印查閱 / 橋接提示 |
| `storage` | depot 入口旁，顯示 `未開啟` |

其他設施預設不放 badge。低 HP、無藥水、補給建議優先進 `town_guidance`。

## 8. Dynamic Text Safety

candidate 通過 dynamic text safety，因為圖中沒有可讀 UI 文字。後續 programmatic GUI 必須維持：

- 圖像不提供文字資料。
- 圖像不提供 gameplay 狀態。
- label / description / action text 都由 render layer 輸出。
- 中文長詞需要留在 overlay layer 處理，不依賴圖中的固定牌匾。

## 9. Mapping Notes

- `synthesis` 建議對應 bottom-left alchemy building，而不是 right purple magic shop；這樣可把合成與魔法商店分清楚。
- `magic_shop` 建議對應 right purple arcane building。
- `relic_preview` 建議對應 bottom-right dome/archive building，而 `temple` 對應 bottom-center chapel/spire building。
- `storage` 建議對應 far bottom-right depot / crate area，不依附 guild，以免和 guild action 混淆。
- `world_map` 只對應 bottom-left compass navigation，不列入 facility grid。

## 10. Recommended Next Step

下一步建議撰寫 Town Hub programmatic layout plan，將上述 mapping 轉成可操作 GUI 的 layout zones、focus order、badge render rules、disabled render rules 與 action dispatch 邊界。

此後才回頭決定是否把 candidate 複製進 `05_assets/gui_references/town_hub/` 作為 reference candidate；那仍屬於 reference governance，不是正式 asset pipeline。

