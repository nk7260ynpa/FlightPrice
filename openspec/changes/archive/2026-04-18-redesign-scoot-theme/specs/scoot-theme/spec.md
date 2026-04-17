## ADDED Requirements

### Requirement: 酷航品牌色彩 Tokens

系統 SHALL 在 `app/static/css/style.css` 的 `:root` 中定義酷航品牌的 CSS 自訂屬性色彩 tokens，所有元件 MUST 透過 `var(--scoot-*)` 引用色彩，不得直接在元件選擇器中寫死色碼。色彩 tokens 內容 SHALL 包含以下項目與對應色碼（允許 ±1% 明度微調，不得改變色相）：

- `--scoot-yellow: #FFDA00`（主品牌黃）
- `--scoot-yellow-bright: #FFEB3D`（提亮層，供 hover／active）
- `--scoot-yellow-deep: #E5B800`（深黃，供描邊與按壓邊）
- `--scoot-ink: #0E0E10`（主要深色文字／深色區塊）
- `--scoot-ink-soft: #24242A`（次要深色區塊）
- `--scoot-slate: #4A4A55`（次要文字）
- `--scoot-muted: #8A8A95`（輔助說明、placeholder）
- `--scoot-canvas: #FAFAF7`（頁面背景，暖米白）
- `--scoot-surface: #FFFFFF`（卡片／面板背景）
- `--scoot-line: #E6E6DF`（分隔線、柔和邊框）
- `--scoot-success: #1FAD66`
- `--scoot-danger: #E4322B`
- `--scoot-warn: #FF8A1F`
- `--scoot-info: #2D6BD6`

#### Scenario: 色彩 tokens 於頁面載入時可用
- **WHEN** 使用者載入任一頁面（`/`、`/flights`、`/charts`、`/status`）
- **THEN** 瀏覽器計算樣式中 `:root` SHALL 解析到上述 14 項 `--scoot-*` CSS 自訂屬性，且對應色碼與本 Requirement 定義一致

#### Scenario: 元件透過變數引用色彩
- **WHEN** 開發者檢視 `app/static/css/style.css` 中任一元件樣式規則
- **THEN** 涉及色彩的屬性（`color`、`background`、`border-color` 等）MUST 使用 `var(--scoot-*)` 形式，而非硬編碼色碼（允許例外：`rgba()` 中以 token 色衍生的透明度表示，或純 `#ffffff`、`transparent`、`currentColor` 等中性值）

### Requirement: 字體堆疊

系統 SHALL 為頁面提供三組 CSS 自訂屬性字體堆疊，分別用於 display（標題）、body（內文）、mono（數字）；字體堆疊 MUST 包含西文優先字型、繁體中文 fallback 與系統字型 fallback，確保任一環境皆可渲染。

- `--font-display`：起首 `"Nunito"`，fallback 依序包含 `"Poppins"`、`"PingFang TC"`、`"Noto Sans TC"`、`-apple-system`、`BlinkMacSystemFont`、`"Helvetica Neue"`、`sans-serif`
- `--font-body`：起首 `"Nunito Sans"`，fallback 依序包含 `"Poppins"`、`"PingFang TC"`、`"Noto Sans TC"`、`-apple-system`、`BlinkMacSystemFont`、`sans-serif`
- `--font-mono`：起首 `"JetBrains Mono"`，fallback 依序包含 `"Fira Code"`、`"Roboto Mono"`、`ui-monospace`、`monospace`

`body` 元素預設使用 `--font-body`；所有標題元素（`h1`–`h3`）與品牌文字 MUST 使用 `--font-display`；票價／金額／班次代碼等數字資訊 MUST 使用 `--font-mono`。

#### Scenario: Body 套用內文字體
- **WHEN** 頁面載入完成
- **THEN** `<body>` 元素的 computed style `font-family` SHALL 以 `Nunito Sans` 開頭，且字串中 SHALL 包含 `PingFang TC` 與 `Noto Sans TC`

