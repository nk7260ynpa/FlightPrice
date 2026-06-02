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
├── k8s/                    # Kubernetes 部署（Kustomize + 腳本）
│   ├── base/
│   ├── overlays/docker-desktop/
│   ├── scripts/
│   └── README.md
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

此指令會透過 Docker Compose 啟動 MySQL 與 Flask 應用容器。容器的 restart 政策設為 `always`，Docker daemon 啟動（包括主機重開機）時會自動拉起服務，無需手動重新執行。

- Web 介面：`http://localhost:5003`
- MySQL：`localhost:3306`

### 3. 單獨建立 Docker Image

```bash
./docker/build.sh
```

### 4. 使用 Kubernetes 部署（選用）

若想以 Kubernetes 部署（適合本機練習或為將來上雲鋪墊），需先啟用 Docker
Desktop 的內建 Kubernetes，然後：

```bash
./docker/build.sh                  # 建立本機 image
./k8s/scripts/deploy.sh            # 部署到 K8s
./k8s/scripts/port-forward.sh      # 將 svc:5000 轉發到 localhost:5003
```

常用操作：

| 動作 | 指令 |
|---|---|
| 看 log | `./k8s/scripts/logs.sh` |
| 拆除但保留資料 | `./k8s/scripts/teardown.sh` |
| 全部清掉（含 PVC） | `./k8s/scripts/purge.sh` |

詳細說明請參考 [`k8s/README.md`](k8s/README.md)。日常開發仍建議使用
`run.sh`，K8s 與 Docker Compose 兩種部署方式並存。

## 測試

```bash
pip install -r requirements.txt pytest
python -m pytest tests/ -v
```

測試使用 SQLite in-memory，不需要 MySQL 容器。

## 授權

Apache License 2.0
