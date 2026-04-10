---
title: "Teachify 開課快手研究與 ClassClaw 整合分析"
date: 2026-04-04
category: tech/tools
type: analysis
project: ClassClaw
priority: P1
status: draft
tags:
  - Teachify
  - ClassClaw
  - 線上課程
  - API
  - 自動化
  - SaaS
---

# Teachify 開課快手 平台研究報告

> 研究日期：2026-04-04
> 目的：分析 Teachify 平台能力，評估與 ClassClaw 教育自動化管線的整合可行性

---

## 1. Teachify 開課快手是什麼？

Teachify 開課快手是一個**台灣本土的 SaaS 線上開課平台**，成立於 2019 年，專注於讓創作者與講師快速建立自己的獨立數位知識商店。它的定位是「知識電商」——結合自架網站與課程系統的一站式解決方案。

### 核心特色

- **自架品牌網站**：每位用戶擁有獨立網域的課程網站，30 秒內即可註冊建站
- **多元內容格式**：支援影片課程、數位產品下載、直播活動、訂閱制文章專欄
- **台灣在地化金流**：信用卡、ATM 轉帳、超商繳費、LINE PAY，並支援電子發票
- **零抽成模式**：不抽取課程銷售分潤（一般平台抽 5-12%），僅收月費
- **繁體中文後台**：完整中文介面，對台灣創作者友善

### 方案價格

| 方案 | 月均費用 | 適合對象 |
|------|---------|---------|
| Lite 輕量版 | NT$840/月 | 剛起步、逐步建立流量 |
| Basic 基本版 | NT$3,150/月 | 穩定經營線上課程收入 |
| Professional 專業版 | NT$6,300/月 | 有經驗、正在擴展課程與銷售模式 |
| Business 企業版 | 客製報價 | 企業內訓、客製化學習方案 |

提供 14 天免費試用（專業版），可隨時升降級，無合約綁定。

### 主要功能模組

- **課程管理**：課程上架、章節管理、作業繳交與評分、證書核發
- **學員管理**：會員系統、學習進度追蹤、課程留言、課前留言
- **銷售與行銷**：多種定價方案設定、折扣碼、銷售頁面
- **數據追蹤**：GA4、Facebook Pixel、Google Tag Manager 整合
- **訂單管理**：視覺化後台、付款狀態追蹤、可匯出 Excel/CSV
- **第三方整合**：Zapier、ConvertKit、Zoom 等

---

## 2. 技術架構與 API 能力

### 2.1 Admin API（GraphQL）

Teachify 提供了 **GraphQL 架構的 Admin API**，開發者文件位於 `teachify.dev`。

**目前狀態：API 文件標註為「Preview（預覽）」，尚未正式對外開放公開使用。**

已知的 API 能力包括：

- **Courses Query**：查詢學校中的課程列表、取得特定課程詳情及相關資料
- **Course Mutations**：程式化建立、更新、刪除課程
- **認證方式**：API Key，綁定特定學校與已授權的應用程式
- **速率限制**：有實施速率限制以確保公平使用（具體數值未公開）
- **最佳實踐文件**：提供 Query/Mutation 結構化建議

### 2.2 Webhooks

Teachify 支援 **Incoming/Outgoing Webhooks**，可在特定事件觸發時發送通知到外部系統。

已知支援的事件類型：

- 付款成功（Payment Success）
- 訂閱成功（Subscription Success）
- 退費成功（Refund Success）
- 訂單建立（Order Created）

Webhook 請求格式為 JSON，建議接收端驗證請求來源的可信度後，再根據業務邏輯處理資料。

### 2.3 OAuth 整合

- 支援 OAuth 整合流程，提供 User Information Endpoint
- 企業版支援 SSO 單一登入，跨不同事業體統一會員管理
- 有 OAuth Integration Quickstart 文件

### 2.4 第三方整合

- **Zapier**：官方支援，可串接數千種第三方工具建立自動化流程
- **ConvertKit**：Email 行銷整合
- **Zoom**：線上直播課程整合
- **GA4 / Facebook Pixel / GTM**：數據追蹤與廣告投放

---

## 3. Claude Code 串接 Teachify 的經驗

### 目前現況

根據研究，**目前沒有找到公開的 Claude Code 串接 Teachify 的案例或經驗分享**。這兩個工具分屬不同領域（AI 開發工具 vs. 線上開課平台），目前社群中尚未出現明確的整合嘗試。

### 預期會遇到的困難

1. **API 尚在預覽階段**：Admin API 標註為 Preview，可能隨時變更、功能不完整、或有存取限制
2. **API Key 取得門檻不明**：不確定是否需要申請、審核，或僅限特定方案
3. **GraphQL Schema 不完整**：預覽版可能缺少某些 Mutation（如批次建課、內容上傳）
4. **文件存取受限**：`teachify.dev` 的開發者文件在部分網路環境下無法存取
5. **無官方 SDK**：沒有 Python/Node.js SDK，需自行封裝 GraphQL Client
6. **速率限制未知**：大量自動化操作可能觸發限制

---

## 4. ClassClaw 整合策略

ClassClaw 作為教育自動化管線，以下是與 Teachify 各面向的整合分析：

### 4.1 課程建立自動化（從大綱自動建課）

**可行性：中等（取決於 API 正式開放）**

- Course Mutations API 已支援「建立、更新、刪除」課程
- 理想流程：大綱 Markdown → Claude 解析 → GraphQL Mutation 建立課程結構
- 限制：Preview API 可能不支援完整的章節、單元層級操作
- 替代方案：透過 Zapier 作為中間層觸發課程建立

```
ClassClaw Pipeline:
課程大綱（Markdown/Notion）
  → Claude 解析為結構化 JSON
  → GraphQL API: createCourse mutation
  → GraphQL API: addSection / addLesson mutations
  → 回傳課程 URL
```

