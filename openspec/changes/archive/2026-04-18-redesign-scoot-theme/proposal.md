## Why

目前網站採用通用航空主題（深航空藍 + 雲朵灰白 + 琥珀色輔助），視覺語彙中性且缺乏品牌個性。為了強化產品識別並帶入廉航活潑、年輕、大膽的氛圍，本次變更將整體視覺系統重新設計為「酷航（Scoot）」品牌風格——以大面積亮黃配近黑對比為核心、圓潤 sans-serif 字體、塊面色彩搭配登機證意象的裝飾細節。

## What Changes

- **BREAKING（視覺層級）**：移除 `aviation-theme` 既有的深航空藍 / 雲朵灰白 / 琥珀色主題，改為酷航的亮黃 + 近黑 + 暖白色系；由於此為純視覺變更，不影響任何路由、資料模型或 API 行為。
- 重寫 `app/static/css/style.css`：新的 CSS 自訂屬性（以 `--scoot-*` 為命名前綴）取代原 `--av-*`，定義主色、次色、文字色、背景色、狀態色、字體堆疊、圓角、陰影等設計 tokens。
- 導航列：以酷航亮黃作為大面積底色，底部加深色粗邊作為「登機證撕線」裝飾，品牌文字改為粗體大寫、搭配飛機符號。
- 卡片：改用「塊面 + 硬派邊框」風格，取代既有的浮空陰影 hover；card-header 可使用黃色強調條。
- 表格：表頭改為近黑背景白字、奇偶行以黃色低透明度交替，數字欄改用 mono 字體。
- 按鈕：主色按鈕採用黃底黑字、底部立體按壓邊；新增次要、危險、成功、警告四種層級，均帶 active 按壓動畫。
- 表單：輸入框採用底邊線樣式，聚焦時底邊轉為酷航黃。
- 統計卡片：由「左側色條 + 數字」改為「整卡塊面染色 + 大數字（mono 字體）」，並可在右下角加登機證打孔裝飾。
- Badge / Alert：調整成酷航色系的 pill 與左側粗彩條風格。
- Chart.js 配色調整：主線條改用近黑色、點改用黃底黑邊、tooltip 深色底白字。
- 模板套用：更新 4 個模板（`base.html`、`flights.html`、`charts.html`、`status.html`）以引用新的 CSS class。
- 可及性：維持 WCAG AA 對比、明確規範「黃底禁白字」、提供 `:focus-visible` 與 `prefers-reduced-motion` 規則。

## Capabilities

### New Capabilities

- `scoot-theme`：定義酷航品牌風格的視覺設計規格，涵蓋色彩 tokens、字體堆疊、元件樣式（導航、卡片、表格、按鈕、表單、統計卡片、Badge、Alert）、Chart.js 配色與 Accessibility 要求。

### Modified Capabilities

- `aviation-theme`：此能力的全部需求將被 `scoot-theme` 取代。於本變更中以 delta 方式 REMOVED 全部需求，並由新的 `scoot-theme` 規格接手。

## Impact

- **程式碼**：
  - `app/static/css/style.css`（完全重寫）
  - `app/templates/base.html`（導航列 class、品牌字串）
  - `app/templates/flights.html`（卡片、表格、表單、按鈕 class）
  - `app/templates/charts.html`（卡片、統計卡片 class、Chart.js 內嵌配色）
  - `app/templates/status.html`（卡片、統計卡片、表格、按鈕 class）
- **Docker**：`docker/Dockerfile` 既有的 `COPY app/` 已包含 `app/static/`，無需調整；完成後需重建 image 並重啟容器。
- **依賴**：沿用 Bootstrap 5.3.3 CDN + Chart.js 4 CDN，不新增套件。如採用 Google Fonts（Nunito）需以 `<link>` 方式載入，或 fallback 至系統字體。
- **資料／API／行為**：無影響，本變更為純視覺層。
- **測試**：需通過既有測試套件（Docker container 內 pytest）不發生迴歸；並新增模板渲染 smoke 驗證，確認關鍵 CSS class 實際出現在渲染結果中。
- **規格**：新增 `openspec/specs/scoot-theme/spec.md`（由 `/opsx:archive` 時從本變更合併產出）；既有 `openspec/specs/aviation-theme/` 將於歸檔時被 REMOVED。