#### Scenario: 標題套用 display 字體
- **WHEN** 頁面中出現 `<h2>` 主標題
- **THEN** 該元素 computed style `font-family` SHALL 以 `Nunito` 開頭，字重 SHALL ≥ 700

#### Scenario: 票價使用 mono 字體
- **WHEN** 頁面呈現票價、班次代碼或統計數值（統計卡片的 `.stat-scoot-value`、表格的價格欄、圖表 tooltip 價格）
- **THEN** 該文字 computed style `font-family` SHALL 包含 `JetBrains Mono` 或其 fallback `monospace`

### Requirement: 頁面背景與整體排版

所有頁面的 `body` 背景色 SHALL 為 `var(--scoot-canvas)`；主要內容容器（`container.mt-4`）上下內距 SHALL ≥ `0.5rem` / `2rem`，確保與導航列保留呼吸空間。預設文字顏色 SHALL 為 `var(--scoot-ink)`。

#### Scenario: 頁面背景色
- **WHEN** 使用者瀏覽任一頁面
- **THEN** `<body>` 的背景色 SHALL 為 `#FAFAF7`（或與之匹配的 `--scoot-canvas` 變數值）

### Requirement: 導航列酷航風格

導航列 SHALL 使用 `var(--scoot-yellow)` 純色實底（不得使用漸層），底部 MUST 有 `4px` 實色 `var(--scoot-ink)` 粗邊作為登機證撕線裝飾。品牌文字 `FlightPrice` MUST 使用 `--font-display`、字重 800、字母全大寫、包含飛機符號（`&#9992;` 或等效 SVG icon）。導航連結 MUST 為 `var(--scoot-ink)` 深色文字，active 狀態 MUST 使用 `var(--scoot-ink)` 實色圓角 pill 背景搭配 `#ffffff` 白色文字。

#### Scenario: 導航列顯示
- **WHEN** 使用者瀏覽任一頁面
- **THEN** 頂部導航列 SHALL 顯示亮黃實色背景、底部 4px 深色粗邊、飛機符號前綴的大寫粗體品牌字

#### Scenario: 當前頁面導航高亮
- **WHEN** 使用者位於 `/flights`、`/charts`、`/status` 任一頁面
- **THEN** 對應的 `.nav-link` SHALL 套用 `.active` 狀態樣式，顯示近黑色圓角 pill 背景與白色文字；其他非當前頁的連結 SHALL 保持深色文字與透明背景

#### Scenario: 禁止黃底白字
- **WHEN** 開發者檢視導航列樣式
- **THEN** 導航列 `.nav-link` 非 active 狀態的文字顏色 MUST 為 `var(--scoot-ink)` 或等效深色，禁止使用白色或淺色文字於黃色底上（AA 對比規範）

### Requirement: 卡片元件風格

所有內容卡片（Bootstrap `.card` 與其他面板容器）SHALL 使用 `var(--scoot-surface)` 白色背景、`16px` 圓角、`1.5px` 實色 `var(--scoot-line)` 邊框；陰影 MUST 採「平面塊面」風格（建議 `0 2px 0 var(--scoot-line)` 或極淺陰影），不得使用大範圍浮空陰影。滑鼠懸浮時，卡片 MUST 不上移，改以 `border-color` 轉為 `var(--scoot-ink)` 的方式回饋互動。

`card-header` SHALL 支援兩種變體：
- 預設：`var(--scoot-surface)` 背景 + `var(--scoot-ink)` 文字 + `var(--font-display)` 字重 700。
- 強調（class 包含 `card-header-scoot` 或同義變體）：`var(--scoot-yellow)` 背景 + `var(--scoot-ink)` 文字。

#### Scenario: 卡片靜態顯示
- **WHEN** 頁面載入包含 `.card` 的內容區塊
- **THEN** 卡片 SHALL 顯示白色背景、`border-radius` ≥ 14px、`border-width` ≥ 1px 且 `border-style: solid`

