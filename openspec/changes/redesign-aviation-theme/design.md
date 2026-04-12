## Context

FlightPrice 目前使用純 Bootstrap 5.3.3 CDN 預設樣式，`app/static/` 目錄為空，所有 JavaScript 以 inline script 嵌入模板。頁面共 4 個模板：`base.html`（含導航列）、`flights.html`（班機管理）、`charts.html`（價格圖表）、`status.html`（抓取狀態）。

## Goals / Non-Goals

**Goals:**

- 建立航空主題色彩系統（深航空藍導航、雲朵灰白背景、琥珀色輔助）
- 透過單一 CSS 檔案覆蓋 Bootstrap 預設，達到全站統一視覺風格
- 提升卡片、表格、表單、按鈕等元件的設計質感
- 保持 Bootstrap 5 響應式框架不變

**Non-Goals:**

- 不更換前端框架（不導入 Tailwind、React 等）
- 不重構 JavaScript 邏輯（僅調整 Chart.js 配色）
- 不改變頁面功能或路由結構
- 不加入動畫框架或額外 CDN 依賴

## Decisions

### 使用單一 CSS 覆蓋檔而非修改 Bootstrap 原始碼

新增 `app/static/css/style.css` 載入於 Bootstrap CSS 之後，透過 CSS 變數與選擇器覆蓋預設樣式。

**替代方案**：使用 Bootstrap Sass 自訂編譯。
**選擇理由**：��案規模小，覆蓋檔維護成本低，不需引入 Sass 編譯工具鏈。

### 使用 CSS 自訂屬性（Custom Properties）管理色彩

在 `:root` 定義所有主題色彩變數，模板中的元件透過 `var()` ���用，方便日後調色。

**替代方案**：直接寫死色碼在各選擇器中。
**選擇理由**：集中管理色彩，一處修改全站生效。

### 色彩系統定義

| 用途 | 色碼 | 名稱 |
|------|------|------|
| 導航列深色 | `#1e3a5f` | 深航空藍 |
| 主要強調色 | `#2563eb` | 航空藍 |
| 主要強調色亮 | `#3b82f6` | 亮航空藍 |
| 輔助強調色 | `#f59e0b` | 琥珀登機牌 |
| 頁面背景 | `#f0f4f8` | 雲朵灰白 |
| 卡片背景 | `#ffffff` | 白 |
| 深色文字 | `#1e293b` | 墨色 |
| 次要文字 | `#64748b` | 霧灰 |
| 成功 | `#16a34a` | 綠 |
| 危險 | `#dc2626` | 紅 |

## Risks / Trade-offs

- **[Bootstrap 版本升級可能破壞覆蓋]** → 覆蓋檔以 CSS 變數為主，減少對 Bootstrap ���部 class 的硬性依賴
- **[深色導航列對比度]** → 導航列文字使用白色，確保 WCAG AA 對比度標準
