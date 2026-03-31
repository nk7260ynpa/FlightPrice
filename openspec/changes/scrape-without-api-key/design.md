## Context

Skyscanner 和 Google Flights 都是 JavaScript SPA，靜態 HTML 不含價格資料。需使用 headless browser 渲染頁面後解析 DOM 取得價格。目前 scraper.py 依賴 Skyscanner Partners API Key。

## Goals / Non-Goals

**Goals:**

- 無需 API Key 即可取得航班價格
- 使用 Playwright headless browser 爬取 Skyscanner 網頁搜尋結果
- 保留 API Key 作為可選的優先方案（有 Key 用 API，無 Key 用網頁爬取）

**Non-Goals:**

- 不實作 Google Flights 爬取（Skyscanner 為主要來源即可）
- 不實作反反爬蟲的進階技術（如 proxy rotation）

## Decisions

### 1. Headless browser：Playwright

**選擇**：使用 Playwright（Python 版）

**理由**：Playwright 比 Selenium 更現代、更快、API 更簡潔。內建等待機制適合 SPA 頁面。支援 headless Chromium。

**替代方案**：Selenium（較笨重、需額外 WebDriver）

### 2. 爬取策略

**選擇**：構造 Skyscanner 搜尋 URL，用 Playwright 渲染後等待價格元素出現，解析最低價。

**URL 格式**：`https://www.skyscanner.com.tw/transport/flights/{origin}/{destination}/{date}/?adultsv2=1&cabinclass=economy&rtn=0`

**日期格式**：`YYMMDD`（如 `260501` 代表 2026-05-01）

### 3. 查詢鏈

```
scrape_flight_price(flight)
    │
    ▼
┌──────────────────────┐
│ 有 API Key？          │ ──→ 是 → 使用 Skyscanner API（原有邏輯）
└──────────────────────┘
    │ 否
    ▼
┌──────────────────────┐
│ Playwright 爬取       │ ──→ 渲染 Skyscanner 網頁，解析最低價
│ Skyscanner 網頁      │
└──────────────────────┘
```

### 4. Docker 整合

**選擇**：在 Dockerfile 中安裝 Playwright 及 Chromium 瀏覽器

**注意**：Playwright 的 Chromium 需要額外系統依賴（libglib、libnss 等），Dockerfile 需要 `playwright install --with-deps chromium`

## Risks / Trade-offs

- **[Skyscanner 頁面結構變更]** → DOM 選擇器可能失效，需定期維護
- **[反爬蟲機制]** → Skyscanner 可能封鎖頻繁請求，需設定合理間隔
- **[Docker image 變大]** → Chromium 瀏覽器約增加 300MB，可接受
- **[爬取速度較慢]** → Playwright 渲染需 5-15 秒/頁，比 API 慢，但每 3 小時才跑一次可接受
