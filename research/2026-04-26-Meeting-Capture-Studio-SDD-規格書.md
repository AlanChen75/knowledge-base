---
title: "Meeting Capture Studio SDD 規格書"
date: 2026-04-26
category: research
tags: [sdd, openspec, meeting-capture, chrome-extension, cloudflare-workers, workers-ai, gemini, rag, self-learning, terminology-extraction, 課程教材, ai-四級課程, ai-智慧製造, mvp-基礎設施]
type: research
source: "個人會議工作流需求 + AI 四級課程進階模組教案規劃"
status: in-progress
implementation_repo: "ai-cooperation/meeting-capture-studio"
phase_1_completed: 2026-04-27
phase_2_started: 2026-04-27
---

# Meeting Capture Studio — SDD 規格書

> **可作為課程教材引用**
> 適用課程：AI 四級課程（進階模組）、AI 智慧製造三級課程、AI 永續兩級課程
> 教學定位：6-8 小時課程，學員 fork 後完成自己的 MVP 版本
> 教學主軸：Chrome Extension + RAG + LLM Provider 抽象層 + 自學習迴路 + 個人化 AI 工作流

## 📌 核心決策快照（2026-04-27 實作後修訂）

| 主題 | 原 SDD 決策 | 實作 v1（4/27）| 備註 |
|---|---|---|---|
| 主入口 | Chrome Extension（Google Meet）| **LINE@ Bot（手機錄音分享）** | v2 路徑提前到 v1，Chrome Extension 改 Phase 2B |
| 後端執行 | Cloudflare Worker + Workflows + D1 | **Worker（webhook receiver）+ GitHub Actions（重活）** | Phase 3 評估遷移到 Workflows |
| STT | Workers AI Whisper | **Groq Whisper Turbo（206x）+ Groq Large + CF Whisper 三層 fallback** | 速度提升 9 倍 |
| 摘要 LLM | Gemini 2.5 Flash | **OpenRouter Ling 1T (free) + GPT-OSS-120B fallback** | 免費、不撞 Gemini quota |
| 校正架構 | 四層信心分層 + 自動晉升 | **L3 + L2 + L1 完成（Phase 2A）；L0 RAG + 自學習 待 Phase 2B** | 路徑一致 |
| 術語表存放 | D1 為主 + Notion + GitHub 鏡像 | **GitHub `terms/*.yaml` 為單一來源** | 簡化，不上 D1 |
| RAG context | Notion 專案頁 + GitHub knowledge-base | **GitHub knowledge-base + Google Calendar event（取代 Notion）** | 用 Calendar 取代 Notion 因更通用 |
| 分發 | GitHub + Notion + Email | **GitHub + LINE push（Phase 2 加 Notion 鏡像作備份）** | Email 暫不做 |
| Notion 整合 | 雙向 | **單向鏡像（備份用，Phase 2A.6）** | 主要紀錄在 GitHub |
| 教學版 | 與個人版同程式碼 | **Phase 3 才做課程模組，先打通自用 + 開源** | 開源後學員 fork |
| 月成本 | $0 | **$0**（已驗證）| 維持 |

---

## 🎯 實作演進記錄

### Phase 1（2026-04-27 完成）

**已實作**：
- ✅ LINE@ Bot webhook → Cloudflare Worker → GitHub Actions repository_dispatch
- ✅ Groq Whisper Turbo STT（三層 fallback：Groq Turbo → Groq Large v3 → CF Whisper）
- ✅ ffmpeg 自動降 bitrate（檔案 > 25MB 自動處理）
- ✅ L3 種子術語字典（30 條 hardcode）+ opencc 簡繁轉換
- ✅ OpenRouter Ling 1T 摘要（Notion 風格 prompt + 反編造規則）
- ✅ GitHub commit + LINE push
- ✅ `_logs/runs.jsonl` 追蹤層（每次處理 metadata）
- ✅ ffprobe 抓 m4a 錄音時間（如 metadata 還在）
- ✅ 額度用量統計（每次跑完印報告）
- ✅ 失敗時 LINE 通知

**未做（從原 SDD 移除）**：
- ❌ D1 schema（用 GitHub repo 取代）
- ❌ KV namespace（沒字幕暫存需求；Phase 2B Chrome Extension 才需要）
- ❌ Sessions API（用 GitHub Actions 取代）
- ❌ Chrome Extension（v1 改用 LINE 入口）
- ❌ Token-based auth middleware（用 LINE 簽名驗證取代）

