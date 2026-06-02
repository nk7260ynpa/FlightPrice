# FlightPrice Kubernetes 部署

本目錄提供 FlightPrice 的 Kubernetes 部署方式，與既有 `docker compose`
（`run.sh`）並存。預設目標叢集為 Docker Desktop 內建的 Kubernetes。

## 前置條件

- 已安裝 Docker Desktop 並啟用 Kubernetes（設定 → Kubernetes → Enable）。
- 確認當前 context 為 `docker-desktop`：

  ```bash
  kubectl config use-context docker-desktop
  ```

- 已準備 `.env`（複製 `.env.example` 修改密碼欄位）。
- 已執行過 `docker/build.sh` 在本機 daemon 內建立 `flightprice-app:latest`。
- **若 Docker Desktop K8s 為 kind 多節點模式**（`docker desktop kubernetes status`
  顯示 `Mode: kind` 且 `Node Count >= 2`），需額外安裝 `kind` CLI 以便將
  本機 image 載入節點：

  ```bash
  brew install kind
  ```

  `deploy.sh` 會偵測 kind 模式並自動呼叫 `load-image.sh`。

## 目錄結構

```
k8s/
├── base/                       Kustomize base（與環境無關）
│   ├── namespace.yaml
│   ├── mysql-configmap.yaml
│   ├── mysql-statefulset.yaml
│   ├── app-configmap.yaml
│   ├── logs-pvc.yaml
│   ├── app-deployment.yaml     # 注意：replicas 必須為 1（見下方）
│   ├── app-service.yaml
│   └── kustomization.yaml
├── overlays/
│   └── docker-desktop/         本機 overlay：imagePullPolicy: Never
│       ├── image-policy-patch.yaml
│       └── kustomization.yaml
└── scripts/
    ├── deploy.sh               檢查 .env → 產生 Secret → 載入 image → apply → 等待 Ready
    ├── teardown.sh             刪除工作負載但保留 PVC
    ├── purge.sh                連同 PVC 與 namespace 一併刪除（會二次確認）
    ├── load-image.sh           將本機 image 載入 kind 節點（kind 模式必需）
    ├── logs.sh                 即時追蹤 Flask 容器 stdout
    └── port-forward.sh         localhost:5003 → svc:5000
```

## 快速啟動

```bash
# 1. 建置本機 image
./docker/build.sh

# 2. 部署到 K8s
./k8s/scripts/deploy.sh

# 3. 將 cluster 內 service 轉發到本機 5003（前景執行，Ctrl-C 結束）
./k8s/scripts/port-forward.sh
```

瀏覽器訪問 <http://localhost:5003/flights>。

## 常用操作

| 動作 | 指令 |
|---|---|
| 看 log（追蹤模式） | `./k8s/scripts/logs.sh` |
| 查看 pod 狀態 | `kubectl -n flightprice get pods` |
| 進入 MySQL CLI | `kubectl -n flightprice exec -it sts/mysql -- mysql -uroot -p"$MYSQL_ROOT_PASSWORD"` |
| 強制重啟 app pod | `kubectl -n flightprice delete pod -l app=flightprice-app` |
| 拆除但保留資料 | `./k8s/scripts/teardown.sh` |
| 全部清掉 | `./k8s/scripts/purge.sh` |

## 設計重點

### Flask Deployment 固定 `replicas: 1`

`app/scheduler.py` 的 APScheduler `BackgroundScheduler` 是 in-process
singleton。若 Deployment 跑多個 replica，每小時的 `periodic_scrape` 會被
重複觸發、污染 `ScrapeLog` 與 `flight_prices`。

未來若要水平擴展，請另開 OpenSpec change，將排程抽到獨立 Deployment
或改用 K8s CronJob。

### Secret 從 `.env` 動態產生

`deploy.sh` 以下列方式產生 `flightprice-secret`：

```bash
kubectl -n flightprice create secret generic flightprice-secret \
  --from-env-file=.env --dry-run=client -o yaml | kubectl apply -f -
```

明文密碼僅存在於本機 `.env`，不會進入 git；`flightprice-secret` 物件本身
也不在 manifest 倉庫中。

### `imagePullPolicy: Never`

`overlays/docker-desktop/image-policy-patch.yaml` 強制使用本機 daemon
內已 build 的 `flightprice-app:latest`，避免叢集嘗試從遠端 registry 拉取。
若 pod 出現 `ErrImageNeverPull` 狀態，表示尚未執行 `docker/build.sh`。

### PVC 生命週期

- `mysql-data`：由 StatefulSet `volumeClaimTemplates` 自動建立，1Gi。
- `flightprice-logs`：獨立 PVC，1Gi，掛載於 `/app/logs`。

`teardown.sh` 不刪 PVC，故重新 `deploy.sh` 後資料保留；要徹底清空請執行
`purge.sh`（連同 namespace 一併刪除）。

## 疑難排解

| 症狀 | 可能原因 / 處理 |
|---|---|
| `flightprice-app` pod 狀態為 `ErrImageNeverPull` | （1）尚未 `./docker/build.sh`；或（2）未執行 `load-image.sh` 將 image 載入 kind 節點（需先 `brew install kind`）。 |
| `wait-for-mysql` initContainer 一直卡住 | MySQL pod 尚未 Ready；`kubectl -n flightprice describe pod mysql-0` 看 events。 |
| 修改程式碼後行為沒變 | K8s 跑的是 image 內的舊版；需重新 `./docker/build.sh` 並 `kubectl -n flightprice rollout restart deployment/flightprice-app`。 |
| 端口被佔用 | `LOCAL_PORT=5004 ./k8s/scripts/port-forward.sh`。 |
| Reset Kubernetes Cluster 後資源全部消失 | 直接重新 `./k8s/scripts/deploy.sh` 即可，image 仍在本機 daemon。 |

## 與 Docker Compose 的差異

| 項目 | Docker Compose | Kubernetes |
|---|---|---|
| 啟動指令 | `./run.sh` | `./k8s/scripts/deploy.sh` |
| 對外 port | host 5003 自動綁定 | 需 `port-forward.sh` |
| logs 觀察 | 直接 `tail -f logs/flightprice.log` | `./k8s/scripts/logs.sh`（kubectl logs） |
| 修改程式碼 | `docker compose up --build -d` 自動 rebuild | 需手動 `build.sh` + `rollout restart` |
| 資料保留 | named volume `mysql_data` | PVC `mysql-data-mysql-0` |

日常開發推薦繼續用 `run.sh`；K8s 路徑適合學習、驗證部署形態、或為將來
上雲鋪墊。
