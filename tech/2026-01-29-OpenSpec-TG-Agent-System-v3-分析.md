---
title: OpenSpec TG Agent System v3 版本分析
date: 2026-01-29
category: tech
tags: [agent, architecture, openspec, multi-agent, telegram, 教學系統]
source: /home/ac-mac/agent-projects/openspec_tg_agent_system_v3/
---

# OpenSpec TG Agent System v3 版本分析

## 摘要
v3 從「高層規範」升級到「可實裝的生產級規格」，新增 5 個檔案，核心改進在 Planner-Executor 分離、入口治理管線、容量規劃（20 人教學場景）與安全管控。

## 關鍵要點
- Planner-Executor 明確分離：外部 LLM 只輸出 Plan JSON，不負責執行
- 10-step Ingress Pipeline 規範化入口處理
- 三層佇列架構（interactive / batch / heavy）支援不同優先級
- API 端點從 4 個擴展到 7 個
- 針對 20 人同時上課場景的容量規劃

---

## 一、v3 新增的檔案

| 檔案 | 內容 |
|------|------|
| `specs/35-ingress-pipeline.md` | 10 步入口處理管線規格 |
| `specs/55-capacity-and-concurrency.md` | 20 人教學場景容量規劃 |
| `specs/56-3090-compute-plane-deployment.md` | 3090 部署規格（軟體依賴、服務切分、網路安全） |
| `design/plan-schema.md` | Planner 輸出的 Plan JSON 結構定義 |
| `design/router-policy.md` | Router 決策表（Planner 選擇 + 執行目標分離） |

## 二、主要架構變更

### 舊架構（v1）
```
TG → Mac mini → 3090/外部 API → 執行（線性流程）
```

### v3 架構
```
TG → Mac mini Gateway
  → Ingress Pipeline（10 步）
    → Identify → Session → Command Detect → Rate Limit
    → Cache Check → Module Routing → Planner Decision
    → Plan Validation → Execution → Audit & Reply
  → Multi-tier Queue + Cache
  → 結果回覆
```

### Planner-Executor 分離
- Router Policy 決策表將 Planner 選擇（none / local / external）與執行目標（local / external / tool_only）獨立分離
- Plan JSON 可被 JSON Schema 驗證，支援 dry-run 與 approval workflow
- 外部 LLM 只產出規劃結果，不直接控制執行

### Ingress Pipeline（10 步）
1. Identify（身份識別）
2. Session & Task（會話管理）
3. Command Detect（指令檢測）
4. Rate Limit & Queue（流量控制）
5. Cache Check（快取檢查）
6. Module Routing（模組路由）
7. Planner Decision（Planner 決策）
8. Plan Validation（計畫驗證）
9. Execution（執行）
10. Audit & Reply（稽核與回覆）

## 三、API 變更

| 端點 | v1 | v3 | 用途 |
|-----|-----|-----|------|
| /v1/llm/generate | ❌ | ✅ | 短輸出生成（區別於 tool-call） |
| /v1/llm/tool-call | ✅ | ✅ | 工具呼叫 |
| /v1/embeddings | ✅ | ✅ | RAG 向量化 |
| /v1/rerank | ✅ | ✅ | RAG 重排 |
| /v1/ocr | ✅（同步） | ✅（非同步 Job） | OCR（submit + result） |
| /v1/tools/run | ❌ | ✅ | 工具鏈執行（白名單 + dry-run） |
| /health | ✅ | ✅（更詳細） | 健康檢查 |

### OCR 改為非同步
- `POST /v1/ocr/submit` → 返回 job_id
- `GET /v1/ocr/result/{job_id}` → 查詢進度與結果

### 工具鏈服務 `/v1/tools/run`
- 白名單安全機制
- 支援 dry-run 預覽
- 統一 Error Response 格式

## 四、容量規劃（20 人場景）

### 三層佇列架構
| 佇列 | 用途 | 優先級 |
|------|------|--------|
| interactive_queue | 即時回應 | 高 |
| batch_queue | 批次任務 | 中 |
| heavy_queue | 重型運算（OCR、大模型） | 低 |

### 併發控制
- per-user 限制 + 系統全域限制
- 快取策略：OCR、Embedding、Retrieval 結果快取
- 成功標準：指令回應 <3 秒、20 人同時操作穩定

### 3090 部署規格
- 5 個獨立微服務切分
- 軟體依賴：OS、Driver、Framework、OCR（PaddleOCR）、RAG、Toolchain
- 內網 API 通訊，安全隔離

## 五、TG Bot 指令變更

| 指令 | v1 | v3 |
|------|-----|-----|
| /start | ✅ | ✅ |
| /modules | ✅ | ✅ |
| /run | ✅ | ✅ |
| /status | ✅ | ✅ |
| /mytasks | ✅ | ✅ |
| /help | ✅ | ✅ |
| /cancel | ❌ | ✅（取消進行中任務） |
| /retry | ❌ | ✅（重跑失敗任務） |

## 六、安全性與可觀測性

| 方面 | v1 | v3 |
|-----|-----|-----|
| Tool 執行 | 基本隔離 | 白名單 + dry-run 預設 |
| Plan 驗證 | 信任為主 | JSON Schema 驗證 + risk_level 標記 |
| 併發控制 | 簡單佇列 | 三層佇列 + per-user 限制 |
| 稽核記錄 | 基本 | + router_decision、Plan JSON、approval 流程 |

## 七、對 Super Happy Coder 的潛在整合方向

1. **Plan JSON** → 整合到 Agent Executor 的流程中
2. **Ingress Pipeline** → 加入 proxy.py 的前處理邏輯
3. **三層佇列** → 優化現有的 ThreadPoolExecutor 排程
4. **`/v1/tools/run` 白名單** → 增強工具執行安全性
5. **非同步 OCR** → 支援長時間 OCR 任務

## 原文資訊
- 來源：/home/ac-mac/agent-projects/openspec_tg_agent_system_v3/
- 時間：2026-01-29
- 前版：/home/ac-mac/agent-projects/openspec_tg_agent_system/
