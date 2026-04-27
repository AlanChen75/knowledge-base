---
title: "AI Agent 架構與實戰 — 知識 Wiki"
date: 2026-04-10
type: wiki
content_layer: L3
topic: ai-agent
source_count: 55
last_compiled: 2026-04-27
_skip_sync: true
---

# AI Agent 架構與實戰 — 知識 Wiki

## 主題概述

AI Agent 正從「對話式 AI」演進為「自主行動 AI」，標誌著軟體開發與知識工作的典範轉移。Jensen Huang 將此定位為 AI 三次拐點中的第三波——從生成式 AI 到推理能力再到 Agent，Token 消耗量將比前一代增加百萬倍 [[2026-03-06-jensen-huang-morgan-stanley-tmt]]。Ethan Mollick 更直言：「使用 AI」的定義已從「在對話框裡聊天」變成「指派任務給能自主使用工具的 Agent」[[2026-03-01-ethan-mollick-agentic-era-ai-guide]]。

本知識庫記錄了從 2026 年 1 月至 4 月的密集探索歷程（55 篇筆記），涵蓋三條主線：(1) Super Happy Coder (SHC) 多 Agent 教學系統的設計、部署與迭代；(2) DesignClaw 室內設計自動化管線的 7-Agent Pipeline 實作；(3) Claude Code、OpenClaw 等 AI Agent 工具的實戰方法論。2026 年 4 月下旬更新加入 Anthropic Project Deal 代理人市集實驗——首次在受控環境中量測「模型品質差距」對代理人議價結果與使用者感知的影響，揭示了代理時代的隱形不平等議題。這些筆記共同勾勒出一幅從理論框架到生產部署的完整 Agent 實踐地圖。

核心主張：Agent 的關鍵不在模型聰不聰明，而在於 **系統工程**——邊界定義、任務分解、記憶管理、多機協作、成本控制。從「寫程式」到「定義規章」的身份轉變，才是這個時代真正的技術紅利 [[2026-02-06-OpenClaw-AI-Agent-新時代思考]]。

## 核心概念

### 1. Agent 架構模式：從單體到多層編排

AI Agent 系統的核心挑戰是任務分解與執行協調。筆記中記錄了三種遞進的架構模式：

- **Simple Skill Matching**：單次意圖匹配 → 執行 → 回應，適合簡單任務但無法處理複雜場景 [[2026-01-28-模組編排系統設計]]
- **Module Orchestrator**：加入 Planner → 任務分解 → 狀態追蹤 → 多步驟執行，SHC v3 採用此模式 [[2026-01-29-OpenSpec-TG-Agent-System-v3-分析]]
- **Hybrid Architecture**：固定模組（低成本）+ 動態 LLM 規劃（靈活）+ Agent-Creator（自動將成功執行轉化為新模組），SHC v4/v5 的設計方向 [[2026-01-31-shc-v4-hybrid-architecture]] [[2026-01-31-shc-v5-hybrid-implementation]]

### 2. Planner-Executor 分離

v3 系統的關鍵設計：外部 LLM 只輸出 Plan JSON，不負責執行。執行器照 Plan 逐步操作，失敗時可重新規劃（最多 3 次）。這解決了 LLM 直接執行時的不確定性問題 [[2026-01-29-OpenSpec-TG-Agent-System-v3-分析]] [[2026-01-31-shc-v5-hybrid-implementation]]。

### 3. 記憶系統三層架構

Agent 的長期有效性取決於記憶管理。SHC 採用 Clawdbot 啟發的三層設計：

- **SOUL.md**：身份定義、個性、邊界（全域不變）
- **AGENTS.md**：行為規範、安全規則（專案級）
- **MEMORY.md**：per-student 長期記憶（個人化）

