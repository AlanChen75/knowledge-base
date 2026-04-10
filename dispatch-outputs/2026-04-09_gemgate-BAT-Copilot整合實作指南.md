---
title: "gemgate × BAT × Copilot：統一 CLI Agent 調度中心完整實作指南"
date: 2026-04-09
category: tech/architecture
tags: [gemgate, BAT, better-agent-terminal, copilot, CLI, agent-dispatch, architecture, implementation]
type: implementation-guide
project: gemgate
priority: high
status: active
---

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
│              WebSocket Bridge                    │
└──────────────────────┬──────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────┐
│  gemgate — Headless Router Daemon                │
│                                                  │
│  ┌─────────────┐  ┌──────────────┐              │
│  │ Task Router │  │ Fallback     │              │
│  │ (規則引擎)   │  │ Chain        │              │
│  └──────┬──────┘  │ claude →     │              │
│         │         │ copilot →    │              │
│         │         │ gemini →     │              │
│         │         │ codex        │              │
│         │         └──────────────┘              │
│  ┌──────┴──────────────────────────┐            │
│  │ Agent Adapters                   │            │
│  │ ┌────────┐ ┌────────┐ ┌──────┐ │            │
│  │ │claude  │ │copilot │ │gemini│ │            │
│  │ │adapter │ │adapter │ │adapt.│ │            │
│  │ └────────┘ └────────┘ └──────┘ │            │
│  └─────────────────────────────────┘            │
└─────────────────────────────────────────────────┘
```

**關鍵設計**：gemgate 是 headless daemon（無 UI），負責「決定誰處理什麼」。BAT 是 UI shell，負責「同時管理多個終端 session」。兩者透過 WebSocket 橋接。

---

## Chapter 1：GitHub Copilot CLI 最新能力（2026 Q1）

### 1.1 已 GA 的功能

Copilot CLI 於 2026/02/25 正式 GA，三大能力：

| 命令 | 功能 | 適合場景 |
|------|------|---------|
| `gh copilot suggest` | 根據自然語言生成 CLI 命令 | DevOps、Git 操作、系統管理 |
| `gh copilot explain` | 解釋任意 CLI 命令 | 學習、除錯 |
| Agent Mode | 完整 agentic 工作流 | 複雜多步驟任務 |

### 1.2 Agent Mode 內建 Agent

- **Explore Agent**：掃描 codebase 回答架構問題
- **Task Agent**：執行多步驟開發任務
- **Code Review Agent**：自動 review PR
- **Plan Agent**：規劃實作方案

### 1.3 Copilot SDK（2026/04 Public Preview）

最大突破：**可程式化嵌入任何 Node/Python/Go 應用**。

```javascript
// 概念範例：在 gemgate 中呼叫 Copilot SDK
import { CopilotClient } from '@github/copilot-sdk';

const copilot = new CopilotClient({
  token: process.env.GITHUB_TOKEN,
  model: 'claude-opus-4-6', // Copilot 支援多模型選擇
});

const result = await copilot.chat({
  messages: [{ role: 'user', content: 'Review this PR diff...' }],
  tools: [/* MCP tools */],
});
```

### 1.4 Copilot 原生 MCP 支援

Copilot CLI 已支援 MCP server 掛載，等於你的 MCP 工具可以同時被 Claude Code 和 Copilot 使用。

---

## Chapter 2：Copilot 在 gemgate 中的角色定位

### 2.1 不是備援，是「GitHub 專家」

Copilot 最強的場景不是寫 code（Claude 更好），而是 **GitHub 生態系操作**：

| 場景 | 最佳 Agent | 原因 |
|------|-----------|------|
| PR 建立、Review、Merge | **Copilot** | 原生 GitHub API 整合 |
| Issues 分類和回覆 | **Copilot** | 原生 context |
| GitHub Actions 除錯 | **Copilot** | 直接讀 workflow logs |
| Deploy 狀態查詢 | **Copilot** | 原生 API |
| 架構設計討論 | Claude | 推理能力 |
| 前端 UI 實作 | Gemini | 視覺理解 + 快速迭代 |
| 重構 / 大範圍修改 | Codex | 平行執行 |

### 2.2 三模式 Adapter 設計

```javascript
// gemgate/adapters/copilot.js
class CopilotAdapter {
  constructor(config) {
    this.modes = {
      // Mode 1: CLI Agent（最完整）
      agent: { cmd: 'gh', args: ['copilot', '--agent'] },
      
      // Mode 2: Suggest（輕量，只生成命令）
      suggest: { cmd: 'gh', args: ['copilot', 'suggest'] },
      
      // Mode 3: SDK（程式化呼叫，最靈活）
      sdk: { client: new CopilotClient({ token: this.token }) }
    };
  }
  
