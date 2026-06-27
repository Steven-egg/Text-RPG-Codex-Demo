# GUI Town Hub Review Checklist

用途：評估 Town Hub reference、mockup、wireframe 或未來 implementation 是否符合 Town Hub V1 的場景式 hub 方向與 `TownHubScreenModel`。此文件只做審查標準，不代表已實作 GUI，也不啟動 asset pipeline。

## 0. 使用時機

使用此 checklist 的情境：

- 評估新的 Town Hub mockup。
- 評估既有 Town Hub visual reference 是否仍符合 model。
- 評估 UI-2 CLI / Rich wireframe 是否符合 Town Hub V1 結構。
- 未來進入 GUI implementation 前，作為品質門檻。

不需要使用此 checklist 的情境：

- 一般新 session 啟動。
- 非 Town Hub 的 Facility Screen 討論。
- Guild Screen V1 內部語意討論。
- runtime gameplay 切片。
- asset registry 例行更新。

## 1. 必讀來源

審查前應先讀：

1. `01_content/gui-planning-index.md`
2. `01_content/gui-ui-direction-brief.md`
3. `01_content/gui-screen-map.md`
4. `01_content/ui-flow-blueprint.md`
5. `01_content/gui-town-hub-screen-model-draft.md`

若審查的是 mockup / generated image，再加讀：

- `01_content/gui-asset-request-schema.md`
- `01_content/gui-asset-registry-draft.md`
- `05_assets/gui_references/README.md`
- `05_assets/gui_references/town_hub/`

## 2. 審查結果格式

建議用以下四種結論：

| Result | 意義 |
|---|---|
| `pass` | 可作為目前 Town Hub 方向或下一步輸入。 |
| `pass_with_notes` | 可保留，但需記錄小問題。 |
| `needs_revision` | 方向可用，但需要調整 layout、text-safe、badge 或 model 對應。 |
| `reject_for_town_hub` | 不適合作為 Town Hub，可歸檔為歷史或改作其他 screen 參考。 |

建議每次審查至少記錄：

```text
review_target:
review_date:
reviewer:
result:
main_strengths:
blocking_issues:
follow_up:
```

## 3. 邊界檢查

- [ ] 沒有要求修改 runtime、data、schema、save 或 combat formula。
- [ ] 沒有要求重構 `03_engine/engine/game.py`。
- [ ] 沒有選定 pygame / HTML / Unity / WebView。
- [ ] 沒有啟動正式 asset pipeline。
- [ ] 沒有把 reference image 當成 runtime asset。
- [ ] 沒有把 mockup 反推 gameplay 規則。
- [ ] 沒有新增城鎮自由行走。
- [ ] 沒有新增 NPC 對話系統。
- [ ] 沒有新增通知中心、已讀狀態或 notification schema。
- [ ] 沒有新增 save 欄位保存 hover、focus 或 `selected_facility_id`。
- [ ] 沒有刪除 runtime 目前已有的設施入口。
- [ ] 沒有把固定中文、資源數值、badge 或 action label 畫死在圖片中。

若任一項不符合，審查結果至少應為 `needs_revision`。

## 4. Screen Identity

Town Hub 必須清楚讀成：

```text
艾爾姆城鎮 / 城鎮設施入口 hub
```

V1 必須服務：

- 看見城鎮與主要設施入口。
- 回到 World Map。
- 掃讀玩家資源與下一步提示。
- 看見少量會影響決策的 facility 狀態。
- 進入 facility，但不處理 facility 內部流程。

檢查項目：

- [ ] 第一印象是城鎮場景，不是純列表、管理後台或商店內頁。
- [ ] facility 以建築、場景熱點或相近方式呈現。
- [ ] 有清楚的 Town title / subtitle 區，但文字由 render layer 動態輸出。
- [ ] `open_world_map` 入口清楚可見。
- [ ] 不把畫面擴成自由行走城鎮或大地圖探索。
- [ ] 不把任一 facility 的內部 list-detail-confirm 流程放進 Town Hub 主畫面。

## 5. Model 對應檢查

審查目標應能對應 `TownHubScreenModel` V1 的主要區塊。

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

檢查項目：

- [ ] 能看出 title / subtitle 的位置。
- [ ] 能看出場景背景或局部城鎮背景。
- [ ] 能容納玩家摘要或資源列。
- [ ] 能容納 1-2 條 town guidance。
- [ ] 能容納多個 facility node。
- [ ] 能表達 selected / hover / focus 狀態。
- [ ] 能容納 global actions：返回世界地圖、角色、背包。
- [ ] 不需要新增 gameplay data 才能顯示 V1 必要欄位。

