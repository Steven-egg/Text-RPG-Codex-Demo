# Town Hub Mockup Review V1

用途：正式評估目前 Town Hub visual reference / user mockup 是否可作為 Town Hub V1 screen model 與後續 wireframe 的輸入。此文件只做 review 記錄，不代表已實作 GUI，也不啟動 asset pipeline。

## 0. Review Metadata

```text
review_target: 05_assets/gui_references/town_hub/town_hub_visual_reference_v1_user_mockup.png
review_date: 2026-05-18
reviewer: Codex
result: pass_with_notes
```

審查依據：

- `01_content/gui-town-hub-screen-model-draft.md`
- `01_content/gui-town-hub-review-checklist.md`
- `01_content/gui-ui-direction-brief.md`
- `01_content/gui-screen-map.md`
- `01_content/ui-flow-blueprint.md`

## 1. Summary

此 mockup 可作為 Town Hub V1 的 visual reference / user mockup。它已清楚支撐「艾爾姆城鎮場景式 hub」方向，並能讓後續 `TownHubScreenModel` 以 `facility_nodes` 承接建築入口，而不是退回純列表或 CLI menu。

審查結論為 `pass_with_notes`，原因是目前沒有 blocking issue，但仍需在後續 wireframe / mockup 補強三個資訊層：

- player / resource strip。
- town guidance。
- 少量高價值 facility badge。

這些 notes 不阻擋 screen model 整理，也不需要先重做整張圖。

## 2. Main Strengths

- 場景式 hub identity 明確：第一眼能讀成艾爾姆城鎮，而不是 facility 內頁或管理後台。
- facility 建築入口清楚：工會、旅館、商店、工坊、合成屋、聖物調查所都有可辨識的位置與視覺語意。
- 上方 title / subtitle 的區域穩定，可承接 `title` 與 `subtitle`。
- 左下 `返回世界地圖` 入口清楚，符合 Town Hub 作為 World Map 與 Facility Screen 之間 hub 的定位。
- 建築入口採 icon + label + short description，適合映射成 `facility_nodes`。
- 畫面氛圍符合「溫暖但危險的邊境城鎮」方向：石路、工坊、旅館、城堡、遠山與旗幟能提供 RPG 場景感。
- 沒有把 facility 內部流程塞進 Town Hub 主畫面，符合 V1 範圍。

## 3. Model Fit

```text
model_fit: pass_with_notes
```

已符合：

- `screen_id` 可對應 `town_hub`。
- `title` / `subtitle` 有明確上方位置。
- `scene` 有明確城鎮背景。
- `facility_nodes` 可直接對應建築入口。
- `global_actions` 至少可對應 `open_world_map`。
- `selected_facility_id` 可由 hover / focus / selected building 承接。

需補強：

- `player_summary` / `resource_strip` 尚未呈現。
- `town_guidance` 尚未呈現。
- `facility_nodes.badges` 尚未呈現。
- `global_actions` 中的 `open_character`、`open_inventory` 尚未呈現。

## 4. Facility Node Fit

```text
facility_node_fit: pass_with_notes
```

目前圖面已清楚呈現：

- `guild`
- `inn`
- `travel_shop`
- `workshop` 視覺分組
- `synthesis`
- `relic_preview`
- `world_map` navigation

需要在 screen model 保留，但 mockup 尚未明確呈現：

- `magic_shop`
- `temple`
- `storage`
- `iron_workshop` 與 `armor_workshop` 的 runtime 分流

判斷：

- 這不是 blocking issue，因為此圖是 visual reference，不是最終完整 layout。
- 後續 model 不應因 mockup 少畫部分建築而刪除 runtime 入口。
- 工坊可在視覺上合併為一個 `workshop` 建築，但 model 仍應保留鐵刃 / 堅甲兩個 runtime 入口或二級選擇。
- 缺少的 magic shop、temple、storage 可在未來 wireframe 中以額外 building node、邊緣入口、次級 icon 或展開式 town action 承接。

## 5. Badge Discipline

```text
badge_discipline: pass_with_notes
```

