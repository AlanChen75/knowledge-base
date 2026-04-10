---
title: "Discord 作為 AI Agent 控制台的選型分析"
date: 2026-04-06
category: tech-analysis
tags: [Discord, OpenClaw, AI-agent, 龍蝦, multi-agent, Claude-Code-Channels, Telegram]
type: analysis
source: "社群貼文分析 + web research"
project: OpenClaw
priority: medium
status: active
---

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
- 定位：多 agent 控制台、長期任務追蹤、團隊協作

### WebChat

- 容易斷線、頁面重整後 connection 丟失
- 任務中斷無法恢復
- 不適合長時間任務

## 二、Discord 的三大優勢（原作者觀點）

### 1. 長週期主動回報

Thread 會持續保留，Agent 跑完後精準在該 Thread 主動更新。適合需要數天完成或每日回報的流程任務。

### 2. 讓 Agent 彼此討論

多個不同職能的 Agent 可以在同一環境互相對話、腦力激盪。目前只有 Discord 能輕鬆做到。

### 3. 出張嘴就能平行分工

討論出 Action Items 後，可直接交代開 Linear 票、各開 Thread 同步執行。加上語音系統可實現純口頭派工。

## 三、Discord 多 Agent 架構：兩種模式

### 分身術（Clone Mode）

- 單一 OpenClaw bot，透過 Bindings 設定在不同 channel 切換 persona
- 例如：#research channel = 研究員，#code channel = 工程師
- 優點：設定簡單、成本低
- 缺點：不能真正平行執行

### 獨立團（Independent Team Mode）

- 多隻 bot 各自獨立，有自己的 model、memory、skill
- Discord 設定：`allowBots: true` + `requireMention: false`
- bot 可互相讀訊息、在同一 thread 討論
- 優點：真正平行、角色專精
- 缺點：token 消耗指數級增長、需要設 loss-control

### 具體設定流程（獨立團模式）

1. Discord Developer Portal 建多個 Application，每個對應一個 agent 角色
2. 每個 bot 各跑一個 OpenClaw instance，各自的 CLAUDE.md / system prompt 定義角色
3. Discord Server 裡按專案或職能開 channel
4. 用 autoThread 功能讓 bot 自動開 thread 回覆，主 channel 保持乾淨像目錄
5. 協作時把多個 bot 拉進同一 thread，打開 allowBots

### Bindings 優先順序（8 級）

1. exact peer match
2. parent peer match
3. guildId + role
4. guildId standalone
5. teamId
6. accountId
7. channel-level
8. default agent fallback

## 四、成本與風險注意事項

- 多 agent 互相對話會指數級燒 token，務必設最大輪數限制
- 初始設定就可能消耗數百萬到上千萬 token
- 建議搭配免費 API（OpenRouter 免費模型）做非關鍵任務
- Discord 上傳檔案曾有 hang 住的 bug，已在 4.2 版修復（PR #58198）

## 五、對 Claw 生態系的應用

Discord 可直接當 DesignClaw 開發控制台：

- #render channel → ComfyUI render agent
- #layout channel → layout agent
- #supply-chain channel → 供應鏈報價 agent
- 手機上用 Discord 就能同時指揮多條線

也適合 OpenClaw 社群的使用者支援和展示。

## 六、Claude Code Channels vs OpenClaw

| 面向 | Claude Code Channels | OpenClaw |
|------|---------------------|----------|
| 開發者 | Anthropic 官方 | 社群開源 |
| 支援平台 | Telegram, Discord | 30+ 平台 |
| 社群技能 | 無 | 5,700+ |
| 整合深度 | 深度整合 Claude Code | 支援多種 LLM |
| 設定難度 | 較簡單 | 較複雜但彈性大 |
| 多 agent | 透過 Dispatch/Cowork | 原生支援 |

## Sources

- [OpenClaw × Discord 伺服器串接完全指南](https://www.meta-intelligence.tech/en/insight-openclaw-discord)
- [OpenClaw 多智能体协作配置完全指南 2026](https://ofox.ai/zh/blog/openclaw-multi-agent-collaboration-guide-2026/)
- [OpenClaw 多Agent配置：分身術 vs 獨立團](https://x.com/indie_maker_fox/status/2032684196129550650)
- [Claude Code Channels 設定教學](https://www.darrelltw.com/claude-code-channels-discord-telegram/)
- [OpenClaw 完整研究報告](https://gist.github.com/lowkingshih/c1f1a5e93ca314d8b08979b8f53b3060)
- [25 個免費 AI API 總整理](https://www.soft4fun.net/tech/ai/25-free-llm-api.htm)
- [Claude Code Channels 官方介紹](https://pub.towardsai.net/claude-code-channels-message-your-ai-coding-agent-from-telegram-and-discord-2026-5f263ccc4b9c)