Claude Code 源碼洩漏揭示其內部也有相似的三層記憶（CLAUDE.md 每輪重載 + context 壓縮四階段 + sub-agent 快取共享）[[2026-01-31-claude-code-agent-setup]] [[2026-03-31_Claude-Code源碼洩漏分析]] [[2026-01-30-Super-Happy-Coder-記憶系統增強-SDD]]。

### 4. Skill 系統與領域知識注入

2026 年 AI 應用的核心從「Prompt」轉向「Skill」——可系統化迭代的知識封裝。律師用 Claude 以兩人精品事務所對抗大型律所，關鍵是將十年實務判斷力編碼為 AI 技能 [[2026-03-01-AI-skill-時代來臨-律師實務應用案例]]。會計三表案例同樣展示了自建 Skill 注入台灣稅務知識的完整方法論 [[2026-04-01_Claude-Code會計三表案例分析]]。Claude Code Skills 推薦清單將能力擴展分為三層：官方必裝 → 進階工具 → Skill Creator [[2026-03-06-claude-code-skills-推薦清單]]。

### 5. 多機 Compute Plane 架構

SHC 部署於三機架構：ac-mac（知識庫 + 監控）、acmacmini2（Agent Executor + Proxy）、ac-3090（GPU Compute Plane）。Compute Plane 提供 LLM 推理、Embedding、Rerank、OCR、Toolchain 五大服務，透過 SSH Tunnel 連通 [[2026-01-29-3090-Compute-Plane-安裝規劃]] [[2026-01-29-3090-Compute-Plane-部署與網路連通紀錄]] [[2026-01-31-Super-Happy-Coder-完整系統現狀與測試分析報告]]。

### 6. DesignClaw 7-Agent Pipeline

室內設計自動化管線展示了 Agent Pipeline 的產業應用：Intake → Vision → Layout → Model → Render → Export → Deliver。每個 Agent 專責一個環節，透過事件驅動串接。核心理念是把 MetaClaw 的「抓取 → 學習 → 進化」模式套用到室內設計 [[2026-04-03_DesignClaw室內裝修自動化系統計畫]] [[2026-04-03_DesignClaw進度紀錄]]。Render Agent 使用 ComfyUI + SDXL + Dual ControlNet 在 RTX 3090 上實現批量渲染 [[2026-04-04_ComfyUI室內設計渲染技術規劃]] [[2026-04-04_DesignClaw-ComfyUI整合架構]]。

### 7. MetaClaw 自進化框架

北卡大學 AIMING Lab 的開源框架，在使用者與 LLM 之間插入透明代理，讓 Agent 能自我進化。最有趣的設計：偵測到你在開會時，自動用閒置資源訓練模型 [[2026-03-30_MetaClaw框架分析]]。DesignClaw 的架構設計直接參考了此框架的進化機制。

### 8. 成本控制與混合模式

Agent 的實際落地繞不開成本。SHC 混合模式用 HIGH tier（OpenAI gpt-4.1-nano）處理複雜任務、LOW tier（本地 vLLM Qwen2.5-7B）處理簡單任務，目標節省 70% API 成本 [[2026-01-31-SHC-混合模式配置與高可用設計]]。9 行 CLAUDE.md 就能減少 63% 輸出 token 的發現，則是從 prompt 端控制成本 [[2026-04-03_Claude-Token-Efficient-CLAUDE-md]]。OpenClaw 玩家社群中，API 花費累積超過 $1,500 USD 的案例提供了真實成本參考 [[2026-04-06_Discord作為AI-Agent控制台分析]]。

### 9. Agent 控制台與介面選型

模型聰明是一回事，介面怎麼管理 Session 才決定能否多工。Discord 三層結構（Server → Channel → Thread）天生適合多 Agent 控制台；Telegram 適合單兵快速指令；Line 基本不適合 [[2026-04-06_Discord作為AI-Agent控制台分析]]。Better Agent Terminal (BAT) 則用 Electron + xterm.js 統一管理多個 CLI Agent [[2026-04-09_Better-Agent-Terminal統一CLI調度中心分析]] [[2026-04-09_gemgate-BAT-Copilot整合實作指南]]。

