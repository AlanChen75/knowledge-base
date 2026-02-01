---
title: Telegram Bot Output 攔截器模組
date: 2026-02-01
category: tech/devops
tags: [telegram, bot, progress, monitoring, automation]
author: Claude + Alan Chen
---

# Telegram Bot Output 攔截器模組

## 概述

`ClaudeOutputInterceptor` 是一個自動化中介層模組，用於攔截 Claude CLI 的執行過程，並將進度即時推送到 Telegram Bot，同時自動產生可點擊的檔案下載按鈕。

**位置**: `/usr/local/bin/server-monitor/claude_output_interceptor.py`

## 核心功能

### 1. 自動攔截 Claude CLI 事件流
- 攔截 JSON 格式的事件流（`--output-format stream-json`）
- 支援事件類型：
  - `tool_use` - 工具開始執行
  - `tool_result` - 工具執行結果
  - `text` - 文字輸出
  - `error` - 錯誤事件
  - `assistant` - AI 回應

### 2. 自動進度推送
- **時間限流**: 每 4.5 秒更新一次（符合 Telegram 20 msg/min 限制）
- **即時更新**: 編輯同一則訊息，避免訊息洪水
- **工具追蹤**: 顯示最近 5 個工具使用情況
- **狀態圖示**:
  - ✅ 完成
  - ⚠️ 失敗
  - ⏳ 執行中

### 3. 自動檔案按鈕生成
- **偵測範圍**: `/reports/` 和 `/super-happy-tests/` 目錄下的檔案
- **自動轉換**: 檔案路徑 → HTTP URL (Tailscale IP)
- **圖示對應**:
  - 📑 `.pptx` - PowerPoint 簡報
  - 📋 `.md` - Markdown 文件
  - 💾 `.json` - JSON 數據
  - 🌐 `.html` - HTML 網頁
  - 🐍 `.py` - Python 程式碼
  - 📄 其他檔案

### 4. 最終摘要統計
- ⏱️ 總耗時
- 🔧 工具使用次數
- 📝 建立檔案數量
- ✏️ 修改檔案數量
- 📤 已直接發送的檔案數量
- ⚠️ 錯誤/警告數量

### 5. 檔案發送策略

#### 自動檔案發送（< 1MB）
小於 1MB 的檔案會自動透過 `bot.send_document()` 直接發送到 Telegram：
- PPTX、PDF、JSON、MD 等常見檔案
- 顯示檔案大小資訊（KB）
- 用戶可直接在 Telegram 中下載
- 優點：即時、方便、無需額外伺服器

#### HTTP 連結按鈕（>= 1MB）
大於等於 1MB 的檔案使用 Inline Keyboard 按鈕：
- 避免 Telegram API 超時問題
- 透過 Tailscale IP (100.116.154.40:8889) 的 HTTP 伺服器提供下載
- 需確保 HTTP 伺服器運行中：`python3 -m http.server 8889`
- 優點：適合大檔案、不受 Telegram 50MB 限制

## 使用方式

### 方式 A: 自動整合（推薦）

已整合到 Happy Coder 系統，**完全自動運作，無需手動調用**。

```python
# 在 happy_coder.py 的 happy_message_handler 中
interceptor = ClaudeOutputInterceptor(bot=context.bot, chat_id=chat.id)
await interceptor.start_intercept(task_name=f"Claude {session['model']}")

# 進度回調函數會自動發送事件給攔截器
async def progress_handler(event_type, data):
    await interceptor.process_event(event_type, data)
    # ... 其他處理 ...

# 任務完成時自動發送摘要
await interceptor.finish_intercept()
```

### 方式 B: 獨立使用

```python
from claude_output_interceptor import ClaudeOutputInterceptor

interceptor = ClaudeOutputInterceptor()

# 開始攔截
await interceptor.start_intercept("任務名稱")

# 處理事件
await interceptor.process_event("tool_use", {
    "name": "Write",
    "input": {"file_path": "/home/ac-mac/test.txt"}
})

await interceptor.process_event("tool_result", {
    "content": "success"
})

# 完成攔截（發送最終摘要 + 檔案按鈕）
await interceptor.finish_intercept()
```

## 技術實作細節

### 檔案路徑轉換邏輯

```python
# 原始路徑
file_path = "/home/ac-mac/super-happy-tests/reports/demo.pptx"

# 轉換為相對路徑
relative_path = file_path.replace("/home/ac-mac/super-happy-tests/reports/", "")
# → "demo.pptx"

# 組合成 HTTP URL
url = f"http://100.116.154.40:8889/{relative_path}"
# → "http://100.116.154.40:8889/demo.pptx"
```

### 工具參數解析

不同工具有不同的參數提取方式：

