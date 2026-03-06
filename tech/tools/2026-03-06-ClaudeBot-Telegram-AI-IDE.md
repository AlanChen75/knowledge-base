---
title: ClaudeBot - 透過 Telegram 打造的行動 AI 開發環境
date: 2026-03-06
source: https://github.com/Jeffrey0117/ClaudeBot
category: tech/tools
tags: [Claude, Telegram, Bot, AI-IDE, 遠端開發, MCP, 語音轉文字]
type: article
raw_file: ../raw/2026-03/2026-03-06-110237-text.txt
difficulty: ⭐⭐⭐⭐
author: Jeffrey0117
---

# ClaudeBot - 透過 Telegram 打造的行動 AI 開發環境

## 📊 元資訊
- **難度**：⭐⭐⭐⭐
- **來源類型**：開源專案 + 社群分享
- **作者**：Jeffrey0117
- **筆記時間**：2026-03-06 11:02

## 📌 摘要
ClaudeBot 是一個透過 Telegram Bot 串接 Claude CLI 的開發工具，讓開發者可以用手機遠端控制 AI 編輯程式碼。不同於一般的聊天機器人包裝，它是完整的開發平台，支援即時串流、多層記憶系統、語音輸入、跨機器遠端協作等功能。作者表示透過這個工具已經產生超過 20 萬行實際使用的程式碼。

## 🏷️ 標籤分類
- **大分類**：tech
- **小分類**：tools
- **核心關鍵字**：Telegram Bot、Claude Code、AI IDE、遠端開發

## 🔑 關鍵要點

1. **從 VSCode 到 CLI 再到 Telegram 的演進**
   - VSCode 插件 → CLI + Windows Terminal 多分頁 → Telegram Bot
   - Telegram Bot 成為「最順手的 IDE」，隨時隨地可用

2. **即時程式碼編輯**
   - 發送 Telegram 訊息 → Claude 改寫程式碼 → 每 300ms 更新的即時串流輸出
   - Claude 指令直接在本地機器執行

3. **四層記憶系統**
   - **Bookmarks**：快速程式碼片段
   - **Context Pins**：自動注入的上下文
   - **AI Memory Base**：長期知識儲存
   - **Vault**：所有訊息索引，可搜尋的歷史紀錄

4. **AI 指令自動執行**
   - Claude 可在回應中嵌入特殊指令：`@cmd(/restart)`、`@file(report.md)`
   - Bot 自動攔截並執行，實現自主行動

5. **技術架構特色**
   - 多機器人支援：用 git worktrees 從同一份程式碼跑 5+ 個獨立 bot
   - 任務佇列系統：跨 bot 檔案鎖定，循序執行
   - 語音管道：本地 Sherpa-ONNX 離線轉錄 + 可選 Gemini 精煉
   - 遠端配對：WebSocket 連線 + 10 種 MCP 工具控制遠端機器

6. **安全機制**
   - Chat ID + bcrypt 認證
   - 速率限制、zod 輸入驗證
   - 保護關鍵檔案（.env、.sessions.json）

7. **使用門檻**
   - 需要 Claude Code Pro 訂閱（透過 CLI 使用）
   - Node.js 20+
   - 一鍵安裝：`npx claudebot-app`（互動式設定精靈）

## 💬 金句摘錄
> "使用 Claude Code 的我原本都在 VSCode 開插件，後來改用 CLI 跟 windows terminal 開一堆 pane，直到龍蝦流行後，就改串 telegram bot 變成我最新最順手的 IDE。"
> — Jeffrey0117

> "通過這個玩具 ClaudeBot 已經幫我幹出 20 萬行以上的代碼了，都是實際在使用的專案。"
> — Jeffrey0117

## 🧠 概念連結
- **Happy Coder**：本機現有的 Claude Code SDK 服務，同樣透過 Telegram Bot 互動
- **MCP (Model Context Protocol)**：ClaudeBot 使用 10 種 MCP 工具進行遠端機器控制
- **語音轉文字管道**：與本機 Gemini Image API 類似，都是整合外部 AI 服務的本地 API 封裝
- **Git Worktrees**：多 bot 共用程式碼的架構，可參考用於本機多服務部署

## 💡 與我的連結

### 與現有系統的對比
本機的 **Happy Coder** 與 ClaudeBot 核心理念相同，但實作方式不同：

