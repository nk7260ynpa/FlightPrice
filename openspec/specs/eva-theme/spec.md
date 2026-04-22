### Requirement: 長榮航空品牌色彩 Tokens

系統 SHALL 於 `app/static/css/style.css` 的 `:root[data-theme="eva"]` scope 中定義長榮航空品牌 CSS 自訂屬性色彩 tokens，並將中性語意 tokens（`--theme-*`）映射至對應品牌 token。色碼如下（允許 ±1% 明度微調，不得改變色相）：

品牌原生 tokens：

- `--eva-primary: #005F3C`（長榮深綠，主色）
- `--eva-primary-bright: #00744A`（hover 提亮）
- `--eva-primary-deep: #004429`（按壓邊）
- `--eva-accent: #D4A84B`（品牌金 / 商務金）
- `--eva-accent-deep: #A6822F`（金色按壓邊）
- `--eva-ink: #15241C`（主文字）
- `--eva-ink-soft: #2A3B33`
- `--eva-slate: #4E5B55`
- `--eva-muted: #8A938F`
- `--eva-canvas: #F6F4EE`（暖米白）
- `--eva-surface: #FFFFFF`
- `--eva-line: #DDE3DD`
- `--eva-success: #2E8B57`
- `--eva-danger: #B83A2E`
- `--eva-warn: #C68A1C`
- `--eva-info: #2B5AA0`

中性 tokens 映射（於同一 scope 內）：`--theme-primary: var(--eva-primary)`、`--theme-primary-bright: var(--eva-primary-bright)`、`--theme-primary-deep: var(--eva-primary-deep)`、`--theme-accent: var(--eva-accent)`、`--theme-accent-deep: var(--eva-accent-deep)`、`--theme-ink: var(--eva-ink)`、`--theme-ink-soft: var(--eva-ink-soft)`、`--theme-slate: var(--eva-slate)`、`--theme-muted: var(--eva-muted)`、`--theme-canvas: var(--eva-canvas)`、`--theme-surface: var(--eva-surface)`、`--theme-line: var(--eva-line)`、`--theme-success: var(--eva-success)`、`--theme-danger: var(--eva-danger)`、`--theme-warn: var(--eva-warn)`、`--theme-info: var(--eva-info)`。

#### Scenario: EVA 色彩 tokens 可解析
- **WHEN** 使用者瀏覽任一頁面且 `<html data-theme="eva">`
- **THEN** 瀏覽器 computed style SHALL 解析 16 項 `--eva-*` token 與 16 項 `--theme-*` 色彩 token，色碼對應本 Requirement 定義

#### Scenario: EVA CSS 規則存在於 style.css
- **WHEN** 開發者檢視 `app/static/css/style.css`
- **THEN** 檔案 MUST 包含 `:root[data-theme="eva"]` selector，且該 block 內 MUST 出現字串 `#005F3C` 與 `#D4A84B`

### Requirement: 長榮字體堆疊

`:root[data-theme="eva"]` scope MUST 設定：

- `--theme-font-display`：起首 `"Noto Serif TC"`，fallback 依序 `"Source Serif Pro"`、`"Georgia"`、`"PingFang TC"`、`serif`
- `--theme-font-body`：起首 `"Source Sans 3"`，fallback 依序 `"Noto Sans TC"`、`"PingFang TC"`、`-apple-system`、`BlinkMacSystemFont`、`sans-serif`
- `--theme-font-mono`：起首 `"IBM Plex Mono"`，fallback 依序 `"JetBrains Mono"`、`ui-monospace`、`monospace`

`app/templates/base.html` 的 Google Fonts `<link>` MUST 載入 `Noto Serif TC`、`Source Sans 3`、`IBM Plex Mono` 等字型 family（可合併於單一 URL）。

#### Scenario: EVA 主題 body 字體
- **WHEN** `<html data-theme="eva">` 載入完成
- **THEN** `<body>` computed `font-family` SHALL 以 `Source Sans 3` 開頭

