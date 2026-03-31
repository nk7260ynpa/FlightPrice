## Why

Phase 1 完成後在實際使用中發現三個問題需要改善：
1. 部分班次（如 TR866）對應多段航線，查詢只回傳第一段導致出發地/抵達地錯誤
2. 爬蟲每日只執行一次，若該次失敗則整天無資料，且無法避免重複抓取
3. MySQL 8.0 預設使用 caching_sha2_password 認證，外部工具連線時出現 "Public Key Retrieval is not allowed" 錯誤

## What Changes

### 多段航班選擇
- 航班查詢 API 改為回傳所有航段列表（如 SIN→TPE、TPE→NRT）
- 前端班機管理表單新增航段選擇下拉選單（查到多段時顯示）
- Flightradar24 爬取邏輯改為解析所有不重複航段

### 智慧排程爬蟲
- 排程頻率從每日 1 次改為每 3 小時 1 次
- 每次觸發前先查 DB 當日是否已有資料，僅對無資料的班機執行爬蟲

### MySQL 認證修正
- docker-compose 加上 `--default-authentication-plugin=mysql_native_password`
- 確保外部工具（DBeaver、DataGrip 等）可正常連線

## Capabilities

### New Capabilities

（無）

### Modified Capabilities

- `flight-info-lookup`: 查詢結果從單一航線改為航段列表，支援多段航班
- `flight-management-page`: 新增追蹤班機表單增加航段選擇互動
- `price-scraper`: 排程改為每 3 小時，新增當日資料檢查邏輯
- `data-storage`: docker-compose MySQL 容器加上 native password 認證設定

## Impact

- `app/flight_lookup.py`：所有查詢函式回傳格式改為列表
- `app/routes/flights.py`：lookup API 回傳格式變更
- `app/templates/flights.html`：前端 JavaScript 新增航段選擇器
- `app/scheduler.py`：排程模式從 cron 改為 interval
- `app/scraper.py`：新增當日資料檢查邏輯
- `docker/docker-compose.yaml`：MySQL 認證設定
- 既有單元測試需配合更新
