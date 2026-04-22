### Requirement: 中華航空品牌色彩 Tokens

系統 SHALL 於 `app/static/css/style.css` 的 `:root[data-theme="china-airlines"]` scope 中定義中華航空品牌 CSS 自訂屬性色彩 tokens，並將中性語意 tokens（`--theme-*`）映射至對應品牌 token。色碼如下（允許 ±1% 明度微調，不得改變色相）：

品牌原生 tokens：

- `--cal-primary: #003F87`（CAL 國航藍，主色）
- `--cal-primary-bright: #0A4FA3`（hover 提亮）
- `--cal-primary-deep: #002C5F`（按壓邊）
- `--cal-accent: #C8102E`（CI 紅，梅花色）
- `--cal-accent-deep: #8F0A20`（紅色按壓邊）
- `--cal-ink: #0F1B33`（主文字，偏藍調深色）
- `--cal-ink-soft: #2A334A`
- `--cal-slate: #4F5870`
- `--cal-muted: #8C93A4`
- `--cal-canvas: #F5F6FA`（冷米白）
- `--cal-surface: #FFFFFF`
- `--cal-line: #DDE1EC`
- `--cal-success: #2E8B4A`
- `--cal-danger: #C8102E`
- `--cal-warn: #D98200`
- `--cal-info: #1A5CB0`

中性 tokens 映射：於同一 scope 內將 `--theme-*` 各項（`--theme-primary`、`--theme-primary-bright`、`--theme-primary-deep`、`--theme-accent`、`--theme-accent-deep`、`--theme-ink`、`--theme-ink-soft`、`--theme-slate`、`--theme-muted`、`--theme-canvas`、`--theme-surface`、`--theme-line`、`--theme-success`、`--theme-danger`、`--theme-warn`、`--theme-info`）設為對應 `var(--cal-*)`。

#### Scenario: 中華色彩 tokens 可解析
- **WHEN** 使用者瀏覽任一頁面且 `<html data-theme="china-airlines">`
- **THEN** 瀏覽器 computed style SHALL 解析 16 項 `--cal-*` token 與 16 項 `--theme-*` 色彩 token，色碼對應本 Requirement 定義

#### Scenario: 中華 CSS 規則存在於 style.css
- **WHEN** 開發者檢視 `app/static/css/style.css`
- **THEN** 檔案 MUST 包含 `:root[data-theme="china-airlines"]` selector，且該 block 內 MUST 出現字串 `#003F87` 與 `#C8102E`

### Requirement: 中華字體堆疊

`:root[data-theme="china-airlines"]` scope MUST 設定：

- `--theme-font-display`：起首 `"Noto Serif TC"`，fallback 依序 `"Playfair Display"`、`"Times New Roman"`、`"PingFang TC"`、`serif`
- `--theme-font-body`：起首 `"Source Sans 3"`，fallback 依序 `"Noto Sans TC"`、`"PingFang TC"`、`-apple-system`、`BlinkMacSystemFont`、`sans-serif`
- `--theme-font-mono`：起首 `"JetBrains Mono"`，fallback 依序 `"IBM Plex Mono"`、`ui-monospace`、`monospace`

`app/templates/base.html` 的 Google Fonts `<link>` MUST 載入 `Noto Serif TC`、`Source Sans 3`（可與 EVA 主題共用）；`Playfair Display` MAY 作為進一步襯線備選字型。

#### Scenario: 中華主題 body 字體
- **WHEN** `<html data-theme="china-airlines">` 載入完成
- **THEN** `<body>` computed `font-family` SHALL 以 `Source Sans 3` 開頭

#### Scenario: 中華主題 display 字體
- **WHEN** `<html data-theme="china-airlines">` 下頁面出現 `<h2>`
- **THEN** 該元素 computed `font-family` SHALL 以 `Noto Serif TC` 開頭

### Requirement: 中華 Navbar 視覺

`<html data-theme="china-airlines">` 下 `.navbar-theme`（或其別名 `.navbar-scoot`）SHALL：

- 背景 `var(--theme-primary)`（即 `#003F87` 國航藍）
- 底部裝飾線 `3px solid var(--theme-accent)`（紅色粗邊，呼應 CI logo 與國旗意象）
- 導航品牌文字 MUST 為 `#FFFFFF` 白色、字重 800
- 導航連結（`.nav-link`）MUST 為 `#FFFFFF` 白色，active 狀態 MUST 為 `var(--theme-accent)` 紅色實底 + `#FFFFFF` 白字

#### Scenario: 中華 Navbar 顯示
- **WHEN** 使用者於 `data-theme="china-airlines"` 下瀏覽任一頁面
- **THEN** 頂部 navbar 背景 SHALL 為深藍 `#003F87`、底部 SHALL 為 3px 紅色粗邊 `#C8102E`、品牌文字與連結 SHALL 為白色

### Requirement: 中華按鈕與元件樣式

`<html data-theme="china-airlines">` 下的按鈕、統計卡裝飾與表格 SHALL 呼應國航正式氣質，元件規則 MUST 符合下列條件：

- `--theme-btn-press-width: 3px`、`--theme-btn-radius: 10px`
- 主按鈕（`.btn-theme` / `.btn-scoot`）背景 `var(--theme-primary)`、文字 `#FFFFFF`、底邊 `3px solid var(--theme-primary-deep)`
- 次按鈕（`.btn-theme-secondary`）透明底 + `2px solid var(--theme-primary)` 邊、文字 `var(--theme-primary)`
- 危險按鈕（`.btn-theme-danger`）背景 `var(--theme-accent)`（CI 紅 `#C8102E`）、文字 `#FFFFFF`、底邊 `3px solid var(--theme-accent-deep)`
- `--theme-stat-motif`：以 inline SVG data URI 表達半透明 `var(--theme-accent)` 色的 5 瓣梅花（plum blossom）圖案，尺寸約 12px，位於統計卡右下角 `::after`（呼應 CI logo）
- 表格 `.table-theme` 表頭 MUST 為 `var(--theme-primary)` 國航藍底、白字；表身偶數列 MUST 為 `var(--theme-primary)` 6% alpha 的極淡藍底

#### Scenario: 中華主按鈕樣式
- **WHEN** `<html data-theme="china-airlines">` 下頁面出現主操作按鈕
- **THEN** 按鈕 SHALL 顯示深藍 `#003F87` 背景、白色文字、`10px` 圓角、底部 `3px solid #002C5F` 按壓邊

#### Scenario: 中華危險按鈕配色
- **WHEN** `<html data-theme="china-airlines">` 下出現 `.btn-theme-danger` 或 `.btn-scoot-danger`
- **THEN** 按鈕 SHALL 顯示 CI 紅 `#C8102E` 背景、白色文字、底部 `3px solid #8F0A20` 按壓邊

### Requirement: 中華主題 AA 對比底線

`<html data-theme="china-airlines">` 下所有文字 SHALL 符合 WCAG 2.1 AA（4.5:1）：

- 深藍 `#003F87` 底 + 白字對比 ≥ 8:1（AAA 過關）
- CI 紅 `#C8102E` 底 + 白字對比 ≥ 5.5:1（AA 過關）
- 梅花裝飾 MUST 以半透明 alpha 呈現，不得遮擋主數值或文字。

#### Scenario: 中華深藍底白字對比
- **WHEN** 開發者檢視 `.navbar-theme`（`data-theme="china-airlines"`）與主按鈕文字
- **THEN** 文字色 MUST 為 `#FFFFFF` 或等效白色，與 `#003F87` 底色對比 ≥ 4.5:1
