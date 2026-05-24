# Facility Shop Screen Visual Reference Guidelines

## 0. 視覺定位與邊界

* **定位**：`星燈行商鋪 (Travel Shop)` 視覺參考與 Mockup 管理說明。
* **位置**：`05_assets/gui_references/facility_shop_screen/`
* **邊界**：
  * 此資料夾用於存放行商鋪的視覺概念參考圖、使用者參考圖及生成的候選 Mockup。
  * 這裡所有的圖像皆為 **Reference / Candidate**，非遊戲實體資產，不得被遊戲引擎或 Python runtime 直接引用。

---

## 1. 核心視覺風格基準 (依據 `gui-ui-direction-brief.md`)

我們秉持「溫暖但危險的邊境冒險」之總體風格，為行商鋪（特里小鋪）設定以下視覺設計要點：

### A. 配色與材質 (Color & Textures)
* **色彩基調**：以 **暖木色 (Warm Wood)、鐵灰色 (Charcoal Iron)、黃銅 (Brass) 與柔和的琥珀色燈火 (Amber Glow)** 作為生活感基底。
* **狀態色點綴**：
  * 「可購買」狀態：使用穩定的草綠色或金色邊框點綴。
  * 「受限 / 金幣不足」狀態：採用低飽和的灰色或暗紅色，且必須搭配文字（如：金幣不足）進行雙重傳達，不單純依賴色彩。
* **材質方向**：UI 面板採用粗糙紙質或輕度磨砂玻璃（Glassmorphism），搭配仿鐵鉚釘或細木紋飾邊，凸顯手作旅行感。

### B. 版面比例配置 (16:9 Game Viewport)
為塑造專注的獨立掌機/機台遊戲感，主介面鎖定 16:9 比例，三欄式橫向分區比例配置如下：
* **左側商品列表 (Left Catalog, ~28% 寬度)**：
  * 包含頂部 4 個緊湊 Tabs（全部、補給品、戰術道具、飾品）與垂直商品清單。
  * 清單項目字體清晰，保持單行顯示不折行。
* **中央選中詳情 (Center Detail, ~46% 寬度)**：
  * 上方為高對比的商品卡片，展示清晰的名稱、效果描述、持有數與用途，移除冗餘價格。
  * 下方為高對比的需求核對區（Met/Missing 條件核對）。
* **右側 NPC 區 (Right Column, ~26% 寬度)**：
  * 專注展示行商「特里」的精美全身或半身立繪，突出商鋪 Presence。
  * 此區立繪為核心視覺焦點，文字僅保留特里的名字與身分。
* **底部行動與回饋區 (Footer, ~15% 高度)**：
  * 左側返回城鎮，中間為特里提示語框，右側為明亮的「購買商品」主動作按鈕。

### C. 動態文字安全 (Dynamic Text Safety)
**嚴格禁止** 將任何有語意的文字、價格或數字直接烘死（Hardbake）在 Mockup 背景圖中。
必須由渲染層動態輸出的內容包括：
1. 商店標題與副標題。
2. 商品名稱、單價、持有數、剩餘庫存。
3. 金幣持有比對值（如：`30G / 420G`）與狀態字眼。
4. 購買按鈕的動作文字與 NPC 台詞。

---

## 2. 建議候選 Mockup 命名規則

未來若為此畫面生成概念圖，請嚴格沿用專案命名規範：

```text
facility_shop_screen_mockup_v1_candidate_001.png
facility_shop_screen_mockup_v1_candidate_002.png
```

---

## 3. 生成 Prompt 實驗草案 (Midjourney / SD Reference)

若未來需要為 NPC 立繪或店鋪背景生成參考圖，可參考以下提示詞方向：

### NPC 特里 (Terry) 肖像 Prompt 草案
> **Prompt**: `A charming fantasy traveling merchant male named Terry, medium-length messy brown hair, friendly smile, wearing a weathered traveler coat with small potion bottles hanging on his belt, warm light, stylized digital painting, game character portrait, cozy fantasy RPG art style, transparent background --ar 3:4`

### 商店場景背景 Prompt 草案
> **Prompt**: `Cozy fantasy traveling merchant shop interior, wooden shelves stacked with colorful potions and ancient scrolls, glowing amber lanterns hanging from low beams, warm and inviting atmosphere, soft painterly digital art, concept art, RPG facility screen background --ar 16:9`