目前圖面沒有過量 badge，這是優點。後續補強時應維持少量、高價值、幫助玩家決策的原則。

建議最小 badge：

- `guild`: `可回報`，來源為 `ready_quest_titles(state)`。
- `guild`: `火印線索`，來源為 `can_ask_fire_mark_guild_inquiry(state)`。
- `synthesis`: `未解鎖`，來源為 `is_unlocked(state, "shop_synthesis_01")`。
- `temple`: 火印橋接或查閱可用時可提示，但不展開正式轉職或火印流程。
- `storage`: 若保留入口，可用 `未開啟` 作 status badge。

不建議：

- 每個設施都加 badge。
- 為商店、工坊、魔法書、合成屋完整計算所有可買 / 可學 / 可強化 / 可製作狀態。
- 建立通知中心、已讀狀態或 notification schema。

## 6. Dynamic Text Safety

```text
dynamic_text_safety: concern
```

目前 mockup 內已有 title、facility label、description 與 action label。作為 reference / user mockup 可以接受，但未來正式 mockup、wireframe 或 implementation 必須確保這些文字由 render layer 動態輸出。

需注意：

- 圖中中文文字只能視為 placeholder / visual direction。
- 未來若使用同類背景圖，建築上的資訊框應保留可疊字安全區。
- title、subtitle、facility label、badge、resource、town guidance、action label 都不可烘在背景圖內。
- 中文長詞需要足夠寬度，不應被固定框線切斷。

## 7. Scene Hub Fit

```text
scene_hub_fit: pass
```

圖面符合 Town Hub 的場景式定位：

- 中央廣場與道路自然連到各建築入口。
- 工會、旅館、商店、工坊等建築具有明確辨識度。
- 左下返回世界地圖不干擾 facility node。
- 畫面不是自由走路操作，也不是完整大地圖。

後續 wireframe 可保留此結構，不需要重做整張圖。

## 8. Asset Governance

```text
asset_governance: pass
```

- 此圖位於 `05_assets/gui_references/town_hub/`，符合 reference 暫存位置。
- 目前標記為 visual reference / user mockup，不是 runtime asset。
- 沒有要求 `03_engine` 直接引用此圖片。
- 沒有啟動正式 asset pipeline。
- 未來若要正式使用，仍需另行處理正式 asset path、來源 / 授權 / 生成參數與替換策略。

## 9. Gameplay Safety

```text
gameplay_safety: pass
```

此 mockup 沒有要求新增 gameplay，也沒有要求改動現有 runtime。

符合：

- 不新增 facility 規則。
- 不改設施解鎖條件。
- 不改任務、商店、合成、工坊、魔法書規則。
- 不改火印、聖物或轉職開放狀態。
- 不新增 Town Hub save state。
- 不把 facility 內部流程併入 Town Hub 主畫面。

需持續防守：

- 不因 mockup 沒畫 magic shop、temple 或 storage 就刪除這些 runtime 入口。
- 不因 mockup 看起來像可點建築，就擴張成自由行走城鎮。

## 10. Blocking Issues

```text
blocking_issues:
- none
```

沒有需要阻擋 Town Hub V1 screen model 的問題。

## 11. Follow-up Notes

後續若要補 mockup，不應重做整張畫面。最小必要調整：

1. 加入低干擾 `resource_strip`。
2. 加入 1-2 行 `town_guidance`。
3. 為少量高價值 facility node 預留 badge 位置。
4. 補足或標註 magic shop、temple、storage 的入口策略。
5. 確保所有 UI 文字可由 render layer 疊上，而不是烘在圖裡。

## 12. Recommended Next Step

建議下一步：

1. 小幅同步 `01_content/gui-screen-map.md`，把 Town Hub 補成場景式 `facility_nodes` hub。
2. 不生成新圖。
3. 不改 runtime。

同步重點應限於：

- Town Hub Purpose。
- Town Hub ScreenModel 補充 `facility_nodes`、`town_guidance`、`resource_strip`。
- Town Hub UIAction 保持 `open_facility`、`open_world_map`、`open_character`、`open_inventory`。

