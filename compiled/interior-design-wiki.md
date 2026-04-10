---
title: "室內設計與 DesignClaw — 知識 Wiki"
date: 2026-04-10
type: wiki
content_layer: L3
topic: interior-design
source_count: 5
last_compiled: 2026-04-10
_skip_sync: true
---

# 室內設計與 DesignClaw — 知識 Wiki

## 主題概述

DesignClaw 是一套 AI 驅動的室內裝修全自動管線系統，目標是將傳統室內設計流程（量屋、出圖、修改、施工）轉化為多 Agent 協作的端對端自動化流程。系統採用 7-Agent Pipeline 架構（Intake → Vision → Layout → Model → Render → Export → Deliver），以 OpenCode Agent 為底層運行時，參考 MetaClaw 自進化架構設計，每個設計環節由專屬 Agent 負責。[[2026-04-03_DesignClaw室內裝修自動化系統計畫]]

此專案的市場切入點是台灣危老都更帶來的龐大裝修需求。全台屋齡超過 30 年住宅突破 500 萬戶，2026 年裝修年產值預估上看 5,500 億台幣，但室內設計師嚴重不足。DesignClaw 借鑑 MEDVi 的輕資產模式（2 人公司做到 $401M 營收），以 AI 取代傳統設計人力瓶頸，結合大陸全屋定制供應鏈，切入「輕硬裝、重軟裝」的市場趨勢。[[2026-04-06_DesignClaw危老都更輕資產商業模式]]

截至 2026-04-04，技術層面已完成 Vision Agent V2（平面圖辨識）、Layout Agent、3D Viewer 及 Dashboard，渲染層確定採用 ComfyUI + SDXL RealVisXL V5.0 + Dual ControlNet 方案，部署於 RTX 3090。目前主要瓶頸在 Render Agent 的 AI 產圖環節，Export Agent 與 Deliver Agent 尚未開發。[[2026-04-03_DesignClaw進度紀錄]]

## 核心概念

### 7-Agent Pipeline 架構

DesignClaw 的核心是七個串接的 Agent：Intake（接案）→ Vision（平面圖辨識）→ Layout（空間規劃）→ Model（3D 建模）→ Render（AI 渲染）→ Export（輸出）→ Deliver（交付）。Agent 之間透過事件驅動的訊息系統串接，形成端對端自動化流程。[[2026-04-03_DesignClaw室內裝修自動化系統計畫]]

### Vision Agent（平面圖 AI 辨識）

Vision Agent 負責將平面圖（手繪或 CAD）轉化為結構化 JSON。V1 版本房間位置判斷不準確，V2 修正後能正確辨識 9 個空間並標註相對位置（主臥左上、客廳中間最大等）。這是整條管線的輸入源頭。[[2026-04-03_DesignClaw進度紀錄]]

### ComfyUI 渲染引擎

Render Agent 以 ComfyUI 作為核心渲染引擎，透過 REST API + WebSocket 整合。選用 SDXL 作為 base model（兼顧品質與 VRAM 需求），搭配 RealVisXL V5.0 寫實風格微調模型，在 RTX 3090 24GB VRAM 環境下實現 6 房間批量渲染，預估 3.5-5 分鐘完成。[[2026-04-04_ComfyUI室內設計渲染技術規劃]]

### Dual ControlNet 空間約束

渲染採用雙重 ControlNet 控制：Canny 邊緣偵測保持結構線條，Depth 深度圖維持空間感。雙控制器確保 AI 生成的渲染圖忠於原始平面圖的空間佈局，不會出現結構偏移。[[2026-04-04_DesignClaw-ComfyUI整合架構]]

### IP-Adapter 風格遷移

可選的 IP-Adapter 模組用於風格轉移，讓使用者提供參考圖片即可將特定設計風格套用到渲染結果上。目前預設風格為日式簡約，針對六種空間類型（客廳、臥室、廚房等）各自調校 prompt 和參數。[[2026-04-04_DesignClaw-ComfyUI整合架構]]

### 輕資產商業模式

借鑑 MEDVi 模式：自己只做品牌前端和 AI 驅動的獲客，所有後端（設計產出、供應鏈、施工）全部外包或平台化。核心壁壘是 AI 設計能力而非實體資產。結合大陸全屋定制供應鏈，用標準化模組降低成本。[[2026-04-06_DesignClaw危老都更輕資產商業模式]]

### 三層系統架構

系統分為三層：Layer 1 Agent 層（各功能 Agent）、Layer 2 基礎設施層（ComfyUI、Blender、FastAPI）、Layer 3 業務層（Notion 專案 UI + Google Drive 檔案倉庫 + Web 檢視器）。這種分層讓技術迭代不影響業務流程。[[2026-04-03_DesignClaw室內裝修自動化系統計畫]]

## 關鍵發現

