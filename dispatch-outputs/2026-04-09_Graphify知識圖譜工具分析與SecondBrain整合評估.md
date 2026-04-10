---
title: "Graphify 知識圖譜工具分析與 SecondBrain 整合評估"
date: 2026-04-09
category: tech/tools
tags: [Graphify, knowledge-graph, Karpathy, knowledge-compilation, SecondBrain, Obsidian, RAG, Leiden]
type: analysis
source: "https://github.com/safishamsi/graphify"
project: SecondBrain
priority: high
status: active
---

## Graphify 是什麼？

Graphify 是受 Andrej Karpathy「知識編譯」工作流啟發的開源工具，三天內在 GitHub 狂掃 15,000+ Stars。核心理念：與其用 RAG 搜尋，不如讓 LLM 把資料夾「編譯」成結構化知識圖譜。

### 核心架構

1. **語意提取**：用 LLM 掃描每個檔案，提取 entities（概念、人名、術語）和 relationships
2. **圖譜建構**：用 NetworkX 建構知識圖譜，節點 = 概念，邊 = 關聯
3. **社群偵測**：用 Leiden 演算法自動發現主題群集（communities）
4. **查詢導航**：查詢時不讀所有檔案，而是沿圖譜導航到精確節點

### 宣稱特點

| 特點 | 說明 |
|------|------|
| Token 消耗降 71.5 倍 | 圖譜導航取代全文讀取 |
| 不需 Vector DB | 不用調校 Embedding 或維護向量庫 |
| 全模態 | 20 種程式語言 + PDF + 圖片 + 截圖 |
| 自動 Backlinks | 生成帶反向連結的筆記庫 |
| Obsidian 輸出 | 可直接產出 Obsidian Vault |

---

## 與 SecondBrain 現有系統的比較

| 維度 | SecondBrain 現行 | Graphify |
|------|-----------------|----------|
| **分類方式** | 規則比對（tags/category/title_keywords） | LLM 語意提取 + Leiden 社群偵測 |
| **知識連結** | 手動 + build-knowledge-map.py 的主題歸類 | 自動發現 entity 關聯 + backlinks |
| **編譯** | 計畫中（compile.py 尚未建構） | 內建知識編譯 |
| **摘要** | 計畫中（enrich.py 尚未建構） | LLM 提取時順便產生 |
| **查詢** | 無（靠 Notion 搜尋或 Obsidian） | 圖譜導航 |
| **視覺化** | 無 | 互動式圖譜 |
| **成本** | 低（規則比對免費） | 高（每個檔案都走 LLM API） |
| **成熟度** | 自建、穩定 | 3 天大，API 快速變動 |

---

## Graphify 最大價值：取代 enrich.py + compile.py

你的 SecondBrain 有兩個尚未建構但已規劃的元件：

1. **enrich.py**：自動生成 summary + related links → Graphify 的語意提取天然做這件事
2. **compile.py**：跨筆記主題編譯成 wiki 頁 → Graphify 的 Leiden 社群偵測 + 知識編譯就是這個

如果 Graphify 成熟度足夠，它可以直接取代這兩個計畫中的工具。

---

## 具體整合方案

### 方案 A：Graphify 作為獨立視覺化層（低風險）

```
現有管線不動：
raw/ → dispatch-outputs/ → build-knowledge-map.py → compiled/

新增：
dispatch-outputs/ → Graphify → 互動式圖譜 + Obsidian Vault
```

- 不改現有 YAML frontmatter 流程
- Graphify 只做額外的圖譜視覺化和關聯發現
- 把 Graphify 發現的 related links 回寫到 frontmatter

### 方案 B：Graphify 取代 compile.py（中風險）

```
raw/ → dispatch-outputs/ → enrich.py（簡化版，只補 summary）
                         → Graphify → compiled/ 主題頁
                         → notion-sync.py → Notion
```

- 讓 Graphify 的 Leiden 社群偵測取代手動的 10 個主題定義
- 自動發現的主題可能比手動定義更精準
- 需要寫轉換層把 Graphify 輸出轉成 KNOWLEDGE_SCHEMA.md 格式

### 方案 C：全面採用 Graphify（高風險，不建議現階段）

- 用 Graphify 取代整個 L2 編譯流程
- 風險：專案太新、API 不穩、深度綁定後難以退回

---

## 建議行動：方案 A 先行

### Step 1：小規模試跑
```bash
# 只對 dispatch-outputs/ 的最近 30 篇試跑
graphify build --input SecondBrain/dispatch-outputs/ --output test-graph/
```

### Step 2：評估結果
- Graphify 的自動分群結果 vs 你的 10 個手動主題，哪個更合理？
- 自動發現的 related links 品質如何？
- LLM API 成本是多少？（258 篇 × 每篇語意提取的 token 數）

### Step 3：決定整合深度
- 如果效果好 → 進入方案 B，讓它取代 compile.py
- 如果效果普通 → 只留作視覺化工具，繼續自建 compile.py

---

## 風險與限制

1. **成熟度**：三天大的專案，breaking changes 隨時可能發生
2. **成本**：258 篇 Markdown 全走 LLM 語意提取，每次 rebuild 都有 API 費用
3. **中文支援**：你的筆記大量使用繁體中文，LLM 提取的 entity 品質需實測
4. **規模**：官方自己說「幾百份文件規模的小型團隊」最適合——你的 258 篇剛好在這個甜蜜點
5. **與現有管線的相容性**：Graphify 輸出格式不一定符合 KNOWLEDGE_SCHEMA.md，需要轉換層

---

## 與 Karpathy 知識編譯理念的對照

Karpathy 的核心觀點：「大半的 Token 都花在編譯知識，而非寫 Code。」

這跟你前天記錄的 Anthropic Growth 六步驟第六點完全呼應：「真正的分水嶺：AI 有沒有接進你的系統。」Graphify 本質上就是把 AI 接進知識管理系統的一個具體實現。

你的 SecondBrain 已經走在這條路上（L0→L1→L2 三層架構、build-knowledge-map.py、Git SHA 追蹤），Graphify 可以加速 L2 層的建設，但不應該取代你已經穩定的 L0→L1 管線。

---

## Sources

- [safishamsi/graphify](https://github.com/safishamsi/graphify)
- Andrej Karpathy 知識編譯工作流
- SecondBrain KNOWLEDGE_SCHEMA.md
