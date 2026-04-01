# FlightPrice

每日自動追蹤特定航班的機票價格變化，透過 Web 介面管理追蹤清單、檢視價格趨勢圖表及抓取狀態。

## 功能

- 班機管理：新增、停用、啟用追蹤班機
- 價格圖表：以 Chart.js 折線圖呈現票價隨時間的變化趨勢
- 抓取狀態：顯示今日各班機的擷取結果與統計
- 後台爬蟲：每日定時從 Skyscanner 擷取航班價格

## 專案架構

```text
FlightPrice/
├── app/                    # Flask 應用程式
│   ├── __init__.py         # 應用工廠
│   ├── models.py           # SQLAlchemy 資料模型
│   ├── scraper.py          # Skyscanner 價格擷取
│   ├── scheduler.py        # APScheduler 排程設定
│   ├── routes/             # 路由藍圖
│   │   ├── flights.py      # 班機管理
│   │   ├── charts.py       # 價格圖表
│   │   └── status.py       # 抓取狀態
│   ├── templates/          # Jinja2 模板
│   └── static/             # 靜態檔案
├── docker/                 # Docker 設定
│   ├── Dockerfile
│   ├── build.sh
│   └── docker-compose.yaml
├── tests/                  # 單元測試
├── logs/                   # 日誌檔案
├── run.sh                  # 啟動腳本
├── requirements.txt        # Python 套件依賴
└── .env.example            # 環境變數範例
```

## 技術棧

- Python 3.12 / Flask（容器時區：Asia/Taipei）
- MySQL 8.0（Docker 容器，時區：Asia/Taipei）
- SQLAlchemy ORM
- Chart.js（前端圖表）
- APScheduler（定時排程）
- Bootstrap 5（前端樣式）

## 安裝與啟動

### 1. 環境設定

```bash
cp .env.example .env
# 編輯 .env 填入 MySQL 密碼與 Skyscanner API Key
```

### 2. 啟動服務

```bash
./run.sh
```

此指令會透過 Docker Compose 啟動 MySQL 與 Flask 應用容器。

- Web 介面：`http://localhost:5000`
- MySQL：`localhost:3306`

### 3. 單獨建立 Docker Image

```bash
./docker/build.sh
```

## 測試

```bash
pip install -r requirements.txt pytest
python -m pytest tests/ -v
```

測試使用 SQLite in-memory，不需要 MySQL 容器。

## 授權

Apache License 2.0
