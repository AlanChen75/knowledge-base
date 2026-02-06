# Telegram Bots 配置說明

本文檔記錄 ac-mac (Mac Mini) 和 ac-3090 伺服器上部署的 Telegram Bot 配置。

---

## Bot 總覽

| Bot 名稱 | Username | Token (前綴) | systemd 服務 | 用途 |
|---------|----------|-------------|-------------|------|
| AC Server Monitor Bot | @ac_server_monitor_bot | `8434771714:AAH***` | `tg-monitor-bot.service` | 系統監控、SSH 登入通知 |
| 知識庫助手 Bot | @RemoteAi123_bot | `8226788629:AAE***` | `tg-claude-bot.service` | 知識庫管理、Claude 互動 |
| ComfyUI Bot | @ac_comfyui_bot | `8163548022:AAH***` | `comfyui-tg-bot.service` | ComfyUI 圖片生成 |

**重要**:
- 三個 Bot 各有獨立的 Token，不會互相衝突
- **所有 Bot 都由 systemd 管理**，請用 `systemctl` 操作，不要手動 kill/啟動

---

## ac-mac 長駐服務總覽

| 服務名稱 | 說明 | 狀態 |
|---------|------|------|
| `tg-monitor-bot.service` | 系統監控 Telegram Bot | 開機自啟 |
| `tg-claude-bot.service` | 知識庫 Telegram Bot | 開機自啟 |
| `comfyui-tg-bot.service` | ComfyUI 圖片生成 Bot | 開機自啟 |
| `happy-coder.service` | Happy Coder 服務 | 開機自啟 |
| `n8n.service` | n8n 工作流自動化 | 開機自啟 |
| `fail2ban.service` | SSH 入侵防護 | 開機自啟 |
| `tailscaled.service` | Tailscale VPN | 開機自啟 |

---

## Bot 詳細資訊

### 1. AC Server Monitor Bot (@ac_server_monitor_bot)
- **用途**: 伺服器監控、SSH 登入通知、系統狀態查詢
- **Bot Token**: `8434771714:AAH***（見 ~/.env）`
- **Chat ID**: `（見 ~/.env）`
- **systemd 服務**: `tg-monitor-bot.service`
- **腳本位置**: `/usr/local/bin/server-monitor/tg-monitor-bot.py`
- **部署主機**: Mac Mini (ac-mac)

#### 可用指令
| 指令 | 功能 |
|------|------|
| `?` 或 `？` | 顯示幫助訊息 |
| `/check` | 檢查 Mac Mini 和 3090 的系統狀態與服務 |
| `/all` | 查看兩台機器的完整效能報告（CPU、RAM、磁碟、GPU） |

#### 自動通知功能
- **SSH 登入通知**: 有人登入時發送通知，包含用戶名、來源 IP、地理位置（或 Tailscale 內網標記）
- **Fail2ban 通知**: IP 封鎖/解封時發送通知
- **每日報告**: 每天早上 8:00 自動發送前一天的運行統計

#### 監控的服務
**Mac Mini:**
- n8n (工作流自動化)
- happy-coder (Happy Coder 服務)
- fail2ban (入侵防護)
- tailscaled (Tailscale VPN)
- tg-claude-bot (知識庫 Bot)

**3090 Server:**
- fail2ban (入侵防護)
- tailscaled (Tailscale VPN)
- nvidia-persistenced (NVIDIA GPU 服務)
- vllm (Qwen2.5-7B-Instruct LLM 推理)
- compute-plane (GPU 運算 API)

#### 相關檔案
```
/usr/local/bin/server-monitor/
├── tg-monitor-bot.py      # Bot 主程式
├── config.py              # 配置檔（Token、User ID）
├── check-services.sh      # /check 指令腳本
├── device-stats.sh        # /all 指令腳本
├── daily-report.sh        # 每日報告腳本
├── send-daily-report.sh   # 每日報告發送腳本
└── help.sh                # ? 幫助腳本

/usr/local/bin/telegram-notify.sh  # 通知發送腳本
/etc/ssh/sshrc                     # SSH 登入觸發腳本
/etc/fail2ban/action.d/telegram.conf  # Fail2ban 通知設定
/etc/systemd/system/tg-monitor-bot.service  # systemd 服務檔
```

#### Cron 設定
```
0 8 * * * /usr/local/bin/server-monitor/send-daily-report.sh
```

---

### 2. 知識庫助手 Bot (@RemoteAi123_bot)
- **用途**: 知識庫管理、Claude CLI 整合、系統狀態查詢
- **Bot Token**: `8226788629:AAE***（見 ~/.env）`
- **systemd 服務**: `tg-claude-bot.service`
- **腳本位置**: `/home/ac-mac/tg-claude-bot/bot.py`
- **部署主機**: Mac Mini (ac-mac)