### 4.2 學員管理

**可行性：中等**

- Webhook 可接收「付款成功」「訂閱成功」等事件，觸發下游自動化
- 訂單資料可匯出 Excel/CSV，支援批次處理
- 整合方向：Webhook 事件 → ClassClaw 處理 → CRM 更新 / Email 序列觸發

```
Teachify Webhook (付款成功)
  → ClassClaw 接收
  → 更新學員 CRM 紀錄
  → 觸發 Welcome Email 序列
  → 分配學習路徑
```

### 4.3 內容上傳

**可行性：低（目前）**

- API 文件中未明確提及影片/檔案上傳的 Mutation
- 影片通常透過 Teachify 後台手動上傳或串接影片託管服務
- 可能需要瀏覽器自動化作為替代方案

### 4.4 銷售頁面生成

**可行性：低至中等**

- Teachify 提供內建的銷售頁面編輯器，但 API 是否支援頁面內容操作尚不明確
- 可能的替代方案：Claude 生成銷售文案 → 手動或透過瀏覽器自動化貼入
- Zapier 整合可能提供部分自動化能力

---

## 5. 替代方案：當 API 不可用時

如果 Teachify 的 API 持續處於預覽階段或功能不足，以下是替代整合方案：

### 5.1 Playwright 瀏覽器自動化（推薦）

```python
# 概念範例：使用 Playwright 自動化 Teachify 後台操作
from playwright.async_api import async_playwright

async def create_course(title, description, sections):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('https://your-school.teachify.tw/admin')
        # 登入 → 建立課程 → 填入資料 → 發布
```

優點：可操作所有後台功能，不受 API 限制
缺點：脆弱（UI 變更即失效）、速度慢、需維護 Session

### 5.2 Chrome DevTools Protocol (CDP)

- 比 Playwright 更底層的控制
- 可搭配 Claude Code 的 MCP Browser 工具使用
- 適合需要精細控制（如攔截網路請求、注入腳本）的場景

### 5.3 Zapier 作為中間層（最穩定）

```
ClassClaw → Zapier Webhook → Teachify 原生整合
```

- Teachify 官方支援 Zapier，穩定性最高
- 限制：Zapier 免費方案有任務數限制，付費方案有額外成本
- 適合：中低頻率的自動化操作（如新課程建立、學員通知）

### 5.4 混合策略（推薦的實務做法）

| 操作類型 | 建議方案 | 原因 |
|---------|---------|------|
| 課程 CRUD | GraphQL API（若可用）或 Zapier | 結構化操作，API 最適合 |
| 學員事件處理 | Webhook + ClassClaw | 即時性高，Webhook 已穩定 |
| 內容上傳 | Playwright 自動化 | API 不支援，需模擬人工操作 |
| 銷售頁面 | Claude 生文案 + Playwright | 半自動化，人工審核後發布 |
| 數據分析 | CSV 匯出 + Python 處理 | 後台支援匯出，可批次分析 |

---

## 6. 總結與建議

### Teachify 對 ClassClaw 的整合評級

| 面向 | 評級 | 說明 |
|------|------|------|
| API 成熟度 | ⭐⭐ (2/5) | GraphQL API 存在但仍為 Preview |
| Webhook 支援 | ⭐⭐⭐⭐ (4/5) | 核心付款事件已支援 |
| 第三方整合 | ⭐⭐⭐⭐ (4/5) | Zapier、GA4、Pixel 等成熟 |
| 自動化友善度 | ⭐⭐⭐ (3/5) | 有基礎，但完整自動化仍受限 |
| 文件完整度 | ⭐⭐ (2/5) | 開發者文件為預覽版，細節不足 |

### 行動建議

1. **短期**：以 Webhook + Zapier 為核心，建立學員事件的自動化流程
2. **中期**：申請 Admin API 存取權限，測試 Course CRUD 操作的穩定性
3. **長期**：根據 API 正式開放的進度，逐步將 Playwright 自動化替換為原生 API 呼叫
4. **備案**：持續關注 Teachify 的 Product Roadmap（他們有公開的開發計畫頁面），評估 API 完善的時程

### 關鍵風險

- Admin API 可能長期停留在 Preview，無法用於生產環境
- Playwright 自動化依賴 UI 穩定性，Teachify 改版可能導致腳本失效
- Teachify 作為台灣在地平台，英文技術社群資源相對稀少

---

## 參考資料

- [Teachify 官方網站](https://teachify.tw/)
- [Teachify 功能特色](https://teachify.tw/features/)
- [Teachify 開發者文件](https://teachify.dev/)
- [Teachify Admin API](https://teachify.dev/api/admin/)
- [Teachify Webhooks](https://teachify.dev/webhooks/overview/)
- [Teachify OAuth 整合](https://teachify.dev/oauth_integration/quickstart/)
- [Teachify 價格方案](https://teachify.tw/pricing/)
- [Teachify Product Roadmap](https://teachify.tw/product-roadmap)
- [Teachify 開課快手完整評測 — 領先時代](https://leadingmrk.com/teachify-tutorial/)
- [Teachify 評價 — 席斯琳](https://sislin.me/teachify-review/)
- [2026 線上開課平台評比 — Teachify 部落格](https://blog.teachify.tw/posts/%E9%96%8B%E8%AA%B2%E5%B9%B3%E5%8F%B0%E6%80%8E%E9%BA%BC%E9%81%B8%EF%BC%9F%E7%B7%9A%E4%B8%8A%E9%96%8B%E8%AA%B2%E5%B8%B8%E8%A6%8B%E5%95%8F%E7%AD%94%E8%88%87%E6%AF%94%E8%BC%83/)
