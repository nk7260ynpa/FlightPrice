## Context

FlightPrice 透過 `docker/docker-compose.yaml` 啟動兩個容器：`flightprice-db`（MySQL 8.0）與 `flightprice-web`（Flask）。目前兩者皆使用 `restart: unless-stopped`，此政策在容器被使用者手動停止後，即使 Docker daemon 重啟（例如主機重開機），也不會自動拉起容器。實務上常發生重開機後服務未啟動、需手動執行 `run.sh` 的情況。

## Goals / Non-Goals

**Goals:**
- 主機開機後（Docker daemon 啟動時）`flightprice-db` 與 `flightprice-web` 容器自動啟動
- 容器異常崩潰時自動重啟
- 不需額外 systemd unit 或作業系統層級設定

**Non-Goals:**
- 不新增主機 OS 層級的開機服務（不涉及 systemd / launchd）
- 不改變現有 `run.sh` 的啟動流程
- 不處理 Docker daemon 本身是否隨開機啟動（由使用者環境決定）

## Decisions

### 決策 1：使用 `restart: always` 取代 `restart: unless-stopped`

**選擇**：將 `db` 與 `web` 服務的 `restart` 政策統一設為 `always`。

**理由**：
- `always`：Docker daemon 啟動時永遠拉起容器，不論先前狀態為何——符合「開機就啟動」需求
- `unless-stopped`：若容器曾被手動 `docker stop`，重開機後不會啟動——不符需求
- `on-failure`：僅於非零退出碼重啟，不處理 daemon 重啟——不符需求

**替代方案**：在 OS 層撰寫 systemd unit 呼叫 `docker compose up`。被否決，因為增加維運複雜度，且 Docker 原生 `restart: always` 已能達成目標。

## Risks / Trade-offs

- [風險] 開發者本地端也會被自動拉起容器，可能干擾開發 → 緩解：開發者可執行 `docker compose down` 完全移除容器，或於需要時調整本地 override
- [風險] 若容器進入 crash loop，會持續重啟並產生大量 log → 緩解：既有 logging 機制已寫入 `logs/`，可於異常時檢視；必要時執行 `docker compose down` 停止
