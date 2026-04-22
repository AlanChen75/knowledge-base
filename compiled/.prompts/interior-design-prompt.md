# 任務：編譯「室內設計與 DesignClaw」知識 Wiki 頁

你是 SecondBrain 知識編譯器。以下是「室內設計與 DesignClaw」主題下的 5 篇筆記摘要。
主題描述：室內設計自動化、DesignClaw pipeline、ComfyUI 渲染、危老都更

## 要求

請根據以下筆記內容，產出一篇結構化的知識 Wiki 頁，格式如下：

```
---
title: "室內設計與 DesignClaw — 知識 Wiki"
date: 2026-04-22
type: wiki
content_layer: L3
topic: interior-design
source_count: 5
last_compiled: 2026-04-22
_skip_sync: true
---

# {主題名稱} — 知識 Wiki

## 主題概述
(2-3 段，概括此主題的核心範圍、為何重要、目前發展階段)

## 核心概念
(列出 5-10 個核心概念，每個用 ### 小節，2-3 句說明 + Wiki Link 引用來源筆記)

## 關鍵發現
(從筆記中提煉的重要洞見，每條用 > blockquote + 來源 Wiki Link)

## 跨筆記關聯
(不同筆記之間的連結、矛盾、演進關係)

## 待探索方向
(筆記中提到但尚未深入的議題，供未來研究)
```

## 引用規則

- 每個段落都必須用 `[[note-filename]]` 或 `[[note-filename|顯示名稱]]` Wiki Link 引用來源筆記
- filename 就是下方每篇筆記的 `filename` 欄位（不含 .md）
- 不要虛構不存在的筆記名稱

---

## 筆記清單（共 5 篇）

### [1/5] DesignClaw 危老都更輕資產商業模式架構
- **filename**: `2026-04-06_DesignClaw危老都更輕資產商業模式`
- **path**: `dispatch-outputs/2026-04-06_DesignClaw危老都更輕資產商業模式.md`
- **date**: 2026-04-06
- **category**: business-model
- **tags**: DesignClaw, 危老重建, 都更, 室內設計, AI, 全屋定制, 輕資產, MEDVi

**內容摘要：**

## 背景：從 MEDVi 模式到 DesignClaw

MEDVi 是一家只有 2 人的美國遠距醫療公司，2025 年銷售額 $401M，靠 AI + 模組化外包做到極致輕資產。創辦人 Matthew Gallagher 用 $20,000 在 2 個月內從零到上線，所有後端（醫師網路、藥局、物流）全部外包，自己只做品牌前端和 AI 驅動的獲客。

DesignClaw 要套用同樣的框架，切入台灣危老都更的室內裝修設計市場，結合大陸全屋定制供應鏈。

## 一、市場機會（時間窗口分析）

### 供需缺口 = MEDVi 的「GLP-1 短缺」

- 全台屋齡超過 30 年住宅突破 500 萬戶
- 2024 年危老都更核准累計破 5,172 件，政府加速推動 8,216 棟 6 層以上老屋改建（約 27 萬戶）
- 2026 年裝修年產值預估上看 5,500 億台幣
- 室內設計師嚴重不足，傳統設計流程慢（量屋→出圖→來回修改→施工），一個設計師同時能接的案有限

### 結構性利多：輕硬裝＋重軟裝趨勢

- 2026 年台灣設計趨勢核心：「輕硬裝、重軟裝」
- 硬裝簡化標準化 
(...截斷)

---

### [2/5] ComfyUI 室內設計渲染技術規劃
- **filename**: `2026-04-04_ComfyUI室內設計渲染技術規劃`
- **path**: `dispatch-outputs/2026-04-04_ComfyUI室內設計渲染技術規劃.md`
- **date**: 2026-04-04
- **category**: tech/ai-ml
- **tags**: ComfyUI, Stable-Diffusion, SDXL, ControlNet, 室內設計, AI渲染, DesignClaw, IP-Adapter, LoRA, prompt-engineering

**內容摘要：**

# ComfyUI 室內設計渲染技術規劃

**DesignClaw Render Agent 整合方案**
**硬體環境：** NVIDIA RTX 3090 (24GB VRAM)
**日期：** 2026-04-04

---

## 摘要

本文件規劃 DesignClaw 自動化管線中 Render Agent 的技術實作方案，以 ComfyUI 作為核心渲染引擎，整合 SDXL base model、Dual ControlNet（floor plan 空間約束）、IP-Adapter（風格遷移）和日式簡約風格 prompt engineering，在 RTX 3090 24GB VRAM 環境下實現 6 房間批量渲染（預估 3.5–5 分鐘），輸出至少 1024×1024 的寫實室內設計渲染圖。