## 6. Facility Nodes

Town Hub V1 使用 `facility_nodes` 承接場景式入口，不預設為純列表。

V1 至少應能承接：

- `guild`
- `inn`
- `iron_workshop`
- `armor_workshop`
- `travel_shop`
- `synthesis`
- `magic_shop`
- `temple`
- `relic_preview`
- `storage`
- `world_map` navigation

檢查項目：

- [ ] 每個 node 有清楚 label 與用途提示。
- [ ] 每個 node 的 label / description 可由 render layer 動態輸出。
- [ ] node 可有 icon，但 icon 不是唯一資訊來源。
- [ ] node 支援 `enabled` / `disabled_reason`。
- [ ] node 支援少量 `badges`。
- [ ] `visual_anchor` 不綁死為唯一像素座標；不同 render layer 可重排。
- [ ] 工坊若視覺上合併成一棟建築，仍不丟失鐵刃 / 堅甲兩個 runtime 入口。
- [ ] `world_map` 是 navigation，不被誤當成 facility。
- [ ] 不把 facility node 擴張成各設施內部項目清單。

## 7. Player Summary / Resource Strip

Town Hub 應讓玩家快速知道目前狀態，但 resource strip 不應壓過場景與 facility node。

V1 可支援：

- 角色名稱。
- 職業與等級。
- HP / MP。
- 金幣。
- 工會積分或 EXP 的輕量摘要。

檢查項目：

- [ ] resource strip 有穩定位置。
- [ ] resource strip 不遮住主要 facility node。
- [ ] HP / MP / gold 等數值可動態渲染。
- [ ] 不要求新增新的資源類型。
- [ ] 不把完整角色狀態頁塞進 Town Hub。

## 8. Town Guidance

Town guidance 用來提供下一步方向，不是完整任務列表。

V1 可支援：

- 主線提示。
- 工會可回報提示。
- 火印下一步提示。
- 旅館或補給提醒。

檢查項目：

- [ ] guidance 區能容納 1-2 行中文。
- [ ] guidance 不被藏在背景招牌或裝飾內。
- [ ] guidance 可對應 `next_step_hint(state)` / `town_hint_lines(state)`。
- [ ] guidance 不取代 Guild Screen 的任務詳情。
- [ ] guidance 不膨脹成完整 quest tracker。

## 9. Badge 規則

Town Hub badge 只服務決策，不服務視覺熱鬧。

建議 badge 型別：

- `notification`：有新事情可處理，例如工會可回報、火印線索。
- `status`：入口狀態，例如合成屋未解鎖、倉庫未開啟。

檢查項目：

- [ ] 工會最多只顯示高價值通知，例如 `可回報`、`火印線索`。
- [ ] 合成屋可顯示 `未解鎖`。
- [ ] 神殿可在火印橋接或查閱可用時提示，但不展開正式轉職或火印流程。
- [ ] 缺藥水等補給提醒優先放在 town guidance，不一定要做商店 badge。
- [ ] 沒有每個 facility 都為了熱鬧而加 badge。
- [ ] badge 不只靠顏色傳達語意。
- [ ] badge label 可動態輸出。
- [ ] 沒有新增通知中心、已讀狀態或通知歷史。

## 10. UIAction

Town Hub V1 應使用語意 action，不綁定鍵盤、滑鼠或觸控。

V1 action：

- `open_facility`
- `open_world_map`
- `open_character`
- `open_inventory`
- `back`

檢查項目：

- [ ] 點選 facility node 對應 `open_facility`。
- [ ] 返回世界地圖對應 `open_world_map`。
- [ ] 角色與背包入口是 global action，不是 facility。
- [ ] disabled node 有清楚 `disabled_reason`。
- [ ] 不在 Town Hub 主畫面加入 `buy_item`、`craft_recipe`、`submit_quest`、`sell_material` 等 facility 內部 action。
- [ ] 不把 Guild Screen 的 `submit_quest` 或 `open_story_hint` 提升成 Town Hub primary action。

## 11. Dynamic Text Safety

以下必須動態渲染，不可畫死在圖中：

- screen title、subtitle。
- facility label、description。
- badge label。
- player summary、HP、MP、gold、EXP、guild points。
- town guidance。
- disabled reason。
- action label。
- selected / hover / focus 狀態文字。
- result message。

可以畫進圖片的內容：

- 城鎮建築、道路、天空、山景、旗幟、燈火。
- 無語意依賴的紋理、符號、印記、邊框。
- 不需讀取的裝飾性標牌。

檢查項目：

