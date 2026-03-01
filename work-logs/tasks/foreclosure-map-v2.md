---
title: 法拍物件地圖 v2
status: pending
priority: medium
machine: acmacmini2
repo: https://github.com/ai-cooperation/foreclosure-map
pages: https://ai-cooperation.github.io/foreclosure-map/
depends_on: foreclosure-map (completed)
---

# 法拍物件地圖 v2

## 前置: v1 已完成
- 全台 22 法院爬取 (8,905 筆)
- 座標轉換: 土地 79% (twland) + 房屋 99.5% (NLSC)
- 前端地圖 + 篩選 + GitHub Pages
- 每週一自動更新 + Telegram/Email 通知
- 詳見: `work-logs/tasks/foreclosure-map.md`

## v2 目標
從「看地圖」進化到「追蹤投資標的」— 讓使用者能追蹤感興趣的物件、比對實價登錄、設定關注區域。

---

## Feature 1: 物件追蹤

### 需求
- 使用者可「收藏」感興趣的物件
- 追蹤物件狀態變化 (拍次遞增、底價下降、已拍定/撤回)
- 收藏的物件有變化時通知

### 技術方案 (純前端，無後端)
- 收藏清單存 localStorage
- 每次載入 current.json 時，比對收藏物件的狀態變化
- 變化偵測: 與上次查看時的 snapshot 比較
- 通知: 頁面內 badge/彈窗顯示變化數量

### 資料結構
```javascript
// localStorage: foreclosure-map-favorites
{
  "TPD-113-執-1234-1-C52": {
    "added_at": "2026-02-14",
    "last_seen": {
      "auction_round": 1,
      "min_price": 19000000,
      "status": "active"
    }
  }
}
```

### UI
- 彈窗加「收藏」按鈕 (星號)
- Sidebar 加「我的收藏」區塊，顯示收藏數量
- 點擊展開收藏列表，變化的物件標紅
- 物件消失 (已拍定) 時顯示提示

---

## Feature 2: 實價登錄整合

### 需求
- 點擊物件時，顯示附近的實價登錄成交行情
- 幫助判斷底價是否合理

### 資料來源
- **內政部實價登錄開放資料**: https://plvr.land.moi.gov.tw/DownloadOpenData
  - 每季更新，CSV/XML 格式
  - 欄位: 交易年月、地址、總價、單價、面積、樓層
- **或**: 內政部不動產資訊平台 API

### 技術方案
- 每季下載實價登錄 CSV → 轉成 JSON (依縣市分檔)
- 前端: 點擊物件時，載入該縣市的實價資料
- 以距離排序，顯示附近 500m 內的近期成交

### 資料結構
```json
// data/market/台北市.json
[
  {
    "address": "大安區忠孝東路三段100號",
    "date": "2025-Q3",
    "total_price": 18500000,
    "unit_price": 680000,
    "area": 27.2,
    "floor": "5/12",
    "lat": 25.041,
    "lng": 121.536
  }
]
```

### UI
- 彈窗新增「附近行情」tab
- 顯示: 近 1 年成交紀錄、平均單價、與底價比較
- 簡易圖表: 底價 vs 市場行情

---

## Feature 3: 關注區域

### 需求
- 使用者在地圖上框選/標記「關注區域」
- 該區域有新物件上架時通知
- 支援多個關注區域

### 技術方案 (純前端)
- Leaflet.draw 外掛：畫矩形或圓形
- 區域定義存 localStorage
- 每次載入 current.json 時，比對區域內是否有新物件
- 新物件以不同顏色 marker 顯示

### 資料結構
```javascript
// localStorage: foreclosure-map-areas
[
  {
    "name": "板橋站周邊",
    "type": "circle",
    "center": [25.014, 121.462],
    "radius": 1000,
    "created_at": "2026-02-14"
  },
  {
    "name": "大安區",
    "type": "rectangle",
    "bounds": [[25.02, 121.52], [25.05, 121.56]],
    "created_at": "2026-02-14"
  }
]
```

### UI
- 工具列加「畫區域」按鈕
- 側邊欄加「關注區域」管理
- 區域內新物件數量 badge
- 可開關區域顯示/隱藏

---

## Feature 4: 進階通知 (需後端)

### 如果要做推播通知 (非純前端)
- 後端: 簡單的 Python 腳本在 acmacmini2 上
- 每週 build.py 執行後，比對「關注區域」和「收藏物件」的變化
- 透過 Telegram Bot 發送個人化通知
- 需要使用者註冊 (Telegram user ID + 關注設定)

### 簡化版: 不做後端
- 所有狀態存 localStorage
- 使用者自己開網頁時才看到變化
- 不需要後端、不需要使用者註冊

---

## 實作順序

### v2.1: 物件追蹤 (純前端)
- [ ] 彈窗加收藏按鈕
- [ ] localStorage 儲存/讀取收藏
- [ ] Sidebar 收藏列表
- [ ] 物件狀態變化偵測

### v2.2: 關注區域 (純前端)
- [ ] 加入 Leaflet.draw
- [ ] 畫區域 + localStorage 儲存
- [ ] 區域內新物件標示
- [ ] 區域管理 UI

### v2.3: 實價登錄 (需資料準備)
- [ ] 下載實價登錄 CSV
- [ ] 轉換 + geocode 為 JSON (依縣市)
- [ ] 彈窗「附近行情」tab
- [ ] 行情比較 UI

### v2.4: 通知整合 (可選)
- [ ] 後端變化偵測腳本
- [ ] Telegram 個人化通知
- [ ] 使用者訂閱管理

---

## 技術棧變化

| 項目 | v1 | v2 新增 |
|------|-----|---------|
| 前端 | Leaflet + vanilla JS | + Leaflet.draw |
| 儲存 | 無 | localStorage |
| 資料 | current.json | + market/*.json (實價) |
| 通知 | Email + TG (全體) | + TG 個人化 (可選) |
| 後端 | 無 | 無 (v2.1~v2.3 純前端) |
