## 1. CSS 主題檔案

- [x] 1.1 建立 `app/static/css/style.css`，定義 `:root` 航空主題色彩變數與全域樣式（body 背景、字型）
- [x] 1.2 在 `style.css` 中新增導航列樣式（深航空藍背景、白色文字、當前頁高亮）
- [x] 1.3 在 `style.css` 中新增卡片樣式（圓角、陰影、hover 浮起效果）
- [x] 1.4 在 `style.css` 中新增表格樣式（深航空藍表頭、交替行色、圓角容器）
- [x] 1.5 在 `style.css` 中新增按鈕與表單樣式（航空藍主色、聚焦藍框）
- [x] 1.6 在 `style.css` 中新增統計卡片樣式（左側色條、大字號數值）
- [x] 1.7 在 `style.css` 中新增 Badge 樣式（與航空主題協調的成功/失敗/停用標籤）

## 2. 模板更新

- [ ] 2.1 更新 `base.html`：引入 style.css、修改導航列 class 與品牌文字（加飛機符號）
- [ ] 2.2 更新 `flights.html`：套用新的卡片、表格、表單、按鈕 class
- [ ] 2.3 更新 `charts.html`：套用新的卡片與統計卡片 class，調整 Chart.js 配色
- [ ] 2.4 更新 `status.html`：套用新的卡片、統計卡片、表格 class

## 3. 驗證

- [ ] 3.1 重建 Docker image 並重啟容器，瀏覽所有頁面確認視覺效果正確
- [ ] 3.2 執行全部測試確認無迴歸
