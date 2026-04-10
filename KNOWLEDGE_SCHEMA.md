---
title: SecondBrain 知識庫統一規格
date: 2026-04-03
_skip_sync: true
---

# SecondBrain 知識庫統一規格

本文件定義所有進入 SecondBrain 的 .md 檔案的統一格式，
不論來源是人工 dispatch、LLM 編譯、或 Telegram Bot 收集。
所有產出都走同一條 notion-sync.py 管線。

---

## 資料流總覽

```
                                     ┌─ dispatch-outputs/  (原始分析、筆記)
來源素材 ─→ raw/YYYY-MM/ ─→ LLM ─→──┤
                                     └─ compiled/          (LLM 編譯的主題頁)

dispatch-outputs/  ──┐
compiled/           ──┼──→ git push → GitHub Actions → notion-sync.py → Notion
work-logs/          ──┘
```

### 三種內容層級

| 層級 | 目錄 | 說明 | 誰寫 |
|------|------|------|------|
| L0 原始素材 | `raw/YYYY-MM/` | Telegram 收集的原始文字、URL、筆記 | Bot 自動 |
| L1 結構化文章 | `dispatch-outputs/` | 有完整 frontmatter 的分析、報告、筆記 | 人 + Claude |
| L2 編譯知識 | `compiled/` | 多篇 L0/L1 融合的主題頁，含交叉引用 | LLM 自動 |

---

## 統一 Frontmatter 規格

所有 L1 和 L2 的 .md 檔案必須包含以下 frontmatter。
notion-sync.py 根據這些欄位建立 Notion page properties。

```yaml
---
# ── 必填 ──
title: "標題（30 字內）"
date: YYYY-MM-DD
category: tech/ai-ml          # 見分類表
tags: [標籤1, 標籤2, 標籤3]   # 最多 10 個
type: analysis                 # 見類型表

# ── 選填（人工 dispatch） ──
source: "來源 URL 或描述"
project: "關聯專案名稱"
priority: P0 | P1 | P2
status: draft | review | final

# ── 選填（LLM 編譯專用） ──
content_layer: L1 | L2         # 預設 L1；compiled/ 下的檔案為 L2
compiled_from:                 # L2 必填：編譯來源
  - dispatch-outputs/2026-03-30_CC-BOS論文分析.md
  - dispatch-outputs/2026-04-01_Claude-Code會計三表案例分析.md
summary: "3-5 句摘要"          # LLM 自動生成
related:                       # LLM 自動生成的關聯文章
  - compiled/ai-agent-patterns.md
  - dispatch-outputs/2026-03-30_MetaClaw框架分析.md
last_compiled: YYYY-MM-DD      # L2 最後編譯日期
---
```

### 欄位說明

| 欄位 | L1 必填 | L2 必填 | 型別 | 說明 |
|------|---------|---------|------|------|
| title | ✅ | ✅ | string | Notion 頁面標題 |
| date | ✅ | ✅ | date | 建立日期 |
| category | ✅ | ✅ | string | 分類路徑，對應 Notion Group |
| tags | ✅ | ✅ | list | 語意標籤，最多 10 個 |
| type | ✅ | ✅ | enum | 文件類型 |
| content_layer | ⬜ | ✅ | enum | L1 原始文章 / L2 編譯知識 |
| compiled_from | ⬜ | ✅ | list | 來源檔案路徑（可追溯性） |
| summary | ⬜ | ✅ | string | LLM 生成的摘要 |
| related | ⬜ | ⬜ | list | 關聯檔案路徑 |
| source | ⬜ | ⬜ | string | 原始來源 URL |
| project | ⬜ | ⬜ | string | 關聯專案 |
| priority | ⬜ | ⬜ | enum | P0/P1/P2 |
| status | ⬜ | ⬜ | enum | draft/review/final |
| last_compiled | ⬜ | ✅ | date | 最後編譯日期 |

---

## Type 類型定義

| type | 適用層級 | 用途 |
|------|---------|------|
| analysis | L1 | 深度分析報告 |
| research | L1 | 研究筆記、文獻摘要 |
| course-design | L1 | 課程設計、教案 |
| brainstorm | L1 | 腦力激盪、點子 |
| plan | L1 | 行動計畫、規劃 |
| report | L1 | 工作報告、摘要 |
| note | L1 | 一般筆記 |
| wiki | L2 | LLM 編譯的主題百科頁 |
| index | L2 | LLM 維護的索引頁 |
| comparison | L2 | 多篇文章的觀點比較 |

---

## Category 分類路徑

與 notion-sync.py 的 `_GROUP_KEYWORDS` 對應：