- [ ] 主要文字區有留白或可疊字區。
- [ ] 背景紋理不干擾中文可讀性。
- [ ] 中文長詞不會被固定框線切斷。
- [ ] mockup 若出現文字，應視為 placeholder，而非 gameplay 資料來源。
- [ ] 不用假中文、亂碼或不可控文字作為 UI 內容。

## 12. Visual Reference Fit

應保留：

- 溫暖但危險的邊境城鎮感。
- 建築式 facility 入口。
- 城鎮 title / subtitle。
- 返回世界地圖入口。
- 清楚、可掃讀的互動熱點。
- 暖木、石路、鐵灰、布旗、黃銅、柔和燈火等城鎮語彙。

應避免：

- 現代科幻儀表板。
- 手遊抽卡式滿版特效。
- 純黑暗硬核奇幻到難以閱讀。
- 所有設施像單層按鈕牆。
- 背景漂亮但入口不可讀。
- 城鎮自由行走暗示太強。
- 把 mockup 中的設施數量反推為 runtime 必須刪減或新增。

## 13. Asset / Reference Governance

- [ ] 審查目標若是圖片，已確認它只是 reference / candidate / baseline。
- [ ] 沒有把圖片放進 runtime path。
- [ ] 沒有要求 `03_engine` 直接引用 reference image。
- [ ] 若是 generated image，來源與用途應記錄在 `gui-asset-registry-draft.md`。
- [ ] 若是 user reference，應標記 `user_mockup` 或 `visual_reference`。
- [ ] 若未來要正式使用圖片，已另列正式 asset path、授權 / 來源紀錄與替換策略需求。

## 14. Gameplay Safety

- [ ] 沒有因畫面需要新增 facility。
- [ ] 沒有因畫面需要刪除 runtime facility。
- [ ] 沒有因畫面需要改設施解鎖條件。
- [ ] 沒有因畫面需要改任務完成條件。
- [ ] 沒有因畫面需要改商店、合成、工坊、魔法書規則。
- [ ] 沒有因畫面需要改火印、聖物或轉職開放狀態。
- [ ] 沒有新增 Town Hub save state。
- [ ] 沒有把 Guild Buyback / Exchange 納入 Town Hub V1。
- [ ] 沒有把 facility 內部流程併入 Town Hub 主畫面。

## 15. UI-2 Wireframe Readiness

若審查目標是 UI-2 / Rich wireframe，額外確認：

- [ ] 每個 facility node 可以用文字、框線、簡單標記表示。
- [ ] 不需要正式圖片也能驗證 layout。
- [ ] 可用 selected / disabled / badge 狀態。
- [ ] 可映射到同一批 UIAction。
- [ ] 不需要先選 pygame / HTML / Unity。

## 16. UI-3 Mockup Readiness

若審查目標是 UI-3 visual mockup，額外確認：

- [ ] 圖像主要驗證場景 hub 與 layout，不驗證 gameplay。
- [ ] 圖像沒有大量不可控文字。
- [ ] 圖像有足夠位置給 render layer 疊字。
- [ ] 圖像能容納 resource strip、town guidance 與少量 badge。
- [ ] 圖像不需要一次產出完整 icon set、所有 facility 內頁或狀態變體。

## 17. Blocking Issues

出現以下任一情況，建議結果為 `needs_revision` 或 `reject_for_town_hub`：

- 看不出這是 Town Hub / 城鎮入口。
- 主要資訊全烘在圖片裡。
- facility 入口不可讀或不可辨識。
- 沒有返回 World Map。
- 沒有空間容納 player/resource strip。
- 沒有空間容納 town guidance。
- badge 過多，像完整通知系統。
- 把各 facility 內部流程塞進 Town Hub。
- 暗示城鎮自由行走或新探索系統。
- 圖像要求修改 runtime gameplay 才能成立。
- 把 reference image 當成 runtime asset。

## 18. Review Summary Template

```text
review_target:
review_date:
reviewer:
result:

model_fit:
- pass / concern / fail

scene_hub_fit:
- pass / concern / fail

facility_node_fit:
- pass / concern / fail

badge_discipline:
- pass / concern / fail

dynamic_text_safety:
- pass / concern / fail

asset_governance:
- pass / concern / fail

gameplay_safety:
- pass / concern / fail

main_strengths:
- ...

blocking_issues:
- ...

recommended_next_step:
- ...
```

## 19. 下一步

若 checklist 通過，下一步可二選一：

1. 小幅同步 `01_content/gui-screen-map.md`，把 Town Hub 補成場景式 `facility_nodes` hub。
2. 針對現有 Town Hub mockup 做一次 review 記錄，不生成新圖、不改 runtime。