#### Scenario: 卡片懸浮互動
- **WHEN** 使用者將滑鼠移至 `.card` 上方且系統未啟用 `prefers-reduced-motion`
- **THEN** 卡片 `border-color` SHALL 從 `var(--scoot-line)` 轉變為 `var(--scoot-ink)`，且 `transform` SHALL 不包含 `translateY` 位移（保持塊面感）

### Requirement: 按鈕系統

系統 SHALL 提供五種按鈕層級：primary（主，黃底黑字）、secondary（次，透明底深邊）、danger（危險）、success、warning。每一層級的按鈕 SHALL：

- 使用 `10px` 圓角、`var(--font-display)` 或 `var(--font-body)` 字重 700、內距 `0.55rem 1.25rem`。
- 具備 `3px` solid 底部「按壓邊」（color：對應主色的深階變體，如 `--scoot-yellow-deep` 或 `#b91c1c` 等）。
- `:active` 狀態 MUST 套用 `transform: translateY(1px)` 並移除或縮短底邊，模擬按壓；當 `prefers-reduced-motion: reduce` 時 MUST 停用此 transform。
- `:focus-visible` MUST 顯示 `2px` 外描邊（`var(--scoot-ink)`）與 `2px` offset，以符合鍵盤操作可及性。

層級對照表（色彩／文字必須符合）：

| 層級 | 背景 | 文字 | 底邊色 |
|------|------|------|--------|
| primary | `var(--scoot-yellow)` | `var(--scoot-ink)` | `var(--scoot-yellow-deep)` |
| secondary | `transparent` | `var(--scoot-ink)` | `var(--scoot-ink)`（2px 邊框代替） |
| danger | `var(--scoot-danger)` | `#ffffff` | `#b91c1c` |
| success | `var(--scoot-success)` | `#ffffff` | `#158A4F` |
| warning | `var(--scoot-warn)` | `var(--scoot-ink)` | `#D9690F` |

#### Scenario: 主按鈕樣式
- **WHEN** 頁面出現主操作按鈕（CSS class 如 `btn-scoot` 或等同語意的 primary）
- **THEN** 按鈕 SHALL 顯示 `#FFDA00` 背景、`#0E0E10` 文字、`10px` 圓角、底部 `3px` 深黃按壓邊

#### Scenario: 危險按鈕樣式
- **WHEN** 頁面出現「立即抓取」等危險／強提示按鈕（class 如 `btn-scoot-danger`）
- **THEN** 按鈕 SHALL 顯示紅色底、白色文字、`10px` 圓角、底部 `3px` 暗紅按壓邊

#### Scenario: 按下反饋
- **WHEN** 使用者滑鼠點擊任一 `btn-scoot*` 並處於 `:active` 狀態，且 `prefers-reduced-motion` 非 `reduce`
- **THEN** 按鈕 SHALL 套用 `translateY(1px)` 向下位移；若 `prefers-reduced-motion: reduce`，則 MUST 不套用 transform

#### Scenario: 鍵盤聚焦可見
- **WHEN** 使用者以鍵盤 Tab 至任一 `btn-scoot*`
- **THEN** 按鈕 SHALL 顯示 `2px` 可見外描邊與 `2px` offset（或等效高對比聚焦指示）

### Requirement: 表單樣式

表單輸入元素（`.form-control`、`.form-select`）SHALL 採「底邊強調」風格：上、左、右邊為 `1px solid var(--scoot-line)`，底邊為 `2px solid var(--scoot-line)`，圓角 `10px`；聚焦時底邊 MUST 轉為 `var(--scoot-yellow)`，並顯示 `3px` 黃色柔和外暈（`rgba(255, 218, 0, 0.25)` 或等效透明層）。Placeholder 顏色 MUST 為 `var(--scoot-muted)`。Label（`.form-label`）MUST 使用 `--font-body` 字重 600、字級 `0.875rem`、顏色 `var(--scoot-ink)`。

#### Scenario: 表單輸入聚焦
- **WHEN** 使用者點擊或 Tab 聚焦任一 `.form-control` 或 `.form-select`
- **THEN** 該元素底邊 SHALL 轉為酷航黃 `var(--scoot-yellow)`，並帶有柔和黃色外暈

