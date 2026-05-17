# Facility Synthesis Screen Prompt Draft

用途：把 `01_content/gui-facility-synthesis-mockup-request.md` 轉成可人工審查的圖像 prompt 草案。此文件不是生成指令；在使用者明確批准前，不生成圖片、不啟動 asset pipeline、不建立 asset registry。

## 0. 邊界

- 只做 prompt draft，不生成圖片。
- 目標是單張 `facility_synthesis_screen` UI-3 visual concept。
- 只處理桌面 16:9。
- 保留米菈 / NPC portrait 或 character-presence 區域。
- 所有文字、數字、配方名稱、素材名稱、價格、按鈕 label 都必須由未來 render layer 動態輸出，不可畫死在圖裡。
- 不新增配方、素材、合成規則、批量合成、拖曳合成或任何新 gameplay。
- 不選定 pygame / HTML / Unity 或其他 GUI 技術。

## 1. Prompt 使用狀態

```yaml
prompt_id: gui_prompt_facility_synthesis_screen_mockup_v0
status: draft
linked_request_id: gui_asset_facility_synthesis_screen_mockup_v0
screen_id: facility_synthesis_screen
flow_id: flow_a_town_facility
target_asset_type: screen_mockup
target_role: ui3_visual_concept
target_ratio: "16:9"
generation_allowed_now: false
```

## 2. Positive Prompt Draft

以下 prompt 偏英文，方便未來接多數圖像工具；正式使用前仍需人工審查。

```text
Create a single desktop 16:9 fantasy RPG GUI visual concept mockup for the Synthesis Screen inside Mila's synthesis house.

The screen is a warm frontier alchemy and crafting workshop, with practical wooden furniture, parchment UI panels, brass and iron fittings, small crystals, bottles, tools, recipe materials, and soft amber lamplight. Add a small amount of star-lamp blue accent lighting for the magic synthesis mood. The visual tone should feel warm, handcrafted, readable, and practical, not flashy.

The composition must clearly show a functional game UI layout:
- Top region: dynamic screen title area, player resource summary area, and short objective or facility hint area.
- NPC region: a visible portrait or bust area for Mila / the synthesis NPC, placed so the screen keeps a sense of character interaction. The portrait must not block recipe controls or detail panels.
- Left region: category tabs or segmented controls above a recipe list. Include visible selected-row and disabled-row states using abstract shapes only.
- Right region: selected recipe detail panel with clear placeholder zones for output, effect or description, base equipment requirement, material requirements, gold requirement, and maximum craft count or availability.
- Bottom region: action bar with primary confirm/craft action area, back/cancel action area, and result or disabled-reason message area.

Use abstract placeholder blocks, lines, icons, and blank UI shapes for all text regions. Do not include readable Chinese, English, numbers, item names, recipe names, prices, stats, button labels, dialogue text, or logo text. All text must be imagined as dynamic overlay text added later by the render layer.

Make the list-detail-confirm-result structure immediately understandable. Keep the recipe list and detail panels calm and uncluttered so dynamic Chinese UI text can be overlaid later. Availability states should be distinguishable by shape, value, border, icon, or panel treatment, not by color alone.

Style: restrained fantasy RPG interface, warm wood, parchment, brass, iron gray, soft amber light, subtle crystals, handcrafted workshop, readable UI hierarchy, desktop game screen mockup.
```

## 3. Negative Prompt Draft

```text
No readable text, no letters, no Chinese characters, no English words, no numbers, no labels, no button text, no recipe names, no item names, no material names, no prices, no stats, no HP or MP numbers, no dialogue text, no logo text.

No modern sci-fi dashboard, no neon gacha UI, no mobile game reward explosion, no card-pack opening style, no cyberpunk interface, no photorealistic modern shop counter, no pure dark hardcore fantasy that makes text unreadable.

No clutter behind list or detail text areas, no UI regions hidden by decoration, no portrait blocking the recipe list, no portrait blocking the detail panel, no full-screen illustration without usable UI layout.

No drag-and-drop crafting implication, no batch crafting controls, no selling flow, no new crafting mechanics, no inventory grid puzzle, no free-roaming town scene, no mobile or narrow layout.

No final production asset sheet, no multiple screens, no multiple variants, no icon set, no isolated character portrait only.
```

## 4. Composition Notes

推薦構圖方向：

- 整體比例：桌面 16:9。
- 視覺重心：右側或右中區域是 recipe detail；左側是 category + recipe list。
- 米菈 / NPC portrait：建議放在右上、左下角旁側，或 detail panel 旁的獨立 character-presence 區，不可壓住主要文字區。
- 背景：工坊內景只做氛圍，功能 UI panel 仍是畫面主體。
- 面板：羊皮紙、木框、黃銅角釘、鐵灰分隔線；保持乾淨，不要過度厚重。
- 狀態：可用 / 不可用 / 選取狀態用圖形、邊框、亮度或小 icon 表達，不只靠紅綠色。
- 文字區：只用空白線條、灰階 block、短橫線或不可讀符號表示。

