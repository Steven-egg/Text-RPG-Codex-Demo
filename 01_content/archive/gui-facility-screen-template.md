# GUI Facility Screen Template Draft

用途：把合成屋 mockup 抽象成 Shop、Forge、Magic Shop、Synthesis 等設施畫面可共用的 UI 模板。此文件只做 GUI 規劃，不代表已開始 GUI 實作、不啟動 asset pipeline、不修改 runtime。

## 0. 邊界

- 不修改 runtime、data、schema、save、combat formula。
- 不重構 `03_engine/engine/game.py`。
- 不選定 pygame / HTML / Unity 或其他 GUI 技術。
- 不新增商品、配方、裝備、魔法書或平衡規則。
- 不把單張 mockup 直接視為最終 UI 架構。
- 不把任何固定文字畫死在圖片裡；設施名稱、列表文字、價格、素材、條件、結果都必須由 render layer 動態輸出。

## 1. 共用模板目標

Facility Screen 的共用模板服務以下設施：

- `facility_synthesis_screen`：米菈合成屋。
- `facility_shop_screen`：旅人小鋪。
- `facility_forge_screen`：鐵刃 / 堅甲工坊。
- `facility_magic_screen`：星燈魔法商店。

共用核心流程：

```text
category
→ item / recipe / service list
→ selected detail
→ requirement / status
→ confirm
→ result feedback
```

這個模板的核心價值不是讓所有設施長得完全一樣，而是讓玩家在每個設施中都能用同一套資訊語法理解「我在看什麼、缺什麼、能做什麼、做完得到什麼」。

## 2. 共用畫面區塊

### Top Region：設施與玩家摘要

用途：
- 動態顯示設施名稱。
- 顯示玩家當前資源摘要。
- 顯示本設施的短目標或提示。

可放內容：
- `screen title`
- `subtitle`
- 金幣
- 背包 / 倉庫相關提示
- 目前選中分類或可處理數量
- 設施短提示

限制：
- 不放長段描述。
- 不放固定烘焙文字。
- 不承載主要決策資訊。

### NPC Region：設施角色互動感

用途：
- 提供設施識別與角色互動感。
- 讓 Shop / Forge / Magic / Synthesis 不只是抽象功能表。

可放內容：
- NPC portrait / bust / character-presence 區。
- 非文字性的情緒、姿勢、工作場景。
- 未來可疊加一小段動態 NPC 提示，但文字不可畫死在圖中。

限制：
- 不壓住主要操作區。
- 不取代 list / detail / requirement 資訊。
- 不為了空間縮到失去角色存在感。
- 若需要挪動，僅允許極輕微調整，不裁切臉部。

### Left Region：分類與列表

用途：
- 放分類 tab / segmented controls。
- 放 item、recipe、equipment、magic book 或 service list。
- 支援 selected、disabled、available、locked 等狀態。

可放內容：
- 分類 tabs。
- 可滾動列表。
- 每列 icon / thumbnail。
- 名稱、摘要、價格、持有數、狀態 badge。

限制：
- 左側列表可以透過滾動解決密度，不要求同屏顯示全部。
- 若中文資訊較多，可以加高 row、減少同屏列數。
- 不把左側列表視為所有詳細資訊的唯一承載區；重點資訊應進 detail。

### Center / Detail Region：選中項目詳情

用途：
- 放玩家做決策前需要看的主要資訊。
- 是 Facility Screen 最重要的中文文字安全區。

可放內容：
- 產出 / 商品 / 裝備 / 魔法書主資訊。
- 效果描述。
- 條件說明。
- 可用職業、等級、持有 / 已裝備狀態。
- 可製作、可購買、可學習、可強化狀態。
- 缺少原因或限制。

限制：
- 需保留清楚的中文文字承載層。
- 背景裝飾不可穿插到主要文字區。
- 不可只有漂亮 icon，而缺少名稱、狀態與條件空間。

### Requirement / Status Region：需求與缺口

用途：
- 告訴玩家為什麼能做或不能做。
- 讓素材、金幣、基底裝備、職業、等級等條件可掃讀。

