---
title: Claude Code Agent 完整設定 - CLAUDE.md 與 Skills
date: 2026-01-31
category: tech/ai-ml
tags: [claude-code, agent, skills, infrastructure, telegram-bot]
---

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
專案目錄下的 `CLAUDE.md` 會在該目錄工作時額外載入。

### Skills 清單

| Skill | 路徑 | 觸發方式 |
|-------|------|---------|
| system-check | `~/.claude/skills/system-check/` | 「檢查系統」「系統狀態」 |
| daily-report | `~/.claude/skills/daily-report/` | 「每日報表」「API 使用量」 |
| knowledge-base | `~/.claude/skills/knowledge-base/` | 「記錄到知識庫」「搜尋知識庫」 |
| service-deploy | `~/.claude/skills/service-deploy/` | 「部署」「更新服務」 |
| conversation-search | `~/.claude/skills/conversation-search/` | 「搜尋對話」「之前的對話」 |
| paper-automation | `~/.claude/skills/paper-automation/` | 學術論文處理（既有） |

### 參考來源

- **OpenClaw** (github.com/openclaw/openclaw): CLAUDE.md 架構模式、SKILL.md 格式規範
- **AgentSkills 規格** (agentskills.io): 開放標準的 AI 編碼助手 skill 格式
- **claude-telegram-bot** (github.com/linuz90/claude-telegram-bot): Claude Agent SDK 整合模式

## 影響範圍

- Happy Coder app 的新 session 會自動載入 CLAUDE.md
- TG Bot 的 `/happy` 模式（使用 `claude -p`）也會載入 CLAUDE.md
- 所有 session 都會知道：機器資訊、服務清單、跨機架構、知識庫位置

## 相關檔案

- `~/.claude/CLAUDE.md` - 全域 agent 指引
- `~/.claude/skills/*/SKILL.md` - 各 skill 定義
- `~/CLAUDE.md` - 專案級規範
