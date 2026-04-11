# container-timezone Specification

## Purpose

定義 FlightPrice 所有 Docker 容器的系統時區規格，確保容器內時間與資料庫時間皆為台灣時間（UTC+8）。

## Requirements

### Requirement: Web 容器使用台灣時區
Web 容器的系統時區 SHALL 設定為 `Asia/Taipei`（UTC+8），確保容器內所有程式取得的本地時間為台灣時間。

#### Scenario: 容器內系統時間為台灣時間
- **WHEN** Web 容器啟動完成
- **THEN** 執行 `date +%Z` 回傳 `CST` 或 `Asia/Taipei`，且 `/etc/localtime` 指向 `Asia/Taipei` 時區資料

#### Scenario: Python logging 時間戳記為台灣時間
- **WHEN** Flask 應用程式寫入 log
- **THEN** log 時間戳記 SHALL 為 UTC+8 台灣時間

### Requirement: MySQL 容器使用台灣時區
MySQL 容器的時區 SHALL 設定為 `Asia/Taipei`（UTC+8），確保資料庫時間函式回傳台灣時間。

#### Scenario: MySQL NOW() 回傳台灣時間
- **WHEN** 在 MySQL 中執行 `SELECT NOW()`
- **THEN** 回傳的時間 SHALL 為 UTC+8 台灣時間

#### Scenario: MySQL 容器系統時間為台灣時間
- **WHEN** MySQL 容器啟動完成
- **THEN** 容器內系統時區 SHALL 為 `Asia/Taipei`
