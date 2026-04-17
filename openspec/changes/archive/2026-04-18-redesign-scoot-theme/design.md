## Context

FlightPrice 目前使用 Bootstrap 5.3.3 CDN 搭配自行撰寫的 `app/static/css/style.css`（通用航空主題）。頁面由 4 個 Jinja2 模板組成（`base.html`、`flights.html`、`charts.html`、`status.html`）；`charts.html` 內以 Chart.js 4 CDN 繪製折線圖。所有 JavaScript 以 inline script 嵌入模板，沒有前端打包工具。

前一個變更 `redesign-aviation-theme` 已建立以 `--av-*` 為前綴的 CSS 自訂屬性體系與 `.navbar-aviation` / `.card` / `.table-aviation` / `.btn-aviation*` / `.stat-card*` / `.badge-aviation-*` 等 class。本次要把這套通用航空主題**整個**置換成更具品牌個性的酷航（Scoot）風格：大面積亮黃 + 近黑色文字、圓潤 sans-serif 字體、塊面色彩與登機證意象。

## Goals / Non-Goals

**Goals:**

- 建立一套以 `--scoot-*` 為命名前綴的 CSS 自訂屬性（tokens），涵蓋色彩、字體、圓角等設計決策。
- 完整重寫 `app/static/css/style.css`，以 scoot-theme class 取代舊 aviation-theme class。
- 更新 4 個模板，使其引用新的 class 與文字字串（例如導航列品牌文字、button 類別）。
- 調整 `charts.html` 內嵌 Chart.js 的配色參數，使圖表視覺與主題一致。
- 保留 Bootstrap 5 的響應式 grid 系統與既有表單／導航基礎結構，不引入新框架。
- 確保所有互動元素滿足 WCAG 2.1 AA 對比、`:focus-visible` 可見與 `prefers-reduced-motion` 尊重。
- 測試層保有既有 pytest 可通過；並新增 Flask test client 的模板渲染 smoke 驗證關鍵 class。

**Non-Goals:**

- 不更換前端框架（不導入 Tailwind、Sass、React 等）。
- 不改寫後端路由、資料模型、scraper 邏輯或 API 介面。
- 不新增前端打包工具（Vite/Webpack/Rollup）。
- 不修改 `app/templates/` 以外的路由或邏輯；`app/routes/*.py` 在本變更中保持不變。
- 不更換 logo／favicon（專案目前未定義自有 logo，沿用 Emoji `&#9992;`；若未來要設計 logo，另開 change）。
- 不實作深色模式（dark mode）切換；本次僅專注於酷航「亮色日間」主題，未來若需暗色版本另議。

## Decisions

### 沿用 CSS 覆蓋檔策略、以 `--scoot-*` 命名 tokens

維持現狀「單一 `app/static/css/style.css` 載入於 Bootstrap CSS 之後」的策略，以 CSS 自訂屬性統一管理色彩、字體、圓角。命名由 `--av-*` 改為 `--scoot-*`，避免新舊變數混淆。

**替代方案**：改用 CSS-in-JS（如 Tailwind）。
**選擇理由**：本變更為純視覺重寫，引入打包工具鏈成本過高；CSS 覆蓋方案變更面可控、rollback 只需回復 style.css 與模板 class。

### 維持 Bootstrap 5.3.3 CDN 不變

本變更不升級 Bootstrap 版本，也不抽換為其他 UI library。透過 CSS 覆蓋與新 class 命名（`btn-scoot*`、`table-scoot*`、`navbar-scoot` 等）建構主題層，Bootstrap 原生 class（`container`、`row`、`col-md-*`、`form-control`）保留不動。

**替代方案**：升級至 Bootstrap 5.3.x 最新或替換為 headless UI。
**選擇理由**：風險增加、收益不顯著。

### 字體採用 Google Fonts Nunito 系列，並加 CJK + 系統字型 fallback