| 工具 | 參數 | 顯示格式 |
|------|------|---------|
| Read | file_path | 檔案名稱 |
| Write | file_path | 檔案名稱（加入追蹤清單）|
| Edit | file_path | 檔案名稱（加入追蹤清單）|
| Bash | command | 前 50 字元 |
| WebSearch | query | 搜尋關鍵字（前 30 字元）|

### 進度訊息格式

```
🚀 Claude sonnet
⏱️ 已執行 15 秒

📋 執行步驟:
⏳ Read: config.py
✅ Write: output.txt
⏳ Bash: python3 script.py

📁 已產生/修改 2 個檔案

⏳ 處理中...
```

### 最終摘要格式（含按鈕）

```
✅ Claude sonnet - 完成

⏱️ 總耗時: 23.5 秒
🔧 使用工具: 8 次
📝 建立檔案: 3 個
✏️ 修改檔案: 1 個

👇 點擊下方按鈕查看檔案

[📑 demo.pptx] [📋 README.md] [💾 data.json]
    (可點擊按鈕)
```

## 系統整合架構

```
用戶 (Telegram)
    ↓
TG Monitor Bot (tg-monitor-bot.py)
    ↓
Happy Coder (happy_coder.py)
    ↓
ClaudeOutputInterceptor ←→ ProgressNotifier
    ↓                           ↓
Claude CLI (JSON Stream)    進度更新訊息
    ↓                           ↓
執行完成 → 檔案按鈕 → 用戶 (Telegram)
```

## 配置參數

### HTTP Server Base URL
- **預設**: `http://100.116.154.40:8889`
- **用途**: Tailscale IP，Telegram 不接受 localhost
- **修改位置**: `claude_output_interceptor.py:33`

### 更新間隔
- **預設**: 4.5 秒
- **原因**: Telegram 限制 20 msg/min，保守設定 4.5s
- **修改位置**: `claude_output_interceptor.py:25`

### 檔案偵測目錄
- **預設**: `/reports/` 或 `/super-happy-tests/`
- **原因**: 只顯示報告相關檔案，避免按鈕過多
- **修改位置**: `_create_file_buttons()` 函數

## 注意事項

### 1. Telegram URL 限制
- ❌ 不支援 `localhost`
- ❌ 不支援 `127.0.0.1`
- ✅ 必須使用公開 IP 或 Tailscale IP
- ✅ 必須是有效的 HTTP/HTTPS URL

### 2. HTTP Server 需求
- 必須啟動 HTTP Server: `python3 -m http.server 8889`
- 在 `/home/ac-mac/super-happy-tests/reports/` 目錄下執行
- 或使用其他 Web Server（Nginx、Apache）

### 3. 檔案權限
- 產生的檔案必須可被 HTTP Server 讀取
- 建議權限: `644` (rw-r--r--)

### 4. 訊息長度限制
- 單則訊息不超過 4096 字元
- 工具追蹤只顯示最近 5 個
- 詳細資訊會被截斷（前 50 字元）

## 錯誤處理

### 網路錯誤
- 攔截器不會因為 TG API 錯誤而中斷主要任務
- 使用 `try-except` 包裹所有 TG API 呼叫
- 錯誤記錄到 logger，不影響 Claude CLI 執行

### 訊息編輯失敗
- 訊息內容沒有變化時會拋出異常 → 忽略
- 訊息已被刪除時 → 停止更新
- 訊息 ID 無效時 → 重新發送新訊息

## 測試

### 獨立測試
```bash
python3 /usr/local/bin/server-monitor/claude_output_interceptor.py
```

會模擬一系列事件並發送到 Telegram。

### 整合測試
透過 TG Bot 發送任何會產生檔案的任務：
```
幫我建立一個 test.md 檔案，內容是 Hello World
```

應該會看到：
1. 即時進度更新（每 4-5 秒）
2. 工具使用記錄（Write: test.md）
3. 最終摘要（含 test.md 下載按鈕）

## 相關檔案

- `/usr/local/bin/server-monitor/claude_output_interceptor.py` - 主要模組
- `/usr/local/bin/server-monitor/happy_coder.py` - Happy Coder 整合
- `/usr/local/bin/server-monitor/progress_notifier.py` - 進度通知器（相關但獨立）
- `/usr/local/bin/server-monitor/config.py` - Bot Token 設定

## 版本歷史

- **2026-02-01**: 初版建立，整合到 Happy Coder
  - 自動攔截 Claude CLI 事件
  - 自動產生檔案按鈕
  - 支援 15 種檔案類型圖示

## 下一步改進

- [ ] 支援更多檔案類型圖示
- [ ] 支援檔案大小顯示
- [ ] 支援檔案預覽（圖片、文字）
- [ ] 支援批次下載（ZIP）
- [ ] 支援檔案分類（報告/程式碼/數據）
- [ ] 支援自訂 HTTP Base URL
- [ ] 支援 HTTPS
- [ ] 支援 CDN 加速
