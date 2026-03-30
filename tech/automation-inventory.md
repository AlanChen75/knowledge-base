# 全節點自動腳本總盤點

> 最後更新: 2026-03-24

## ac-mac（中央節點）— 12 cron + 6 systemd

### Cron Jobs
| # | 排程 | 任務 | 說明 |
|---|------|------|------|
| 1 | 每日 05:50 | chrome-hold-check.sh | Chrome 版本鎖定檢查 |
| 2 | 每日 06:00 | send-daily-report.sh | 每日系統報告（TG） |
| 3 | 每日 06:05 | ai-hub-health-check.py | AI Hub 健康檢查，彙整所有 heartbeat 推送 TG |
| 4 | 每日 06:10 | backfill-images.py --site all | ai100 + s100 補圖 |
| 5 | 每日 09/13/18:05 | ai-news-pipeline.py --max 3 | AI 100 + 永續 100 新聞更新 |
| 6 | 週一 03:30 | aeo-monitor.py | AEO 監控 |
| 7 | 週三 04:00 | aeo-monitor.py | AEO 監控 |
| 8 | 週五 04:30 | aeo-monitor.py | AEO 監控 |
| 9 | 每 5 分鐘 | collect-metrics.sh | 基礎設施指標收集 |
| 10 | 每 5 分鐘 | collect-ai-hub.sh | AI Hub 指標收集 |
| 11 | 每日 00:10 | daily-push.sh | 指標日推送 |
| 12 | 3/6 08:00（一次性） | generate-brand-film.sh | Brand Film 生成 |

### Systemd Services
| # | 服務 | 說明 |
|---|------|------|
| 1 | ai-hub.service | AI Service Hub Gateway |
| 2 | ai-hub-funnel.service | AI Hub Tailscale Funnel（公開 HTTPS） |
| 3 | tg-monitor-bot.service | Telegram 監控 Bot |
| 4 | tg-claude-bot.service | Telegram 知識庫 Bot |
| 5 | comfyui-tg-bot.service | ComfyUI Telegram Bot |
| 6 | n8n.service | n8n 工作流自動化 |

## acmacmini2 — 8 cron

| # | 排程 | 任務 | 說明 |
|---|------|------|------|
| 1 | 週二 10:00 | foreclosure-map/scripts/run.sh | 法拍地圖週更新 |
| 2 | 每 30 分鐘 | world-monitor/deploy/warm-cache.sh | World Monitor 快取預熱 |
| 3 | 每日 08:30 | insurance-kb/run-insurance-kb.sh | 保險知識庫爬取 |
| 4 | 每日 20:30 | insurance-kb/run-insurance-kb.sh | 保險知識庫爬取 |
| 5 | 每 5 分鐘 | taipower-data/cron-collect.sh | 台電即時數據收集 |
| 6 | 每小時 :05 | taipower-data/cron-push.sh | 台電數據推送 |
| 7 | 每日 14:00 | taipower-data/cron-screenshot.sh | 台電截圖 |
| 8 | 每 5 分鐘 | collect-metrics.sh | 基礎設施指標收集 |

## ac-3090 — 3 cron

| # | 排程 | 任務 | 說明 |
|---|------|------|------|
| 1 | 每日 08:00 | daily-report.sh | 日報 |
| 2 | 每 5 分鐘 | tailscale-monitor.sh | Tailscale 新裝置偵測 |
| 3 | 每 5 分鐘 | collect-metrics.sh | 基礎設施指標收集 |

## ac-rpi5 — 1 cron

| # | 排程 | 任務 | 說明 |
|---|------|------|------|
| 1 | 每 5 分鐘 | collect-metrics.sh | 基礎設施指標收集 |

## 統計

| 節點 | Cron | Systemd | 合計 |
|------|------|---------|------|
| ac-mac | 12 | 6 | 18 |
| acmacmini2 | 8 | 0 | 8 |
| ac-3090 | 3 | 0 | 3 |
| ac-rpi5 | 1 | 0 | 1 |
| **合計** | **24** | **6** | **30** |

## Heartbeat 機制

各 pipeline 透過 heartbeat.sh 回報 ok/failed → 每日 06:05 ai-hub-health-check.py 彙整所有狀態 → 推送 TG 通知。
若 pipeline crash 導致 heartbeat 未呼叫，health-check 會顯示「過期/無回報」。

## ai-sustainability-platform — 5 GitHub Actions

| # | 排程 | Workflow | 說明 | TG 通知 |
|---|------|---------|------|---------|
| 1 | 每小時 | Hourly Real-Time Update | 即時數據（碳強度/空氣/天氣/AQI/水庫） | 無 |
| 2 | 每 6 小時 | API Health Check | 31 資料源 API 健康檢查 | 已停用 (2026-03-24) |
| 3 | 每日 UTC 06:00 (台灣 14:00) | Daily Pipeline Update | 6 大 pipeline + AI Forecast | 已停用 (2026-03-24) |
| 4 | push 觸發 | CI | 持續整合 | 無 |
| 5 | push/手動 | Deploy Dashboard | 部署儀表板到 GitHub Pages | 無 |

### 已停用通知 (2026-03-24)
- Daily Pipeline Summary（每日 ~15:00 推送 pipeline 結果 + forecast）
- API Health Check TG 通知（每 6 小時推送 API 狀態）
- 原因：通知過多，干擾日常

## 更新後統計

| 節點/平台 | Cron | Systemd | GitHub Actions | 合計 |
|-----------|------|---------|----------------|------|
| ac-mac | 12 | 6 | 0 | 18 |
| acmacmini2 | 8 | 0 | 0 | 8 |
| ac-3090 | 3 | 0 | 0 | 3 |
| ac-rpi5 | 1 | 0 | 0 | 1 |
| ai-sustainability-platform | 0 | 0 | 5 | 5 |
| **合計** | **24** | **6** | **5** | **35** |
