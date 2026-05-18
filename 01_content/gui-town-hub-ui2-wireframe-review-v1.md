# Town Hub UI-2 Wireframe Review V1

用途：正式評估 `gui-town-hub-ui2-wireframe-draft.md` 是否符合 Town Hub V1 的 UI-2 / Rich wireframe 目標。此文件只做 review 記錄，不代表已實作 GUI，也不啟動 asset pipeline。

## 0. Review Metadata

```text
review_target: 01_content/gui-town-hub-ui2-wireframe-draft.md
review_date: 2026-05-18
reviewer: Codex
result: pass_with_notes
```

審查依據：

- `01_content/gui-town-hub-screen-model-draft.md`
- `01_content/gui-town-hub-review-checklist.md`
- `01_content/gui-town-hub-wireframe-plan.md`
- `01_content/gui-town-hub-mockup-review-v1.md`

## 1. Summary

此 UI-2 markdown wireframe draft 可作為 Town Hub V1 下一步 visual prompt 或 Rich wireframe 的輸入。它已補足 mockup review 中指出的三個資訊層：`resource_strip`、`town_guidance`、少量 high-value badge，並為 `magic_shop`、`temple`、`storage` 提供了入口策略。

審查結論為 `pass_with_notes`。目前沒有 blocking issue，但在進入 visual mockup prompt 前，仍需保留幾個 open questions：

- 工坊是單一建築加二級選擇，還是同建築雙入口。
- `open_character` / `open_inventory` 最終是否移到全域 navigation。
- `storage` 是獨立建築還是工會旁次級入口。
- `temple` 與 `relic_preview` 是否在視覺上相鄰。

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
- pass_with_notes

asset_governance:
- pass

gameplay_safety:
- pass
```

## 3. Main Strengths

- Base layout 清楚分出 header、scene / facility nodes、town guidance、world map entry 與 global actions。
- `resource_strip` 已有位置，且保持輕量，不塞完整角色狀態。
- `town_guidance` 放在底部，能承接主線、補給、可回報提示，不膨脹成 quest tracker。
- facility node 結構有 label、short description、badge、selected / hover / focus 與 disabled reason hook。
- badge 優先級清楚，避免每個 facility 都加通知。
- 狀態變體覆蓋 Default Town、工會火印線索、合成屋未解鎖、低 HP / 無藥水、selected node focus。
- 補足 `magic_shop`、`temple`、`storage` 的次級 facility rail 策略，沒有因 mockup 缺漏而刪除 runtime 入口。
- 明確註記 `open_character` / `open_inventory` 只是現階段主 hub 相容入口。

## 4. Boundary Check

- [x] 沒有要求修改 runtime、data、schema、save 或 combat formula。
- [x] 沒有要求重構 `03_engine/engine/game.py`。
- [x] 沒有選定 pygame / HTML / Unity / WebView。
- [x] 沒有生成新圖。
- [x] 沒有啟動正式 asset pipeline。
- [x] 沒有把 reference image 當成 runtime asset。
- [x] 沒有把 facility 內部流程塞進 Town Hub。
- [x] 沒有建立通知中心或新增通知 schema。
- [x] 沒有新增 Town Hub save state。

## 5. Model Fit

```text
model_fit: pass
```

wireframe 已能對應：

- `title`
- `subtitle`
- `resource_strip`
- `town_guidance`
- `facility_nodes`
- `selected_facility_id`
- `global_actions`

`result_message` 未在草圖中明確呈現，但 V1 已標為 optional，不構成問題。

## 6. Scene Hub Fit

```text
scene_hub_fit: pass
```

wireframe 保留場景式 hub，不是純列表。雖然 markdown 草圖以文字框線呈現，但 layout 仍保留城鎮建築入口與中央場景區。

通過點：

- facility nodes 位於主要 scene 區。
- world map entry 是 navigation，而非一般 facility。
- guidance 與 global actions 放在底部，不遮住主要建築入口。
- 沒有暗示自由行走城鎮或新增探索系統。

## 7. Facility Node Fit

```text
facility_node_fit: pass_with_notes
```

已覆蓋必要 node：

- `guild`
- `inn`
- `travel_shop`
- `workshop` visual group
- `synthesis`
- `relic_preview`
- `magic_shop`
- `temple`
- `storage`
- `world_map` navigation

notes：

- `iron_workshop` / `armor_workshop` 仍需在下一步確定是二級選擇或雙入口。
- `magic_shop`、`temple`、`storage` 目前以次級 rail 補位；visual mockup prompt 應決定是否做成小建築、邊緣入口或更多設施展開區。
- 若未來使用 `更多設施`，不得隱藏火印或主線相關提示。

## 8. Badge Discipline

```text
badge_discipline: pass
```

wireframe 遵守少量、高價值原則：

- 工會火印線索優先於可回報。
- 合成屋未解鎖為 status badge。
- 低 HP / 無藥水使用 town guidance，不硬加旅館與商店 badge。
- 每個 node 預設最多一個 badge。

未發現通知系統膨脹風險。

## 9. Dynamic Text Safety

```text
dynamic_text_safety: pass_with_notes
```

wireframe 已明確標示 `{dynamic}`，並聲明所有 label / description / badge / resource / guidance 都由 render layer 輸出。

notes：

- State variant 中使用具體中文與數值作為示例可以接受，但若轉成 visual mockup prompt，需改寫成 placeholder / dynamic text safe area 語言。
- visual prompt draft 應避免要求圖片生成器產出固定中文 UI 文字。

## 10. Asset Governance

```text
asset_governance: pass
```

- wireframe 是 markdown-only。
- 沒有新增 image。
- 沒有把 reference 放入 runtime path。
- 沒有要求正式 asset registry 或 prompt builder。

## 11. Gameplay Safety

```text
gameplay_safety: pass
```

wireframe 沒有新增 gameplay 規則。

符合：

- 不改設施解鎖。
- 不改任務完成條件。
- 不改商店、合成、工坊、魔法書規則。
- 不改火印、聖物或轉職開放狀態。
- 不新增 save state。
- 不把 Guild Buyback / Exchange 納入 Town Hub V1。

## 12. Blocking Issues

```text
blocking_issues:
- none
```

沒有阻擋後續 visual prompt draft 或 Rich wireframe refinement 的問題。

## 13. Follow-up Notes

進入 visual mockup prompt draft 前，建議先定三個小決策：

1. 工坊入口策略：`workshop` 單一建築 + 二級選擇，或鐵刃 / 堅甲雙入口。
2. `magic_shop`、`temple`、`storage` 的視覺補位策略。
3. `open_character` / `open_inventory` 在 prompt 中只作為暫時 global actions，不把它們定成最終導航。

不需要先做：

- World Map model。
- 正式 asset pipeline。
- runtime builder。
- GUI framework。

## 14. Recommended Next Step

建議下一步：

1. 寫一份 Town Hub visual mockup prompt draft，但不生成新圖。
2. prompt draft 應明確要求：
   - dynamic text safe areas。
   - no baked UI text。
   - resource strip / town guidance / badge slots。
   - magic shop / temple / storage entrance strategy。
   - Town Hub remains facility hub, not free-roam town.

