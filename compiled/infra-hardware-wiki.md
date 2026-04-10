---
title: "基礎設施與硬體 — 知識 Wiki"
date: 2026-04-10
type: wiki
content_layer: L3
topic: infra-hardware
source_count: 13
last_compiled: 2026-04-10
_skip_sync: true
---

# 基礎設施與硬體 — 知識 Wiki

## 主題概述

本主題涵蓋個人 AI 基礎設施的完整硬體架構——以 RTX 3090 GPU 工作站為運算核心，搭配兩台 Mac Mini（2011/2014）與 Raspberry Pi 5 組成的分散式節點網路。這套基礎設施透過 Tailscale VPN 互聯，承載 LLM 推理（vLLM）、Embedding、Rerank、OCR 等 AI 服務，同時支撐教學平台、監控系統與多 Agent 協作框架。

從 2026 年 1 月底的密集部署紀錄可以看出，這套系統經歷了從硬體測試、軟體部署、壓力驗證到生產穩定運行的完整生命週期。過程中累積了大量實戰經驗：注意力後端相容性問題、Tailscale ACL 配置引發的系統死當、SSH Tunnel 繞過網路限制等。這些經驗構成了「小型 AI 基礎設施」的寶貴知識庫。

從產業趨勢來看，本地硬體部署正在成為 AI Agent 時代的重要基礎設施形態。黃仁勳提出的「運算等於營收」觀點，以及 OpenClaw 社群中「本地硬體勝過雲端」的實戰結論，都指向同一方向：擁有可控的 GPU 運算資源，是 AI 應用落地的關鍵競爭力。

## 核心概念

### RTX 3090 GPU 運算節點

3090 工作站（AMD Ryzen 9 3900X + 24GB VRAM）是整套基礎設施的運算心臟。硬體壓力測試 6/6 全通過，成功部署 vLLM 運行 Qwen2.5-7B-Instruct 模型，並在 50 人並發壓力測試中達成 100% 成功率。GPU 推理是唯一真正的瓶頸，網路與 CPU 均非限制因素。[[2026-01-30-3090-vLLM-硬體測試與部署紀錄]] [[2026-01-30-3090-遠端壓力測試報告]]

### vLLM 部署與注意力後端

vLLM v0.14.1 在 RTX 3090 上部署時遭遇注意力後端相容性問題——預設選擇的 FLASH_ATTN 未安裝導致啟動掛起，最終改用 TRITON_ATTN 後端成功運行。這個排查經驗對 consumer-grade GPU 部署 LLM 極具參考價值。關鍵參數：`--max-model-len 4096 --gpu-memory-utilization 0.75 --dtype float16 --enforce-eager`。[[2026-01-30-vLLM-Qwen-3090-部署紀錄]]

### Compute Plane 五大服務架構

Super Happy Coder 的 Compute Plane 在 3090 上提供 LLM 推理、Embedding、Rerank、OCR、Toolchain 五大服務，透過 FastAPI + Uvicorn 對外暴露 API（port 9000）。Phase 6 測試達 87.5% 通過率（7/8），Compute Plane proxy 層額外開銷僅 5-8%。[[2026-01-29-3090-Compute-Plane-安裝規劃]] [[2026-01-31-SHC-Phase6-Compute-Plane-測試報告]]

### Tailscale VPN 與網路拓撲

所有節點透過 Tailscale 組成 VPN 網路（100.x.x.x 網段），ACL 規則控制節點間存取權限。因 acmacmini2 → ac-3090 的 ACL 僅開放 port 9000/8188/3003（無 SSH），改用 SSH Tunnel 實現連通。Tailscale ACL 變更曾引發 ac-mac 系統死當，是高風險操作。[[2026-01-29-3090-Compute-Plane-部署與網路連通紀錄]] [[2026-01-30-ac-mac-死當分析]]

### 多節點服務架構

三台主機各司其職：ac-mac 負責知識庫管理、TG Bot 監控中心；acmacmini2 運行 Super Happy Coder Proxy；ac-3090 專注 GPU 運算。所有服務以 systemd 管理，實現開機自啟與持久化運行。[[2026-01-30-全機服務清單]]

### PaddleOCR-VL 視覺語言模型

百度 PaddleOCR-VL-1.5（0.9B 參數）規劃部署到 ac-3090，支援 111 種語言的文件視覺理解。其推理速度比 MinerU 2.5 快 14%、比 dots.ocr 快 2 倍，在文件解析上不遜於 Qwen3-VL (235B)，是輕量級 OCR 的強力選項。[[paddleocr-vl-deployment]]

### AI Agent 基礎設施化趨勢

AI Agent 正從單點功能演進為基礎設施層級存在，六大路線包括：瀏覽器/IDE 成為 Agent 身體、Agent OS 管理平台、Multi-Agent 協作、Coding Agent 成熟化等。本地硬體在此趨勢中扮演「Agent 的物理載體」角色。[[2026-03-01-ai-agent-infrastructure-trend]]

### 本地硬體 vs 雲端的實戰取捨

OpenClaw 社群實戰表明：非工程師用 Mac Mini 比雲端 EC2 更容易上手，「看得到在幹嘛」大幅降低焦慮感。Heartbeat Protocol 取代 Agile 站會，SaaS 定價模式正被 Agent 經濟顛覆。[[2026-03-04-openclaw-agent-實戰經驗]]

## 關鍵發現

> **50 人並發 100% 成功率**：vLLM 的 continuous batching 機制極為高效，20→50 人批次總耗時僅增加 4 秒，GPU 推理是唯一瓶頸，網路頻寬完全不是問題。——[[2026-01-30-3090-遠端壓力測試報告]]

