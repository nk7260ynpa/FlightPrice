## Context

FlightPrice Web 服務目前透過 `.env` 的 `FLASK_PORT=5001` 設定對外 port，但 5001 已被本機其他容器（docker-web-1）佔用，導致存取衝突。需將 port 改為 5002。

## Goals / Non-Goals

**Goals:**

- 將 Web 服務對外 port 改為 5002，解除 port 衝突
- 同步更新所有相關組態檔與文件

**Non-Goals:**

- 不變更容器內部 Flask 運行的 port（仍為 5000）
- 不調整 MySQL 的 port 設定

## Decisions

### 統一修改所有 port 預設值

修改範圍：

1. `.env`：`FLASK_PORT=5001` → `FLASK_PORT=5002`
2. `.env.example`：`FLASK_PORT=5001` → `FLASK_PORT=5002`
3. `docker/docker-compose.yaml`：fallback `${FLASK_PORT:-5000}` → `${FLASK_PORT:-5002}`
4. `README.md`：Web 介面說明 `localhost:5000` → `localhost:5002`

**理由**：確保所有進入點的 port 資訊一致，避免使用者混淆。

## Risks / Trade-offs

- [風險] 使用者若有其他服務佔用 5002 → 使用者可自行透過 `.env` 調整 `FLASK_PORT`
- [風險] 舊容器未重啟仍綁定舊 port → 需重新 `docker compose up` 才能生效
