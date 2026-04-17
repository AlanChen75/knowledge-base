---
title: "Paper Pipeline 自動化研究助理工作流 vs SecondBrain 對照分析"
date: 2026-04-17
category: knowledge-management
tags: [paper-pipeline, SecondBrain, workflow-comparison, Zotero, Slack, Notion, RSS, automation, token-optimization]
type: analysis
source: 社群分享文（獸醫學研究者）
project: Claw 生態系
priority: P2
status: active
---

## 背景

一位獸醫學研究者分享了他用 Claude Code 打造的自動化論文處理管線（Paper Pipeline），流程從「看到一篇論文」到「整理成適合閱讀的筆記」全自動化。以下是與 SecondBrain 系統的對照分析。

## Paper Pipeline 架構

```
學術期刊 RSS 訂閱 → 每天自動掃描新論文
OR 手動發現有趣論文
       ↓
手機：發到 Slack #paper-triage
OR 電腦：Zotero connector 加到指定資料夾
       ↓
Slack emoji 分流決策
  ✅ 標準整理 → Claude 標準處理
  🔬 深度分析 → Claude 嚴格方法學批判
  🗑️ 不要讀 → 丟棄
  不按 → 7 天後自動丟棄
       ↓
Claude 讀 PDF → 依論文類型選模板 → 產出結構化筆記
       ↓
存到 Notion 三個資料庫：
  - Journal Notes（完整筆記）
  - Knowledge Base（按臨床主題整理）
  - AI Knowledge（AI/ML 論文獨立區）
```

涉及工具：Slack（收件匣）、Zotero（文獻管理）、Claude（讀 PDF、寫筆記）、Notion（知識庫）

## 與 SecondBrain 對照

### Paper Pipeline 做得比較好的地方

**1. 輸入端的零摩擦設計**

他的輸入鏈路是全自動的：RSS 自動掃描 → Slack 推送 → emoji 決策。我目前的輸入還是「看到什麼就丟給 Cowork/Dispatch 處理」，沒有固定收件匣和自動分類機制。

**2. 處理深度分級（emoji 三級分類）**

✅ 標準 / 🔬 深度 / 🗑️ 丟棄 — 不同輸入直接觸發不同深度的處理，省 token 也省注意力。這個概念可以直接對應到 YAML frontmatter 加一個 `depth` 欄位。

**3. 元資料與內容分層**

用 Zotero 管 PDF 和書目元資料，Notion 管筆記和知識庫。SecondBrain 目前是一層打天下，YAML frontmatter 同時扛元資料和內容。

### SecondBrain 做得比較好的地方

**1. 輸出端架構更深**

他到 Notion 就結束了，三個資料庫本質上是分類存放。SecondBrain 有 compile.py 的概念——跨筆記合成 wiki 頁。他的「按臨床主題整理的概念頁」其實就是 compile.py 要做的事，但他看起來是手動維護的。

**2. 知識圖譜能力**

Graphify 計畫讓筆記之間有關聯機制。他的三個 Notion 資料庫之間是孤島式存放，沒有自動關聯。

**3. Token 效率**

SecondBrain 用 YAML frontmatter + 本地 markdown，只在 compile.py 階段才呼叫 LLM，平時存取不需要 token。他每篇論文都過 Claude 才存到 Notion，成本會線性成長。

## 值得借鏡的 3 個設計

### 1. 固定入口 + 快速分級（Slack 收件匣模式）

可以用 Cowork 排程任務每天掃描 RSS / Slack / email，推到一個 triage 頻道讓手機決策。不一定要 Slack，但「固定入口 + 快速分級」這個模式值得採用。

### 2. 處理深度標記

在 YAML frontmatter 加 `depth: standard | deep | skim` 欄位，讓 compile.py 知道每篇要花多少力氣合成。對應到他的 emoji 分流概念。

### 3. PDF → 結構化筆記自動化

他用 Claude 讀 PDF 再按論文類型選模板，這個目前是手動的。可以做成一個 Cowork skill 或排程任務，類似他的流程但存到 dispatch-outputs/ 而不是直接進 Notion。

## 他的痛點：Token 消耗

他問社群有沒有省 token 的方法。SecondBrain 架構天然解決了一部分——本地存取不需要 token，只在合成階段才呼叫 LLM。如果他把 Zotero → Notion 的中間層改成本地 markdown + 批次處理，token 成本可以從「每篇即時」降到「批次合成」。

## 後續待辦

- [ ] 評估在 SecondBrain 加入 `depth` frontmatter 欄位
- [ ] 設計 triage 收件匣機制（Slack channel 或其他方式）
- [ ] 建立 PDF → dispatch-outputs/ 的自動化 skill
- [ ] 把這套分級概念整合進 compile.py 設計

## 交叉連結

- [[2026-04-09_Graphify知識圖譜工具分析與SecondBrain整合評估|Graphify 整合評估]]：知識圖譜能力是 SecondBrain 優於 Paper Pipeline 的關鍵差異
- [[2026-04-10_知識庫搜尋三層機制與領域差異分析|搜尋三層機制]]：BM25/Vector/Graph 的分層跟他的 Notion 三資料庫可以對照
- [[2026-04-09_Graphify-RAG機制與對話知識庫方案深度分析|Graphify RAG 深度分析]]：4 層組合方案中的 Cowork 排程層就是他的 RSS 自動掃描概念
