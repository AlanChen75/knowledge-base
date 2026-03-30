---
title: World Monitor APAC Fork
status: active
priority: medium
started: 2026-03-04
---

# World Monitor APAC Fork

Fork koala73/worldmonitor (AGPL-3.0) → ai-cooperation/world-monitor
亞太/台灣焦點情報儀表板

## 架構
- 前端: GitHub Pages → https://cooperation.tw/world-monitor/
- 後端: acmacmini2 → https://api-monitor.cooperation.tw (Cloudflare Tunnel)
- 快取: Upstash Redis (雲端)

## 已完成 ✅
- [x] Fork repo + develop branch
- [x] Express API Server wrapper (deploy/api-server.mjs, 44 route handlers)
- [x] Systemd services (world-monitor-api + world-monitor-relay)
- [x] Nginx reverse proxy (port 3001 API + port 3004 relay)
- [x] Cloudflare Tunnel (HKG01 → api-monitor.cooperation.tw)
- [x] 前端域名適配 (runtime.ts ALLOWED_REDIRECT_HOSTS + cooperation.tw)
- [x] CORS 白名單 (server/cors.ts, api/_cors.js, api/_api-key.js)
- [x] Vite build (base=/world-monitor/, VITE_WS_API_URL)
- [x] GitHub Actions deploy-pages.yml
- [x] 地圖預設中心 → 台灣 (121.5, 25.0)
- [x] 6 個 APAC hotspots (南海、東海、緬甸、首爾、東協、新竹)
- [x] 5 個 CII 國家 (PH, VN, ID, SG, TH)
- [x] 20+ APAC RSS feeds + 13 sustainability/ESG feeds
- [x] API Keys: Upstash, Groq, AISStream, FRED, EIA, NASA FIRMS
- [x] tsx loader for TypeScript RPC handlers
- [x] 修復重複 CORS headers (Access-Control-Allow-Origin 大小寫重複)
- [x] Panel 排序 (有資料的排前面)
- [x] Cache warming cron (每 30 分鐘)

## API 端點狀態 (22 RPC + legacy)
有資料: 16/22 (news, intelligence, seismology, climate, cyber, market,
  wildfire, infrastructure, aviation, prediction, displacement, giving,
  trade, supply-chain, natural, research)
空資料: conflict/unrest (ACLED OAuth 已知問題), military (WINGBITS 付費),
  maritime (NGA 地區限制), positive-events (cache 累積中)

## 已知問題
- RSS 新聞聚合在 Mac Mini 上太慢 (>120s, Cloudflare 超時)
- ACLED 需 OAuth 24h token, 上游 issue #290 未解
- WINGBITS 需付費
- News panel 需要 RSS 個別載入而非聚合

## 關鍵檔案
- deploy/api-server.mjs — Express wrapper (44 routes)
- deploy/systemd/*.service — systemd 服務
- deploy/nginx/world-monitor.conf — Nginx config
- deploy/warm-cache.sh — Cache 預熱腳本
- src/config/panels.ts — Panel 排序
- src/config/geo.ts — APAC hotspots
- src/config/feeds.ts — RSS feeds
- src/services/runtime.ts — API redirect

## acmacmini2 服務
- world-monitor-api.service (port 3001, Node+tsx)
- world-monitor-relay.service (port 3004, AIS+Market+CII)
- Nginx (port 80, reverse proxy)
- cloudflared (Cloudflare Tunnel)
- Cron: warm-cache.sh 每 30 分鐘

## .env (acmacmini2:/home/ac-macmini2/world-monitor/.env)
包含: UPSTASH_REDIS_*, GROQ_API_KEY, AISSTREAM_API_KEY,
  FRED_API_KEY, EIA_API_KEY, NASA_FIRMS_API_KEY,
  RELAY_SHARED_SECRET, WS_RELAY_URL
