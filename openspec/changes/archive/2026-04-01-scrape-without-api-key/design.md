## Context

Skyscanner 網頁有 Cloudflare「Are you a robot?」驗證，Playwright headless browser 無法通過。實測 Google Flights 無此限制，可正常載入搜尋結果並擷取價格。

## Goals / Non-Goals

**Goals:**

- 無需 API Key 即可取得航班價格
- 使用 Playwright headless browser 爬取 Google Flights 搜尋結果
- 保留 Skyscanner API Key 作為可選的優先方案

**Non-Goals:**

- 不實作 Skyscanner 網頁爬取（Cloudflare 會擋）
- 不實作反反爬蟲的進階技術

## Decisions

### 1. 爬取來源：Google Flights

**選擇**：改用 Google Flights 取代 Skyscanner 網頁爬取

**理由**：實測 Skyscanner 有 Cloudflare 驗證（Press & Hold），headless browser 無法通過。Google Flights 無此限制，頁面可正常載入並包含完整價格資料。

### 2. URL 格式

**URL**：`https://www.google.com/travel/flights?q=Flights to {destination} from {origin} on {YYYY-MM-DD} one way&curr=TWD&hl=zh-TW&gl=tw`

**理由**：使用自然語言查詢參數，Google Flights 可正確解析並回傳搜尋結果。

### 3. 價格選擇器

**選擇**：使用 `[data-gs]` CSS 選擇器取得所有航班價格文字，再用 regex `\$([\d,]+)` 解析數字。

**理由**：實測確認 `[data-gs]` 元素包含所有航班價格，格式為 `$5,699`。

### 4. 查詢鏈

```
scrape_flight_price(flight)
    │
    ▼
┌──────────────────────┐
│ 有 API Key？          │ ──→ 是 → 使用 Skyscanner API
└──────────────────────┘
    │ 否
    ▼
┌──────────────────────┐
│ Playwright 爬取       │ ──→ Google Flights [data-gs] 選擇器
│ Google Flights       │     解析最低價
└──────────────────────┘
```

## Risks / Trade-offs

- **[Google Flights DOM 結構變更]** → `[data-gs]` 選擇器可能失效，需定期維護
- **[爬取速度]** → Playwright 渲染需 10-15 秒/頁，但每 3 小時才跑一次可接受
