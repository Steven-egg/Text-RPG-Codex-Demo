# Town Hub Visual Mockup Prompt Review V1

用途：正式評估 `gui-town-hub-visual-mockup-prompt-draft.md` 是否足以作為 Town Hub V1 visual mockup candidate 的輸入。此文件只做 markdown-only review，不生成新圖、不選 GUI framework、不啟動 asset pipeline。

## 0. Review Metadata

```text
review_target: 01_content/gui-town-hub-visual-mockup-prompt-draft.md
review_date: 2026-05-19
reviewer: Codex
result: pass_with_notes
```

審查依據：

- `01_content/gui-town-hub-visual-mockup-prompt-draft.md`
- `01_content/gui-town-hub-review-checklist.md`
- `01_content/gui-town-hub-ui2-wireframe-review-v1.md`

## 1. Summary

此 prompt draft 可作為 Town Hub V1 visual mockup candidate 的輸入。它已明確保留 Town Hub 作為「艾爾姆城鎮場景式 facility hub」的方向，並要求圖像只提供場景、建築入口、safe areas 與 badge slots，不把 UI 文字或 gameplay 資料烘進圖片。

審查結論為 `pass_with_notes`。目前沒有 blocking issue，但在真正生成 candidate 前，仍建議保留幾個小決策：

- 工坊是單一建築加二級選擇，還是同建築雙入口。
- `open_character` / `open_inventory` 仍應只視為暫時 global actions。
- `storage` 是獨立小建築，還是工會旁次級入口。
- `temple` 與 `relic_preview` 是否視覺相鄰。

## 2. Checklist Result

```text
model_fit:
- pass

scene_hub_fit:
- pass

facility_node_fit:
- pass_with_notes

badge_discipline:
- pass

dynamic_text_safety:
- pass

asset_governance:
- pass

gameplay_safety:
- pass
```

## 3. Boundary Check

- [x] 沒有要求修改 runtime、data、schema、save 或 combat formula。
- [x] 沒有要求重構 `03_engine/engine/game.py`。
- [x] 沒有選定 pygame / HTML / Unity / WebView。
- [x] 沒有生成新圖。
- [x] 沒有啟動正式 asset pipeline。
- [x] 沒有把 reference image 當成 runtime asset。
- [x] 沒有把 mockup 反推 gameplay 規則。
- [x] 沒有新增城鎮自由行走。
- [x] 沒有新增 NPC 對話系統。
- [x] 沒有新增通知中心、已讀狀態或 notification schema。
- [x] 沒有新增 save 欄位保存 hover、focus 或 `selected_facility_id`。
- [x] 沒有刪除 runtime 目前已有的設施入口。
- [x] 明確禁止把固定中文、資源數值、badge 或 action label 畫死在圖片中。

## 4. Main Strengths

- prompt 明確要求 Town Hub 是場景式 facility hub，不是純列表、自由行走城鎮或 world map。
- prompt 把圖像定位為 visual reference mockup only，不是 runtime asset。
- `facility_nodes` 的主要入口都有覆蓋，包含原 mockup 缺漏的 `magic_shop`、`temple`、`storage`。
- 對 `workshop` 採保守策略：允許單一建築，但保留 `iron_workshop` / `armor_workshop` 的後續分流可能。
- dynamic text safety 足夠明確，要求所有 UI 文字由 render layer 動態輸出。
- safe areas 覆蓋 title / subtitle、resource strip、town guidance、world map navigation、global actions 與 badge slots。
- badge 規則保持少量、高價值，不導向通知中心。
- tone and style 延續既有「溫暖但危險的邊境城鎮」方向。

## 5. Model Fit

```text
model_fit: pass
```

prompt 可支援 `TownHubScreenModel` 的主要區塊：

- `title`
- `subtitle`
- `scene`
- `resource_strip`
- `town_guidance`
- `facility_nodes`
- `selected_facility_id`
- `global_actions`

