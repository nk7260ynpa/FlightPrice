## Why

目前 Docker 容器使用預設的 UTC 時區，導致 log 時間戳記、排程任務及資料庫時間紀錄與台灣實際時間不一致（差距 +8 小時），造成除錯與資料分析上的困擾。需將容器時區統一設定為 `Asia/Taipei`（UTC+8）。

## What Changes

- 修改 Dockerfile，於映像建置階段設定系統時區為 `Asia/Taipei`
- 修改 docker-compose.yaml，為 web 與 db 容器設定時區環境變數
- 確保 MySQL 容器的時區同步為台灣時間

## Capabilities

### New Capabilities

- `container-timezone`: 容器時區設定，確保所有服務容器使用台灣時間（Asia/Taipei）

### Modified Capabilities

（無既有規格需修改）

## Impact

- `docker/Dockerfile`：新增時區設定指令
- `docker/docker-compose.yaml`：新增時區環境變數與 volume 掛載
- 所有容器內的 log 時間戳記將從 UTC 變為 UTC+8
- MySQL 的 `NOW()` 等時間函式將回傳台灣時間
