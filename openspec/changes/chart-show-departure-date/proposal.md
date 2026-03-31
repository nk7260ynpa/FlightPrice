## Why

價格趨勢圖表頁面的班機選擇下拉選單目前僅顯示班次代碼與航線，但同一班次可能有不同出發日期的追蹤紀錄，使用者無法區分要查看哪一筆。需在選項中加上出發日期。

## What Changes

- 圖表頁面班機選擇下拉選單的選項文字加上出發日期

## Capabilities

### New Capabilities

（無）

### Modified Capabilities

- `price-chart-page`: 班機選擇下拉選單選項增加出發日期顯示

## Impact

- `app/templates/charts.html`：下拉選單 option 文字格式調整