`result_message` 未被特別要求，但 Town Hub V1 中仍屬 optional，不構成問題。

## 6. Scene Hub Fit

```text
scene_hub_fit: pass
```

prompt 要求 compact RPG town hub、central plaza、stone paths、building entrances、signboards、banners 與 distant hills，能延續 Town Hub mockup V1 的場景式 identity。

通過點：

- 明確禁止 free-roam town。
- 明確禁止 world map 誤讀。
- 明確要求 facility nodes 可被選取。
- 沒有要求產出 facility 內部流程。

## 7. Facility Node Fit

```text
facility_node_fit: pass_with_notes
```

已覆蓋：

- `guild`
- `inn`
- `travel_shop`
- `workshop`
- `synthesis`
- `relic_preview`
- `magic_shop`
- `temple`
- `storage`

notes：

- `workshop` 目前仍是視覺合併策略，生成後需確認是否留足二級選擇或雙入口的表現空間。
- `magic_shop`、`temple`、`storage` 允許小建築、邊緣入口或 secondary facility rail，生成後需確認不是被視覺弱化到像裝飾物。
- `world_map` 已被正確描述為 navigation safe area，不是 facility。

## 8. Badge Discipline

```text
badge_discipline: pass
```

prompt 符合少量、高價值 badge 原則：

- 不顯示 notification center。
- 不建立大量 badges。
- 每個 facility node 最多一個可見 badge。
- 只預留 guild、synthesis、temple、storage 等高價值 badge slots。

未發現通知系統膨脹風險。

## 9. Dynamic Text Safety

```text
dynamic_text_safety: pass
```

prompt 明確要求：

- 不烘任何 UI text。
- 不輸出可讀中文、英文、數字、資源值、label、badge text、tooltip、button 或 action name。
- 建築標牌只能使用抽象符號、空白招牌或不可讀裝飾 glyphs。
- 所有 UI 文字後續由 render layer 疊加。
- 所有 text-safe regions 需要留白與足夠對比。

這已足以回應前一輪 review 中的 dynamic text concern。

## 10. Asset Governance

```text
asset_governance: pass
```

- prompt draft 是 markdown-only。
- 沒有生成 image。
- 沒有新增 asset registry entry。
- 沒有正式 asset path。
- 沒有要求 runtime 引用 reference。
- 明確聲明 output intent 是 visual reference mockup only。

若未來真的生成 candidate，再另行記錄來源、用途、檔案位置與 review 結果。

## 11. Gameplay Safety

```text
gameplay_safety: pass
```

prompt 沒有新增或修改 gameplay。

符合：

- 不新增 facility。
- 不刪除 runtime facility。
- 不改設施解鎖條件。
- 不改任務、商店、合成、工坊、魔法書規則。
- 不改火印、聖物或轉職開放狀態。
- 不新增 Town Hub save state。
- 不把 facility 內部流程併入 Town Hub 主畫面。

## 12. Blocking Issues

```text
blocking_issues:
- none
```

沒有阻擋 prompt draft 作為後續 visual mockup candidate 輸入的問題。

## 13. Follow-up Notes

生成 candidate 前可以先保留，不必現在解決：

1. 工坊入口策略：單一建築 + 二級選擇，或鐵刃 / 堅甲雙入口。
2. `open_character` / `open_inventory` 仍只作為現階段 global action，不定為最終 navigation。
3. `storage` 若放在工會旁，需保留可辨識的入口語意。
4. `temple` 若與 `relic_preview` 相鄰，需避免讓兩者誤讀成同一 facility。

## 14. Recommended Next Step

建議下一步有兩種安全選擇：

1. 若仍維持 planning：把本 review 視為 prompt draft gate，暫停在 markdown-only 狀態。
2. 若使用者明確批准生成：使用 `gui-town-hub-visual-mockup-prompt-draft.md` 生成一張 visual mockup candidate，之後再做 candidate review。

目前不建議進入 GUI framework 選型、asset pipeline、runtime builder 或 implementation。

