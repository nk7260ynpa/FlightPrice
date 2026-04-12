## 1. 修改爬蟲查詢邏輯

- [x] 1.1 修改 `app/scraper.py` 的 `scrape_all_active_flights()`，將查詢條件從 `filter_by(is_active=True)` 改為同時加入 `TrackedFlight.departure_date >= date.today()` 過濾

## 2. 測試

- [x] 2.1 在 `tests/test_scraper.py` 新增測試案例：出發日期已過的航班不應被選入爬取清單
- [x] 2.2 在 `tests/test_scraper.py` 新增測試案例：出發日期為今天的航班仍應被選入爬取清單
- [ ] 2.3 執行全部測試確認無迴歸
