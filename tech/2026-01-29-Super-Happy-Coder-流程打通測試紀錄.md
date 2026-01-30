---
title: Super Happy Coder 流程打通測試紀錄
date: 2026-01-29
category: tech
tags: [super-happy-coder, gemini, compute-plane, agent-executor, integration-test]
source: 工作日誌
---

# Super Happy Coder 流程打通測試紀錄

## 摘要

使用 Gemini CLI 作為後端，完成 Super Happy Coder v2.1.0 全鏈路端到端測試。
測試涵蓋 Chat API、Agent Executor 自動匹配、Compute Plane GPU 服務串接。

---

## 一、測試環境

| 項目 | 設定 |
|------|------|
| Proxy 主機 | Mac Mini 2 (acmacmini2, 192.168.1.103:8081) |
| CLI Backend | Gemini CLI 0.26.0 |
| Compute Plane | 3090 (ac-3090, localhost:9000 via SSH Tunnel) |
| Proxy 版本 | Super Happy Coder v2.1.0 |
| 認證方式 | Google 帳號 (o970117818@gmail.com)，瀏覽器認證 |

---

## 二、測試結果

### 2.1 Chat API 端到端

```bash
curl -X POST http://localhost:8081/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"student_id": "test-user", "prompt": "用繁體中文說你好", "wait": true}'
```

| 項目 | 結果 |
|------|------|
| 狀態 | ✅ 通過 |
| Backend | gemini |
| 回應 | 「你好。」 |
| Skill 匹配 | coding-agent（預設） |
| 用量追蹤 | 正常（quota 扣減） |

### 2.2 Agent Executor 自動匹配

```bash
curl -X POST http://localhost:8081/api/v1/auto \
  -H "Content-Type: application/json" \
  -d '{"student_id": "test-user", "prompt": "寫一個 Python hello world 程式"}'
```

| 項目 | 結果 |
|------|------|
| 狀態 | ✅ 通過 |
| 匹配 Agent | M1 (CLI Agent 控制器) |
| Skill | coding-agent |
| 執行結果 | 建立 `/tmp/super-happy-sessions/test-user/hello.py` |
| 檔案內容 | `print("Hello, World!")` — 已驗證存在 |

### 2.3 Compute Plane — Embedding

```bash
curl -X POST http://localhost:8081/api/v1/compute/embed \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Super Happy Coder 流程測試", "3090 GPU 運算"]}'
```

| 項目 | 結果 |
|------|------|
| 狀態 | ✅ 通過 |
| 模型 | BAAI/bge-base-zh-v1.5 |
| 維度 | 768 |
| 向量數 | 2 |

### 2.4 Compute Plane — GPU 狀態

```bash
curl http://localhost:8081/api/v1/compute/gpu
```

| 項目 | 結果 |
|------|------|
| 狀態 | ✅ 通過 |
| GPU | NVIDIA GeForce RTX 3090 |
| VRAM | 24124 MB (已用 399 MB) |
| 溫度 | 41°C |
| 功耗 | 17.52W |

### 2.5 Compute Plane — Toolchain

```bash
curl -X POST http://localhost:8081/api/v1/compute/tools \
  -H "Content-Type: application/json" \
  -d '{"tool": "lint", "language": "python", "code": "def hello():\n    print(\"hello\")\n"}'
```

| 項目 | 結果 |
|------|------|
| 狀態 | ✅ 通過 |
| 工具 | ruff lint |
| Exit Code | 0 |
| 輸出 | All checks passed! |

### 2.6 Health 整合檢查

```bash
curl http://localhost:8081/health
```

| 項目 | 結果 |
|------|------|
| 狀態 | ✅ 通過 |
| 版本 | 2.1.0 |
| Backend | gemini |
| Skills | 5 個已載入 |
| Agents | 3 個（M1 CLI、M2 Web Deploy、M3 RAG） |
| Compute Plane | ok (RTX 3090, 5 services) |

---

## 三、已載入的 Agent 定義