> **MEDVi 模式可複製到室內設計產業**：2 人公司靠 AI + 模組化外包做到 $401M 營收。DesignClaw 的機會在於台灣危老都更創造的供需缺口——設計師不足但需求暴增，與 MEDVi 面對的 GLP-1 醫師短缺結構性相似。[[2026-04-06_DesignClaw危老都更輕資產商業模式]]

> **SDXL 是室內設計渲染的最佳平衡點**：SD 1.5 品質不足，Flux.1-dev 吃 VRAM 太重，SDXL 在 RTX 3090 上能兼顧 1024×1024 品質與批量渲染速度。搭配 RealVisXL V5.0 微調模型可達到接近照片級寫實效果。[[2026-04-04_ComfyUI室內設計渲染技術規劃]]

> **Dual ControlNet 是空間忠實度的關鍵**：單一 ControlNet 無法同時保證結構線條和空間深度，Canny + Depth 雙控制器的組合解決了 AI 渲染偏離原始平面圖的核心問題。[[2026-04-04_DesignClaw-ComfyUI整合架構]]

> **Vision Agent 從 V1 到 V2 的教訓**：V1 的房間位置判斷不準確，V2 修正後才能正確辨識空間。這說明平面圖辨識的精確度直接影響下游所有 Agent 的品質，是管線中最不能出錯的環節。[[2026-04-03_DesignClaw進度紀錄]]

> **「輕硬裝、重軟裝」趨勢有利於 AI 自動化**：硬裝簡化標準化意味著可以用模組化方案處理，軟裝個性化則是 AI 風格遷移（IP-Adapter）的優勢場域。市場趨勢與技術能力恰好匹配。[[2026-04-06_DesignClaw危老都更輕資產商業模式]]

## 跨筆記關聯

**系統計畫 → 技術實作 → 進度追蹤的演進鏈**：[[2026-04-03_DesignClaw室內裝修自動化系統計畫]] 定義了 7-Agent 架構和三層系統設計，[[2026-04-04_ComfyUI室內設計渲染技術規劃]] 與 [[2026-04-04_DesignClaw-ComfyUI整合架構]] 將其中 Render Agent 落地為具體的 ComfyUI 技術方案，而 [[2026-04-03_DesignClaw進度紀錄]] 記錄了實際開發中遇到的問題（Vision Agent V1 失準、Render Agent 卡關）。三者構成「規劃→實作→驗證」的完整迭代迴圈。

**技術規劃與整合架構的互補關係**：[[2026-04-04_ComfyUI室內設計渲染技術規劃]] 側重模型選型（SDXL vs Flux vs SD 1.5）和參數規劃，[[2026-04-04_DesignClaw-ComfyUI整合架構]] 則聚焦於 ComfyUI API 整合和工程實作。前者是「選什麼」，後者是「怎麼接」。

**商業模式與技術架構的策略對齊**：[[2026-04-06_DesignClaw危老都更輕資產商業模式]] 的輕資產策略要求技術端必須高度自動化、低人力介入。這解釋了為何 [[2026-04-03_DesignClaw室內裝修自動化系統計畫]] 要設計成全自動 Agent Pipeline 而非半自動輔助工具——商業模式的「2 人公司」目標決定了技術架構必須是端對端自動化。

## 待探索方向

- **Export Agent 與 Deliver Agent 的設計**：管線後半段尚未開發，需要定義輸出格式（BIM/IFC？PDF？3D 可互動？）和交付流程（與施工團隊的介面）。[[2026-04-03_DesignClaw進度紀錄]]
- **全屋定制供應鏈整合細節**：商業模式提到結合大陸全屋定制供應鏈，但具體的供應商對接、報價系統、物流串接尚未展開。[[2026-04-06_DesignClaw危老都更輕資產商業模式]]
- **多風格支援**：目前僅針對日式簡約風格調校 prompt，未來需擴展到北歐、工業、現代等風格，可能需要額外的 LoRA 微調或 IP-Adapter 風格庫。[[2026-04-04_ComfyUI室內設計渲染技術規劃]]
- **Render Agent 的 AI Service Hub 連線問題**：進度紀錄指出目前卡在此處，需要釐清是網路架構問題還是 API 相容性問題。[[2026-04-03_DesignClaw進度紀錄]]
- **MetaClaw 自進化機制的實際導入**：系統計畫提到參考 MetaClaw 的「抓取→學習→進化」模式，但目前各 Agent 尚無自我學習迴路的具體設計。[[2026-04-03_DesignClaw室內裝修自動化系統計畫]]
- **客戶獲取與市場驗證**：輕資產模式的前提是有效的獲客引擎，需驗證 AI 生成的渲染圖是否足以說服屋主下單，以及定價策略與傳統設計師的競爭力比較。[[2026-04-06_DesignClaw危老都更輕資產商業模式]]
