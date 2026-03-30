## Context

FlightPrice 是一個全新專案，目標是每日追蹤特定航班的機票價格變化。使用者透過 Web 介面管理追蹤清單、檢視價格趨勢圖表及當日抓取狀態。資料來源為 Skyscanner，所有服務透過 Docker 容器執行。

## Goals / Non-Goals

**Goals:**

- 建立可運作的機票價格追蹤系統，包含資料擷取、儲存、視覺化
- 所有服務容器化，透過 docker-compose 一鍵啟動
- 提供直覺的 Web 介面管理追蹤班機與檢視價格趨勢

**Non-Goals:**

- 不實作自動購票或價格提醒通知功能
- 不支援多使用者認證與權限管理
- 不實作即時價格更新（僅每日定時擷取）

## Decisions

### 1. Web 框架：Flask

**選擇**：Flask + Jinja2 模板引擎

**理由**：專案規模適中，Flask 輕量且容易上手，搭配 Jinja2 可快速建立伺服器端渲染頁面，不需要前後端分離的複雜架構。

**替代方案**：Django（過於龐大）、FastAPI + React（前後端分離增加複雜度）

### 2. 圖表套件：Chart.js

**選擇**：前端使用 Chart.js 渲染折線圖

**理由**：Chart.js 輕量、無需後端渲染、互動性佳，適合呈現時間序列價格趨勢。後端僅需提供 JSON 資料即可。

**替代方案**：Matplotlib 生成靜態圖片（互動性差）、Plotly（較肥大）

### 3. 資料庫：MySQL via Docker

**選擇**：使用官方 MySQL Docker image，透過 docker-compose 管理

**理由**：符合使用者指定需求，MySQL 成熟穩定，Docker 化便於部署與環境一致性。

### 4. 資料擷取方式：Skyscanner API

**選擇**：透過 Skyscanner API 擷取航班價格資訊

**理由**：API 方式穩定可靠，比網頁爬蟲更不易因頁面改版而失效。若 API 存取受限，可退而使用 requests + BeautifulSoup 爬蟲方案。

### 5. 航班資訊查詢：AviationStack API

**選擇**：使用 AviationStack API 根據班次代碼查詢航空公司、出發地、抵達地

**理由**：AviationStack 提供免費方案，支援以航班號碼查詢航班詳細資訊（航空公司、出發/抵達機場），可簡化使用者輸入流程。若 API 不可用，退而使用內建的 IATA 航空公司代碼對照表解析班次代碼前綴。

**替代方案**：FlightAware API（付費）、手動維護航班資料庫（維護成本高）

### 6. 排程機制：APScheduler

**選擇**：使用 APScheduler 在 Flask 應用內執行每日定時抓取任務

**理由**：無需額外的 cron 容器或系統排程，APScheduler 可直接整合至 Flask 應用中，簡化部署架構。

**替代方案**：系統 crontab（需額外設定）、Celery + Redis（過於複雜）

### 7. 專案結構

```
FlightPrice/
├── docker/
│   ├── Dockerfile
│   ├── build.sh
│   └── docker-compose.yaml
├── app/
│   ├── __init__.py          # Flask 應用工廠
│   ├── models.py            # SQLAlchemy 資料模型
│   ├── flight_lookup.py     # 航班資訊查詢
│   ├── scraper.py           # Skyscanner 價格擷取
│   ├── scheduler.py         # APScheduler 排程設定
│   ├── routes/
│   │   ├── flights.py       # 追蹤班機管理路由
│   │   ├── charts.py        # 價格圖表路由
│   │   └── status.py        # 抓取狀態路由
│   ├── templates/
│   │   ├── base.html
│   │   ├── flights.html     # 班機管理頁面
│   │   ├── charts.html      # 價格圖表頁面
│   │   └── status.html      # 抓取狀態頁面
│   └── static/
├── logs/
├── tests/
├── run.sh
├── requirements.txt
└── README.md
```

## Risks / Trade-offs

- **[Skyscanner API 存取限制]** → 若 API 需付費或有速率限制，需評估替代資料來源或調整抓取頻率
- **[資料擷取失敗]** → 每次抓取需記錄成功/失敗狀態，失敗時記錄錯誤原因供抓取狀態頁面顯示
- **[MySQL 容器資料持久化]** → 使用 Docker volume 掛載資料目錄，避免容器重建時遺失資料