## 5. Dynamic Text Reminders

以下內容絕對不可出現在生成圖中：

- `米菈合成屋`、`全部`、`裝備`、`戰術道具` 等任何固定 UI 文字。
- 配方名稱、素材名稱、裝備名稱、道具名稱。
- 價格、持有數、素材數量、最多可製作次數。
- `合成`、`確認`、`返回`、`取消` 或任何按鈕文字。
- NPC 對話或提示文字。
- 數字、英文字母、中文字、日文字、假字母、可辨識符號字。

允許：

- 不可讀的裝飾符號。
- 無語意的刻痕、花紋、魔法紋路。
- 空白 label slot、placeholder bar、icon-like abstract marks。

## 6. Review Checklist Before Generation

在真正生成圖片前，先人工確認：

- 是否仍是單張 `facility_synthesis_screen`，沒有擴到其他 screen？
- 是否清楚要求 UI-3 visual concept，而不是 UI-2 wireframe？
- 是否只要求桌面 16:9？
- 是否保留米菈 / NPC portrait 區域？
- 是否保留 category、recipe list、detail、requirements、action bar、result feedback 區域？
- 是否禁止所有可讀文字與數字？
- 是否禁止新合成規則、拖曳合成、批量合成或賣出功能？
- 是否沒有指定 pygame / HTML / Unity？
- 是否沒有要求生成 icon set、角色立繪集、背景集或多張變體？

## 7. Acceptance Checklist For Candidate Image

若未來生成一張候選圖，審查時至少確認：

- 圖像是桌面 16:9。
- 畫面一眼看得出是合成 / 工坊類設施 UI。
- 米菈 / NPC 位置存在，且不壓住操作區。
- category、list、detail、requirements、actions、result feedback 的區域清楚。
- 所有文字位置都可由未來 render layer 疊加。
- 沒有可讀文字、數字、假 UI label 或固定 logo。
- 背景和裝飾沒有干擾文字可讀性。
- 不暗示任何未批准的新 gameplay。
- 視覺方向符合溫暖邊境工坊、羊皮紙、木材、黃銅、柔和燈火、少量星燈藍點綴。

## 8. 下一步

建議下一步不是立刻生成圖片，而是先人工審查此 prompt draft。若通過，再由使用者明確批准「只生成一張 `facility_synthesis_screen` UI-3 visual concept 候選圖」。

## 9. V2 Refinement Notes

以下是第一張候選 mockup 產出後的人工判斷，用於未來若要做第二版 prompt 時調整方向。本段不是生成指令，也不代表現在要生成第二張。

### 保留方向

- 左側配方列表不是主要版面問題。畫面已有滾動條語彙，代表列表可以上下拖曳；若單列 row 需要承載較多中文資訊，後續可加高 row、減少同屏顯示列數，不必視為版面失敗。
- 米菈 / NPC portrait 尺寸目前適合，應保留角色存在感。她的視覺重量有助於維持設施互動感，不建議縮小。
- 若未來真的需要讓中央詳情區稍寬，可以接受米菈人物區極輕微往右移，但不可移位過頭，不可裁切臉部，也不可變成只顯示半張臉。

### V2 微調優先焦點

1. 中央詳情區中文安全區更清楚。
   - 主詳情 panel 需要更明確的文字承載層。
   - 要能容納配方效果、產出說明、缺少原因等較長中文。
   - 背景裝飾與圖示不可干擾中文可讀性。

2. 中央素材 / 需求區能承接素材名稱與數量。
   - 素材 row 不應只有 icon。
   - 應預留「素材 icon + 素材名稱 + 需求數 / 持有數」的結構。
   - 這是合成屋最重要的決策資訊，優先級高於純裝飾。

3. 底部結果訊息區保留 1-2 行中文提示。
   - 中央底部長條應能放結果或不可用原因。
   - 例如：素材不足、金幣不足、缺少基底裝備、合成成功。
   - 文字區要比單行裝飾 label 更穩，避免被邊框或背景紋理壓縮。

### V2 Prompt Delta 草案

若未來要生成第二版，可在 positive prompt 中加入以下調整：

```text
Compared with the first concept, prioritize clearer Chinese text-safe zones in the central recipe detail panel. The material requirements section must have wider structured rows that can later support a material icon, material name, required count, and owned count. The bottom center result message area must be large and calm enough for one to two lines of dynamic Chinese feedback text.

Keep the left recipe list scrollable; it may show fewer, taller rows rather than many dense rows. Preserve the Mila / NPC portrait at a strong, friendly size. If more room is needed for the central detail panel, shift the portrait only slightly to the right, without cropping the face and without reducing the character interaction feeling.
```

若未來要更新 negative prompt，可加入：

```text
Do not shrink the NPC portrait. Do not crop Mila's face. Do not make the material requirement row icon-only. Do not compress the bottom result message area into a tiny label. Do not overfill the central detail panel with decorative objects.
```
