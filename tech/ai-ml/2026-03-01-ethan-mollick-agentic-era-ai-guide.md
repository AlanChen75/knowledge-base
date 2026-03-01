---
title: Ethan Mollick 代理時代 AI 使用指南
date: 2026-03-01
source: Ethan Mollick - A Guide to Which AI to Use in the Agentic Era
category: tech/ai-ml
tags: [AI Agent, Claude, GPT, Gemini, 工作效率, 典範轉移]
type: article
raw_file: ../../raw/2026-03/2026-03-01-091736-text.txt
difficulty: ⭐⭐⭐
author: Ethan Mollick
---

# Ethan Mollick 代理時代 AI 使用指南

## 📊 元資訊
- **難度**：⭐⭐⭐
- **來源類型**：文章
- **作者**：Ethan Mollick（華頓商學院教授）
- **筆記時間**：2026-03-01 09:17

## 📌 摘要
Ethan Mollick 發布第八版 AI 使用指南，指出我們已正式進入「代理時代 (Agentic Era)」。他提出「模型、應用程式、AI 工作套件（Harness）」三大維度框架，強調從「提示工程」轉型為「管理者思維」的重要性，並建議透過付費方案與專業工作框架來極大化生產力。

## 🏷️ 標籤分類
- **大分類**：tech
- **小分類**：ai-ml

## 🔑 關鍵要點

### 1. 認知斷裂：AI 使用定義的根本改變
- 過去「使用 AI」= 在對話框裡聊天
- 現在「使用 AI」= 指派任務 (Assigning) 給能自主使用工具的 Agent
- 這是自 ChatGPT 發布以來最大的典範轉移

### 2. 三大構面框架
| 構面 | 說明 | 範例 |
|------|------|------|
| **模型 (Models)** | AI 的「大腦」，決定聰明程度與能力 | GPT-5.2/5.3、Claude Opus 4.6、Gemini 3 Pro |
| **應用 (Apps)** | 與模型互動的產品介面 | chatgpt.com、Claude Code、Claude Cowork |
| **AI 工作套件 (Harnesses)** | 讓 AI 能使用外部工具、自主完成多步驟任務的系統 | 程式碼執行環境、瀏覽器控制、檔案系統存取 |

### 3. Harness 的威力
- **Mollick 的比喻**：「Harness 就像馬具，能擷取馬匹的原始力量，讓它具備拉車或耕田的能力」
- **實例**：Claude Opus 4.6 透過網頁 = 博學對話者；透過 Claude Code = 能自主編寫、測試軟體數小時
- **案例**：Mollick 僅提供想法，Claude Code 一小時內自主完成：排版 GPT-1 參數成 80 本書 → 設計封面 → 架設網站 → 串接 Stripe 金流

### 4. 避開效能陷阱
- 免費模型為「聊天速度」優化，非「準確性」
- 「自動 (Auto)」模式會偷切到較弱模型
- **專業做法**：
  - 手動切換至 GPT-5.2 Thinking Extended 或 Gemini 3 Pro/Thinking
  - Claude 選擇 Opus 4.6 並開啟「進階思維 (extended thinking)」

### 5. 心態轉型：從 Prompting 到 Managing
- 不再精雕細琢 prompt
- 像管理「能力極強但不可預測」的初階員工
- 責任：設定清晰目標 → 提供真實複雜任務 → 看 AI 拆解執行 → 糾正引導

### 6. 2026 年工具推薦
| 工具 | 用途 | 特點 |
|------|------|------|
| **Claude Code / OpenAI Codex** | 開發者代理 | 自主建置與修復系統，改變軟體工程型態 |
| **Claude Cowork** | 非技術知識工作 | 強隔離虛擬機環境，自動操作電腦 |
| **Claude for Excel/PowerPoint** | 專業分析 | 直接在軟體內擔任初級分析師 |
| **NotebookLM** | 大量資訊理解 | AI Podcast 可中途打斷提問 |
| **Gemini 多媒體** | 圖片/影片生成 | nano banana pro + Veo 3.1 |
| **OpenClaw** | 開源本機代理 | 高風險，僅供技術參考 |

## 💬 金句摘錄
> "AI 工作套件 (Harness) 就像馬具一樣，它能擷取馬匹的原始力量，並讓它具備拉車或耕田的能力。"
> — Ethan Mollick

> "AI 開始會做事了，而不只是會說話。"
> — Ethan Mollick

## 🧠 概念連結
- **Agentic AI**：具備自主行動能力的 AI 系統，能使用工具、規劃步驟、執行任務
- **典範轉移**：從「對話模式」跨入「執行模式」
- **數位員工**：將 AI 視為需要管理的員工而非工具

## 💡 與我的連結
- 目前使用 Claude Code 進行開發工作，正是 Mollick 所說的 Harness 應用
- Happy Coder 系統本質上也是一種 Harness，讓 Claude 能透過 Telegram 執行實際系統操作
- 應該更有意識地將任務「指派」而非僅「詢問」

## ✅ 行動項目
- [ ] 檢視目前 AI 使用習慣，是否還停留在「聊天模式」
- [ ] 確保付費方案都手動選擇高階模型，避免自動模式
- [ ] 嘗試將更複雜的任務完整交給 Claude Code 執行
- [ ] 練習以「管理者」角度設定任務目標與驗收標準

## 📝 我的註解與思考
Mollick 這份指南的核心洞見在於：**決定 AI 效能的不只是模型本身，更是「Harness」— 讓 AI 能實際行動的系統框架**。這解釋了為什麼同樣的 Claude 模型，在網頁版和 Claude Code 中表現天差地遠。

對我而言最有啟發的是「管理者心態」的轉變。過去我還是會花很多時間調整 prompt，但更有效的方式是：給予清晰目標、提供完整上下文（SOP、規格文件等），然後讓 AI 自己拆解執行。這就像帶新人一樣，與其告訴他每個步驟怎麼做，不如說清楚目標讓他自己想辦法。

另一個值得注意的是付費方案的必要性。免費模型的「優化方向」根本不是為嚴肅工作設計的，這是很多人對 AI 印象不佳的原因。每月 20 美金的投資，換來的是「選擇權」— 能手動選擇真正強大的模型。

## 🎬 延伸學習 - YouTube
- [Ethan Mollick 相關演講](https://www.youtube.com/@ethanmollick)
- [AI Agent 概念介紹](https://www.youtube.com/results?search_query=AI+Agent+2026)

## 🔗 延伸閱讀
- [Ethan Mollick Substack - One Useful Thing](https://www.oneusefulthing.org/)
- [Claude Code 官方文件](https://docs.anthropic.com/claude-code)
- [OpenAI Codex 介紹](https://openai.com/codex)

## ℹ️ 原文資訊
- **原始輸入**：[查看原始資料](../../raw/2026-03/2026-03-01-091736-text.txt)
- **來源連結**：A Guide to Which AI to Use in the Agentic Era - Ethan Mollick
- **收錄時間**：2026-03-01 09:17:36
