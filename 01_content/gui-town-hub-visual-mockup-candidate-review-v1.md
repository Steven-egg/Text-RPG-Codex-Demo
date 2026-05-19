# Town Hub Visual Mockup Candidate Review V1

用途：正式評估第一張 Town Hub visual mockup candidate 是否符合 Town Hub V1 的場景式 hub 方向。此文件只做 markdown-only review，不代表已實作 GUI，也不啟動正式 asset pipeline。

## 0. Review Metadata

```text
review_target: C:\Users\user\.codex\generated_images\019e3bba-e6c2-78f0-97e2-59bb0436eaa8\ig_0978a4b347977fd9016a0b9da7c12c8191aa682dbfa91fc510.png
review_date: 2026-05-19
reviewer: Codex
user_reaction: 符合期待
result: pass_with_notes
```

審查依據：

- `01_content/gui-town-hub-visual-mockup-prompt-draft.md`
- `01_content/gui-town-hub-visual-mockup-prompt-review-v1.md`
- `01_content/gui-town-hub-review-checklist.md`
- `01_content/gui-town-hub-ui2-wireframe-review-v1.md`

## 1. Summary

此 candidate 可作為 Town Hub V1 的 visual mockup reference。它清楚呈現「艾爾姆城鎮場景式 facility hub」：中央廣場、主要建築入口、工會、旅館、商店、工坊、魔法系設施、神殿、倉庫 / depot 類入口與世界地圖導航區都能一眼辨識。

審查結論為 `pass_with_notes`。目前沒有 blocking issue。主要 notes 是後續若要納入 reference registry，需先確認這張圖仍是 reference / candidate，不是 runtime asset；另外部分設施需要後續由 render layer 和 `facility_nodes` mapping 明確命名。

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
- pass_with_notes

