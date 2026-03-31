## Context

Phase 1 已完成機票價格追蹤系統的核心功能。在實際使用中發現多段航班查詢錯誤、爬蟲容錯不足、外部 DB 工具無法連線三個問題，需一併修正。

## Goals / Non-Goals

**Goals:**

- 多段航班正確回傳所有航段，使用者可選擇要追蹤的航段
- 排程每 3 小時自動檢查，僅對無當日資料的班機執行爬蟲
- 外部工具可透過 mysql_native_password 正常連線 MySQL

**Non-Goals:**

- 不自動判斷使用者要追蹤哪段航線（由使用者選擇）
- 不支援使用者自訂排程頻率
- 不實作同一天多次抓取同一班機

## Decisions

### 1. 航班查詢 API 回傳格式：routes 陣列

**選擇**：lookup API 回傳 `{routes: [{airline, origin, destination}, ...]}`

**理由**：統一格式，單段航班為長度 1 的陣列，多段為 > 1。前端依長度決定是否顯示選擇器。

### 2. Flightradar24 多段解析

**選擇**：修改爬取函式為 `_extract_fr24_routes`，從歷史表格解析所有不重複航段。

**理由**：FR24 頁面包含多段航班的所有航段紀錄，去重後即為完整航段列表。

### 3. 排程模式：interval 每 3 小時

**選擇**：APScheduler 從 cron daily 改為 interval 每 3 小時

**理由**：容器啟動後 3 小時內必定執行，比固定時間更適合容器化部署。

### 4. 當日資料檢查

**選擇**：在 `scrape_all_active_flights` 中查詢 `flight_prices` 表 `scrape_date = today`，有資料則跳過。

**理由**：直接查既有資料表，不需額外狀態欄位。

### 5. MySQL 認證

**選擇**：docker-compose 加上 `--default-authentication-plugin=mysql_native_password`

**理由**：mysql_native_password 相容所有 MySQL 客戶端工具，無 Public Key Retrieval 問題。

## Risks / Trade-offs

- **[API 回傳格式 breaking change]** → 內部 API，前端 JS 同步修改即可
- **[3 小時間隔首次延遲]** → 容器啟動後最多等 3 小時，可接受
- **[mysql_native_password 安全性較低]** → 開發環境可接受，生產環境可改回 caching_sha2_password + SSL
