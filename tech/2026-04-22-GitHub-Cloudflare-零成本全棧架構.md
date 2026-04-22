---
title: GitHub + Cloudflare 零成本知識庫 × 學習系統全棧架構
date: 2026-04-22
category: tech
tags: [cloudflare, github, workers-ai, rag, 知識庫, 學習系統, 架構設計, flux, vectorize, d1]
---

# GitHub + Cloudflare 零成本全棧架構

知識庫建立在 GitHub 上（生產端），學員入口在 Cloudflare（消費端）。一人維護，多人使用，月成本 $0。

## 架構概覽

```
┌─ GitHub（知識工廠）──────────────┐    ┌─ Cloudflare（學員入口）──────────┐
│ 老師 / 自動化 寫入                │    │ 多學員同時使用                   │
│                                  │    │                                 │
│ SecondBrain/*.md (Obsidian)      │    │ TG Bot / Discord / Pages 網頁   │
│       │ git push                 │    │       │                         │
│       ▼                          │    │       ▼                         │
│ GitHub Actions                   │    │ Worker（API 路由）               │
│ ├── compile.py → wiki            │    │ ├── D1（題庫/進度/知識索引）      │
│ ├── 爬蟲 → 新知識卡片             │    │ ├── R2（圖片/附件, 10GB）        │
│ ├── 論文搜集 → 摘要              │    │ ├── Vectorize（語意搜尋, 5M 向量）│
│ ├── AI 出題 → 題庫               │    │ ├── Workers AI（即時問答）        │
│ └── Graphify → 圖譜              │    │ └── FLUX（圖片生成, 3s）          │
│       │ 完成後                    │    │       │                         │
│       ▼                          │    │       ▼                         │
│ POST → api.cooperation.tw ──────┼───→│ Pages（瀏覽/圖譜/學習頁）        │
└──────────────────────────────────┘    └─────────────────────────────────┘
  寫入方：1 人                            讀取方：N 人
  重型、慢、不限時間（6hr/job）            輕型、快、即時回應（<3s）
```

## 分工原則

| 任務類型 | 在哪跑 | 為什麼 |
|---------|--------|--------|
| 問答、搜尋、快速回覆 | Cloudflare Worker | <10ms CPU，即時 |
| 存取知識、圖片生成 | Cloudflare D1/R2/FLUX | 免費額度內 |
| 爬蟲、深度研究 | GitHub Actions | 6hr/job，無限分鐘（public repo）|
| compile、Graphify | GitHub Actions | 需完整 Python 環境 |
| GPU 推理（大模型）| ac-3090 | vLLM、ComfyUI |

## 已驗證組件（2026-04-22 實測）

### 文字模型排名（5 題 iPAS 術語測試）

| 排名 | 模型 | 延遲 | 得分 |
|:---:|------|:---:|:---:|
| 1 | Qwen3-30B (`@cf/qwen/qwen3-30b-a3b-fp8`) | 1-3s | 5/5 |
| 2 | llama-3.3-70b (`@cf/meta/llama-3.3-70b-instruct-fp8-fast`) | 1-4s | 5/5 |
| 3 | deepseek-r1-32b | 5-8s | 3/5（不推薦）|

### 語意搜尋（Qwen3-embedding-0.6B）

用口語問題搜尋專業術語卡片，3/3 全部命中：
- 「碳盤查是什麼」→ ✅ 找到 LCI 生命週期盤查分析
- 「買綠電可以減碳嗎」→ ✅ 找到 Scope 2 間接排放
- 「歐盟對進口商品課碳稅」→ ✅ 找到 CBAM 碳邊境調整機制

### RAG 全流程（語意搜尋 + Qwen3-30B 生成回答）

10 張知識卡片，5 個學員問題，5/5 回答全部正確：
- 「碳盤查用什麼軟體？」→ SimaPro/GaBi（2.7s）
- 「公司電費高碳排怎麼算？」→ Scope 2 + 碳費制度交叉引用（3.2s）
- 「台灣碳費一噸多少？」→ 300 元/噸，優惠 100 元（1.0s）
- 「甲烷暖化是 CO2 幾倍？」→ 28 倍（0.7s）
- 「RAG 跟 ChatGPT 差在哪？」→ 完整流程解釋 + 差異比較（3.7s）

### FLUX 圖片生成（6 場景測試）

