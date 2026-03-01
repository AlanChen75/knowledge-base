---
title: GitHub 新專案監控
status: pending
priority: medium
machine: ac-mac
---

# GitHub 新專案監控

## 目標
自動監控 GitHub 上特定主題/關鍵字的新專案，發現有趣的開源項目時透過 Telegram 通知。

## 核心概念

GitHub **沒有** 內建「關注某個主題的新專案」功能。需要自己用 **Search API 輪詢** 來實現：
- 每 30 分鐘用 Search API 搜尋「最近建立」的 repo
- 比對已見過的 repo，過濾出新的
- 發送 Telegram 通知

## GitHub API 方案比較

| 方案 | 能發現新 repo？ | 即時性 | 需要 Key？ | 適合 |
|------|---------------|--------|-----------|------|
| **Search API** | **是 (最佳)** | 輪詢 | 建議 | **依主題/關鍵字找新 repo** |
| Events API | 部分 (CreateEvent) | 30s~6h 延遲 | 否 | 監控已知用戶/組織 |
| Atom/RSS Feed | 否 (per repo/user) | 接近即時 | 否 | 追蹤已知 repo 的 release |
| Webhooks | 否 (僅自己的 repo) | 即時 | N/A | 監控自己的 repo |
| Notifications | 否 (僅 watch 的 repo) | 接近即時 | 是 | 管理已 watch 的 repo |

**結論：用 Search API + cron 輪詢是唯一可行方案。**

## 實作架構

```
ac-mac (cron 每 30 分鐘)
├── github-topic-monitor.py
│   ├── 呼叫 GitHub Search API (5 個搜尋條件)
│   ├── 比對已見過的 repo (state file)
│   ├── 新 repo → Telegram 通知
│   └── 更新 state file
└── ~/.github-monitor-state.json (已見過的 repo 列表)
```

## Search API 用法

### 端點
```
GET https://api.github.com/search/repositories
  ?q={query}&sort=created&order=desc&per_page=10
```

### 搜尋語法 (q 參數)

| 語法 | 範例 | 說明 |
|------|------|------|
| `topic:` | `topic:ai-agents` | 依 topic 標籤 |
| `created:` | `created:>2026-02-14` | 建立日期 |
| `pushed:` | `pushed:>2026-02-14` | 最後推送日期 |
| `language:` | `language:python` | 程式語言 |
| `stars:` | `stars:>10` | 最低星數 |
| `in:` | `in:name,description` | 搜尋範圍 |

### 範例搜尋

```bash
# 最近 AI agent 相關新 repo
gh search repos --topic ai-agents --created ">2026-02-08" --sort updated --limit 20

# 台灣開放資料相關
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/search/repositories?q=taiwan+open+data+created:>2026-02-08&sort=stars"
```

### 頻率限制
- 認證: 30 次/分鐘 (Search API 專用限制)
- 未認證: 10 次/分鐘
- 5 個搜尋每 30 分鐘 = 遠低於限制

## 監控主題 (規劃)

| 分類 | 搜尋條件 | 說明 |
|------|---------|------|
| AI Agents | `topic:ai-agents created:>{date}` | AI 代理框架 |
| LLM Tools | `topic:llm+topic:tool created:>{date}` | LLM 工具 |
| Taiwan Data | `taiwan open data created:>{date}` | 台灣開放資料 |
| Claude/Anthropic | `claude+anthropic in:name,description created:>{date}` | Claude 相關 |
| MCP Servers | `topic:mcp-server created:>{date}` | MCP 伺服器 |

## Telegram 通知格式

```
GitHub Monitor: 3 new repos found

[AI Agents]
  langchain-ai/new-agent-framework
  A new framework for building AI agents
  Lang: Python | Stars: 15

[Taiwan Data]
  g0v/taiwan-realtime-data
  Real-time data visualization for Taiwan
  Lang: JavaScript | Stars: 3
```

## 補充：Atom Feed (追蹤已知 repo)

追蹤特定 repo 的更新，不需要 API key：

```
# Release 通知
https://github.com/{owner}/{repo}/releases.atom

# Commit 通知
https://github.com/{owner}/{repo}/commits.atom

# 用戶活動
https://github.com/{username}.atom
```

可搭配 RSS 閱讀器 (Feedly, Miniflux) 或自建 RSS→Telegram 轉發。

## 環境需求
- ac-mac 上的 Python3
- GitHub Token (已有: `$GITHUB_TOKEN` 或用 gh CLI 認證)
- Telegram Bot (已有: tg-monitor-bot)
- crontab 排程

## 待辦
- [ ] 決定要監控的主題/關鍵字清單
- [ ] 寫 github-topic-monitor.py
- [ ] 設定 crontab (每 30 分鐘)
- [ ] 整合到 tg-monitor-bot (或獨立 cron)
- [ ] 測試 Telegram 通知格式
