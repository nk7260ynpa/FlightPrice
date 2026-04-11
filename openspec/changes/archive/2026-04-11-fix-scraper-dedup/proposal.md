## Why

目前 `force_scrape_all_active_flights()` 繞過去重檢查，可能在同一天對同一班機產生多筆價格紀錄。且 `flight_prices` 資料表缺少唯一約束，無法在資料庫層面保證每日每班機僅一筆資料。需從應用層與資料庫層同時加固，確保每日每個班機只有一筆價格紀錄。

## What Changes

- 修改 `force_scrape_all_active_flights()`，加入去重檢查，若當日已有資料則跳過（與 `scrape_all_active_flights()` 行為一致）
- 在 `FlightPrice` 模型新增 `(flight_number, scrape_date)` 唯一約束，從資料庫層面防止重複
- 更新相關單元測試

## Capabilities

### New Capabilities

（無新增能力）

### Modified Capabilities

- `price-scraper`: 強制擷取功能須納入去重檢查，當日已有資料的班機不再重複擷取
- `data-storage`: `flight_prices` 資料表新增 `(flight_number, scrape_date)` 唯一約束

## Impact

- `app/scraper.py`：修改 `force_scrape_all_active_flights()` 邏輯
- `app/models.py`：FlightPrice 新增唯一約束
- `tests/`：更新相關測試案例
- 既有重複資料需在遷移前清理
