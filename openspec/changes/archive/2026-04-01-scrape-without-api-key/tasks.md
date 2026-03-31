## 1. 依賴與環境

- [x] 1.1 requirements.txt 新增 playwright 依賴
- [x] 1.2 Dockerfile 安裝 Playwright 及 Chromium 瀏覽器與系統依賴
- [x] 1.3 .env.example 將 SKYSCANNER_API_KEY 說明改為選用

## 2. 爬取邏輯改寫

- [x] 2.1 scraper.py 新增 _fetch_price_via_playwright 函式
- [x] 2.2 修改 scrape_flight_price：有 API Key 用 API，無則用 Playwright 爬取
- [x] 2.3 構造搜尋 URL

## 3. 測試與驗證（原 Skyscanner 版）

- [x] 3.1 撰寫 Playwright 爬取函式的單元測試（mock Playwright）
- [x] 3.2 撰寫查詢鏈切換邏輯的測試（有/無 API Key）
- [x] 3.3 執行全部測試確認無回歸
- [x] 3.4 重建 Docker 容器驗證 Playwright 可正常運作

## 4. 改用 Google Flights

- [x] 4.1 改寫 _fetch_price_via_playwright：URL 改為 Google Flights 格式，選擇器改為 [data-gs]，價格 regex 改為 \$([\d,]+)
- [x] 4.2 更新單元測試配合 Google Flights 格式
- [x] 4.3 執行全部測試確認無回歸
- [x] 4.4 重建 Docker 容器驗證
