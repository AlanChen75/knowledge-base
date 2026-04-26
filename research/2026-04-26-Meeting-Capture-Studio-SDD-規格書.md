---
title: "Meeting Capture Studio SDD 規格書"
date: 2026-04-26
category: research
tags: [sdd, openspec, meeting-capture, chrome-extension, cloudflare-workers, workers-ai, gemini, rag, self-learning, terminology-extraction, 課程教材, ai-四級課程, ai-智慧製造, mvp-基礎設施]
type: research
source: "個人會議工作流需求 + AI 四級課程進階模組教案規劃"
---

# Meeting Capture Studio — SDD 規格書

> **可作為課程教材引用**
> 適用課程：AI 四級課程（進階模組）、AI 智慧製造三級課程、AI 永續兩級課程
> 教學定位：6-8 小時課程，學員 fork 後完成自己的 MVP 版本
> 教學主軸：Chrome Extension + RAG + LLM Provider 抽象層 + 自學習迴路 + 個人化 AI 工作流

## 📌 核心決策快照

| 主題 | 決策 |
|---|---|
| 入口 | Chrome Extension 抓 Google Meet 字幕（MVP）；架構預留實體會議入口（v2） |
| 校正架構 | 四層信心分層（L0 觀察 / L1 候選 / L2 正式 / L3 核心），自動晉升降級 |
| 術語抽取 | LLM（Workers AI）為主 + TF-IDF/jieba（JS）為輔 |
| 術語表存放 | D1 為主 + Notion + GitHub 雙鏡像 |
| 抽取觸發 | 每天定時批次（自動）+ 手動觸發（並存） |
| LLM 策略 | 校正用 Workers AI、摘要用 Gemini Flash（預設）、可切 Groq/OpenAI |
| Notion 整合 | 雙向（讀脈絡 + 寫紀錄 + 鏡像術語表） |
| 教學版 | 與個人版同一份程式碼，學員 fork 即用 |
| 月成本 | $0（Workers AI + Gemini Flash 免費額度內） |

---

# 1. Proposal（提案）

## 名稱
`meeting-capture-studio`

## 為什麼做（Why）

每月開十場以上的會議——學術研討、企業培訓、政府客戶簡報、論文討論——產生的口頭資訊量遠大於任何書面紀錄。但既有市售工具有四個明確痛點：

1. **使用量被閹割**：Tactiq 免費版每月僅 10 場會議，剛好不夠用，付費門檻又是另一筆綁約。
2. **校正品質差**：Google Meet 即時字幕對台灣用語、專業術語、人名（如 HTF-CNN、NILM、智慧製造、永續、特定客戶名）辨識率低，產出的逐字稿錯字到看了會痛。
3. **RAG 校正缺位**：現有工具不知道使用者的「專案脈絡」——它們無法讀 Notion 專案頁、無法讀 SecondBrain 知識庫，因此無法針對性修正關鍵字。
4. **資料主權問題**：政府客戶、企業培訓涉及機密內容，不能丟到第三方雲端。

更深的動機是**教學**。AI 四級課程學員問「能不能教我們做自己的會議工具」——直接照抄 Tactiq 教不出價值，必須建立**「擁有資料主權 + 個人化校正 + 自學習迴路 + 多 provider 抽象層」**的版本，才能讓學員學到真正的架構素養。

## 做什麼（What Changes）

建立一個由五部分組成的個人會議基礎設施：

1. **Chrome Extension**：在 Google Meet 頁面內注入 content script，用 MutationObserver 監聽字幕 DOM，將字幕片段帶 timestamp 推送到後端。會議開始時可選擇關聯的 Notion 專案頁（提供 RAG 脈絡）。

2. **Cloudflare Workers 後端**：接收字幕串流、暫存於 KV、會議結束後觸發後處理 Workflow（背景非同步，避免主 request 撞 CPU 限制）。

3. **四層信心分層校正引擎**：
   - **L3 核心層**（confidence ≥ 0.95）：硬替換、純 string replace、零成本
   - **L2 正式層**（0.7-0.95）：jieba 分詞 + 模糊比對
   - **L1 候選層**（0.3-0.7）：包進 LLM prompt、弱權重
   - **L0 觀察層**（< 0.3）：候選詞，不參與校正
   - 每個術語自動晉升/降級，使用者手動修正過的詞強制升 L3

