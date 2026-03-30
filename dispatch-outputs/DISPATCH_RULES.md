---
title: Dispatch 產出格式規範
date: 2026-03-30
category: dispatch-outputs
tags: [規範, template]
type: note
_skip_sync: true
---

# Dispatch 產出格式規範

## 目的

所有 Claude dispatch 對話結束時，產出的 .md 檔案必須符合此格式，
讓 `notion-sync.py` 能自動解析 frontmatter 並正確寫入 Notion。

---

## 必填 Frontmatter

```yaml
---
title: 標題（簡潔，30 字內）
date: YYYY-MM-DD
category: 分類路徑（見下方分類表）
tags: [標籤1, 標籤2, 標籤3]
type: analysis | course-design | research | brainstorm | plan | report
source: 來源描述或 URL（選填）
project: 關聯專案名稱（需與 Notion 專案總覽一致，選填）
priority: P0 | P1 | P2（選填）
status: draft | review | final（預設 draft）
---
```

### 欄位說明

| 欄位 | 必填 | 說明 |
|------|------|------|
| title | ✅ | 簡潔標題，會成為 Notion 頁面標題 |
| date | ✅ | 產出日期 YYYY-MM-DD |
| category | ✅ | 分類路徑，對應 notion-sync.py 的 Group 分類 |
| tags | ✅ | 最多 10 個標籤 |
| type | ✅ | 文件類型（見下方） |
| source | ⬜ | 觸發這份產出的來源（URL、對話、人名） |
| project | ⬜ | 關聯的 Notion 專案名稱 |
| priority | ⬜ | P0 緊急 / P1 重要 / P2 可緩 |
| status | ⬜ | draft 初稿 / review 待審 / final 定稿 |

---

## Type 類型定義

| type | 用途 | 範例 |
|------|------|------|
| analysis | 深度分析報告 | CC-BOS 論文分析、競品分析 |
| course-design | 課程設計 / 教案 | 未來辯論場課程介紹、產投班大綱 |
| research | 研究筆記 / 文獻摘要 | NILM 方法比較、期刊調研 |
| brainstorm | 腦力激盪 / 點子 | 企業永續轉型種子、新產品構想 |
| plan | 行動計畫 / 規劃 | 系統架構規劃、專案計畫 |
| report | 工作報告 / 摘要 | 悠識 RAG 系統規劃、會議紀錄 |

---

## Category 分類路徑

對應 notion-sync.py 的 Group 關鍵字分類：

| category | Notion Group | 使用場景 |
|----------|-------------|---------|
| tech/ai-ml | 技術 | AI/ML/LLM 相關技術 |
| tech/devops | 技術 | 部署/運維/自動化 |
| tech/tools | 技術 | 工具使用/開發環境 |
| research | 研究 | 論文/學術研究 |
| business/strategy | 商業 | 商業策略/市場分析 |
| business/sustainability | 商業 | 永續/ESG/碳管理 |
| education/course | 學習 | 課程設計/教學內容 |
| education/workshop | 學習 | 工作坊設計 |
| personal/ideas | 創意 | 靈感/腦力激盪 |
| work-logs | 紀錄 | 工作日誌/進度紀錄 |

---

## 內容結構

Frontmatter 之後的內容結構根據 type 不同而不同：

### analysis（分析報告）

```markdown
## 摘要
一段話說清楚「分析了什麼，結論是什麼」

## 背景
為什麼需要這份分析

## 分析內容
### 面向一
...
### 面向二
...

## 結論與建議
- 建議 1
- 建議 2

## 行動項目
- [ ] 具體下一步行動（可同步到任務排程）
```

### course-design（課程設計）

```markdown
## 一句話定位
這門課解決什麼問題

## 目標學員
誰需要這門課，前置知識

## 課程大綱
### 模組 1：標題（時長）
- 內容重點
### 模組 2：標題（時長）
- 內容重點

## 教學方法
互動方式、實作練習、評量

## 資源需求
教材、工具、場地、人力

## 行動項目
- [ ] 下一步
```

### brainstorm（腦力激盪）

```markdown
## 核心想法
一段話描述想法

## 背景脈絡
什麼觸發了這個想法

## 展開思考
### 可能性 1
...
### 可能性 2
...

## 現實限制
已知的限制和風險

## 行動項目
- [ ] 需要驗證的假設
- [ ] 下一步小實驗
```

---

## 檔案命名

```
YYYY-MM-DD_簡短標題.md
```

- 日期前綴必須有
- 標題用底線 `_` 分隔（不用空格）
- 中英文混合可以
- 範例：`2026-03-30_CC-BOS論文分析.md`

---

## 收集流程

```
Claude dispatch 對話
    ↓ 產出 .md 到 ~/Desktop/
    ↓
collect-dispatch.sh --auto-commit
    ↓ 移到 SecondBrain/dispatch-outputs/
    ↓ git add + commit + push
    ↓
GitHub Actions (notion-sync.yml)
    ↓ 讀 frontmatter → 寫入 Notion
    ↓
Notion SecondBrain Database
    ✅ 自動分類、可搜尋、可關聯專案
```

---

## Claude 產出指令

在 dispatch 對話結束前，加這句話：

> 請將產出存為 .md 檔到 ~/Desktop/，格式依照 ~/SecondBrain/dispatch-outputs/DISPATCH_RULES.md 規範，包含完整 frontmatter。
