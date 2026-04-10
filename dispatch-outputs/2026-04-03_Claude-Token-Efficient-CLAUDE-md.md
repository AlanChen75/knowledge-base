---
title: claude-token-efficient — 9 行 CLAUDE.md 減少 63% 輸出 token
date: 2026-04-03
category: tech/tools
tags: [Claude-Code, token優化, CLAUDE.md, prompt工程, 成本控制]
type: analysis
source: https://github.com/drona23/claude-token-efficient
project: AI工具實戰
status: draft
---

# claude-token-efficient — 9 行 CLAUDE.md 減少 63% 輸出 token

## 摘要

drona23/claude-token-efficient 是一個只有 9 行的 CLAUDE.md 檔案，丟進專案根目錄即可生效，透過禁止 Claude Code 的拍馬屁開頭、空洞結尾、重複問題、未被要求的建議等行為，聲稱可減少輸出 token 63%。1,900+ stars。實際效果取決於使用場景，重度使用者（日均 100+ prompt）才有明顯省錢效果。

## 背景

Claude Code 預設行為傾向冗長——每次回覆都帶 "Sure! Great question!" 開頭、"hope this helps!" 結尾、重述使用者問題、加入未被要求的建議。這些行為在單次對話中只是小麻煩，但在重度開發場景下（一天跑上百個 prompt），累積的 token 成本非常可觀。

## 分析內容

### 核心指令（9 行 CLAUDE.md）

```markdown
- Think before acting. Read existing files before writing code.
- Be concise in output but thorough in reasoning.
- Prefer editing over rewriting whole files.
- Do not re-read files you have already read.
- Test your code before declaring done.
- No sycophantic openers or closing fluff.
- Keep solutions simple and direct.
- User instructions always override this file.
```

### 實測數據

| 指標 | 改善幅度 |
|------|---------|
| 代碼 review | 120 詞 → 30 詞（-75%） |
| 模組重構 | 180 詞 → 55 詞（-69%） |
| 修正錯誤 | 55 詞 → 20 詞（-64%） |
| 信息量 | 不變 |

**注意：** 63% 是 5 個 prompt 的方向性指標（T1-T3, T5 測詞數減少，T4 測格式），非嚴格統計研究。

### 省錢邏輯

- 編譯器每次編譯成本下降 17.4%
- 配合 v8 子工具減少 prompt 層數
- 重度使用者每月可省顯著費用
- 但 CLAUDE.md 本身每次對話都被讀取，會增加 input token，低使用量場景可能反而更貴

### 本質分析

推文作者 @chenchengpro 的觀點值得記錄：

這本質上是 prompt 注入控制模型行為。把「輸入 token 換抑制 token」的概念，放在都在做洗牌的 AI 生態裡，日均 100+ prompt 才有感覺。一個文件本身也帶 token，所以要拿成本做計算。

更深層的意義：這 9 行指令的效果，側面證明了 LLM 預設輸出中有大量「禮貌性廢話」。如果 9 行 prompt 就能砍掉 63% 的輸出而不損失信息量，那原本的 63% 就是純噪音。

### 適用場景

**適合：**
- 日均 100+ prompt 的重度 Claude Code 使用者
- 大型專案的批量程式碼修改
- CI/CD 中使用 Claude API 的自動化流程
- token 成本敏感的場景

**不適合：**
- 低頻使用者（input token 成本 > 節省的 output token）
- 需要詳細解釋的學習場景
- 需要 Claude 主動提供建議的探索性開發

### 與其他 token 優化方法的比較

| 方法 | 原理 | 效果 |
|------|------|------|
| CLAUDE.md 指令 | 行為約束 | ~63% output 減少 |
| 模型降級（Haiku） | 用更小模型 | ~80% 成本減少，能力降低 |
| Prompt 壓縮工具 | 壓縮 input | ~40% input 減少 |
| Caching（prompt cache） | 避免重複計算 | ~50% 成本減少 |

最佳策略是組合使用：CLAUDE.md + prompt cache + 按任務選模型。

## 結論與建議

值得在 Claude Code 專案中嘗試。成本低（複製一個檔案），風險低（隨時可刪），對重度使用者有明顯效益。但不要盲信 63% 這個數字，實際效果因場景而異。

## 行動項目

- [ ] 把 CLAUDE.md 加到常用的 Claude Code 專案中測試
- [ ] 觀察一週的 token 用量變化，跟之前做對比
- [ ] 考慮在 AI 工具實戰系列分享這個技巧，搭配實測數據

---

**資料來源：**
- [drona23/claude-token-efficient（GitHub）](https://github.com/drona23/claude-token-efficient)
- [Before/After 範例](https://github.com/drona23/claude-token-efficient/blob/main/examples/before-after.md)
- [CLAUDE.md 原始內容](https://github.com/drona23/claude-token-efficient/blob/main/CLAUDE.md?plain=1)