4. **自學習迴路**（每日批次 + 手動觸發）：
   - 收集當天所有會議的 corrected_caption
   - LLM 抽取候選術語 + TF-IDF 補強
   - 多訊號評分：LLM 信心、出現頻率、跨會議分布、Notion 共現、使用者修正
   - 自動分配信心層級

5. **多目的地分發 + LLM Provider 抽象層**：
   - 分發：GitHub（複用 SecondBrain MCP）+ Notion API（雙向）+ Email（Resend）
   - LLM Provider：Workers AI 校正 + Gemini Flash 摘要（預設）；Groq、OpenAI 可切換

## 範圍（Scope）

### MVP 包含（Phase 1 簡化版）
- Chrome Extension（Manifest V3）抓 Google Meet 字幕
- Cloudflare Workers 接收 + 暫存 + 觸發處理
- L3 核心層 + L2 正式層校正（手動維護的種子術語表）
- Workers AI 字幕校正
- Gemini Flash 摘要 + Action Items
- 三條分發路徑：GitHub + Notion + Email
- 內建常用術語表（智慧製造、NILM、永續、ESG、AI/ML、學術寫作六領域種子資料）

### Phase 2 加入
- L1 候選層 + L0 動態 RAG（讀 Notion + GitHub 知識庫脈絡）
- 自學習迴路（每日批次抽取、信心分層、自動晉升降級）
- Notion 雙向同步、術語表 D1 ↔ Notion ↔ GitHub 三向鏡像
- 使用者修正捕捉與訓練回饋

### MVP 不包含（明確排除）
- 視訊會議 bot（headless browser 加入 Meet）—— ToS 灰區、維護成本高
- 完整使用者註冊系統 —— 個人 + 學員自架
- 即時逐字稿顯示 —— 批次處理已足夠
- 手機端錄音入口 —— v2，但架構預留
- 實體會議錄音上傳 —— v2
- iOS/Android 原生 App —— Chrome Extension 已涵蓋桌機需求
- Speaker diarization —— v2
- 跨會議搜尋與分析 —— v2
- KeyBERT / YAKE 進階抽取 —— 需獨立 Python service，v2 才考慮

## 成功指標

| 類別 | 指標 | 目標 |
|---|---|---|
| **效能** | 端到端處理時間 | 會議結束 → 知識庫 ≤ 5 分鐘 |
| **校正** | L3 核心層準確率 | ≥ 99% |
| **校正** | L2 正式層準確率 | ≥ 95% |
| **校正** | L1 候選層準確率 | ≥ 90% |
| **校正** | 整體校正準確度 | ≥ 95% |
| **學習** | 啟動時間 | 第 5-10 場會議後候選層 ≥ 50 條 |
| **學習** | 自動晉升準確度 | 進入正式層後修正率 < 10% |
| **學習** | 人工介入頻率 | 每月手動修正 < 1 次 |
| **成本** | 個人月費 | $0（Workers AI + Gemini Flash 免費額度內） |
| **成本** | 學員自架月費 | $0 |
| **教學** | 學員完成率 | 6-8 小時課程內完成 MVP fork |
| **可維護** | 6 個月後可用性 | Google Meet DOM 變動 ≤ 一行 selector 修復 |

---

# 2. Design（系統設計）

## 2.1 架構概覽

