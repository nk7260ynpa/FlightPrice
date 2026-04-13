## ADDED Requirements

### Requirement: 航空主題色彩系統

系統 SHALL 提供以航空為主題的統一色彩系統，透過 CSS 自訂屬性定義於 `:root`，所有頁面元件 MUST 引用這些變數以保持視覺一致性。

#### Scenario: 色彩變數可用
- **WHEN** 任一頁面載入
- **THEN** `:root` 中 SHALL 定義導航深藍 (`--av-navy`)、航空藍 (`--av-blue`)、琥珀色 (`--av-amber`)、雲朵灰白 (`--av-cloud`)、卡片白 (`--av-white`) 等主題色彩��數

### Requirement: 導航列航空風格

導航列 SHALL 使用深航空藍 (`#1e3a5f`) 背景，品牌名稱前 MUST 包含飛機符號 (✈)，導航連結文字為白色。

#### Scenario: 導��列顯示
- **WHEN** 使用者瀏覽任一頁面
- **THEN** 頂部導航列 SHALL 顯示深航空藍背景、白色文字、飛機圖標品牌

#### Scenario: 當前頁面導航高亮
- **WHEN** 使用者位於某一頁面
- **THEN** 該���面對應的��航連結 SHALL 以較亮的色調或底線標示為當前頁

### Requirement: 卡片元件風格

所有內容卡片 SHALL 使用白色背景、圓角邊框、柔和陰影，並在滑鼠懸���時提升陰影深度產生浮起效果。

#### Scenario: 卡片靜態顯示
- **WHEN** 頁面載入包含卡片的內容區塊
- **THEN** 卡片 SHALL 顯示白���背景、圓角 (`border-radius >= 12px`)、柔和陰影

#### Scenario: 卡片懸浮效果
- **WHEN** 使用者將滑鼠移至卡片上方
- **THEN** 卡片陰影 SHALL 加深，並產生微幅上移的視覺效果

### Requirement: 頁面背景風格

所有頁面的 `body` 背景色 SHALL 為雲朵灰白 (`#f0f4f8`)，與白色卡片形成層次對比。

#### Scenario: 頁面背景
- **WHEN** 使用者瀏覽任一頁面
- **THEN** 頁面背景 SHALL 為 `#f0f4f8` 灰白色調

### Requirement: 按鈕與表單風格

主要操作按鈕 SHALL 使用航空藍色系，危險操作按鈕保持紅色系。表單輸入框 SHALL 使用圓角樣式與聚焦時的航空藍邊框。

#### Scenario: 主要按鈕樣式
- **WHEN** 頁面顯示主要操作按鈕（如新增班機、查詢）
- **THEN** 按鈕 SHALL 使用航空藍背景色與白色文字

#### Scenario: 表單輸入聚焦
- **WHEN** 使用者點擊表單輸入框
- **THEN** 輸入框 SHALL 顯示航空藍色邊框與柔和藍色外暈

### Requirement: 表格風格

資料表格 SHALL 使用圓角��器包裹，表頭使用深航空藍背景與白色文字，行列交替使��極淺藍灰色背景。

#### Scenario: 表格顯示
- **WHEN** 頁面載入包含資料表格的區塊
- **THEN** 表頭 SHALL 為深航空藍背景白色文字，資料行交替淺色背景

### Requirement: 統計卡片風格

圖表頁與狀態頁的統計數據卡片 SHALL 使用左側色條標示類型，數值以大字號顯示。

#### Scenario: 統計卡片顯示
- **WHEN** 頁面包含統計數據（最高價、最低價、成功數、失敗數等）
- **THEN** 每張統計卡片 SHALL 顯示左側色條、大字號數值、次要說明文字