  async execute(task) {
    // GitHub 相關任務用 agent mode
    if (task.context.includes('github') || task.type === 'pr-review') {
      return this.runAgent(task);
    }
    // 命令生成用 suggest mode
    if (task.type === 'command-gen') {
      return this.runSuggest(task);
    }
    // 程式化整合用 SDK
    return this.runSDK(task);
  }
}
```

---

## Chapter 3：gemgate 路由引擎設計

### 3.1 路由規則配置

```yaml
# gemgate.config.yml
router:
  rules:
    # GitHub 操作 → Copilot 優先
    - match:
        keywords: [pr, issue, actions, deploy, github, review]
        files: ['.github/**']
      route: copilot
      fallback: claude
    
    # 前端任務 → Gemini 優先（參考 CCG Workflow）
    - match:
        files: ['*.tsx', '*.jsx', '*.vue', '*.css']
        keywords: [component, UI, layout, responsive]
      route: gemini
      fallback: claude
    
    # 後端 / 系統 → Codex 優先
    - match:
        files: ['*.py', '*.go', '*.rs']
        keywords: [API, backend, database, migration]
      route: codex
      fallback: claude
    
    # 架構 / 設計 / 複雜推理 → Claude 永遠優先
    - match:
        keywords: [architecture, design, plan, strategy, debug]
      route: claude
      fallback: copilot

  # Fallback Chain
  fallback_chain: [claude, copilot, gemini, codex]
  
  # 超時自動切換
  timeout_ms: 30000
  retry_next_on_error: true
```

### 3.2 Fallback Chain 邏輯

```javascript
// gemgate/router.js
async function routeWithFallback(task, chain) {
  for (const agentName of chain) {
    try {
      const adapter = adapters.get(agentName);
      if (!adapter.isAvailable()) continue;
      
      const result = await Promise.race([
        adapter.execute(task),
        timeout(config.timeout_ms)
      ]);
      
      // 記錄成功路由（用於學習）
      metrics.record(agentName, task.type, 'success');
      return { agent: agentName, result };
      
    } catch (err) {
      metrics.record(agentName, task.type, 'fail', err);
      continue; // 試下一個
    }
  }
  throw new Error('All agents in fallback chain failed');
}
```

---

## Chapter 4：BAT UI 整合

### 4.1 新增 gemgate 控制面板

在 BAT 的 React UI 加入路由狀態顯示：

```
┌─────────────────────────────────────────┐
│  gemgate router: ● active               │
│  ┌──────┬─────────┬──────────┬────────┐ │
│  │Claude│ Copilot │ Gemini   │ Codex  │ │
│  │  ●   │   ●     │   ○      │   ○    │ │
│  │active│ standby │ offline  │offline │ │
│  └──────┴─────────┴──────────┴────────┘ │
│                                         │
│  Last route: PR review → Copilot (1.2s) │
│  Fallback used: 0 times today           │
└─────────────────────────────────────────┘
```

### 4.2 Agent Preset 配置擴展

```json
// BAT agent presets — 新增 gemgate 統一入口
{
  "agents": [
    {
      "name": "gemgate",
      "command": "gemgate",
      "args": ["--interactive"],
      "description": "統一路由 — 自動派發到最佳 Agent",
      "icon": "🚀",
      "default": true
    },
    {
      "name": "claude",
      "command": "claude",
      "args": [],
      "description": "架構設計、複雜推理"
    },
    {
      "name": "copilot",
      "command": "gh",
      "args": ["copilot"],
      "description": "GitHub 操作、PR Review"
    },
    {
      "name": "gemini",
      "command": "gemini",
      "args": [],
      "description": "前端 UI、快速迭代"
    }
  ]
}
```

---

## Chapter 5：Copilot 外部呼叫具體實作

### 5.1 讓 Copilot 處理 PR Review

```bash
# gemgate 收到 PR review 請求時，自動轉發給 Copilot
gemgate route --type=pr-review --pr=123 --repo=user/designclaw

