## 1. Web 容器時區設定

- [x] 1.1 修改 `docker/Dockerfile`，新增 `ENV TZ=Asia/Taipei` 並透過 `ln -sf /usr/share/zoneinfo/Asia/Taipei /etc/localtime` 設定系統時區

## 2. MySQL 容器時區設定

- [x] 2.1 修改 `docker/docker-compose.yaml`，為 `db` 服務新增環境變數 `TZ: Asia/Taipei`

## 3. Web 容器 Compose 時區設定

- [x] 3.1 修改 `docker/docker-compose.yaml`，為 `web` 服務新增環境變數 `TZ: Asia/Taipei`

## 4. 驗證與文件

- [x] 4.1 重建 Docker image 並啟動容器，驗證 web 與 db 容器時區皆為 `Asia/Taipei`
- [x] 4.2 更新 README.md 說明容器時區設定
