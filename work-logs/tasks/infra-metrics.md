---
title: Infrastructure Metrics 監控系統
status: active
priority: high
created: 2026-03-09
repo: https://github.com/AlanChen75/infra-metrics
dashboard: https://alanchen75.github.io/infra-metrics/
---

# Infrastructure Metrics 監控系統

## 目標
建立去中心化的時序監控系統，每 5 分鐘採集所有節點指標，每日推送到 GitHub，配合 Dashboard 觀察歷史趨勢與任務關聯性。

## 架構
- **採集**: 各台本地 cron 每 5 分鐘 → /var/lib/infra-metrics/YYYY-MM-DD.csv
- **主推送**: ac-mac cron 00:10 → SSH 拉 5 台 CSV → git push
- **備案推送**: GitHub Actions 06:00 (台灣) → Tailscale SSH 拉數據
- **Dashboard**: GitHub Pages + Chart.js 暗色主題

## 節點採集狀態

| 節點 | 採集腳本 | cron | 資料項 |
|------|---------|------|--------|
| ac-3090 | /var/lib/infra-metrics/collect-metrics.sh | */5 | CPU/RAM/溫度/磁碟/GPU |
| ac-mac | /var/lib/infra-metrics/collect-metrics.sh | */5 | CPU/RAM/溫度/磁碟 |
| ac-mac | /var/lib/infra-metrics/collect-ai-hub.sh | */5 | AI Hub 服務狀態+用量 |
| ac-rpi5 | /var/lib/infra-metrics/collect-metrics.sh | */5 | CPU/RAM/溫度/磁碟 |
| acmacmini2 | /var/lib/infra-metrics/collect-metrics.sh | */5 | CPU/RAM/溫度/磁碟 |
| ac-2012 | /var/lib/infra-metrics/collect-metrics.sh | */5 | CPU/RAM/溫度/磁碟 |

## 推送排程 (ac-mac cron)
- 00:10 daily-push.sh — 拉所有節點 CSV + git push

## CSV 格式
### 節點指標
timestamp,cpu_percent,mem_used_mb,mem_total_mb,temp_c,disk_percent,gpu_temp,gpu_util,gpu_mem_used_mb,gpu_mem_total_mb

### AI Hub
timestamp,provider,category,busy,healthy,today_used,daily_limit,remaining

## 關鍵檔案
- Repo: AlanChen75/infra-metrics (public)
- 腳本: ~/infra-metrics/scripts/
- Actions: .github/workflows/backup-collect.yml
- Dashboard: index.html (GitHub Pages root)
- PAT: ~/.env (GITHUB_PAT_INFRA) — fine-grained, 僅限 infra-metrics repo
- gh auth: ~/.config/gh/hosts.yml (AlanChen75)

## 完成項目
- [x] GitHub repo 建立 (public)
- [x] collect-metrics.sh 通用採集腳本
- [x] collect-ai-hub.sh AI Hub 採集
- [x] daily-push.sh 集中推送
- [x] GitHub Actions 備案 workflow
- [x] 5 台 cron 部署 + 驗證
- [x] GitHub Pages Dashboard 上線

## 待辦
- [ ] GitHub Actions Secrets 設定 (TS_OAUTH_CLIENT_ID, TS_OAUTH_SECRET, SSH_PRIVATE_KEY)
- [ ] 清理 gh-pages 分支 (不需要，可刪除)
- [ ] 累積數據後驗證 Dashboard 曲線顯示
- [ ] 考慮加入 CSV 自動清理 (保留 N 天)
