# 任務：編譯「AI Agent 架構與實戰」知識 Wiki 頁

你是 SecondBrain 知識編譯器。以下是「AI Agent 架構與實戰」主題下的 54 篇筆記摘要。
主題描述：AI Agent 設計模式、多代理協作、OpenClaw/DesignClaw/MetaClaw 等框架

## 要求

請根據以下筆記內容，產出一篇結構化的知識 Wiki 頁，格式如下：

```
---
title: "AI Agent 架構與實戰 — 知識 Wiki"
date: 2026-04-23
type: wiki
content_layer: L3
topic: ai-agent
source_count: 54
last_compiled: 2026-04-23
_skip_sync: true
---

# {主題名稱} — 知識 Wiki

## 主題概述
(2-3 段，概括此主題的核心範圍、為何重要、目前發展階段)

## 核心概念
(列出 5-10 個核心概念，每個用 ### 小節，2-3 句說明 + Wiki Link 引用來源筆記)

## 關鍵發現
(從筆記中提煉的重要洞見，每條用 > blockquote + 來源 Wiki Link)

## 跨筆記關聯
(不同筆記之間的連結、矛盾、演進關係)

## 待探索方向
(筆記中提到但尚未深入的議題，供未來研究)
```

## 引用規則

- 每個段落都必須用 `[[note-filename]]` 或 `[[note-filename|顯示名稱]]` Wiki Link 引用來源筆記
- filename 就是下方每篇筆記的 `filename` 欄位（不含 .md）
- 不要虛構不存在的筆記名稱

---

## 筆記清單（共 54 篇）

### [1/54] Hermes Agent × Telegram × LLM Wiki — AI 補助案助手架構分析與機會研究
- **filename**: `2026-04-18_Hermes-Agent-AI補助案助手架構分析與機會研究`
- **path**: `dispatch-outputs/2026-04-18_Hermes-Agent-AI補助案助手架構分析與機會研究.md`
- **date**: 2026-04-18
- **category**: tool-analysis
- **tags**: Hermes-Agent, Telegram, LLM-Wiki, ChatGPT, government-grants, SBIR, SIIR, CITD, AI-agent, automation, business-opportunity

**內容摘要：**

## 原始貼文摘要

一位計劃輔導顧問分享了他用「Hermes Agent × Telegram × LLM Wiki × ChatGPT」串起來的 AI 計劃書助手：

1. 每天定期巡查相關網站，追最新補助公告，下載相關資料
2. 根據下載的申請須知，自動產生訪綱與索資清單
3. 針對特定計劃內容做即時問答，不用再翻 PDF
4. 具備長短期記憶，知道目前在處理哪一案、哪個計劃、還缺什麼資料

定位：第一個能協助計劃輔導顧問工作的「AI 員工」。

---

## Part 1：系統架構分析

### 各元件角色

**Hermes Agent**（Nous Research 開源框架）
- GitHub 95.6K+ stars 的開源 AI Agent 框架
- 內建 Cron 排程（定時巡查網站）、Telegram Bot 整合、40+ 工具
- 支援 Function Calling，可串接各種 API
- 在此系統中扮演「排程引擎 + 任務調度器」角色
- 官方：https://github.com/NousResearch/Hermes-Function-Calling
(...截斷)

---

### [2/54] Better Agent Terminal：統一 CLI Agent 調度中心可行性分析
- **filename**: `2026-04-09_Better-Agent-Terminal統一CLI調度中心分析`
- **path**: `dispatch-outputs/2026-04-09_Better-Agent-Terminal統一CLI調度中心分析.md`
- **date**: 2026-04-09
- **category**: tech/tools
- **tags**: CLI, agent-terminal, Claude-Code, Codex, Gemini-CLI, electron, xterm, multi-agent, dispatch

**內容摘要：**

## 專案概覽

Better Agent Terminal (BAT) 是一個 Electron 桌面終端聚合器，讓你在同一個視窗管理多個 AI Agent CLI。技術棧：React 18 + xterm.js + node-pty，Google Meet 風格的 70/30 主面板 + 縮圖列佈局。

### 已內建的 Agent Preset

- Claude Code (`claude`)
- Gemini CLI (`gemini`)
- OpenAI Codex (`codex`)
- GitHub Copilot (`gh copilot`)
- Aider (`aider`)
- 支援自訂新 Agent

### 核心功能

1. **多終端管理**：每個 Agent 一個獨立 PTY，可同時運行
2. **工作區管理**：支援不同專案切不同工作區
3. **快捷切換**：主視窗 + 縮圖預覽，一鍵切 Agent
4. **統一配置**：所有 Agent 的啟動指令集中管理

---

## 作為統一調度中心的可行性評估

### ✅ 已具備

- 多 Agent 
(...截斷)

---

### [3/54] gemgate × BAT × Copilot：統一 CLI Agent 調度中心完整實作指南
- **filename**: `2026-04-09_gemgate-BAT-Copilot整合實作指南`
- **path**: `dispatch-outputs/2026-04-09_gemgate-BAT-Copilot整合實作指南.md`
- **date**: 2026-04-09
- **category**: tech/architecture
- **tags**: gemgate, BAT, better-agent-terminal, copilot, CLI, agent-dispatch, architecture, implementation

**內容摘要：**

## 核心架構：gemgate 是大腦，BAT 是身體

```
┌─────────────────────────────────────────────────┐
│  Better Agent Terminal (BAT) — UI Shell          │
│  React 18 + xterm.js + node-pty                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│  │ Claude   │ │ Copilot  │ │ Gemini   │  ...    │
│  │ Terminal │ │ Terminal │ │ Terminal │        │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘        │
│       │            │            │               │
│  ─────┴────────────┴────────────┴───────        │

(...截斷)

---

### [4/54] DesignClaw 危老都更輕資產商業模式架構
- **filename**: `2026-04-06_DesignClaw危老都更輕資產商業模式`
- **path**: `dispatch-outputs/2026-04-06_DesignClaw危老都更輕資產商業模式.md`
- **date**: 2026-04-06
- **category**: business-model
- **tags**: DesignClaw, 危老重建, 都更, 室內設計, AI, 全屋定制, 輕資產, MEDVi

**內容摘要：**

## 背景：從 MEDVi 模式到 DesignClaw

MEDVi 是一家只有 2 人的美國遠距醫療公司，2025 年銷售額 $401M，靠 AI + 模組化外包做到極致輕資產。創辦人 Matthew Gallagher 用 $20,000 在 2 個月內從零到上線，所有後端（醫師網路、藥局、物流）全部外包，自己只做品牌前端和 AI 驅動的獲客。

DesignClaw 要套用同樣的框架，切入台灣危老都更的室內裝修設計市場，結合大陸全屋定制供應鏈。

## 一、市場機會（時間窗口分析）

### 供需缺口 = MEDVi 的「GLP-1 短缺」

- 全台屋齡超過 30 年住宅突破 500 萬戶
- 2024 年危老都更核准累計破 5,172 件，政府加速推動 8,216 棟 6 層以上老屋改建（約 27 萬戶）
- 2026 年裝修年產值預估上看 5,500 億台幣
- 室內設計師嚴重不足，傳統設計流程慢（量屋→出圖→來回修改→施工），一個設計師同時能接的案有限

### 結構性利多：輕硬裝＋重軟裝趨勢

- 2026 年台灣設計趨勢核心：「輕硬裝、重軟裝」
- 硬裝簡化標準化 
(...截斷)

---

### [5/54] Discord 作為 AI Agent 控制台的選型分析
- **filename**: `2026-04-06_Discord作為AI-Agent控制台分析`
- **path**: `dispatch-outputs/2026-04-06_Discord作為AI-Agent控制台分析.md`
- **date**: 2026-04-06
- **category**: tech-analysis
- **tags**: Discord, OpenClaw, AI-agent, 龍蝦, multi-agent, Claude-Code-Channels, Telegram

**內容摘要：**

## 背景

一位重度 OpenClaw（龍蝦）使用者分享了三個月的使用心得，API 花費累積超過 $1,500 USD。從 Telegram → Line → Telegram → WebChat，最終全部搬到 Discord。核心發現：模型聰不聰明是一回事，介面怎麼管理 Session 才是決定能不能多工作業的關鍵。

## 一、社群工具選型比較

### Telegram

- 適合「單兵快速指令」，手機上丟一句話讓龍蝦去跑
- Claude Code Channels 官方支援，設定最簡單
- 缺點：單線程對話，無法平行追蹤多任務
- 定位：一對一、輕量指令、行動優先

### Line

- 基本不適合 AI agent 使用
- API 限制多、Bot 生態封閉、無 thread 概念、群組功能弱
- 不建議使用

### Discord（最佳解）

- 天生三層結構：Server → Channel → Thread
- 每一層都可獨立承載一個 agent session
- 支援多 bot 在同一 channel 互相讀訊息
- 定位：多 agent 控制台、長期任務追
(...截斷)

---

### [6/54] ComfyUI 室內設計渲染技術規劃
- **filename**: `2026-04-04_ComfyUI室內設計渲染技術規劃`
- **path**: `dispatch-outputs/2026-04-04_ComfyUI室內設計渲染技術規劃.md`
- **date**: 2026-04-04
- **category**: tech/ai-ml
- **tags**: ComfyUI, Stable-Diffusion, SDXL, ControlNet, 室內設計, AI渲染, DesignClaw, IP-Adapter, LoRA, prompt-engineering

**內容摘要：**

# ComfyUI 室內設計渲染技術規劃

**DesignClaw Render Agent 整合方案**
**硬體環境：** NVIDIA RTX 3090 (24GB VRAM)
**日期：** 2026-04-04

---

## 摘要

本文件規劃 DesignClaw 自動化管線中 Render Agent 的技術實作方案，以 ComfyUI 作為核心渲染引擎，整合 SDXL base model、Dual ControlNet（floor plan 空間約束）、IP-Adapter（風格遷移）和日式簡約風格 prompt engineering，在 RTX 3090 24GB VRAM 環境下實現 6 房間批量渲染（預估 3.5–5 分鐘），輸出至少 1024×1024 的寫實室內設計渲染圖。

---

## 1. 最適合室內設計的 Model 組合

### 1.1 Base Model 選擇：SDXL vs Flux vs SD 1.5

| 特性 | SD 1.5 | SDXL | Flux.1-dev |
|------|--------|------|---
(...截斷)

---

### [7/54] DesignClaw ComfyUI 整合架構
- **filename**: `2026-04-04_DesignClaw-ComfyUI整合架構`
- **path**: `dispatch-outputs/2026-04-04_DesignClaw-ComfyUI整合架構.md`
- **date**: 2026-04-04
- **category**: tech/ai-ml
- **tags**: DesignClaw, ComfyUI, SDXL, ControlNet, Render-Agent, 室內設計, AI渲染

**內容摘要：**

# DesignClaw ComfyUI 整合架構

## 摘要

DesignClaw 的 Render Agent 層已完成實作，透過 ComfyUI REST API + WebSocket 將 SDXL RealVisXL V5.0 整合進室內設計渲染流水線。支援 dual ControlNet（Canny 結構線 + Depth 空間感）與可選的 IP-Adapter 風格轉移，針對六種日式簡約空間類型各自調校 prompt 和參數。目標部署機器為 ac-3090（RTX 3090, 24GB VRAM）。

---

## 1. 完整架構：ComfyUI 整合到 DesignClaw Render Agent

```
DesignClaw Pipeline
───────────────────────────────────────────────────────────
平面圖輸入（JPG/PNG）
    │
    ▼
