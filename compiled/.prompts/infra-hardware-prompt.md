# 任務：編譯「基礎設施與硬體」知識 Wiki 頁

你是 SecondBrain 知識編譯器。以下是「基礎設施與硬體」主題下的 13 篇筆記摘要。
主題描述：伺服器配置、3090 GPU、Mac Mini、Raspberry Pi、網路架構

## 要求

請根據以下筆記內容，產出一篇結構化的知識 Wiki 頁，格式如下：

```
---
title: "基礎設施與硬體 — 知識 Wiki"
date: 2026-04-22
type: wiki
content_layer: L3
topic: infra-hardware
source_count: 13
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

## 筆記清單（共 13 篇）

### [1/13] Jensen Huang Morgan Stanley TMT 科技大會演講重點
- **filename**: `2026-03-06-jensen-huang-morgan-stanley-tmt`
- **path**: `tech/ai-ml/2026-03-06-jensen-huang-morgan-stanley-tmt.md`
- **date**: 2026-03-06
- **category**: tech/ai-ml
- **tags**: NVIDIA, Jensen Huang, AI Agent, 運算經濟學, 物理AI, GPU, Token經濟

**內容摘要：**

# Jensen Huang Morgan Stanley TMT 科技大會演講重點

## 📊 元資訊
- **難度**：⭐⭐⭐
- **來源類型**：科技大會演講
- **作者**：Jensen Huang (NVIDIA 執行長)
- **筆記時間**：2026-03-06 11:00

## 📌 摘要
NVIDIA 執行長黃仁勳在 Morgan Stanley TMT 科技大會上闡述 AI 產業的三次拐點（生成式 AI → 推理 → Agent），並提出「運算等於營收」的核心觀點。他預測軟體產業將從工具授權轉型為 Token 服務，同時揭示物理 AI 將是下一個十年的前沿領域。

## 🏷️ 標籤分類
- **大分類**：tech
- **小分類**：ai-ml

## 🔑 關鍵要點

### AI 三次拐點
1. **生成式 AI**：ChatGPT 讓 GPT-3 變得易用，開啟 AI 普及化
2. **推理能力**：o1 帶來自我反思和修正能力，運算量增加 1000 倍
3. **AI Agent**：提示詞從「查詢」變成「行動」，Token 消耗量再增 100 萬倍


(...截斷)

---

### [2/13] OpenClaw Agent 省錢實戰：三個玩家的第一線經驗
- **filename**: `2026-03-04-openclaw-agent-實戰經驗`
- **path**: `tech/ai-ml/2026-03-04-openclaw-agent-實戰經驗.md`
- **date**: 2026-03-04
- **category**: tech/ai-ml
- **tags**: OpenClaw, AI Agent, Heartbeat Protocol, OpenHome, SaaS, Mac Mini, Raspberry Pi

**內容摘要：**

# OpenClaw Agent 省錢實戰：三個玩家的第一線經驗

## 📊 元資訊
- **難度**：⭐⭐⭐
- **來源類型**：Podcast 節目整理
- **原節目**：This Week in Startups (TWIST)
- **主持人**：Jason Calacanis、Lon Harris
- **筆記時間**：2026-03-04 14:22

## 📌 摘要
三位 OpenClaw 玩家分享實戰經驗：非工程師用 Mac Mini 比雲端更易上手、Heartbeat Protocol 取代 Agile 站會、OpenHome 把 Agent 帶入智慧音箱、SaaS 定價模式正被 Agent 顛覆。

## 🏷️ 標籤分類
- **大分類**：tech
- **小分類**：ai-ml

## 🔑 關鍵要點

### 1. 本地硬體勝過雲端（給非工程師）
- Jordy Coltman 花了 80 小時和 $800 踩坑後的結論
- Mac Mini 能看到畫面、截圖 debug，體驗遠勝 AWS EC2 + Linux 終端機
- 「看不到在幹嘛」的焦慮感是真實的
(...截斷)

---

### [3/13] AI Agent 正在變成基礎設施：六大發展路線分析
- **filename**: `2026-03-01-ai-agent-infrastructure-trend`
- **path**: `tech/ai-ml/2026-03-01-ai-agent-infrastructure-trend.md`
- **date**: 2026-03-01
- **category**: tech/ai-ml
- **tags**: AI Agent, 基礎設施, Multi-Agent, Coding Agent, Agent OS, 趨勢分析

**內容摘要：**

# AI Agent 正在變成基礎設施：六大發展路線分析

## 📊 元資訊
- **難度**：⭐⭐⭐⭐
- **來源類型**：產業趨勢分析文章
- **作者**：未知（產業觀察者）
- **筆記時間**：2026-03-01 09:22

## 📌 摘要
這篇文章系統性地整理了近期 AI Agent 的發展趨勢，歸納出六條清晰的發展路線。作者認為 Agent 正在從單點功能演進為「工作系統」，最終將成為基礎設施層級的存在。這是一篇非常有價值的產業地圖式分析。

## 🏷️ 標籤分類
- **大分類**：tech
- **小分類**：ai-ml

## 🔑 關鍵要點

### 六大發展路線

1. **瀏覽器與 IDE 成為 Agent 的身體**
   - Google Auto Browse 整合進 Chrome
   - Apple 將 Claude Agent SDK 整合進 Xcode
   - IDE 從編輯器變成「agent-native 開發環境」

2. **Agent 管理平台出現（Agent OS 雛形）**
   - OpenAI Frontier 涵蓋：sha
(...截斷)

---

### [4/13] SHC Phase 6 Compute Plane 測試報告
- **filename**: `2026-01-31-SHC-Phase6-Compute-Plane-測試報告`
- **path**: `tech/2026-01-31-SHC-Phase6-Compute-Plane-測試報告.md`
- **date**: 2026-01-31
- **category**: tech
- **tags**: Super Happy Coder, Phase 6, Compute Plane, 3090, 測試報告

**內容摘要：**

# SHC Phase 6 Compute Plane 測試報告

## 摘要

Phase 6 Compute Plane 測試已完成,**87.5% 通過率 (7/8)**。3090 GPU 所有主要 API 均正常運作,包括 LLM 推理、Embedding、Rerank、Toolchain 和 GPU 監控。

---

## 一、測試概覽

**測試時間**: 2026-01-31 12:45-12:50
**測試環境**: ac-mac → SSH Tunnel (localhost:9000) → ac-3090:9000
**認證方式**: Bearer Token (shc-compute-2026)

| 指標 | 數據 |
|------|------|
| 總測試數 | 8 項 |
| 通過 | 7 項 (87.5%) |
| 失敗 | 1 項 (12.5%) |
| 跳過 | 0 項 |

---

## 二、測試結果詳情

### ✅ 通過測試 (7 項)

#### 1. test_p6_01_gpu_health - GPU 健康檢查
**狀態**: ✅
(...截斷)

---

### [5/13] 3090 vLLM 硬體測試與部署紀錄
- **filename**: `2026-01-30-3090-vLLM-硬體測試與部署紀錄`
- **path**: `tech/2026-01-30-3090-vLLM-硬體測試與部署紀錄.md`
- **date**: 2026-01-30
- **category**: tech
- **tags**: 3090, vLLM, GPU, flash-attn, Qwen2.5, 硬體測試

**內容摘要：**

# 3090 vLLM 硬體測試與部署紀錄

## 摘要
完成 RTX 3090 硬體壓力測試（6/6 通過），安裝 CUDA 12.8 toolkit + flash-attn 2.8.3，成功啟動 vLLM 0.14.1 並完成 Qwen2.5-7B-Instruct 推理測試。

## 系統環境

| 項目 | 規格 |
|------|------|
| GPU | NVIDIA GeForce RTX 3090 (24GB) |
| CPU | AMD Ryzen 9 3900X 12-Core |
| RAM | 32GB |
| OS | Ubuntu 22.04 (Kernel 6.8.0-90-generic) |
| NVIDIA Driver | 590.48.01 |
| CUDA | 13.1 (Driver) / 12.8 (Toolkit) |
| PyTorch | 2.9.1+cu128 |
| vLLM | 0.14.1 |
| flash-attn | 2.8.3 |
| flashinfer | 0.5.3 |
| triton | 3.5.1 
(...截斷)

---

### [6/13] 3090 遠端壓力測試報告（20/30/50 學生）
- **filename**: `2026-01-30-3090-遠端壓力測試報告`
- **path**: `tech/2026-01-30-3090-遠端壓力測試報告.md`
- **date**: 2026-01-30
- **category**: tech
- **tags**: 3090, vLLM, stress-test, Qwen2.5, Compute-Plane

**內容摘要：**

# 3090 遠端壓力測試報告

## 摘要

從 ac-mac 透過 SSH Tunnel 對 3090 上的 vLLM (Qwen2.5-7B-Instruct) 進行遠端壓力測試。分別測試 vLLM 直連 (port 8000) 與 Compute Plane API (port 9000) 兩個端點，模擬 20/30/50 學生同時發送交叉複雜任務。**全部測試 100% 成功，50 人同時並發也在 28 秒內完成。**

## 關鍵要點

- 50 學生同時並發，成功率 100%，無任何超時或錯誤
- vLLM continuous batching 機制極為高效，20→50 人批次總耗時僅增加 4 秒
- Compute Plane proxy 層額外開銷在 5-8% 之間，可忽略
- 網路頻寬完全不是瓶頸（Tailscale 延遲 ~5ms，LLM API 純文字傳輸量極小）
- GPU 推理是唯一瓶頸：排隊越多，個別請求等待時間越長

---

## 1. 測試環境

| 項目 | 規格 |
|------|------|
| **測試端** | ac-mac (Mac
(...截斷)

---

### [7/13] ac-mac 系統死當分析（Tailscale ACL 變更引發）
- **filename**: `2026-01-30-ac-mac-死當分析`
- **path**: `tech/2026-01-30-ac-mac-死當分析.md`
- **date**: 2026-01-30
- **category**: tech
- **tags**: ac-mac, crash, tailscale, snapd, watchdog, 系統維護

**內容摘要：**

# ac-mac 系統死當分析

## 摘要

2026-01-30 約 18:48，ac-mac 發生系統無回應（死當），無法透過 SSH、Tailscale、Telegram Bot 連線。系統未自動重啟，需手動重開機。**根因為 Tailscale ACL 設定變更（重設 ACL + 關閉 macmini2 SSH），導致 Tailscale 網路連線異常**，snapd 因網路相關操作卡住而 CPU 暴衝，最終觸發 watchdog timeout 連鎖凍結系統。

## 關鍵要點

- **根因是 Tailscale ACL 變更**，不是 snapd 本身——snapd 是受害者
- 約 18:48 修改 Tailscale ACL 並關閉 macmini2 SSH 功能，造成網路連線異常
- Tailscale 持續 3 分鐘以上瘋狂重連報錯，應在此階段就介入重啟 Tailscale
- snapd 可能因網路操作（snap store 連線等）被卡住，CPU 暴衝 3m46s 後被 SIGKILL
- 系統未自動重啟，約 20:59 手動重開機恢復
- **需要監控機制
(...截斷)

---

### [8/13] vLLM Qwen2.5-7B-Instruct 在 RTX 3090 部署紀錄
- **filename**: `2026-01-30-vLLM-Qwen-3090-部署紀錄`
- **path**: `tech/2026-01-30-vLLM-Qwen-3090-部署紀錄.md`
- **date**: 2026-01-30
- **category**: tech
- **tags**: vLLM, Qwen, RTX3090, LLM, 部署

**內容摘要：**

# vLLM Qwen2.5-7B-Instruct 在 RTX 3090 部署紀錄

## 摘要

成功在 ac-3090 (RTX 3090 24GB) 上部署 vLLM v0.14.1 運行 Qwen2.5-7B-Instruct 模型。
過程中遇到多個注意力後端相容性問題，最終使用 TRITON_ATTN 後端成功啟動。

## 環境資訊

| 項目 | 版本/規格 |
|------|-----------|
| GPU | NVIDIA RTX 3090 24GB |
| Driver | 590.48.01 |
| CUDA (PyTorch) | 12.8 |
| PyTorch | 2.9.1+cu128 |
| vLLM | 0.14.1 (V1 engine) |
| Triton | 3.5.1 |
| 模型 | Qwen/Qwen2.5-7B-Instruct (~15GB) |

## 排查過程

### 問題：vLLM 啟動後掛起

初始啟動時，vLLM 自動選擇 FLASH_ATTN 後端，但實際上 flash-attn 套件未安裝，
導致模型載入階段無
(...截斷)

---

### [9/13] 全機服務清單
- **filename**: `2026-01-30-全機服務清單`
- **path**: `tech/server-config/2026-01-30-全機服務清單.md`
- **date**: 2026-01-30
- **category**: tech/server-config
- **tags**: 服務清單, ac-mac, ac-3090, acmacmini2, systemd, 架構

**內容摘要：**

# 全機服務清單

## 摘要
三台主機（Mac Mini、Mac Mini 2、3090）的完整服務清單與管理指令，截至 2026-01-30 最新狀態。

---

## 一、主機總覽

| 主機 | 別名 | Tailscale IP | 用途 |
|------|------|-------------|------|
| Mac Mini | ac-mac | 100.116.154.40 | 知識庫管理、TG Bot、監控中心 |
| Mac Mini 2 | acmacmini2 | 100.118.162.26 | Super Happy Coder Proxy |
| 3090 Server | ac-3090 | 100.108.119.78 | GPU 運算（LLM、Embedding、Rerank、OCR） |

---

## 二、3090 Server (ac-3090) 服務

### 硬體規格
- GPU: NVIDIA GeForce RTX 3090 (24GB VRAM)
- CPU: AMD Ryzen 9 3900X 12-Core
- RAM
(...截斷)

---

### [10/13] 3090 Compute Plane 部署與網路連通紀錄
- **filename**: `2026-01-29-3090-Compute-Plane-部署與網路連通紀錄`
- **path**: `tech/2026-01-29-3090-Compute-Plane-部署與網路連通紀錄.md`
- **date**: 2026-01-29
- **category**: tech
- **tags**: 3090, compute-plane, ssh-tunnel, tailscale, networking, super-happy-coder

**內容摘要：**

# 3090 Compute Plane 部署與網路連通紀錄

## 摘要

在 3090 主機 (ac-3090) 上完成 Compute Plane API 部署，包含 LLM (vLLM)、Embedding、
Rerank、OCR、Toolchain 五大服務。因 Tailscale ACL 限制，改用 SSH Tunnel 實現
Mac Mini 2 到 3090 的 port 9000 連通。

---

## 一、3090 已安裝元件

### Phase 1：基礎環境
- FastAPI 0.128.0 + Uvicorn 0.40.0
- Redis Server 6.0.16（systemd 自啟）
- poppler-utils、ImageMagick
- httpx、pydantic、pyyaml

### Phase 2：Embedding + Rerank
- sentence-transformers 5.2.2
- transformers 4.57.6（被 vLLM 降級至此版本）
- faiss-gpu 1.7.2
- 預設 Embedding 模型
(...截斷)

---

### [11/13] 3090 Compute Plane 安裝規劃
- **filename**: `2026-01-29-3090-Compute-Plane-安裝規劃`
- **path**: `tech/2026-01-29-3090-Compute-Plane-安裝規劃.md`
- **date**: 2026-01-29
- **category**: tech
- **tags**: 3090, GPU, compute-plane, super-happy-coder, deployment

**內容摘要：**

# 3090 Compute Plane 安裝規劃

## 摘要

規劃在 RTX 3090 主機 (ac-3090) 上安裝 Super Happy Coder 所需的 Compute Plane 服務。
目標：提供 LLM 推理、Embedding、Rerank、OCR、Toolchain 五大服務，
由 Mac Mini 2 上的 Agent Executor 透過內網 API 呼叫。

---

## 現況評估

### 硬體
| 項目 | 規格 |
|------|------|
| GPU | NVIDIA RTX 3090 24GB VRAM |
| RAM | 32GB |
| 磁碟 | 457GB (394GB 可用) |
| OS | Ubuntu 22.04 LTS |
| NVIDIA Driver | 590.48.01 |
| CUDA (PyTorch) | 12.1 |

### 已安裝
- Python 3 + pip3
- PyTorch 2.5.1+cu121（CUDA 可用）
- Git
- ComfyUI（使用中，佔用約 7GB VRAM）


(...截斷)

---

### [12/13] 工作日誌 - Happy 服務設定與除錯
- **filename**: `2026-01-28-工作日誌`
- **path**: `personal/2026-01-28-工作日誌.md`
- **date**: 2026-01-28
- **category**: 工作日誌
- **tags**: happy, codex, rpi5, mac-mini, tailscale, 系統維護

**內容摘要：**

# 2026-01-28 工作日誌

## 主要任務：各機器 Happy 服務設定與除錯

### 1. RPI5 Happy 服務問題排查

**問題現象**：手機 App 可以正常對話，但權限確認時會卡住無回應

**根本原因**：
- RPI5 的 Linux 核心不支援 Landlock（Linux 安全沙盒功能）
- Codex 執行命令時嘗試使用 Landlock sandbox 失敗
- 錯誤訊息：`error running landlock: Sandbox(LandlockRestrict)`
- Happy 的權限處理流程有 bug，`call_id` 變成 `undefined` 導致卡住

**解決方案**：
修改 Happy 的 Codex 設定，強制使用 `danger-full-access` 模式跳過 Landlock

```bash
# 備份
cp ~/.nvm/versions/node/v20.20.0/lib/node_modules/happy-coder/dist/runCodex-DarzxcRd.mjs \
   ~/.nvm/ver
