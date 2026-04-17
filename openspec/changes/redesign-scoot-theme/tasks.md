## 1. CSS 主題檔完全重寫

**檔案範圍**：`app/static/css/style.css`

- [ ] 1.1 在 `:root` 定義酷航 14 項 `--scoot-*` 色彩 tokens（`scoot-yellow` / `scoot-yellow-bright` / `scoot-yellow-deep` / `scoot-ink` / `scoot-ink-soft` / `scoot-slate` / `scoot-muted` / `scoot-canvas` / `scoot-surface` / `scoot-line` / `scoot-success` / `scoot-danger` / `scoot-warn` / `scoot-info`），色值必須與 `specs/scoot-theme/spec.md` 的「酷航品牌色彩 Tokens」一致
- [ ] 1.2 在 `:root` 定義 `--font-display`、`--font-body`、`--font-mono` 三組字體堆疊變數，含繁體中文與系統字型 fallback；設定 `body` 套用 `--font-body`、`body` 背景為 `var(--scoot-canvas)`、預設文字 `var(--scoot-ink)`
- [ ] 1.3 新增 `.navbar-scoot` 樣式：亮黃底、`4px` solid 近黑底邊、品牌文字 `--font-display` 字重 800 大寫、`.nav-link` 深色文字、`.nav-link.active` 使用 `var(--scoot-ink)` 圓角 pill + 白字
- [ ] 1.4 新增 `.card` 與 `.card-header-scoot` 樣式：白底、`16px` 圓角、`1.5px solid var(--scoot-line)` 邊框、平面陰影、hover 時邊框轉 `var(--scoot-ink)`；`.card-header-scoot` 變體為黃底近黑字
- [ ] 1.5 新增 `.btn-scoot`、`.btn-scoot-secondary`、`.btn-scoot-danger`、`.btn-scoot-success`、`.btn-scoot-warning` 五種按鈕層級，包含背景色、文字色、`10px` 圓角、`3px` solid 底部按壓邊、`:active` 套用 `translateY(1px)`、`:focus-visible` 顯示 2px 外描邊
- [ ] 1.6 覆蓋 `.form-control`、`.form-select`、`.form-label`：輸入元素採上左右 `1px` + 底 `2px` 邊、`10px` 圓角，`:focus` 底邊轉 `var(--scoot-yellow)` 並加 `3px` 黃色外暈；`.form-label` 字重 600、`0.875rem`、`var(--scoot-ink)`
- [ ] 1.7 新增 `.table-scoot-wrap`、`.table-scoot` 樣式：`12px` 圓角容器、`overflow: hidden`、`thead th` 近黑底白字 `--font-display` 字重 700、`tbody tr:nth-child(even)` 淡黃背景、hover 時加深、價格欄位（透過 `.num` / `.price` 輔助 class 或欄位 `td.text-end`）使用 `--font-mono` 右對齊
- [ ] 1.8 新增 `.stat-scoot` 家族樣式：整卡塊面背景、主數值 `--font-mono` 字級 `2.25rem` 字重 800、label uppercase `letter-spacing: 0.08em`，包含 `.stat-scoot--ink`、`.stat-scoot--yellow`、`.stat-scoot--success`、`.stat-scoot--danger`、`.stat-scoot--slate` 五種變體，禁止 `.stat-scoot--yellow` 出現白字
- [ ] 1.9 新增 `.badge-scoot-success`、`.badge-scoot-danger`、`.badge-scoot-muted` 樣式：`border-radius: 999px`、字重 700、`0.75rem` uppercase、12% alpha 底色
- [ ] 1.10 覆蓋 `.alert` 與其變體（info/success/warning/danger）：白底、`12px` 圓角、左側 `6px` 實色彩條、深色文字
- [ ] 1.11 新增全域 `@media (prefers-reduced-motion: reduce)` 規則，停用按鈕 `translateY` 位移、卡片 hover 過渡、alert 動畫（`transition` 設為 `none` 或 `0.01ms`）
- [ ] 1.12 移除舊 `--av-*` 變數與 `.navbar-aviation` / `.btn-aviation*` / `.table-aviation*` / `.stat-card*` / `.badge-aviation-*` 所有 class；結果 style.css 內 **不得** 出現 `--av-` 或 `aviation` 字串（禁止遺留）

