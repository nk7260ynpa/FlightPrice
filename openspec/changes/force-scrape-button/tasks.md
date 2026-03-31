## 1. 強制抓取後端

- [x] 1.1 scraper.py 新增 force_scrape_all_active_flights 函式（不檢查當日資料）
- [x] 1.2 status.py 新增 POST /status/scrape 路由，呼叫強制抓取並 flash 結果

## 2. 前端按鈕

- [x] 2.1 status.html 新增「立即抓取」按鈕（POST 表單）

## 3. 測試與驗證

- [x] 3.1 撰寫 force_scrape_all_active_flights 單元測試
- [x] 3.2 撰寫 POST /status/scrape 路由單元測試
- [x] 3.3 執行全部測試確認無回歸
- [x] 3.4 重建 Docker 容器驗證
