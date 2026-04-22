## MODIFIED Requirements

### Requirement: 酷航品牌色彩 Tokens

系統 SHALL 在 `app/static/css/style.css` 的 `:root[data-theme="scoot"]` scope 中定義酷航品牌的 CSS 自訂屬性色彩 tokens（原先置於 `:root` 無屬性限定，現改為以 data-theme 屬性作為啟用 scope）；並於同一 scope 內將中性語意 tokens（`--theme-*`）映射至對應 `--scoot-*` 品牌 token。元件 CSS MUST 透過 `var(--theme-*)` 引用色彩（不再直接使用 `var(--scoot-*)`），以達成多主題架構下的即時切換。

色彩 tokens 內容（允許 ±1% 明度微調，不得改變色相，與先前版本一致）：

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

中性 tokens 映射（於 `:root[data-theme="scoot"]` 內）：`--theme-primary: var(--scoot-yellow)`、`--theme-primary-bright: var(--scoot-yellow-bright)`、`--theme-primary-deep: var(--scoot-yellow-deep)`、`--theme-accent: var(--scoot-ink)`（Scoot 以近黑為 accent）、`--theme-accent-deep: #000000`、`--theme-ink: var(--scoot-ink)`、`--theme-ink-soft: var(--scoot-ink-soft)`、`--theme-slate: var(--scoot-slate)`、`--theme-muted: var(--scoot-muted)`、`--theme-canvas: var(--scoot-canvas)`、`--theme-surface: var(--scoot-surface)`、`--theme-line: var(--scoot-line)`、`--theme-success: var(--scoot-success)`、`--theme-danger: var(--scoot-danger)`、`--theme-warn: var(--scoot-warn)`、`--theme-info: var(--scoot-info)`。

#### Scenario: 色彩 tokens 於頁面載入時可用
- **WHEN** 使用者載入任一頁面（`/`、`/flights`、`/charts`、`/status`）且 `<html data-theme="scoot">`
- **THEN** 瀏覽器計算樣式中 SHALL 解析到上述 14 項 `--scoot-*` CSS 自訂屬性，且對應色碼與本 Requirement 定義一致

#### Scenario: 元件透過中性 tokens 引用色彩
- **WHEN** 開發者檢視 `app/static/css/style.css` 中任一元件樣式規則
- **THEN** 涉及色彩的屬性（`color`、`background`、`border-color` 等）MUST 使用 `var(--theme-*)` 形式，不得使用 `var(--scoot-*)` 或硬編碼色碼（允許例外：`rgba()` 中以 token 色衍生的透明度表示，或純 `#ffffff`、`transparent`、`currentColor` 等中性值）

#### Scenario: data-theme 未指定時預設 scoot
- **WHEN** `<html>` 未指定 `data-theme` 屬性（例：FOUC script 尚未執行完畢，或屬性被移除）
- **THEN** `app/static/css/style.css` MUST 提供 fallback，使 `:root:not([data-theme])` 或等效 selector 套用與 `[data-theme="scoot"]` 相同的 token 映射；MUST 不得出現整頁無樣式的情況

### Requirement: 字體堆疊

系統 SHALL 於 `:root[data-theme="scoot"]` scope 中為頁面提供三組中性 CSS 自訂屬性字體堆疊（`--theme-font-display`、`--theme-font-body`、`--theme-font-mono`），並映射至品牌堆疊變數 `--font-display` / `--font-body` / `--font-mono`（保留既有命名以利除錯）；字體堆疊 MUST 包含西文優先字型、繁體中文 fallback 與系統字型 fallback，確保任一環境皆可渲染。

- `--font-display` / `--theme-font-display`：起首 `"Nunito"`，fallback 依序包含 `"Poppins"`、`"PingFang TC"`、`"Noto Sans TC"`、`-apple-system`、`BlinkMacSystemFont`、`"Helvetica Neue"`、`sans-serif`
- `--font-body` / `--theme-font-body`：起首 `"Nunito Sans"`，fallback 依序包含 `"Poppins"`、`"PingFang TC"`、`"Noto Sans TC"`、`-apple-system`、`BlinkMacSystemFont`、`sans-serif`
- `--font-mono` / `--theme-font-mono`：起首 `"JetBrains Mono"`，fallback 依序包含 `"Fira Code"`、`"Roboto Mono"`、`ui-monospace`、`monospace`

`body` 元素預設使用 `--theme-font-body`；所有標題元素（`h1`–`h3`）與品牌文字 MUST 使用 `--theme-font-display`；票價／金額／班次代碼等數字資訊 MUST 使用 `--theme-font-mono`。

#### Scenario: Body 套用內文字體
- **WHEN** 頁面載入完成且 `data-theme="scoot"`
- **THEN** `<body>` 元素的 computed style `font-family` SHALL 以 `Nunito Sans` 開頭，且字串中 SHALL 包含 `PingFang TC` 與 `Noto Sans TC`

#### Scenario: 標題套用 display 字體
- **WHEN** `data-theme="scoot"` 下頁面中出現 `<h2>` 主標題
- **THEN** 該元素 computed style `font-family` SHALL 以 `Nunito` 開頭，字重 SHALL ≥ 700

#### Scenario: 票價使用 mono 字體
- **WHEN** `data-theme="scoot"` 下頁面呈現票價、班次代碼或統計數值（統計卡片的 `.stat-scoot-value` / `.stat-theme-value`、表格的價格欄、圖表 tooltip 價格）
- **THEN** 該文字 computed style `font-family` SHALL 包含 `JetBrains Mono` 或其 fallback `monospace`

### Requirement: 按鈕系統

