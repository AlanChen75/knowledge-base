---
title: "Graphify RAG 機制與對話知識庫方案深度分析"
date: 2026-04-09
category: tech/tools
tags: [Graphify, RAG, knowledge-graph, Obsidian, Karpathy, SecondBrain, Khoj, Smart-Connections, compile, enrich]
type: analysis
project: SecondBrain
priority: high
status: active
---

## 你問的七個問題，逐一回答

---

## 1. Graphify 如何建立 RAG DB？

**Graphify 完全不用 Vector DB。** 它用的是 Graph-based Retrieval，而非傳統的 Vector-based RAG。

底層機制：

```
你的檔案 → LLM 語意提取 → entities + relationships
                ↓
         NetworkX 知識圖譜（節點 = 概念，邊 = 關聯）
                ↓
         Leiden 社群偵測（自動分群）
                ↓
         查詢時沿圖譜路徑導航（不是向量相似度搜尋）
```

| 維度 | 傳統 RAG | Graphify |
|------|---------|----------|
| 儲存 | Vector DB（Pinecone/Chroma/Weaviate） | NetworkX 圖（JSON/pickle） |
| 索引 | Embedding 向量 | Entity + Relationship 節點 |
| 查詢 | 向量餘弦相似度 | 圖譜路徑導航 |
| 優點 | 對自然語言開放式問答好 | 結構清晰、Token 省、關聯精準 |
| 缺點 | Token 消耗大、需調校 | 不擅開放式對話 |

**結論**：Graphify 的「RAG」是一種不同典範。它不是讓你跟筆記「聊天」的工具，而是建立一個可導航的知識結構。

---

## 2. 如何收集資訊來源？

Graphify 支援的輸入：

- 本地檔案夾（你的 SecondBrain/）
- 20+ 種程式語言原始碼
- PDF、圖片、截圖（多模態）
- **但沒有自動收集管線**

你得手動指向一個資料夾，然後 `graphify build`。它不會自動去抓 Telegram、RSS、網頁。

**對你的意義**：你的 L0 收集管線（Telegram bot → raw/）已經比 Graphify 內建的強。Graphify 只是個處理器，不是收集器。

---

## 3. 只是視覺工具就有點可惜？

**不只是視覺工具，但也沒你想像的那麼全能。**

Graphify 能做的：

| 功能 | 說明 |
|------|------|
| 互動式圖譜 | 3D/2D 可縮放、可點擊節點 |
| `/graphify query` | CLI 查詢，沿圖譜找答案 |
| 路徑追蹤 | 顯示概念 A 到概念 B 的連結路徑 |
| 節點解釋 | 解釋某個 entity 在圖譜中的位置和關聯 |
| MCP Server | 暴露查詢 API，可被其他工具呼叫 |
| Obsidian Vault 輸出 | 產出帶 backlinks 的 Markdown 筆記庫 |

Graphify 不能做的：

- ❌ 開放式自然語言對話（「關於 DesignClaw 你覺得還有什麼風險？」）
- ❌ 主動分析和建議
- ❌ 自動收集新資訊
- ❌ 跨知識庫推理

---

## 4. 筆記建立在 Obsidian？

Graphify 和 Obsidian 的關係是**單向輸出**：

```
Graphify build → 產出 Obsidian Vault（帶 Wiki Links + backlinks）
```

Graphify 本身不住在 Obsidian 裡。它是獨立的 CLI 工具，可以產出 Obsidian 格式的筆記，但也可以不用 Obsidian。

**對你來說**：你的 SecondBrain 已經在用 Obsidian Wiki Links 格式（`[[note-name]]`），Graphify 輸出的格式跟你相容。但你不需要 Graphify 來產出 Wiki Links——你的 build-knowledge-map.py 已經在做這件事。

---

## 5. RAG DB 也是利用 Obsidian？

**Obsidian 本身不是 RAG DB。** 但有插件可以在 Obsidian 上加 RAG 層：

| 工具 | 運作方式 | 價格 |
|------|---------|------|
| **Obsidian Copilot** | 在 Obsidian 側邊欄加 chat，用 local embedding 建 vector index | 免費（自帶 API key） |
| **Smart Connections** | 自動計算筆記間的語意相似度，推薦相關筆記 | 免費 |
| **Khoj** | 獨立服務，多端存取，排程自動化，對話式 | 免費自架 / 付費雲端 |

**最接近你要的「對話知識庫」的方案**：

```
你的 SecondBrain Markdown 筆記
        ↓
Obsidian Copilot（建立 local vector index）
        ↓
在 Obsidian 側邊欄直接問：
  「DesignClaw 的商業模式有哪些風險？」
  「MEDVi 和 DesignClaw 有什麼共同點？」
        ↓
Copilot 搜尋你的筆記，引用來源回答
```