#### 可用指令
| 指令 | 功能 |
|------|------|
| `?` 或 `？` | 顯示幫助訊息 |
| `/new` | 開始新對話 |
| `/check` | 檢查 Mac Mini 和 3090 的系統狀態與服務 |
| `/all` | 查看兩台機器的完整效能報告 |

#### 功能
- 收集整理文章、連結、筆記
- 自動分類並建立 Markdown 筆記
- 搜尋知識庫
- 與 Claude 互動
- 圖片分析並存檔
- PDF 處理並提取重點

#### 相關檔案
```
/home/ac-mac/tg-claude-bot/
├── bot.py                 # Bot 主程式
├── config.py              # 配置檔（Token、User ID、知識庫路徑）
├── claude_cli.py          # Claude CLI 整合
├── content_classifier.py  # 內容分類器
├── processing_config.py   # 處理策略配置
├── simplified_prompts.py  # 簡化版 System Prompt
└── bot.log                # 日誌檔

/etc/systemd/system/tg-claude-bot.service  # systemd 服務檔
```

#### systemd 服務設定
```ini
[Unit]
Description=Telegram Knowledge Base Bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=ac-mac
WorkingDirectory=/home/ac-mac/tg-claude-bot
ExecStart=/usr/bin/python3 /home/ac-mac/tg-claude-bot/bot.py
Restart=always
RestartSec=10
Environment=HOME=/home/ac-mac
Environment=PATH=/usr/local/bin:/usr/bin:/bin:/home/ac-mac/.local/bin

[Install]
WantedBy=multi-user.target
```

---

### 3. ComfyUI Bot (@ac_comfyui_bot)
- **用途**: ComfyUI 圖片生成
- **Bot Token**: `8163548022:AAH***（見 ~/.env）`
- **systemd 服務**: `comfyui-tg-bot.service`
- **腳本位置**: `/home/ac-mac/comfyui-telegram-bot.py`
- **部署主機**: Mac Mini (ac-mac)

#### 相關檔案
```
/home/ac-mac/comfyui-telegram-bot.py  # Bot 主程式
/etc/systemd/system/comfyui-tg-bot.service  # systemd 服務檔
```

#### systemd 服務設定
```ini
[Unit]
Description=ComfyUI Telegram Bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=ac-mac
WorkingDirectory=/home/ac-mac
ExecStart=/usr/bin/python3 /home/ac-mac/comfyui-telegram-bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

---

## 維護指令

### 查看所有 Bot 服務狀態
```bash
sudo systemctl status tg-monitor-bot tg-claude-bot comfyui-tg-bot
```

### 查看單一服務狀態
```bash
sudo systemctl status tg-monitor-bot.service
sudo systemctl status tg-claude-bot.service
sudo systemctl status comfyui-tg-bot.service
```

### 重啟服務（正確方式）
```bash
# ⚠️ 重要：使用 systemctl，不要手動 kill + 啟動
sudo systemctl restart tg-monitor-bot.service
sudo systemctl restart tg-claude-bot.service
sudo systemctl restart comfyui-tg-bot.service
```

### 查看日誌
```bash
# Monitor Bot
sudo journalctl -u tg-monitor-bot.service -f

# 知識庫 Bot
sudo journalctl -u tg-claude-bot.service -f
# 或查看檔案日誌
tail -f /home/ac-mac/tg-claude-bot/bot.log

# ComfyUI Bot
sudo journalctl -u comfyui-tg-bot.service -f
```

### 停止/啟動服務
```bash
sudo systemctl stop tg-claude-bot.service
sudo systemctl start tg-claude-bot.service
```

### 禁用/啟用開機自啟
```bash
sudo systemctl disable tg-claude-bot.service  # 禁用開機自啟
sudo systemctl enable tg-claude-bot.service   # 啟用開機自啟
```

---

## 注意事項

1. **三個 Bot 使用不同的 Token**，不會互相衝突
2. **所有 Bot 都由 systemd 管理**（`Restart=always`），不要手動 kill 後用 nohup 啟動，會造成多進程衝突
3. **正確的重啟方式**：`sudo systemctl restart <service-name>`
4. SSH 登入通知使用 `/etc/ssh/sshrc` 觸發
5. 3090 上只部署監控腳本，不運行 Bot 服務（由 Mac Mini 的 Bot 透過 SSH 遠端執行）
6. 已禁用舊的 `telegram-bot.service`（避免與 Monitor Bot 衝突）
7. **Token 安全**：所有 token 只存放在 `~/.env` 或程式碼的環境變數讀取中，不要 commit 到 git

---

## 其他長駐服務

### Happy Coder (`happy-coder.service`)
- **用途**: Happy Coder AI 助手服務
- **腳本位置**: `/home/ac-mac/.nvm/versions/node/v20.20.0/bin/happy`

### n8n (`n8n.service`)
- **用途**: 工作流自動化平台
- **Web UI**: http://localhost:5678

---

*最後更新: 2026-02-06*
