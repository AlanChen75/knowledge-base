---
title: Claude Code 源碼洩漏分析 — 51.2 萬行 TypeScript 揭示的架構秘密
date: 2026-03-31
category: tech/ai-ml
tags: [Claude-Code, Anthropic, 源碼分析, KAIROS, multi-agent, 架構設計]
type: analysis
source: https://github.com/ChinaSiro/claude-code-sourcemap
status: draft
---

# Claude Code 源碼洩漏分析

## 摘要

Anthropic 的 Claude Code CLI 工具因為 npm 套件中包含了 sourcemap 檔案（cli.js.map），被安全研究員透過逆向工程還原出完整 TypeScript 源碼，共約 1,900 個檔案、512,000 行程式碼。ChinaSiro/claude-code-sourcemap 是其中一個還原版本（v2.1.88）。源碼揭示了多個尚未公開的功能：KAIROS（常駐背景 Agent）、ULTRAPLAN（30 分鐘遠端規劃）、Coordinator 多 Agent 協調模式、Buddy 伴侶 UI、Agent Swarm 等。

## 背景

- **發現時間：** 2026 年 3 月 31 日
- **發現者：** 安全研究員 Chaofan Shou
- **來源：** npm 套件 `@anthropic-ai/claude-code` v2.1.88 中的 `cli.js.map`
- **還原方式：** 提取 sourcemap 的 `sourcesContent` 欄位
- **GitHub Stats：** 4,300+ stars、7,700+ forks
- **版權聲明：** 源碼版權屬 Anthropic，僅供技術研究

## 分析內容

### Claude Code 的完整架構

還原的源碼揭示 Claude Code 不只是一個 CLI 聊天工具，而是一個完整的多模態開發平台：

```
claude-code/
├── main.tsx          # CLI 入口點
├── tools/            # 30+ 工具實作（Bash、FileEdit、Grep、MCP）
├── commands/         # 40+ 指令（commit、review、config）
├── services/         # API、MCP、分析服務
├── coordinator/      # 多 Agent 協調引擎
├── assistant/        # KAIROS 常駐助手模式
├── buddy/            # AI 伴侶 UI
├── plugins/          # 插件系統
├── skills/           # 技能系統
├── voice/            # 語音互動
├── vim/              # Vim 模式
```

### 未公開的核心功能

#### KAIROS — 常駐背景 Agent

KAIROS 是一個「永遠在運行」的 Claude 助手。不等你打字，主動監控並對它注意到的事情採取行動。這跟目前公開版的「你問它答」模式完全不同，是一個自主型常駐守護程式（daemon）。

目前被 compile-time feature flag 完全隱藏，外部版本看不到。

#### ULTRAPLAN — 30 分鐘遠端規劃

長時間的規劃任務，可以 offload 到遠端執行。

#### Coordinator 模式 — 多 Agent 協調

一個主 Agent 分配任務給多個 worker，worker 平行執行後回報。當 worker 要執行危險操作時，透過 mailbox 向 leader 請求權限。

這跟 Anthropic 那篇 Harness Design 文章描述的 Planner-Generator-Evaluator 架構完全吻合。

#### Agent Swarm

多個 Agent 群體協作，規模比 Coordinator 更大。

#### Buddy — 伴侶 UI

更友善的互動介面，可能是面向非開發者的版本。

### 隱藏的安全機制

源碼中還發現了一些有趣的內部機制：

- **Fake Tools：** 提供假工具給模型作為 honeypot，用來偵測模型是否試圖繞過限制
- **Frustration Regexes：** 偵測使用者是否感到沮喪的正則表達式
- **Undercover Mode：** 隱身模式（用途不明）
- **Three-Gate Trigger Architecture：** 三層觸發架構，控制功能的啟用條件
- **Dream System：** 類似「做夢」的系統（可能是背景學習或預處理機制）

### 這次洩漏的意義

1. **Anthropic 的產品路線圖被提前曝光。** KAIROS、ULTRAPLAN、Coordinator 都是重大功能，現在競爭對手可以直接參考架構設計。

2. **多 Agent 協調是確定的方向。** Coordinator + Agent Swarm 證實了 Anthropic 正在內部大力發展 multi-agent 系統，不只是論文層級。

3. **Claude Code 遠比公開版強大。** Feature flag 後面藏了大量功能，目前使用者看到的只是冰山一角。

4. **安全設計值得學習。** Fake tools、frustration detection、three-gate architecture 這些機制，對任何在建 Agent 系統的人都有參考價值。

### 對你的工作的啟示

1. **你的 RAG 系統可以借鏡 Coordinator 模式。** 查詢分析 Agent + 檢索 Agent + 回答生成 Agent，平行跑再合併結果，就是 Claude Code 內部的做法。

2. **KAIROS 的常駐監控概念，跟 MetaClaw 的 OMLS 排程器異曲同工。** 都是讓 AI 不只在你叫它的時候才工作，而是持續在背景觀察和行動。

3. **Plugin 和 Skill 系統已經內建。** 你現在在 Cowork 裡用的 skill 系統，在 Claude Code 端也有對應的實作。兩邊的 skill 格式有可能最終會統一。

4. **Codex Plugin 的整合方式，跟 Claude Code 源碼中的 MCP 架構一致。** 這驗證了 MCP 是 Anthropic 長期的工具整合策略。

## 結論與建議

這次 sourcemap 洩漏不是安全漏洞（sourcemap 本來就在公開的 npm 套件裡），而是 Anthropic 的疏忽——沒有在發佈前移除 sourcemap。但對整個 AI Agent 生態來說，這是一份極有價值的學習材料。

Claude Code 的架構設計，特別是 Coordinator 模式、feature flag 管理、安全機制，都是建構 Agent 系統的最佳實踐範例。

## 行動項目

- [ ] 瀏覽 restored-src/src/coordinator/ 目錄，學習多 Agent 協調的實作方式
- [ ] 研究 tools/ 目錄中的工具實作，看有沒有可以移植到 RAG 系統的設計模式
- [ ] 關注 KAIROS 和 Buddy 的後續公開發布
- [ ] 考慮在 AI 工具實戰系列文章中分享這次洩漏的架構洞察

---

**資料來源：**
- [ChinaSiro/claude-code-sourcemap（GitHub）](https://github.com/ChinaSiro/claude-code-sourcemap)
- [VentureBeat: Claude Code's source code appears to have leaked](https://venturebeat.com/technology/claude-codes-source-code-appears-to-have-leaked-heres-what-we-know)
- [DEV.to: 512,000 Lines Exposed](https://dev.to/evan-dong/claude-codes-entire-source-code-just-leaked-512000-lines-exposed-3139)
- [Alex Kim: fake tools, frustration regexes, undercover mode](https://alex000kim.com/posts/2026-03-31-claude-code-source-leak/)
- [awesome-claude-code-postleak-insights](https://github.com/nblintao/awesome-claude-code-postleak-insights)
- [Kuberwastaken: Claude Code in Rust & Breakdown](https://github.com/Kuberwastaken/claude-code)
