## Context

排程每 3 小時自動抓取且會跳過當日已有資料的班機。使用者有時需要手動觸發立即抓取，不受當日資料檢查限制。

## Goals / Non-Goals

**Goals:**

- 在抓取狀態頁面提供「立即抓取」按鈕
- 點擊後對所有啟用班機執行強制抓取（不檢查當日是否已有資料）
- 抓取完成後顯示結果摘要

**Non-Goals:**

- 不支援選擇性抓取單一班機（全部啟用班機一起抓）
- 不實作非同步抓取（同步執行，等待完成後回傳結果）

## Decisions

### 1. 強制抓取路由

**選擇**：POST `/status/scrape`，執行完成後 redirect 回 `/status` 並以 flash 顯示結果

**理由**：POST 避免重複提交，flash 訊息在 redirect 後自動顯示在頁面頂部。

### 2. 強制抓取邏輯

**選擇**：在 `scraper.py` 新增 `force_scrape_all_active_flights`，與 `scrape_all_active_flights` 類似但跳過當日資料檢查

**理由**：保持原有 `scrape_all_active_flights`（排程用）不變，強制抓取用獨立函式。

## Risks / Trade-offs

- **[同步執行可能較慢]** → 班機數量少時可接受，大量班機時可能需等待數秒