建議 row 結構：

```text
icon / marker
→ requirement name
→ required count or condition
→ owned count / current state
→ status marker
```

設施差異：
- Synthesis：基底裝備、素材、金幣、最多可製作次數。
- Shop：價格、持有數、解鎖狀態、是否可購買。
- Forge：基底裝備、素材、金幣、完成品能力差異。
- Magic Shop：職業、等級、金幣、素材、已學習狀態、技能 MP。

限制：
- 不應 icon-only。
- 不只靠紅綠色判斷。
- 需能承接中文素材名稱與數量。

### Bottom Region：Action 與 Result Feedback

用途：
- 放主要 action、返回 / 取消，以及結果或不可用原因。

可放內容：
- 左側返回 / 取消。
- 右側確認 / 購買 / 合成 / 強化 / 學習。
- 中央 1-2 行結果提示或 disabled reason。

限制：
- 中央結果訊息區不可壓縮成小 label。
- 按鈕 label 必須動態渲染。
- 結果文字不可藏在角色對話或背景裝飾中。

## 3. 各設施差異

| Facility | 主要列表項 | Detail 重點 | Requirement 重點 | Confirm Action |
|---|---|---|---|---|
| Synthesis | 配方 | 產出、效果、基底裝備 | 素材、金幣、最多可製作次數、缺口 | 合成 |
| Shop | 商品 | 效果、持有數、價格 | 金幣、解鎖狀態、背包限制 | 購買 |
| Forge | 裝備 / 強化項 | 裝備能力、可用職業、完成品差異 | 基底裝備、素材、金幣 | 購買 / 強化 |
| Magic Shop | 魔法書 | 技能效果、MP、可用職業 | 等級、素材、金幣、已學習 | 學習 |

## 4. 共用 UIAction

通用：

- `select_category`
- `select_item`
- `open_detail`
- `close_detail`
- `confirm`
- `cancel`
- `back`

設施專用：

- `craft_recipe`
- `buy_item`
- `upgrade_equipment`
- `learn_magic`

注意：
- UIAction 是 gameplay 語意，不綁定滑鼠、鍵盤、觸控或 CLI 數字輸入。
- 不同 render layer 應映射到同一批 action。

## 5. 共用 ScreenModel 欄位建議

```text
FacilityScreenModel
- screen_id
- facility_id
- title
- subtitle
- npc
- player_summary
- category_tabs
- selected_category_id
- list_rows
- selected_item_id
- detail_sections
- requirement_rows
- primary_action
- secondary_actions
- result_message
- disabled_reason
```

```text
RequirementRow
- id
- icon_id
- label
- required_value
- current_value
- status
- disabled_reason
```

```text
FacilityListRow
- id
- title
- category
- summary
- thumbnail_id
- price
- owned_count
- status
- disabled_reason
```

## 6. V2 Visual Template Rules

未來 V2 prompt 或 mockup 應遵守：

- 保留左側可滾動列表語彙。
- 左側 row 可加高，降低同屏列數以承接中文資訊。
- 保留 NPC portrait 的設施互動感。
- 中央詳情區必須有清楚中文安全區。
- Requirement row 必須支援名稱與數量，不可 icon-only。
- 底部中央結果訊息區必須容納 1-2 行中文。
- 任何固定文字、數字、價格、素材名稱都不可畫死在圖片裡。

## 7. 防止 Mockup 帶歪的規則

- 單張 mockup 只驗證方向，不直接決定 runtime 架構。
- 視覺稿不可新增 gameplay。
- 裝飾不能壓過資訊可讀性。
- NPC 存在感是優點，但不能遮擋核心資訊。
- 左側列表的資訊密度可透過滾動與 row 高度解決，不應過早判定為版面失敗。
- Facility 共用模板不等於所有設施完全同構；各設施仍需保留差異。

## 8. 下一步

下一步可依此模板整理 `gui-facility-synthesis-v2-prompt-draft.md`。若未來批准生成 V2，只生成一張 `facility_synthesis_screen` 候選圖，不擴到 Shop / Forge / Magic Shop。

