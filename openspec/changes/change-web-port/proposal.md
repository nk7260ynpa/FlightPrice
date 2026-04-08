## Why

目前 FlightPrice Web 服務對外 port 為 5001，與本機其他服務（docker-web-1）衝突，需改為 5002 以避免 port 佔用問題。

## What Changes

- 將 `.env` 中 `FLASK_PORT` 預設值從 `5001` 改為 `5002`
- 將 `.env.example` 中 `FLASK_PORT` 預設值同步更新為 `5002`
- 更新 `docker-compose.yaml` 中 `FLASK_PORT` 的 fallback 預設值為 `5002`
- 更新 `README.md` 中 Web 介面的 port 說明

## Capabilities

### New Capabilities

（無新增功能）

### Modified Capabilities

（無規格層級的行為變更，僅為組態調整）

## Impact

- `docker/docker-compose.yaml`：port mapping 預設值變更
- `.env` / `.env.example`：環境變數預設值變更
- `README.md`：文件說明更新
- 使用者需重啟容器才能生效
