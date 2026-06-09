# Workshop Skinning Lab Background Image

此目錄下的貼圖將作為邊境工坊設施場景背景圖。

## 預期圖片檔案

- 預期檔案 1 (武器/葛雷葛)：`workshop-background.jpg`
- 預期檔案 2 (防具/布琳)：`workshop-background-02.jpg`
- 位置：`08_experiments/mockup_to_html/workshop_skinning_lab/assets/`
- 格式：JPG
- 建議解析度：1920x1080 (或更高，寬螢幕比例)
- 建議構圖：鍛造工坊環境、金屬與火焰火花氣氛，應注意左右兩側與中間區域的負空間。當在網頁上切換至防具分類（NPC 布琳，類名 `brin-armor`）時，CSS 會自動以 `:has()` 選擇器切換至 `workshop-background-02.jpg` 背景。
