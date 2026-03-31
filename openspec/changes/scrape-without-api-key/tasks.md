## 1. 依賴與環境

- [x] 1.1 requirements.txt 新增 playwright 依賴
- [x] 1.2 Dockerfile 安裝 Playwright 及 Chromium 瀏覽器與系統依賴
- [x] 1.3 .env.example 將 SKYSCANNER_API_KEY 說明改為選用

## 2. 爬取邏輯改寫

- [x] 2.1 scraper.py 新增 _fetch_price_via_playwright 函式：用 Playwright 爬取 Skyscanner 網頁搜尋結果
- [x] 2.2 修改 scrape_flight_price：有 API Key 用 API，無則用 Playwright 爬取
- [x] 2.3 構造 Skyscanner 搜尋 URL（origin/destination/date 格式）

## 3. 測試與驗證

- [ ] 3.1 撰寫 Playwright 爬取函式的單元測試（mock Playwright）
- [ ] 3.2 撰寫查詢鏈切換邏輯的測試（有/無 API Key）
- [ ] 3.3 執行全部測試確認無回歸
- [ ] 3.4 重建 Docker 容器驗證 Playwright 可正常運作