---

## 1. 最適合室內設計的 Model 組合

### 1.1 Base Model 選擇：SDXL vs Flux vs SD 1.5

| 特性 | SD 1.5 | SDXL | Flux.1-dev |
|------|--------|------|---
(...截斷)

---

### [3/5] DesignClaw ComfyUI 整合架構
- **filename**: `2026-04-04_DesignClaw-ComfyUI整合架構`
- **path**: `dispatch-outputs/2026-04-04_DesignClaw-ComfyUI整合架構.md`
- **date**: 2026-04-04
- **category**: tech/ai-ml
- **tags**: DesignClaw, ComfyUI, SDXL, ControlNet, Render-Agent, 室內設計, AI渲染

**內容摘要：**

# DesignClaw ComfyUI 整合架構

## 摘要

DesignClaw 的 Render Agent 層已完成實作，透過 ComfyUI REST API + WebSocket 將 SDXL RealVisXL V5.0 整合進室內設計渲染流水線。支援 dual ControlNet（Canny 結構線 + Depth 空間感）與可選的 IP-Adapter 風格轉移，針對六種日式簡約空間類型各自調校 prompt 和參數。目標部署機器為 ac-3090（RTX 3090, 24GB VRAM）。

---

## 1. 完整架構：ComfyUI 整合到 DesignClaw Render Agent

```
DesignClaw Pipeline
───────────────────────────────────────────────────────────
平面圖輸入（JPG/PNG）
    │
    ▼
[Render Agent — render_agent.py]
    │  ├── 載入 workflow template (japanes
(...截斷)

---

### [4/5] DesignClaw — AI 室內裝修全自動管線系統計畫
- **filename**: `2026-04-03_DesignClaw室內裝修自動化系統計畫`
- **path**: `dispatch-outputs/2026-04-03_DesignClaw室內裝修自動化系統計畫.md`
- **date**: 2026-04-03
- **category**: tech/ai-ml
- **tags**: DesignClaw, 室內設計, OpenCode, MetaClaw, 多代理, BIM, IFC, 自動化管線, AI-Agent

**內容摘要：**

# DesignClaw — AI 室內裝修全自動管線系統計畫

## 一、系統定位

DesignClaw 是一套以 OpenCode Agent 為底層運行時、參考 MetaClaw 自進化架構設計的 AI 室內裝修全自動協作管線。每個設計環節由專屬 Agent 負責，Agent 之間透過事件驅動的訊息系統串接，形成從「手繪草稿」到「施工交付」的端對端自動化流程。

核心理念：**把 MetaClaw 的「Claw」（抓取 → 學習 → 進化）模式套用到室內設計產業的每一個環節。**

---

## 二、架構總覽

### 2.1 三層架構

```
┌─────────────────────────────────────────────────────────┐
│                    Layer 3: 業務層                        │
│  Notion（專案 UI）+ Google Drive（檔案倉庫）+ Web 檢視器   │
└────────────────────────┬───────────────────────
(...截斷)

---

### [5/5] DesignClaw 專案進度紀錄（2026-04-03）
- **filename**: `2026-04-03_DesignClaw進度紀錄`
- **path**: `dispatch-outputs/2026-04-03_DesignClaw進度紀錄.md`
- **date**: 2026-04-03
- **category**: work-logs
- **tags**: DesignClaw, AI, interior-design, agent-pipeline, three-js, 3D, render, FastAPI

**內容摘要：**

## 摘要

DesignClaw 是一套 AI 室內設計自動化管線，採 7-Agent Pipeline 架構：Intake → Vision → Layout → Model → Render → Export → Deliver。截至 2026-04-03，Vision Agent V2、Layout Agent、3D Viewer、Dashboard 及日式簡約設計概念皆已完成；目前卡在 Render Agent 的 AI 產圖環節（AI Service Hub 連線問題），Export Agent 與 Deliver Agent 尚未開發。

## 已完成項目

### 1. 專案初始化

designclaw/ 目錄結構已建立於 `~/Desktop/designclaw/`，包含各 agent 模組及測試輸出目錄。

### 2. Vision Agent（V1 → V2）

- V1：實現平面圖辨識功能，但房間位置判斷不準確。
- V2（修正版）：正確辨識出 9 個空間——主臥（左上）、書房（右上）、客廳（中間最大）、廚房（左下）等，輸出為結構化 JSON。

### 
(...截斷)

---
