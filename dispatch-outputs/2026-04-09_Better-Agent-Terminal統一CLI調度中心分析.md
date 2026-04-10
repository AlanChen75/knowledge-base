---
title: "Better Agent Terminal：統一 CLI Agent 調度中心可行性分析"
date: 2026-04-09
category: tech/tools
tags: [CLI, agent-terminal, Claude-Code, Codex, Gemini-CLI, electron, xterm, multi-agent, dispatch]
type: analysis
source: "https://github.com/Grepsaw/better-agent-terminal"
project: gemgate
priority: high
status: active
---

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

- 多 Agent 並行執行（PTY 隔離）
- Agent 預設系統（新增 Agent 只需 config）
- 工作區隔離

### ❌ 需要新增

| 缺失能力 | 說明 | 參考方案 |
|----------|------|---------|
| **智慧路由引擎** | 根據任務類型自動派發到合適 Agent | CCG Workflow 的 `/route` 邏輯 |
| **跨 Agent 上下文共享** | A 的輸出自動成為 B 的輸入 | 共享 clipboard 或 MCP context |
| **安全審查層** | 外部 Agent 的修改需審查後才套用 | CCG 的 patch-only 模型 |
| **Token 壓縮** | 大型 codebase 輸入前先壓縮 | RTK 嵌入作為中間層 |
| **MCP 自動註冊** | 根據專案自動掛載相關 MCP server | wmux 的 auto-register 機制 |

---

## 與已研究工具的比較

| 維度 | BAT | CCG Workflow | CLI_Runner | RTK | gemgate |
|------|-----|-------------|------------|-----|---------|
| **定位** | 終端 UI 聚合器 | slash 命令調度 | 任務調度 + worktree | Token 壓縮代理 | API 統一介面 |
| **多 Agent** | ✅ 視覺化並行 | ✅ 命令式路由 | ❌ 單 Agent | ❌ 單 Agent | ✅ API 層路由 |
| **UI** | Electron 桌面 | CLI 內嵌 | CLI | CLI | API/CLI |
| **安全模型** | ❌ 無 | ✅ patch 審查 | ❌ | ❌ | ❌ |
| **Token 優化** | ❌ | ❌ | ❌ | ✅ 60-90% 壓縮 | ❌ |
| **互補性** | 作為框架基座 | 路由邏輯參考 | worktree 參考 | 嵌入壓縮層 | API 層整合 |

---

## 建議擴展路線圖

### Phase 1：基礎強化
- Fork 後加入 gemgate 作為新 Agent Preset
- 加入工作目錄自動偵測（根據 .git 位置設定 cwd）

### Phase 2：智慧路由
- 參考 CCG Workflow 實作任務分類器
- 規則引擎：前端任務 → Gemini，後端 → Codex，架構決策 → Claude

### Phase 3：安全層
- 外部 Agent 輸出走 patch 模式
- Claude 作為審查者，自動 review 後才 apply

### Phase 4：Token 優化
- 嵌入 RTK 或類似壓縮層
- 大檔案自動壓縮後再送給 Agent

### Phase 5：上下文共享
- 跨 Agent 共享 context buffer
- Agent A 完成後自動把 summary 注入 Agent B

### Phase 6：MCP 整合
- 根據專案 .claude 配置自動註冊 MCP server
- 所有 Agent 共享 MCP 工具

---

## 注意事項

- 原始 repo 擁有者是 **Grepsaw**，不是 scandnavik（確認 fork 來源）
- 專案較新，star 數增長快但成熟度待觀察
- Electron 應用有記憶體開銷，多 PTY 同時跑需注意資源

---

## 結論

BAT 作為「統一 CLI Agent 調度中心」的框架基座非常合適。它解決了最基礎的問題（多 Agent 並行 + 視覺化管理），而你需要的智慧路由、安全審查、Token 壓縮這些進階功能，都可以從 CCG Workflow、RTK、wmux 等專案借鏡，逐步疊加上去。最終目標是讓 BAT 成為你的 gemgate 的桌面端入口。

---

## Sources

- [Grepsaw/better-agent-terminal](https://github.com/Grepsaw/better-agent-terminal)
- [fengshao1227/ccg-workflow](https://github.com/fengshao1227/ccg-workflow)
- [rtk-ai/rtk](https://github.com/rtk-ai/rtk)
- [openwong2kim/wmux](https://github.com/openwong2kim/wmux)