```
┌─────────────────────────────────────────────────────────────────────┐
│  使用者端                                                              │
│  ┌──────────────────────────┐      ┌───────────────────────────┐  │
│  │ Chrome Extension          │      │ Notion（工作介面）          │  │
│  │  - content.js（抓字幕）    │      │  - 專案頁（脈絡來源）        │  │
│  │  - background.js（推送）   │      │  - 術語表頁（鏡像 + 微調）   │  │
│  │  - popup.html（設定）      │      │  - 會議紀錄頁（寫入目的地）   │  │
│  └──────────────┬───────────┘      └─────────────┬─────────────┘  │
└─────────────────┼─────────────────────────────────┼────────────────┘
                  │ HTTPS                            │ Notion API
                  ▼                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│  Cloudflare Workers 後端（Hono.js + Workflows）                       │
│                                                                       │
│  API 層                                                              │
│   POST /sessions/start       建立會議 session                         │
│   POST /sessions/:id/caption 接收字幕片段                              │
│   POST /sessions/:id/end     結束會議，觸發 Workflow                   │
│   GET  /sessions/:id/result  取得處理結果                              │
│   POST /terms/extract        手動觸發術語抽取                          │
│   GET  /terms                取得當前術語表                            │
│   POST /corrections          記錄使用者修正                             │
│                                                                       │
│  儲存                                                                 │
│   D1 (SQL)：terms, sessions, corrections, observations, candidates    │
│   KV：字幕片段暫存（TTL 7 天）                                          │
│   Workflows：背景處理 + 每日批次抽取                                    │
│                                                                       │
│  處理 Pipeline                                                        │
│   1. 字幕收集 → KV 暫存                                                │
│   2. 會議結束 → Workflow 啟動                                          │
│   3. 拉 Notion 脈絡 + GitHub 知識庫（v2）                              │
│   4. 四層校正引擎                                                      │
│   5. 摘要 + Action Items                                              │
│   6. 分發到 GitHub / Notion / Email                                    │
│   7. 紀錄候選詞（等每日批次抽取）                                        │
│                                                                       │
│  LLM Provider 抽象層                                                  │
│   llm({ task, provider, messages, options })                          │
│    ├─ workers-ai     原生 binding                                    │
│    ├─ gemini         OpenAI-compat                                    │
│    ├─ groq           OpenAI-compat                                    │
│    └─ openai         OpenAI 規格                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## 2.2 技術選型

| 層 | 選擇 | 理由 |
|---|---|---|
| Chrome Extension | Manifest V3 + Vanilla JS + Tailwind | 無框架負擔、學員學習曲線低 |
| 後端框架 | Cloudflare Workers + Hono.js | 已熟悉、免費額度足、Hono 路由清晰 |
| 資料庫 | Cloudflare D1 (SQLite) | 原生整合、零部署、SQL 對學員親切 |
| 暫存 | Cloudflare KV | 字幕片段暫存、7 天 TTL |
| 排程 | Workflows + Cron Triggers | 每日抽取、避開主 request CPU 限制 |
| 校正 LLM | Workers AI（Llama 3.3 70B） | 同生態、免費、品質夠用 |
| 摘要 LLM | Gemini 2.5 Flash | 中文佳、免費額度寬、OpenAI-compat |
| TF-IDF | 純 TS + jieba-js | Workers 內可跑、零外部依賴 |
| 分發 | SecondBrain MCP（GitHub）+ Notion API + Resend | 複用既有基礎設施 |

## 2.3 資料模型（D1 Schema）

```sql
-- 會議 session
CREATE TABLE sessions (
  id TEXT PRIMARY KEY,
  started_at INTEGER NOT NULL,
  ended_at INTEGER,
  meet_url TEXT,
  notion_project_id TEXT,
  status TEXT NOT NULL,          -- recording | processing | completed | failed
  raw_caption TEXT,
  corrected_caption TEXT,
  summary_md TEXT,
  action_items_json TEXT,
  github_url TEXT,
  notion_page_id TEXT,
  created_at INTEGER NOT NULL
);

-- 術語表（核心）
CREATE TABLE terms (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  surface TEXT NOT NULL,
  category TEXT,                 -- person | project | company | tech | acronym | other
  domain TEXT,
  confidence REAL NOT NULL,
  layer TEXT NOT NULL,           -- L0_observe | L1_candidate | L2_official | L3_core
  occurrences INTEGER DEFAULT 0,
  sessions_seen INTEGER DEFAULT 0,
  user_corrections INTEGER DEFAULT 0,
  last_seen_at INTEGER,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL,
  UNIQUE(surface, domain)
);

-- 術語別名（錯誤拼寫變體）
CREATE TABLE term_aliases (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  term_id INTEGER NOT NULL,
  alias TEXT NOT NULL,
  source TEXT,                   -- llm_inferred | user_correction | manual
  confidence REAL,
  FOREIGN KEY (term_id) REFERENCES terms(id),
  UNIQUE(alias)
);

