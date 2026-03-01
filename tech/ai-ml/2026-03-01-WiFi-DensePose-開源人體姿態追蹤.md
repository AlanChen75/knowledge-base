---
title: WiFi DensePose：無需攝影機的 WiFi 人體姿態追蹤系統
date: 2026-03-01
source: https://unwire.hk/2026/02/28/wifi-densepose-github-open-source/tech-secure/
category: tech/ai-ml
tags: [WiFi, CSI, 人體姿態追蹤, 電腦視覺, 開源專案, MIT授權, 隱私保護, 即時偵測]
type: article
raw_file: ../../raw/2026-03/2026-03-01-085759-url.txt
difficulty: ⭐⭐⭐⭐
author: Reuven Cohen
---

# WiFi DensePose：無需攝影機的 WiFi 人體姿態追蹤系統

## 📊 元資訊
- **難度**：⭐⭐⭐⭐
- **來源類型**：技術新聞 / 開源專案
- **作者**：Reuven Cohen
- **筆記時間**：2026-03-01 08:57

## 📌 摘要
WiFi DensePose 是一個突破性的開源專案，利用普通 WiFi 路由器的 Channel State Information (CSI) 訊號，無需攝影機即可即時追蹤人體姿態，並能穿透牆壁進行偵測。系統達到 94.2% 姿態偵測準確率和 96.5% 跌倒偵測靈敏度，延遲低於 50 毫秒，支援同時追蹤 10 人。

## 🏷️ 標籤分類
- **大分類**：tech
- **小分類**：ai-ml
- **技術領域**：電腦視覺、訊號處理、人體姿態估計
- **應用領域**：醫療保健、智慧家居、健身、安全監控

## 🔑 關鍵要點

1. **突破性技術**：使用 WiFi CSI 訊號取代攝影機進行人體姿態追蹤，可穿透牆壁運作
2. **高效能表現**：姿態偵測準確率 94.2%、跌倒偵測靈敏度 96.5%、延遲 < 50ms、30 FPS 輸出
3. **多人追蹤能力**：同時支援最多 10 人的即時追蹤和身份識別維持
4. **開源友善**：MIT 授權、支援多款主流路由器、記憶體需求僅 2.1 GB
5. **隱私保護**：不使用攝影機，避免影像隱私問題，適合醫療、居家照護場景

## 💬 金句摘錄
> "將這些訊號變化轉換為人體關鍵點座標，再由多目標追蹤器維持每個人的持續身份識別"

> "相較於傳統攝像頭，WiFi 訊號可穿透牆壁運作"

## 🧠 概念連結

- **Channel State Information (CSI)**：WiFi 路由器傳輸過程中的細緻訊號特性，可捕捉環境變化
- **DensePose**：Facebook AI 開發的人體姿態估計技術，原本需要影像輸入
- **多目標追蹤 (Multi-Object Tracking)**：電腦視覺中維持多個物件身份識別的技術
- **邊緣運算 (Edge Computing)**：在路由器端進行即時運算，減少雲端依賴

## 💡 與我的連結

這項技術對於個人 AI 系統基礎設施有重要意義：

1. **隱私優先的監控方案**：可在 ac-mac 或 ac-rpi5 上部署，實現居家照護而不侵犯隱私
2. **跨牆監控能力**：適合多房間的健康監測或長者照護應用
3. **低成本硬體需求**：利用現有 WiFi 路由器，無需額外攝影機投資
4. **整合潛力**：可與現有 Telegram Bot 系統整合，提供即時跌倒警報

## ✅ 行動項目

- [ ] 在 GitHub 上 Star 並研究 WiFi DensePose 專案程式碼
- [ ] 評估 ac-mac 或 ac-rpi5 硬體是否支援 CSI 訊號擷取
- [ ] 研究與現有 TG 監控 Bot 的整合可行性
- [ ] 調查 Tailscale 網路環境下的跨機部署方案
- [ ] 了解所需 WiFi 路由器硬體規格（CSI 支援）

## 📝 我的註解與思考

**技術亮點分析**：
- CSI 訊號處理是關鍵，需要特定 WiFi 晶片支援（Intel 5300、Atheros AR9380 等）
- 準確率 94.2% 已達實用級別，但仍低於視覺方案（通常 >98%），權衡點在隱私保護
- 延遲 45.2ms 對即時應用足夠（人類反應時間約 200-300ms）

**實作考量**：
- 需確認現有路由器是否支援 CSI 輸出（大部分消費級路由器不支援）
- 可能需要刷特定韌體或使用研究級設備
- 2.1 GB 記憶體需求對 ac-rpi5 (8GB) 可行，但需注意多服務競爭

**應用場景思考**：
- **長者照護**：夜間跌倒偵測，不需燈光和攝影機，保護隱私
- **健身追蹤**：在不同房間運動時的姿勢校正
- **安全警報**：偵測異常活動模式而不錄影

**潛在限制**：
- 訊號穿牆後準確度可能下降
- 金屬障礙物、大型家具可能影響訊號
- 多人擁擠場景的辨識挑戰

## 🎬 延伸學習 - YouTube

（建議搜尋關鍵字）：
- "WiFi CSI human pose estimation"
- "WiFi sensing technology"
- "DensePose explained"
- "channel state information applications"

## 🔗 延伸閱讀

- [GitHub - WiFi DensePose](https://github.com/ruvnet/wifi-densepose)
- [DensePose 原始論文](http://densepose.org/)
- [WiFi CSI 技術介紹](https://en.wikipedia.org/wiki/Channel_state_information)
- [隱私保護的感測技術趨勢](https://arxiv.org/search/?query=privacy+preserving+sensing)

## 📚 技術規格摘要

### 效能指標
| 指標 | 數值 |
|------|------|
| 姿態偵測準確率 | 94.2% |
| 跌倒偵測靈敏度 | 96.5% |
| 處理延遲 | < 50ms (平均 45.2ms) |
| 輸出幀率 | 30 FPS |
| 同時追蹤人數 | 最多 10 人 |
| 記憶體需求 | 約 2.1 GB |

### 支援硬體
- Intel WiFi Link 5300
- Atheros AR9380
- 其他支援 CSI 輸出的 WiFi 晶片

### 應用場景設定
- 醫療保健（跌倒警報）
- 健身（動作計算）
- 智慧家居監控
- 安全偵測

## ℹ️ 原文資訊
- **原始輸入**：[查看原始資料](../../raw/2026-03/2026-03-01-085759-url.txt)
- **來源連結**：https://unwire.hk/2026/02/28/wifi-densepose-github-open-source/tech-secure/
- **收錄時間**：2026-03-01 08:57:59
- **GitHub 專案**：https://github.com/ruvnet/wifi-densepose
- **授權方式**：MIT License
