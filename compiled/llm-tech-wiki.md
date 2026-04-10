---
title: "LLM 技術與模型 — 知識 Wiki"
date: 2026-04-10
type: wiki
content_layer: L3
topic: llm-tech
source_count: 58
last_compiled: 2026-04-10
_skip_sync: true
---

# LLM 技術與模型 — 知識 Wiki

## 主題概述

大型語言模型（LLM）已從研究玩具蛻變為生產基礎設施。黃仁勳將 AI 發展劃分為三次拐點——生成式 AI、推理能力、AI Agent——每一次拐點的 Token 消耗量較前一代增加數個量級 [[2026-03-06-jensen-huang-morgan-stanley-tmt]]。Ethan Mollick 的第八版 AI 使用指南更直指我們已進入「代理時代」，「使用 AI」的定義從對話框聊天轉變為指派任務給自主 Agent [[2026-03-01-ethan-mollick-agentic-era-ai-guide]]。這意味著 LLM 不再只是回答問題的工具，而是需要被部署、量化、成本優化、與業務流程深度整合的運算引擎。

本知識庫匯集 58 篇筆記，涵蓋四條主線：(1) 模型選型、部署與量化（vLLM、QwenASR Int8、PaddleOCR-VL）；(2) Prompt Engineering 與成本控制（Token 優化、CLAUDE.md 精簡、模型降級策略）；(3) LLM 在專業領域的落地實踐（法律、會計、行銷、室內設計、學術研究）；(4) AI 對產業與社會結構的衝擊（企業 AI 五等級、教育系統重塑、職業角色轉型）。這些筆記共同描繪出一幅「從模型到應用到社會」的完整技術地圖。

當前階段的核心張力在於：模型能力快速膨脹，但落地的關鍵瓶頸不在模型本身，而在系統工程——邊界定義、成本控制、領域知識注入、品質把關。Andrej Karpathy 用兩個月從 80% 手動翻轉為 80% Agent [[2026-01-27-andrej-karpathy-ai-coding-workflow]]，但 SHC 系統 61.8% 的測試通過率提醒我們，從「能用」到「穩定可靠」的距離仍然遙遠 [[2026-01-31-shc-v5-hybrid-implementation]]。

## 核心概念

### 1. 本地 LLM 部署與推理加速

在 RTX 3090（24GB VRAM）上部署 vLLM 運行 Qwen2.5-7B-Instruct 是本知識庫中反覆驗證的核心基礎設施。部署過程需處理注意力後端相容性問題（FLASH_ATTN 未安裝導致掛起，最終改用 TRITON_ATTN）[[2026-01-30-vLLM-Qwen-3090-部署紀錄]]。壓力測試證實 vLLM 的 continuous batching 機制極為高效——50 人同時並發仍能在 28 秒內 100% 完成，GPU 推理是唯一瓶頸 [[2026-01-30-3090-遠端壓力測試報告]]。硬體測試則涵蓋 CUDA 12.8 toolkit + flash-attn 2.8.3 的完整安裝鏈 [[2026-01-30-3090-vLLM-硬體測試與部署紀錄]]。

### 2. 模型量化與輕量化部署

量化技術讓 LLM 跳脫 GPU 依賴。QwenASR 1.7B 模型成功量化至 Int8，在 5 年前的 8GB RAM 筆電上以 CPU 運行語音辨識（1 小時音檔 20 分鐘完成），效果接近原始權重 [[2026-03-01-QwenASR-int8-CPU語音辨識]]。PaddleOCR-VL-1.5 則以僅 0.9B 參數的視覺語言模型達到 94.5% 文件解析準確率，推理速度超越許多大型模型，展示了「小模型 + 任務專精」的威力 [[2026-01-31-paddleocr-vl-1.5]]。

### 3. Token 經濟學與成本控制