# 內部執行：
gh copilot suggest "review PR #123, focus on security and performance"
# 或用 SDK：
copilot.codeReview({ pr: 123, focus: ['security', 'performance'] })
```

### 5.2 讓 Copilot 處理 GitHub Actions

```bash
# Actions 失敗時自動診斷
gemgate route --type=ci-debug --run-id=12345

# 內部執行：
gh copilot explain "$(gh run view 12345 --log-failed)"
```

### 5.3 Copilot 作為 MCP Bridge

```javascript
// 讓 Copilot 共享你的 MCP 工具
// copilot-mcp-config.json
{
  "mcpServers": {
    "secondbrain": {
      "command": "node",
      "args": ["./mcp-servers/secondbrain-server.js"],
      "description": "搜尋 SecondBrain 知識庫"
    },
    "designclaw": {
      "command": "node",
      "args": ["./mcp-servers/designclaw-server.js"],
      "description": "DesignClaw 專案操作"
    }
  }
}
```

---

## Chapter 6：8 週實作路線圖

### Phase 1（Week 1-2）：基礎路由

- [ ] 建立 gemgate adapter 抽象層（interface）
- [ ] 實作 Claude adapter（最熟悉的，先做）
- [ ] 實作 Copilot CLI adapter（`gh copilot suggest/explain`）
- [ ] 基礎 fallback chain

### Phase 2（Week 3-4）：Copilot 深度整合

- [ ] Copilot Agent Mode adapter
- [ ] Copilot SDK 整合（如果 public preview 已開放）
- [ ] GitHub 操作自動路由規則
- [ ] PR Review 自動化流程

### Phase 3（Week 5-6）：BAT UI 整合

- [ ] Fork BAT，加入 gemgate 作為預設 Agent
- [ ] 路由狀態面板 UI
- [ ] Agent 健康度監控
- [ ] WebSocket 橋接

### Phase 4（Week 7-8）：進階功能

- [ ] RTK Token 壓縮層嵌入
- [ ] CCG 安全模型（patch-only + Claude review）
- [ ] 跨 Agent context 共享
- [ ] 並行執行（同一任務同時發給多個 Agent，取最快/最佳）

---

## Chapter 7：關鍵設計決策

### gemgate 包 BAT，還是 BAT 包 gemgate？

**答案：各司其職，WebSocket 橋接。**

gemgate 是 CLI daemon，可以獨立運行（headless），也可以被任何 UI 調用。BAT 是桌面 UI，專門做終端管理。不存在「誰包誰」——它們是平級的，gemgate 做決策，BAT 做呈現。

這個設計的好處：
1. gemgate 可以被 CI/CD、cron job、其他工具調用（不需要 UI）
2. BAT 可以在沒有 gemgate 的情況下手動操作各 Agent
3. 兩者結合時 = 智慧自動調度 + 視覺化管理

### Copilot 的 Token 計費

Copilot 有獨立的 token quota（不計入 Claude/Gemini 的額度），所以讓它處理 GitHub 操作 = 免費借力。特別是 PR Review 和 CI Debug 這種高頻操作，用 Copilot 處理可以省下大量 Claude token。

---

## Sources

- [Copilot CLI GA 公告](https://github.blog/changelog/2026-02-25-github-copilot-cli-is-now-generally-available/)
- [Copilot CLI 增強 Agents](https://github.blog/changelog/2026-01-14-github-copilot-cli-enhanced-agents-context-management-and-new-ways-to-install/)
- [Copilot SDK 公告](https://github.blog/news-insights/company-news/build-an-agent-into-any-app-with-the-github-copilot-sdk/)
- [BAT GitHub Repo](https://github.com/tony1223/better-agent-terminal)
