## 1. CSS 架構重構（Scoot 主題維持視覺不變）

**檔案範圍**：`app/static/css/style.css`、`app/templates/base.html`
**相依**：無
**說明**：此階段僅重構架構（data-theme scope + 中性 token + 中性 class 別名），視覺 100% 不變，所有 `tests/test_theme_smoke.py` 既有斷言必須依然通過。

- [x] 1.1 於 `app/templates/base.html` 的 `<html>` 標籤新增 `data-theme="scoot"` 預設屬性
- [x] 1.2 將 `style.css` 中 `:root { --scoot-* }` 改寫為 `:root[data-theme="scoot"] { --scoot-*; }` 並加入 `:root:not([data-theme]) { ... }` fallback（套用與 scoot 相同值）
- [x] 1.3 於 `:root[data-theme="scoot"]` 內新增中性語意 tokens 映射：`--theme-primary`、`--theme-primary-bright`、`--theme-primary-deep`、`--theme-accent`、`--theme-accent-deep`、`--theme-ink`、`--theme-ink-soft`、`--theme-slate`、`--theme-muted`、`--theme-canvas`、`--theme-surface`、`--theme-line`、`--theme-success`、`--theme-danger`、`--theme-warn`、`--theme-info`、`--theme-font-display`、`--theme-font-body`、`--theme-font-mono`、`--theme-radius-sm`、`--theme-radius`、`--theme-radius-lg`、`--theme-navbar-bg`、`--theme-navbar-accent-line`、`--theme-btn-press-width`、`--theme-btn-radius`、`--theme-stat-motif`
- [x] 1.4 將 style.css 中所有元件規則（body、h1-h3、.navbar-scoot、.card、.card-header、.card-header-scoot、.btn-scoot*、.form-control、.form-select、.form-label、.table-scoot*、.stat-scoot*、.badge-scoot-*、.alert、`@media prefers-reduced-motion`）中的 `var(--scoot-*)` 全數改為對應 `var(--theme-*)`
- [x] 1.5 為每條既有元件 selector 加入中性 class 別名：`.navbar-scoot` → `.navbar-scoot, .navbar-theme`、`.btn-scoot` → `.btn-scoot, .btn-theme`、`.btn-scoot-secondary/danger/success/warning` 各自加上 `.btn-theme-secondary/danger/success/warning`、`.card-header-scoot` → `.card-header-scoot, .card-header-theme`、`.table-scoot-wrap` → `.table-scoot-wrap, .table-theme-wrap`、`.table-scoot` → `.table-scoot, .table-theme`、`.stat-scoot*` 系列加上 `.stat-theme*` 對應變體（`--yellow` → `--primary`）、`.badge-scoot-*` 加上 `.badge-theme-*`
- [x] 1.6 使用 Docker container 執行 `pytest tests/test_theme_smoke.py -v`，確認 14 項既有斷言全數通過（Scoot 預設視覺無破壞）

## 2. 新增 3 主題 token scope（EVA / China Airlines / Starlux）

**檔案範圍**：`app/static/css/style.css`
**相依**：Task 1

- [x] 2.1 新增 `:root[data-theme="eva"] { ... }` block：定義 16 項 `--eva-*` 品牌 tokens（色碼見 `specs/eva-theme/spec.md`）與中性 `--theme-*` 映射；字體堆疊 `--theme-font-display: "Noto Serif TC", "Source Serif Pro", ...`、`--theme-font-body: "Source Sans 3", ...`、`--theme-font-mono: "IBM Plex Mono", ...`
- [x] 2.2 於 EVA scope 設定 `--theme-btn-press-width: 3px`、`--theme-btn-radius: 10px`、`--theme-navbar-accent-line: 1px solid var(--theme-accent)`、`--theme-stat-motif: linear-gradient(45deg, transparent 45%, var(--theme-accent) 45%, var(--theme-accent) 55%, transparent 55%)`
- [x] 2.3 新增 `:root[data-theme="china-airlines"] { ... }` block：定義 16 項 `--cal-*` 品牌 tokens 與中性映射；字體堆疊 `--theme-font-display: "Noto Serif TC", "Playfair Display", ...`、`--theme-font-body: "Source Sans 3", ...`
- [x] 2.4 於 China Airlines scope 設定 `--theme-btn-press-width: 3px`、`--theme-btn-radius: 10px`、`--theme-navbar-accent-line: 3px solid var(--theme-accent)`、`--theme-stat-motif` 為 inline SVG data URI（5 瓣梅花，半透明 accent 色）
- [x] 2.5 新增 `:root[data-theme="starlux"] { ... }` block：定義 17 項 `--jx-*` 品牌 tokens（含 `--jx-accent-bright`）與中性映射；字體堆疊 `--theme-font-display: "Cormorant Garamond", ...`、`--theme-font-body: "Inter Tight", ...`、`--theme-font-mono: "JetBrains Mono", ...`
- [x] 2.6 於 Starlux scope 設定 `--theme-btn-press-width: 0px`（差異化）、`--theme-btn-radius: 4px`、`--theme-navbar-accent-line: 1px solid var(--theme-accent)`、`--theme-stat-motif` 為 inline SVG data URI（6pt 金色星形）
- [x] 2.7 為 Starlux 的按鈕 `:active` 規則加入條件樣式（透過 `[data-theme="starlux"] .btn-theme:active` selector group），使用 `box-shadow: inset 0 1px 2px rgba(0,0,0,0.2)` 取代 transform+border shrink；`@media (prefers-reduced-motion: reduce)` 下停用
- [x] 2.8 為 Starlux 的 `.navbar-theme .nav-link.active` 覆寫樣式：透明底 + `border-bottom: 2px solid var(--theme-accent)`（金色下劃線），不用實色 pill
- [x] 2.9 為 Starlux 的 `.card` / `.table-theme thead th` 覆寫：card 背景使用 `var(--theme-surface)`（象牙色），表頭字體以 `var(--theme-font-display)` 襯線金字

