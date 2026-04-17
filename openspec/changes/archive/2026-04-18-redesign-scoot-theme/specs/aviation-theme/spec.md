## REMOVED Requirements

### Requirement: 航空主題色彩系統

**Reason**: 整體視覺風格由「通用航空主題」改為「酷航（Scoot）品牌風格」；原先 `--av-*` 色彩系統（深航空藍、雲朵灰白、琥珀色）全數被 `--scoot-*`（亮黃、近黑、暖米白）取代。
**Migration**: 所有引用 `--av-*` 變數或 `.navbar-aviation`、`.card-header`、`.table-aviation*`、`.btn-aviation*`、`.stat-card*`、`.badge-aviation-*` class 的模板 MUST 改為新的 `scoot-theme` 規格所定義之 class 與 tokens（見 `specs/scoot-theme/spec.md`）。原 `app/static/css/style.css` 內容 MUST 完全重寫。

### Requirement: 導航列航空風格

**Reason**: 由 `scoot-theme` 規格中的「導航列酷航風格」接手：改為亮黃實色底 + 近黑粗邊與文字，品牌文字粗體大寫。
**Migration**: 將 `base.html` 中 `navbar-aviation` 類別替換為 `scoot-theme` 對應 class（如 `navbar-scoot`），並確認 `.nav-link.active` 套用新規範定義的近黑 pill 樣式。

### Requirement: 卡片元件風格

**Reason**: 由 `scoot-theme` 規格中的「卡片元件風格」接手：改為塊面硬派邊框、hover 以邊框色變取代上浮，並支援黃色強調 header。
**Migration**: 沿用 Bootstrap `.card` 類別；既有 `.card-header` 僅需要黃色強調樣式時套用新的 `card-header-scoot`（或等同）變體。

### Requirement: 頁面背景風格

**Reason**: 由 `scoot-theme` 規格中的「頁面背景與整體排版」接手：背景色改為暖米白 `#FAFAF7`。
**Migration**: 無需模板層變更；CSS 由 `--scoot-canvas` 設定 `body` 背景。

### Requirement: 按鈕與表單風格

**Reason**: 由 `scoot-theme` 規格中的「按鈕系統」與「表單樣式」接手：按鈕主色改為黃底黑字並具「按壓邊」反饋；表單改為底邊強調樣式、聚焦時底邊轉黃。
**Migration**: 將模板中 `btn-aviation*` 系列類別替換為 `btn-scoot*` 對應層級（primary / secondary / danger / success / warning）；表單欄位保留 Bootstrap `.form-control` / `.form-select` 類別，由 `scoot-theme` CSS 接手樣式。

### Requirement: 表格風格

**Reason**: 由 `scoot-theme` 規格中的「表格風格」接手：表頭改為近黑底白字、奇偶行改為淡黃交替、價格欄改為 mono 字體右對齊。
**Migration**: 將 `.table-aviation-wrap` / `.table-aviation` 類別替換為 `scoot-theme` 所定義的類別（如 `table-scoot-wrap` / `table-scoot`），對應欄位 HTML 結構不變。

### Requirement: 統計卡片風格

**Reason**: 由 `scoot-theme` 規格中的「統計卡片風格」接手：由「左側色條 + 數字」改為「整卡塊面染色 + mono 大字」。
**Migration**: 模板中 `.stat-card`、`.stat-card-stripe*`、`.stat-card-content`、`.stat-card-label`、`.stat-card-value*` 結構 MUST 改為新規格所定義的 `.stat-scoot` 家族 class；語意色彩 mapping（danger／success／blue／amber／navy）需轉換為酷航主題的語意類別（ink／yellow／success／danger／slate）。