### Phase 2A（2026-04-27 開始）

**已實作**：
- ✅ **2A.1 術語字典模組化**（`terms/*.yaml` 按領域分檔）
  - `_global.yaml` / `energy.yaml` / `ai-tech.yaml` / `sustainability.yaml`
  - 領域自動偵測（命中 ≥ 2 個 keyword 才載入）
- ✅ **2A.4 L1 LLM 校正**（Groq Llama 3.3 70B + glossary 候選詞表）
- ✅ **2A.5 L2 jieba 模糊比對**（編輯距離 1 的近似詞）
- ✅ **2A.2 一次性提煉 script**（`scripts/extract-terms.py`，從 knowledge-base 抽術語）
- ✅ **2A.7 README**（部署指南）
- ✅ **2A.8 SDD 更新**（本檔案）

**進行中**：
- 🔄 **2A.6 Notion 雙向鏡像**（單向寫入會議紀錄到 Notion DB 作備份/展示，需用戶提供 Notion API + DB ID）
- 🔄 **2A.3 L0 Google Calendar 整合**（STT 後比對候選會議，LINE quick reply 讓使用者選；需用戶提供 Google OAuth）

### Phase 2B（待開始）

- Chrome Extension 入口（Google Meet 字幕抓取）
- KV namespace（暫存字幕片段）
- 自學習迴路（L1 修正詞 → 候選詞庫 → 自動晉升 L3）

### Phase 3（延後）

**目標**：開源 + 帶學員 fork 重做
**範圍**：原 SDD Phase 3 課程模組（共 8 小時 7 個 module）
**啟動條件**：Phase 2B 完成、自己用順手 1 個月以上

---

## 🔄 流程修正（重要）

**原 SDD 流程**：
```
Chrome Extension 抓字幕 → 立刻問用戶選 Notion 專案頁 → 注入 RAG context → 處理
```

**實作 v1 流程**：
```
LINE 收音檔 → 立刻觸發 pipeline → 處理完才推 LINE
（無 Calendar 對應、無與會者註解）
```

**Phase 2A 修正流程（待實作）**：
```
LINE 收音檔 → 觸發 pipeline 自動跑：
  Stage 1: Groq STT → 逐字稿
  Stage 2: L3/L2/L1 校正 → 乾淨逐字稿
  Stage 2.5 (Phase 2A.3): 比對 Calendar 候選會議
    ├─ 抓最近 4 小時內結束、時長相符的 events
    ├─ LLM 比對逐字稿 vs event title/description
    ├─ 信心 > 80% → 自動 link
    └─ 信心 < 80% → LINE quick reply 問用戶選
  Stage 3: 注入 Calendar context（與會者、議程）→ 摘要
  Stage 4: GitHub + Notion + LINE push
```

**為什麼 STT 後才比對 Calendar 是對的**：
- 拿到逐字稿才有 context 可以比對 event title/description（更準）
- 用戶傳完音檔當下不一定方便互動
- 只在「不確定」時才打擾用戶

---

# 1. Proposal（保留原文）

[原內容保留，略]

---

# 2. Design — 實作版

## 2.1 實際架構（v1）

```
┌──────────────────────────────────────────────────────┐
│ Entry Layer                                           │
│  LINE@ Bot（手機錄音分享）                              │
│       ↓                                                │
│  Cloudflare Worker（webhook receiver + dispatcher）    │
└─────────────┬─────────────────────────────────────────┘
              ▼
┌──────────────────────────────────────────────────────┐
│ Processing Pipeline（GitHub Actions）                  │
│  Stage 1: STT 三層 fallback                            │
│    ├─ Groq Whisper Turbo（主，206x realtime）          │
│    ├─ Groq Whisper Large v3（備）                      │
│    └─ CF Workers AI Whisper Turbo（最後）              │
│  Stage 2: L3 字典 + opencc 簡繁                        │
│  Stage 2.5: L2 jieba 模糊比對                          │
│  Stage 2.6: L1 LLM 語境校正（Groq Llama 70B）          │
│  Stage 3: OpenRouter Ling 1T 摘要（Notion 風格）       │
│  Stage 5: GitHub commit + LINE push + jsonl 追蹤      │
└──────────────────────────────────────────────────────┘
```

