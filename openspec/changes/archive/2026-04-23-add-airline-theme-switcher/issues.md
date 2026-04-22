# Issues — add-airline-theme-switcher

本檔供 Specialist 回報 spec／tasks.md 範圍外但影響實作完整度的疑慮，交由
Coordinator 評估後決定是否更新 tasks 或 spec。

---

## [Specialist] [2026-04-18] [LOW] README.md 未涵蓋多主題架構說明

Task 8.1 要求檢查 `README.md` 是否需補充多主題說明。檢查結果：

- 目前 `README.md` 的「功能」與「技術棧」章節皆未提及多主題能力。
- 「專案架構」段落的 `app/static/` 下僅顯示 `css/`，未提及新增的 `js/`
  子目錄（含 `theme-switcher.js`）。

建議補充（若 Coordinator 認同，請更新 `tasks.md` 將 `README.md` 納入
新任務範圍後，再由 Specialist 實作；Specialist 不得直接修改 `README.md`）：

1. 「功能」章節新增一條目：「多品牌主題：Scoot / EVA / China Airlines
   / Starlux 即時切換，localStorage 持久化」。
2. 「技術棧」章節補上「CSS `[data-theme]` attribute + CSS custom
   properties 主題架構」。
3. 「專案架構」段落於 `app/static/` 下加入 `js/theme-switcher.js`
   說明；或直接擴展成 `css/` + `js/`。

本項為低優先；即便不更新 `README.md`，目前功能與測試皆完整，對使用者
流程無影響。

---

## [Specialist] [2026-04-18] [LOW] Docker 測試路徑雙層副本

於 `/opsx:apply` 過程中以 `docker cp tests flightprice-web:/app/tests`
同步檔案時，pytest discovery 會收到 `tests/` 與 `tests/tests/` 兩份
相同測試（188 = 94×2）。此為 container 內目錄結構殘留，不影響實作正確
性；Verifier 若執行 `docker compose run --rm app pytest tests/` 於乾淨
容器內即為單份（94 項）。本項純粹為環境提示，無需 spec 變更。
