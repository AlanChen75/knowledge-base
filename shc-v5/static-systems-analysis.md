# 靜態網頁開源系統分析 — GitHub Pages 教學案例

## 部署優先序

### 第一階段（零建置，直接部署）

| 系統 | 類別 | GitHub | 技術 |
|------|------|--------|------|
| localstorage-markdown-editor | 筆記本 | ConcurrentHashMap/localstorage-markdown-editor | Vanilla JS, LocalStorage |
| my-todo-app | 待辦 | developer-az/my-todo-app | Vanilla JS, Tailwind |
| Budget-Tracker-Javascript | 預算 | ayush8303/Budget-Tracker-Javascript | HTML/CSS/JS |
| PlainAdmin | 儀表板 | PlainAdmin/plain-free-bootstrap-admin-template | Bootstrap 5, Vanilla JS |
| kanban-light | 看板(MES替代) | mmvergara/kanban-light | Pure JS, LocalStorage |

### 第二階段（簡單設定）

| 系統 | 類別 | GitHub | 技術 |
|------|------|--------|------|
| E-Com-LocalStorage | 電商 | SAD0XER/E-Com-LocalStorage | HTML/CSS/JS |
| Inventory Management | 庫存(ERP替代) | edilancode/inventory-management-System-HTML-CSS-JavaScript | Vanilla JS |
| Kanban-Board | 看板 | mtrong100/Kanban-Board | HTML/CSS/JS |
| offline-todo | 離線應用 | matthew-andrews/offline-todo | IndexedDB |
| Volt Dashboard | 儀表板 | themesberg/volt-bootstrap-5-dashboard | Bootstrap 5 |

### 第三階段（需建置步驟）

| 系統 | 類別 | GitHub | 技術 |
|------|------|--------|------|
| Laverna | 加密筆記 | Laverna/laverna | JS, IndexedDB |
| PWA POS Terminal | POS | Asatelit/pwa-pos-terminal | React, TypeScript, IndexedDB |
| TUI Calendar | 行事曆 | nhn/tui.calendar | Pure JS |

## 關鍵發現

1. **ERP/MES**: 純靜態版本少，用庫存管理+看板系統替代
2. **電商**: 多個成熟的 LocalStorage 方案可用
3. **POS**: IndexedDB 方案功能完整，支援離線
4. **筆記本**: Laverna 最完整，但需建置；markdown-editor 最簡單
5. **儀表板**: PlainAdmin、Volt 都是零建置、零 jQuery

## 教學價值

- 初級：Todo、Budget Tracker（CRUD + LocalStorage）
- 中級：電商、庫存管理（複雜資料結構 + 搜尋）
- 進階：POS、Laverna（IndexedDB + PWA + 加密）
