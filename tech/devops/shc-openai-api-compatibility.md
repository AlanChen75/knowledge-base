---
title: SHC 對 OpenAI API 不同版本模型的相容性問題
date: 2026-02-02
category: tech/devops
tags: [SHC, OpenAI, API, GPT-5, 相容性]
---

# SHC 對 OpenAI API 不同版本模型的相容性問題

## 問題摘要

SHC (Super Happy Coder) 可以正常使用 GPT-4.1-nano，但無法使用 GPT-5 mini，原因是 OpenAI 在 GPT-5 系列變更了 API 參數規格，而 SHC 程式碼使用舊版參數。

## 關鍵發現

### OpenAI API 參數演變

| 特性 | GPT-4 系列 (含 4.1-nano) | GPT-5 系列 (含 5-mini) |
|------|------------------------|---------------------|
| **Token 限制參數** | `max_tokens` ✅ | `max_completion_tokens` ✅<br>`max_tokens` ❌ |
| **Temperature 範圍** | 0.0-2.0 可調整 | 固定 1.0（不可設定） |
| **向下相容** | 支援舊參數 | 不支援舊參數 |

### 錯誤訊息

當使用 `max_tokens` 參數呼叫 GPT-5 mini 時：

```
HTTP 400 Bad Request
Unsupported parameter: 'max_tokens' is not supported with this model.
Use 'max_completion_tokens' instead.
```

## 根本原因

### SHC 程式碼問題位置

**檔案**: `~/workshop/super-happy-coder/llm_router.py`
**類別**: `OpenAIAdapter.chat()`
**問題行數**: 約 45 行

```python
def chat(self, messages, max_tokens=0, temperature=0.0, model=""):
    use_model = model or self.config.model
    use_max = max_tokens or self.config.max_tokens
    use_temp = temperature if temperature > 0 else self.config.temperature

    try:
        with httpx.Client(timeout=self.config.timeout) as client:
            resp = client.post(
                f'{self.config.base_url}/chat/completions',
                headers=self._headers(),
                json={
                    "model": use_model,
                    "messages": messages,
                    "max_tokens": use_max,      # ❌ GPT-5 不支援
                    "temperature": use_temp,     # ❌ GPT-5 固定為 1.0
                }
            )
```

**問題**：
1. 寫死使用 `max_tokens` 參數
2. 寫死設定 `temperature` 參數
3. 沒有根據模型版本動態調整參數

## 解決方案

### 方案：修改 SHC 程式碼支援新舊 API

需要修改 `llm_router.py` 的 `OpenAIAdapter.chat()` 方法，根據模型名稱動態選擇參數：

```python
def chat(self, messages, max_tokens=0, temperature=0.0, model=""):
    use_model = model or self.config.model
    use_max = max_tokens or self.config.max_tokens
    use_temp = temperature if temperature > 0 else self.config.temperature

    # 根據模型選擇 API 參數格式
    if use_model.startswith('gpt-5'):
        # GPT-5 系列使用新參數
        payload = {
            "model": use_model,
            "messages": messages,
            "max_completion_tokens": use_max,  # 新參數名稱
            # temperature 不設定（GPT-5 固定 1.0）
        }
    else:
        # GPT-4 及更早版本使用舊參數
        payload = {
            "model": use_model,
            "messages": messages,
            "max_tokens": use_max,
            "temperature": use_temp,
        }

    try:
        with httpx.Client(timeout=self.config.timeout) as client:
            resp = client.post(
                f'{self.config.base_url}/chat/completions',
                headers=self._headers(),
                json=payload
            )
            # ... 後續處理相同
```

### 修改影響範圍

- **向下相容**：不影響現有 GPT-4.x 模型的使用
- **向上支援**：新增 GPT-5 系列模型支援
- **風險**：低（僅修改參數組裝邏輯，不改變核心流程）

## 實際測試結果

### GPT-4.1-nano (via SHC)
- ✅ 可正常呼叫
- Token 輸出：約 819 tokens
- 生成頁數：7.1 頁平均
- 成本：$0.014/簡報

### GPT-4o-mini (直接 API)
- ✅ 可正常呼叫（JSON mode）
- Token 輸出：約 2500+ tokens
- 生成頁數：23.3 頁平均
- 成本：$0.002/簡報

### GPT-5 mini (via SHC - 修改前)
- ❌ 失敗：`Unsupported parameter: 'max_tokens'`
- 無法測試

### GPT-5 mini (直接 API - 修改前)
- ⚠️ 測試中遇到其他問題（空回應）

## 相關檔案

- SHC 路由器：`acmacmini2:~/workshop/super-happy-coder/llm_router.py`
- SHC 設定檔：`acmacmini2:~/workshop/super-happy-coder/.env`
- SHC 服務：`acmacmini2 systemd: super-happy-coder.service`

## 後續發現：GPT-5 mini 的 Reasoning Tokens 問題

### 問題描述

修改參數後，GPT-5 mini API 呼叫成功，但回應 `content` 欄位為空字串：
```
[OpenAI] gpt-5-mini: 12143 prompt + 4096 completion tokens
Content: ''  (空字串)
Reasoning tokens: 4096/4096
```

### 根本原因

**GPT-5 mini 的 reasoning tokens 會耗盡 `max_completion_tokens` 配額**，導致沒有剩餘 tokens 用於實際內容生成。

這是 GPT-5 系列的已知行為模式（非 bug）：
- GPT-5 會先進行內部推理（產生 reasoning tokens）
- 推理過程消耗大量 tokens
- 當 `max_completion_tokens` 不足時，推理就耗盡配額
- 結果：`finish_reason: length`，但 `content` 為空

### 解決方案

**新增 `reasoning_effort` 參數**控制推理強度：

```python
if use_model.startswith('gpt-5'):
    payload = {
        "model": use_model,
        "messages": messages,
        "max_completion_tokens": use_max,
        "reasoning_effort": "low",  # 關鍵參數！
    }
```

### 測試結果

| 配置 | Content | Reasoning Tokens | 結果 |
|------|---------|------------------|------|
| 200 tokens, 無 reasoning_effort | 0 chars | 200 | ❌ |
| 500 tokens, 無 reasoning_effort | 186 chars | 192 | ✅ 但推理佔 38% |
| **500 tokens, reasoning_effort=low** | **279 chars** | **64** | ✅ **最佳**（推理僅 13%） |

### SHC 實際運作確認

```
[OpenAI] gpt-5-mini: 2016 prompt + 51 completion tokens
Response: 機器學習是讓電腦從資料中自動學習模式與規則，進而預測或決策，無需明確程式化每個步驟。
```

✅ 成功！GPT-5 mini 現在能正常輸出內容。

## 後續行動

1. ✅ 記錄問題到知識庫
2. ✅ 修改 SHC 程式碼支援 GPT-5 API（參數 + reasoning_effort）
3. ✅ 測試修改後能否正常呼叫 GPT-5 mini
4. ✅ 重啟 SHC 服務並驗證
5. ⏳ 使用 SHC Proxy 生成測試簡報進行品質測試

## 參考資料

- OpenAI API 文件：https://platform.openai.com/docs/api-reference/chat
- GPT-5 mini 定價：$0.250/1M input, $2.000/1M output tokens
- **GPT-5 empty content 問題**：
  - https://github.com/openai/openai-python/issues/2546
  - https://community.openai.com/t/how-to-get-reasoning-summary-using-gpt-5-mini-in-agent-sdk/1358227
  - https://learn.microsoft.com/en-us/answers/questions/5590694/ai-foundry-model-gpt-5-nano-returns-empty-response