---

## 6. AI 主動分析與提建議？

這是最前沿的需求，**目前沒有成熟的開源工具能做到。**

最接近的方案：

### 方案 A：Khoj 排程自動化
```
Khoj 設定：每週一早上 9 點
→ 掃描上週新增筆記
→ 產出「本週知識摘要」
→ 推送到 Telegram/Email
```
缺點：不是真的「主動分析」，而是定時摘要。

### 方案 B：你自建 enrich.py + cron
```python
# enrich.py（建議實作）
async def proactive_analysis(notes_dir):
    recent = get_notes_since(days=7)
    
    prompt = f"""
    以下是最近 7 天的新筆記：
    {format_notes(recent)}
    
    請分析：
    1. 這些筆記之間有什麼隱藏的關聯？
    2. 有什麼知識缺口需要補充？
    3. 基於這些新知識，對我的專案（DesignClaw、gemgate、OpenClaw）有什麼新啟發？
    4. 有沒有矛盾的觀點需要釐清？
    """
    
    response = await llm.complete(prompt)
    save_to(f"compiled/weekly-insight-{date}.md", response)
```
優點：完全客製化，結合你的專案上下文。

### 方案 C：Claude 排程任務（Cowork）

你現在就在 Cowork 裡，可以設定排程任務讓我每週自動掃描 SecondBrain 並產出 insight：

```
每週一 09:00 → 掃描 SecondBrain 新筆記
→ 分析跨主題關聯
→ 產出 weekly-insight.md
→ 推送通知
```

---

## 7. 透過 AI 對話知識庫要如何做？

### 推薦方案：分層組合

```
┌──────────────────────────────────────────────┐
│          你的「對話知識庫」完整架構            │
│                                              │
│  Layer 1: Obsidian Copilot（立即可用）        │
│  → 在 Obsidian 裡直接問你的筆記              │
│  → Local embedding，隱私安全                 │
│  → 最適合快速查找「我之前寫過什麼」           │
│                                              │
│  Layer 2: Graphify 知識圖譜（結構化導航）     │
│  → 視覺化概念關聯                            │
│  → 適合探索「這些概念之間有什麼連結」         │
│  → MCP server 可被 gemgate 呼叫              │
│                                              │
│  Layer 3: compile.py + enrich.py（深度編譯）  │
│  → L2 compiled 主題頁 = LLM 編譯的 Wiki      │
│  → 比 RAG 搜尋更完整、更有結構               │
│  → Karpathy 模式的完整實現                   │
│                                              │
│  Layer 4: Cowork 排程（主動分析）             │
│  → 每週自動掃描 + insight 產出               │
│  → 知識缺口偵測                              │
│  → 跨專案關聯發現                            │
└──────────────────────────────────────────────┘
```

---

## 你的三層架構 vs Karpathy 的 LLM Wiki

```
Karpathy:  raw content → LLM compile → wiki pages → query
你的:      L0 raw/     → L1 outputs  → L2 compiled → ???
```

你已經走到 90% 了。差的就是：

1. **compile.py**（L1 → L2 的 LLM 編譯）— 把同主題的 dispatch-outputs 編譯成完整的主題 wiki 頁
2. **enrich.py**（L1 自動摘要 + related links）— 每篇筆記自動補上 summary 和相關連結
3. **查詢層**（query interface）— Obsidian Copilot 或 Graphify MCP 或自建 API

Graphify 可以加速第 1、3 點，但不能取代你已有的 YAML frontmatter + build-knowledge-map.py 體系。

---

## 具體行動建議

### 今天就做（5 分鐘）
- 在 Obsidian 安裝 Copilot 插件 → 立刻能對話你的筆記

### 本週做
- 對 dispatch-outputs/ 的 30 篇跑 Graphify → 評估自動分群品質 vs 你的 10 個手動主題

### 下週做
- 實作 compile.py 第一版 → 先挑「AI Agent」主題，把 51 篇 outputs 編譯成一篇完整 wiki

### 月底前
- 設定 Cowork 排程任務 → 每週一自動掃描 + insight
- 評估是否需要 Khoj 自架

---

## Sources

- [Graphify README](https://github.com/safishamsi/graphify)
- [Karpathy LLM Wiki 概念](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Obsidian Copilot](https://www.obsidiancopilot.com/en)
- [Smart Connections](https://github.com/brianpetro/obsidian-smart-connections)
- [Khoj AI](https://github.com/khoj-ai/khoj)
- [Microsoft GraphRAG](https://github.com/microsoft/graphrag)