### 11. Anthropic Project Deal：AI 代理人市集與隱形不平等

Anthropic 於 2025 年 12 月執行為期一週的 Project Deal 內部實驗：69 名員工各持 100 美元，全程由 Claude 代理人在 Slack 自主議價購買實體物品，共完成 186 筆交易、總值逾 4,000 美元。實驗跨越四個平行市集，比較 Opus 4.5、Haiku 4.5 等不同模型作為議價代理人時的客觀成果差異 [[2026-04-26-Anthropic-Project-Deal-代理人市集實驗]]。

核心發現稱為「隱形不平等」（agent quality gap）：當 Agent 由較強模型代表時客觀上獲得更佳結果，但弱模型（Haiku 4.5）使用者完全察覺不到自己吃虧——感知滿意度與客觀收益脫鉤。這引發了代理時代的公平性疑問：若 AI 能力差距對使用者不透明，算法性不平等將以「服務滿意」的假象穩定存在。此實驗也驗證了「多代理議價」作為研究場景的可行性，為後續 Agent 協作、競爭動態的系統研究提供方法論藍圖 [[2026-04-26-Anthropic-Project-Deal-代理人市集實驗]]。

### 10. 垂直領域 Agent 實戰：政府補助助手案例

Hermes Agent（Nous Research 開源框架）× Telegram × LLM Wiki × ChatGPT 的組合，實現了「AI 計劃書補助助手」的完整閉環：每日定期巡查補助公告並下載資料、根據申請須知自動產生訪綱與索資清單、針對特定計劃做即時 PDF 問答、具備長短期記憶追蹤各案進度。架構亮點：Hermes Agent 負責工具呼叫與記憶編排，LLM Wiki 提供領域知識庫，Telegram 作為顧問的行動指令介面。這個案例展示了用開源框架快速組裝「AI 員工」的可行路徑，而非從頭自建 Agent 系統 [[2026-04-18_Hermes-Agent-AI補助案助手架構分析與機會研究]]。

### 10. WFGY 語義防火牆

WFGY Problem Map 定義了 16 種 RAG/Agent 故障模式及修復方法。核心理念：在生成輸出之前檢查系統狀態（語義防火牆），而非事後打補丁。已被 RAGFlow、LlamaIndex 等主流框架收錄 [[2026-03-01-WFGY-RAG-16問題清單]]。

## 關鍵發現

> **從「寫程式」到「定義規章」的典範轉移**：OpenClaw 的出現標誌著核心戰場從程式碼轉移到 agents.md 與 skills.md 這兩份檔案。這是從程式設計師到系統工程師的身份轉變。 [[2026-02-06-OpenClaw-AI-Agent-新時代思考]]

> **80/20 相位轉移**：Andrej Karpathy 在 2 個月內從 80% 手動 + 20% Agent 翻轉為 80% Agent + 20% 人工，稱其為二十年程式生涯最大的工作流程變革。 [[2026-01-27-andrej-karpathy-ai-coding-workflow]]

> **通用 AI 勝過垂直 AI**：律師案例證明，通用型 Claude + 自建 Skill 的組合，比專門法律 AI 產品更有效。關鍵是把人的判斷力編碼進 Skill。 [[2026-03-01-AI-skill-時代來臨-律師實務應用案例]]

> **Cisco 五步驟的最大卡關點是「劃清邊界」**：沒有邊界的 AI 會自行擴張任務範疇。Cisco 框架偏「設計時」架構規範，會計五步法偏「執行時」工作流程，合併使用形成完整落地方法論。 [[2026-04-01_Cisco五步驟vs會計三表五步法對照分析]]