LLM 落地的隱藏殺手是 Token 成本。9 行 CLAUDE.md 禁止拍馬屁開頭和空洞結尾等冗餘行為，聲稱可減少 63% 輸出 Token [[2026-04-03_Claude-Token-Efficient-CLAUDE-md]]。建立 Token Dashboard 視覺化 context 消耗後發現，啟動載入的 context 可從 13,190 tokens 壓縮至 6,673 tokens（約 50% 節省），關鍵洞見是「你根本不知道問題存在，直到視覺化它」[[2026-03-04-AI-Context-Token-優化術]]。更系統性的策略是用高階模型（Claude Opus）將任務知識固化為 skills 和 web services，之後由免費模型（GPT-4o）執行 [[2026-03-01-AI模型成本優化-用高階模型訓練低階模型]]。

### 4. Prompt Engineering 與真實感生成

AI 圖片生成的 prompt 工程已形成可複製的結構公式：「主體 + 鏡頭描述 + 光線條件 + 細節紋理 + 色彩設定 + 拍攝器材感 + 排除修圖」。真實感的關鍵不是完美，而是不完美——紀實攝影感加上微瑕疵細節 [[2026-03-04-AI圖片生成-真實照片風格提示詞]]。在文字生成領域，ComfyUI 室內設計渲染管線展示了 prompt 如何與 ControlNet、IP-Adapter 配合，在特定領域（日式簡約空間）達到產業級品質 [[2026-04-04_ComfyUI室內設計渲染技術規劃]]。

### 5. LLM 落地專業領域的方法論

會計三表案例展示了完整的領域落地流程：自建 Skill 注入台灣稅務知識 → 分輪次處理不同資料源 → 互動式補齊缺失 → subagent 紅隊演練品質把關，3 小時內從散落文件產出通過會計師查帳的三表 [[2026-04-01_Claude-Code會計三表案例分析]]。律師案例則證明通用型 Claude + 自建 Skill 比專門法律 AI 產品更有效，關鍵是將十年實務判斷力編碼為 AI 技能 [[2026-03-01-AI-skill-時代來臨-律師實務應用案例]] [[2026-03-01-claude-desktop-lawyer-workflow]]。Cisco 五步驟框架與會計五步法高度互補——前者偏設計時架構規範，後者偏執行時工作流程 [[2026-04-01_Cisco五步驟vs會計三表五步法對照分析]]。

### 6. AI Coding 與開發工具鏈

Andrej Karpathy 的「80/20 相位轉移」是本主題最具標誌性的觀察 [[2026-01-27-andrej-karpathy-ai-coding-workflow]]。Stanford CS146S 課程將其系統化，提出「人類-代理協作工程」新範式——開發者應成為 AI 代理實習生的管理者 [[2026-01-25-stanford-cs146s-modern-software-developer]]。工具層面，Claude Code Remote Control 將 coding agent 從桌面擴展到手機 [[2026-03-01-claude-code-remote-control]]，ClaudeBot 更將 Telegram 打造為行動 AI 開發環境，產出超過 20 萬行實際使用的程式碼 [[2026-03-06-ClaudeBot-Telegram-AI-IDE]]。行銷人案例則提醒非工程師使用 AI coding 工具時，Human-in-the-loop 原則不可或缺 [[2026-03-04-行銷人使用claude-code實戰指南]]。

### 7. RAG 系統與知識管理架構

知識管理分為兩種對立哲學：LLM Knowledge Base（Karpathy 式）讓 LLM 作為知識編譯器自動湧現結構，SecondBrain → Notion 管線則以人工設計的結構作為骨架 [[knowledge-management-comparison]]。RAG 的生產部署需處理 16 種可重現的故障模式，WFGY Problem Map 提出「語義防火牆」概念——在生成輸出前檢查系統狀態，而非事後打補丁 [[2026-03-01-WFGY-RAG-16問題清單]]。悠識數位 RAG 系統規劃則展示了從 MVP 到可部署系統的完整擴展路徑，以 Qdrant 向量資料庫 + FastAPI 為核心 [[2026-03-30_悠識RAG系統規劃]]。

