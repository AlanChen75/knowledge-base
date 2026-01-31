---
title: SHC v5 混合編排系統實作紀錄
date: 2026-01-31
category: tech/ai-ml
tags: [SHC, hybrid-orchestrator, dynamic-planner, agent-creator, implementation]
source: 內部開發
---

# SHC v5 混合編排系統實作紀錄

## 背景

SHC v330 使用純靜態 MODULE.yaml 管線，無法處理模組庫中不存在的任務。
本次實作將混合架構整合進系統，結合固定模組的確定性與動態規劃的靈活性。

## 實作摘要

### 新增 3 個核心模組

#### 1. `dynamic_planner.py`（~350 行）
- TodoWrite 式動態任務規劃器
- LLM 生成 3-8 步任務清單
- 逐步執行，失敗時重新規劃（最多 3 次）
- 支援 4 種 action_type：llm, shell, code, validate
- 整合 ProgressEmitter 推送即時進度
- 完整執行日誌供 AgentCreator 分析

#### 2. `agent_creator.py`（~330 行）
- 自動將成功的動態執行轉化為 MODULE.yaml
- 三道品質防線：品質分數 ≥ 0.8、YAML schema 驗證、可選人工審核
- LOW tier LLM 評估可重複性（~200 token）
- HIGH tier LLM 生成 MODULE.yaml（~1500 token）
- `_pending/` 目錄審核機制
- 任務模式統計追蹤（`_pattern_stats.json`）

#### 3. `hybrid_orchestrator.py`（~350 行）
- 三層路由：觸發詞匹配 → 語義匹配 → 動態規劃
- 語義匹配快取（記憶體，TTL 1 小時）
- 統計追蹤：fixed_hits, semantic_hits, dynamic_runs, modules_created
- 整合 AgentExecutor + DynamicPlanner + AgentCreator

### proxy.py 整合方案

`proxy_patch.py` 記錄了所有改動：
1. import HybridOrchestrator
2. 全域初始化（含 ProgressEmitter + FeedbackCollector）
3. SessionManager 新增 `execute_hybrid()` 方法
4. `/api/v1/chat` 新增 `mode=hybrid` 參數
5. 管理 API：`/api/v1/admin/hybrid/*`

**注意**：proxy.py 的改動尚未直接套用，以 `proxy_patch.py` 作為改動說明。
正式啟用前需要人工整合到 proxy.py 中。

### OpenSpec 更新（v4 → v5）

| 檔案 | 操作 | 內容 |
|------|------|------|
| `README.md` | 更新 | 標題改為 v5，加入 v5 變更紀錄 |
| `specs/20-architecture.md` | 追加 | Hybrid Orchestration Layer 架構圖 |
| `specs/80-modules-catalog.md` | 追加 | 模組自動生成機制、_pending/ 目錄 |
| `specs/85-hybrid-orchestration.md` | 新增 | 完整混合編排規格 |
| `tasks/milestone-hybrid.md` | 新增 | 實作 milestone 追蹤 |

## Token 成本分析

| 場景 | Token/次 | 說明 |
|------|---------|------|
| 已知任務（觸發詞） | ~1,000 | 零額外路由成本 |
| 已知任務（語義） | ~1,200 | +200 語義匹配 |
| 已知任務（快取） | ~1,000 | 語義結果已快取 |
| 新任務（動態） | ~6,000 | TodoWrite 完整循環 |
| 新任務（+建模組） | ~9,500 | 動態 + 評估 + 生成 |
| 同類第二次起 | ~1,000 | 模組已建立 |

## 待完成事項

1. **正式整合 proxy.py**：依照 proxy_patch.py 說明修改
2. **Redis 語義快取**：取代記憶體快取
3. **Context 壓縮**：降低動態規劃 token
4. **單元測試**：各組件獨立測試
5. **整合測試**：完整流程端對端測試
6. **Token 監控**：新增使用量儀表板

## 相關檔案（acmacmini2）

```
/home/ac-macmini2/workshop/super-happy-coder/
├── hybrid_orchestrator.py   # 新增：混合編排器
├── dynamic_planner.py       # 新增：動態規劃器
├── agent_creator.py         # 新增：自動模組生成
├── proxy_patch.py           # 新增：proxy.py 改動說明
├── proxy.py                 # 待修改：整合 hybrid mode
├── agent_executor.py        # 不變：固定管線執行器
├── orchestrator.py          # 不變：舊版編排器（保留）
├── skills/
│   ├── _pending/            # 新增：待審核模組目錄
│   └── ...
└── openspec-v4/
    ├── README.md            # 更新：v5
    ├── specs/85-hybrid-orchestration.md  # 新增
    └── tasks/milestone-hybrid.md        # 新增
```

## proxy.py 正式整合（v5.0.0）

### 改動摘要
- 新增 `from hybrid_orchestrator import HybridOrchestrator` import
- 延遲初始化 `get_hybrid_orchestrator()` 避免循環依賴
- SessionManager 新增 `execute_hybrid()` / `_execute_hybrid_task()` 方法
- `/api/v1/chat` 新增 `mode=hybrid` 參數
- 新增 4 個 admin API endpoints:
  - GET `/api/v1/admin/hybrid/stats`
  - GET `/api/v1/admin/hybrid/modules`
  - POST `/api/v1/admin/hybrid/modules/reload`
  - POST `/api/v1/admin/hybrid/modules/<id>/approve`
- 版本號 3.3.0 → 5.0.0

### 驗證結果
- 服務重啟成功，health endpoint 回報 v5.0.0
- hybrid admin APIs 全部回應正常
- 4 個固定模組 (M1/M2/M3/M6) 正常載入
