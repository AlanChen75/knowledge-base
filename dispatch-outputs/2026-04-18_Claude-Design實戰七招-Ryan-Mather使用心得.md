---
title: "Claude Design 實戰七招 — Anthropic 設計師 Ryan Mather 的使用心得"
date: 2026-04-18
category: tool-analysis
tags: [Claude-Design, Anthropic, design-system, AI-design, mockup, Figma, prototyping, Ryan-Mather, Nate-Parrott, agentic-design]
type: analysis
source: "Ryan Mather X thread + 狐說八道翻譯解說"
project: Claw 生態系
priority: P1
status: active
---

## 背景

Claude Design 跟著 Anthropic Labs 同步推出。Anthropic 內部 verticals team 設計師 Ryan Mather（一人服務 7 條產品線）在 X 上分享了實戰 tips。核心開發者是 Nate Parrott。

關鍵定位：**Claude Design 不是 Figma 的升級版，而是 Claude Code 的設計版。** 心智模型不是「我在排版」，而是「我跟一個會做東西的助手對話」。

---

## 七個實戰技巧

### Tip 1：先把設計系統跟核心畫面設好

花一小時把 design system（色彩、字型、按鈕樣式、間距、元件庫）和核心畫面（登入、首頁、設定）餵給 Claude Design。後面每次生成都在這個基礎上延伸，視覺一致性自動保持。

**原理**：跟所有 AI 工具一樣，第一步給的脈絡越明確，後面產出品質越穩。省掉逐張修圖的時間。

### Tip 2：跟工程師即時一起迭代

一個會議裡就能跟一位工程師把新功能設計完。Claude 畫 mockup 超快，對話可以保持在「這個功能要解決什麼問題、有哪些約束」的高層次，邊玩概念邊看東西成形。

**流程變革**：設計師跟工程師的協作粒度從「文件交接（1-2 週）」變成「對話中即時定案（1 個會議）」。

### Tip 3：用 Comment 工具做快速精準修改

粗稿出來後直接點選元件做評註（point and crit），不用嘴描述。

**為什麼重要**：自然語言描述 UI 修改的效率極低。「右上角那個按鈕再小一點、顏色淡一點」這種描述有大量歧義。點選元件直接給指令，資訊損耗幾乎是零。

### Tip 4：請 Claude 做影片 demo

Claude Design 幾乎什麼想得到的事都做得到。它比較接近 Claude Code 的使用體驗，離以畫布為核心的設計工具（Figma、Sketch）比較遠。

**關鍵定位**：把它當 Figma 升級版會用不出力氣，當 Claude Code 的設計版才對味。除了靜態稿還能做影片 demo、互動原型、客製小工具。

### Tip 5：用 Connector（特別是 Docs 跟 Slack）

設好 Connector 後，可以送出指令：「請讀一下產品檢討會議的筆記，做一份簡報探索裡面提到的所有問題的不同設計方案」，然後出去散步，回來用清醒的眼睛看成果。

**流程壓縮**：「整理會議結論 → 產出設計方向」從幾小時壓到幾分鐘。人力負擔從「讀、想、做」變成「下指令、散步、驗收」。

### Tip 6：請 Claude 臨時做客製小工具

不要用畫布工具的思路來用 Claude Design，它是另一種動物。例如：設計色彩選擇器時，先讓 Claude 做一個互動的色彩預覽 prototype，邊玩邊調規格。

**能力差異**：這個在傳統設計軟體需要工程師配合，在 Claude Design 裡設計師一個人就能完成。

### Tip 7：知道什麼時候要慢下來、親手做

新圖示、小插畫、命名——這些細節永遠帶來不成比例的衝擊。知道什麼時候慢下來是一門藝術。

**深度觀點**：這三類東西的共通點是「決策空間極小、品質天花板極高」。AI 能快速生出可用版本，但要做到「讓人記住」還是人在定奪。不是對 AI 的懷疑，是對「什麼適合自動化、什麼不適合」的清醒判斷。

---

## Ryan 的結尾補充

1. **最喜歡的一點**：Claude Design 讓設計過程變得很愉悅（joyful），可以嘗試更多發散的點子，對每個點子的執著比較鬆。工具加速讓沉沒成本降低，決策更誠實。

2. **感謝 Nate Parrott**：Claude Design 核心開發者，他的 whimsy（奇想）和玩心塑造了整個產品氣氛。

3. **自嘲**：Ryan 自己也貢獻過幾個 PR（檔案畫面、composer 元件），但那些程式碼現在全被改掉了。

4. **預告**：正式上線後會分享更多 tips。

---

## 對我的啟示

### 跟 Claw 生態系的關聯

1. **Tip 1（先設好設計系統）= YAML frontmatter**：先定好規範，後面所有產出自動遵循。跟 SecondBrain 的 DISPATCH_RULES.md 邏輯完全一致。

2. **Tip 4（不是 Figma 是 Claude Code）= Cowork 不是任務管理器**：工具定位決定使用方式。Cowork 不是 Asana 的替代品，而是「會做事的同事」。

3. **Tip 5（Connector + 散步）= Dispatch + 非同步**：下指令→離開→回來驗收，這就是 Dispatch 模式。

4. **Tip 7（知道什麼時候慢下來）= compile.py 的人工審查環節**：AI 做初稿，人做最後的品質把關。不是所有東西都適合自動化。

### DesignClaw 的可能性

如果 Claw 生態系要做設計相關的垂直應用（DesignClaw），Claude Design 的七個 tips 就是產品設計原則：
- 先設好 design system（Tip 1）
- 即時協作而非文件交接（Tip 2）
- 點選元件做精準修改（Tip 3）
- 能做影片 demo 和互動原型（Tip 4）
- 整合外部資料源（Tip 5）
- 客製小工具（Tip 6）
- 保留人工精修空間（Tip 7）

---

## 後續待辦

- [ ] 測試 Claude Design 的實際功能和限制
- [ ] 評估 Claude Design + Cowork 的整合可能性
- [ ] 研究 Nate Parrott 的其他作品和設計哲學
- [ ] 考慮 DesignClaw 作為 Claw 垂直應用的可行性

---

## 交叉連結

- [[2026-04-09_Better-Agent-Terminal統一CLI調度中心分析|BAT 分析]]：「不是 X 的升級版，而是另一種動物」的定位思路
- [[2026-04-09_gemgate-BAT-Copilot整合實作指南|gemgate 整合指南]]：工具間的 Connector 整合概念
- [[2026-04-17_Paper-Pipeline工作流對照分析|Paper Pipeline 對照]]：Tip 5 的「Connector + 散步」模式跟 Paper Pipeline 的「emoji + 離開」模式同構

---

## Sources

- [Ryan Mather X thread](https://x.com/ryanmather) — 原始 tips
- [Claude Design - Anthropic Labs](https://claude.ai/design) — 產品頁面
- [狐說八道翻譯解說](https://threads.net/) — 繁體中文翻譯 + 脈絡補充
