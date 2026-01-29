---
title: Super Happy Coder TG Bot 部署紀錄
date: 2026-01-29
category: tech
tags: [super-happy-coder, telegram-bot, token-quota, user-management]
source: 工作日誌
---

# Super Happy Coder TG Bot 部署紀錄

## 摘要

建立雙 Bot 架構的 Telegram 介面，整合 Token 配額控制與管理後台。
學員透過 @SupperHappyCoder_bot 使用 AI 助手，管理者透過 @SupperHappyAdmin_bot 監控系統。

---

## 一、Bot 架構

### 1.1 雙 Bot 設計

| Bot | 用途 | Token |
|-----|------|-------|
| @SupperHappyCoder_bot | 學員使用 | `8307879072:AAF6USUWoLUraAcENIpz7D4crFIlfkcKeyk` |
| @SupperHappyAdmin_bot | 管理後台 | `8582272061:AAGkHMyeiUZ1WwdgyM8UajD7W-i0H6Hcy1w` |

**架構流程：**
```
TG Bot → Proxy API (localhost:8081) → CLI Backend / Compute Plane
```

### 1.2 服務配置

- **主機：** Mac Mini 2 (acmacmini2)
- **檔案位置：** `/home/ac-macmini2/workshop/super-happy-coder/tg_bot.py`
- **systemd 服務：** `super-happy-tgbot.service`
- **狀態：** enabled, running

---

## 二、Token 配額管理

### 2.1 配額策略

| 項目 | 設定 |
|------|------|
| 每日上限 | 50,000 tokens |
| Token 估算 | `len(text) // 4` |
| 80% 提醒 | 40,000 tokens（單次提醒） |
| 100% 暫停 | 達上限後暫停 4 小時 |
| 跨日重置 | 自動重置（00:00） |

**Token 用量估算：**
- 簡單問答（~250 tokens）：200 次
- 中等程式（~600 tokens）：83 次
- 完整任務（~2200 tokens）：22 次
- 大型任務（~5300 tokens）：9 次
- Debug（~3500 tokens）：14 次

### 2.2 配額控制機制

**資料來源：**
- **Proxy Redis** — 真實 token 統計（`record_usage()` 記錄 input/output tokens）
- **TG Bot 本地 JSON** — 暫停狀態、提醒旗標（`data/quota.json`）

**控制流程：**
1. 使用前：檢查本地暫停狀態 + proxy 配額剩餘
2. 使用後：記錄 tokens（proxy）+ 處理提醒/暫停（TG Bot）
3. 80% 警告：單次推送，本地記錄 `notified_80`
4. 100% 暫停：設定 `suspended_until`（4 小時後）

---

## 三、學員 Bot 指令

### 3.1 基本指令

| 指令 | 功能 |
|------|------|
| `/start` | 歡迎訊息與指令列表 |
| `/help` | 使用說明 |
| `？` or `?` | 快速引導 |

### 3.2 用量查詢

**`/usage` — 今日用量**
```
今日用量：
• 狀態：✅ 正常
• Input Tokens：1.2K
• Output Tokens：3.5K
• 總 Tokens：4.7K / 50.0K
• 剩餘：45.3K tokens
• 使用率：9.4%
• 請求次數：8
```

**`/status` — Session 狀態**
- 顯示：狀態、請求數、技能、最後活動時間

**`/history` — 最近 5 筆對話**

### 3.3 其他功能

- `/clear` — 清除對話歷史
- `/skills` — 列出可用技能
- `/agents` — 列出可用 Agent
- 一般訊息 → 呼叫 `/api/v1/chat`

---

## 四、管理者 Bot 指令

### 4.1 系統監控

**`/check` — 系統儀表板**
```
📊 系統儀表板 — 01/29 19:56

🟢 系統狀態：ok  v2.1.0
🖥️ Backend：gemini
👥 在線 Session：2

📈 今日統計：
• 使用人數：3
• 總請求數：15
• Input Token：5.2K
• Output Token：12.8K
• 總 Token：18.0K
• 最高用量：test-user（8.5K tokens）

🚦 配額警示：
• ⚠️ 接近上限：1 人

🎮 GPU（NVIDIA GeForce RTX 3090）：
• VRAM：399/24124 MB（1%）
• 溫度：41°C  功耗：17.5W  使用率：0%
• 服務：embedding, rerank, ocr, toolchain, llm
```

**`/health` — 系統健康檢查**
- 版本、Backend、Compute Plane、Skills、Agents

**`/gpu` — GPU 狀態**
- VRAM、溫度、功耗、使用率

### 4.2 用戶管理

**`/quota` — 用戶 Token 配額狀態**
```
📊 用戶 Token 配額狀態：

• test-user: 18.0K/50.0K (36%) 15次
• tg-123456: 42.1K/50.0K (84%) 28次 ⚠️
• tg-789012: 50.0K/50.0K (100%) 35次 🚫已達上限
```

**`/reset <user_id>` — 解除用戶暫停**
- 重置本地暫停狀態
- Token 配額需在 Redis 手動清除

**`/remove <user_id>` — 移除用戶**
- 刪除本地暫停記錄

**`/sessions` — 活躍 Session**

**`/allusage` — 所有用戶今日用量**

**`/feedbacks` — 最近回饋記錄**

### 4.3 系統操作

**`/agents` — Agent 列表與版本**

**`/reload` — 熱重載 Agent 定義**

---

