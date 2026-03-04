---
title: World Monitor - 開源全球情報儀表板
date: 2026-03-04
source: https://github.com/koala73/worldmonitor
category: tech/tools
tags: [開源專案, 情報儀表板, 地緣政治, AI, 即時監控, 數據視覺化]
type: tool
raw_file: ../../raw/2026-03/2026-03-04-172809-text.txt
difficulty: ⭐⭐⭐
author: koala73
---

# World Monitor - 開源全球情報儀表板

## 📊 元資訊
- **難度**：⭐⭐⭐
- **來源類型**：開源專案
- **作者**：koala73
- **授權**：MIT License
- **筆記時間**：2026-03-04 17:28
- **最新版本**：v2.5.21 (2026-03-01)

## 📌 摘要
World Monitor 是一個即時的全球情報儀表板，整合 AI 驅動的新聞彙整、地緣政治監控、基礎設施追蹤於統一的態勢感知介面中。提供三大分類：世界、科技、金融，並且完全開源，支援本地 LLM、多語言介面，讓每個人都能擁有個人版的「全球情資指揮中心」。

## 🏷️ 標籤分類
- **大分類**：tech
- **小分類**：tools
- **關鍵字**：開源、情報儀表板、地緣政治、即時監控、AI 摘要、3D 地球儀

## 🔑 關鍵要點

### 1. AI 與本地處理能力
- **四層式 LLM 回退機制**：Ollama (本地) → Groq (雲端) → OpenRouter (雲端) → 瀏覽器端 T5 模型
- 支援 **Ollama 和 LM Studio**，AI 摘要完全在本地硬體執行，無需 API 金鑰，資料不外流
- 客戶端 RAG 系統使用 ONNX 模型進行語意搜尋，資料儲存於 IndexedDB

### 2. 數據涵蓋範圍
- **170+ RSS 新聞源**：涵蓋地緣政治、國防、能源、科技、金融
- **40+ 資料圖層**：
  - 軍事：衝突區域、軍事基地、核設施
  - 基礎建設：海底電纜、管線、資料中心
  - 災害：衛星火災偵測、天然災害、抗議活動
- **18+ 即時新聞頻道**：Sky News、Euronews、DW、France24 等，使用原生 HLS 串流

### 3. 多語言與區域監控
- **19 種語言介面**：英、法、西、德、義、波蘭、葡、荷、瑞典、俄、阿拉伯、中、日、土耳其、泰、越南、捷克、希臘、韓
- **專屬區域監控面板**：非洲、拉丁美洲、中東、亞洲，整合在地新聞來源

### 4. 開源與自訂性
- **MIT License**：完全開源，任何人都可 fork 並客製化
- 可串接其他 AI 模型、新增自訂資料來源
- 支援 PWA、桌面版，可離線使用

## 💬 金句摘錄
> "一個人在那邊把全球衝突／天然災害、軍事動態、航班、船舶、股票、加密貨幣、央行政策、各國風險指數、關鍵基礎建設通通塞進同一個 3D 地球儀裡，還支援本機 LLM、RAG、桌面版、PWA，整個就是個人版「全球情資指揮中心」。"
> — 社群評論

## 🧠 概念連結
- **情報儀表板**：類似軍事/政府情資中心的介面，但開源且免費
- **態勢感知（Situational Awareness）**：即時掌握全球動態的能力
- **RAG（Retrieval-Augmented Generation）**：結合檢索與生成的 AI 技術
- **本地 LLM**：隱私優先，資料不外流的 AI 部署方式

## 💡 與我的連結

### 1. 整合到個人 AI 系統
- **可部署在 ac-mac 或 ac-3090 上**，使用本地 Ollama 進行 AI 摘要
- 與現有的 Telegram Bot 整合，定期推送全球重大事件摘要
- 結合知識庫系統，自動將重要新聞分類存檔

### 2. 地緣政治與技術趨勢追蹤
- 作為每日晨間資訊來源，快速掌握全球動態
- 監控科技產業動態（資料中心、基礎建設）
- 追蹤 AI/ML 相關新聞與政策變化

### 3. 開源專案學習
- 研究其資料彙整架構（170+ RSS 源如何管理）
- 學習 AI 回退機制的設計模式
- 參考其多語言實作方式

## ✅ 行動項目
- [ ] 訪問線上 Demo：worldmonitor.app 體驗功能
- [ ] Fork GitHub 專案：https://github.com/koala73/worldmonitor
- [ ] 研究技術架構：閱讀 docs/DOCUMENTATION.md
- [ ] 評估本地部署：在 ac-mac 上使用 Docker 部署
- [ ] 整合 Ollama：串接現有的本地 LLM 環境
- [ ] 客製化新聞源：新增關注的 RSS 來源
- [ ] 定期摘要推送：撰寫腳本定期抓取摘要並推送到 Telegram

## 📝 我的註解與思考

### 技術亮點
1. **四層式 LLM 回退**：這個設計模式很值得學習，確保服務可用性的同時優先使用本地資源
2. **客戶端 RAG**：使用 ONNX + IndexedDB 在瀏覽器端實作，完全不依賴後端
3. **PWA + 桌面版**：提供多種部署選項，適合不同使用情境

### 應用場景
- **每日晨間簡報**：快速掌握全球重大事件
- **投資決策參考**：監控地緣政治風險、市場動態
- **技術趨勢追蹤**：關注資料中心、基礎建設、AI 政策

### 潛在改進
- 可新增「自訂關注清單」功能，過濾特定國家/主題
- 整合更多亞洲新聞源（目前以歐美為主）
- 新增歷史事件時間軸，方便回顧脈絡

## 🎬 延伸學習 - YouTube
- [搜尋：World Monitor 開源專案介紹](https://www.youtube.com/results?search_query=World+Monitor+open+source+dashboard)
- [搜尋：Ollama 本地 LLM 部署教學](https://www.youtube.com/results?search_query=Ollama+local+LLM+deployment)

## 🔗 延伸閱讀
- [World Monitor GitHub Repository](https://github.com/koala73/worldmonitor)
- [World Monitor Documentation](https://github.com/koala73/worldmonitor/blob/main/docs/DOCUMENTATION.md)
- [Medium: Geopolitical Intelligence For Everyone](https://medium.com/@william.couturier/world-monitor-geopolitical-intelligence-for-everyone-3637d3240616)
- [Threads 社群討論](https://www.threads.com/@cyh.289/post/DVX0iHHk_EP)

## 🌐 線上資源
- **主站**：https://worldmonitor.app
- **技術版**：https://tech.worldmonitor.app
- **GitHub**：https://github.com/koala73/worldmonitor
- **最新版本**：v2.5.21 (2026-03-01)

## ℹ️ 原文資訊
- **原始輸入**：[查看原始資料](../../raw/2026-03/2026-03-04-172809-text.txt)
- **來源**：Telegram 使用者分享
- **收錄時間**：2026-03-04 17:28:09
- **觸發原因**：美國與伊朗戰事新聞，想到這個即時情報工具