> **本地硬體勝過雲端（對非工程師而言）**：Mac Mini 能看到畫面、截圖 debug，體驗遠勝 AWS EC2 + Linux 終端機。「看不到在幹嘛」的焦慮感是真實的。 [[2026-03-04-openclaw-agent-實戰經驗]]

> **Heartbeat Protocol 取代 Agile 站會**：Agent 定期喚醒檢查任務、自動工作，減少人類協調成本。SHC 和 Clawdbot 都實作了此機制。 [[2026-03-04-openclaw-agent-實戰經驗]] [[2026-01-28-增強型-Multi-Agent-系統設計]]

> **Claude Code 內部架構遠比表面複雜**：源碼洩漏揭示 KAIROS（常駐背景 Agent）、ULTRAPLAN（30 分鐘遠端規劃）、Coordinator 多 Agent 協調、Agent Swarm 等尚未公開功能。 [[2026-03-31_Claude-Code源碼洩漏分析]]

> **SHC 測試覆蓋率 61.8%（21/34 有效通過）**：切換到 Claude Backend 後比 Gemini 改善 +3 通過，但仍有 13 項失敗。Phase 6 Compute Plane 達 87.5%。 [[2026-01-30-Super-Happy-Coder-修復後完整測試報告]] [[2026-01-31-SHC-Phase6-Compute-Plane-測試報告]]

> **VibeResearch 的學術驗證**：史丹佛教授用 Claude Code 在不到一小時內擴展已發表論文，準確率 29/30 縣正確、數據相關係數 > 0.999。 [[2026-01-25-VibeResearch-Claude-Code寫論文]]

> **Project Deal 揭示「隱形不平等」**：Haiku 4.5 使用者在 Slack 議價市集中客觀上吃了虧，但感知滿意度與真實收益完全脫鉤——他們根本不知道自己的代理人比別人弱。這是 Agent 品質差距的倫理面向：能力差異若對使用者不透明，將以「滿意」的假象穩定存在，成為難以干預的結構性不平等。 [[2026-04-26-Anthropic-Project-Deal-代理人市集實驗]]

## 跨筆記關聯

### SHC 演進軸線（v2 → v3 → v4 → v5）

SHC 的架構演進形成清晰的技術債歸還路徑：v2 Simple Skill Matching [[2026-01-28-模組編排系統設計]] → v3 OpenSpec 加入 Planner-Executor 分離與容量規劃 [[2026-01-29-OpenSpec-TG-Agent-System-v3-分析]] → v4 Hybrid Architecture 結合固定模組與動態規劃 [[2026-01-31-shc-v4-hybrid-architecture]] → v5 實作 dynamic_planner + agent_creator [[2026-01-31-shc-v5-hybrid-implementation]]。但截至 2026-03-03，SHC 服務已停止運作，因 ac-3090 vLLM 停機導致 HealthMonitor 反覆切換狀態並發送假警報 [[shc-service-review]]。

### Clawdbot 的持續影響

Clawdbot（OpenClaw 前身）的設計模式被反覆引用為 Agent 架構的「最佳實踐模板」：SOUL.md/AGENTS.md/MEMORY.md 三層記憶 [[2026-01-31-claude-code-agent-setup]]、PTY + Background 執行 [[2026-01-28-AI-Agent-架構分析-Clawdbot-vs-Happy-Coder]]、Heartbeat 主動喚醒 [[2026-01-28-增強型-Multi-Agent-系統設計]]。SHC 和 DesignClaw 的設計都大量借鑑了 Clawdbot。

### DesignClaw 與 MetaClaw 的連接

DesignClaw 不只是一個室內設計工具，它是 MetaClaw 自進化框架的產業應用試驗場 [[2026-04-03_DesignClaw室內裝修自動化系統計畫]] [[2026-03-30_MetaClaw框架分析]]。同時，它的商業模式分析引入了 MEDVi 輕資產框架，將技術架構與商業策略對齊 [[2026-04-06_DesignClaw危老都更輕資產商業模式]]。