系統 SHALL 透過中性 class（`.btn-theme`、`.btn-theme-secondary`、`.btn-theme-danger`、`.btn-theme-success`、`.btn-theme-warning`）提供五種按鈕層級，並保留既有 `.btn-scoot`、`.btn-scoot-secondary`、`.btn-scoot-danger`、`.btn-scoot-success`、`.btn-scoot-warning` 作為別名 selector（與中性 class 於同一 CSS rule group 中共用 declarations）。每一層級的按鈕 SHALL：

- 使用 `var(--theme-btn-radius)` 圓角（Scoot 下為 `10px`）、`var(--theme-font-display)` 字重 700、內距 `0.55rem 1.25rem`。
- 具備 `var(--theme-btn-press-width)` solid 底部「按壓邊」（Scoot 下為 `3px`）；color 為對應主色的深階變體（如 `var(--theme-primary-deep)`）。
- `:active` 狀態 MUST 套用 `transform: translateY(1px)` 並移除或縮短底邊（Scoot 條件下），模擬按壓；當 `prefers-reduced-motion: reduce` 時 MUST 停用此 transform。
- `:focus-visible` MUST 顯示 `2px` 外描邊（`var(--theme-ink)`）與 `2px` offset，以符合鍵盤操作可及性。

層級對照表（`data-theme="scoot"` 下色彩／文字必須符合，與先前版本等效；其他 data-theme 以各自 spec 定義的 token 映射為準）：

| 層級 | 背景 | 文字 | 底邊色 |
|------|------|------|--------|
| primary | `var(--theme-primary)` | `var(--theme-ink)` | `var(--theme-primary-deep)` |
| secondary | `transparent` | `var(--theme-ink)` | `var(--theme-ink)`（2px 邊框代替） |
| danger | `var(--theme-danger)` | `#ffffff` | `#b91c1c`（scoot）／ `var(--theme-accent-deep)`（其他主題可覆寫） |
| success | `var(--theme-success)` | `#ffffff` | `#158A4F`（scoot） |
| warning | `var(--theme-warn)` | `var(--theme-ink)` | `#D9690F`（scoot） |

#### Scenario: 主按鈕樣式
- **WHEN** `data-theme="scoot"` 下頁面出現主操作按鈕（`.btn-theme` 或其別名 `.btn-scoot`）
- **THEN** 按鈕 SHALL 顯示 `#FFDA00` 背景、`#0E0E10` 文字、`10px` 圓角、底部 `3px` 深黃按壓邊

#### Scenario: 危險按鈕樣式
- **WHEN** `data-theme="scoot"` 下頁面出現 `.btn-theme-danger` 或 `.btn-scoot-danger`
- **THEN** 按鈕 SHALL 顯示紅色底、白色文字、`10px` 圓角、底部 `3px` 暗紅按壓邊

#### Scenario: 按下反饋
- **WHEN** 使用者滑鼠點擊任一 `btn-theme*` / `btn-scoot*` 並處於 `:active` 狀態，且 `prefers-reduced-motion` 非 `reduce`
- **THEN** 按鈕 SHALL 套用 `translateY(1px)` 向下位移；若 `prefers-reduced-motion: reduce`，則 MUST 不套用 transform

#### Scenario: 鍵盤聚焦可見
- **WHEN** 使用者以鍵盤 Tab 至任一 `btn-theme*` / `btn-scoot*`
- **THEN** 按鈕 SHALL 顯示 `2px` 可見外描邊與 `2px` offset（或等效高對比聚焦指示）

### Requirement: Chart.js 配色

價格趨勢圖（`charts.html` 內 Chart.js 線圖）SHALL 透過 `getComputedStyle(document.documentElement).getPropertyValue('--theme-<token>').trim()` 動態取得主題色，不得硬編色碼；配色語意對應如下（各主題下實際色碼由該主題 tokens 決定，於 `data-theme="scoot"` 下需等效於先前版本）：

- 線條（borderColor）：`var(--theme-ink)`（Scoot：`#0E0E10`）
- 填滿區（backgroundColor）：`var(--theme-ink)` 約 8% alpha
- 資料點：填色 `var(--theme-primary)`（Scoot：`#FFDA00`）、邊框 `var(--theme-ink)`、邊框寬度 ≥ 2px
- Grid line：`var(--theme-ink)` 約 6% alpha
- 座標刻度文字：`var(--theme-slate)`（Scoot：`#4A4A55`）
- Tooltip：背景 `var(--theme-ink)`、文字 `#ffffff`、價格數值顏色 `var(--theme-primary)`（Scoot 下為 `#FFDA00`）
- Legend：文字色 `var(--theme-ink)`、字重 600

Chart.js 實例 MUST 監聽 `document` 的 `themechange` CustomEvent；事件觸發時 MUST 重新計算上述色彩並呼叫 `chart.update()` 以套用新主題。

#### Scenario: 圖表線條與資料點
- **WHEN** 使用者於 `data-theme="scoot"` 選擇某班機並載入價格趨勢圖
- **THEN** 折線 SHALL 以近黑色繪製，資料點 SHALL 呈黃色填色搭配近黑色邊框

#### Scenario: Tooltip 配色
- **WHEN** 使用者於 `data-theme="scoot"` 將滑鼠移至圖表資料點
- **THEN** Tooltip SHALL 顯示深色背景、白色標籤與黃色票價數值

#### Scenario: 主題切換後圖表重繪
- **WHEN** 使用者於 `/charts?flight_id=<id>` 頁面切換主題（觸發 `themechange` event）
- **THEN** Chart.js 實例 MUST 呼叫 `chart.update()`；折線 `borderColor`、資料點 `backgroundColor` SHALL 更新為新主題對應的 `--theme-ink` 與 `--theme-primary` 色碼
