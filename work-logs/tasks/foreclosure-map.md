---
title: 法拍物件地圖系統
status: completed
priority: high
machine: acmacmini2
repo: https://github.com/ai-cooperation/foreclosure-map
pages: https://ai-cooperation.github.io/foreclosure-map/
---

# 法拍物件地圖系統 (foreclosure-map)

## 目標
全自動化全台法拍物件爬取 → 座標轉換 → 地圖顯示系統

## 專案位置
- **acmacmini2**: `/home/ac-macmini2/foreclosure-map/`
- **GitHub**: https://github.com/ai-cooperation/foreclosure-map
- **公開網頁**: https://ai-cooperation.github.io/foreclosure-map/
- **OpenSpec**: `OPENSPEC.md` (repo 根目錄)

## 進度

### Phase 1: 基礎驗證 ✅
- [x] acmacmini2 Python + Playwright 環境
- [x] scrape.py — AJAX 攔截爬蟲 (22 法院)
- [x] geocode.py — 土地 twland + 房屋 NLSC
- [x] build.py — 歷史追蹤邏輯

### Phase 2: 前端地圖 ✅
- [x] index.html + Leaflet + NLSC 底圖
- [x] js/app.js — 篩選、標記聚合、多邊形
- [x] css/style.css — RWD
- [x] GitHub Pages 啟用

### Phase 3: 全台擴展 ✅
- [x] 全台 22 法院完整爬取 (8,905 筆)
- [x] 權利範圍 (rrange) 欄位 + 篩選
- [x] 公告原文 PDF 連結 (DO_VIEWPDF.htm)

### Phase 4: 自動化 ✅
- [x] acmacmini2 GitHub SSH deploy key (write access)
- [x] run.sh cron 入口腳本
- [x] crontab: 每週一 06:00
- [x] Email 通知 (Gmail SMTP)
- [x] Telegram 通知 (成功/失敗)
- [x] `/check` 指令整合 (check-services.sh)
- [x] 狀態檔 `/tmp/foreclosure-map-status.json`

### Phase 5: 座標轉換 ✅
- [x] 土地: twland.ronny.tw API — 79% (5,408/6,847)
- [x] 房屋: NLSC MapSearch API — 99.5% (2,048/2,058)
- [x] 座標快取 (land_cache.json + address_cache.json)
- [x] 總計: 7,456/8,905 = 83.7% 有座標

## 最終數據 (2026-W06)
| 項目 | 數量 |
|------|------|
| 物件總數 | 8,905 |
| 有座標 (地圖顯示) | 7,456 (83.7%) |
| 土地 geocode | 5,408/6,847 (79.0%) |
| 房屋 geocode | 2,048/2,058 (99.5%) |
| 法院數 | 22 |

## 外部服務 (全部免費免 key)
| 服務 | 用途 |
|------|------|
| twland.ronny.tw | 土地地號→座標+地籍邊界 |
| NLSC MapSearch API | 地址→座標 (門牌等級) |
| NLSC WMTS | 地圖底圖 |
| GitHub Pages | 靜態網站部署 |

## 監控方式
- **Telegram**: 每週執行後即時通知 (成功/失敗)
- **`/check` 指令**: 顯示上次更新日期和物件數
- **Email**: 每週更新通知 (notify-emails.txt)

## 已知限制
1. twland API 資料為 2015 年前地籍圖，重測後新段名查不到 (21% 土地失敗主因)
2. 10 筆房屋 geocode 失敗：地址欄位為「無」或「.」(原始資料問題)

## 關鍵技術筆記
- 法拍系統 AJAX: `WHD1A02/QUERY.htm` 回傳 JSON，用 `page.on("response")` 攔截
- NLSC geocoding: 地址需雙重 URL encode，優先取「門牌」類型結果
- twland 多筆結果: 以鄉鎮名稱匹配正確地段

## Session 紀錄
| 日期 | 工作內容 |
|------|---------|
| 2026-02-10 | Phase 1+2: 爬蟲+座標+前端+GitHub Pages 部署 |
| 2026-02-11 | Phase 3: 全台 22 法院 8,298 筆 |
| 2026-02-12 | Phase 4: run.sh + cron + deploy key + Email 通知 |
| 2026-02-13 | rrange 欄位、PDF 連結修正、TGOS 批次工具 |
| 2026-02-14 | NLSC geocoding 整合 (房屋 0%→99.5%)、Telegram 監控 |
