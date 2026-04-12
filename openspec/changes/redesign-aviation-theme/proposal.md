## Why

目前頁面完全依賴 Bootstrap 5 預設樣式，沒有任何自訂 CSS，缺乏品牌辨識度與專業感。作為航班價格追蹤工具，採用航空主題視覺風格能提升使用體驗與產品質感。

## What Changes

- 新增自訂 CSS 檔案 `app/static/css/style.css`，建立航空主題���彩系統與元件樣式
- 重新設計導航列：深航空藍漸層背景、飛機圖標 Logo
- 重新設計卡片元件：白色背景、柔和陰影、懸浮效果
- 統一色彩系統：航空藍 (#1e3a5f / #2563eb)、雲朵灰白背景 (#f0f4f8)、琥珀色輔助色 (#f59e0b)
- 改善表格樣式、表單樣式、按鈕樣式、Badge 樣式
- 統一統計卡片設計風格（圖表頁與狀態頁）
- 調整 Chart.js 圖表配色以符合航空主題
- 更新所有模板以套用新的 CSS class

## Capabilities

### New Capabilities

- `aviation-theme`: 定義航空主題的視覺設計規格，涵蓋色彩系統、排版、元件樣式

### Modified Capabilities

（無 — 這是純視覺變更，不改變功能需求）

## Impact

- **程式碼**: `app/templates/` 全部 4 個模板、新增 `app/static/css/style.css`
- **Docker**: `docker/Dockerfile` 確認 `app/static/` 有被 COPY（目前只 COPY `app/`，已包含）
- **依賴**: 無新增套件，仍使用 Bootstrap 5 CDN + Chart.js CDN
- **行為**: 純視覺變更，不影響後端邏輯與 API