-- 術語在每場會議的觀察紀錄
CREATE TABLE term_observations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  term_id INTEGER NOT NULL,
  session_id TEXT NOT NULL,
  occurrences_in_session INTEGER NOT NULL,
  observed_at INTEGER NOT NULL,
  FOREIGN KEY (term_id) REFERENCES terms(id),
  FOREIGN KEY (session_id) REFERENCES sessions(id)
);

-- 候選詞（每場會議產出，等每日批次處理）
CREATE TABLE term_candidates (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  surface TEXT NOT NULL,
  source_session_id TEXT NOT NULL,
  llm_confidence REAL,
  tfidf_score REAL,
  category_guess TEXT,
  status TEXT NOT NULL,          -- pending | promoted | rejected
  created_at INTEGER NOT NULL
);

-- 使用者校正事件（最強訓練信號）
CREATE TABLE corrections (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT NOT NULL,
  original TEXT NOT NULL,
  corrected TEXT NOT NULL,
  context TEXT,
  applied_to_term_id INTEGER,
  created_at INTEGER NOT NULL
);

-- 多 LLM provider 設定
CREATE TABLE provider_config (
  task TEXT PRIMARY KEY,         -- correction | summary | extraction
  provider TEXT NOT NULL,
  model TEXT NOT NULL,
  options_json TEXT
);
```

## 2.4 四層校正引擎流程

```
[原始字幕] "我們的 H T F C N N 模型在尼姆任務上效果不錯"
     │
     ▼
L3 核心層（硬替換、零成本）
  - alias "H T F C N N" 命中 → 替換為 "HTF-CNN"
     │
     ▼
L2 正式層（純算術、jieba 分詞 + 模糊比對）
  - "尼姆" + 讀音映射表 → "NILM"
     │
     ▼
L1 候選層（弱權重、LLM 輔助）
  - 候選詞包進 LLM prompt，LLM 對照脈絡判斷
     │
     ▼
L0 動態 RAG（脈絡感知、Workers AI Llama）
  - 讀 Notion 專案頁 + GitHub 知識庫
  - LLM 用脈絡校正未登錄但能推斷的詞
     │
     ▼
[校正後] "我們的 HTF-CNN 模型在 NILM 任務上效果不錯"
```

設計哲學：先用最便宜方法解決 80%，再讓昂貴方法處理剩下的 20%。

## 2.5 自學習迴路（每日批次 + 手動觸發）

每天 UTC 00:00 透過 Cron Trigger 執行；使用者也可從 Extension 手動觸發：

```
Step 1：收集當天所有會議 corrected_caption
Step 2：LLM 抽取候選術語（Workers AI Llama）
Step 3：TF-IDF 補強（純 TS）
Step 4：多訊號信心分數計算
   score = 0.4 * llm_confidence
         + 0.2 * normalize(occurrences)
         + 0.2 * normalize(sessions_seen)
         + 0.1 * normalize(tfidf_score)
         + 0.1 * notion_match_score
   if has user_correction: score = max(score, 0.95)
Step 5：分層分配
   ≥ 0.95 → L3_core
   0.7-0.95 → L2_official
   0.3-0.7 → L1_candidate
   < 0.3 → L0_observe
Step 6：寫入 D1 + 同步 Notion + 同步 GitHub terms.yaml
```

**降級邏輯**：30 天未出現的 L1 詞自動降回 L0；60 天未出現的 L2 詞降回 L1。

## 2.6 API 設計（精選）

```
POST /api/sessions/start
  Body: { meet_url, notion_project_id?, user_token }
  Response: { session_id, started_at }

POST /api/sessions/:id/caption
  Body: { speaker?, text, timestamp }
  Response: { ack: true }

POST /api/sessions/:id/end
  Response: { session_id, status: "processing", estimated_completion }

GET /api/sessions/:id/result
  Response: { status, corrected_caption_url, summary_md, action_items, github_url, notion_page_url }