## 3. 主題切換器 UI（navbar 下拉）

**檔案範圍**：`app/templates/base.html`、`app/static/css/style.css`
**相依**：Task 1、Task 2

- [ ] 3.1 於 `base.html` navbar 的 `.navbar-collapse` 內右側（與現有 `navbar-nav` 平行或使用 `ms-auto`）新增 Bootstrap dropdown：`<button aria-label="主題切換" class="btn btn-theme-secondary dropdown-toggle" data-bs-toggle="dropdown">` + `<ul class="dropdown-menu dropdown-menu-end">`
- [ ] 3.2 下拉選單中列出四個 `<li><button type="button" class="dropdown-item" role="menuitemradio" data-theme-value="scoot">酷航 Scoot</button></li>` 等四項；當前生效項目 MUST 加上 `aria-current="true"` 並加上勾選符號（`✓` 或 SVG icon）於文字前
- [ ] 3.3 於 style.css 新增 `.theme-switcher` 或 `.dropdown-menu` 的主題專屬樣式（若預設 Bootstrap 樣式不符合，加上最小必要覆寫以保持各主題風格）

## 4. 主題切換 JS（持久化 + themechange event）

**檔案範圍**：`app/static/js/theme-switcher.js`（新檔）、`app/templates/base.html`
**相依**：Task 3

- [ ] 4.1 建立 `app/static/js/theme-switcher.js`，內容包含：合法主題白名單 `['scoot','eva','china-airlines','starlux']`、`applyTheme(value)` 函式（設定 data-theme、寫入 localStorage key `flightprice-theme`、派發 `CustomEvent('themechange', { detail: { theme: value } })`、更新選單 `aria-current`）、DOMContentLoaded 後綁定所有 `[data-theme-value]` click 事件、頁面載入時依 localStorage 初始化選單 `aria-current` 標示
- [ ] 4.2 於 `base.html` 底部 `<script>` 區塊引入 `<script src="{{ url_for('static', filename='js/theme-switcher.js') }}"></script>`（Bootstrap bundle 之後）
- [ ] 4.3 於 `base.html` `<head>` 的第一個 `<link>` 之前嵌入 FOUC 防護 inline script：`try { var t = localStorage.getItem('flightprice-theme'); var valid = ['scoot','eva','china-airlines','starlux']; document.documentElement.setAttribute('data-theme', valid.indexOf(t)>=0 ? t : 'scoot'); } catch(e) { document.documentElement.setAttribute('data-theme','scoot'); }`
- [ ] 4.4 確認 `app/templates/base.html` 中 `<html>` 起始標籤移除硬編 `data-theme="scoot"`（改由 inline script 負責）；若 script 未執行則以 style.css 的 `:root:not([data-theme])` fallback 保底

## 5. Google Fonts 合併載入

**檔案範圍**：`app/templates/base.html`
**相依**：Task 2

- [ ] 5.1 將 `base.html` 現有的 Google Fonts `<link>` URL 擴充為合併版本，`family=` 參數涵蓋四主題所需字型：Nunito:wght@700;800、Nunito+Sans:wght@400;500;600、JetBrains+Mono:wght@500、Noto+Serif+TC:wght@500;700、Source+Sans+3:wght@400;500;600、IBM+Plex+Mono:wght@500、Cormorant+Garamond:wght@500;600;700、Inter+Tight:wght@400;500;600；加上 `display=swap`
- [ ] 5.2 保留 `preconnect` 至 `fonts.googleapis.com` 與 `fonts.gstatic.com`

## 6. Chart.js 主題色動態化

**檔案範圍**：`app/templates/charts.html`
**相依**：Task 4