| category | Notion Group | 使用場景 |
|----------|-------------|---------|
| tech/ai-ml | 技術 | AI/ML/LLM 相關 |
| tech/devops | 技術 | 部署/運維/自動化 |
| tech/tools | 技術 | 工具使用/開發環境 |
| tech/agent | 技術 | AI Agent 設計與框架 |
| research | 研究 | 論文/學術研究 |
| business/strategy | 商業 | 商業策略/市場分析 |
| business/sustainability | 商業 | 永續/ESG/碳管理 |
| education/course | 學習 | 課程設計/教學內容 |
| education/workshop | 學習 | 工作坊設計 |
| personal/ideas | 創意 | 靈感/腦力激盪 |
| work-logs | 紀錄 | 工作日誌/進度紀錄 |

---

## 檔案命名

### L1（dispatch-outputs/）

```
YYYY-MM-DD_簡短標題.md
```
範例：`2026-04-03_Claude-Token-Efficient-CLAUDE-md.md`

### L2（compiled/）

```
主題名稱.md          ← 主題頁，用 kebab-case
_index.md            ← 該目錄的總索引
```
範例：
```
compiled/
├── _index.md                      ← LLM 維護的總索引
├── ai-agent-design-patterns.md    ← 主題頁：AI Agent 設計模式
├── llm-knowledge-management.md    ← 主題頁：LLM 知識管理
├── interior-design-automation.md  ← 主題頁：室內設計自動化
└── claude-code-ecosystem.md       ← 主題頁：Claude Code 生態系
```

L2 不用日期前綴，因為它是持續更新的活文件，用 `last_compiled` 追蹤版本。

---

## L2 編譯頁的內容結構

```markdown
---
title: "AI Agent 設計模式"
date: 2026-04-03
category: tech/agent
tags: [AI-agent, design-pattern, multi-agent, tool-use]
type: wiki
content_layer: L2
compiled_from:
  - dispatch-outputs/2026-03-30_MetaClaw框架分析.md
  - dispatch-outputs/2026-04-03_DesignClaw室內裝修自動化系統計畫.md
  - dispatch-outputs/2026-03-30_悠識RAG系統規劃.md
summary: "整理 SecondBrain 中所有 AI Agent 相關文章的核心模式..."
related:
  - compiled/claude-code-ecosystem.md
  - compiled/llm-knowledge-management.md
last_compiled: 2026-04-03
---

## 概述
（LLM 從多篇來源文章融合的主題總覽）

## 核心模式
### 模式一：多代理管線
（引用來源：→ MetaClaw框架分析、DesignClaw計畫）
...

### 模式二：工具使用
...

## 開放問題
（跨文章比較後發現的未解問題）

## 來源索引
| 來源文章 | 貢獻段落 | 日期 |
|----------|---------|------|
| MetaClaw框架分析 | 核心模式一、二 | 2026-03-30 |
| DesignClaw計畫 | 核心模式一 | 2026-04-03 |
```

---

## notion-sync.py 需要的擴充

讓 compiled/ 也能被同步，需在 notion-sync.py 加：

1. **掃描範圍**：加入 `compiled/` 目錄
2. **Group 分類**：`compiled/` 下的檔案根據 category 分類，不硬編為「創意」
3. **新 Properties**：
   - `ContentLayer`：select，L1 或 L2
   - `CompiledFrom`：rich_text，來源列表
   - `Summary`：rich_text，摘要
   - `Related`：rich_text，關聯文章
   - `LastCompiled`：date，最後編譯日期

---

## LLM 編譯指令（enrich.py / compile.py）

### enrich.py — L1 metadata 增強

對 dispatch-outputs/ 中缺少 `summary` 和 `related` 的檔案：
1. 讀取檔案內容
2. 用 LLM 生成 summary（3-5 句）
3. 比對現有所有 L1 檔案，生成 related 列表
4. 回寫到 frontmatter（不動內容本體）

### compile.py — L2 知識編譯

1. 讀取指定主題相關的所有 L1 檔案（by tags/category）
2. 用 LLM 編譯成結構化主題頁
3. 輸出到 compiled/主題名稱.md
4. 自動填寫 compiled_from、last_compiled
5. 更新 compiled/_index.md

---

## 整合到現有工作流

```
# 日常（不變）
Claude dispatch → .md 到 dispatch-outputs/ → collect-dispatch.sh → Notion

# 新增：定期 LLM 增強
enrich.py --dir dispatch-outputs/    # 自動補 summary + related

# 新增：定期 LLM 編譯
compile.py --topic "ai-agent"        # 編譯主題頁到 compiled/
compile.py --all                     # 重新編譯所有主題

# 同步（擴充後）
notion-sync.py                       # 同時同步 dispatch-outputs/ + compiled/
```

---

## 設計原則

1. **向下相容**：現有 dispatch-outputs/ 的檔案不需任何修改，新欄位都是選填
2. **可追溯**：L2 的每段內容都能追回 L1 來源（compiled_from + 內文標註）
3. **LLM 可操作**：所有格式都是純 .md + YAML，LLM 直接 read/write
4. **單一管線**：不論 L1 或 L2，都走 notion-sync.py 進 Notion
5. **漸進式**：可以先只跑 enrich.py（零架構改動），再慢慢加 compile.py
