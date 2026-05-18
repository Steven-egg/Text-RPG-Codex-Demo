# GUI Guild Screen Review Checklist

用途：評估 Guild Screen reference、mockup、wireframe 或未來 implementation 是否符合已採納的 visual baseline 與 `GuildScreenModel` V1。此文件只做審查標準，不代表已實作 GUI，也不啟動 asset pipeline。

## 0. 使用時機

使用此 checklist 的情境：

- 評估新的 Guild Screen mockup。
- 評估既有 Guild Screen visual baseline 是否仍符合 model。
- 評估 UI-2 CLI / Rich wireframe 是否符合 Guild Screen V1 結構。
- 未來進入 GUI implementation 前，作為品質門檻。

不需要使用此 checklist 的情境：

- 一般新 session 啟動。
- 非 Guild Screen 的 Facility template 討論。
- runtime gameplay 切片。
- asset registry 例行更新。

## 1. 必讀來源

審查前應先讀：

1. `01_content/gui-planning-index.md`
2. `01_content/gui-guild-screen-visual-baseline.md`
3. `01_content/gui-guild-screen-model-draft.md`
4. `01_content/gui-facility-screen-template.md`
5. `01_content/gui-asset-registry-draft.md`

若審查的是 mockup / generated image，再加讀：

- `01_content/gui-asset-request-schema.md`
- `05_assets/gui_references/README.md`
- `05_assets/gui_references/guild_screen/README.md`

## 2. 審查結果格式

建議用以下四種結論：

| Result | 意義 |
|---|---|
| `pass` | 可作為目前 Guild Screen 方向或下一步輸入。 |
| `pass_with_notes` | 可保留，但需記錄小問題。 |
| `needs_revision` | 方向可用，但需要重做部分 layout / text-safe / model 對應。 |
| `reject_for_guild` | 不適合作為 Guild Screen，可歸檔為歷史或改作其他 screen 參考。 |

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
- [ ] 沒有新增任務、報酬、工會積分、任務歷史或工會管理系統。
- [ ] 沒有新增「接任務」系統或 `active_quests`。
- [ ] 沒有把工會素材收購納入 Guild Screen V1 主視覺。
- [ ] 沒有把固定中文、任務資料、數值或 action label 畫死在圖片中。

若任一項不符合，審查結果至少應為 `needs_revision`。

## 4. Screen Identity

Guild Screen 必須清楚讀成：

```text
Adventurers' Guild / Quest Board
冒險者工會 / 委託板
```

V1 必須清楚服務：

- 已解鎖委託瀏覽。
- 任務需求與報酬查看。
- 條件滿足時提交 / 回報任務。
- 三枚火印碎片後的諾亞詢問入口。

檢查項目：

- [ ] 畫面第一印象是工會 / 委託板，而不是商店、合成屋、倉庫或角色管理頁。
- [ ] 接待員、櫃台、委託板、旗幟、冒險者徽記或類似元素能提供工會識別。
- [ ] 有清楚的 Guild title 區，但 title 文字應由 render layer 動態輸出。
- [ ] 不使用語意不明的資源槽或黑色資訊框干擾主任務區。
- [ ] 不把畫面擴成完整工會管理後台。

## 5. Model 對應檢查

審查目標應能對應 `GuildScreenModel` V1 的主要區塊。

```text
GuildScreenModel
- title / subtitle
- npc
- task_filters
- selected_filter_id
- task_rows
- story_hint_card
- task_detail
- reward_summary
- condition_rows
- feedback_message
- primary_action
- secondary_actions
- empty_state
```

檢查項目：

- [ ] 能看出左側已解鎖任務列表區。
- [ ] 能看出 UI-only task filters：全部委託、可回報、已完成。
- [ ] 能容納三枚火印碎片後的 story hint card；layout 受限時可降級為特殊互動列。
- [ ] 能看出中央任務詳情區。
- [ ] 能看出任務報酬摘要區。
- [ ] 能看出任務達成 / 回報條件檢查區。
- [ ] 能看出底部 feedback / NPC guidance 區。
- [ ] 能看出右下單一主要 action。
- [ ] 能看出返回 Town Hub 的 secondary action。
- [ ] 沒有把多個主要 action 並列成按鈕牆。