Display / Body 選擇 Nunito 與 Nunito Sans，兼顧圓潤、活潑廉航廣告感與可讀性；CJK fallback 使用 PingFang TC（macOS/iOS 預設）與 Noto Sans TC。數字使用 JetBrains Mono 強化登機證票面感。

**載入方式決策**：於 `base.html` `<head>` 中加入 Google Fonts `<link>`（preconnect + display=swap），以避免 FOIT 並縮短首屏等待；若網路連線失敗，fallback 至系統字體，不影響功能。

**替代方案**：(a) 不載入外部字體，僅使用系統字型；(b) 自行下載字體放在 `app/static/fonts/`。
**選擇理由**：CDN `<link>` 實作最輕量，且 Nunito 家族授權允許 CDN 引用；若未來要離線，可將字體檔下載到 `app/static/fonts/` 並改為 `@font-face`，屬後續優化。

### Class 命名策略：新增 `scoot-*` 前綴，不復用舊 `aviation-*`

新主題的所有自訂 class 以 `scoot-` 為前綴（`.navbar-scoot`、`.btn-scoot`、`.btn-scoot-danger`、`.table-scoot`、`.stat-scoot`、`.card-header-scoot`、`.badge-scoot-success` 等）。舊 class（`.navbar-aviation`、`.btn-aviation*`、`.stat-card*`、`.badge-aviation-*`、`.table-aviation*`）於本變更中**全部移除**，不做別名相容。

**替代方案**：同時保留新舊 class，讓舊 class 沿用新樣式。
**選擇理由**：本專案模板僅 4 個、無外部呼叫，全域一次性切換風險低；維持兩套命名反而造成長期維護負擔。

### 統計卡片由「左側色條 + 白底」改為「整卡塊面染色」

語意分類使用卡片背景色塊而非左側 stripe。這是酷航風格的關鍵差異化點之一（塊面感）。

**語意對應**（供 Specialist 在模板實作）：

| 資訊 | 原 aviation class | 新 scoot class |
|------|-------------------|----------------|
| 追蹤班機數 | `stat-card-stripe--navy` | `stat-scoot--ink`（近黑底白字） |
| 成功擷取 | `stat-card-stripe--success` | `stat-scoot--success`（綠底白字） |
| 失敗擷取 | `stat-card-stripe--danger` | `stat-scoot--danger`（紅底白字） |
| 最高價 | `stat-card-stripe--danger` | `stat-scoot--danger` |
| 最低價 | `stat-card-stripe--success` | `stat-scoot--success` |
| 平均價 | `stat-card-stripe--blue` | `stat-scoot--ink`（中性近黑，避免與品牌藍衝突） |

### 按鈕層級 mapping

模板內既有按鈕的語意對應：

| 使用情境 | 原 class | 新 class |
|---------|----------|----------|
| 新增（班機） | `btn-aviation` | `btn-scoot`（primary：黃底黑字） |
| 查詢 | `btn-aviation-outline` | `btn-scoot-secondary`（透明底深邊） |
| 立即抓取 | `btn-aviation-danger` | `btn-scoot-danger` |
| 停用（操作班機） | `btn-aviation-warning` | `btn-scoot-warning` |
| 啟用（操作班機） | `btn-aviation-success` | `btn-scoot-success` |

### Chart.js 配色採內嵌定義，不抽成 CSS 變數

Chart.js 無法直接讀 CSS 變數，若要動態讀取會需要 JavaScript runtime `getComputedStyle()` 解析；為控制複雜度，於 `charts.html` inline script 中以硬編碼色碼呈現（符合 `scoot-theme` spec「色彩硬編碼例外」中的 allowable case，因為該色碼位於 JS 而非 CSS 選擇器中）。

**替代方案**：於 inline script 中以 `getPropertyValue('--scoot-ink')` 讀取變數。
**選擇理由**：實作複雜度提高，收益僅為一致性；此變更先以硬碼 + spec 規範維持對齊。

### 測試策略

