# Telegram Bots 配置說明

本文檔記錄 ac-mac (Mac Mini) 和 ac-3090 伺服器上部署的 Telegram Bot 配置。

---

## Bot 清單

### 1. AC Server Monitor Bot (登入監控 Bot)
- **用途**: 伺服器監控、SSH 登入通知、系統狀態查詢
- **Bot Token**: `8434771714:AAH***REDACTED***`
- **Chat ID**: `CHAT_ID_REDACTED`
- **服務名稱**: `tg-monitor-bot.service`
- **腳本位置**: `/usr/local/bin/server-monitor/`
- **部署主機**: Mac Mini (ac-mac)

#### 可用指令
| 指令 | 功能 |
|------|------|
| `?` | 顯示幫助訊息 |
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

#### 相關檔案
```
/usr/local/bin/server-monitor/
├── tg-monitor-bot.py      # Bot 主程式
├── check-services.sh      # /check 指令腳本
├── device-stats.sh        # /all 指令腳本
├── daily-report.sh        # 每日報告腳本
├── send-daily-report.sh   # 每日報告發送腳本
└── help.sh                # ? 幫助腳本

/usr/local/bin/telegram-notify.sh  # 通知發送腳本
/etc/ssh/sshrc                     # SSH 登入觸發腳本
/etc/fail2ban/action.d/telegram.conf  # Fail2ban 通知設定
/etc/systemd/system/tg-monitor-bot.service  # 系統服務
```

#### Cron 設定
```
0 8 * * * /usr/local/bin/server-monitor/send-daily-report.sh
```

---

### 2. 知識庫助手 Bot (tg-claude-bot)
- **用途**: 知識庫管理、Claude CLI 整合
- **Bot Token**: `8226788629:AAE***REDACTED***`
- **服務位置**: `/home/ac-mac/tg-claude-bot/`
- **部署主機**: Mac Mini (ac-mac)

#### 功能
- 收集整理文章、連結、筆記
- 自動分類並建立 Markdown 筆記
- 搜尋知識庫
- 與 Claude 互動

#### 相關檔案
```
/home/ac-mac/tg-claude-bot/
├── bot.py        # Bot 主程式
├── config.py     # 配置檔
├── claude_cli.py # Claude CLI 整合
└── bot.log       # 日誌檔
```

---

## 維護指令

### 查看服務狀態
```bash
# Monitor Bot
sudo systemctl status tg-monitor-bot.service

# 知識庫 Bot
ps aux | grep "python3 bot.py"
```

### 重啟服務
```bash
# Monitor Bot
sudo systemctl restart tg-monitor-bot.service

# 知識庫 Bot
cd /home/ac-mac/tg-claude-bot && pkill -f "python3 bot.py" && nohup python3 bot.py >> bot.log 2>&1 &
```

### 查看日誌
```bash
# Monitor Bot
sudo journalctl -u tg-monitor-bot.service -f

# 知識庫 Bot
tail -f /home/ac-mac/tg-claude-bot/bot.log
```

---

## 注意事項

1. **兩個 Bot 使用不同的 Token**，不會互相衝突
2. **Monitor Bot** 負責系統監控，使用 systemd 管理，開機自動啟動
3. **知識庫 Bot** 負責知識管理，需手動啟動或設定自動啟動
4. SSH 登入通知使用 `/etc/ssh/sshrc` 觸發
5. 3090 上只部署監控腳本，不運行 Bot 服務（由 Mac Mini 的 Bot 透過 SSH 遠端執行）

---

*最後更新: 2026-01-25*