| ID | 名稱 | 步驟數 | 觸發詞 |
|----|------|--------|--------|
| M1 | CLI Agent 控制器 | 5 | 程式、寫程式、code、coding、開發、debug |
| M2 | 網站生成與部署 | 6 | 部署、deploy、網站、建立網站 |
| M3 | RAG 知識庫問答 | 8 | rag、知識庫、問答、查詢文件、embedding |

---

## 四、Gemini CLI 設定備忘

### 認證方式
- 在 Mac Mini 2 上透過 AnyDesk 登入
- 執行 `gemini` 觸發瀏覽器認證
- Google 帳號：o970117818@gmail.com
- 認證資訊存放：`~/.gemini/google_accounts.json`

### stream-json 輸出格式
```json
{"type":"init","session_id":"...","model":"auto-gemini-2.5"}
{"type":"message","role":"user","content":"..."}
{"type":"message","role":"assistant","content":"...","delta":true}
{"type":"result","status":"success","stats":{"total_tokens":...}}
```

### proxy.py 中的 Gemini CLI 命令
```python
cmd = ['gemini', '-p', enhanced_prompt, '-o', 'stream-json', '-y']
```

---

## 五、Qwen2.5-7B vLLM 部署

### 5.1 模型下載與自動化測試

**下載狀態：** 進行中（已續傳，支援自動恢復）

| 項目 | 說明 |
|------|------|
| 模型 | Qwen/Qwen2.5-7B-Instruct |
| 預估大小 | 13 GB |
| 當前進度 | ~42% (5.47 GB) |
| 下載方式 | HuggingFace Hub（自動續傳） |
| 監控腳本 | `/tmp/monitor_qwen_download.sh` (ac-3090) |
| 日誌檔案 | `/tmp/qwen-monitor.log` (ac-3090) |

**自動化流程：**
1. 背景下載 Qwen2.5-7B 模型（PID 65596）
2. 監控腳本每分鐘檢查進度（PID 自動）
3. 下載完成後自動啟動 vLLM 服務
4. 自動執行 3 項測試：
   - 健康檢查
   - 模型列表驗證
   - 文字生成測試（繁體中文五言絕句）

**查看狀態：**
```bash
# 本地快速檢查
/tmp/check_qwen_status.sh

# 查看即時日誌
ssh ac-3090 "tail -f /tmp/qwen-monitor.log"

# 檢查下載進程
ssh ac-3090 "ps aux | grep 'huggingface.*Qwen'"

# 檢查檔案大小
ssh ac-3090 "du -sh ~/.cache/huggingface/models--Qwen--Qwen2.5-7B-Instruct"
```

### 5.2 vLLM 服務配置

**啟動參數：**
```bash
python3 -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-7B-Instruct \
  --host 127.0.0.1 \
  --port 8000 \
  --max-model-len 4096 \
  --gpu-memory-utilization 0.9
```

**API 端點：**
- 健康檢查: `http://127.0.0.1:8000/health`
- 模型列表: `http://127.0.0.1:8000/v1/models`
- 文字生成: `http://127.0.0.1:8000/v1/completions`
- Chat 補全: `http://127.0.0.1:8000/v1/chat/completions`

---

## 六、待辦事項

- [x] vLLM 模型下載（Qwen2.5-7B-Instruct，15GB 完成）
- [x] vLLM 測試結果驗證 → 5/5 通過（中文/英文/程式碼生成）
- [x] 整合 vLLM 到 Compute Plane API → systemd 服務 `vllm.service` 開機自啟
- [x] Rerank 端點測試 → 通過（bge-reranker-v2-m3，排序正確）
- [x] Embedding 端點測試 → 通過（bge-base-zh-v1.5，768 維）
- [ ] OCR 端點測試 → `use_gpu` 參數不相容，待修
- [ ] CLI Backend 切換到 Claude 後的完整端到端測試
- [ ] 壓力測試（多用戶並發）

> 完整服務清單見：`tech/server-config/2026-01-30-全機服務清單.md`
