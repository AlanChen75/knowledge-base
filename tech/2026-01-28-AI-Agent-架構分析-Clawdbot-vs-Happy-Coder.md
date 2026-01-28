---
title: AI Agent 架構分析 - Clawdbot vs Happy Coder vs VS Code
date: 2026-01-28
category: tech
tags: [AI, agent, clawdbot, happy-coder, claude, codex, 架構分析]
---

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
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
│         └────────────────┼─────────────────────┘             │
│                          ▼                                   │
│              ┌───────────────────────┐                       │
│              │   Session Manager     │                       │
│              │   ┌───────────────┐   │                       │
│              │   │ AGENTS.md     │◄──┼── 行為規範            │
│              │   │ SOUL.md       │◄──┼── 身份/個性           │
│              │   │ MEMORY.md     │◄──┼── 長期記憶           │
│              │   │ memory/*.md   │◄──┼── 每日日誌           │
│              │   └───────────────┘   │                       │
│              └───────────┬───────────┘                       │
│                          ▼                                   │
│              ┌───────────────────────┐                       │
│              │     Skills System     │ ◄── 50+ skills        │
│              │  (coding-agent, github, obsidian, etc.)       │
│              └───────────┬───────────┘                       │
│                          ▼                                   │
│              ┌───────────────────────┐                       │
│              │   Process Manager     │                       │
│              │   - PTY allocation    │                       │
│              │   - Background jobs   │                       │
│              │   - Session tracking  │                       │
│              └───────────────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

### 關鍵機制

#### 1.1 Workspace 隔離
每個 agent 有獨立的 sandbox 目錄：`~/.clawdbot/sandboxes/agent-xxx/`

#### 1.2 Context Files（核心差異）

| 檔案 | 用途 |
|------|------|
| `AGENTS.md` | 行為規範、記憶讀取流程、安全規則 |
| `SOUL.md` | 身份定義、個性、邊界 |
| `MEMORY.md` | 長期記憶（只在主 session 載入） |
| `memory/YYYY-MM-DD.md` | 每日日誌 |
| `TOOLS.md` | 本地工具設定（相機名稱、SSH hosts 等） |

每個 session 開始時會讀取這些檔案，讓 AI 有**持續的身份和記憶**。

#### 1.3 Skills 系統
每個 skill 有 `SKILL.md` 說明文件，例如 `coding-agent/SKILL.md`：
- 如何呼叫 Codex/Claude CLI
- PTY 參數設定
- Background process 管理
- 範例命令

#### 1.4 Process Manager
```bash
# 啟動背景任務（PTY 是關鍵！）
bash pty:true workdir:~/project background:true command:"codex --yolo 'Build feature X'"

# 監控進度
process action:log sessionId:XXX
process action:poll sessionId:XXX

# 發送輸入
process action:submit sessionId:XXX data:"yes"
```

#### 1.5 Heartbeat 機制
定期喚醒 AI 檢查：
- 信箱有新郵件嗎？
- 行事曆有即將到來的事件嗎？
- 背景任務完成了嗎？
- 需要更新 MEMORY.md 嗎？

---

## 2. Happy Coder 架構

### 系統架構圖

```
┌─────────────────────────────────────────────────────────────┐
│                     Happy Mobile App                         │
│                          │                                   │
│                          ▼                                   │
│              ┌───────────────────────┐                       │
│              │   Happy Cloud API     │                       │
│              │   (WebSocket relay)   │                       │
│              └───────────┬───────────┘                       │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Happy Daemon (local)                      │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Session Manager                         │    │
│  │  - Spawn Claude/Codex CLI as child process          │    │
│  │  - Route messages via socket.io                      │    │
│  └─────────────────────────────────────────────────────┘    │
│                          │                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Permission Handler                      │    │
│  │  - permissionMode: default/plan/acceptEdits/yolo    │    │
│  │  - Forward approval requests to mobile app           │    │
│  └─────────────────────────────────────────────────────┘    │
│                          │                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │         Claude/Codex CLI (child process)            │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### 設計理念
- **透明代理**：把手機指令轉發給 CLI
- **權限控制**：在手機上確認權限
- **輕量級**：不需要複雜的 workspace 設定

### 沒有的功能
- 持久記憶
- Skill 系統
- Background process 管理
- Context injection

---

## 3. VS Code Claude Extension

```
┌─────────────────────────────────────────────────────────────┐
│                      VS Code Extension                       │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              WebView Panel / Terminal                │    │
│  │  - Direct UI integration                             │    │
│  │  - File system access via VS Code API               │    │
│  └─────────────────────────────────────────────────────┘    │
│                          │                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │           Claude Code Process (embedded)             │    │
│  │  - Direct Anthropic API calls                        │    │
│  │  - No cloud relay                                    │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. 核心差異比較

| 特性 | Clawdbot | Happy Coder | VS Code |
|------|----------|-------------|---------|
| **中介層** | Gateway + Skills + Process Manager | Cloud Relay + Permission Handler | VS Code Extension |
| **記憶系統** | ✅ MEMORY.md + 每日日誌 | ❌ 無 | ❌ 無 |
| **任務持續性** | ✅ Background process + heartbeat | ❌ 只有 session 期間 | ❌ 只有 session 期間 |
| **多 CLI 整合** | ✅ Codex, Claude, OpenCode, Pi | ⚠️ 選一個 | ❌ 只有 Claude |
| **PTY 支援** | ✅ `pty:true` 參數 | ❌ 透過 stdin/stdout | ✅ 內建 terminal |
| **並行任務** | ✅ 多 background sessions | ❌ 單一 session | ❌ 單一 session |
| **Context 注入** | ✅ AGENTS.md, SOUL.md 等 | ⚠️ 只有 change_title | ❌ 無 |

---

## 5. 為什麼 Clawdbot 能完成更複雜的任務？

### 5.1 持續的身份和記憶
每個 session 開始時讀取 SOUL.md、AGENTS.md、MEMORY.md，AI 知道：
- 自己是誰
- 該怎麼行動
- 之前發生什麼

### 5.2 Skills 系統
每個 skill 有詳細說明文件，AI 可以**查閱說明書**來正確使用工具。

### 5.3 Background Process + PTY
```bash
bash pty:true workdir:~/project background:true command:"codex --yolo 'Build feature X'"
```
- `pty:true` - 分配偽終端，讓 CLI 正常運作
- `background:true` - 不阻塞，可並行多個任務
- `process action:log` - 隨時檢查進度

### 5.4 Heartbeat 機制
定期喚醒 AI 主動工作，不只是被動回應。

---

## 6. 實作建議

如果要建構類似 Clawdbot 的能力，核心是：

1. **Workspace 結構**
   - AGENTS.md（行為規範）
   - SOUL.md（身份定義）
   - MEMORY.md（長期記憶）

2. **Skills 系統**
   - 每個工具有說明文件
   - 標準化的呼叫方式

3. **Process 管理**
   - PTY 分配
   - Background 執行
   - Polling 機制

4. **Heartbeat/Cron**
   - 定期喚醒
   - 主動檢查任務

---

## 7. 相關連結

- Clawdbot 文件：https://docs.clawd.bot/
- Happy Coder：https://happy.engineering/
- Claude Code：https://claude.ai/code