## 2.2 LLM 用量分布

| 環節 | 平台 | 模型 | 限制 |
|------|------|------|------|
| Stage 1 STT 主 | Groq | whisper-large-v3-turbo | 7200s/hr, 28800s/day |
| Stage 1 STT 備 1 | Groq | whisper-large-v3 | 同上（獨立 model）|
| Stage 1 STT 備 2 | Cloudflare | @cf/openai/whisper-large-v3-turbo | 10K neurons/day |
| Stage 2.6 L1 校正 | Groq | llama-3.3-70b-versatile | 30 RPM |
| Stage 3 摘要主 | OpenRouter | inclusionai/ling-2.6-1t:free | 50 req/day（充值後 1000/day）|
| Stage 3 摘要備 | OpenRouter | openai/gpt-oss-120b:free | 同上 |

[原 2.3-2.8 內容保留]

---

# 3. Tasks — 實作進度

## Phase 1（已完成 2026-04-27）

達成率 ~70%（核心 pipeline 跑通；Chrome Extension 移到 Phase 2B；D1/KV 移到 Phase 2B）

詳細進度見 `_logs/runs.jsonl`。

## Phase 2A（進行中）

| # | 任務 | 狀態 | 備註 |
|---|------|------|------|
| 2A.1 | 術語字典模組化（terms/*.yaml）| ✅ | 4 個領域檔 |
| 2A.2 | 一次性提煉 script | ✅ | scripts/extract-terms.py |
| 2A.3 | L0 Google Calendar 整合 | 🔄 | 需 OAuth setup |
| 2A.4 | L1 LLM 校正（Groq Llama）| ✅ | glossary 候選詞表 |
| 2A.5 | L2 jieba 模糊比對 | ✅ | 編輯距離 1 |
| 2A.6 | Notion 雙向鏡像 | 🔄 | 需 Notion API key |
| 2A.7 | README 部署指南 | ✅ | |
| 2A.8 | SDD spec 更新 | ✅ | 本檔案 |

## Phase 2B（待開始）

- Chrome Extension 入口（Google Meet 字幕）
- KV namespace 暫存
- 自學習迴路

## Phase 3（延後 — 開源教學版）

[原 SDD Phase 3 內容保留，目前不啟動]

---

# 💡 與我的連結

[原內容保留]

# 📝 個人註記（4/27 補充）

**實作驗證了 SDD 的核心哲學是對的**：
- 「先用最便宜方法解決 80%」— Groq Whisper Turbo（free, 206x realtime）取代 Workers AI 是對的決定，速度提升 9 倍
- 「分層校正」— L3 簡繁字典 + L2 jieba + L1 LLM 各司其職，每層處理一種錯誤
- 「Provider 抽象層」— 三層 STT fallback 證明這個架構彈性

**SDD 偏離但更務實的決定**：
- 入口從 Chrome Extension 改 LINE@ — 手機錄音場景比 Google Meet 更普遍
- D1 → GitHub `terms/*.yaml` — 版本控制 + diff 可審查，比 D1 更友善
- Notion → Calendar — 通用性更高，桌機用戶都有 Calendar
- Workers + Workflows → Worker + GitHub Actions — 短期工程穩定優先，未來再遷移

**沒做但要記得的**：
- Phase 3 課程模組（學員教學版）— Phase 2B 完成且自用順手後再做
- 教材主軸：「擁有資料主權 + 個人化校正 + 自學習迴路 + 多 provider 抽象層」

# 🔗 延伸閱讀（補充）

- 實作 repo: https://github.com/ai-cooperation/meeting-capture-studio
- ARCHITECTURE.md: 完整架構圖
- README.md: 部署指南

[原延伸閱讀保留]

# ℹ️ 規格資訊

- **規格類型**：SDD（Spec-Driven Development）
- **狀態**：~~Draft v1.0~~ → **In Progress**（Phase 1 完成、Phase 2A 進行中）
- **建立時間**：2026-04-26
- **Phase 1 完成**：2026-04-27
- **Phase 2A 開始**：2026-04-27
- **實作 repo**：ai-cooperation/meeting-capture-studio