#### Scenario: Label 樣式
- **WHEN** 頁面渲染包含 `.form-label` 的表單欄位
- **THEN** label 文字 SHALL 以字重 600、`var(--scoot-ink)` 顏色、字級 `0.875rem` 顯示

### Requirement: 表格風格

資料表格 SHALL 使用 `12px` 圓角容器並設 `overflow: hidden` 以裁切邊角；表頭 MUST 使用 `var(--scoot-ink)` 深色背景搭配 `#ffffff` 白色文字與 `var(--font-display)` 字重 700、`letter-spacing: 0.04em`；表身行列交替 MUST 使用 `var(--scoot-yellow)` 約 8% alpha 的淡黃底（`rgba(255, 218, 0, 0.08)`），hover 時提升至約 16% alpha；價格欄位 MUST 使用 `--font-mono` 並右對齊。

#### Scenario: 表格顯示
- **WHEN** 頁面載入包含 `.table-scoot` 的資料表
- **THEN** 表頭 SHALL 為近黑色背景白色粗體文字，偶數行 SHALL 套用淡黃色背景，價格欄位 SHALL 使用 mono 字體

#### Scenario: 表格互動
- **WHEN** 使用者將滑鼠移至任一資料列
- **THEN** 該列 SHALL 套用更深一階的黃色底（約 16% alpha）以示 hover

### Requirement: 統計卡片風格

統計卡片（用於價格圖表頁的最高／最低／平均，以及抓取狀態頁的追蹤／成功／失敗數）SHALL 以「整卡塊面」取代原本「左側色條 + 數字」的樣式。每張統計卡片 MUST：

- 具備背景色類別（如 `.stat-scoot--ink` 近黑、`.stat-scoot--yellow` 亮黃、`.stat-scoot--success`、`.stat-scoot--danger`、`.stat-scoot--slate`），各自搭配 AA 對比的文字色。
- 主數值使用 `var(--font-mono)`、字級 `2.25rem`、字重 800。
- 說明 label 使用 `var(--font-body)`、uppercase、`letter-spacing: 0.08em`、字級 `0.75rem`，放置於數值上方。
- 於卡片右下角 MAY 加入半透明圓點或打孔裝飾（登機證意象），不得遮擋主數值。

AA 對比對照（必須符合）：

- 黃底 `.stat-scoot--yellow` 搭配 `var(--scoot-ink)` 文字（禁止白字）。
- 近黑底 `.stat-scoot--ink` 搭配 `#ffffff` 白色文字。
- 綠／紅／灰底搭配 `#ffffff` 白色文字。

#### Scenario: 統計卡片顯示
- **WHEN** 頁面載入統計區塊
- **THEN** 每張統計卡片 SHALL 顯示整卡塊面背景色、位於上方的 uppercase label、大字號 mono 字體主數值

#### Scenario: 黃底不得白字
- **WHEN** 開發者檢視 `.stat-scoot--yellow` 樣式
- **THEN** 其文字顏色 MUST 為 `var(--scoot-ink)` 或等效深色，禁止出現 `#fff` 或 `white`

### Requirement: Badge 樣式

Badge SHALL 採圓角 pill（`border-radius: 999px`）、字重 700、字級 `0.75rem`、uppercase、內距 `0.35em 0.75em`。系統 SHALL 至少提供三種 badge 類別：

- success：`var(--scoot-success)` 12% alpha 底色 + `var(--scoot-success)` 文字
- danger：`var(--scoot-danger)` 12% alpha 底色 + `var(--scoot-danger)` 文字
- muted：`var(--scoot-muted)` 12% alpha 底色 + `var(--scoot-slate)` 文字

#### Scenario: 班機啟用 / 停用 badge
- **WHEN** 班機管理頁顯示每筆班機的啟用狀態
- **THEN** 啟用 SHALL 渲染為 success badge（綠色文字 + 淡綠底 pill），停用 SHALL 渲染為 muted badge（灰色系 pill）

