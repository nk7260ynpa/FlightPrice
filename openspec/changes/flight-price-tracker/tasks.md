## 1. 專案基礎建設

- [x] 1.1 建立專案目錄結構（app/、docker/、logs/、tests/）
- [x] 1.2 建立 requirements.txt（Flask、SQLAlchemy、PyMySQL、APScheduler、requests、beautifulsoup4）
- [x] 1.3 建立 Dockerfile 與 build.sh
- [x] 1.4 建立 docker-compose.yaml（MySQL 容器 + Flask 應用容器，含 volume 持久化）
- [x] 1.5 建立 run.sh 啟動腳本（啟動 docker-compose 並掛載 logs 資料夾）
- [x] 1.6 建立 .env 範例檔（MySQL 連線設定、Skyscanner API 設定）

## 2. 資料庫與資料模型

- [x] 2.1 建立 Flask 應用工廠（app/__init__.py），設定 SQLAlchemy 連線 MySQL
- [x] 2.2 建立 SQLAlchemy 資料模型（app/models.py）：FlightPrice 與 TrackedFlight
- [x] 2.3 建立資料庫初始化腳本，確保容器啟動時自動建立資料表
- [x] 2.4 撰寫資料模型的單元測試

## 3. 爬蟲服務

- [x] 3.1 建立 Skyscanner 價格擷取模組（app/scraper.py），實作價格擷取邏輯
- [x] 3.2 實作抓取狀態紀錄機制（成功/失敗/錯誤原因/時間戳記）
- [x] 3.3 建立 APScheduler 排程設定（app/scheduler.py），每日定時執行擷取
- [x] 3.4 撰寫爬蟲模組的單元測試

## 4. 班機管理頁面

- [x] 4.1 建立班機管理路由（app/routes/flights.py）：清單、新增、停用/啟用
- [x] 4.2 建立班機管理頁面模板（app/templates/flights.html）：表格 + 新增表單
- [x] 4.3 實作表單驗證（必填欄位、重複班次檢查）
- [x] 4.4 撰寫班機管理路由的單元測試

## 5. 價格圖表頁面

- [x] 5.1 建立價格圖表路由（app/routes/charts.py）：頁面渲染 + JSON 資料 API
- [x] 5.2 建立價格圖表頁面模板（app/templates/charts.html）：下拉選單 + Chart.js 折線圖
- [x] 5.3 實作價格統計摘要（最高價、最低價、平均價）
- [x] 5.4 撰寫價格圖表路由的單元測試

## 6. 抓取狀態頁面

- [x] 6.1 建立抓取狀態路由（app/routes/status.py）：今日狀態查詢
- [x] 6.2 建立抓取狀態頁面模板（app/templates/status.html）：統計摘要 + 狀態表格
- [x] 6.3 實作失敗原因顯示
- [x] 6.4 撰寫抓取狀態路由的單元測試

## 7. 頁面整合與導覽

- [x] 7.1 建立共用基礎模板（app/templates/base.html）：導覽列、頁面佈局
- [x] 7.2 設定 Flask 靜態檔案目錄（app/static/）
- [x] 7.3 設定 logging 模組，日誌輸出至 logs 資料夾

## 9. 航班資訊查詢與表單改版

- [x] 9.1 建立航班資訊查詢模組（app/flight_lookup.py），根據班次代碼查詢航空公司、出發地、抵達地
- [x] 9.2 新增航班查詢 API 路由（GET /api/flights/lookup?flight_number=XX）
- [x] 9.3 TrackedFlight 模型新增 departure_date 欄位，移除 flight_number 唯一約束（同班次不同日期可追蹤）
- [x] 9.4 更新班機管理表單：僅需輸入班次代碼與出發日期，自動查詢帶入航班資訊
- [x] 9.5 更新班機管理路由（add_flight）：接收 departure_date，支援自動查詢後的資料
- [x] 9.6 更新班機清單表格：顯示出發日期欄位
- [x] 9.7 撰寫航班查詢模組與路由的單元測試
- [x] 9.8 重建 Docker 容器驗證變更

## 10. 航班查詢多層備援策略

- [ ] 10.1 flight_lookup.py 新增 DB 快取查詢：從 tracked_flights 查同班次已有紀錄，直接複製 airline/origin/destination
- [ ] 10.2 flight_lookup.py 新增 Flightradar24 爬取函式：從網頁解析航空公司、出發地、抵達地 IATA 代碼
- [ ] 10.3 調整 lookup_flight_info 查詢鏈順序：DB 快取 → Flightradar24 → AviationStack → IATA 對照表
- [ ] 10.4 撰寫多層備援查詢的單元測試
- [ ] 10.5 重建 Docker 容器驗證變更

## 8. 文件與收尾

- [x] 8.1 更新 README.md：專案說明、架構圖、安裝與啟動步驟
- [x] 8.2 更新 .gitignore：排除 .env、logs/*.log
- [x] 8.3 端對端驗證：啟動所有容器，測試完整流程