### 方法論收斂：Cisco 五步驟 × 會計五步法

兩套看似無關的方法論在 Agent 落地上互補：Cisco 偏設計時（身份定位、劃清邊界、選擇工具、建立護欄、疊代優化），會計五步法偏執行時（領域 Skill → 分輪處理 → 互動補齊 → 紅隊演練 → 人工確認）[[2026-04-01_Cisco五步驟vs會計三表五步法對照分析]] [[2026-04-01_Claude-Code會計三表案例分析]]。

### 控制台選型的演進

從 Telegram 單線程 → Discord 多層結構 → BAT 統一桌面終端，反映了 Agent 管理從「一對一指令」走向「多 Agent 並行調度」的需求演進 [[2026-04-06_Discord作為AI-Agent控制台分析]] [[2026-04-09_Better-Agent-Terminal統一CLI調度中心分析]]。

### API 相容性是持續痛點

SHC 遭遇 OpenAI GPT-5 系列 API 參數變更（`max_tokens` → `max_completion_tokens`、Temperature 固定 1.0），導致無法直接升級模型 [[shc-openai-api-compatibility]]。這類問題在 Agent 長期運作中反覆出現。

## 待探索方向

1. **SHC 復活計畫**：服務已停止近 6 週 [[shc-service-review]]，需決定是修復現有架構還是基於 v5 混合架構重建。Agent-Creator 自動模組化的效果尚未在生產環境驗證。

2. **MetaClaw 自進化的實際效果**：理論上「你開會時 AI 在進化」很吸引人，但筆記中尚未有實際部署的效果數據 [[2026-03-30_MetaClaw框架分析]]。

3. **DesignClaw Render Agent 之後的環節**：Vision/Layout/Render 已完成，Export Agent 和 Deliver Agent 尚未開發 [[2026-04-03_DesignClaw進度紀錄]]。從技術 POC 到可交付產品還有多遠？

4. **Agent 安全與合規**：WFGY 語義防火牆提供了故障診斷框架 [[2026-03-01-WFGY-RAG-16問題清單]]，但在多 Agent 協作場景下的安全邊界、資料隔離、審計追蹤仍待系統化設計。

5. **非工程師的 Agent 使用方法論**：行銷人案例 [[2026-03-04-SEO行銷人用Claude-Code工作流實戰]] [[2026-03-04-行銷人使用claude-code實戰指南]] 開了頭，但從「消除等待」到「系統化運用」的完整方法論尚未形成。

6. **成本模型的系統化**：散見於各筆記的成本數據（OpenAI Rate Limits [[2026-01-30-OpenAI-API-Rate-Limits]]、OpenClaw $1,500+ [[2026-04-06_Discord作為AI-Agent控制台分析]]、Token Efficient CLAUDE.md [[2026-04-03_Claude-Token-Efficient-CLAUDE-md]]）需要整合為可量化的 Agent ROI 框架。

7. **BAT × gemgate 整合落地**：統一調度中心的架構已清楚 [[2026-04-09_gemgate-BAT-Copilot整合實作指南]]，但尚未進入實作階段。

8. **垂直領域 Agent 的商業化路徑**：Hermes Agent 補助案助手案例 [[2026-04-18_Hermes-Agent-AI補助案助手架構分析與機會研究]] 展示了以開源框架快速組裝垂直 AI 員工的可行性。SBIR/SIIR/CITD 補助輔導顧問市場有多大？類似模式能否複製到其他高文件負荷的專業服務（如會計師事務所、法律事務所）？

9. **隱形不平等的緩解機制**：Project Deal 揭示代理人品質差距對使用者不透明 [[2026-04-26-Anthropic-Project-Deal-代理人市集實驗]]。如何設計「能力標示」或「議價代理人評級」機制，讓使用者在部署前理解模型選擇的後果？這是 Agent 治理與 AI Safety 的交叉議題，值得進一步研究。