gameplay_safety:
- pass
```

## 3. Main Strengths

- 第一眼明確讀成 fantasy RPG town hub，不是純列表、商店內頁、世界地圖或自由行走城鎮。
- 中央廣場與道路自然連向各建築入口，符合 `facility_nodes` 的場景式 hot spot 方向。
- 上方左側有大面積 title / subtitle safe area。
- 上方右側有 compact resource strip safe area。
- 底部中央有 town guidance safe area。
- 左下角可承接 `open_world_map` navigation。
- 右下角可承接暫時 global actions。
- 沒有任何可讀中文、英文、數字或固定 UI copy。
- 建築入口使用 icon / heraldic marker 而不是文字，符合 render layer 動態疊字要求。
- 畫面氛圍符合「溫暖但危險的邊境城鎮」：暖光、石路、工坊煙囪、遠山與城牆都能支撐 RPG 場景感。

## 4. Boundary Check

- [x] 沒有修改 runtime、data、schema、save 或 combat formula。
- [x] 沒有要求重構 `03_engine/engine/game.py`。
- [x] 沒有選定 pygame / HTML / Unity / WebView。
- [x] 沒有啟動正式 asset pipeline。
- [x] 沒有把 candidate 放進 runtime path。
- [x] 沒有把圖片反推 gameplay 規則。
- [x] 沒有新增城鎮自由行走。
- [x] 沒有新增 NPC 對話系統。
- [x] 沒有新增通知中心或 notification schema。
- [x] 沒有新增 save 欄位保存 hover、focus 或 `selected_facility_id`。
- [x] 沒有刪除 runtime 目前已有的設施入口。
- [x] 沒有把固定中文、資源數值、badge 或 action label 畫死在圖片中。

## 5. Model Fit

```text
model_fit: pass
```

candidate 可支援：

- `title`
- `subtitle`
- `scene`
- `resource_strip`
- `town_guidance`
- `facility_nodes`
- `selected_facility_id`
- `global_actions`

`result_message` 仍未特別呈現，但 V1 中屬 optional，不構成問題。

## 6. Scene Hub Fit

```text
scene_hub_fit: pass
```

場景 hub 表現很強：

- 中央廣場清楚。
- 建築入口環繞廣場。
- 遠景提供城鎮外部世界感，但沒有變成 world map。
- 畫面沒有暗示玩家可在城鎮中自由移動。
- UI 面板與場景互不衝突，適合後續 overlay planning。

## 7. Facility Node Fit

```text
facility_node_fit: pass_with_notes
```

可讀的入口語意：

- `guild`：中央大型建築，可作主要工會入口。
- `inn`：左側暖光紅屋頂建築，可作旅館。
- `travel_shop`：中左小型商店或攤棚，可作補給 / 旅人商店。
- `workshop`：右側煙囪工業建築，可作工坊 visual group。
- `magic_shop`：右側紫色魔法建築，語意清楚。
- `temple`：下方中央尖頂建築，可作神殿入口。
- `storage`：右下箱籠 / 小屋區，可作倉庫或 depot。
- `relic_preview` / research area：下方偏右圓頂書卷建築可承接聖物調查或 archive 類入口。

notes：

- `synthesis` 與 `travel_shop`、`magic_shop` 的視覺分工需要後續由 `facility_nodes` mapping 和 icon role 明確化。
- `workshop` 目前是單一大型建築，適合「單一建築 + 二級選擇」策略；若要鐵刃 / 堅甲雙入口，後續 overlay 需補 sub-choice。
- 每個入口目前已有 icon plaque，後續要確認哪些是 icon role、哪些才是 badge slot。

## 8. Badge Discipline

```text
badge_discipline: pass
```

圖中沒有大量通知，也沒有 notification center。建築上的 icon plaque 比較像 facility icon / marker，不像狀態 badge；後續 render layer 可另外疊加少量 badge。

通過點：

- 沒有每個設施都塞 notification。
- 沒有已讀狀態或通知歷史。
- badge slot 可在 guild、synthesis、temple、storage 附近保留。

## 9. Dynamic Text Safety

```text
dynamic_text_safety: pass
```

candidate 沒有可讀 UI 文字，符合 prompt 要求。

可用 safe areas：

- top-left title / subtitle panel。
- top-right resource strip panel。
- bottom-center town guidance panel。
- bottom-left world map navigation panel。
- bottom-right global action panel。
- 多個建築 marker 周圍可疊 facility labels / badges。

notes：

- 部分面板視覺已經很像 finalized UI chrome，後續 review 應持續把它視為 reference，而不是要求 render layer 照抄。
- 建築 icon 不可取代 label；正式 UI 仍需 render layer 輸出 facility label / description。

## 10. Asset Governance

```text
asset_governance: pass_with_notes
```

目前 candidate 位於 Codex generated image 目錄：

```text
C:\Users\user\.codex\generated_images\019e3bba-e6c2-78f0-97e2-59bb0436eaa8\ig_0978a4b347977fd9016a0b9da7c12c8191aa682dbfa91fc510.png
```

notes：

- 目前不要視為 runtime asset。
- 目前不要直接加入 `03_engine` 或 GUI implementation。
- 若之後要收進 `05_assets/gui_references/town_hub/`，應明確標為 `visual_mockup_candidate` 或 `reference`。
- 若之後要正式使用，仍需另行處理正式 asset path、來源 / 生成參數、授權與替換策略。

## 11. Gameplay Safety

```text
gameplay_safety: pass
```

candidate 沒有要求新增或修改 gameplay。

符合：

- 不新增 facility。
- 不刪除 runtime facility。
- 不改設施解鎖條件。
- 不改任務完成條件。
- 不改商店、合成、工坊、魔法書規則。
- 不改火印、聖物或轉職開放狀態。
- 不新增 Town Hub save state。
- 不把 facility 內部流程併入 Town Hub 主畫面。

## 12. Blocking Issues

```text
blocking_issues:
- none
```

沒有阻擋此 candidate 作為 Town Hub visual reference 的問題。

## 13. Follow-up Notes

後續若要繼續收斂，建議只做 markdown / reference 管理層面的事：

1. 決定是否把此 candidate 複製進 `05_assets/gui_references/town_hub/`，並標記為 reference candidate。
2. 若保留，建立對應的 asset registry draft entry，但仍不得視為 runtime asset。
3. 補一份 facility node mapping note，標示每個畫面入口對應哪個 `facility_id`。
4. 暫不進入 GUI framework 選型或 implementation。

## 14. Recommended Next Step

建議下一步：

1. 若使用者同意，把 candidate 作為 Town Hub visual mockup V1 candidate 留存到 reference 目錄。
2. 同步更新 reference / planning index 或 asset registry draft，僅標為 reference，不啟動正式 asset pipeline。
3. 之後再進行 facility node mapping note，確認圖中入口與 `facility_nodes` 的對位。