## 6. Task Filters

Guild Screen V1 可保留 task filters，但它們只作為 UI-only filter，不代表 gameplay state，也不寫入 save/state/schema。

V1 filter：

- `all`：全部委託。
- `ready_to_submit`：可回報。
- `completed`：已完成。

檢查項目：

- [ ] 使用 `task_filters` 命名，不使用 `category_tabs`。
- [ ] 有 `selected_filter_id` 或等價的目前 filter 狀態。
- [ ] `all` 由已解鎖任務推導。
- [ ] `ready_to_submit` 由 `quest_ready(state, quest_id)` 推導。
- [ ] `completed` 由 `state["completed_quests"]` 推導。
- [ ] filter 只影響可見 `task_rows`，不改任務規則。
- [ ] 沒有出現 `可接任務` tab。
- [ ] 沒有出現 `進行中任務` tab。
- [ ] 沒有用 `available` / `active` 暗示接任務流程。
- [ ] story hint 不做成 tab，不計入 filter 數量。

## 7. Task List

左側任務列表只服務掃描，並顯示套用 `selected_filter_id` 後的任務列。

每列 V1 建議承載：

```text
任務名稱
委託人
任務狀態 marker
```

狀態 marker 限制為：

- `ready_to_submit`：可回報。
- `requirements_missing`：條件不足。
- `completed`：已完成。
檢查項目：

- [ ] 任務列表不承載完整任務描述。
- [ ] 任務列表不承載完整報酬。
- [ ] 任務列表不承載完整完成條件。
- [ ] 任務列表不顯示 `可接`、`接取` 或 `進行中` 作為 gameplay 狀態。
- [ ] row 高度足以承接中文任務名稱。
- [ ] 若任務多，能透過 scroll 或 pagination 解決，而不是壓縮到不可讀。
- [ ] selected row 明確。
- [ ] disabled / unavailable row 有可理解狀態，不只靠顏色。
- [ ] 狀態 icon 是語意輔助，不是唯一資訊來源。

## 7-1. Story Hint Card

三枚火印碎片後的諾亞詢問入口優先用 story hint card 呈現。

檢查項目：

- [ ] story hint card 不寫入 `QUESTS`。
- [ ] story hint card 不計入 `task_filters`。
- [ ] story hint card 顯示條件忠於目前 runtime：`key_fire_mark_shard x3` 且尚未完成 `fire_mark_guild_inquiry_done`。
- [ ] story hint card 的 primary action 是 `open_story_hint`。
- [ ] 若 layout 受限，可降級為特殊互動列，但仍不成為 tab。

## 8. Task Detail

中央任務詳情區應放玩家做決策前需要看的主要資訊。

V1 應支援：

- 任務名稱。
- 委託人。
- 2-4 行中文任務描述。
- 任務目前狀態。
- 可選的 unlock 摘要或備註。

V1 延後：

- 任務類型。
- 任務地點。
- 建議等級。
- 由迷宮 / Boss 推導出的風險提示。

檢查項目：

- [ ] 中央詳情區有清楚中文文字安全區。
- [ ] 背景裝飾不穿插或壓住主要文字區。
- [ ] 任務描述不被塞進左側列表。
- [ ] 任務描述、條件、報酬三者分區清楚。
- [ ] 較長描述有預留 scroll / overflow 策略。
- [ ] 不依賴圖片內文字承載任務內容。
- [ ] 不需要新增 adapter mapping 才能顯示 V1 必要欄位。

## 9. Reward Summary

報酬摘要應與完成 / 回報條件分開。

V1 可支援：

- 金幣。
- 工會積分。
- 道具報酬。
- 解鎖內容摘要。

檢查項目：

