---
title: "Slop 自製學習法 — 用書籍試閱 + 目錄當 Prompt 的知識消費捷徑"
date: 2026-04-20
category: methodology
tags: [slop, prompt-engineering, knowledge-consumption, book-summary, NotebookLLM, Remotion, TTS, self-learning, information-anxiety]
type: insight
source: 網路貼文（社群分享）
project: AI工作流課程
priority: P2
status: active
---

## 核心方法

在 Token 週重置前把用量燒一燒的「無聊實驗」，意外發現了一套高效的知識消費流程：

**步驟**：
1. 到博客來等書店頁面，取得商業暢銷書的**目錄 + 試讀頁**
2. Prompt：「照這架構跟文風把整本書寫完」
3. 加上 WebSearch，用 APA 格式引用真實來源
4. 結果：寫出來的東西常常比原書好

**延伸**：
- 線上課程的試聽 + 課程大綱 = 優質 Prompt
- 補教講義的試閱 = 優質 Prompt
- 所有提供「預覽」的知識商品都是現成的 Prompt

## 為什麼有效

目錄和試閱頁本身就是作者（或編輯）花大量時間壓縮出來的「知識骨架」。這個骨架包含：
- 章節結構（邏輯順序）
- 核心概念（關鍵字）
- 文風範本（語氣、深度、目標讀者）
- 知識邊界（涵蓋什麼、不涵蓋什麼）

用這個骨架當 Prompt，等於直接跳過「定義結構」的步驟，讓 LLM 專注在「填充內容」。加上 WebSearch 引用真實來源，品質自然超越很多「水很多」的暢銷書。

## 產出管線

```
書籍目錄 + 試閱 → LLM 展開全文
     ↓
pipe to Remotion → 影片
pipe to NotebookLLM + TTS → 有聲內容
```

**關鍵洞察**：有了 Prompt 再展開就好。緩解 AI 以外的資訊焦慮——不需要買每本書、上每堂課，只要掌握結構，隨時可以展開。

## 已產出的「自製 Slop」

原作者的系列：
- 蜥蜴的簡報的技術
- 蜥蜴的實現 AI 自動化的第一步
- 蜥蜴習慣
- 24 天英文口說的蜥蜴
- 蜥蜴占星學

（「蜥蜴」應為作者的品牌/暱稱，所有標題都是對應暢銷書的 AI 重寫版）

## 對我的應用價值

### 1. 課程教材快速產出

AI 工具實戰課程的教材可以用這個方法加速：找到相關暢銷書的目錄結構 → 用自己的觀點和案例重新展開 → 比從零開始寫快得多。

### 2. SecondBrain 知識補充

看到一本有興趣但不想買的書 → 用目錄 + 試閱當 Prompt → 產出一份筆記存到 dispatch-outputs/ → 等 compile.py 合成時可以交叉比對。

### 3. Remotion + NotebookLLM 管線

這條管線值得研究：
- **Remotion**：React 驅動的程式化影片製作框架，可以把 markdown → 影片
- **NotebookLLM + TTS**：Google 的 NotebookLM 可以把文字轉成 podcast 風格的對話音頻

兩者結合 = 從書籍目錄到影片/音頻的全自動管線。

### 4. 「Slop」的正名

「自己做 Slop 給自己吃」——這裡的 Slop 不是貶義的 AI 垃圾內容，而是「個人化的 AI 生成學習材料」。差別在於：
- 給別人看的 Slop = 垃圾
- 給自己用的 Slop = 高效學習工具

這個區分很重要，可以用在課程中解釋 AI 內容的價值判斷。

## 倫理考量

這個方法遊走在智慧財產權的灰色地帶：
- 目錄和試閱頁是公開的（書店刻意展示的）
- 但用它來「重寫整本書」可能侵犯著作權
- 加上 WebSearch 引用真實來源是一種緩解
- 用於個人學習 vs 公開發布，法律風險不同

建議：用於個人學習筆記可以，公開發布要謹慎。

## 後續待辦

- [ ] 測試 Remotion 的 markdown → 影片管線
- [ ] 研究 NotebookLM 的 TTS podcast 功能
- [ ] 用這個方法為 AI 課程教材做一次實驗
- [ ] 建立「書籍速讀 Prompt 模板」存到 SecondBrain

## 交叉連結

- [[2026-04-11_三次技術革命社會抗爭故事卡片_課程教材|故事卡片課程教材]]：課程教材的另一種產出方式
- [[2026-04-17_Paper-Pipeline工作流對照分析|Paper Pipeline]]：同樣是「結構化輸入 → AI 展開 → 存儲」的模式
- [[2026-04-18_Claude-Design實戰七招-Ryan-Mather使用心得|Claude Design 七招]]：Tip 7「知道什麼時候慢下來」同樣適用——不是所有書都適合這樣處理