- [ ] 6.1 將 `charts.html` 內嵌 Chart.js 初始化程式碼重構為：建立 `readThemeColors()` 函式透過 `getComputedStyle(document.documentElement).getPropertyValue('--theme-<token>').trim()` 讀取 `--theme-ink`、`--theme-primary`、`--theme-slate` 等；datasets 與 scales（`borderColor`、`backgroundColor`、`pointBackgroundColor`、`pointBorderColor`、`grid.color`、`ticks.color`、`plugins.tooltip.backgroundColor`、`plugins.tooltip.titleColor`、`plugins.tooltip.bodyColor`、`plugins.legend.labels.color`）改由該函式回傳值填入
- [ ] 6.2 註冊 `document.addEventListener('themechange', () => { /* 重新讀色、套用至 chart.data.datasets 與 chart.options，呼叫 chart.update() */ });`
- [ ] 6.3 確認原有硬編色碼（`'#0E0E10'`、`'#FFDA00'`、`'rgba(14, 14, 16, 0.08)'` 等）全數從 Chart.js 配置中移除

## 7. 測試擴充

**檔案範圍**：`tests/test_theme_smoke.py`
**相依**：Task 1–6

- [ ] 7.1 新增 `TestThemeSwitcherUI` 類別：驗證 `/`、`/charts`、`/status` 皆渲染主題切換器 DOM（`data-theme-value="scoot"`、`data-theme-value="eva"`、`data-theme-value="china-airlines"`、`data-theme-value="starlux"` 四個選項同時存在，切換按鈕具 `aria-label="主題切換"`）
- [ ] 7.2 新增 `TestThemeSwitcherScript` 類別：以 Flask test client 取 `/static/js/theme-switcher.js`，斷言回應 200、Content-Type 含 `javascript`、原始碼包含 `flightprice-theme`、`data-theme-value`、`themechange`、白名單 `['scoot','eva','china-airlines','starlux']`、MUST 不含 `location.reload`
- [ ] 7.3 新增 `TestBaseTemplateFOUC` 類別：驗證 `base.html` 渲染結果中，`<head>` 內 `bootstrap.min.css` link 之前有 `<script>` 區塊，且該 script 包含字串 `flightprice-theme`、`data-theme`、`try`
- [ ] 7.4 新增 `TestEvaThemeCss` 類別：取 `/static/css/style.css`，斷言內容包含 `:root[data-theme="eva"]`、`#005F3C`、`#D4A84B`、`Noto Serif TC`、`Source Sans 3`
- [ ] 7.5 新增 `TestChinaAirlinesThemeCss` 類別：斷言內容包含 `:root[data-theme="china-airlines"]`、`#003F87`、`#C8102E`
- [ ] 7.6 新增 `TestStarluxThemeCss` 類別：斷言內容包含 `:root[data-theme="starlux"]`、`#0E1842`、`#C8A96A`、`Cormorant Garamond`、`Inter Tight`；斷言 `--theme-btn-press-width: 0px` 於 starlux block 內出現（以 regex 或 substring 檢查）
- [ ] 7.7 新增 `TestChartsThemeIntegration` 類別：取 `/charts`，斷言 HTML 回應含 `getPropertyValue('--theme-` 與 `themechange` 字串；MUST 不含硬編色 `'#0E0E10'` 或 `'#FFDA00'` 在 Chart.js 配置中（可用簡單 substring 檢查）
- [ ] 7.8 新增 `TestNeutralClassAliases` 類別：斷言 style.css 內同時出現 `.navbar-theme`、`.btn-theme`、`.btn-theme-danger`、`.stat-theme`、`.stat-theme--ink`、`.table-theme`、`.badge-theme-success` 與對應 `.*-scoot` class（證明別名共存）
- [ ] 7.9 確認既有 `TestFlightsPageScootTheme`、`TestChartsPageScootTheme`、`TestStatusPageScootTheme`、`TestStaticCssFile`、`TestBaseTemplateFonts` 全數維持通過（預設 data-theme="scoot"，Scoot 視覺不變）
- [ ] 7.10 在 Docker container 內執行完整測試：`./run.sh` 或 `docker compose run --rm app pytest tests/test_theme_smoke.py -v`，所有斷言 MUST 通過

## 8. 文件同步檢查

**檔案範圍**：無（僅檢查；若需更新 README.md / CLAUDE.md 則寫入 `issues.md` 回報 Coordinator）
**相依**：Task 1–7

- [ ] 8.1 檢查 `README.md` 專案架構章節是否需補充多主題說明；若需要，Specialist MUST 將修改需求寫入 `openspec/changes/add-airline-theme-switcher/issues.md` 交由 Coordinator 更新 tasks.md，不得直接修改 README.md
- [ ] 8.2 Commit 前以 `git diff --cached | rg -iE 'api[_-]?key|secret|token|password'` 掃描，確認無 API key 外洩
