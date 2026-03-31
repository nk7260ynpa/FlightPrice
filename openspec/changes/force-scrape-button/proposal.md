## Why

目前爬蟲僅透過排程每 3 小時自動執行，使用者無法手動觸發。當排程剛跳過（當日已有資料）或需要立即更新價格時，缺少強制抓取的入口。

## What Changes

- 抓取狀態頁面新增「立即抓取」按鈕
- 新增 POST 路由執行強制抓取（忽略當日資料檢查，對所有啟用班機執行）
- 抓取完成後重導回狀態頁面並顯示結果

## Capabilities

### New Capabilities

（無）

### Modified Capabilities

- `scrape-status-page`: 新增強制抓取按鈕與對應路由
- `price-scraper`: 新增強制抓取函式（忽略當日資料檢查）

## Impact

- `app/routes/status.py`：新增 POST `/status/scrape` 路由
- `app/templates/status.html`：新增「立即抓取」按鈕
- `app/scraper.py`：新增 `force_scrape_all_active_flights` 函式