### 8. 混合模式 LLM 路由

SHC v3.3.0 的混合模式 LLM Router 代表了成本與品質的權衡設計：HIGH tier（OpenAI gpt-4.1-nano）處理複雜任務，LOW tier（本地 vLLM Qwen2.5-7B）處理簡單任務，目標節省 70% API 成本 [[2026-01-31-SHC-混合模式配置與高可用設計]]。v4 混合架構更進一步：優先使用固定模組（低成本、高確定性）→ 缺乏模組時啟動動態 LLM 規劃 → Agent-Creator 將成功執行自動轉化為新模組 [[2026-01-31-shc-v4-hybrid-architecture]] [[2026-01-31-shc-v5-hybrid-implementation]]。

### 9. AI 圖像生成與渲染管線

ComfyUI + SDXL（RealVisXL V5.0）+ Dual ControlNet（Canny 結構線 + Depth 空間感）構成 DesignClaw 的核心渲染引擎，在 RTX 3090 上實現 6 房間批量渲染（預估 3.5-5 分鐘）[[2026-04-04_ComfyUI室內設計渲染技術規劃]] [[2026-04-04_DesignClaw-ComfyUI整合架構]]。更廣泛的開源生態調查顯示，目前不存在端到端的 AI 室內設計管線，但每個環節都有可用的開源工具，最大缺口是 D5 Render 無法自動化需改用 Blender + Cycles [[2026-04-03_AI室內設計管線開源資源研究]]。

### 10. 企業 AI 應用成熟度模型

企業 AI 應用分為五個等級：L1 工具輔助（員工自己找神器）→ L2 流程協作（部門有了新 SOP）→ L3 決策協作（AI 開始打 KPI）→ L4 模式變革（做以前做不到的生意）→ L5 自行進化（系統級自我強化飛輪）[[2026-01-26-ai應用五等級]] [[2026-01-26-AI應用五等級與企業AI踩坑解析]]。大語言模型執行任務的錯誤率約 30%-40%，消費級產品需達 95% 以上才「可用」、99% 以上才「好用」，這個差距是企業 AI 落地的核心瓶頸 [[2026-02-03-豆包AI手機與系統級AI助手的博弈分析]]。

## 關鍵發現

> **80/20 相位轉移**：Andrej Karpathy 在兩個月內從 80% 手動 + 20% Agent 翻轉為 80% Agent + 20% 人工，稱其為二十年程式生涯最大的工作流程變革。主要用「英文」編寫程式，下達高層次指令。 [[2026-01-27-andrej-karpathy-ai-coding-workflow]]

> **通用 AI + 自建 Skill 勝過垂直 AI 產品**：律師案例證明，通用型 Claude 搭配自建 Skill 的組合比專門法律 AI 更有效。2026 年 AI 應用的核心從 Prompt 轉向 Skill——可系統化迭代的知識封裝。 [[2026-03-01-AI-skill-時代來臨-律師實務應用案例]]

> **Token 浪費是隱形成本**：9 行 CLAUDE.md 可減少 63% 輸出 token；Token Dashboard 視覺化後發現啟動 context 可壓縮 50%。問題不在省多少，而在「你根本不知道浪費存在，直到視覺化它」。 [[2026-04-03_Claude-Token-Efficient-CLAUDE-md]] [[2026-03-04-AI-Context-Token-優化術]]

> **50 人並發的本地推理已可行**：RTX 3090 + vLLM + Qwen2.5-7B 在 50 人同時並發下 100% 成功、28 秒完成。GPU 推理是唯一瓶頸，網路頻寬完全不是問題。 [[2026-01-30-3090-遠端壓力測試報告]]