| 項目 | Happy Coder (本機) | ClaudeBot |
|------|-------------------|-----------|
| **Claude 接口** | 直接呼叫 `claude` CLI | 同樣使用 Claude CLI |
| **Session 管理** | 單 bot 多 session 切換 | 多 bot 實例 (git worktrees) |
| **記憶系統** | Session 狀態持久化 | 四層記憶（Bookmarks/Pins/Memory/Vault） |
| **任務佇列** | ❌ 無 | ✅ 跨 bot 檔案鎖定 |
| **語音輸入** | ❌ 無 | ✅ Sherpa-ONNX + Gemini |
| **遠端控制** | SSH 執行腳本 | WebSocket + MCP 工具 |
| **即時串流** | ❌ 無 | ✅ 300ms 更新 |

### 可借鑑的功能
1. **四層記憶系統**：可整合到 Happy Coder
   - Bookmarks → 常用指令快捷
   - Context Pins → 自動注入系統資訊
   - Memory → 與知識庫整合
   - Vault → 對話歷史搜尋（已有 conv-track）

2. **AI 指令攔截機制** (`@cmd()`, `@file()`)
   - Happy Coder 可擴充類似功能
   - 讓 Claude 自主執行系統指令

3. **即時串流輸出**
   - 現在 Happy Coder 是等全部執行完才回覆
   - 可改為每 1-2 秒推送進度

4. **語音輸入管道**
   - 本機有 GPU (ac-3090)，可跑 Whisper 或 Sherpa-ONNX
   - 語音 → 文字 → Happy Coder 執行

5. **任務佇列系統**
   - 避免同時執行多個 Claude 指令衝突
   - 可用 Redis 或簡單的檔案鎖

## ✅ 行動項目
- [x] 保存 ClaudeBot 資訊到知識庫
- [ ] 研究 ClaudeBot 的 git worktrees 多 bot 架構
- [ ] 評估將四層記憶系統整合到 Happy Coder 的可行性
- [ ] 測試 Sherpa-ONNX 在 ac-3090 上的語音轉文字效能
- [ ] 設計 Happy Coder 的即時串流輸出機制
- [ ] 研究 MCP 工具的應用場景

## 📝 我的註解與思考

### 開發模式的演進
這個演進路徑很有啟發性：
```
VSCode 插件（IDE 綁定）
    ↓
CLI + Terminal Panes（本地化，多視窗）
    ↓
Telegram Bot（隨時隨地，手機可用）
```

這證明了「最好的 AI IDE 不是在桌面，而是在最容易存取的地方」。

### 20 萬行代碼的意義
不是玩具專案，而是實際生產環境使用的工具。這表示：
- AI 輔助開發已經成熟到可以取代大部分手工編碼
- Telegram 作為開發界面的可行性（流量截圖證明實際使用）

### 與本機系統整合的可能性
本機已有：
- Happy Coder（Telegram + Claude CLI）
- 知識庫系統（Markdown + Git）
- 多機器 SSH 互連（Tailscale）
- Gemini Image API（圖片生成）

可以打造：
- **語音 → 文字 → Happy Coder 執行** 管道
- **四層記憶 + 知識庫** 整合
- **跨機器任務佇列**（ac-mac 排程 → ac-3090 執行 GPU 任務）
- **即時進度推播**（每 2 秒更新 Telegram 訊息）

### Git Worktrees 的應用
ClaudeBot 用 worktrees 跑多個 bot 實例，本機可以用來：
- 同一份 server-monitor 程式碼跑多個監控服務
- 不同機器（ac-mac, ac-3090, ac-rpi5）各自 checkout 不同 branch

### 安全設計的參考
- bcrypt 認證（本機目前只用 Chat ID）
- zod 輸入驗證（可防止注入攻擊）
- 關鍵檔案保護（已有 pre-commit hook，但可加強執行時檢查）

## 🎬 延伸學習 - YouTube
- [搜尋：Claude Code Telegram Bot 開發實戰](https://www.youtube.com/results?search_query=Claude+Code+Telegram+Bot)
- [搜尋：Sherpa-ONNX 語音轉文字教學](https://www.youtube.com/results?search_query=Sherpa-ONNX+speech+recognition)

## 🔗 延伸閱讀
- [ClaudeBot 官方文件](https://jeffrey0117.github.io/ClaudeBot)
- [ClaudeBot GitHub Repo](https://github.com/Jeffrey0117/ClaudeBot)
- [Model Context Protocol (MCP) 官方文件](https://modelcontextprotocol.io/)
- [Git Worktrees 官方文件](https://git-scm.com/docs/git-worktree)
- [Sherpa-ONNX GitHub](https://github.com/k2-fsa/sherpa-onnx)

## ℹ️ 原文資訊
- **原始輸入**：[查看原始資料](../raw/2026-03/2026-03-06-110237-text.txt)
- **來源連結**：
  - 官網：https://jeffrey0117.github.io/ClaudeBot
  - GitHub：https://github.com/Jeffrey0117/ClaudeBot
- **收錄時間**：2026-03-06 11:02:37
