## Context

FlightPrice 目前單一主題（Scoot）直接寫在 `:root`，所有元件 CSS 使用 `var(--scoot-*)` 引用。若要支援 4 個主題且即時切換，必須在同一份 `style.css` 內建立「主題 scope」機制，同時讓元件 CSS 不再綁死特定品牌 token 名，否則每次切換都要重算 class 對應，無法達成「切換屬性值即整頁換風」的即時體驗。

受影響的現有檔案為 `app/static/css/style.css`（單一 CSS）、`app/templates/base.html`（單一模板根）、`app/templates/charts.html`（Chart.js 配置硬編色碼）。`tests/test_theme_smoke.py` 已針對預設 Scoot 主題做 22 項以上 class／靜態 CSS 斷言，這些斷言必須在 data-theme="scoot" 情境下持續通過。

使用者需求中三個新主題各有鮮明性格：長榮（商務沉穩）、中華（國航正式）、星宇（精品奢華）。若僅是色票替換而沿用 Scoot 的「粗邊按壓、打孔裝飾」，星宇的精品氣質會被破壞。因此設計必須支援「同架構下允許元件層有主題微差異」的能力。

## Goals / Non-Goals

**Goals**：

- 4 個主題（scoot / eva / china-airlines / starlux）共用一份 `style.css`，透過 `<html data-theme="...">` 切換。
- 元件 CSS 一律引用「中性語意 tokens」（`--theme-primary`、`--theme-ink`、`--theme-canvas` 等），品牌色票集中於 `[data-theme="..."]` scope 內映射。
- 使用者切換主題後 **不刷新頁面即可套用**，且在 localStorage 持久化；下次進站自動恢復。
- 防止首屏主題閃爍（FOUC-like flash）：透過 `<head>` 內 inline script 在樣式計算前就設定 `data-theme`。
- 向下相容：所有既有 `.scoot-*` class 保留為別名；現有 `tests/test_theme_smoke.py` 斷言在預設 scoot 主題下依然通過。
- Chart.js 色彩透過 `getComputedStyle` 讀取 CSS custom properties，主題切換時重繪圖表使用新色。
- 可及性：四個主題皆 MUST 通過 WCAG AA 對比（4.5:1）；禁止品牌主色底搭配白字造成對比不足。

**Non-Goals**：

- 不實作使用者自訂主題（自選色）。
- 不實作系統暗／亮模式（`prefers-color-scheme`）自動切換；主題是品牌性質，非色彩模式。
- 不支援伺服器端記憶使用者主題（不建立資料表、不寫 cookie 後端讀取）；持久化僅在瀏覽器端。
- 不改變現有業務邏輯、資料模型與 Python 路由。

## Decisions

### D1：主題切換實作方式 — 採「`<html data-theme>` + CSS custom properties scope」

**選擇**：`<html data-theme="eva">` 為切換開關，CSS 以 `:root[data-theme="eva"] { --theme-primary: ... }` 定義各主題 token，元件 CSS 只使用中性 token（如 `var(--theme-primary)`）。

**替代方案**：

- (A) 分檔多個 CSS（`style-scoot.css`、`style-eva.css`…），切換時 swap `<link>`：**否決**。每次切換都要 HTTP 請求不同 CSS，首屏有 flash，無法即時切換；且 4 份 CSS 維護元件規則重複率極高。
- (B) class 切換（`<body class="theme-eva">`）：**否決**。與 `data-theme` 屬性相比語意較弱，且 CSS 選擇器特異度（specificity）不如 attribute + `:root`，且 `html` 層級較 `body` 更能涵蓋 `<meta theme-color>` 等未來擴充。

**理由**：data-theme 屬性切換為純 DOM 屬性寫入，由瀏覽器引擎即時套用所有 `[data-theme="..."]` 選擇器，零 HTTP 請求、零 flash（配合 inline script）、易於測試（只需檢查屬性值）。

### D2：中性 token 命名 — `--theme-*` 前綴

所有元件 CSS 引用的 token 統一改為 `--theme-*`：

- 色彩：`--theme-primary`、`--theme-primary-bright`、`--theme-primary-deep`、`--theme-accent`、`--theme-accent-deep`、`--theme-ink`、`--theme-ink-soft`、`--theme-slate`、`--theme-muted`、`--theme-canvas`、`--theme-surface`、`--theme-line`、`--theme-success`、`--theme-danger`、`--theme-warn`、`--theme-info`
- 字體：`--theme-font-display`、`--theme-font-body`、`--theme-font-mono`
- 半徑：`--theme-radius-sm`、`--theme-radius`、`--theme-radius-lg`
- navbar／按鈕／stat 特殊屬性：`--theme-navbar-bg`、`--theme-navbar-accent-line`（navbar 底部裝飾色與粗度）、`--theme-btn-press-width`（按鈕按壓邊粗度，Scoot/EVA/CAL=3px、Starlux=0px）、`--theme-btn-radius`、`--theme-stat-motif`（統計卡右下角 `::after` 裝飾的 background）