> **AI 取代的是任務，不是職業**：黃仁勳指出 AI 沒有取代放射科醫師，反而讓需求增加；未來寫程式的人從三千萬變十億。智慧正在商品化，但判斷力無法被商品化。 [[2026-03-31_黃仁勳Lex-Fridman三個觀點]]

> **小模型 + 任務專精的威力**：PaddleOCR-VL-1.5 僅 0.9B 參數，在文件解析任務上與 235B 的 Qwen3-VL 不遑多讓。QwenASR 1.7B Int8 讓 8GB 筆電能跑語音辨識。模型不是越大越好。 [[2026-01-31-paddleocr-vl-1.5]] [[2026-03-01-QwenASR-int8-CPU語音辨識]]

> **VibeResearch 的學術驗證**：史丹佛教授用 Claude Code 在不到一小時內擴展已發表論文，準確率 29/30 縣正確、數據相關係數 > 0.999。學術工作流程的 AI 輔助已跨過可用門檻。 [[2026-01-25-VibeResearch-Claude-Code寫論文]]

> **AI 三大技術流派分化**：湧現派（Altman，規模即一切）、訓鳥派（李飛飛，AI 需要身體與物理互動）、飛機派（LeCun，需要全新非生成式世界模型）。路線之爭正在從學術辯論變為千億美元級的資本押注。 [[2026-02-04-AI產業年末三大趨勢-技術分化-資本分化-賭注極端化]]

> **Claude Code 內部架構遠超表面**：源碼洩漏揭示 KAIROS（常駐背景 Agent）、ULTRAPLAN（30 分鐘遠端規劃）、Coordinator 多 Agent 協調等尚未公開功能。512,000 行 TypeScript，1,900 個檔案。 [[2026-03-31_Claude-Code源碼洩漏分析]]

## 跨筆記關聯

### LLM 部署的完整技術棧

從硬體測試 [[2026-01-30-3090-vLLM-硬體測試與部署紀錄]] → vLLM 部署排錯 [[2026-01-30-vLLM-Qwen-3090-部署紀錄]] → 壓力測試驗證 [[2026-01-30-3090-遠端壓力測試報告]] → 混合模式路由 [[2026-01-31-SHC-混合模式配置與高可用設計]] → RPM 限制測試 [[2026-01-31-工作日誌]]，形成一條從「能不能跑」到「跑得多穩」的完整驗證鏈。

### 成本控制的三層策略

Token 優化（減少冗餘輸出）[[2026-04-03_Claude-Token-Efficient-CLAUDE-md]] [[2026-03-04-AI-Context-Token-優化術]] → 模型降級（高階訓練 + 低階執行）[[2026-03-01-AI模型成本優化-用高階模型訓練低階模型]] → 混合路由（按任務複雜度分派模型）[[2026-01-31-SHC-混合模式配置與高可用設計]]，三層策略逐漸從 prompt 端走向系統架構端，但尚未整合為統一的 ROI 框架。

### Skill 系統的跨領域驗證

律師案例 [[2026-03-01-AI-skill-時代來臨-律師實務應用案例]] [[2026-03-01-claude-desktop-lawyer-workflow]]、會計案例 [[2026-04-01_Claude-Code會計三表案例分析]]、室內設計管線 [[2026-04-04_ComfyUI室內設計渲染技術規劃]]、Everything Claude Code hackathon [[everything-claude-code]] 都指向同一結論：LLM 的差異化不在模型選擇，在 Skill 注入。Cisco 五步驟框架提供了 Skill 系統的設計方法論 [[2026-04-01_Cisco五步驟vs會計三表五步法對照分析]]。

### AI 社會衝擊的多視角收斂