#### Scenario: 抓取成功 / 失敗 badge
- **WHEN** 抓取狀態頁顯示抓取紀錄
- **THEN** 成功列 SHALL 顯示 success badge，失敗列 SHALL 顯示 danger badge

### Requirement: Alert 樣式

Alert 元件 SHALL 使用 `12px` 圓角、白色背景（`var(--scoot-surface)`），並以左側 `6px` 實色粗邊指示語意（info 藍、success 綠、warning 橘、danger 紅）。文字顏色 MUST 為 `var(--scoot-ink)`；標題／強調文字字重 600；關閉按鈕（若存在）需可聚焦。

#### Scenario: 資訊 alert 顯示
- **WHEN** 頁面出現 Bootstrap `.alert-info` 或本主題對應類別
- **THEN** alert SHALL 顯示白底、左側 6px 藍色粗邊、`var(--scoot-ink)` 深色文字

### Requirement: Chart.js 配色

價格趨勢圖（`charts.html` 內 Chart.js 線圖）SHALL 採用以下配色：

- 線條（borderColor）：`#0E0E10`（`--scoot-ink`）
- 填滿區（backgroundColor）：`rgba(14, 14, 16, 0.08)` 或等效的 `--scoot-ink` 低透明度
- 資料點：填色 `#FFDA00`（`--scoot-yellow`）、邊框 `#0E0E10`、邊框寬度 ≥ 2px
- Grid line：`rgba(14, 14, 16, 0.06)`
- 座標刻度文字：`#4A4A55`（`--scoot-slate`）
- Tooltip：背景 `#0E0E10`、文字 `#ffffff`、價格數值顏色 `#FFDA00`
- Legend：文字色 `#0E0E10`、字重 600

#### Scenario: 圖表線條與資料點
- **WHEN** 使用者選擇某班機並載入價格趨勢圖
- **THEN** 折線 SHALL 以近黑色繪製，資料點 SHALL 呈黃色填色搭配近黑色邊框

#### Scenario: Tooltip 配色
- **WHEN** 使用者將滑鼠移至圖表資料點
- **THEN** Tooltip SHALL 顯示深色背景、白色標籤與黃色票價數值

### Requirement: 可及性（Accessibility）

主題 SHALL 滿足 WCAG 2.1 AA 的對比與操作指引：

- 所有文字對比 MUST ≥ 4.5:1（AA 正文），大字（≥ 18pt 或 14pt bold）≥ 3:1。
- `var(--scoot-yellow)` 背景 MUST 僅搭配 `var(--scoot-ink)` 或等效深色文字；禁止黃底白字。
- 所有互動元素（按鈕、連結、表單）MUST 提供清楚的 `:focus-visible` 樣式，與預設狀態可視覺區分。
- 狀態（成功／失敗／停用）MUST 不只靠顏色區分，必須同時顯示文字標籤或 icon。
- 主題 MUST 尊重 `prefers-reduced-motion: reduce`：在此媒體查詢下，按鈕 active 位移、卡片互動動畫、hover transition 皆 MUST 停用或縮短至 `0.01ms`。

#### Scenario: 黃底文字對比
- **WHEN** 開發者於 `.navbar-scoot`、`.btn-scoot`、`.stat-scoot--yellow` 或任何使用 `--scoot-yellow` 背景的元件上檢視文字色
- **THEN** 文字顏色 MUST 為 `var(--scoot-ink)` 或其他與 `#FFDA00` 對比 ≥ 4.5:1 的深色

#### Scenario: 鍵盤聚焦可見
- **WHEN** 使用者以 Tab 鍵依序聚焦導航連結、按鈕、表單欄位
- **THEN** 每個聚焦元素 SHALL 顯示至少 `2px` 寬的 `:focus-visible` 描邊，且描邊與該元件背景對比 ≥ 3:1

#### Scenario: 減少動畫偏好
- **WHEN** 使用者系統偏好設定為 `prefers-reduced-motion: reduce`
- **THEN** 所有按鈕 active 位移、卡片 hover transition、alert 淡入 MUST 停用或動畫時間 ≤ 0.01ms