**品牌原生 token 保留**：`--scoot-*`、`--eva-*`、`--cal-*`、`--jx-*` 仍於各自 scope 定義，但元件 CSS 只引用 `--theme-*`，品牌 token 僅作為「映射來源」供除錯與延伸使用。

### D3：Class 命名策略 — 中性 class 為主、`.*-scoot` 別名向下相容

- 新增中性 class：`.navbar-theme`、`.btn-theme`、`.btn-theme-secondary`、`.btn-theme-danger`、`.btn-theme-success`、`.btn-theme-warning`、`.table-theme-wrap`、`.table-theme`、`.stat-theme`、`.stat-theme--ink`、`.stat-theme--primary`、`.stat-theme--accent`、`.stat-theme--success`、`.stat-theme--danger`、`.stat-theme--slate`、`.badge-theme-success`、`.badge-theme-danger`、`.badge-theme-muted`、`.card-header-theme`。
- 既有 class 別名：`.navbar-scoot`、`.btn-scoot`、`.btn-scoot-secondary/danger/success/warning`、`.table-scoot-wrap`、`.table-scoot`、`.stat-scoot`、`.stat-scoot--ink/yellow/success/danger/slate`、`.badge-scoot-success/danger/muted`、`.card-header-scoot` 以 selector 群組方式指向同一組樣式規則，保持視覺 identical。模板可保留使用 `.scoot-*` class（測試依此驗證不破壞）。

**理由**：原 `tests/test_theme_smoke.py` 驗證 `navbar-scoot`、`btn-scoot`、`btn-scoot-danger`、`table-scoot`、`badge-scoot-success`、`stat-scoot--ink/danger/success` 等 class 存在；若刪除會破壞既有測試。保留別名同時引入中性 class，讓後續新 template／新頁面可以只使用中性 class。

### D4：Starlux 按鈕與裝飾差異化

Starlux 為精品風格，`--theme-btn-press-width: 0px`（不顯示 3px 粗底邊）；按壓回饋改用：

- `box-shadow: inset 0 1px 0 rgba(0,0,0,0.15)` 模擬微凹
- `transform: translateY(0.5px)`（若 `prefers-reduced-motion` 則停用）
- `border-radius: var(--theme-btn-radius)`，Starlux 主題下 `--theme-btn-radius: 4px`（editorial 感），其他三主題 `10px`

Stat card 右下角裝飾透過 `--theme-stat-motif` 以 `background-image` 注入：

- Scoot：半透明圓點（登機證打孔）— `radial-gradient(circle, rgba(14,14,16,0.2) 40%, transparent 41%)`
- EVA：45° 金色斜線（商務折角）— `linear-gradient(45deg, transparent 45%, var(--theme-accent) 45%, var(--theme-accent) 55%, transparent 55%)`
- China Airlines：5 瓣梅花 SVG（inline data URI，半透明 accent 色）
- Starlux：6pt 金色星形 SVG（inline data URI，半透明 accent 色）

### D5：Chart.js 配色讀取 CSS custom properties

`charts.html` 中 Chart.js 配置原本硬寫 `#0E0E10`、`#FFDA00` 等色。改為：

```js
const cs = getComputedStyle(document.documentElement);
const ink = cs.getPropertyValue('--theme-ink').trim();
// ...
```

並於主題切換事件（自訂 `themechange` event）觸發 `chart.update()` 重繪。

### D6：主題持久化 — localStorage（key: `flightprice-theme`）

**選擇**：`localStorage.setItem('flightprice-theme', 'eva')`。

**替代方案**：

- (A) cookie + 伺服器端渲染 `<html data-theme>`：**否決**。需改動 Flask route，增加 Cookie 解析複雜度；此主題純屬前端視覺選擇，無須伺服器知情。
- (B) `sessionStorage`：**否決**。跨 tab / 關閉瀏覽器後丟失，違反「持久」目標。

**首屏 FOUC 防護**：`base.html` 在 `<head>` 最上方（`<link>` 載入前）嵌入 inline script：

```html
<script>
(function(){
  try {
    var t = localStorage.getItem('flightprice-theme');
    var valid = ['scoot','eva','china-airlines','starlux'];
    document.documentElement.setAttribute('data-theme', valid.indexOf(t) >= 0 ? t : 'scoot');
  } catch(e) {
    document.documentElement.setAttribute('data-theme', 'scoot');
  }
})();
</script>
```

此 script 在 CSS 套用前就設定 `data-theme`，瀏覽器只會渲染一次、一次就用正確主題。

### D7：主題切換器 UI — navbar 右側 dropdown

- 位置：navbar 右側（與現有左側品牌、中間 nav links 相對平衡）。
- 元件：Bootstrap 5 dropdown（語意 `<button aria-haspopup="listbox">` + `<ul role="listbox">` 或直接 Bootstrap dropdown），每個主題項目以 `<button role="option" data-theme-value="eva">長榮航空</button>` 呈現，當前主題 MUST 標示 `aria-current="true"` 並顯示勾選。
- 鍵盤操作：Tab 聚焦、Enter/Space 觸發切換、`Esc` 關閉選單。
- ARIA label：切換按鈕 MUST 有 `aria-label="主題切換"`。