## 2. base.html 骨架更新

**檔案範圍**：`app/templates/base.html`

- [ ] 2.1 於 `<head>` 加入 Google Fonts `<link>` 標籤，preload `Nunito`（700, 800）與 `Nunito Sans`（400, 500, 600）、`JetBrains Mono`（500），含 `preconnect` 至 `fonts.googleapis.com` 與 `fonts.gstatic.com`、`display=swap`；務必置於 Bootstrap CSS 之前或與之並列
- [ ] 2.2 將 `<nav class="navbar navbar-expand-lg navbar-dark navbar-aviation">` 中的 `navbar-aviation` 替換為 `navbar-scoot`；移除 `navbar-dark`（黃底需深色文字）；品牌 `<a class="navbar-brand">` 文字改為 `✈ FlightPrice` 或維持 `&#9992;` entity，並套用 `text-uppercase fw-bold` 對應類或依 CSS 預設生效
- [ ] 2.3 檢查 `.nav-link` 與 `.nav-link.active` 的 Jinja 條件判斷維持原樣，確認 CSS 會由 `.navbar-scoot .nav-link.active` 接手 pill 樣式

## 3. flights.html 模板更新

**檔案範圍**：`app/templates/flights.html`

- [ ] 3.1 將「新增追蹤班機」卡片的 `.card-header` 加上 `card-header-scoot` 輔助類（或更新 spec 中 primary header 樣式），讓黃色強調套用到該標題列
- [ ] 3.2 將「查詢」按鈕 `btn-aviation-outline` 替換為 `btn-scoot-secondary`
- [ ] 3.3 將「新增」按鈕 `btn-aviation` 替換為 `btn-scoot`
- [ ] 3.4 將追蹤清單區塊的表格容器 `.table-aviation-wrap` 與表格 `.table-aviation` 替換為 `.table-scoot-wrap` / `.table-scoot`
- [ ] 3.5 將班機狀態 badge 由 `badge-aviation-success` / `badge-aviation-muted` 替換為 `badge-scoot-success` / `badge-scoot-muted`
- [ ] 3.6 將操作按鈕 `btn-aviation-warning` / `btn-aviation-success` 替換為 `btn-scoot-warning` / `btn-scoot-success`
- [ ] 3.7 檢查模板內不得遺留任何 `aviation` 字串或 `btn-aviation*`、`table-aviation*`、`badge-aviation-*` 類別

## 4. charts.html 模板與 Chart.js 配色更新

**檔案範圍**：`app/templates/charts.html`

- [ ] 4.1 將下拉選單卡片與圖表卡片使用的樣式類別確認與 scoot-theme 相容；若有 `aviation` 類殘留，一併移除
- [ ] 4.2 將三張統計卡片由「`.stat-card` + `.stat-card-stripe*`」結構改為新的 `.stat-scoot` 結構：最高價 → `.stat-scoot--danger`、最低價 → `.stat-scoot--success`、平均價 → `.stat-scoot--ink`；主數值仍透過 `id="maxPrice"` / `minPrice` / `avgPrice` 綁定以供 JS 填入
- [ ] 4.3 將 Chart.js `borderColor` 改為 `#0E0E10`、`backgroundColor` 改為 `rgba(14,14,16,0.08)`、`pointBackgroundColor` 改為 `#FFDA00`、`pointBorderColor` 改為 `#0E0E10`、`pointBorderWidth` ≥ `2`、tooltip 背景 `#0E0E10` / 文字 `#ffffff`、價格數值 label 色 `#FFDA00`
- [ ] 4.4 將 grid line 顏色改為 `rgba(14,14,16,0.06)`、座標刻度 `ticks.color` 改為 `#4A4A55`、legend 文字 `#0E0E10` 字重 600
- [ ] 4.5 檢查模板內不得遺留任何 `aviation` 字串或舊 stat-card 類別

