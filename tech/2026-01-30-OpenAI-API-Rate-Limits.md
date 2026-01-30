---
title: OpenAI API Rate Limits - SHC v3.1 專用
date: 2026-01-30
category: tech
tags: [openai, api, rate-limit, super-happy-coder, gpt-4.1-nano]
source: https://platform.openai.com/docs/guides/rate-limits
---

# OpenAI API Rate Limits - Super Happy Coder 專案

## 帳號資訊

- **Organization**: user-r5dgaynl1bjjmpgwwdgcimy4
- **Project**: proj_P9JWjaezzj2TtN9L2H2JAjbs
- **用途**: Super Happy Coder v3.1 LLM fallback（替代 3090 vLLM）

## 使用模型

**GPT-4.1 nano** (`gpt-4.1-nano-2025-04-14`)

### 定價

| 類型 | 價格 |
|------|------|
| Input | $0.20 / M tokens |
| Cached Input | $0.05 / M tokens |
| Output | $0.80 / M tokens |

### Rate Limits（實測值）

| 項目 | 限制 |
|------|------|
| Requests per minute | **5,000 RPM** |
| Tokens per minute | **2,000,000 TPM** |

### Response Headers

每次 API 回應都包含以下 header：

| Header | 說明 | 範例值 |
|--------|------|--------|
| `x-ratelimit-limit-requests` | 每分鐘最大請求數 | 5000 |
| `x-ratelimit-limit-tokens` | 每分鐘最大 token 數 | 2000000 |
| `x-ratelimit-remaining-requests` | 剩餘可用請求數 | 4999 |
| `x-ratelimit-remaining-tokens` | 剩餘可用 token 數 | 1999996 |
| `x-ratelimit-reset-requests` | 請求限制重置時間 | 12ms |
| `x-ratelimit-reset-tokens` | Token 限制重置時間 | 0s |

## 成本估算

假設每天 200 次內部 LLM 呼叫，平均 500 token in / 300 token out：

```
Daily: (200 × 500 × $0.20 + 200 × 300 × $0.80) / 1,000,000
     = ($20 + $48) / 1,000,000
     = $0.068/天
Monthly: ≈ $2/月
```

## 系統整合方式

```
呼叫路徑：
proxy.py → compute_client.llm_generate()
  ├── 嘗試 3090 vLLM (localhost:9000 → 8000)
  ├── 失敗 → fallback 到 OpenAI (gpt-4.1-nano)
  └── openai_llm.py → OpenAI Chat Completions API
```

### 設定位置

- **API Key**: `macmini2:~/workshop/super-happy-coder/.env`
- **模型設定**: `OPENAI_MODEL=gpt-4.1-nano`

### 注意事項

- API Key 存在 `.env` 中，`.gitignore` 應排除此檔案
- 當 3090 vLLM 啟動後，系統會優先使用本地 LLM（免費）
- OpenAI 只作為 fallback，不是主要路徑
- `load_dotenv()` 必須在 `import openai_llm` 之前執行

## Fine-tuning Rate Limits 查詢

```bash
curl https://api.openai.com/v1/fine_tuning/model_limits \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

## 錯誤處理

API 錯誤時 HTTP status code 對照：

| Code | 說明 | 處理方式 |
|------|------|----------|
| 429 | Rate limit exceeded | 等待 `x-ratelimit-reset-*` 後重試 |
| 401 | Invalid API key | 檢查 `.env` 中的 key |
| 500 | OpenAI 內部錯誤 | 重試 1 次 |
| 503 | Service unavailable | 等待後重試 |