> **注意力後端踩坑**：vLLM 自動選擇 FLASH_ATTN 但未安裝時不會報錯而是直接掛起，必須手動指定 TRITON_ATTN。consumer-grade GPU 部署 LLM 的必知陷阱。——[[2026-01-30-vLLM-Qwen-3090-部署紀錄]]

> **Tailscale ACL 變更是高風險操作**：修改 ACL 並關閉節點 SSH 功能，觸發 Tailscale 瘋狂重連→snapd 卡住→CPU 暴衝→watchdog timeout 連鎖凍結。根因是網路配置變更，不是 snapd。——[[2026-01-30-ac-mac-死當分析]]

> **運算等於營收**：黃仁勳預測軟體產業從工具授權轉型為 Token 服務，AI Agent 的 Token 消耗量將比推理再增 100 萬倍。擁有運算資源 = 擁有營收引擎。——[[2026-03-06-jensen-huang-morgan-stanley-tmt]]

> **本地硬體對非工程師更友好**：Mac Mini 能看到畫面、截圖 debug，體驗遠勝 AWS EC2 + Linux 終端機。80 小時 $800 踩坑後的結論。——[[2026-03-04-openclaw-agent-實戰經驗]]

> **RPI5 不支援 Landlock 沙盒**：Raspberry Pi 5 的 Linux 核心缺少 Landlock 支援，Codex 執行命令時會失敗。解法是強制使用 `danger-full-access` 模式跳過沙盒。——[[2026-01-28-工作日誌]]

> **PaddleOCR-VL 以 0.9B 參數達到 235B 模型水準**：在文件解析任務上不遜於 Qwen3-VL，推理速度快 2 倍以上，適合部署在有限 GPU 資源上。——[[paddleocr-vl-deployment]]

## 跨筆記關聯

**部署時間線（2026-01-28 → 01-31）**：四天內完成從環境準備到生產就緒的全流程。[[2026-01-28-工作日誌]] 記錄各機器服務除錯 → [[2026-01-29-3090-Compute-Plane-安裝規劃]] 與 [[2026-01-29-3090-Compute-Plane-部署與網路連通紀錄]] 完成規劃與部署 → [[2026-01-30-vLLM-Qwen-3090-部署紀錄]] 和 [[2026-01-30-3090-vLLM-硬體測試與部署紀錄]] 解決 vLLM 問題 → [[2026-01-30-3090-遠端壓力測試報告]] 壓力驗證 → [[2026-01-31-SHC-Phase6-Compute-Plane-測試報告]] 完成 Phase 6 測試。

**網路事故與架構調整**：[[2026-01-30-ac-mac-死當分析]] 揭示 Tailscale ACL 變更風險，直接影響了 [[2026-01-29-3090-Compute-Plane-部署與網路連通紀錄]] 中改用 SSH Tunnel 的決策。ACL 限制是 Compute Plane 網路架構設計的核心約束。

**產業趨勢驗證本地部署**：[[2026-03-06-jensen-huang-morgan-stanley-tmt]] 的「運算等於營收」和 [[2026-03-01-ai-agent-infrastructure-trend]] 的 Agent 基礎設施化趨勢，被 [[2026-03-04-openclaw-agent-實戰經驗]] 的本地硬體實戰所驗證。自建 GPU 節點不只是省錢，更是建立 AI 能力的護城河。

**服務全景與單點深入**：[[2026-01-30-全機服務清單]] 提供三台主機的鳥瞰視圖，而 [[2026-01-30-3090-vLLM-硬體測試與部署紀錄]]、[[2026-01-31-SHC-Phase6-Compute-Plane-測試報告]]、[[paddleocr-vl-deployment]] 則分別深入 LLM、Compute Plane、OCR 三個服務的技術細節。

**RPI5 的定位困境**：[[2026-01-28-工作日誌]] 顯示 RPI5 因 Landlock 限制需要特殊處理，而 [[2026-03-04-openclaw-agent-實戰經驗]] 指出 Mac Mini 對非工程師更友好。RPI5 在 Agent 基礎設施中的角色需要重新定位。

## 待探索方向

- **GPU 記憶體分時共用**：目前 ComfyUI 佔用約 7GB VRAM，與 vLLM 的 GPU memory utilization 0.75 設定存在潛在衝突。需要探索動態 VRAM 分配或服務排程機制。
- **自動化故障恢復**：[[2026-01-30-ac-mac-死當分析]] 指出系統未自動重啟，需要 watchdog 監控與自動恢復機制，特別是 Tailscale 連線異常的自動處理。
- **PaddleOCR-VL 與現有 OCR 服務整合**：[[paddleocr-vl-deployment]] 的部署計畫尚待執行，需評估與 Compute Plane 現有 OCR 服務的整合方式與資源競爭。
- **多 GPU 擴展路徑**：目前僅單張 3090，若 Token 消耗量如黃仁勳預測增長百萬倍，需要規劃第二張 GPU（ac-4090 跨帳號整合？）或混合雲方案。
- **Agent OS 層建設**：[[2026-03-01-ai-agent-infrastructure-trend]] 提到的 Agent 管理平台概念，可從現有的 Super Happy Coder + Compute Plane 架構演進。
- **Tailscale ACL 安全審計與變更 SOP**：ACL 變更已證實是高風險操作，需建立變更前備份、灰度切換、自動回滾的標準流程。
- **RPI5 角色定位**：受限於 Landlock 不支援和運算能力，需重新評估 RPI5 在 Agent 基礎設施中的最佳用途（邊緣監控？IoT 閘道？輕量排程器？）。