| 場景 | 品質 | 關鍵 prompt 元素 |
|------|:---:|------------------|
| 人像 | ⭐5 | Canon EOS R5 85mm f/1.2, Kodak Portra 400 |
| 室內 | ⭐5 | Sony A7IV 35mm f/1.4, 材質細節描述 |
| 產品攝影 | ⭐5 | 85mm f/2.8, directional lighting |
| 風景 | ⭐5 | 24-70mm, Kodak Portra 400, fog/mist |
| 夜景 | ⭐4 | 35mm f/1.8, neon reflections（文字是弱點）|
| 空拍 | ⭐5 | DJI Mavic 3 Pro, Fuji Velvia 50 |

**FLUX 不能生中文字**，需要 PIL 疊加。Prompt 必須用自然語言完整句 + 真實攝影器材。

## 免費額度

| 資源 | 免費額度 | 個人使用估算 |
|------|---------|------------|
| GitHub Actions | 無限（public repo） | ~30 min/天 |
| Workers | 100K req/天 | ~500 req |
| Workers AI | 10K neurons/天 | ~200 次對話 |
| D1 | 5M reads/天 | ~2K reads |
| R2 | 10GB, 0 出站費 | ~2GB |
| Vectorize | 5M 向量 | ~10K 文件 |
| Pages | 無限部署 | 1 站 |
| **月成本** | **$0** | |

## 10 個場景應用

### 學習系統
1. **iPAS AI 問答助教** — 學員 TG 問問題 → Vectorize 搜知識庫 → Qwen3-30B 用知識卡片回答（<3s）
2. **三問法 + 知識庫 RAG** — 答錯時從知識庫動態生成追問，不是罐頭
3. **個人化學習路徑** — D1 追蹤弱項 → 推薦知識卡片 + 出針對性題目

### 知識庫自動成長
4. **每日新聞入庫** — Actions cron 爬蟲 → AI 摘要 → 知識卡片 → D1 + Vectorize
5. **論文自動搜集** — Scholar + PubMed → 摘要 → 分類 → 圖譜長新節點
6. **學員提問反哺** — 知識缺口標記 → Actions 自動補資料 → 下次秒答

### 教學輔助
7. **課前自動備課** — TG 說「明天上 ESG」→ Actions 撈卡片 → 出測驗 + 大綱
8. **課後即時複習** — 掃 QR → Pages 複習頁 → 測驗 → AI 追問

### 知識分享
9. **公開知識庫網站** — Pages: 瀏覽/圖譜/語意搜尋/wiki/每日簡報
10. **多課程共用** — 同一知識庫，不同課程過濾不同分類切面

## 技術限制

| 限制 | 影響 | 解法 |
|------|------|------|
| Workers CPU 10ms | 不能跑重型運算 | 重型任務走 GitHub Actions |
| FLUX 不能生中文字 | 圖片標題要後製 | PIL 疊中文，或用 Gemini |
| 無即時推播（免費） | 網頁不能 realtime update | TG Bot 本身就是推播通道 |
| Vectorize 搜尋非 100% | 偶爾 Top1 不是最佳 | 取 Top2-3 一起給 LLM 判斷 |

## 與現有系統關係

- **不取代 Firebase** — ClassClaw 即時互動繼續用 Firebase Auth + RTDB
- **不取代 ac-mac** — 重型 AI 任務（Gemini browser automation）仍在 ac-mac
- **補強 GitHub** — 現有 SecondBrain repo 不動，加 Actions + Cloudflare 前端
- **統一 API 入口** — api.cooperation.tw 已有，擴充 endpoint 即可

## 調用方式速查

### 文字模型
```bash
curl -s -X POST https://api.cooperation.tw/api/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt":"你的問題","model":"qwen3-30b"}'
```

### 圖片生成
```bash
OAUTH_TOKEN=$(npx wrangler auth token 2>&1 | grep -v "^[⛅─]" | grep -v "^$" | tail -1)
curl -s -X POST "https://api.cloudflare.com/client/v4/accounts/cb8f37b75da7355292c6c23a17adf6c6/ai/run/@cf/black-forest-labs/flux-1-schnell" \
  -H "Authorization: Bearer ${OAUTH_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"natural language description here","width":1920,"height":1080}'
```

### 語意搜尋（embedding）
```bash
curl -s -X POST "https://api.cloudflare.com/client/v4/accounts/cb8f37b75da7355292c6c23a17adf6c6/ai/run/@cf/qwen/qwen3-embedding-0.6b" \
  -H "Authorization: Bearer ${OAUTH_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"text":["你的查詢"]}'
```