(...截斷)

---

### [13/13] PaddleOCR-VL-1.5 部署到 ac-3090
- **filename**: `paddleocr-vl-deployment`
- **path**: `work-logs/tasks/paddleocr-vl-deployment.md`
- **date**: 
- **category**: 
- **tags**: (無)

**內容摘要：**

# PaddleOCR-VL-1.5 部署任務

## 目標
在 ac-3090 (RTX 3090) 上部署百度最新發布的 PaddleOCR-VL-1.5 文件視覺語言模型

## 模型資訊

### 基本規格
- **模型大小**: 0.9B 參數
- **架構**: NaViT 動態高解析度視覺編碼器 + ERNIE-4.5-0.3B 語言模型
- **準確率**: OmniDocBench v1.5 達 94.5%，Real5-OmniDocBench 達 92.05%
- **語言支援**: 111 種語言
- **輸出格式**: 結構化 Markdown 與 JSON

### 核心能力
- 文字辨識（OCR）
- 表格解析
- 數學公式辨識
- 圖表分析
- 印章識別
- 文字定位
- 兩階段流程：版面分析（PP-DocLayoutV3）→ 元素識別

### 效能對比
- 推理速度比 MinerU 2.5 快 14%
- 推理速度比 dots.ocr 快 2 倍以上
- 在文件解析任務上不遜於 Qwen3-VL (235B)

### 真實場景支援（Real5-Omn
(...截斷)

---