#### Scenario: EVA 主題 display 字體
- **WHEN** `<html data-theme="eva">` 下頁面出現 `<h2>`
- **THEN** 該元素 computed `font-family` SHALL 以 `Noto Serif TC` 開頭

### Requirement: 長榮 Navbar 視覺

`<html data-theme="eva">` 下 `.navbar-theme`（或其別名 `.navbar-scoot`）SHALL：

- 背景 `var(--theme-primary)`（即 `#005F3C` 深綠）
- 底部裝飾線 `1px solid var(--theme-accent)`（金色細線，取代 Scoot 的 4px 粗撕線）
- 導航品牌文字（`.navbar-brand`）MUST 為 `#FFFFFF` 白色、使用 `--theme-font-display` 字重 800
- 導航連結（`.nav-link`）MUST 為 `#FFFFFF` 白色，active 狀態 MUST 為 `var(--theme-accent)` 金色實底 + `var(--theme-primary)` 深綠字

#### Scenario: EVA Navbar 顯示
- **WHEN** 使用者於 `data-theme="eva"` 下瀏覽任一頁面
- **THEN** 頂部 navbar 背景 SHALL 為深綠 `#005F3C`，底部 SHALL 為 1px 金色細線；品牌文字與連結 SHALL 為白色

### Requirement: 長榮按鈕與元件樣式

`<html data-theme="eva">` 下的按鈕、統計卡裝飾與表格 SHALL 採商務沉穩配置，元件規則 MUST 符合下列條件：

- `--theme-btn-press-width: 3px`、`--theme-btn-radius: 10px`（與 Scoot 共用按壓金屬感）
- 主按鈕（`.btn-theme` / `.btn-scoot`）背景 `var(--theme-primary)`、文字 `#FFFFFF`、底邊 `3px solid var(--theme-primary-deep)`
- 次按鈕（`.btn-theme-secondary`）透明底 + `2px solid var(--theme-primary)` 邊、文字 `var(--theme-primary)`
- 危險按鈕（`.btn-theme-danger`）背景 `var(--theme-danger)`、文字 `#FFFFFF`
- `--theme-stat-motif`：`linear-gradient(45deg, transparent 45%, var(--theme-accent) 45%, var(--theme-accent) 55%, transparent 55%)`（統計卡右下角金色斜線折角裝飾）
- 表格 `.table-theme` 表頭 MUST 為 `var(--theme-primary)` 深綠底、白字；表身偶數列 MUST 為 `var(--theme-accent)` 10% alpha 的淡金底

#### Scenario: EVA 主按鈕樣式
- **WHEN** `<html data-theme="eva">` 下頁面出現主操作按鈕
- **THEN** 按鈕 SHALL 顯示深綠 `#005F3C` 背景、白色文字、`10px` 圓角、底部 `3px solid #004429` 按壓邊

#### Scenario: EVA 表格表頭配色
- **WHEN** `<html data-theme="eva">` 下載入 `.table-theme`（或 `.table-scoot`）資料表
- **THEN** 表頭 `thead th` SHALL 為深綠 `#005F3C` 底色搭配白色文字

### Requirement: 長榮主題 AA 對比底線

`<html data-theme="eva">` 下所有文字 SHALL 符合 WCAG 2.1 AA（4.5:1）：

- 深綠 `#005F3C` 底 + 白字對比 ≥ 7:1（AAA 過關）
- 金色 `#D4A84B` 底 MUST 僅搭配 `var(--theme-ink)` 深色文字；禁止白字。
- `.stat-theme--primary`（亮綠底變體）MUST 使用白字、`.stat-theme--accent`（若採金底）MUST 使用 `var(--theme-ink)`。

#### Scenario: EVA 金底禁白字
- **WHEN** 開發者檢視任何使用 `var(--theme-accent)`（金色）為背景的元件樣式
- **THEN** 其文字 MUST 為 `var(--theme-ink)` 或等效深色，不得為 `#ffffff`、`white` 或白色等效色
