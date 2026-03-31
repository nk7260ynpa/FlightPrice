## Why

目前價格擷取依賴 Skyscanner Partners API Key，該 API 為申請制且對個人用途難以取得。需改為網頁爬取方式，無需 API Key 即可取得航班價格。Skyscanner 和 Google Flights 都是 JavaScript SPA，需使用 headless browser（Playwright）渲染頁面後擷取價格。

## What Changes

- 新增 Playwright 作為 headless browser 依賴
- 改用 Google Flights 作為網頁爬取來源（Skyscanner 有 Cloudflare 驗證會被擋）
- 移除 SKYSCANNER_API_KEY 的必要性（改為選用，有 API Key 時優先使用 Skyscanner API，無則爬 Google Flights）
- Dockerfile 需安裝 Playwright 瀏覽器

## Capabilities

### New Capabilities

（無）

### Modified Capabilities

- `price-scraper`: 價格擷取改為 Playwright 網頁爬取，API Key 變為選用

## Impact

- `app/scraper.py`：改寫價格擷取邏輯
- `requirements.txt`：新增 playwright 依賴
- `docker/Dockerfile`：安裝 Playwright 瀏覽器
- `.env.example`：SKYSCANNER_API_KEY 改為選用說明