[Render Agent — render_agent.py]
    │  ├── 載入 workflow template (japanes
(...截斷)

---

### [8/54] DesignClaw 專案進度紀錄（2026-04-03）
- **filename**: `2026-04-03_DesignClaw進度紀錄`
- **path**: `dispatch-outputs/2026-04-03_DesignClaw進度紀錄.md`
- **date**: 2026-04-03
- **category**: work-logs
- **tags**: DesignClaw, AI, interior-design, agent-pipeline, three-js, 3D, render, FastAPI

**內容摘要：**

## 摘要

DesignClaw 是一套 AI 室內設計自動化管線，採 7-Agent Pipeline 架構：Intake → Vision → Layout → Model → Render → Export → Deliver。截至 2026-04-03，Vision Agent V2、Layout Agent、3D Viewer、Dashboard 及日式簡約設計概念皆已完成；目前卡在 Render Agent 的 AI 產圖環節（AI Service Hub 連線問題），Export Agent 與 Deliver Agent 尚未開發。

## 已完成項目

### 1. 專案初始化

designclaw/ 目錄結構已建立於 `~/Desktop/designclaw/`，包含各 agent 模組及測試輸出目錄。

### 2. Vision Agent（V1 → V2）

- V1：實現平面圖辨識功能，但房間位置判斷不準確。
- V2（修正版）：正確辨識出 9 個空間——主臥（左上）、書房（右上）、客廳（中間最大）、廚房（左下）等，輸出為結構化 JSON。

### 
(...截斷)

---

### [9/54] claude-token-efficient — 9 行 CLAUDE.md 減少 63% 輸出 token
- **filename**: `2026-04-03_Claude-Token-Efficient-CLAUDE-md`
- **path**: `dispatch-outputs/2026-04-03_Claude-Token-Efficient-CLAUDE-md.md`
- **date**: 2026-04-03
- **category**: tech/tools
- **tags**: Claude-Code, token優化, CLAUDE.md, prompt工程, 成本控制

**內容摘要：**

# claude-token-efficient — 9 行 CLAUDE.md 減少 63% 輸出 token

## 摘要

drona23/claude-token-efficient 是一個只有 9 行的 CLAUDE.md 檔案，丟進專案根目錄即可生效，透過禁止 Claude Code 的拍馬屁開頭、空洞結尾、重複問題、未被要求的建議等行為，聲稱可減少輸出 token 63%。1,900+ stars。實際效果取決於使用場景，重度使用者（日均 100+ prompt）才有明顯省錢效果。

## 背景

Claude Code 預設行為傾向冗長——每次回覆都帶 "Sure! Great question!" 開頭、"hope this helps!" 結尾、重述使用者問題、加入未被要求的建議。這些行為在單次對話中只是小麻煩，但在重度開發場景下（一天跑上百個 prompt），累積的 token 成本非常可觀。

## 分析內容

### 核心指令（9 行 CLAUDE.md）

```markdown
- Think before acting. Read existing fi
(...截斷)

---

### [10/54] DesignClaw — AI 室內裝修全自動管線系統計畫
- **filename**: `2026-04-03_DesignClaw室內裝修自動化系統計畫`
- **path**: `dispatch-outputs/2026-04-03_DesignClaw室內裝修自動化系統計畫.md`
- **date**: 2026-04-03
- **category**: tech/ai-ml
- **tags**: DesignClaw, 室內設計, OpenCode, MetaClaw, 多代理, BIM, IFC, 自動化管線, AI-Agent

**內容摘要：**

# DesignClaw — AI 室內裝修全自動管線系統計畫

## 一、系統定位

DesignClaw 是一套以 OpenCode Agent 為底層運行時、參考 MetaClaw 自進化架構設計的 AI 室內裝修全自動協作管線。每個設計環節由專屬 Agent 負責，Agent 之間透過事件驅動的訊息系統串接，形成從「手繪草稿」到「施工交付」的端對端自動化流程。

核心理念：**把 MetaClaw 的「Claw」（抓取 → 學習 → 進化）模式套用到室內設計產業的每一個環節。**

---

## 二、架構總覽

### 2.1 三層架構

```
┌─────────────────────────────────────────────────────────┐
│                    Layer 3: 業務層                        │
│  Notion（專案 UI）+ Google Drive（檔案倉庫）+ Web 檢視器   │
└────────────────────────┬───────────────────────
(...截斷)

---

### [11/54] Cisco AI Agent 五步驟 vs 會計三表五步法 — 方法論對照與應用
- **filename**: `2026-04-01_Cisco五步驟vs會計三表五步法對照分析`
- **path**: `dispatch-outputs/2026-04-01_Cisco五步驟vs會計三表五步法對照分析.md`
- **date**: 2026-04-01
- **category**: tech/ai-ml
- **tags**: AI-Agent, Cisco, 方法論, skill, Claude-Code, 框架設計

**內容摘要：**

# Cisco AI Agent 五步驟 vs 會計三表五步法 — 方法論對照與應用

## 摘要

思科首席工程師 Yuri Kramarz 提出的 AI Agent 五步驟框架，與從會計三表案例中歸納的五步法，本質上在解決同一個問題：如何讓 AI 從「偶爾能用」變成「穩定可靠」。兩套方法論高度互補——Cisco 偏向「設計時」的架構規範，會計五步法偏向「執行時」的工作流程。合併使用可以形成完整的 AI Agent 落地方法論。

## 背景

思科官網由首席工程師 Yuri Kramarz 撰寫的文章指出：AI 代理不是更聰明的 AI，而是一套可以被設計、拆解與優化的思考與行動流程。最多人卡關在第二步——劃清邊界。

## 分析內容

### Cisco 五步驟框架

| 步驟 | 核心概念 | 重點 |
|------|---------|------|
| 1. 身份定位 | 給 AI Agent 清晰的功能定位 | 不是擬人化，而是明確目的和判斷標準 |
| 2. 劃清邊界 ⭐ | 定義「不該做什麼」 | **最多人卡關處**——沒有邊界的 AI 會自行擴張任務範疇 |
| 
(...截斷)

---

### [12/54] Claude Code 會計三表案例分析 — AI 落地專業領域的實戰拆解
- **filename**: `2026-04-01_Claude-Code會計三表案例分析`
- **path**: `dispatch-outputs/2026-04-01_Claude-Code會計三表案例分析.md`
- **date**: 2026-04-01
- **category**: tech/ai-ml
- **tags**: Claude-Code, 會計三表, skill, subagent, 紅隊演練, 台灣稅務, vibe-coding

**內容摘要：**

# Claude Code 會計三表案例分析

## 摘要

用 Claude Code 在 3 小時內從散落的 PDF、Excel、銀行對帳單和收據截圖，產出完整的會計三表（損益表、資產負債表、現金流量表），通過會計師查帳。這個案例展示了 AI 落地到專業領域的完整方法論：自建 skill 注入領域知識 → 分輪次處理不同資料源 → 互動式補齊缺失資訊 → subagent 紅隊演練品質把關。

## 背景

連鎖餐飲業加盟主隔天會計要來查帳，需要快速產出會計三表。靈感來自日本稅務師畠山謙人用 Claude Code 一個人服務 60 家顧問公司的案例。

## 分析內容

### 工作流程拆解

整個流程分為五個階段，每個階段都有明確的方法論意義：

#### 階段一：自建領域 Skill（/taiwan-tax）

**做了什麼：** 搜尋 GitHub 沒有現成台灣會計工具，於是自己寫了一個 Claude Code skill，包含：
- 台灣會計科目對應規則
- 含稅未稅轉換公式
- 401 營業稅雙月申報邏輯
- 哪些可以自動化、哪些不能

**方法論意義：** 這是整個案
(...截斷)

---

### [13/54] Claude Code 源碼洩漏分析 — 51.2 萬行 TypeScript 揭示的架構秘密
- **filename**: `2026-03-31_Claude-Code源碼洩漏分析`
- **path**: `dispatch-outputs/2026-03-31_Claude-Code源碼洩漏分析.md`
- **date**: 2026-03-31
- **category**: tech/ai-ml
- **tags**: Claude-Code, Anthropic, 源碼分析, KAIROS, multi-agent, 架構設計

**內容摘要：**

# Claude Code 源碼洩漏分析

## 摘要

Anthropic 的 Claude Code CLI 工具因為 npm 套件中包含了 sourcemap 檔案（cli.js.map），被安全研究員透過逆向工程還原出完整 TypeScript 源碼，共約 1,900 個檔案、512,000 行程式碼。ChinaSiro/claude-code-sourcemap 是其中一個還原版本（v2.1.88）。源碼揭示了多個尚未公開的功能：KAIROS（常駐背景 Agent）、ULTRAPLAN（30 分鐘遠端規劃）、Coordinator 多 Agent 協調模式、Buddy 伴侶 UI、Agent Swarm 等。

## 背景

- **發現時間：** 2026 年 3 月 31 日
- **發現者：** 安全研究員 Chaofan Shou
- **來源：** npm 套件 `@anthropic-ai/claude-code` v2.1.88 中的 `cli.js.map`
- **還原方式：** 提取 sourcemap 的 `sourcesContent` 欄位
- **
(...截斷)

---

### [14/54] MetaClaw 框架分析 — 自進化 AI Agent 整合方案
- **filename**: `2026-03-30_MetaClaw框架分析`
- **path**: `dispatch-outputs/2026-03-30_MetaClaw框架分析.md`
- **date**: 2026-03-30
- **category**: tech/ai-ml
- **tags**: MetaClaw, AI-Agent, RL, 透明代理, vibe-coding, 工具整合

**內容摘要：**

# MetaClaw 框架分析 — 整合與利用方案

> 針對悠識數位現有工具鏈（Claude Code / Cursor / Antigravity）的整合評估

---

## 一、MetaClaw 是什麼

MetaClaw 是北卡羅來納大學 AIMING Lab 開發的開源 AI Agent 框架。核心概念：在你和 LLM 之間插入一個「透明代理」(transparent proxy)，讓 AI Agent 能夠自我進化——你每次跟它互動，它都在學。

最有趣的設計：它會看你的 Google Calendar，發現你在開會時，就自動開始用閒置的運算資源訓練模型。你開會的時間 = AI 進化的時間。

**GitHub:** [aiming-lab/MetaClaw](https://github.com/aiming-lab/MetaClaw)
**論文:** [arXiv:2603.17187](https://arxiv.org/abs/2603.17187)

---

## 二、技術架構

### 2.1 透明代理架構

```
你的工具（Claude Code / C
(...截斷)

---

### [15/54] Claude Code Skills 推薦清單（三層架構）
- **filename**: `2026-03-06-claude-code-skills-推薦清單`
- **path**: `tech/tools/2026-03-06-claude-code-skills-推薦清單.md`
- **date**: 2026-03-06
- **category**: tech/tools
- **tags**: claude-code, skills, ai-tools, productivity, automation

**內容摘要：**

# Claude Code Skills 推薦清單（三層架構）

## 📊 元資訊
- **難度**：⭐⭐
- **來源類型**：文章 / 資源清單
- **作者**：BrowserAct
- **筆記時間**：2026-03-06 11:04

## 📌 摘要
整理 Claude Code Skills 的三層推薦架構，從官方必裝的文件處理 Skills，到進階實用工具，最後是最具影響力的 Skill Creator 和 Superpowers。這份清單幫助使用者系統化地建立 Claude Code 的能力擴展。

## 🏷️ 標籤分類
- **大分類**：tech
- **小分類**：tools

## 🔑 關鍵要點
1. **Layer 1（必裝）**：Anthropic 官方四件套 — PDF、DOCX、PPTX、XLSX 文件處理
2. **Layer 2（進階）**：前端設計、SEO、行銷、Obsidian 整合等專業領域 Skills
3. **Layer 3（核心）**：Skill Creator（自建 Skill）+ Superpowers（需求分析優先）
4. 作者
(...截斷)

---

### [16/54] OpenClaw 實戰書籍目錄（第三部分）- Canvas、Twilio 語音與附錄
- **filename**: `2026-03-06-openclaw-book-toc-part3`
- **path**: `tech/tools/2026-03-06-openclaw-book-toc-part3.md`
- **date**: 2026-03-06
- **category**: tech/tools
- **tags**: OpenClaw, AI Agent, Canvas, Twilio, Voice Call, CLI, TUI, 設定檔

**內容摘要：**

# OpenClaw 實戰書籍目錄（第三部分）- Canvas、Twilio 語音與附錄

## 📊 元資訊
- **難度**：⭐⭐⭐
- **來源類型**：書籍目錄
- **作者**：Alan Chen
- **筆記時間**：2026-03-06 10:14

## 📌 摘要
OpenClaw 實戰書籍的後半部分，包含第十章的 Canvas 互動內容、第十一章的 Twilio 語音通話整合，以及三個完整的附錄：CLI 指令大全、TUI 斜線指令大全、openclaw.json 設定大全。

## 🏷️ 標籤分類
- **大分類**：tech
- **小分類**：tools

## 🔑 關鍵要點

### 第十章後半：Canvas 互動功能
1. **Canvas 基礎**：理解 Canvas 是什麼、如何啟用
2. **實戰應用**：天氣圖表、互動式倒數計時器
3. **Talk Mode**：語音與 Agent 對話模式

### 第十一章：Twilio 語音通話
1. **Twilio 註冊流程**：帳號建立、電話驗證、Trial 方案
2. **Onboarding 設定**：
(...截斷)

---

### [17/54] Jensen Huang Morgan Stanley TMT 科技大會演講重點
- **filename**: `2026-03-06-jensen-huang-morgan-stanley-tmt`
- **path**: `tech/ai-ml/2026-03-06-jensen-huang-morgan-stanley-tmt.md`
- **date**: 2026-03-06
- **category**: tech/ai-ml
- **tags**: NVIDIA, Jensen Huang, AI Agent, 運算經濟學, 物理AI, GPU, Token經濟

**內容摘要：**

# Jensen Huang Morgan Stanley TMT 科技大會演講重點

## 📊 元資訊
- **難度**：⭐⭐⭐
- **來源類型**：科技大會演講
- **作者**：Jensen Huang (NVIDIA 執行長)
- **筆記時間**：2026-03-06 11:00

## 📌 摘要
NVIDIA 執行長黃仁勳在 Morgan Stanley TMT 科技大會上闡述 AI 產業的三次拐點（生成式 AI → 推理 → Agent），並提出「運算等於營收」的核心觀點。他預測軟體產業將從工具授權轉型為 Token 服務，同時揭示物理 AI 將是下一個十年的前沿領域。

## 🏷️ 標籤分類
- **大分類**：tech
- **小分類**：ai-ml

## 🔑 關鍵要點

### AI 三次拐點
1. **生成式 AI**：ChatGPT 讓 GPT-3 變得易用，開啟 AI 普及化
2. **推理能力**：o1 帶來自我反思和修正能力，運算量增加 1000 倍
3. **AI Agent**：提示詞從「查詢」變成「行動」，Token 消耗量再增 100 萬倍


(...截斷)

---

### [18/54] 玩爆你的龍蝦 — 最強 OpenClaw 安裝設定應用實機演練
- **filename**: `2026-03-06-玩爆你的龍蝦-OpenClaw安裝設定應用實機演練`
- **path**: `tech/ai-ml/2026-03-06-玩爆你的龍蝦-OpenClaw安裝設定應用實機演練.md`
- **date**: 2026-03-06
- **category**: tech/ai-ml
- **tags**: OpenClaw, AI Agent, 技術書籍, 台灣原創, LINE Bot, Telegram, 多機協作

**內容摘要：**

# 玩爆你的龍蝦 — 最強 OpenClaw 安裝設定應用實機演練

## 📊 元資訊
- **難度**：⭐⭐⭐
- **來源類型**：新書預購公告
- **作者**：Alan Chen（本人）
- **筆記時間**：2026-03-06 10:11

## 📌 摘要
中文第一本 OpenClaw（龍蝦）專書在天瓏開始預購！從龍蝦發布到成書僅花 14 天，涵蓋完整安裝設定、LINE/Telegram 整合、多機協作 Nodes 架構等實戰內容。

## 🏷️ 標籤分類
- **大分類**：tech
- **小分類**：ai-ml

## 🔑 關鍵要點
1. **中文第一本 OpenClaw 專書**：填補繁體中文市場空白
2. **14 天閃電寫作**：從工具發布到成書的超高效率
3. **LINE 完整設定**：最多人詢問的整合教學
4. **多機協作 Nodes**：控制其他電腦、手機、平板的進階功能
5. **五章完整架構**：從概念理解到正式域名部署

## 💬 金句摘錄
> "從龍蝦一出來，馬上安裝在 Linux 中，然後第二天立即訂了 Mac Mini，第三天規劃書籍，第四
(...截斷)

---

### [19/54] SEO 行銷人用 Claude Code 工作流實戰
- **filename**: `2026-03-04-SEO行銷人用Claude-Code工作流實戰`
- **path**: `tech/tools/2026-03-04-SEO行銷人用Claude-Code工作流實戰.md`
- **date**: 2026-03-04
- **category**: tech/tools
- **tags**: Claude-Code, SEO, 行銷自動化, AI工作流, Firecrawl, 內容行銷

**內容摘要：**

# SEO 行銷人用 Claude Code 工作流實戰

## 📊 元資訊
- **難度**：⭐⭐⭐
- **來源類型**：部落格文章
- **作者**：Hiba Fathima（Firecrawl SEO 主管）
- **筆記時間**：2026-03-04 08:49

## 📌 摘要
Firecrawl 的 SEO 主管 Hiba Fathima 分享她如何用 Claude Code（包含 Desktop 版本）處理大部分行銷工作。核心觀點是：這不能取代工程師，但能消除「等別人排程」的問題，讓行銷人自己快速上線各種小工具和自動化流程。

## 🏷️ 標籤分類
- **大分類**：tech
- **小分類**：tools

## 🔑 關鍵要點

### Claude Code 的核心價值
1. **消除依賴等待**：以前活動頁面流程「設計師→工程師→驗收→修改」，現在想清楚就能直接上線
2. **專案級存取**：Claude Code 住在專案裡，能讀取整個目錄、跨檔案修改、執行指令
3. **非技術人員友善**：可用 Desktop App，拖拉截圖、貼圖片，不需面對終端機

#
(...截斷)

---

### [20/54] OpenClaw Agent 省錢實戰：三個玩家的第一線經驗
- **filename**: `2026-03-04-openclaw-agent-實戰經驗`
- **path**: `tech/ai-ml/2026-03-04-openclaw-agent-實戰經驗.md`
- **date**: 2026-03-04
- **category**: tech/ai-ml
- **tags**: OpenClaw, AI Agent, Heartbeat Protocol, OpenHome, SaaS, Mac Mini, Raspberry Pi

**內容摘要：**

# OpenClaw Agent 省錢實戰：三個玩家的第一線經驗

## 📊 元資訊
- **難度**：⭐⭐⭐
- **來源類型**：Podcast 節目整理
- **原節目**：This Week in Startups (TWIST)
- **主持人**：Jason Calacanis、Lon Harris
- **筆記時間**：2026-03-04 14:22

## 📌 摘要
三位 OpenClaw 玩家分享實戰經驗：非工程師用 Mac Mini 比雲端更易上手、Heartbeat Protocol 取代 Agile 站會、OpenHome 把 Agent 帶入智慧音箱、SaaS 定價模式正被 Agent 顛覆。

## 🏷️ 標籤分類
- **大分類**：tech
- **小分類**：ai-ml

## 🔑 關鍵要點

### 1. 本地硬體勝過雲端（給非工程師）
- Jordy Coltman 花了 80 小時和 $800 踩坑後的結論
- Mac Mini 能看到畫面、截圖 debug，體驗遠勝 AWS EC2 + Linux 終端機
- 「看不到在幹嘛」的焦慮感是真實的
(...截斷)

---

### [21/54] 行銷人使用 Claude Code 實戰指南
- **filename**: `2026-03-04-行銷人使用claude-code實戰指南`
- **path**: `tech/ai-ml/2026-03-04-行銷人使用claude-code實戰指南.md`
- **date**: 2026-03-04
- **category**: tech/ai-ml
- **tags**: Claude Code, AI工具, 行銷自動化, 非工程師, 人機協作

**內容摘要：**

# 行銷人使用 Claude Code 實戰指南

## 📊 元資訊
- **難度**：⭐⭐
- **來源類型**：文章/心得分享
- **作者**：未知（行銷從業者）
- **筆記時間**：2026-03-04 08:52

## 📌 摘要
這是一篇針對非工程師背景的行銷人員，如何有效使用 Claude Code 的實戰指南。強調不需要精通程式碼，但需要理解基礎概念，並保持「人在迴路中」(Human-in-the-loop) 的工作模式。

## 🏷️ 標籤分類
- **大分類**：tech
- **小分類**：ai-ml

## 🔑 關鍵要點
1. **懂基礎不代表要會寫程式**：了解 HTML/CSS/JS 的角色、框架基礎、SEO 原理、部署概念
2. **Human-in-the-loop 原則**：AI 做苦差事（草稿、數據整理），人負責品牌語氣、策略決策、編輯判斷、創意方向
3. **請工程師把關**：涉及產品或面向用戶的改動，發布前必須請工程師 review
4. **自動化重複性工作**：定期報表、整理試算表、檢查排名等崩潰日常可以交給 AI
5. **誠實面對缺點*
(...截斷)

---

### [22/54] Claude Code Remote Control — 手機遠端操控 AI Coding Agent
- **filename**: `2026-03-01-claude-code-remote-control`
- **path**: `tech/tools/2026-03-01-claude-code-remote-control.md`
- **date**: 2026-03-01
- **category**: tech/tools
- **tags**: Claude, Claude Code, Anthropic, AI Agent, Remote Control, 開發工具

**內容摘要：**

# Claude Code Remote Control — 手機遠端操控 AI Coding Agent

## 📊 元資訊
- **難度**：⭐⭐
- **來源類型**：新聞/產品更新
- **作者**：未知
- **筆記時間**：2026-03-01 09:01

## 📌 摘要
Claude Code 推出 Remote Control 功能，讓使用者可以透過手機或瀏覽器遠端操控 CLI session。這解決了 AI coding agent 必須綁在終端機前的痛點，使用場景從桌面擴展到任何有手機的地方。

## 🏷️ 標籤分類
- **大分類**：tech
- **小分類**：tools

## 🔑 關鍵要點
1. **Remote Control 啟用方式**：在終端機輸入 `claude rc`，手機或瀏覽器即可接手 session
2. **端對端加密**：Anthropic 完全看不到使用者程式碼，滿足企業安全需求
3. **自動重連機制**：筆電闔上、網路斷線，session 不會中斷，恢復後自動接上
4. **多 session 支援**：手機 app 上可同時
(...截斷)

---

### [23/54] AI Skill 時代來臨：律師實務應用案例
- **filename**: `2026-03-01-AI-skill-時代來臨-律師實務應用案例`
- **path**: `tech/ai-ml/2026-03-01-AI-skill-時代來臨-律師實務應用案例.md`
- **date**: 2026-03-01
- **category**: tech/ai-ml
- **tags**: AI應用, Skill, Agent, 法律科技, Claude, 專業服務, 判斷力, 通用AI

**內容摘要：**

# AI Skill 時代來臨：律師實務應用案例

## 📊 元資訊
- **難度**：⭐⭐⭐⭐
- **來源類型**：文章/心得分析
- **作者**：轉述者分析 + Zack Shapiro（小型律師事務所共同創辦人）
- **筆記時間**：2026-03-01 08:33

## 📌 摘要
2026 年 AI 應用的核心已從「Prompt」轉向「Skill」。Skill 是可系統化迭代的知識封裝，驅動 Agent 分工協作。律師 Zack Shapiro 分享如何用通用型 AI（Claude）而非專門法律 AI 產品，以兩人精品事務所的規模對抗大型律所，關鍵在於將個人十年實務判斷力編碼為 AI 技能。

## 🏷️ 標籤分類
- **大分類**：tech
- **小分類**：ai-ml

## 🔑 關鍵要點
1. **從 Prompt 到 Skill**：2026 年 AI 顯學不再是 prompt，而是可被系統化迭代更新的 Skill
2. **Skill 驅動 Agent**：Agent 之所以有別，主要因為掌握的 Skill 不同（發想/撰寫/校驗）
3. **人類角色轉變
(...截斷)

---

### [24/54] Ethan Mollick 代理時代 AI 使用指南
- **filename**: `2026-03-01-ethan-mollick-agentic-era-ai-guide`
- **path**: `tech/ai-ml/2026-03-01-ethan-mollick-agentic-era-ai-guide.md`
- **date**: 2026-03-01
- **category**: tech/ai-ml
- **tags**: AI Agent, Claude, GPT, Gemini, 工作效率, 典範轉移

**內容摘要：**

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
|------|------|--
(...截斷)

---

### [25/54] AI Agent 正在變成基礎設施：六大發展路線分析
- **filename**: `2026-03-01-ai-agent-infrastructure-trend`
- **path**: `tech/ai-ml/2026-03-01-ai-agent-infrastructure-trend.md`
- **date**: 2026-03-01
- **category**: tech/ai-ml
- **tags**: AI Agent, 基礎設施, Multi-Agent, Coding Agent, Agent OS, 趨勢分析

**內容摘要：**

# AI Agent 正在變成基礎設施：六大發展路線分析

## 📊 元資訊
- **難度**：⭐⭐⭐⭐
- **來源類型**：產業趨勢分析文章
- **作者**：未知（產業觀察者）
- **筆記時間**：2026-03-01 09:22

## 📌 摘要
這篇文章系統性地整理了近期 AI Agent 的發展趨勢，歸納出六條清晰的發展路線。作者認為 Agent 正在從單點功能演進為「工作系統」，最終將成為基礎設施層級的存在。這是一篇非常有價值的產業地圖式分析。

## 🏷️ 標籤分類
- **大分類**：tech
- **小分類**：ai-ml

## 🔑 關鍵要點

### 六大發展路線

1. **瀏覽器與 IDE 成為 Agent 的身體**
   - Google Auto Browse 整合進 Chrome
   - Apple 將 Claude Agent SDK 整合進 Xcode
   - IDE 從編輯器變成「agent-native 開發環境」

2. **Agent 管理平台出現（Agent OS 雛形）**
   - OpenAI Frontier 涵蓋：sha
(...截斷)

---

### [26/54] WFGY RAG 16 問題清單 - 語義防火牆診斷框架
- **filename**: `2026-03-01-WFGY-RAG-16問題清單`
- **path**: `tech/ai-ml/2026-03-01-WFGY-RAG-16問題清單.md`
- **date**: 2026-03-01
- **category**: tech/ai-ml
- **tags**: RAG, LLM, 除錯, Agent, 語義防火牆, 向量資料庫, 幻覺問題

**內容摘要：**

# WFGY RAG 16 問題清單 - 語義防火牆診斷框架

## 📊 元資訊
- **難度**：⭐⭐⭐⭐
- **來源類型**：開源專案 / 技術文件
- **作者**：阿紫BigBig (onestardao)
- **授權**：MIT License
- **GitHub Stars**：1.5k+
- **筆記時間**：2026-03-01 09:09

## 📌 摘要
WFGY Problem Map 是一份開源的 RAG/Agent 系統診斷框架，定義了 16 種可重現的 AI 故障模式及其修復方法。核心概念是「語義防火牆」(Semantic Firewall)——在生成輸出之前檢查系統狀態，而非在輸出後打補丁。這份清單已被 RAGFlow、LlamaIndex、哈佛 MIMS Lab 等主流框架和學術單位收錄。

## 🏷️ 標籤分類
- **大分類**：tech
- **小分類**：ai-ml
- **應用場景**：RAG 系統、Agent 開發、LLM 應用除錯

## 🔑 關鍵要點

### 核心理念：語義防火牆
1. **傳統方式**：輸出後偵測錯誤 → 手動打
(...截斷)

---

### [27/54] Everything Claude Code - Anthropic Hackathon 獲勝專案
- **filename**: `everything-claude-code`
- **path**: `tech/ai-ml/everything-claude-code.md`
- **date**: 2026-02-06
- **category**: tech/ai-ml
- **tags**: claude, anthropic, hackathon, claude-code, skills, agents

**內容摘要：**

# Everything Claude Code - Anthropic Hackathon 獲勝專案

## 摘要

這是一個在 Anthropic x Forum Ventures Hackathon (NYC) 中獲勝的開源專案，包含完整的 Claude Code 配置集合。作者團隊在 8 小時內用 Claude Code 建立了 zenith.chat，贏得 $15,000 API credits。

## 專案資訊

- **GitHub**: https://github.com/affaan-m/everything-claude-code
- **作者**: Affaan Mustafa 和團隊
- **授權**: MIT License
- **Hackathon**: Anthropic x Forum Ventures (NYC)
- **獎勵**: $15,000 API credits
- **成就**: 8 小時內建立 zenith.chat

## 專案規模

經過 10+ 個月密集日常使用驗證：

- **15+ agents**（專業代理）
- **3
(...截斷)

---

### [28/54] OpenClaw 與 AI Agent 新時代:從寫程式到定義規章的典範轉移
- **filename**: `2026-02-06-OpenClaw-AI-Agent-新時代思考`
- **path**: `tech/ai-ml/2026-02-06-OpenClaw-AI-Agent-新時代思考.md`
- **date**: 2026-02-06
- **category**: tech/ai-ml
- **tags**: OpenClaw, AI-Agent, 第一性原理, MECE, 系統工程, 硬體需求

**內容摘要：**

# OpenClaw 與 AI Agent 新時代:從寫程式到定義規章的典範轉移

## 📊 元資訊
- **難度**:⭐⭐⭐⭐
- **來源類型**:個人洞察
- **作者**:Alan Chen
- **筆記時間**:2026-02-06 20:19

## 📌 摘要
OpenClaw 的出現標誌著我們從「寫程式」時代進入「定義規章」時代。真正的核心戰場不再是程式碼,而是在 agents.md 與 skills.md 這兩份檔案中定義 AI Agent 的行為規章、權限邊界與應變邏輯。這是一場從程式設計師到系統工程師的身份轉變。

## 🏷️ 標籤分類
- **大分類**:tech
- **小分類**:ai-ml
- **關鍵概念**:AI Agent、第一性原理、MECE、系統工程

## 🔑 關鍵要點

### 1. 數位樂高:程式碼的「極小化」
- OpenClaw 的架構將本機程式碼需求縮減到極致
- 戰場轉移:從 Debug 轉向設計產品邏輯藍圖
- **核心轉變**:不再是「刻」功能,而是「定義」章程
- 兩大關鍵檔案:**agents.md** 與 **skills.
(...截斷)

---

### [29/54] SHC 對 OpenAI API 不同版本模型的相容性問題
- **filename**: `shc-openai-api-compatibility`
- **path**: `tech/devops/shc-openai-api-compatibility.md`
- **date**: 2026-02-02
- **category**: tech/devops
- **tags**: SHC, OpenAI, API, GPT-5, 相容性

**內容摘要：**

# SHC 對 OpenAI API 不同版本模型的相容性問題

## 問題摘要

SHC (Super Happy Coder) 可以正常使用 GPT-4.1-nano，但無法使用 GPT-5 mini，原因是 OpenAI 在 GPT-5 系列變更了 API 參數規格，而 SHC 程式碼使用舊版參數。

## 關鍵發現

### OpenAI API 參數演變

| 特性 | GPT-4 系列 (含 4.1-nano) | GPT-5 系列 (含 5-mini) |
|------|------------------------|---------------------|
| **Token 限制參數** | `max_tokens` ✅ | `max_completion_tokens` ✅<br>`max_tokens` ❌ |
| **Temperature 範圍** | 0.0-2.0 可調整 | 固定 1.0（不可設定） |
| **向下相容** | 支援舊參數 | 不支援舊參數 |

### 錯誤訊息

當使用 `max_tokens` 參數呼叫 GPT-5 min
(...截斷)

---

### [30/54] SHC 功能配置與測試進度報告
- **filename**: `2026-01-31-SHC-功能配置與測試進度報告`
- **path**: `tech/2026-01-31-SHC-功能配置與測試進度報告.md`
- **date**: 2026-01-31
- **category**: tech
- **tags**: Super Happy Coder, 測試進度, Phase 6, 配置, 功能驗證

**內容摘要：**

# SHC 功能配置與測試進度報告

## 執行摘要

完成 **Phase 6 Compute Plane 完整測試**,通過率 **87.5% (7/8)**。確認 3090 GPU 所有核心 API 正常,外部 API 配置為 **OpenAI gpt-4.1-nano**。系統已就緒進入混合模式測試與 SHC Proxy 整合階段。

---

## 一、已完成任務

### ✅ 1. Qwen 模型下載完成狀態檢查

**結果**: ✅ 完成
**檔案數**: 4 個 safetensors 檔案
**位置**: `~/.cache/huggingface/hub/models--Qwen--Qwen2.5-7B-Instruct/`

**服務狀態**:
- vllm.service: ✅ active (running), PID 145399
- compute-plane.service: ✅ active (running), PID 145933
- 運行時間: 18+ 小時無中斷

**vLLM 配置**:
```bash
Model: Qwen/Qwen2.5
(...截斷)

---

### [31/54] SHC Phase 6 Compute Plane 測試報告
- **filename**: `2026-01-31-SHC-Phase6-Compute-Plane-測試報告`
- **path**: `tech/2026-01-31-SHC-Phase6-Compute-Plane-測試報告.md`
- **date**: 2026-01-31
- **category**: tech
- **tags**: Super Happy Coder, Phase 6, Compute Plane, 3090, 測試報告

**內容摘要：**

# SHC Phase 6 Compute Plane 測試報告

## 摘要

Phase 6 Compute Plane 測試已完成,**87.5% 通過率 (7/8)**。3090 GPU 所有主要 API 均正常運作,包括 LLM 推理、Embedding、Rerank、Toolchain 和 GPU 監控。

---

## 一、測試概覽

**測試時間**: 2026-01-31 12:45-12:50
**測試環境**: ac-mac → SSH Tunnel (localhost:9000) → ac-3090:9000
**認證方式**: Bearer Token (shc-compute-2026)

| 指標 | 數據 |
|------|------|
| 總測試數 | 8 項 |
| 通過 | 7 項 (87.5%) |
| 失敗 | 1 項 (12.5%) |
| 跳過 | 0 項 |

---

## 二、測試結果詳情

### ✅ 通過測試 (7 項)

#### 1. test_p6_01_gpu_health - GPU 健康檢查
**狀態**: ✅
(...截斷)

---

### [32/54] Claude Code Agent 完整設定 - CLAUDE.md 與 Skills
- **filename**: `2026-01-31-claude-code-agent-setup`
- **path**: `tech/2026-01-31-claude-code-agent-setup.md`
- **date**: 2026-01-31
- **category**: tech/ai-ml
- **tags**: claude-code, agent, skills, infrastructure, telegram-bot

**內容摘要：**

# Claude Code Agent 完整設定

## 摘要

在 ac-mac 上建立完整的 Claude Code agent 配置，包含全域 CLAUDE.md 指引檔和 5 個自訂 skills，
參考 OpenClaw (原 Clawdbot) 專案的架構模式。

## 架構

### CLAUDE.md 層級

| 檔案 | 作用範圍 | 說明 |
|------|---------|------|
| `~/.claude/CLAUDE.md` | 全域（所有 Claude Code session） | 機器資訊、服務清單、多機基礎設施、工作原則 |
| `~/CLAUDE.md` | 主目錄 session | 語言規範、Git 規範、知識庫規範、任務檢查清單 |
| `/usr/local/bin/server-monitor/CLAUDE.md` | server-monitor 專案 | 專案特定開發指引 |

Claude Code 會自動載入 `~/.claude/CLAUDE.md`，無論從哪個目錄啟動 session。
專案目錄下的 `CLAUDE.m
(...截斷)

---

### [33/54] Super Happy Coder 完整系統現狀與測試分析報告
- **filename**: `2026-01-31-Super-Happy-Coder-完整系統現狀與測試分析報告`
- **path**: `tech/2026-01-31-Super-Happy-Coder-完整系統現狀與測試分析報告.md`
- **date**: 2026-01-31
- **category**: tech
- **tags**: Super Happy Coder, 系統分析, 測試報告, 架構評估, 開發計畫

**內容摘要：**

# Super Happy Coder 完整系統現狀與測試分析報告

## 摘要

Super Happy Coder (SHC) 是一個基於多 Agent 架構的 AI 教學系統,部署於三機架構 (ac-mac, acmacmini2, ac-3090),目前系統測試覆蓋率為 **61.8%**,已完成 9 個階段共 54 項測試,其中 21 項通過。系統正處於記憶系統增強 (v3.3.0) 和 M-SYS v2 智慧分析系統的設計階段。

---

## 一、系統架構全景

### 1.1 三機部署架構

```
┌─────────────────────────────────────────────────────────────────┐
│                    ac-mac (Mac Mini)                             │
│         知識庫中心 & 監控 & Happy Coder Daemon                    │
│                                     
(...截斷)

---

### [34/54] SHC Proxy 端口配置問題分析
- **filename**: `2026-01-31-SHC-端口配置問題分析`
- **path**: `tech/2026-01-31-SHC-端口配置問題分析.md`
- **date**: 2026-01-31
- **category**: tech/devops
- **tags**: shc, proxy, port, configuration

**內容摘要：**

# SHC Proxy 端口配置問題分析

## 問題現象

測試時發現 SHC Proxy 的端口在 8080 和 8081 之間「飄來飄去」,導致混淆。

## 根本原因

### 1. 程式碼預設端口

**proxy.py** 的端口配置:

```python
port = int(os.environ.get('PORT', 8080))  # 預設 8080
app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
```

- **預設**: 8080
- **可覆蓋**: 環境變數 `PORT`

### 2. 目前實際運行狀態

**acmacmini2 上的 SHC Proxy (PID 293143)**:

```bash
# 實際監聽端口
ss -tlnp | grep 293143
# 結果: LISTEN 0.0.0.0:8081

# 環境變數
cat /proc/293143/environ | tr '\0' '\n' | grep PORT
# 結果: PORT=8081
```
(...截斷)

---

### [35/54] SHC 混合模式配置與高可用設計
- **filename**: `2026-01-31-SHC-混合模式配置與高可用設計`
- **path**: `tech/2026-01-31-SHC-混合模式配置與高可用設計.md`
- **date**: 2026-01-31
- **category**: tech/ai-ml
- **tags**: SHC, LLM, vLLM, OpenAI, High-Availability, Cost-Optimization

**內容摘要：**

# SHC 混合模式配置與高可用設計

## 摘要

Super Happy Coder (SHC) v3.3.0 支援混合模式 LLM Router:
- **HIGH tier**: OpenAI gpt-4.1-nano (複雜任務)
- **LOW tier**: 本地 vLLM Qwen2.5-7B (簡單任務)
- **目標**: 節省 70% API 成本,同時確保高可用性

**目前狀態**: LOW tier 也使用 OpenAI,並非真正混合模式
**待實作**: 動態切換系統,根據 3090 運作狀況自動調整路由

---

## 一、目前配置狀態

### 1.1 環境變數配置 (acmacmini2)

**路徑**: `~/workshop/super-happy-coder/.env`

**目前設定**:
```bash
# SHC Proxy
PORT=8081

# LLM Router 配置
LLM_HIGH_PROVIDER=openai
LLM_HIGH_MODEL=gpt-4.1-nano

LLM_LOW_PROVIDER=openai  
(...截斷)

---

### [36/54] SHC 測試修復腳本與執行指南
- **filename**: `2026-01-31-SHC-測試修復腳本與執行指南`
- **path**: `tech/2026-01-31-SHC-測試修復腳本與執行指南.md`
- **date**: 2026-01-31
- **category**: tech
- **tags**: Super Happy Coder, 測試, 修復腳本, 執行指南

**內容摘要：**

# SHC 測試修復腳本與執行指南

## 摘要

已建立完整的測試修復與整合腳本,並確認系統配置正確。由於網路架構限制(SHC Proxy 僅監聽 localhost),需要建立 SSH tunnel 才能執行測試。

---

## 一、當前系統狀態

### 1.1 服務運行狀態

| 服務 | 主機 | 端口 | 狀態 | 備註 |
|------|------|------|------|------|
| SHC Proxy | acmacmini2 | 8081 | ✅ 運行中 | 僅監聽 localhost |
| 3090 Compute Plane | ac-3090 | 9000 | ✅ 運行中 | 已透過 SSH tunnel 可訪問 |
| vLLM | ac-3090 | 8000 | ✅ 運行中 | Qwen2.5-7B-Instruct |

### 1.2 LLM Router 配置 (已確認)

```bash
HIGH tier: openai gpt-4.1-nano
LOW tier:  openai gpt-4.1-nano
Fallback
(...截斷)

---

### [37/54] SHC v5 混合編排系統實作紀錄
- **filename**: `2026-01-31-shc-v5-hybrid-implementation`
- **path**: `tech/ai-ml/2026-01-31-shc-v5-hybrid-implementation.md`
- **date**: 2026-01-31
- **category**: tech/ai-ml
- **tags**: SHC, hybrid-orchestrator, dynamic-planner, agent-creator, implementation

**內容摘要：**

# SHC v5 混合編排系統實作紀錄

## 背景

SHC v330 使用純靜態 MODULE.yaml 管線，無法處理模組庫中不存在的任務。
本次實作將混合架構整合進系統，結合固定模組的確定性與動態規劃的靈活性。

## 實作摘要

### 新增 3 個核心模組

#### 1. `dynamic_planner.py`（~350 行）
- TodoWrite 式動態任務規劃器
- LLM 生成 3-8 步任務清單
- 逐步執行，失敗時重新規劃（最多 3 次）
- 支援 4 種 action_type：llm, shell, code, validate
- 整合 ProgressEmitter 推送即時進度
- 完整執行日誌供 AgentCreator 分析

#### 2. `agent_creator.py`（~330 行）
- 自動將成功的動態執行轉化為 MODULE.yaml
- 三道品質防線：品質分數 ≥ 0.8、YAML schema 驗證、可選人工審核
- LOW tier LLM 評估可重複性（~200 token）
- HIGH tier LLM 生成 MOD
(...截斷)

---

### [38/54] SHC v4 混合架構設計 — 固定模組 + 動態規劃 + Agent-Creator
- **filename**: `2026-01-31-shc-v4-hybrid-architecture`
- **path**: `tech/ai-ml/2026-01-31-shc-v4-hybrid-architecture.md`
- **date**: 2026-01-31
- **category**: tech/ai-ml
- **tags**: SHC, architecture, hybrid-agent, module-creation, token-optimization

**內容摘要：**

# SHC v4 混合架構設計

## 背景

SHC v330 使用純靜態 MODULE.yaml 管線，優點是確定性高、token 消耗低，但缺點是無法處理模組庫中不存在的任務。Happy Coder 的 Claude Code 使用純動態 TodoWrite 驅動，靈活但 token 消耗大。

**目標**：結合兩者優勢，建立三層混合架構：
1. **優先使用固定模組**（低成本、高確定性）
2. **缺乏模組時啟用動態 LLM 規劃**（TodoWrite 模式）
3. **Agent-Creator 將成功的動態任務轉化為新模組**（擴充能力、降低未來成本）

## 架構總覽

```
用戶請求
    │
    ▼
┌─────────────────────────────┐
│   HybridOrchestrator        │
│                             │
│  1. ModuleRegistry.match()  │ ─── 命中 ──▶ AgentExecutor（固定管線）
│     觸發詞 + 語義匹配     
(...截斷)

---

### [39/54] Super Happy Coder 記憶系統增強 SDD
- **filename**: `2026-01-30-Super-Happy-Coder-記憶系統增強-SDD`
- **path**: `tech/2026-01-30-Super-Happy-Coder-記憶系統增強-SDD.md`
- **date**: 2026-01-30
- **category**: tech
- **tags**: super-happy-coder, memory, personalization, SDD, architecture, 使用者偏好

**內容摘要：**

# Super Happy Coder 記憶系統增強 SDD

## Software Design Document

---

## 一、背景與動機

### 1.1 現狀分析

Super Happy Coder（以下簡稱 SHC）目前已實作 Clawdbot 風格的 Context Injection（SOUL.md + AGENTS.md + per-student MEMORY.md），但在使用者偏好追蹤和長期記憶方面存在明顯不足。

#### 現有記憶機制

| 機制 | 實作狀態 | 問題 |
|------|----------|------|
| SOUL.md | ✅ 已實作 | 全域，非個人化 |
| AGENTS.md | ✅ 已實作 | 全域，非個人化 |
| MEMORY.md (per-student) | ⚠️ 粗糙 | 只記任務摘要，不記偏好 |
| Conversation History | ⚠️ Redis 7天過期 | 超過 TTL 後遺失 |
| Feedback Collector | ⚠️ 有設計未產出 | feedback_store
(...截斷)

---

### [40/54] OpenAI API Rate Limits - SHC v3.1 專用
- **filename**: `2026-01-30-OpenAI-API-Rate-Limits`
- **path**: `tech/2026-01-30-OpenAI-API-Rate-Limits.md`
- **date**: 2026-01-30
- **category**: tech
- **tags**: openai, api, rate-limit, super-happy-coder, gpt-4.1-nano

**內容摘要：**

# OpenAI API Rate Limits - Super Happy Coder 專案

## 帳號資訊

- **Organization**: user-r5dgaynl1bjjmpgwwdgcimy4
- **Project**: proj_P9JWjaezzj2TtN9L2H2JAjbs
- **用途**: Super Happy Coder v3.1 LLM fallback（替代 3090 vLLM）

## 使用模型

**GPT-4.1 nano** (`gpt-4.1-nano-2025-04-14`)

### 定價

| 類型 | 價格 |
|------|------|
| Input | $0.20 / M tokens |
| Cached Input | $0.05 / M tokens |
| Output | $0.80 / M tokens |

### Rate Limits（實測值）

| 項目 | 限制 |
|------|------|
| Requests per minute | **5,000 RPM** |
| Tokens 
(...截斷)

---

### [41/54] Super Happy Coder 修復後完整測試報告
- **filename**: `2026-01-30-Super-Happy-Coder-修復後完整測試報告`
- **path**: `tech/2026-01-30-Super-Happy-Coder-修復後完整測試報告.md`
- **date**: 2026-01-30
- **category**: 測試報告
- **tags**: Super Happy Coder, 測試, Claude Backend, 修復, Compute Plane

**內容摘要：**

# Super Happy Coder 修復後完整測試報告

## 一、測試概覽

| 項目 | 資訊 |
|------|------|
| 測試時間 | 2026-01-30 06:58-07:00 (約 2 分鐘) |
| Backend | **Claude CLI** (已從 Gemini 切換) |
| 測試平台 | Python 3.10.12, pytest 9.0.2 |
| 總測試數 | 54 項 |
| 通過 | ✅ 21 項 (38.9%) ⬆️ |
| 失敗 | ❌ 13 項 (24.1%) ⬇️ |
| 跳過 | ⏭️ 20 項 (37.0%) |
| **有效通過率** | **61.8%** (21/34，扣除跳過) ⬆️ |

### 📈 與之前測試對比 (Gemini Backend)

| 指標 | Gemini (1/29) | Claude (1/30) | 改善 |
|------|---------------|---------------|------|
| 通過數 | 18 | 21 | ⬆️ **+3** |
| 失敗數 | 16 
(...截斷)

---

### [42/54] Super Happy Coder 流程打通測試紀錄
- **filename**: `2026-01-29-Super-Happy-Coder-流程打通測試紀錄`
- **path**: `tech/2026-01-29-Super-Happy-Coder-流程打通測試紀錄.md`
- **date**: 2026-01-29
- **category**: tech
- **tags**: super-happy-coder, gemini, compute-plane, agent-executor, integration-test

**內容摘要：**

# Super Happy Coder 流程打通測試紀錄

## 摘要

使用 Gemini CLI 作為後端，完成 Super Happy Coder v2.1.0 全鏈路端到端測試。
測試涵蓋 Chat API、Agent Executor 自動匹配、Compute Plane GPU 服務串接。

---

## 一、測試環境

| 項目 | 設定 |
|------|------|
| Proxy 主機 | Mac Mini 2 (acmacmini2, 192.168.1.103:8081) |
| CLI Backend | Gemini CLI 0.26.0 |
| Compute Plane | 3090 (ac-3090, localhost:9000 via SSH Tunnel) |
| Proxy 版本 | Super Happy Coder v2.1.0 |
| 認證方式 | Google 帳號 (o970117818@gmail.com)，瀏覽器認證 |

---

## 二、測試結果

### 2.1 Chat API 端到端

```bash
curl 
(...截斷)

---

### [43/54] Super Happy Coder - 互動進度顯示與回饋迭代機制設計
- **filename**: `2026-01-29-互動進度與回饋機制設計`
- **path**: `tech/2026-01-29-互動進度與回饋機制設計.md`
- **date**: 2026-01-29
- **category**: tech
- **tags**: agent, UX, feedback-loop, progress, super-happy-coder, 互動設計

**內容摘要：**

# 互動進度顯示與回饋迭代機制設計

## 摘要
兩個核心需求的整合設計：(1) 任務執行時的即時互動進度顯示，結合 Happy 的可見性與 Clawdbot 的不打擾哲學；(2) 用戶調整請求的回饋迭代機制，將修改記錄轉化為模組規格的持續優化。

## 關鍵要點
- 用戶在執行過程中能即時看到任務進度、當前動作、完成項目
- 不需要確認的部分採預設規格直接跑通，用戶有疑慮可隨時中斷
- 所有輸入/輸出/調整都會記錄，形成回饋閉環
- 後台管理者可決定是否將回饋迭代到模組規格

---

## 一、互動進度顯示系統（Task Progress UX）

### 1.1 設計哲學

結合兩套系統的優點：

| 面向 | Happy 風格 | Clawdbot 風格 | 整合設計 |
|------|-----------|--------------|---------|
| 可見性 | 高 - 顯示任務清單、逐項打勾 | 低 - 靜默執行到底 | 高 - 即時顯示但不要求互動 |
| 打擾程度 | 中 - 有時需確認 | 低 - 幾乎不問 | 低 - 只在開始時確認目標，之後不問 |

(...截斷)

---

### [44/54] Super Happy Coder TG Bot 部署紀錄
- **filename**: `2026-01-29-Super-Happy-Coder-TG-Bot-部署紀錄`
- **path**: `tech/2026-01-29-Super-Happy-Coder-TG-Bot-部署紀錄.md`
- **date**: 2026-01-29
- **category**: tech
- **tags**: super-happy-coder, telegram-bot, token-quota, user-management

**內容摘要：**

# Super Happy Coder TG Bot 部署紀錄

## 摘要

建立雙 Bot 架構的 Telegram 介面，整合 Token 配額控制與管理後台。
學員透過 @SupperHappyCoder_bot 使用 AI 助手，管理者透過 @SupperHappyAdmin_bot 監控系統。

---

## 一、Bot 架構

### 1.1 雙 Bot 設計

| Bot | 用途 | Token |
|-----|------|-------|
| @SupperHappyCoder_bot | 學員使用 | `8307879072:AAF6USUWoLUraAcENIpz7D4crFIlfkcKeyk` |
| @SupperHappyAdmin_bot | 管理後台 | `8582272061:AAGkHMyeiUZ1WwdgyM8UajD7W-i0H6Hcy1w` |

**架構流程：**
```
TG Bot → Proxy API (localhost:8081) → CLI Backend / Compute Plane
```

### 1.2 服務配
(...截斷)

---

### [45/54] OpenSpec TG Agent System v3 版本分析
- **filename**: `2026-01-29-OpenSpec-TG-Agent-System-v3-分析`
- **path**: `tech/2026-01-29-OpenSpec-TG-Agent-System-v3-分析.md`
- **date**: 2026-01-29
- **category**: tech
- **tags**: agent, architecture, openspec, multi-agent, telegram, 教學系統

**內容摘要：**

# OpenSpec TG Agent System v3 版本分析

## 摘要
v3 從「高層規範」升級到「可實裝的生產級規格」，新增 5 個檔案，核心改進在 Planner-Executor 分離、入口治理管線、容量規劃（20 人教學場景）與安全管控。

## 關鍵要點
- Planner-Executor 明確分離：外部 LLM 只輸出 Plan JSON，不負責執行
- 10-step Ingress Pipeline 規範化入口處理
- 三層佇列架構（interactive / batch / heavy）支援不同優先級
- API 端點從 4 個擴展到 7 個
- 針對 20 人同時上課場景的容量規劃

---

## 一、v3 新增的檔案

| 檔案 | 內容 |
|------|------|
| `specs/35-ingress-pipeline.md` | 10 步入口處理管線規格 |
| `specs/55-capacity-and-concurrency.md` | 20 人教學場景容量規劃 |
| `specs/56-3090-compute-plane-
(...截斷)

---

### [46/54] 3090 Compute Plane 部署與網路連通紀錄
- **filename**: `2026-01-29-3090-Compute-Plane-部署與網路連通紀錄`
- **path**: `tech/2026-01-29-3090-Compute-Plane-部署與網路連通紀錄.md`
- **date**: 2026-01-29
- **category**: tech
- **tags**: 3090, compute-plane, ssh-tunnel, tailscale, networking, super-happy-coder

**內容摘要：**

# 3090 Compute Plane 部署與網路連通紀錄

## 摘要

在 3090 主機 (ac-3090) 上完成 Compute Plane API 部署，包含 LLM (vLLM)、Embedding、
Rerank、OCR、Toolchain 五大服務。因 Tailscale ACL 限制，改用 SSH Tunnel 實現
Mac Mini 2 到 3090 的 port 9000 連通。

---

## 一、3090 已安裝元件

### Phase 1：基礎環境
- FastAPI 0.128.0 + Uvicorn 0.40.0
- Redis Server 6.0.16（systemd 自啟）
- poppler-utils、ImageMagick
- httpx、pydantic、pyyaml

### Phase 2：Embedding + Rerank
- sentence-transformers 5.2.2
- transformers 4.57.6（被 vLLM 降級至此版本）
- faiss-gpu 1.7.2
- 預設 Embedding 模型
(...截斷)

---

### [47/54] 3090 Compute Plane 安裝規劃
- **filename**: `2026-01-29-3090-Compute-Plane-安裝規劃`
- **path**: `tech/2026-01-29-3090-Compute-Plane-安裝規劃.md`
- **date**: 2026-01-29
- **category**: tech
- **tags**: 3090, GPU, compute-plane, super-happy-coder, deployment

**內容摘要：**

# 3090 Compute Plane 安裝規劃

## 摘要

規劃在 RTX 3090 主機 (ac-3090) 上安裝 Super Happy Coder 所需的 Compute Plane 服務。
目標：提供 LLM 推理、Embedding、Rerank、OCR、Toolchain 五大服務，
由 Mac Mini 2 上的 Agent Executor 透過內網 API 呼叫。

---

## 現況評估

### 硬體
| 項目 | 規格 |
|------|------|
| GPU | NVIDIA RTX 3090 24GB VRAM |
| RAM | 32GB |
| 磁碟 | 457GB (394GB 可用) |
| OS | Ubuntu 22.04 LTS |
| NVIDIA Driver | 590.48.01 |
| CUDA (PyTorch) | 12.1 |

### 已安裝
- Python 3 + pip3
- PyTorch 2.5.1+cu121（CUDA 可用）
- Git
- ComfyUI（使用中，佔用約 7GB VRAM）


(...截斷)

---

### [48/54] Super Happy Coder 功能測試報告分析
- **filename**: `2026-01-29-Super-Happy-Coder-測試報告分析`
- **path**: `tech/2026-01-29-Super-Happy-Coder-測試報告分析.md`
- **date**: 2026-01-29
- **category**: 測試報告
- **tags**: Super Happy Coder, 測試, Claude Backend, Gemini CLI, 問題分析

**內容摘要：**

# Super Happy Coder 功能測試報告分析

## 一、測試概覽

| 項目 | 資訊 |
|------|------|
| 測試時間 | 2026-01-29 18:46-18:48 (約 2 分鐘) |
| 測試對象 | Claude Backend (Mac Mini 2:8081 via SSH tunnel) |
| 測試平台 | Python 3.10.12, pytest 9.0.2 |
| 總測試數 | 54 項 |
| 通過 | ✅ 18 項 (33.3%) |
| 失敗 | ❌ 16 項 (29.6%) |
| 跳過 | ⏭️ 20 項 (37.0%) |
| **有效通過率** | **52.9%** (18/34，扣除跳過) |

---

## 二、各階段測試結果

### Phase 1: Infrastructure (基礎設施) ✅ 100%

**測試項目：** 6 項
**結果：** 4 通過 / 0 失敗 / 2 跳過

| 測試 | 結果 | 說明 |
|------|------|------|
| test_p1_01_hea
(...截斷)

---

### [49/54] AI Agent 架構分析 - Clawdbot vs Happy Coder vs VS Code
- **filename**: `2026-01-28-AI-Agent-架構分析-Clawdbot-vs-Happy-Coder`
- **path**: `tech/2026-01-28-AI-Agent-架構分析-Clawdbot-vs-Happy-Coder.md`
- **date**: 2026-01-28
- **category**: tech
- **tags**: AI, agent, clawdbot, happy-coder, claude, codex, 架構分析

**內容摘要：**

# AI Agent 架構分析

比較三種 AI Coding Agent 的架構設計：Clawdbot、Happy Coder、VS Code Claude Extension

## 核心問題

為什麼 Clawdbot 能完成更複雜的任務，即使它也是調用 CLI (Codex/Claude)？中間有什麼機制讓複雜任務可以更完整地被分派與執行？

---

## 1. Clawdbot 架構

### 系統架構圖

```
┌─────────────────────────────────────────────────────────────┐
│                      Clawdbot Gateway                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Telegram   │  │   Discord   │  │  Other Channels     │  │
│  └──────┬──────┘  └──────
(...截斷)

---

### [50/54] 模組編排系統設計 - Module Orchestrator
- **filename**: `2026-01-28-模組編排系統設計`
- **path**: `tech/2026-01-28-模組編排系統設計.md`
- **date**: 2026-01-28
- **category**: tech
- **tags**: AI, agent, module, orchestrator, state-machine, 架構設計

**內容摘要：**

# 模組編排系統設計

分析 OpenSpec 的 Module Orchestrator 如何強化 Super Happy Coder 的產出精準度與精緻度。

---

## 1. 現有 vs 增強架構

### 現有架構（Simple Skill Matching）

```
User Request → Intent Router → Match Skill → Execute CLI → Response
                    ↓
              (單次匹配)
```

**問題**：
- 只做一次性的 Skill 匹配
- 沒有任務分解
- 沒有狀態追蹤
- 複雜任務容易失敗或不完整

### 增強架構（Module Orchestrator）

```
User Request → Intent Router → Module Selection → Planner
                                                     ↓
                                  
(...截斷)

---

### [51/54] 增強型 Multi-Agent 系統設計 - Super Happy Coder
- **filename**: `2026-01-28-增強型-Multi-Agent-系統設計`
- **path**: `tech/2026-01-28-增強型-Multi-Agent-系統設計.md`
- **date**: 2026-01-28
- **category**: tech
- **tags**: AI, agent, clawdbot, happy-coder, multi-agent, 架構設計

**內容摘要：**

# 增強型 Multi-Agent 系統設計

整合 Clawdbot 中介層設計 + OpenSpec TG Agent 規格 + RPI5 多學員 Proxy，打造高度整合的教學用 AI Agent 系統。

---

## 1. 現有系統分析

### 1.1 Clawdbot 的優勢（學習點）

| 機制 | 功能 | 價值 |
|------|------|------|
| **SOUL.md** | 身份定義、個性、邊界 | AI 有一致的行為模式 |
| **AGENTS.md** | 行為規範、安全規則 | 標準化的執行流程 |
| **MEMORY.md** | 長期記憶 | 跨 Session 的上下文續接 |
| **Skills 系統** | 每個工具有說明文件 | AI 可查閱說明書正確使用工具 |
| **PTY + Background** | 偽終端 + 背景執行 | 支援複雜的互動式任務 |
| **Heartbeat** | 定期喚醒 | 主動檢查任務、自動工作 |

### 1.2 RPI5 Proxy 的基礎（現有能力）

```python

(...截斷)

---

### [52/54] Andrej Karpathy：AI 輔助程式開發的相位轉移
- **filename**: `2026-01-27-andrej-karpathy-ai-coding-workflow`
- **path**: `tech/ai-ml/2026-01-27-andrej-karpathy-ai-coding-workflow.md`
- **date**: 2026-01-27
- **category**: tech/ai-ml
- **tags**: AI編程, LLM, Claude, Agent, 軟體工程, 工作流程, Andrej-Karpathy

**內容摘要：**

# Andrej Karpathy：AI 輔助程式開發的相位轉移

## 📊 元資訊
- **難度**：⭐⭐⭐
- **來源類型**：社群媒體長文
- **作者**：Andrej Karpathy（OpenAI 創始成員、前特斯拉 AI 主管）
- **筆記時間**：2026-01-27 23:27

## 📌 摘要
AI 大神 Andrej Karpathy 分享他近期高強度使用 Claude 進行程式開發的深刻轉變。他描述從 11 月的 80% 手動 + 20% Agent，到 12 月已變成 80% Agent + 20% 人工潤飾的「相位轉移」。這是他二十年程式生涯中最大的工作流程變革，預示著軟體工程正進入一個由 AI Agent 主導的新時代。

## 🏷️ 標籤分類
- **大分類**：tech
- **小分類**：ai-ml

## 🔑 關鍵要點

### 1. 工作流程劇變
- 11 月：80% 手動編碼 + 20% Agent
- 12 月：80% Agent 編寫 + 20% 人工修改
- 現在主要用「英文」編寫程式，下達高層次指令

### 2. AI 的現有局限
(...截斷)

---

### [53/54] VibeResearch - Claude Code 自動撰寫學術論文
- **filename**: `2026-01-25-VibeResearch-Claude-Code寫論文`
- **path**: `tech/ai-ml/2026-01-25-VibeResearch-Claude-Code寫論文.md`
- **date**: 2026-01-25
- **category**: tech/ai-ml
- **tags**: Claude, AI寫作, 學術研究, Vibe Coding, Prompt Engineering

**內容摘要：**

# VibeResearch - Claude Code 自動撰寫學術論文

## 📊 元資訊
- **難度**：⭐⭐⭐⭐
- **來源類型**：社群分享 / 學術實驗
- **作者**：Andy Hall（史丹佛大學商學院教授）
- **筆記時間**：2026-01-25 19:22

## 📌 摘要
史丹佛大學教授 Andy Hall 使用 Claude Code 在不到一小時內成功擴展了一篇已發表的政治科學論文。經過人工驗證，Claude 的準確率極高（29/30 縣正確編碼，數據相關係數 > 0.999），僅有三個小錯誤，類似人類首次撰寫時可能犯的錯誤。

## 🏷️ 標籤分類
- **大分類**：tech
- **小分類**：ai-ml

## 🔑 關鍵要點
1. **Claude Code 完成的任務**：下載程式庫、轉換 Stata→Python、網路爬取數據、分析延伸至 2024、製作圖表、文獻回顧、撰寫論文、推送 GitHub
2. **準確率驗證**：29/30 加州縣正確編碼，選舉數據相關係數 > 0.999
3. **模組化工作流程**：一次一個模組，測試通過才
(...截斷)

---

### [54/54] SHC (Super Happy Coder) 服務盤點與規劃
- **filename**: `shc-service-review`
- **path**: `work-logs/tasks/shc-service-review.md`
- **date**: 
- **category**: 
- **tags**: (無)

**內容摘要：**

# SHC 服務盤點與規劃

## 背景
SHC 原先配置的基礎設施已大幅變動，需要重新盤點服務架構再做完整規劃。

## 現況 (2026-03-03)

### 已停止的服務 (acmacmini2)
- [x] super-happy-coder.service — stopped + disabled
- [x] ssh-tunnel-3090-vllm.service — stopped + disabled (localhost:8000 → ac-3090:8000)
- [x] ssh-tunnel-3090-compute.service — stopped + disabled (localhost:9000 → ac-3090:9000)

### 停止原因
- ac-3090 vLLM (Qwen2.5-7B-Instruct) 自 2/17 已停，port 8000 被 Edit-Banana 佔用
- SHC HealthMonitor 每 30s 打到錯誤服務，導致 healthy↔degraded 反覆切換
- 持續發送假警報 Telegram 通知


(...截斷)

---