- [ ] 報酬摘要不與條件檢查表混在一起。
- [ ] 報酬名稱與數量可由 render layer 動態輸出。
- [ ] 使用 `guild_points` / 工會積分語意，不使用 reputation / 聲望暗示新系統。
- [ ] 沒有報酬時有 readable empty state。
- [ ] 報酬 icon 不取代文字名稱與數量。

## 10. Condition Checklist

任務達成 / 回報條件檢查表應可掃讀。

V1 建議 row：

```text
條件類型 icon
→ 條件名稱
→ 需求數量 / 目前持有數或目前狀態
→ 狀態 marker
```

V1 支援：

- `turn_in_item`：回報素材、物品或裝備。
- `flag_set`：`flag:xxx` 條件，例如 Boss 擊敗 flag。
- `none`：沒有交付需求。

檢查項目：

- [ ] 條件 row 支援中文條件名稱。
- [ ] 條件 row 支援需求數與目前數，或 flag 是否成立。
- [ ] 條件狀態可分辨 `met`、`missing`、`not_applicable`。
- [ ] 不只靠紅綠色判斷條件狀態。
- [ ] 不做過密的大型管理表格。
- [ ] 第一版以 3-5 條條件為合理密度。
- [ ] 條件不足原因能連到 feedback 或 disabled reason。
- [ ] 沒有新增討伐數、探索完成度、前置任務鏈等 V1 外 adapter。

## 11. Feedback Bar

底部中央區是 NPC guidance / operation feedback。

應支援：

- 接待員提示。
- 任務尚未完成原因。
- 任務可回報提示。
- 回報成功。
- 任務已完成提示。
- 三枚火印碎片後的諾亞詢問提示。
- 錯誤或不可用原因。

檢查項目：

- [ ] feedback 區能容納 1-2 行中文。
- [ ] feedback 不被壓縮成過小 label。
- [ ] feedback 不藏在角色對話泡泡或背景裝飾裡。
- [ ] feedback 能承接 disabled reason。
- [ ] feedback 語氣可以保留工會接待員感，但不承載唯一關鍵資料。
- [ ] 不顯示接取成功訊息。
- [ ] 不顯示素材收購結果。

## 12. Primary Action

右下只能有一個主要 action。

V1 狀態對應：

| Selected row status | Primary Action |
|---|---|
| `ready_to_submit` | `submit_quest` |
| `requirements_missing` | `unavailable` |
| `completed` | `unavailable` |
| `story_hint` | `open_story_hint` |
| 無選取 | `unavailable` |

檢查項目：

- [ ] 畫面中只有一個視覺上的 primary action。
- [ ] primary action label 可動態輸出。
- [ ] disabled / unavailable 狀態有明確原因。
- [ ] 返回 Town Hub 是 secondary action，不和 primary action 搶層級。
- [ ] 不新增多個並列主 action。
- [ ] 不出現 `accept_quest`。
- [ ] 不出現素材收購 primary action。

## 13. Dynamic Text Safety

以下必須動態渲染，不可畫死在圖中：

- screen title、subtitle。
- 任務名稱、委託人。
- 任務描述。
- 報酬名稱、數量、金幣、工會積分。
- 條件名稱、需求數量、目前數量、狀態。
- filter label。
- story hint card label。
- 接待員提示、feedback、錯誤訊息。
- primary / secondary action label。
- unavailable / disabled reason。

V1 延後，不應成為 mockup 必要文字區：

- 任務類型。
- 任務地點。
- 建議等級。

檢查項目：

- [ ] 主要文字區是空白 / placeholder / 非語意裝飾，能讓 render layer 疊字。
- [ ] 文字安全區不被高對比紋理干擾。
- [ ] 中文長詞或多行文字不會被固定框線切斷。
- [ ] 圖中若有裝飾性標牌，不承載 gameplay 資訊。
- [ ] 不用假中文、亂碼或不可控文字作為 UI 內容。

## 14. Visual Baseline Fit

應保留：

