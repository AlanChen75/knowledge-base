# Knowledge Base System
# 個人知識庫管理系統

## 系統目的 Purpose

透過 Telegram Bot 收集各種資訊（文章、連結、PDF、圖片、影片筆記等），
自動分析、分類並建立可搜尋的個人知識庫。

## 目錄結構 Directory Structure

```
~/knowledge-base/
├── inbox/              # 待處理暫存區（Bot 初次存放）
├── tech/               # 技術類
│   ├── programming/    # 程式開發
│   ├── ai-ml/         # AI/機器學習
│   ├── devops/        # DevOps/運維
│   └── tools/         # 工具使用
├── business/           # 商業類
│   ├── strategy/      # 策略規劃
│   ├── marketing/     # 行銷
│   └── finance/       # 財務
├── research/           # 研究/論文
├── news/               # 新聞時事
├── personal/           # 個人筆記
├── resources/          # 原始資源檔案
│   ├── pdf/           # PDF 檔案
│   ├── images/        # 圖片
│   └── videos/        # 影片截圖/筆記
└── _index/             # 索引檔（供 RAG 搜尋）
```

## 檔案命名規則 Naming Convention

**Markdown 筆記：**
```
YYYY-MM-DD-簡短標題.md
```

範例：
- `2026-01-25-claude-code-使用技巧.md`
- `2026-01-25-openai-gpt5-發布新聞.md`

**資源檔案：**
```
YYYY-MM-DD-描述.ext
```

範例：
- `2026-01-25-ai-架構圖.png`
- `2026-01-25-論文-attention-is-all-you-need.pdf`

## Markdown 筆記格式 Note Format

```markdown
---
title: 標題
date: YYYY-MM-DD
source: 來源網址或描述
category: 分類路徑 (e.g., tech/ai-ml)
tags: [標籤1, 標籤2, 標籤3]
type: article | news | paper | video | image | note
---

# 標題

## 摘要
簡短摘要或重點整理

## 內容
詳細內容或筆記

## 關鍵要點
- 要點 1
- 要點 2
- 要點 3

## 相關連結
- [連結描述](URL)

## 個人筆記
自己的想法或補充
```

## 使用方式 How to Use

### 透過 Telegram Bot

1. **新增知識**：直接發送文字、連結、圖片、PDF 給 Bot
2. **查詢知識**：發送「搜尋 關鍵字」
3. **瀏覽分類**：發送「列出 tech/ai-ml」

### 支援的輸入類型

| 類型 | 處理方式 |
|------|---------|
| 文字 | 直接分析並建立筆記 |
| URL 連結 | 抓取內容並摘要 |
| YouTube | 提取影片資訊和重點 |
| PDF | 提取文字並建立摘要 |
| 圖片 | 分析內容並建立描述 |
| 簡報 | 提取重點並建立筆記 |

## 分類規則 Classification Rules

### 自動分類關鍵字

| 分類 | 關鍵字/Pattern |
|------|---------------|
| tech/programming | code, 程式, python, javascript, api, 開發 |
| tech/ai-ml | AI, ML, 機器學習, GPT, LLM, 神經網路 |
| tech/devops | docker, k8s, CI/CD, 部署, 運維 |
| tech/tools | 工具, 軟體, app, 效率 |
| business/strategy | 策略, 商業模式, 市場 |
| business/marketing | 行銷, 廣告, SEO, 品牌 |
| business/finance | 財務, 投資, 股票, 加密貨幣 |
| research | 論文, paper, 研究, arxiv |
| news | 新聞, 發布, 公告, 宣布 |
| personal | 筆記, 想法, 心得 |

### 手動分類

發送時可指定分類：
```
#tech/ai-ml 這是一篇關於 GPT-5 的文章...
```

## 索引系統 Index System

`_index/` 目錄包含：

- `master-index.json` - 所有筆記的元資料索引
- `tags-index.json` - 標籤索引
- `full-text-index/` - 全文搜尋索引

### 索引格式

```json
{
  "lastUpdated": "2026-01-25T10:00:00Z",
  "totalNotes": 100,
  "notes": [
    {
      "id": "uuid",
      "title": "標題",
      "path": "tech/ai-ml/2026-01-25-xxx.md",
      "date": "2026-01-25",
      "category": "tech/ai-ml",
      "tags": ["AI", "GPT"],
      "summary": "摘要...",
      "keywords": ["關鍵字1", "關鍵字2"]
    }
  ]
}
```

## 與 Claude 對話系統整合

本知識庫與 `~/.claude/` 對話系統互補：

| 系統 | 用途 |
|------|------|
| `~/.claude/` | AI 對話記錄、協作索引 |
| `~/knowledge-base/` | 外部知識收集、個人筆記 |

**整合方式：**
- Claude AI 可同時存取兩個系統
- 查詢時會同時搜尋對話記錄和知識庫
- 知識庫的變更會記錄到對話系統中

## 維護指令

```bash
# 重建索引
km-reindex

# 搜尋知識庫
km-search "關鍵字"

# 列出最近新增
km-recent 10

# 統計資訊
km-stats

# 備份知識庫
km-backup
```

## 最佳實踐

1. **及時整理** - 收到資料後盡快分類
2. **標籤一致** - 使用統一的標籤命名
3. **定期回顧** - 每週瀏覽 inbox，確保都已分類
4. **關聯連結** - 在筆記中互相連結相關內容
5. **定期備份** - 每週備份一次知識庫

---

建立日期：2026-01-25
最後更新：2026-01-25
