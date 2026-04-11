## 1. 資料模型修改

- [x] 1.1 在 `app/models.py` 的 FlightPrice 模型新增 `UniqueConstraint('flight_number', 'scrape_date')`

## 2. 爬蟲邏輯修改

- [x] 2.1 在 `app/scraper.py` 的 `scrape_flight_price()` 加入去重檢查，若當日已有該班機資料則直接回傳 None
- [x] 2.2 移除 `scrape_all_active_flights()` 中重複的去重檢查邏輯（已移至底層）
- [x] 2.3 移除 `force_scrape_all_active_flights()` 函式
- [x] 2.4 移除所有呼叫 `force_scrape_all_active_flights()` 的路由或引用

## 3. 測試更新

- [x] 3.1 新增或更新測試：驗證當日已有資料時 `scrape_flight_price()` 跳過擷取
- [x] 3.2 新增測試：驗證 FlightPrice 唯一約束拒絕重複寫入
- [x] 3.3 執行全部測試確認通過