GET /api/terms?layer=L2_official&domain=NILM
POST /api/terms/extract { range_start, range_end }
POST /api/corrections { session_id, original, corrected, context }
```

## 2.7 安全與隱私

| 項目 | 設計 |
|---|---|
| 認證 | Token-based，token 存 chrome.storage.local |
| CORS | Worker 只允許 https://meet.google.com origin |
| 音訊 | Extension 只抓字幕、不接觸音訊；後端不持久化（KV TTL 7 天） |
| 機密會議 | 使用者可標記「機密」，但 corrections 仍保留供學習（決策 d） |
| API key 保護 | 全部存 Worker secrets，永不送到 Extension |
| 學員 fork 隔離 | 每個學員自己的 Cloudflare 帳號 + D1，完全資料隔離 |

## 2.8 依賴與限制

### 外部服務依賴與免費額度

| 服務 | 用途 | 免費額度 |
|---|---|---|
| Cloudflare Workers | 後端執行 | 100k req/day |
| Cloudflare D1 | 資料庫 | 5GB / 5M reads/day |
| Cloudflare KV | 暫存 | 100k reads/day |
| Workers AI | 校正 + 抽取 | 10k Neurons/day |
| Gemini Flash | 摘要 | 寬鬆免費額度 |
| Notion API | 雙向同步 | 完全免費 |
| GitHub API | 知識庫推送 | 5000 req/hour |
| Resend | Email | 3000 封/月 |

### 已知限制與緩解

1. **Google Meet UI 變動**：DOM selector 失效。**緩解**：selector 寫在 Worker secrets 動態下發，不硬寫在 Extension。
2. **字幕本身不準**：校正能修拼錯/縮寫，無法救「整句誤聽」。
3. **D1 eventual consistency**：跨地區寫入毫秒延遲，個人使用無感。
4. **Workers 免費 plan CPU 限制**：摘要可能超時。**緩解**：用 Workflows 丟背景，主 request 直接 return（任務 1.13 涵蓋）。
5. **Cron Trigger 最小 1 分鐘**：足夠應付每日批次。

---

# 3. Tasks（任務清單）

## 3.1 整體規劃

採用「**極瘦身 MVP + 拆分 Phase 2 + Phase 3 在 Phase 2 後**」策略：

- **Phase 1（極瘦身 MVP）**：3-5 天，只做 L3 核心層 + Gemini 摘要 + GitHub 推送
- **Phase 2A（脈絡校正）**：3-4 天，加 L1 動態校正、Notion 脈絡讀取、Email、Notion 寫回
- **Phase 2B（自學習迴路）**：4-5 天，每日批次抽取、信心分層、自動晉升、術語表三向鏡像
- **Phase 3（教學打磨）**：5-7 天，課程模組、starter template、教學文件

複雜度：**S** = 半天內、**M** = 1-2 天、**L** = 3+ 天

## Phase 1：極瘦身 MVP（3-5 天）

**目標**：開一場真會議 → 5 分鐘內 GitHub 收到 Markdown 紀錄。只做 L3 核心層 + Gemini 摘要 + GitHub 推送，不含 Notion / Email / L2-L0 / 自學習。

### 基礎設施
| # | 任務 | 複雜度 | 依賴 |
|---|---|---|---|
| 1.1 | Cloudflare Workers + Hono.js 專案骨架 | S | - |
| 1.2 | D1 資料庫 + 初始 schema（sessions, terms, term_aliases, corrections） | S | 1.1 |
| 1.3 | KV namespace（字幕暫存、TTL 7 天） | S | 1.1 |
| 1.4 | Worker secrets（Gemini key、GitHub token） | S | 1.1 |
| 1.5 | Token-based auth middleware | S | 1.1 |

### Chrome Extension（前端）
| # | 任務 | 複雜度 | 依賴 |
|---|---|---|---|
| 1.6 | Manifest V3 骨架、icon、permissions | S | - |
| 1.7 | content.js：MutationObserver 監聽 Meet 字幕 DOM | M | 1.6 |
| 1.8 | background.js：字幕 batch 推送（每 10 秒） | S | 1.7 |
| 1.9 | popup.html：開始/結束按鈕、會議狀態 | M | 1.6 |
| 1.10 | Settings 頁：Worker URL、token | S | 1.9 |

### 後端 API + 處理 Pipeline
| # | 任務 | 複雜度 | 依賴 |
|---|---|---|---|
| 1.11 | POST /sessions/start | S | 1.2, 1.5 |
| 1.12 | POST /sessions/:id/caption | S | 1.3, 1.11 |
| 1.13 | POST /sessions/:id/end → 觸發背景 Workflow | M | 1.12 |
| 1.14 | 後處理 Workflow：拉字幕 → L3 校正 → 摘要 → GitHub | L | 1.15-1.17 |
| 1.15 | LLM Provider 抽象層（workers-ai + gemini） | M | 1.4 |
| 1.16 | L3 核心層校正（純 string replace） | S | 1.2 |
| 1.17 | 摘要引擎：Gemini Flash → Markdown + Action Items | M | 1.15 |
| 1.18 | GitHub 推送（複用 SecondBrain MCP commit pattern） | M | 1.14 |
| 1.19 | GET /sessions/:id/result | S | 1.18 |

### 整合
| # | 任務 | 複雜度 | 依賴 |
|---|---|---|---|
| 1.20 | 端到端測試：真實 Google Meet → 完整跑一次 | M | 1.19 |
| 1.21 | 種子資料：手動寫入 30-50 條 L3 核心術語 | S | 1.2 |
| 1.22 | Phase 1 README + 部署指南 | S | 1.20 |

**Phase 1 完成標準**：開一場真會議 → 5 分鐘內 GitHub 收到 Markdown 紀錄。

## Phase 2A：脈絡校正（3-4 天）

**目標**：加上 L1 動態校正、Notion 脈絡讀取、Email/Notion 分發。**不含每日批次抽取與自動晉升**。

| # | 任務 | 複雜度 | 依賴 |
|---|---|---|---|
| 2A.1 | L2 正式層校正（jieba-js 分詞 + 模糊比對） | M | 1.16 |
| 2A.2 | L0 動態 RAG：讀 Notion 專案頁脈絡 | L | 1.15 |
| 2A.3 | L0 動態 RAG：讀 GitHub 知識庫脈絡（用 session 關鍵字搜尋） | M | 2A.2 |
| 2A.4 | L1 候選層：包進 LLM prompt 弱權重 | M | 2A.2 |
| 2A.5 | Notion API 寫入：建立會議紀錄頁 | M | 1.14 |
| 2A.6 | Email 分發（Resend） | S | 1.14 |
| 2A.7 | Chrome Extension：Notion 專案頁選擇下拉 | S | 1.9 |
| 2A.8 | Phase 2A 整合測試 | M | 2A.1-2A.7 |

**Phase 2A 完成標準**：會議結束後三條分發路徑都收到結果，且 L1+L0 動態校正能從 Notion 脈絡修正未登錄詞。

## Phase 2B：自學習迴路（4-5 天）

**目標**：每日批次抽取、信心分層、自動晉升、術語表三向鏡像。

### 自學習基礎
| # | 任務 | 複雜度 | 依賴 |
|---|---|---|---|
| 2B.1 | 擴充 D1 schema：term_observations, term_candidates, provider_config | S | - |
| 2B.2 | Cron Trigger（每日 UTC 00:00） | S | 2B.1 |
| 2B.3 | TF-IDF 計算工具（純 TS） | M | 2B.1 |
| 2B.4 | LLM 抽取 prompt + parser | M | 1.15 |
| 2B.5 | 信心分數計算函式（多訊號融合） | M | 2B.3, 2B.4 |

### 自動晉升降級
| # | 任務 | 複雜度 | 依賴 |
|---|---|---|---|
| 2B.6 | 晉升邏輯：寫入 / 更新 terms 表 layer | M | 2B.5 |
| 2B.7 | POST /corrections：強制晉升 L3 | M | 2B.1 |
| 2B.8 | 降級邏輯：30/60 天未出現自動降級 | S | 2B.6 |

### 三向鏡像
| # | 任務 | 複雜度 | 依賴 |
|---|---|---|---|
| 2B.9 | Notion 術語表 database schema | S | - |
| 2B.10 | D1 → Notion 同步（每天批次） | M | 2B.6, 2B.9 |
| 2B.11 | D1 → GitHub terms.yaml 同步 | M | 2B.6 |
| 2B.12 | Notion → D1 反向 sync（每天讀回） | M | 2B.9 |

### 手動觸發
| # | 任務 | 複雜度 | 依賴 |
|---|---|---|---|
| 2B.13 | POST /terms/extract（手動觸發） | S | 2B.5 |
| 2B.14 | Extension popup「立即抽取術語」按鈕 | S | 2B.13 |

### 整合測試
| # | 任務 | 複雜度 | 依賴 |
|---|---|---|---|
| 2B.15 | 跑 5-10 場真會議，驗證學習迴路 | L | 2B.1-2B.14 |
| 2B.16 | 校正準確度量測（標 100 句，比對校正前後） | M | 2B.15 |
| 2B.17 | 調參：信心分數權重、晉升閾值 | M | 2B.16 |

**Phase 2B 完成標準**：第 5-10 場會議後候選層自動累積 50+ 術語；至少 3-5 個你「沒手動加但被自動晉升 L2/L3」的詞，後續會議真的被正確校正。

## Phase 3：教學打磨（5-7 天）

**啟動時機**：Phase 2B 完全跑順之後。

### 課程模組
| # | 任務 | 複雜度 | 對應教材 |
|---|---|---|---|
| 3.1 | Module 1（1.5h）：Chrome Extension + Google Meet DOM 抓取 | M | 投影片 + repo |
| 3.2 | Module 2（1h）：Cloudflare Workers + Hono + D1 | M | - |
| 3.3 | Module 3（1.5h）：四層校正引擎與信心分層哲學 | L | 含 demo notebook |
| 3.4 | Module 4（1.5h）：自學習迴路（無人工 HITL）設計 | L | - |
| 3.5 | Module 5（1h）：LLM Provider 抽象層與成本敏感選型 | M | - |
| 3.6 | Module 6（1h）：分發層（GitHub MCP / Notion / Email） | S | - |
| 3.7 | Module 7（0.5h）：學員自架部署 walkthrough | S | - |

### Starter Template
| # | 任務 | 複雜度 |
|---|---|---|
| 3.8 | GitHub 公開 repo `meeting-capture-studio-starter` | M |
| 3.9 | 6 領域常用術語表種子資料（智慧製造、NILM、永續、ESG、AI/ML、學術寫作） | M |
| 3.10 | 學員作業：「換掉某個元件」三個方向 | S |
| 3.11 | 5 分鐘 demo 影片 | S |

### 文件
| # | 任務 | 複雜度 |
|---|---|---|
| 3.12 | README：架構圖、Quick Start、各 module 連結 | M |
| 3.13 | 學員手冊：每 module 對應 markdown，含學習目標 + 作業 | L |
| 3.14 | 故障排除指南：DOM 變動、API key、D1 連線等 | M |
| 3.15 | 維護計畫：每月檢查 selector、季度 review 學習迴路 | S |

## 任務依賴與關鍵路徑

```
Phase 1 關鍵路徑：1.1 → 1.2 → 1.11 → 1.12 → 1.13 → 1.14 → 1.18 → 1.19 → 1.20

