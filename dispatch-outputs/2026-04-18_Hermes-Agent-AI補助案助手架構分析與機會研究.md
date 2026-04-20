---
title: "Hermes Agent × Telegram × LLM Wiki — AI 補助案助手架構分析與機會研究"
date: 2026-04-18
category: tool-analysis
tags: [Hermes-Agent, Telegram, LLM-Wiki, ChatGPT, government-grants, SBIR, SIIR, CITD, AI-agent, automation, business-opportunity]
type: analysis
source: 社群貼文 + WebSearch 查證
project: Claw 生態系
priority: P2
status: active
---

## 原始貼文摘要

一位計劃輔導顧問分享了他用「Hermes Agent × Telegram × LLM Wiki × ChatGPT」串起來的 AI 計劃書助手：

1. 每天定期巡查相關網站，追最新補助公告，下載相關資料
2. 根據下載的申請須知，自動產生訪綱與索資清單
3. 針對特定計劃內容做即時問答，不用再翻 PDF
4. 具備長短期記憶，知道目前在處理哪一案、哪個計劃、還缺什麼資料

定位：第一個能協助計劃輔導顧問工作的「AI 員工」。

---

## Part 1：系統架構分析

### 各元件角色

**Hermes Agent**（Nous Research 開源框架）
- GitHub 95.6K+ stars 的開源 AI Agent 框架
- 內建 Cron 排程（定時巡查網站）、Telegram Bot 整合、40+ 工具
- 支援 Function Calling，可串接各種 API
- 在此系統中扮演「排程引擎 + 任務調度器」角色
- 官方：https://github.com/NousResearch/Hermes-Function-Calling

**LLM Wiki**（Karpathy 提出的概念）
- 核心理念：AI 主動維護的知識庫，不只是 RAG 的「查詢→檢索→回答」
- 新資訊被「整合」進現有知識，而非只是索引
- 類似我的 compile.py 概念——把原始筆記合成為 wiki 頁面
- 在此系統中扮演「知識演化層」，讓 AI 越來越了解每個補助計畫
- 參考：https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

**Telegram**
- 人機互動介面（手機友好）
- 類似 Paper Pipeline 中 Slack 的角色
- 推送新公告通知 + 接收使用者提問

**ChatGPT**
- 最終的 LLM 推理引擎
- 讀 PDF、產生訪綱、即時問答

### 整體流程

```
[Hermes Agent Cron]
    ↓ 定時觸發
[巡查政府網站] → 偵測新公告 → 下載 PDF/文件
    ↓
[LLM Wiki 整合] → 更新知識庫（不只存檔，而是理解+合成）
    ↓
[Telegram 推送] → 通知使用者有新公告
    ↓
[使用者互動] → 問答 / 產生訪綱 / 索資清單
    ↓
[ChatGPT 推理] → 基於 LLM Wiki 的知識回答
```

### 與 SecondBrain + Cowork 架構對比

| 維度 | Hermes Agent 系統 | SecondBrain + Cowork |
|------|------------------|---------------------|
| 輸入 | Cron 自動巡查 + Telegram 手動輸入 | 手動丟給 Dispatch 處理 |
| 知識存儲 | LLM Wiki（AI 主動合成） | YAML frontmatter + markdown |
| 知識演化 | 自動整合新資訊到現有知識 | compile.py（規劃中） |
| 互動介面 | Telegram Bot | Cowork Dispatch |
| LLM 使用 | 每次互動都用 | 只在 compile 階段用 |
| Token 效率 | 較高消耗（每次都過 LLM） | 較省（本地存取不需 token） |
| 主動性 | 高（自動巡查 + 推送） | 低（被動接收指令） |

**最值得借鏡的兩點**：
1. **主動巡查模式** — Hermes Agent 的 Cron 排程 = Cowork 排程任務的完美用例
2. **知識演化機制** — LLM Wiki 的「整合而非索引」= compile.py 的核心理念

---

