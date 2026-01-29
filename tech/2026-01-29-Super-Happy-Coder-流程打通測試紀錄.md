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

## 五、待辦事項

- [ ] vLLM 模型下載完成後啟動測試（Qwen2.5-7B-Instruct，~15GB 下載中）
- [ ] Rerank 端點測試（模型首次載入時自動下載）
- [ ] OCR 端點測試（需要圖片素材）
- [ ] TG Bot 整合（等 Token）
- [ ] 壓力測試（多用戶並發）