教育面：學校需從工廠流水線升級為創業孵化器 [[2026-01-30-AI時代學校系統升級]] [[2026-02-10-AI時代教育系統級創新]]。職業面：五類不可替代的人——決策者、提問者、看門人、執行者、責任人 [[2026-01-30-AI時代留給普通人的五個角色]]。社會面：數位留痕取代一次性文憑成為新信號 [[2026-01-30-AI時代君子社會與數字留痕]]。產業面：台灣新創在窄河道市場找到生存空間 [[2026-01-26-台灣AI新創3法則]]。黃仁勳的結論：AI 取代任務不取代職業 [[2026-03-31_黃仁勳Lex-Fridman三個觀點]]。多條線索收斂到同一判斷——人的稀缺價值在判斷力、責任承擔與主動性。

### DesignClaw 渲染管線的技術演進

從開源資源調查（30+ 工具評估）[[2026-04-03_AI室內設計管線開源資源研究]] → 系統計畫（7-Agent Pipeline）[[2026-04-03_DesignClaw室內裝修自動化系統計畫]] → ComfyUI 渲染技術規劃（Model 選型 + ControlNet + IP-Adapter）[[2026-04-04_ComfyUI室內設計渲染技術規劃]] → 整合架構實作 [[2026-04-04_DesignClaw-ComfyUI整合架構]]，展示了 LLM + 擴散模型在垂直領域的完整落地路徑。

### 知識管理的兩種路線之爭

LLM Knowledge Base（Karpathy 式）讓結構從內容自動湧現，SecondBrain → Notion 管線以人工結構為骨架 [[knowledge-management-comparison]]。本 Wiki 本身就是前者的實踐——58 篇原始筆記經 LLM 編譯後產出結構化知識。Open NotebookLM 則是第三條路：支援多 AI 提供商的 RAG 檢索 + Podcast 生成 [[2026-01-25-open-notebookllm]]。

## 待探索方向

1. **統一成本模型**：散見於各筆記的 Token 成本數據（Token Efficient CLAUDE.md 減少 63%、Context Dashboard 壓縮 50%、SHC 混合路由目標 70%）需要整合為可量化的 LLM 應用 ROI 框架。目前缺乏從「每請求成本」到「每業務產出成本」的換算模型。

2. **小模型部署的系統化**：QwenASR Int8 [[2026-03-01-QwenASR-int8-CPU語音辨識]] 和 PaddleOCR-VL-1.5 [[2026-01-31-paddleocr-vl-1.5]] 證明小模型在特定任務上可媲美大模型，但何時該用大模型、何時該用小模型的決策框架尚未建立。

3. **RAG 故障模式的生產驗證**：WFGY 16 問題清單 [[2026-03-01-WFGY-RAG-16問題清單]] 提供了理論框架，悠識 RAG 系統 [[2026-03-30_悠識RAG系統規劃]] 開始了工程實作，但兩者尚未交叉驗證——哪些故障模式在實際部署中最常出現？

4. **FDE 架構師培訓方法論**：Smart4A 以 FDE 思維重新定位課程 [[2026-03-30_FDE角色與Smart4A轉型分析]]，但從「知道 FDE 是什麼」到「能培養出 FDE」的教學設計仍待補足。

5. **WiFi DensePose 的 LLM 整合潛力**：WiFi 人體姿態追蹤 [[2026-03-01-WiFi-DensePose-開源人體姿態追蹤]] 達到 94.2% 準確率，與 LLM 的多模態推理結合（如智慧家居場景理解）是值得探索但筆記中尚未觸及的方向。

6. **AI Agent 基礎設施六大路線的落地追蹤**：瀏覽器/IDE 成為 Agent 的身體、Agent OS 雛形出現、Agent 市集標準化等六條路線 [[2026-03-01-ai-agent-infrastructure-trend]] 已被識別，但後續演進尚未追蹤記錄。

7. **Claude Code 源碼洩漏的架構啟示**：KAIROS、ULTRAPLAN、Agent Swarm 等隱藏功能 [[2026-03-31_Claude-Code源碼洩漏分析]] 揭示了 Anthropic 對 Agent 未來的設計思路，值得持續追蹤這些功能何時公開，以及對自建 Agent 架構的影響。