## 五、技術實作

### 5.1 QuotaManager 類別

**職責分工：**
- **Proxy Redis** — Token 統計（input/output/total/request_count）
- **TG Bot 本地** — 暫停控制、提醒旗標

**關鍵方法：**
```python
def check_suspended(user_id) -> dict
    # 檢查本地暫停狀態
    # 回傳：suspended, suspended_until

def process_quota_status(user_id, quota_info) -> dict
    # 根據 proxy quota 處理提醒與暫停
    # 輸入：{used, limit, remaining, percent}
    # 回傳：{notify_80, suspended, suspended_until}
```

### 5.2 配額檢查流程

**發送訊息前：**
1. `check_suspended()` — 本地暫停檢查
2. 若暫停 → 推送暫停通知，拒絕請求
3. 查詢 proxy `/api/v1/usage/<student_id>`
4. 若 `remaining <= 0` → 觸發暫停，拒絕請求

**發送訊息後：**
1. Proxy 自動記錄 tokens（`record_usage()`）
2. 取得更新後的 `quota` 資訊
3. `process_quota_status()` 處理提醒/暫停
4. 推送 80% 提醒（單次）
5. 推送 100% 暫停通知（4 小時）

### 5.3 資料存儲

**Proxy Redis：**
```
usage:{student_id}:{date}:
  - input_tokens
  - output_tokens
  - total_tokens
  - request_count
  - last_request_at
```

**TG Bot 本地 JSON：**
```json
{
  "users": {
    "tg-123456": {
      "date": "2026-01-29",
      "suspended_until": "2026-01-29T23:30:00",
      "notified_80": true
    }
  }
}
```

### 5.4 儀表板實作

**並行查詢（asyncio.gather）：**
```python
health_data, usage_data, gpu_data = await asyncio.gather(
    proxy_request("GET", "/health"),
    proxy_request("GET", "/api/v1/all-usage"),
    proxy_request("GET", "/api/v1/compute/gpu"),
)
```

**統計彙整：**
- 遍歷所有 students，累計 input/output tokens
- 計算 suspended_count、warning_count（80%+）
- 找出最高用量用戶

---

## 六、systemd 服務

### 6.1 服務定義

**檔案：** `/etc/systemd/system/super-happy-tgbot.service`

```ini
[Unit]
Description=Super Happy Coder TG Bot (學員 + 管理者)
After=network-online.target super-happy-coder.service
Wants=network-online.target

[Service]
Type=simple
User=ac-macmini2
WorkingDirectory=/home/ac-macmini2/workshop/super-happy-coder
ExecStart=/usr/bin/python3 tg_bot.py
Restart=always
RestartSec=10
Environment=PROXY_URL=http://localhost:8081

[Install]
WantedBy=multi-user.target
```

### 6.2 管理指令

```bash
# 重啟
sudo systemctl restart super-happy-tgbot.service

# 狀態
sudo systemctl status super-happy-tgbot.service

# 日誌
journalctl -u super-happy-tgbot.service -f
```

---

## 七、環境變數

| 變數 | 預設值 | 說明 |
|------|--------|------|
| `STUDENT_BOT_TOKEN` | （見上） | 學員 Bot Token |
| `ADMIN_BOT_TOKEN` | （見上） | 管理者 Bot Token |
| `PROXY_URL` | `http://localhost:8081` | Proxy API 位址 |
| `COOLDOWN_HOURS` | `4` | 超額冷卻時間（小時） |
| `QUOTA_DATA_DIR` | `./data` | 本地狀態資料目錄 |

---

## 八、測試與驗證

### 8.1 學員 Bot 測試

- [ ] `/start` 顯示歡迎訊息
- [ ] `？` 快速引導
- [ ] 發送問題 → 取得回應
- [ ] `/usage` 顯示 token 用量
- [ ] 80% 提醒推送
- [ ] 100% 暫停生效

### 8.2 管理者 Bot 測試

- [ ] `/check` 儀表板完整顯示
- [ ] `/quota` 用戶配額列表
- [ ] `/reset <id>` 解除暫停
- [ ] `/gpu` GPU 狀態
- [ ] `/health` 系統健康

---

## 九、已知限制與改進

### 9.1 限制

1. **Token 估算不精確** — `len(text) // 4` 對中文偏高估
2. **Compute Plane API 不計入** — embedding/rerank/ocr 未計入配額
3. **開放制** — 無加入審核機制，任何人可用

### 9.2 未來改進

- [ ] 精確 Token 計算（使用 tiktoken）
- [ ] Compute Plane API 計入配額
- [ ] 審核制/邀請碼制
- [ ] 管理員白名單限制
- [ ] 尖峰時段分析
- [ ] 改用 `/api/v1/auto`（Agent Executor）而非 `/api/v1/chat`

---

## 十、相關文件

- [Super Happy Coder 流程打通測試紀錄](./2026-01-29-Super-Happy-Coder-流程打通測試紀錄.md)
- [3090 Compute Plane 部署與網路連通紀錄](./2026-01-29-3090-Compute-Plane-部署與網路連通紀錄.md)

---

## 附錄：快速指令參考

### 學員常用

```
？              # 快速引導
/usage          # 查看用量
/status         # Session 狀態
/clear          # 清除對話
```

### 管理者常用

```
/check          # 系統儀表板
/quota          # 用戶配額
/reset tg-xxx   # 解除暫停
/gpu            # GPU 狀態
```
