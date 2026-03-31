## 1. MySQL 認證修正

- [x] 1.1 docker-compose.yaml 加上 `--default-authentication-plugin=mysql_native_password`
- [x] 1.2 重建 MySQL 容器驗證外部工具可連線

## 2. 多段航班查詢改造

- [x] 2.1 修改 Flightradar24 爬取：從 `_extract_fr24_airport` 改為 `_extract_fr24_routes`，解析所有不重複航段
- [x] 2.2 修改 `_lookup_via_flightradar24` 回傳航段列表
- [x] 2.3 修改 `_lookup_via_aviationstack` 回傳航段列表格式
- [x] 2.4 修改 `_lookup_from_db_cache` 回傳航段列表格式
- [x] 2.5 修改 `_lookup_from_code_table` 回傳航段列表格式
- [x] 2.6 修改 `lookup_flight_info` 統一回傳列表格式
- [x] 2.7 修改 `/api/flights/lookup` 回傳 `{routes: [...]}`

## 3. 前端航段選擇器

- [x] 3.1 修改 flights.html JavaScript：處理 routes 陣列回傳
- [x] 3.2 新增航段選擇下拉選單：routes 長度 > 1 時動態顯示
- [x] 3.3 routes 長度 = 1 時維持原行為直接填入

## 4. 智慧排程爬蟲

- [x] 4.1 修改 scheduler.py：從 cron daily 改為 interval 每 3 小時
- [x] 4.2 修改 scraper.py 的 scrape_all_active_flights：新增當日資料檢查
- [x] 4.3 已有當日資料的班機跳過，回傳結果增加 skipped 計數

## 5. 測試與驗證

- [ ] 5.1 更新 test_flight_lookup.py：所有查詢函式回傳改為列表格式
- [ ] 5.2 更新 test_flights.py：lookup API 回傳改為 routes 陣列
- [ ] 5.3 新增多段航班解析與當日資料跳過的測試
- [ ] 5.4 執行全部測試確認無回歸
- [ ] 5.5 重建 Docker 容器驗證所有變更
