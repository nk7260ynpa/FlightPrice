## Context

TrackedFlight 已有 `departure_date` 欄位，但圖表頁面的下拉選單未顯示。同一班次不同出發日期時無法區分。

## Goals / Non-Goals

**Goals:**

- 下拉選單選項顯示出發日期，格式如 `CI100 (中華航空 TPE → NRT) 2026-05-01`

**Non-Goals:**

- 不改變查詢邏輯或資料 API

## Decisions

### 1. 選項格式

**選擇**：`{{ flight_number }} ({{ airline }} {{ origin }} → {{ destination }}) {{ departure_date }}`

**理由**：出發日期放在最後，與既有格式一致，不破壞視覺習慣。
