---
title: DesignClaw 專案進度紀錄（2026-04-03）
date: 2026-04-03
category: work-logs
tags: [DesignClaw, AI, interior-design, agent-pipeline, three-js, 3D, render, FastAPI]
type: report
project: DesignClaw
priority: P1
status: draft
---

## 摘要

DesignClaw 是一套 AI 室內設計自動化管線，採 7-Agent Pipeline 架構：Intake → Vision → Layout → Model → Render → Export → Deliver。截至 2026-04-03，Vision Agent V2、Layout Agent、3D Viewer、Dashboard 及日式簡約設計概念皆已完成；目前卡在 Render Agent 的 AI 產圖環節（AI Service Hub 連線問題），Export Agent 與 Deliver Agent 尚未開發。

## 已完成項目

### 1. 專案初始化

designclaw/ 目錄結構已建立於 `~/Desktop/designclaw/`，包含各 agent 模組及測試輸出目錄。

### 2. Vision Agent（V1 → V2）

- V1：實現平面圖辨識功能，但房間位置判斷不準確。
- V2（修正版）：正確辨識出 9 個空間——主臥（左上）、書房（右上）、客廳（中間最大）、廚房（左下）等，輸出為結構化 JSON。

### 3. Layout Agent

根據 Vision Agent V2 的輸出，自動生成家具配置 JSON，共配置 24 件家具，包含位置座標與尺寸資訊。

### 4. 3D Viewer（Three.js 互動視圖）

功能包含：OrbitControls 旋轉/縮放、CSS2DRenderer 房間標籤、Raycaster 家具 hover tooltip、多視角切換。

### 5. Dashboard

`designclaw_dashboard.html` 整合所有管線產出，提供單頁總覽介面。

### 6. 日式簡約設計概念

完成 6 個房間的設計 prompt，涵蓋材質、色彩方案及家具描述，供 Render Agent 使用。

## 進行中 / 卡住

### Render Agent（AI 產圖）— 阻塞中

需透過 Alan 的 AI Service Hub（Mac Mini 上的 FastAPI 服務）產生真實感渲染圖。

- Endpoint: `POST /api/image/generate`，model: `flow`
- 免費替代方案（Pollinations、flux1.ai）皆因限速或需登入而無法使用
- AI Hub 目前從 Chrome 瀏覽器也連不上，疑似 Tailscale 網路問題或服務未啟動

**解除阻塞需要：** 確認 Mac Mini 上 FastAPI 服務已啟動，並排查 Tailscale 連線狀態。

### Export Agent & Deliver Agent — 尚未開發

待 Render Agent 通後再進行開發。

## 待開發

- **Layer 1: OpenCode Agent Runtime** — 使用 OpenHarness 或類似框架跑完整 agent pipeline 自動化
- **Layer 3: Business Layer** — Notion / Google Drive / Web Viewer 整合，讓最終產出可交付給客戶

## 相關檔案

- `~/Desktop/designclaw/test_outputs/3d_viewer.html` — 互動 3D 視圖
- `~/Desktop/designclaw/test_outputs/floorplan_formal_design_v2.json` — 修正版 Vision 輸出
- `~/Desktop/designclaw/test_outputs/design_renders.html` — 渲染 prompt 頁面
- `~/Desktop/designclaw/test_outputs/designclaw_dashboard.html` — 儀表板

## 行動項目

- [ ] 排查 Tailscale 連線 & 確認 Mac Mini FastAPI 服務狀態
- [ ] Render Agent 接通 AI Service Hub 後，跑 6 個房間的渲染
- [ ] 開發 Export Agent（輸出 PDF / 圖片包）
- [ ] 開發 Deliver Agent（自動交付至客戶端）
- [ ] 規劃 OpenCode Agent Runtime 整合方案
- [ ] 規劃 Business Layer（Notion / GDrive / Web Viewer）