- 工會接待員與角色互動感。
- 委託板 / 接待櫃台氛圍。
- 羊皮紙、木材、黃銅、藍色工會旗幟、指南針 / 冒險者徽記。
- 左側任務列表 + 中央詳情 + 條件檢查 + 底部 feedback + 右下 action 的層級。

應避免：

- 合成屋 / 商店道具感過重。
- 現代科幻儀表板。
- 過度霓虹或手遊抽卡感。
- 全畫面都同色系到區塊難以辨識。
- 背景漂亮但資訊不可讀。
- UI 看起來像管理後台而不是 RPG 工會。
- 視覺上暗示接任務或任務接取狀態。

## 15. Asset / Reference Governance

- [ ] 審查目標若是圖片，已確認它只是 reference / candidate / baseline。
- [ ] 沒有把圖片放進 runtime path。
- [ ] 沒有要求 `03_engine` 直接引用 reference image。
- [ ] 若是 generated image，來源與用途應記錄在 `gui-asset-registry-draft.md`。
- [ ] 若是 user reference，應標記 `user_reference` 與 `accepted_visual_baseline` 等狀態。
- [ ] 若未來要正式使用圖片，已另列正式 asset path、授權 / 來源紀錄與替換策略需求。

## 16. Gameplay Safety

- [ ] 沒有因畫面需要新增任務。
- [ ] 沒有因畫面需要新增報酬。
- [ ] 沒有因畫面需要新增工會積分系統。
- [ ] 沒有因畫面需要新增接任務流程。
- [ ] 沒有新增 `active_quests` 或 save 欄位。
- [ ] 沒有因畫面需要修改任務完成條件。
- [ ] 沒有因畫面需要修改 boss gate。
- [ ] 沒有因畫面需要修改 save / schema。
- [ ] 沒有把 `story_hint` 當成正式 quest completion 規則。
- [ ] 沒有把素材收購擴成 Guild Screen V1 主視覺或完整工會管理系統。

## 17. UI-2 Wireframe Readiness

若審查目標是 UI-2 / Rich wireframe，額外確認：

- [ ] 每個區塊可以用文字、框線、簡單標記表示。
- [ ] 不需要正式圖片也能驗證 layout。
- [ ] 可用 selected / unavailable / ready_to_submit 狀態。
- [ ] 可映射到同一批 UIAction。
- [ ] 不需要先選 pygame / HTML / Unity。

## 18. UI-3 Mockup Readiness

若審查目標是 UI-3 visual mockup，額外確認：

- [ ] 圖像主要驗證 visual baseline 與 layout，不驗證 gameplay。
- [ ] 圖像沒有大量不可控文字。
- [ ] 圖像有足夠留白給 render layer 疊字。
- [ ] 圖像可以容納 Guild model 的主要區塊。
- [ ] 圖像不需要一次產出 icon set、角色立繪、背景、所有狀態變體。

## 19. Blocking Issues

出現以下任一情況，建議結果為 `needs_revision` 或 `reject_for_guild`：

- 看不出這是 Guild / Quest Board。
- 主要資訊全烘在圖片裡。
- 沒有任務列表。
- 沒有任務詳情區。
- 報酬與條件混在一起，難以掃讀。
- 沒有 feedback / disabled reason 區。
- 出現多個同級 primary actions。
- 出現接任務 / accept quest 作為 V1 核心流程。
- 把素材收購放進 Guild Screen V1 主視覺。
- 中央文字安全區不足。
- 畫面暗到中文文字不可讀。
- 圖像要求修改 gameplay 才能成立。
- 把 reference image 當成 runtime asset。

## 20. Review Summary Template

```text
review_target:
review_date:
reviewer:
result:

model_fit:
- pass / concern / fail

visual_fit:
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

## 21. 下一步

若 checklist 通過，下一步可二選一：

1. 針對 Guild Screen 做一份 UI-2 / Rich wireframe 規劃，不選平台、不改 runtime。
2. 若未來要實作，先做最小 `build_guild_screen_model(state, selected_filter_id, selected_task)` 規劃，不改任務規則、不改 save/schema。
