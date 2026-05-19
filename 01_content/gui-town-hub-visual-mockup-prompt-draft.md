# Town Hub Visual Mockup Prompt Draft

用途：整理 Town Hub V1 下一張 visual mockup 的 prompt 草稿。此文件只做 markdown-only planning，不生成新圖、不選 GUI framework、不啟動正式 asset pipeline，也不代表 GUI 已開始實作。

## 0. Status

```text
screen: town_hub
draft_date: 2026-05-18
status: prompt_draft_only
generation_status: not_generated
review_basis:
- 01_content/gui-town-hub-screen-model-draft.md
- 01_content/gui-town-hub-mockup-review-v1.md
- 01_content/gui-town-hub-wireframe-plan.md
- 01_content/gui-town-hub-ui2-wireframe-draft.md
- 01_content/gui-town-hub-ui2-wireframe-review-v1.md
```

## 1. Boundary

- 不生成新圖。
- 不修改 runtime、data、schema、save 或 combat formula。
- 不讀取或改動 `03_engine/engine/game.py`。
- 不選定 pygame、HTML、Unity 或 WebView。
- 不啟動正式 asset pipeline。
- 不把 reference image 當作 runtime asset。
- 不把 Town Hub 擴成自由行走城鎮。
- 不把 facility 內部流程塞進 Town Hub 主畫面。
- 不新增 notification schema、save state 或 gameplay rule。

## 2. Visual Goal

Town Hub V1 應維持「艾爾姆城鎮場景式 facility hub」：玩家看到的是可辨識的城鎮廣場與建築入口，而不是純列表、管理後台或大地圖。

畫面要支援 `facility_nodes`，讓 render layer 可以在建築入口上疊出 label、description、badge、focus state 與 disabled reason。背景圖本身只提供場景、建築輪廓、入口位置、光影和安全留白。

## 3. Prompt Draft

以下 prompt 是未執行草稿。除非後續明確批准，不得拿來生成新圖。

```text
Create a visual mockup reference for a fantasy RPG Town Hub screen.

Scene:
- A warm frontier town square called Elm Town, used as a facility hub for adventurers.
- The scene should feel like a compact RPG town hub with clear building entrances, stone paths, signboards, banners, distant hills, and a central plaza.
- The hub is not a free-roam town and not a world map. It is a screen where facility nodes can be selected.
- Keep the composition readable for UI overlays and keyboard/controller focus states.

Required facility entrance zones:
- Adventurers' Guild as a prominent central or upper-middle building entrance.
- Inn as a readable rest facility.
- Travel shop / item shop as a readable supply facility.
- Workshop as one major building group. Leave room for the render layer to later represent Iron Workshop and Armor Workshop either as a secondary choice or two sub-entrances.
- Synthesis / crafting shop as a distinct alchemy or crafting entrance.
- Relic preview / relic investigation area as a distinct research or archive entrance.
- Magic shop, temple, and storage must remain present as facility nodes.

Missing facility entrance strategy:
- Magic shop may appear as a smaller star-lamp or arcane sign entrance near the scene edge.
- Temple may appear as a shrine, chapel, or spire entrance, preferably near the relic investigation area if composition allows.
- Storage may appear as a small warehouse, guild-side depot, or secondary building entrance.
- If space is tight, magic shop / temple / storage may be placed on a secondary facility rail, but they must still read as available facility node slots, not hidden or removed.

UI overlay safe areas:
- Reserve a clean top-left or top-center safe area for the dynamic title and subtitle.
- Reserve a clean top-right safe area for a compact dynamic resource strip, such as name / job / level / HP / MP / gold / optional guild points.
- Reserve a bottom safe area for 1-2 lines of dynamic town guidance.
- Reserve a clear bottom-left navigation safe area for returning to the world map.
- Reserve a small bottom-right safe area for temporary global actions such as character and inventory.
- Reserve small badge slots near selected high-value facility entrances, especially guild, synthesis, temple, and storage.

Dynamic text safety:
- Do not bake any UI text into the image.
- Do not render readable Chinese, English, numbers, resource values, labels, badge text, tooltips, buttons, or action names.
- Building signs may use abstract marks, icons, blank signboards, or unreadable decorative glyphs only.
- All UI text, including title, subtitle, facility labels, short descriptions, resource strip, town guidance, badge labels, disabled reasons, and action labels, will be drawn later by the render layer.
- Leave enough empty space and contrast behind every text-safe region so dynamic text can be overlaid cleanly.

Badge and notification discipline:
- Do not show a notification center.
- Do not create many badges.
- Only reserve subtle slots for a few high-value badges.
- The visual should support at most one visible badge per facility node.

Tone and style:
- Warm but slightly dangerous frontier RPG town.
- Cozy lights, stone roads, practical fantasy buildings, banners, workshop smoke, and adventuring atmosphere.
- Clear isometric or slightly elevated game UI composition is acceptable.
- Avoid a generic mobile city-builder look, busy MMO clutter, or a flat list of buttons.

Output intent:
- This is a visual reference mockup only.
- It is not a runtime asset.
- It should be suitable for later review of layout, safe areas, facility nodes, and UI overlay planning.
```

## 4. Render Layer Text Contract

所有 UI 文字都必須由 render layer 動態輸出，不可烘在圖裡：

- `title`
- `subtitle`
- `resource_strip`
- `town_guidance`
- `facility_nodes.label`
- `facility_nodes.description`
- `facility_nodes.badges`
- `disabled_reason`
- `open_world_map`
- `open_character`
- `open_inventory`

visual mockup 只應提供可疊字的安全區與建築入口視覺語意。

## 5. Facility Node Coverage

必須保留的入口：

- `guild`
- `inn`
- `travel_shop`
- `workshop`
- `synthesis`
- `relic_preview`
- `magic_shop`
- `temple`
- `storage`

`world_map` 是 navigation entry，不是 facility node。

`workshop` 可視覺上合併為單一建築，但不得在 planning 上刪除 `iron_workshop` / `armor_workshop` 的 runtime 分流可能性。

## 6. Review Checklist

後續若此 prompt 被用來生成 candidate mockup，review 時至少確認：

- Town Hub 仍是場景式 facility hub，不是純列表。
- top title / subtitle safe area 可用。
- resource strip safe area 可用且不壓迫場景。
- town guidance safe area 可用且不變成 quest tracker。
- badge slots 少量、高價值、低干擾。
- `magic_shop`、`temple`、`storage` 有明確入口策略。
- 圖中沒有烘入任何可讀 UI 文字。
- 所有文字都能由 render layer 動態疊加。
- 沒有暗示 runtime、data、schema、save 或 gameplay rule 變更。

## 7. Open Questions

- 工坊在 visual mockup 中要維持單一建築加二級選擇，還是同建築雙入口？
- `open_character` / `open_inventory` 是否只保留為暫時 global actions？
- `storage` 最適合獨立建築，還是工會旁次級入口？
- `temple` 與 `relic_preview` 是否應視覺相鄰，以暗示未來成長 / 聖物資訊區？

## 8. Recommended Next Step

先 review 本 prompt draft 是否足夠收斂。若通過，再由使用者明確批准是否生成新的 visual mockup candidate。