## Part 2：應用場景分析

### 「監控 → 擷取 → 轉化 → 互動」通用模式

這個流程模式是高度通用的：

| 領域 | 監控對象 | 轉化產出 | 互動需求 |
|------|---------|---------|---------|
| 政府補助 | 補助公告網站 | 訪綱、索資清單 | 計畫問答 |
| 學術研究 | 期刊 RSS | 論文筆記、文獻綜述 | 研究問答 |
| 法規合規 | 法規公報 | 合規檢查表 | 法規解讀 |
| 招標監控 | 政府電子採購網 | 投標評估表 | 標案問答 |
| 專利追蹤 | 專利公報 | 技術趨勢報告 | 侵權分析 |
| ESG 法規 | 各國 ESG 公報 | 合規差異表 | 報告產出 |
| 競品監控 | 競品網站/社群 | 競品動態報告 | 策略問答 |

### 與 Paper Pipeline 的同構性

Paper Pipeline（獸醫論文）和這個系統本質上同構：

```
Paper Pipeline:   RSS掃描 → Slack emoji → Claude讀PDF → Notion筆記
Hermes 補助助手:  Cron巡查 → Telegram通知 → ChatGPT讀PDF → LLM Wiki
SecondBrain:      手動輸入 → Dispatch處理 → YAML+markdown → compile.py
```

差異只在「領域設定檔」——監控哪些網站、用什麼模板、存到哪裡。底層的 Agent 框架是一樣的。

---

## Part 3：台灣 AI 相關政府補助計畫

### 主要計畫一覽

#### 1. SBIR 小型企業創新研發計畫
- **主管機關**：經濟部中小及新創企業署
- **補助金額**：
  - Phase 1（先期研究）：最高 100 萬 / 6 個月
  - Phase 2（研究開發）：最高 600 萬 / 1 年，或 1,200 萬 / 2 年
  - Phase 2+（加值應用）：最高 500 萬 / 1 年
- **申請時程**：隨到隨審（常年開放）
- **適用**：AI 產品/服務的研發
- **官方網站**：https://www.sbir.org.tw/

#### 2. SIIR 服務業創新研發計畫
- **主管機關**：經濟部商業發展署
- **補助金額**：最高 200-500 萬（依計畫類型）
- **申請時程**：年度公告
- **適用**：AI 導入服務業的創新應用
- **官方網站**：https://gcis.nat.gov.tw/neo-s/Web/Default.aspx

#### 3. CITD 協助傳統產業技術開發計畫
- **主管機關**：經濟部產業發展署
- **補助金額**：最高 200-300 萬
- **申請時程**：年度公告
- **適用**：傳統產業導入 AI 技術升級
- **官方網站**：https://citd.cpc.tw/

#### 4. AI+ 產業共創計畫
- **主管機關**：數位發展部 / 經濟部
- **補助金額**：依計畫規模，最高可達數百萬
- **適用**：AI 技術與產業結合的示範計畫
- **官方網站**：https://aisubsidy.tca.org.tw/

#### 5. DIGITAL+ 數位轉型計畫
- **主管機關**：數位發展部
- **補助金額**：依計畫類型
- **適用**：企業數位轉型，包含 AI 導入
- **官方網站**：https://digiplus.adi.gov.tw/

#### 6. 國科會研究計畫
- **主管機關**：國家科學及技術委員會
- **補助金額**：依計畫規模
- **適用**：AI 基礎研究、應用研究
- **申請時程**：年度公告（通常 8-10 月）
- **官方網站**：https://www.nstc.gov.tw/

#### 7. 文化部文化科技計畫
- **主管機關**：文化部
- **適用**：AI 結合文化內容產業（影視、出版、表演藝術等）
- **官方網站**：https://www.moc.gov.tw/

#### 8. 工業局智慧機械計畫
- **主管機關**：經濟部產業發展署
- **適用**：AI + 智慧製造
- **官方網站**：https://www.moeaidb.gov.tw/

