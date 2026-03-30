## Why

使用者需要追蹤特定日期的機票價格變化，以便在最佳時機購買機票。目前沒有自動化工具能每日從 Skyscanner 擷取價格並記錄歷史趨勢，需要建立一套完整的追蹤系統。

## What Changes

- 新增 MySQL 資料庫，包含兩張資料表：航班價格紀錄表（flight_prices）與追蹤清單表（tracked_flights）
- 新增後台爬蟲服務，從 Skyscanner 擷取指定班機的價格資訊
- 新增 Web 頁面：追蹤班機管理（僅需輸入班次代碼與出發日期，系統自動查詢航空公司、出發地、抵達地）
- 新增 Web 頁面：價格趨勢圖表（以折線圖呈現票價隨時間變化）
- 新增 Web 頁面：今日抓取狀態儀表板（顯示當日各班機的抓取結果）
- 所有服務透過 Docker container 執行

## Capabilities

### New Capabilities

- `data-storage`: MySQL 資料庫架構，包含 flight_prices 表（班次、價格、抓取日期、出發時間、航空公司、出發地、抵達地）與 tracked_flights 表（追蹤清單，含出發日期）
- `flight-info-lookup`: 航班資訊查詢服務，輸入班次代碼自動查詢航空公司、出發地、抵達地
- `price-scraper`: 後台爬蟲服務，從 Skyscanner 擷取指定班機的價格資訊並寫入資料庫
- `flight-management-page`: Web 頁面，管理追蹤班機清單（僅需輸入班次代碼與出發日期，自動帶入航班資訊）
- `price-chart-page`: Web 頁面，以圖表顯示指定班機的價格隨時間變化趨勢
- `scrape-status-page`: Web 頁面，顯示今日各班機的抓取狀態與結果

### Modified Capabilities

（無既有 capabilities 需修改）

## Impact

- 新增 Docker 服務：MySQL 資料庫容器、Python 後端應用容器
- 新增 Python 套件依賴：Web 框架、資料庫連線、圖表套件、爬蟲相關套件
- 需要 Skyscanner 資料擷取方式（API 或網頁爬蟲）
- 需要航班資訊查詢 API 或資料來源，根據班次代碼反查航空公司、出發地、抵達地
- 專案結構從空專案轉變為完整的 Web 應用程式
