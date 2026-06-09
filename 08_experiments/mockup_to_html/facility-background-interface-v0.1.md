# Facility Background Interface Specification V0.1

此文件定義了 8 個 Facility Skinning Labs 的「全畫面場景背景圖片接口」規格與配置說明。

> [!IMPORTANT]
> 此背景接口目前僅適用於 `08_experiments/mockup_to_html/` 底下的 **fixture-only mockup 實驗室**，並非正式的 runtime 遊戲資源管道（Asset Pipeline）。
> 目的在於提供一個純前端靜態調試接口，讓設計者能觀察場景背景與 HTML UI 的互動、NPC 構圖是否被面板遮蔽、以及面板的透明度與文字可讀性。

---

## 1. 背景圖片命名與放置路徑

各設施預期的貼圖檔名與完整相對路徑如下（限 **JPG** 格式）：

| 設施 (Lab 檔名) | 圖片放置相對路徑 | 建議構圖安全區與視覺重點 |
| :--- | :--- | :--- |
| **Guild** (`guild_skinning_lab`) | `guild_skinning_lab/assets/guild-background.jpg` | 公會大廳/櫃檯環境；負空間（暗區）建議偏左或中間偏右，避免遮擋任務面板及 NPC。 |
| **Inn** (`inn_skinning_lab`) | `inn_skinning_lab/assets/inn-background.jpg` | 溫暖的旅店客房/壁爐；NPC 莉莉位於右側，背景宜偏暖暗色調，確保文字可讀。 |
| **Workshop** (`workshop_skinning_lab`) | `workshop_skinning_lab/assets/workshop-background.jpg`<br>`workshop_skinning_lab/assets/workshop-background-02.jpg` | 包含武器及防具雙背景：<br>- 預設武器/葛雷 (`workshop-background.jpg`)：左側與中央為面板，右側為葛雷立繪。<br>- 防具/布琳 (`workshop-background-02.jpg`)：切換為布琳時，CSS 會透過 `:has(.brin-armor)` 自動切換為此背景。 |
| **Magic Shop** (`magic_shop_skinning_lab`) | `magic_shop_skinning_lab/assets/magic-shop-background.jpg` | 奧秘圖書館/魔晶商店；右側有 NPC 伊芙，背景宜使用神祕的深紫/深藍暗色調。 |
| **Synthesis** (`synthesis_skinning_lab`) | `synthesis_skinning_lab/assets/synthesis-background.jpg` | 鍊金工房/藥劑桌；右側有 NPC 米菈，背景宜使用金綠或琥珀灰等暗色調。 |
| **Storage** (`storage_skinning_lab`) | `storage_skinning_lab/assets/storage-background.jpg` | 陰暗的工會保管箱庫房；因操作頻繁，構圖宜沉穩乾淨，避免搶眼的角色或高光。 |
| **Temple** (`temple_skinning_lab`) | `temple_skinning_lab/assets/temple-background.jpg` | 莊嚴的神殿/彩繪玻璃；NPC 艾莉希亞位於右側，背景以深藍/深紫為主，突顯 Sacred Gold 主題。 |
| **Relic Preview** (`relic_preview_skinning_lab`) | `relic_preview_skinning_lab/assets/relic-preview-background.jpg` | 聖物祭壇/遺物石碑；中央為發光的 Orb 特寫，背景中間應為暗色，防止光效衝突。 |

---

## 2. 建議解析度與格式

- **支援格式**: 固定為 `.jpg` (JPEG) 格式。
- **解析度建議**: 最低 `1920 x 1080`（推薦使用 `16:9` 或 `16:10` 等主流寬螢幕比例，以獲得最佳的 `cover` 縮放裁剪效果）。
- **色彩對比**: 圖片整體應保持暗色調，或在面板疊加區域預留足夠的暗影/負空間，確保白色、淡金色文字有足夠的可讀對比度。

---

## 3. CSS 變數接口 (Facility Background Interface)

每個設施的 CSS 檔案頂部均聲明了以下變數接口：

```css
/* ==========================================
   Facility Background Interface
   ========================================== */
:root {
  --facility-background-image: url('./assets/<filename>-background.jpg');
  --facility-background-position: center;
  --facility-background-size: cover;
  --facility-background-overlay: rgba(0, 0, 0, 0.45);
  --facility-shell-wash: rgba(12, 13, 16, 0.6);
}
```

### 變數功能說明：

1. `--facility-background-image`
   - **用途**: 設定全畫面背景圖片的本地相對路徑。
   - **預設值**: 指向各自 `assets/` 目錄下的 JPG 檔案。
2. `--facility-background-image-2` (僅限 **Workshop**)
   - **用途**: 設定防具工匠模式（布琳）的背景圖片路徑（對應 `workshop-background-02.jpg`）。
3. `--facility-background-position`
   - **用途**: 調整背景圖在頁面上的對齊錨點。
   - **預設值**: `center` (可根據圖片構圖手動微調如 `top left`、`50% 30%` 等)。
3. `--facility-background-size`
   - **用途**: 設定背景圖縮放模式。
   - **預設值**: `cover` (確保圖片在任何視窗尺寸下皆鋪滿全畫面且不重複)。
4. `--facility-background-overlay`
   - **用途**: 全畫面背景的暗色亮度遮罩（獨立疊加層）。
   - **預設值**: `rgba(0, 0, 0, 0.45)` (若貼圖本身較暗，可調低為 `rgba(0, 0, 0, 0.2)`；若貼圖較亮，可調高為 `rgba(0, 0, 0, 0.6)` 以確保文字清晰度)。
5. `--facility-shell-wash`
   - **用途**: 最外層 Shell 容器的背景顏色/透明度洗底。
   - **預設值**: 透明或半透明的暗色（如 `rgba(12, 13, 16, 0.6)`），允許背景貼圖從 UI 排版間隙中自然透出，而不會使內層的文字面板變透明。

---

## 4. 如何暫時停用背景圖片

當您想要比對「無圖片」與「有圖片」的差別，或暫時恢復原本原型背景時，可以使用以下兩種方式之一：

1. **方式 A：在 CSS 中將圖片路徑設為 `none`**
   ```css
   --facility-background-image: none;
   ```
   此時瀏覽器會自動隱藏 `body::before`，並安全地退回顯示 `body` 上原本設定的背景漸層或背景底色。

2. **方式 B：移除 HTML 中的 `facility-body` Class**
   在 `index.html` 中將 `<body>` 的 class 移除：
   ```html
   <!-- 變更前 -->
   <body class="facility-body">
   
   <!-- 變更後 -->
   <body>
   ```
   這會使 `body::before` 與 `body::after` 偽元素完全失效，不套用任何背景圖片及亮度遮罩。