- **既有測試**：於 Docker container 中執行 `pytest`，確保沒有迴歸。
- **新增模板渲染 smoke 測試**：以 Flask test client 發 GET 至主要頁面（`/`、`/charts`、`/status`），驗證 HTML 回應中包含新主題關鍵 class（例如 `navbar-scoot`、`btn-scoot`、`stat-scoot`、`table-scoot`）。此類測試不需要瀏覽器，只做字串／DOM 斷言。
- **靜態檔案可達性測試**：驗證 `GET /static/css/style.css` 回應 200 且包含 `--scoot-yellow` token 定義。
- **視覺驗證**：Specialist 於重建 Docker image 後手動瀏覽 3 頁，核對與 design.md 敘述一致；不強制自動化 visual regression（範圍偏大）。

## Risks / Trade-offs

- **[外部字體載入延遲或失敗]** → 字體堆疊提供完整 fallback（PingFang TC / Noto Sans TC / system font），網頁仍可正常渲染，僅字型樣式略異。
- **[黃色視覺疲勞]** → 黃色僅用於導航列、主按鈕、統計卡片單張與表格交替色（低 alpha），大面積內容仍是白色／暖米白；避免全頁鋪黃。
- **[對比不足風險（黃底白字）]** → spec 明文禁止，並在設計層規劃 `.stat-scoot--yellow`、`.btn-scoot` 等所有黃色元件僅搭配深色文字；PR review 與 smoke test 要檢查。
- **[Bootstrap 升級破壞覆蓋]** → class 以自訂 `scoot-*` 命名，對 Bootstrap 內部 class 依賴降至最低；未來升級只需檢視 `.form-control`、`.card` 等少數基礎 class 覆蓋。
- **[Chart.js 色碼硬編碼導致與 CSS 不一致]** → spec 明列 Chart.js 色碼與對應 token 值；修改任一端時需同步檢查。
- **[使用者對品牌強烈色彩接受度]** → 本變更屬純視覺；若需退回通用主題，rollback 方式為 `git revert` 該 feature branch merge commit，或重新 apply aviation-theme 的檔案版本。

## Migration Plan

1. Coordinator 已切出 feature branch `opsx/redesign-scoot-theme`，commit spec artifacts。
2. Specialist 於 `/opsx:apply` 階段：
   1. 重寫 `app/static/css/style.css` 為 scoot-theme。
   2. 更新 4 個模板以引用新 class。
   3. 在 `base.html` 加入 Google Fonts `<link>`。
   4. 調整 `charts.html` Chart.js 配色參數。
   5. 新增 `tests/test_theme_smoke.py`（或既有測試檔擴充）做模板渲染 smoke 測試。
   6. 每完成一組 task 即 commit and push。
3. Verifier 於 `/opsx:verify`：在 Docker container 執行全部測試、對照 spec 檢查各 requirement，FAIL 寫入 `issues.md`。
4. PASS 後 `/opsx:archive`：以 no-ff merge 回 main；`openspec/specs/aviation-theme/` 被 REMOVED，`openspec/specs/scoot-theme/` 被建立。
5. **Rollback**：若視覺嚴重不符期待，執行 `git revert -m 1 <merge-commit>` 回復至 aviation-theme；因無資料模型變更，無需 DB migration。

## Open Questions

- **Logo / favicon**：目前沿用 Emoji `&#9992;` 作為品牌符號，未自行設計 logo；是否未來要產製酷航風格 SVG logo、替換 favicon，另立 change。本變更維持 Emoji 方案，假設使用者可接受。
- **深色模式**：本變更不實作 dark mode；若未來需要，可再定義 `--scoot-*-dark` 並以 `prefers-color-scheme` 切換。此假設在 proposal.md 已敘明。
- **字體授權／離線化**：當前採 Google Fonts CDN，若部署環境對外網不通（例如 intranet），需改為下載字體檔到 `app/static/fonts/` 並補 `@font-face`；待人類 review 時確認是否有此需求。
- **Accessibility 檢測自動化**：本變更僅以手動規範 + spec 驗證對比；是否導入 axe-core / Pa11y 自動檢測，列為後續優化，暫不納入本 change。