Phase 1 可並行群組：
- 前端：1.6 → 1.7 + 1.8 + 1.9 + 1.10
- LLM 抽象層：1.15（與其他並行）

Phase 2A 關鍵路徑：2A.1 + 2A.2 → 2A.4 → 2A.8

Phase 2B 關鍵路徑：2B.1 → 2B.5 → 2B.6 → 2B.15 → 2B.17

Phase 3 大量並行：3.1-3.7 module 之間獨立、3.8-3.11 之間獨立
```

## 風險清單與緩解

| 風險 | 緩解 |
|---|---|
| Google Meet DOM 變動 | Selector 動態下發 |
| Workers 免費 CPU 超限 | Workflows 丟背景（任務 1.13） |
| Workers AI 額度耗盡 | Provider 抽象層切 Gemini |
| D1 schema 演進 | wrangler migrations、只加不刪 |
| 學習迴路收斂慢 | 任務 2B.16 量測 → 2B.17 調權重 |
| Notion API rate limit | batch 寫入、讀回每天一次 |

## 完整任務統計

| Phase | 任務數 | 預估時間 |
|---|---|---|
| Phase 1（極瘦身 MVP）| 22 | 3-5 天 |
| Phase 2A（脈絡校正） | 8 | 3-4 天 |
| Phase 2B（自學習迴路） | 17 | 4-5 天 |
| Phase 3（教學打磨） | 15 | 5-7 天 |
| **總計** | **62** | **2.5-3 週** |

---

# 💡 與我的連結

## 對個人工作流的價值
1. 學術論文工作流：採訪業界專家、與指導教授討論時可錄音轉摘要
2. 企業培訓：講課時開錄音，課後直接產出講義初稿
3. 客戶會議：政府/企業客戶會議走機密模式（保留學習信號）
4. 知識管理：每場會議自動進知識庫，未來可被其他 AI 檢索

## 對教學的價值
1. **完整 vertical slice**：從 Chrome Extension 到 D1 到 LLM 到分發，學員一路看下來
2. **實用性**：學員學完馬上有自己的工具，每天開會都用得到
3. **可複製、可客製**：每個學員的版本都會不同（不同 LLM、不同分發目的地、不同術語表）
4. **教架構素養而非工具操作**：信心分層、學習迴路、Provider 抽象層、成本敏感選型——這些都是大型 AI 系統設計的通用素養
5. **與既有課程體系完美互補**：補足「實戰專案」這塊空缺

## 對網站基礎設施的擴展
- 第五個 MVP 網站：「會議筆記基礎設施」
- 與既有四個網站共用 Cloudflare 帳號、共用部署 pipeline
- 未來可對外提供（白標版本給企業客戶）

# 📝 個人註記

**這個專案的真正價值不在「會議錄音」**，而在「**這是學員第一個能完整擁有的 AI 基礎設施**」。市面上的會議工具都把使用者鎖在他們的雲端；自己打造的版本，學員學會的不是「怎麼用工具」，而是「**怎麼造工具**」。

**Self-learning 迴路的設計是這個專案最強的差異化**。Tactiq、Otter、Fireflies 都沒做這個——他們是通用工具，不可能為每個使用者建立個人化術語表。**自建版本反而能做到他們做不到的事**——因為「個人化」需要的是擁有資料主權，而不是雲端規模。

**呼應「不要做免費仔」的更高層次論述**：不只是付費用最強的，更不是省錢用最差的。是**理解每個元件成本與品質的權衡**——L3 用 string replace 不用 LLM、校正用 Workers AI 免費版、摘要才用 Gemini 品質版——這個工程素養是課程真正能教給學員的東西。

**Harness engineering 的具體案例**：這個系統是「會議專屬 agent」，包含 perception（字幕抓取）、memory（術語表 + 知識庫）、reasoning（四層校正 + 摘要）、action（多目的地分發）四個經典 agent 元件。教學上是 agent 架構的絕佳入門案例。

# 🔗 延伸閱讀

- [Tactiq](https://tactiq.io/)—— 商業參考實作（差異化標的）
- [Cloudflare Workers AI 文件](https://developers.cloudflare.com/workers-ai/)
- [Hono.js 文件](https://hono.dev/)
- [Gemini API 文件](https://ai.google.dev/)
- [Manifest V3 Migration Guide](https://developer.chrome.com/docs/extensions/develop/migrate)
- [pke_zh](https://github.com/shibing624/pke_zh) —— 中文關鍵字抽取多算法包（v2 進階參考）
- [KeyBERT](https://github.com/MaartenGr/KeyBERT) —— BERT-based keyword extraction
- [YAKE!](https://github.com/LIAAD/yake) —— 統計式關鍵字抽取
- [Self-RAG paper](https://selfrag.github.io/) —— 自我反思 RAG（進階課程教材）
- [Awesome RAG](https://github.com/Danielskry/Awesome-RAG)

# ℹ️ 規格資訊

- **規格類型**：SDD（Spec-Driven Development）
- **狀態**：Draft v1.0（已完成需求釐清，待進入實作）
- **建立流程**：透過 SecondBrain MCP openspec_propose 取得模板，經 7 輪需求釐清對話確定
- **下一步**：等待啟動決策（建議：完成 EPSR 論文審稿後啟動 Phase 1）
- **建立時間**：2026-04-26