#### 9. 地方政府 SBIR
- **主管機關**：各縣市政府
- **補助金額**：通常 50-100 萬
- **適用**：在地產業 + AI 應用
- **特點**：門檻較低，適合初創公司

### 補助計畫資訊彙整來源

- JustSyn 補助總整理：https://justsyn.com/
- 中小企業處：https://www.moeasmea.gov.tw/
- 政府補助資源網：https://www.gov.tw/

---

## Part 4：商業機會分析

### 市場規模

台灣每年政府補助案相關市場：
- 管顧公司代寫計畫書：估計年產值 15-30 億台幣
- 每年 SBIR 收件量：約 2,000-3,000 件
- 加上 SIIR、CITD、國科會等，全年約 8,000-10,000 件補助申請
- 每件計畫書代寫費用：5-30 萬（依複雜度）

### 目標客戶

1. **管顧公司 / 計畫輔導顧問**（最直接）— 提高產能、降低重複工作
2. **中小企業主**（量最大）— 自己寫計畫書、省管顧費
3. **會計師事務所**（高價值）— 協助客戶申請補助是增值服務
4. **大學產學合作處**（穩定需求）— 國科會計畫書批量處理
5. **創投/加速器**（影響力大）— 協助被投公司申請補助

### 競爭分析

台灣目前**沒有專門的「AI 補助案助手」SaaS**。現有的：
- 管顧公司用人力處理（主流）
- 部分管顧用 ChatGPT 輔助（但沒有系統化）
- 有些法規監控工具（如 LawSnote），但不做補助案

**這是一個空白市場。**

### 與 Claw 生態系的交集

- **GovClaw**（假設的補助案助手 Plugin）可以是 Claw 的一個垂直應用
- 技術棧跟 SecondBrain 高度重疊：巡查 → 存儲 → 合成 → 問答
- Cowork 排程任務可以直接支持「每日巡查政府網站」
- compile.py 的跨筆記合成 = 跨計畫的知識整合

### 建議策略

1. **短期**：先做 Cowork Plugin 驗證 PMF（最小可行產品）
2. **中期**：如果 PMF 驗證成功，考慮獨立 SaaS
3. **定價**：月費 2,000-5,000 / 管顧版年費 50,000-100,000
4. **差異化**：不只是「AI 寫計畫書」，而是「全流程自動化助手」

---

## 後續待辦

- [ ] 評估 Hermes Agent 框架是否適合整合進 Claw 生態系
- [ ] 測試 Cowork 排程任務巡查 SBIR 網站的可行性
- [ ] 研究 LLM Wiki 概念如何整合進 compile.py 設計
- [ ] 考慮「GovClaw」作為 Claw 垂直應用的可能性

---

## 交叉連結

- [[2026-04-17_Paper-Pipeline工作流對照分析|Paper Pipeline 對照分析]]：同構的「監控→擷取→轉化→互動」模式
- [[2026-04-09_Graphify-RAG機制與對話知識庫方案深度分析|Graphify RAG 深度分析]]：LLM Wiki 的「知識演化」概念與 Graphify 的社群偵測相呼應
- [[2026-04-09_Graphify知識圖譜工具分析與SecondBrain整合評估|Graphify 整合評估]]：知識庫架構的不同選擇

---

## Sources

- [Hermes Agent - Nous Research GitHub](https://github.com/NousResearch/Hermes-Function-Calling)
- [Karpathy LLM Wiki 概念](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [SBIR 官方網站](https://www.sbir.org.tw/)
- [SIIR 官方網站](https://gcis.nat.gov.tw/neo-s/Web/Default.aspx)
- [CITD 官方網站](https://citd.cpc.tw/)
- [AI+ 產業共創計畫](https://aisubsidy.tca.org.tw/)
- [DIGITAL+ 平台](https://digiplus.adi.gov.tw/)
- [JustSyn 台灣補助總整理](https://justsyn.com/)
