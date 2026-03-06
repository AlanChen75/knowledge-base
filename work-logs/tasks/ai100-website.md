---
title: AI100 講網站建置
status: completed
priority: high
started: 2026-02-17
repo: ai-cooperation/ai100
url: https://ai-cooperation.github.io/ai100/
---

# AI100 講網站建置

## 目標
建立 iPAS AI 應用規劃師導向的 100 講教學網站，部署在 GitHub Pages。

## 整體進度

### ✅ 基礎架構（已完成）
- [x] GitHub repo: ai-cooperation/ai100（Jekyll + GitHub Pages）
- [x] 深色科技風主題：navy #0f172a / cyan #06b6d4 / purple #8b5cf6
- [x] 首頁 + 講座卡片 + 模組篩選
- [x] 講座詳情頁（Cornell Note、答案折疊、關鍵字檢核）
- [x] iPAS 評鑑碼標籤系統

### ✅ DOL 框架整合（已完成）
- [x] _data/dol_framework.yml（5 領域 + 7 原則）
- [x] 雙軌導航（iPAS 模組 / DOL 框架）
- [x] DOL 專屬頁面 /dol-framework/
- [x] 講座標籤 + 首頁篩選

### ✅ M01-M10 全部 100 講內容（已完成）
- [x] M01 AI 思維與治理 — 10 講
- [x] M02 資料素養與資料流程 — 10 講
- [x] M03 機器學習入門 — 10 講
- [x] M04 深度學習與代表架構 — 10 講
- [x] M05 生成式 AI 基礎 — 10 講
- [x] M06 No/Low Code 與應用規劃 — 10 講
- [x] M07 NLP / CV / 多模態應用 — 10 講
- [x] M08 大數據處理分析與應用 — 10 講
- [x] M09 MLOps 與系統部署整合 — 10 講
- [x] M10 iPAS 題型策略與實戰 — 10 講

### ✅ 講座配圖（已完成）
- [x] 100 張講座配圖（assets/images/lectures/）
- [x] 25 張 Bing 壞圖用 Gemini 重新生成

### ✅ 模組封面圖（已完成 2026-02-20）
- [x] M01-M10 十張模組封面圖（橫式 878x490, 16:9）
- [x] 深色主題配色、繁體中文標題 + 關鍵概念文字
- [x] 適配 module-cover CSS (340x160 object-fit: cover)

### ✅ 模組詳情頁（已完成 2026-02-20）
- [x] _layouts/module.html 模組頁面 layout
- [x] modules/M01-M10.md 十個模組頁面
- [x] 首頁模組卡片改為可點擊連結 → /modules/M0X/
- [x] 模組頁顯示封面大圖 + 10 講完整列表
- [x] 講座頁返回連結改為回到所屬模組
- [x] 模組間前後導覽

### ✅ AI 動態新聞功能（已完成 2026-02-20）
- [x] _layouts/post.html 新聞文章 layout
- [x] news.md 新聞列表頁 /news/
- [x] tools/ai-news-pipeline.py 自動化 pipeline
- [x] RSS 源：The Decoder, Simon Willison, Ars Technica AI, 電腦王阿達, 硬是要學, Google AI, OpenAI, Anthropic
- [x] Groq LLM 分析 + Gemini 生圖 + Jekyll post 自動生成
- [x] 部署到 ac-mac cron（每日 9:00, 18:00）
- [x] 新聞 ↔ 講座反向連結

### 🔲 待辦
- [ ] ai-news-pipeline.py timeout 調整（已在本地修改，未推送）
- [ ] 首頁新增「最新動態」區塊（可選）
- [ ] 模組進度追蹤功能（可選）

## 技術備忘

### 部署
- repo: github.com/ai-cooperation/ai100
- push: HTTPS
- build: GitHub Pages legacy build
- URL: https://ai-cooperation.github.io/ai100/

### AI 新聞 Pipeline
- 狀態檔：~/.ai100-news-state.json（ac-mac）
- AI Hub API：http://127.0.0.1:8760
- 端點：/api/llm/chat, /api/web/fetch, /api/image/generate
- Cron：0 9,18 * * * (ac-mac)

### 關鍵檔案
| 檔案 | 用途 |
|------|------|
| _config.yml | Jekyll 設定 |
| _data/modules.yml | 10 大模組定義 |
| _data/dol_framework.yml | DOL 框架資料 |
| _lectures/M01-XX.md ~ M10-XX.md | 100 講內容 |
| _layouts/home.html | 首頁模板 |
| _layouts/lecture.html | 講座頁面模板 |
| _layouts/module.html | 模組詳情頁模板 |
| _layouts/post.html | 新聞文章模板 |
| _layouts/dol-framework.html | DOL 框架頁面 |
| modules/M01-M10.md | 模組頁面 |
| news.md | 新聞列表頁 |
| tools/ai-news-pipeline.py | 新聞 pipeline |
| assets/css/style.css | 全站樣式 |
| assets/js/main.js | 篩選互動邏輯 |
| assets/images/lectures/ | 講座配圖 |
| assets/images/modules/ | 模組封面圖 |
| assets/images/news/ | 新聞配圖 |

### ✅ 新聞 Pipeline v2 升級（2026-02-22）
- [x] 來源多元化：時間排序取代 tier 排序
- [x] 配圖：Gemini 思考型 + 繁體中文標題
- [x] 摘要：Gemini 思考型 + 網路查證 + verified 欄位
- [x] 排程：3 次/天（09:05, 13:05, 18:05），每次 3 篇
- [x] 監控：verified=false 寫 log WARNING + TG ⚠️ 標記
- [x] 移除失效 Anthropic RSS，Simon Willison 加 AI filter
- [x] gemini_chat provider 新增 `_ensure_thinking_model()`
