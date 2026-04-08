## 1. 組態檔修改

- [x] 1.1 將 `.env` 中 `FLASK_PORT` 從 `5001` 改為 `5003`
- [x] 1.2 將 `.env.example` 中 `FLASK_PORT` 從 `5001` 改為 `5003`
- [x] 1.3 將 `docker/docker-compose.yaml` 中 `FLASK_PORT` fallback 預設值改為 `5003`

## 2. 文件更新

- [x] 2.1 更新 `README.md` 中 Web 介面 port 說明為 `localhost:5003`

## 3. 驗證

- [ ] 3.1 重啟容器並確認 Web 服務可透過 `localhost:5003` 存取
