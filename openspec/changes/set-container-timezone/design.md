## Context

目前所有 Docker 容器（web、db）皆使用預設的 UTC 時區。專案的 log、排程、資料庫時間紀錄與台灣使用者的實際時間存在 8 小時差距，增加除錯與資料判讀的難度。

現有 Docker 設定：
- `docker/Dockerfile`：基於 `python:3.12-slim`（Debian），未設定時區
- `docker/docker-compose.yaml`：包含 `web`（Flask）與 `db`（MySQL 8.0）兩個服務，均未設定時區

## Goals / Non-Goals

**Goals:**
- 將 web 容器的系統時區設定為 `Asia/Taipei`
- 將 MySQL 容器的時區設定為 `Asia/Taipei`
- 確保 Python logging 與 MySQL `NOW()` 皆回傳台灣時間

**Non-Goals:**
- 不修改應用程式碼中的時間處理邏輯
- 不引入額外的時區管理工具或套件
- 不處理跨時區顯示需求

## Decisions

### 決策 1：Web 容器時區設定方式

**選擇**：在 Dockerfile 中透過環境變數 `TZ=Asia/Taipei` 搭配 `ln -sf` 設定 `/etc/localtime`

**替代方案**：
- 僅設定 `TZ` 環境變數 → 部分工具不讀取 `TZ`，可能不一致
- 在 docker-compose.yaml 掛載主機 `/etc/localtime` → 跨平台不相容（macOS 無此檔案路徑）
- 安裝 `tzdata` 套件後用 `dpkg-reconfigure` → 過於複雜

**理由**：`python:3.12-slim` 基於 Debian，已包含 `/usr/share/zoneinfo` 時區資料。透過 `ln -sf` 加上 `TZ` 環境變數是最輕量且可靠的做法。

### 決策 2：MySQL 容器時區設定方式

**選擇**：在 docker-compose.yaml 中設定環境變數 `TZ=Asia/Taipei`

**替代方案**：
- 透過 MySQL 設定檔 `default-time-zone='+08:00'` → 需額外掛載設定檔
- 在 SQL init script 中執行 `SET GLOBAL time_zone` → 每次重啟需重新執行

**理由**：MySQL 官方映像支援 `TZ` 環境變數，設定簡單且隨容器生命週期自動生效。

## Risks / Trade-offs

- **[風險] 既有資料時間欄位解讀差異** → 本專案尚在初始階段，資料庫無既有資料，無需遷移。若未來有既有資料，需注意 DATETIME 欄位儲存的是無時區資訊的本地時間。
- **[風險] slim 映像可能缺少時區資料** → 已確認 `python:3.12-slim` 包含 `/usr/share/zoneinfo`，無需額外安裝 `tzdata`。
- **[取捨] 硬編碼時區 vs 可配置** → 本專案僅面向台灣使用者，硬編碼 `Asia/Taipei` 足夠，避免不必要的複雜度。
