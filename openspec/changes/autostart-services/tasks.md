## 1. 修改 docker-compose 設定

- [x] 1.1 將 `docker/docker-compose.yaml` 中 `db` 服務的 `restart` 由 `unless-stopped` 改為 `always`
- [x] 1.2 將 `docker/docker-compose.yaml` 中 `web` 服務的 `restart` 由 `unless-stopped` 改為 `always`

## 2. 驗證

- [x] 2.1 執行 `docker compose -f docker/docker-compose.yaml config` 確認 YAML 合法
- [x] 2.2 執行 `./run.sh` 啟動服務，確認容器正常運作
- [x] 2.3 執行 `docker inspect flightprice-db flightprice-web` 確認 RestartPolicy 為 `always`

## 3. 文件更新

- [ ] 3.1 更新 `README.md` 安裝與啟動段落，註明服務會隨 Docker daemon 自動啟動