### D8：字體策略 — 4 主題各自載入 Google Fonts

- Scoot：Nunito, Nunito Sans, JetBrains Mono（現狀保留）
- EVA：Noto Serif TC, Source Sans 3, IBM Plex Mono
- China Airlines：Noto Serif TC（共用）, Source Sans 3（共用）, JetBrains Mono
- Starlux：Cormorant Garamond, Inter Tight, JetBrains Mono

合併 `<link>` 至 `base.html`（單一 `https://fonts.googleapis.com/css2?...` URL）一次載入四主題需要的字型；對首屏效能有影響但可接受（4 主題情境下請求數合併為 1～2 個）。

## Risks / Trade-offs

- **風險 R1**：重構 `style.css` 範圍大，可能破壞既有 scoot 主題像素還原。→ **緩解**：以 data-theme="scoot" 作為預設，元件規則透過 token 映射維持同色；`tests/test_theme_smoke.py` 現有斷言全數在預設主題下跑過作為回歸閘門。
- **風險 R2**：Google Fonts 同時請求 4 套字型影響 LCP。→ **緩解**：合併為單一 CSS request、使用 `font-display=swap`、`preconnect` 至 `fonts.gstatic.com`；後續如影響效能可改為按需載入。
- **風險 R3**：Starlux 按壓樣式與其他三主題不一致，測試撰寫複雜度上升。→ **緩解**：透過 `--theme-btn-press-width` 控制，測試針對「屬性值」而非固定像素；每主題單獨 scenario 即可清楚驗收。
- **風險 R4**：Chart.js 讀取 CSS custom properties 在某些舊瀏覽器字串 trim 問題。→ **緩解**：取值後 `.trim()`；單元測試以 Flask test client 驗證 JS 原始碼含 `getPropertyValue('--theme-ink')` 字串即可，不跑 headless browser。
- **風險 R5**：Starlux `--theme-danger: #8C2E2A` 過暗，與白字對比不足。→ **緩解**：以對比公式驗算（`#8C2E2A` 對 `#FFFFFF` 約 6.8:1，AA 過關）；`--theme-warn: #B8893A` 對白字約 3.6:1，僅 AA large 過關，故 warn badge 文字 MUST 使用 Starlux ink 深色或調整 badge 底色透明度處理。於 spec 中明確規範。
- **Trade-off T1**：保留 `.scoot-*` class 別名造成 CSS 規則重複（每條規則需兩個 selector）。接受此重複以換取零向下相容破壞。
- **Trade-off T2**：主題切換僅前端 localStorage；使用者在不同裝置不同瀏覽器會看到不同預設（scoot）。接受此限制，避免引入後端狀態。

## Migration Plan

1. **階段 A：CSS 架構重構**（不改動任何 template 行為）
   - 將 `:root { --scoot-* }` 改為 `:root[data-theme="scoot"] { --scoot-*; --theme-*: var(--scoot-*) }`
   - 元件規則中所有 `var(--scoot-*)` 改為 `var(--theme-*)`
   - base.html 加上 `<html data-theme="scoot">`（預設值），預期此階段視覺 100% 不變
2. **階段 B：新增 3 主題 token scope 與中性 class** — 新增 `[data-theme="eva"]`、`[data-theme="china-airlines"]`、`[data-theme="starlux"]` 的 token 映射；新增中性 class 與既有 `.scoot-*` 的別名規則。
3. **階段 C：主題切換 UI + JS + FOUC 防護 script** — base.html 加入 dropdown、inline FOUC script、`app/static/js/theme-switcher.js`。
4. **階段 D：Chart.js 取色重構** — charts.html 讀取 CSS custom properties、綁定 themechange event。
5. **階段 E：測試擴充** — 更新 `tests/test_theme_smoke.py`：每主題 smoke、切換器 DOM 存在、FOUC script 存在、localStorage key 於 JS 原始碼中。

**回滾策略**：若階段 A 破壞視覺，直接 revert 該 commit；階段 B–E 每階段獨立 commit，可個別回滾而不影響 Scoot 預設體驗。

## Open Questions

目前已全數於 D1–D8 做出合理決策，無需使用者阻塞的 open questions。若人類 Review 有以下方向的調整需求，再由 Coordinator 修訂 spec：

- OQ1（低優先）：主題選單是否需要縮圖／色塊預覽？目前決定以文字 label + 勾選 icon，保持 navbar 緊湊。
- OQ2（低優先）：`flightprice-theme` localStorage key 命名是否符合使用者偏好？預設採此命名。
- OQ3（低優先）：是否要支援 query string 主題預覽（`?theme=eva`）方便分享？先不支援，留給未來變更。