## 5. status.html 模板更新

**檔案範圍**：`app/templates/status.html`

- [ ] 5.1 將「立即抓取」按鈕 `btn-aviation-danger` 替換為 `btn-scoot-danger`
- [ ] 5.2 將三張統計卡片（追蹤班機數、成功擷取、失敗擷取）改為 `.stat-scoot` 結構：追蹤班機數 → `.stat-scoot--ink`、成功擷取 → `.stat-scoot--success`、失敗擷取 → `.stat-scoot--danger`
- [ ] 5.3 將「抓取紀錄」區塊 `.table-aviation-wrap` / `.table-aviation` 替換為 `.table-scoot-wrap` / `.table-scoot`
- [ ] 5.4 將成功 / 失敗 badge `badge-aviation-success` / `badge-aviation-danger` 替換為 `badge-scoot-success` / `badge-scoot-danger`
- [ ] 5.5 檢查模板內不得遺留任何 `aviation` 字串

## 6. 自動化驗證與測試

**檔案範圍**：`tests/test_theme_smoke.py`（新增）、既有測試維持不動

- [ ] 6.1 新增 `tests/test_theme_smoke.py`，使用 Flask test client 驗證 `GET /`、`GET /charts`、`GET /status` 的 HTML 回應：
  - 斷言 `navbar-scoot` class 出現在 `/` 回應中
  - 斷言 `/` 回應包含 `btn-scoot` 字串（「新增」主按鈕）
  - 斷言 `/charts` 回應包含 `stat-scoot--ink` 或 `stat-scoot--success` 或 `stat-scoot--danger`
  - 斷言 `/status` 回應包含 `table-scoot` 與 `badge-scoot-success` 或對應 badge 類別
  - 斷言所有回應皆不得包含 `navbar-aviation`、`btn-aviation`、`table-aviation`、`stat-card-stripe`、`badge-aviation-` 等舊 class 字串
- [ ] 6.2 新增 `tests/test_theme_smoke.py` 中的「CSS 靜態檔」測試：`GET /static/css/style.css` 回應 200、Content-Type 為 `text/css`、內容包含 `--scoot-yellow: #FFDA00`（或等同色碼宣告），且不包含 `--av-` 與 `aviation` 字串
- [ ] 6.3 於 Docker container 內執行 `pytest`（`./run.sh pytest` 或 `docker compose run --rm app pytest`），確認所有測試通過、無迴歸

## 7. 手動視覺驗證與容器重啟

**檔案範圍**：無程式碼變更；僅執行與觀察

- [ ] 7.1 重建 Docker image（`docker/build.sh`）並重啟容器（`./run.sh` 或等效指令）
- [ ] 7.2 依序瀏覽 `/`、`/charts`、`/status` 三頁，驗證：導航列為黃底黑字底部粗邊、主按鈕為黃底黑字、卡片為白底深邊、統計卡片為整卡塊面染色、表格表頭近黑底白字、badge 為圓角 pill
- [ ] 7.3 開啟瀏覽器開發者工具，確認：`body` 的 computed `font-family` 以 `Nunito Sans` 開頭、`<h2>` 以 `Nunito` 開頭、票價欄位以 `JetBrains Mono` 開頭；`:root` 定義了 `--scoot-yellow` 等 tokens
- [ ] 7.4 以鍵盤 Tab 依序聚焦導航連結、表單欄位、按鈕，確認每一步皆有可見 focus 外描邊
- [ ] 7.5 暫時於作業系統啟用「減少動畫」偏好，確認按鈕按下時 `translateY` 位移被停用
