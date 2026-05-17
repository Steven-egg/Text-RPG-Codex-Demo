# Facility Synthesis Screen V2 Prompt Draft

用途：把第一張合成屋 mockup 的審查結果與 `gui-facility-screen-template.md` 的共用模板規則，整理成第二版 `facility_synthesis_screen` prompt 草案。此文件不是生成指令；在使用者明確批准前，不生成圖片。

## 0. 邊界

- 只做 V2 prompt draft，不生成圖片。
- 目標仍是單張 `facility_synthesis_screen` UI-3 visual concept。
- 只處理桌面 16:9。
- 不擴到 Shop / Forge / Magic Shop 生成。
- 不啟動正式 asset pipeline。
- 不把候選圖放入 runtime 或 `05_assets`。
- 不修改 runtime、data、schema、save、combat formula。
- 所有文字、數字、配方名稱、素材名稱、價格、按鈕 label 都必須由 render layer 動態輸出。

## 1. Prompt 使用狀態

```yaml
prompt_id: gui_prompt_facility_synthesis_screen_mockup_v2
status: draft
linked_request_id: gui_asset_facility_synthesis_screen_mockup_v0
linked_template: 01_content/gui-facility-screen-template.md
screen_id: facility_synthesis_screen
flow_id: flow_a_town_facility
target_asset_type: screen_mockup
target_role: ui3_visual_concept_v2
target_ratio: "16:9"
generation_allowed_now: false
```

## 2. Positive Prompt Draft V2

以下 prompt 偏英文，方便未來接多數圖像工具；正式使用前仍需人工審查。

```text
Create one desktop 16:9 fantasy RPG GUI visual concept mockup for the Synthesis Screen inside Mila's synthesis house. This is a V2 refinement of the first concept, focused on making the facility screen template more usable for dynamic Chinese UI text.

The scene is a warm frontier alchemy and crafting workshop with practical wooden furniture, parchment UI panels, brass and iron fittings, small crystals, bottles, tools, recipe materials, and soft amber lamplight. Add subtle star-lamp blue accents for the magic synthesis mood. Keep the visual tone warm, handcrafted, readable, and practical.

Preserve the strong character interaction feeling from the first concept. Include a visible portrait or bust area for Mila / the synthesis NPC at a friendly, strong size. Do not shrink the portrait. If more room is needed for the central detail panel, shift the portrait only slightly to the right, without cropping her face and without making her feel detached from the facility.

The layout must clearly communicate a reusable Facility Screen template:
- Top region: empty dynamic screen title area, player resource summary area, and short objective / facility hint area.
- NPC region: visible Mila / NPC portrait or bust, separated from the functional text panels.
- Left region: category tabs or segmented controls above a scrollable recipe list. The list may show fewer, taller rows rather than many dense rows. Selected and disabled row states should be visible using abstract shapes, borders, brightness, or badges only.
- Central detail region: a large, calm recipe detail panel with clearer Chinese text-safe zones. Leave wide blank placeholder areas for recipe output, effect description, missing reason, and selected recipe explanation.
- Material / requirement region: structured rows wide enough to later support material icon, material name, required count, owned count, and status marker. Do not make this section icon-only.
- Bottom region: left back/cancel action area, right confirm/craft action area, and a wide calm center result message area large enough for one to two lines of dynamic Chinese feedback text.

Use abstract placeholder blocks, lines, blank labels, empty bars, and icon-like shapes for all UI text regions. Do not render readable Chinese, English, letters, numbers, item names, recipe names, material names, prices, stats, button labels, dialogue text, or logo text. All text must be imagined as dynamic overlay text added later by the render layer.

Make the category -> recipe list -> detail -> requirements -> confirm -> result pattern immediately understandable. The central detail panel and material requirements section must be more text-safe and less decorative than the first version. Availability states should be distinguishable by shape, border, icon-like abstract marks, row treatment, or panel treatment, not color alone.

Style: restrained fantasy RPG interface, warm wood, parchment, brass, iron gray, soft amber light, subtle blue crystal accents, handcrafted workshop, readable UI hierarchy, desktop game screen visual concept.
```

## 3. Negative Prompt Draft V2

```text
No readable text, no letters, no Chinese characters, no English words, no numbers, no labels, no button text, no recipe names, no item names, no material names, no prices, no stats, no HP or MP numbers, no dialogue text, no logo text.

Do not shrink the NPC portrait. Do not crop Mila's face. Do not push the portrait so far right that only half the face is visible. Do not make the NPC feel disconnected from the facility.

Do not make the material requirement row icon-only. Do not omit space for material names and counts. Do not compress the central detail text-safe zone. Do not compress the bottom result message area into a tiny label.

No clutter behind list, detail, requirement, or result text areas. No decorative objects over the main detail panel. No portrait blocking category, recipe list, detail, requirements, action, or result regions.

No drag-and-drop crafting implication, no batch crafting controls, no selling flow, no new crafting mechanics, no inventory grid puzzle, no free-roaming town scene, no mobile or narrow layout.

No modern sci-fi dashboard, no neon gacha UI, no mobile game reward explosion, no card-pack opening style, no cyberpunk interface, no photorealistic modern shop counter, no pure dark unreadable fantasy.

No final production asset sheet, no multiple screens, no multiple variants, no icon set, no isolated character portrait only.
```

## 4. V2 Composition Requirements

- 整體比例：桌面 16:9。
- 左側：保留可滾動配方列表語彙；可以更少列、更高 row。
- 中央：detail panel 是主要資訊區，文字安全區比 v0 更清楚。
- 素材 / 需求：必須有可放「icon + 名稱 + 需求數 / 持有數 + 狀態」的 row。
- 底部中央：結果訊息區需能承接 1-2 行中文。
- 右側 / 旁側：米菈 / NPC portrait 保留強存在感，不縮小、不裁臉。
- 背景：保持工坊氛圍，但不干擾文字疊加。

## 5. V2 Acceptance Checklist

若未來生成 V2 候選圖，審查時至少確認：

- 圖像是桌面 16:9。
- 畫面仍明確是合成屋 / 工坊類 facility UI。
- 米菈 / NPC 仍有強烈角色互動感，且沒有遮擋操作區。
- 左側列表有滾動語彙，row 可承接較多中文資訊。
- 中央詳情區有清楚的中文文字安全區。
- 素材 / 需求區不是 icon-only，能放素材名稱與數量。
- 底部中央結果區可放 1-2 行中文提示。
- 沒有可讀文字、數字、假 UI label 或固定 logo。
- 不暗示新合成規則、拖曳合成、批量合成或賣出功能。
- 仍可作為 Shop / Forge / Magic Shop 共用模板的參考，而不是只服務單一漂亮插圖。

## 6. 與 V0 的差異

| 項目 | V0 狀態 | V2 目標 |
|---|---|---|
| 左側列表 | 可接受，有滾動語彙 | 保留，允許更高 row |
| 米菈 portrait | 尺寸與存在感適合 | 保留，不縮小 |
| 中央詳情 | 方向成立但文字安全區可更清楚 | 加強中文文字承載層 |
| 素材需求 | 偏 icon / 格狀呈現 | 支援名稱與數量 row |
| 底部結果 | 大方向成立 | 明確容納 1-2 行中文 |

## 7. 下一步

此文件完成後，建議先人工審查。若通過，再由使用者明確批准「只生成一張 V2 `facility_synthesis_screen` UI-3 visual concept 候選圖」。

