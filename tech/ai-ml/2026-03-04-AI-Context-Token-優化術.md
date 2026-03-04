---
title: AI Context Token 優化術 - 視覺化你的 Token 消耗
date: 2026-03-04
source: Telegram 社群分享
category: tech/ai-ml
tags: [AI, Token優化, 成本控制, Context管理, Prompt工程, Claude]
type: technique
raw_file: ../../raw/2026-03/2026-03-04-173012-text.txt
difficulty: ⭐⭐
---

# AI Context Token 優化術 - 視覺化你的 Token 消耗

## 📊 元資訊
- **難度**：⭐⭐
- **來源類型**：社群實戰分享
- **筆記時間**：2026-03-04 17:30
- **適用對象**：使用 Claude Code、Cursor、Copilot 等 AI 助手的開發者

## 📌 摘要
透過建立 Token Dashboard 視覺化 context 檔案的 token 消耗，發現啟動時載入的 context 可從 13,190 tokens 壓縮至 6,673 tokens（約 50% 節省）。關鍵不是省錢，而是**你根本不知道問題存在，直到視覺化它**。

## 🏷️ 標籤分類
- **大分類**：tech
- **小分類**：ai-ml
- **關鍵字**：Token 優化、Context 管理、成本控制、視覺化、AI 助手

## 🔑 關鍵要點

### 1. 問題發現
- **每次啟動 AI 對話**都會載入大量 context 檔案
- 原作者發現啟動消耗 **13,190 tokens**
- 很多內容是「已經內化的規則」，不需要每次載入

### 2. 優化成果
| 檔案 | 優化前 | 優化後 | 節省 |
|------|--------|--------|------|
| AGENTS.md | 4,355 tokens | 1,117 tokens | 74% |
| MEMORY.md | 4,648 tokens | 1,700 tokens | 63% |
| **總計** | 13,190 tokens | 6,673 tokens | **49%** |

### 3. 額外發現
- 在 workspace 裡找到 **3 個不該存在的巨型資料檔案**
- 其中一個高達 **27MB**
- 這些檔案會被 AI 嘗試索引，浪費大量 tokens

## 💡 實作方法：Token Dashboard

### 可直接使用的 Prompt
```
幫我建立一個 Token 使用量 Dashboard，讓我能清楚看到所有活動消耗了多少 tokens。

我想了解的包含：
- 每個 .md 檔案有多大、載入時消耗多少 tokens
- 每個 cron job 跑一次用多少 tokens
- 每次啟動新 session 消耗多少 tokens
- 過去 5 天的每日使用量（依 LLM 分類）

我要一個可以瀏覽的 context 檔案目錄，能點開資料夾查看每個檔案的大小和 context 佔用量。

然後，審計我們的檔案結構和系統，找出在不損失功能的前提下優化 token 使用量的方法。

在執行任何變更之前，先給我計劃和建議清單讓我確認。
```

### Dashboard 功能清單
1. **檔案大小分析**：掃描所有 .md 檔案，顯示 bytes 和估算 tokens
2. **載入分類**：區分「必載」vs「按需載入」
3. **使用量追蹤**：過去 N 天的 token 消耗趨勢
4. **目錄瀏覽器**：可展開的樹狀結構，點擊查看詳情
5. **優化建議**：自動分析並提出改善方案

## 🧠 概念連結

### Context Window 管理策略
- **必載 (Always Load)**：核心系統設定、安全規則
- **按需載入 (On-Demand)**：特定專案說明、歷史記錄
- **永不載入 (Never Load)**：大型資料檔、二進位檔案

### Token 估算公式
- **英文**：約 1 token ≈ 4 字元 ≈ 0.75 單字
- **中文**：約 1 token ≈ 1-2 個漢字
- **程式碼**：變數名、語法符號會增加 token 數

### 相關工具
- **tiktoken**：OpenAI 官方 tokenizer
- **Claude tokenizer**：Anthropic 的 token 計算
- **VS Code 擴充**：即時顯示檔案 token 數

## 💬 金句摘錄
> "每天省下來的費用不是重點，重點是我根本不知道有這個問題，直到我把它視覺化"

> "你的 AI 每次對話燒多少錢，你知道嗎？"

## 💡 與我的連結

### 1. 審計現有 CLAUDE.md
我目前的 `/home/ac-mac/.claude/CLAUDE.md` 和 `/home/ac-mac/CLAUDE.md` 可能也有類似問題：
- 檢查是否有過時或重複的內容
- 區分「必須每次載入」vs「可按需查詢」
- 精簡冗長的說明文字

### 2. 建立本地 Token Dashboard
可以在 ac-mac 上建立類似工具：
```bash
# 估算 CLAUDE.md 的 token 數
wc -c ~/.claude/CLAUDE.md  # 先看檔案大小
# 約 bytes / 4 = 估算 tokens（英文）
# 中文則 bytes / 3 ≈ tokens
```

### 3. 整合到每日報表
將 token 使用量整合到現有的 `daily-claude-report.py`，追蹤長期趨勢

## ✅ 行動項目
- [ ] 計算現有 CLAUDE.md 的 token 數
- [ ] 審計 context 檔案，找出可精簡的內容
- [ ] 區分必載 vs 按需載入的內容
- [ ] 檢查 workspace 是否有不該存在的大型檔案
- [ ] 考慮建立簡易 Token Dashboard
- [ ] 將 token 趨勢整合到每日報表

## 📝 我的註解與思考

### 為什麼這很重要
1. **成本控制**：Claude API 按 token 計費，context 越大成本越高
2. **回應品質**：過多無關 context 可能干擾 AI 理解
3. **效能提升**：減少 context 可加快首次回應速度
4. **系統維護**：定期審計可發現過時或冗餘的設定

### 優化策略
1. **精簡語言**：用簡潔的條列取代冗長說明
2. **移除重複**：多個檔案間可能有重複內容
3. **動態載入**：將「偶爾需要」的內容改為按需查詢
4. **定期清理**：設定週期性審計 context 檔案

### 注意事項
- 不要過度壓縮導致 AI 失去重要上下文
- 核心安全規則、關鍵設定必須保留
- 壓縮前先備份原始版本

## 🔗 延伸閱讀
- [OpenAI Tokenizer 工具](https://platform.openai.com/tokenizer)
- [Anthropic Claude 定價頁面](https://www.anthropic.com/pricing)
- [tiktoken GitHub](https://github.com/openai/tiktoken)

## ℹ️ 原文資訊
- **原始輸入**：[查看原始資料](../../raw/2026-03/2026-03-04-173012-text.txt)
- **來源**：Telegram 社群分享
- **收錄時間**：2026-03-04 17:30:12
