---
title: 低碳永續100講
status: in_progress
priority: high
started: 2026-02-15
updated: 2026-02-20
---

# 低碳永續100講 — 系統規格與進度追蹤

## 1. 專案概況

| 項目 | 說明 |
|------|------|
| 總議題數 | 100 講（10 系列 × 10 講） |
| 每日產量 | 2 集（DAILY_LIMIT = 2） |
| 預估完成 | ~43 天（87 集待處理） |
| 自動排程 | ac-mac systemd timer，每日 10:00 自動執行 |
| 網站 | https://ai-cooperation.github.io/sustainability-100/ |
| GitHub repo | github-s100:ai-cooperation/sustainability-100.git |
| 網站 repo 本地 | `/home/ac-mac/sustainability-100` |
| 內容目錄 | `/usr/local/bin/ai-hub/content/sustainability100/` |
| Topics 定義 | `topics.json`（100 筆，含 id/title/outline/subtopics/series） |
| Log 目錄 | `/var/log/ai-hub/`（pipeline.log, podcast-tracker.log, pipeline-audit.log） |

---

## 2. 系統架構

### 2.1 Pipeline 7 步驟

```
Step 1: 研究（Research）
  └─ Groq LLM + Gemini Search → research.md + verification.json

Step 2: Podcast 生成（NotebookLM）
  └─ 建立 Notebook → 加入來源 → 生成英文 + 中文音訊（非同步）
  └─ 回傳 notebook_url，podcast_tracker 負責下載

Step 3: 影片製作（Video）
  └─ LLM 腳本 → Gemini Veo 或 NotebookLM Video Overview

Step 4: 簡報（Slides）
  └─ LLM 大綱 → 4 張簡報 → Gemini 配圖（含 retry 3 次）

Step 5: 逐字稿（Transcript）— 目前未實作
  └─ 需要 TTS 或 Whisper 處理

Step 6: 發佈（Publish）
  └─ 生成 _episodes/EPXXX.md，複製 assets 到網站 repo

Step 7: 部署（Deploy）
  └─ git add → pull --rebase --autostash → commit → push
```

### 2.2 排程時間表

| 時間 | 服務 | 說明 |
|------|------|------|
| 09:00 | ai-hub-watchdog | 系統健康檢查 |
| 10:00 | ai-hub-pipeline | 每日執行 2 集 pipeline（step 1-7） |
| 10:30 | automation-pipeline-audit | 巡檢 log + TG 推送報告 |
| 每 15 分 | automation-podcast-tracker | 偵測 NotebookLM 完成的音訊/影片並下載 |
| 每 2 分 | ai-hub-idle-check | Chrome 閒置超過 20 分鐘自動關閉 |

### 2.3 關鍵檔案

| 檔案 | 位置 | 說明 |
|------|------|------|
| sustainability100.py | `/usr/local/bin/ai-hub/content/sustainability100/` | 主 pipeline |
| podcast_tracker.py | `/usr/local/bin/ai-hub/automations/` | Podcast 下載追蹤器 |
| pipeline_audit.py | `/usr/local/bin/ai-hub/automations/` | 每日巡檢報告 |
| job_tracker.py | `/usr/local/bin/ai-hub/automations/` | 非同步 job 完成追蹤 |
| notebooklm.py | `/usr/local/bin/ai-hub/providers/` | NotebookLM provider（Phase 1） |
| notebooklm_video.py | `/usr/local/bin/ai-hub/providers/` | NotebookLM Video provider |
| topics.json | 內容目錄 | 100 講主題定義 |
| state.json | 內容目錄/EPXXX/ | 每集執行狀態 |

### 2.4 AI Hub 依賴鏈

| 功能 | Provider chain |
|------|---------------|
| Podcast | notebooklm（Chrome port 9225） |
| Video | notebooklm_video → gemini_video（Chrome port 9222） |
| Image | gemini_image（Chrome port 9222） |
| LLM | groq_llm → gemini_chat（Chrome port 9226） |
| 搜尋 | Gemini Search（via gemini_chat） |

---

## 3. Podcast 雙語音機制

### 3.1 NotebookLM 生成流程（Provider）

```
Step 5a: 點擊 Audio Overview card → 英文音訊直接開始生成
Step 5b: 點擊 ✏️ 自訂按鈕 → 填入中文 topic → 點擊「生成」→ 中文音訊開始生成
Step 7:  點擊 Video Overview card → 影片開始生成
```

- 英文和中文音訊**同時在同一個 Notebook 中生成**
- 生成時間：約 5-15 分鐘
- NotebookLM Pro 帳號（d11351004@gmail.com）：每日 20 audio + 20 video

### 3.2 Podcast Tracker 下載流程

```
1. 連接 Chrome CDP (port 9225)
2. 設定 Browser.setDownloadBehavior（CRITICAL：不設定 = 下載被靜默封鎖）
3. 進入 Studio 分頁
4. 偵測 audio_magic_eraser 項目（= 音訊）
5. 點擊相鄰的「更多」按鈕 → 選「下載」
6. 監控 ~/下載/ 目錄等待新檔案或覆寫
7. 移動檔案到 content/EPXXX/podcast.m4a
8. 部署到 website repo + git push
```

### 3.3 Podcast 部署狀態

| EP | 英文 (podcast.m4a) | 中文 (podcast_zh.m4a) | 網站部署 |
|----|-------------------|---------------------|---------|
| EP001 | podcast_en.m4a (26MB) | 0-byte (失敗) | 僅英文 |
| EP002 | 25MB | 32MB | EN + ZH |
| EP003 | 27MB | 29MB | EN + ZH |
| EP004 | 26MB | 33MB | EN + ZH |
| EP005 | 33MB | 28MB | EN + ZH |
| EP006 | 30MB | 31MB | EN + ZH |
| EP007 | 29MB | 15MB（偏小？） | EN + ZH |
| EP008-EP011 | 無 | 無 | 無 |
| EP012 | 24MB | 無 | 僅英文 |

**待修復：**
1. Podcast Tracker 需下載**兩個**音訊（EN + ZH），分別存為 `podcast.m4a` 和 `podcast_zh.m4a`
2. Deploy 函式需同時部署兩個檔案 + 更新 front matter
3. EP001 中文 Podcast 需重新生成（之前 0-byte）
4. EP007 中文 Podcast 品質確認（15MB vs 其他 28-33MB）

### 3.4 網站模板（已支援雙語）

```yaml
# episode front matter
podcast_audio: podcast.m4a       # → Podcast (English) 播放器
podcast_zh: podcast_zh.m4a       # → Podcast（中文）播放器（缺此欄位則不顯示）
transcript_en: transcript_en.txt  # → Download Transcript (EN)
video_overview: video_overview.mp4
```

---

## 4. 進度統計（截至 2026-02-20）

### 4.1 總覽

| 狀態 | 數量 |
|------|------|
| completed | 9 |
| in_progress | 4 |
| pending | 87 |

### 4.2 各集詳細狀態

| EP | 狀態 | Steps 完成 | Podcast | Video | EN音訊 | ZH音訊 |
|----|------|-----------|---------|-------|--------|--------|
| EP001 | completed | 1,3,4,6,7 | failed | skipped | - | - |
| EP002 | completed | 1,2,3,4,6,7 | completed | skipped | 24MB | 31MB |
| EP003 | completed | 1,3,4,6,7 | completed | skipped | 26MB | 28MB |
| EP004 | completed | 1,2,3,4,6,7 | completed | skipped | 25MB | 32MB |
| EP005 | completed | 1,2,3,4,6,7 | completed | skipped | 32MB | 27MB |
| EP006 | completed | 1,3,4,6,7 | completed | skipped | 29MB | 30MB |
| EP007 | completed | 1,3,4,6,7 | completed | skipped | 28MB | 14MB |
| EP008 | in_progress | 1,6,7 | pending | skipped | - | - |
| EP009 | completed | 1,2,3,4,6,7 | failed | skipped | - | - |
| EP010 | in_progress | 1,6,7 | pending | skipped | - | - |
| EP011 | completed | 1,2,3,4,6,7 | failed | skipped | - | - |
| EP012 | in_progress | 1,2,3,7 | completed | skipped | 23MB | - |
| EP013 | in_progress | 1,3,4,6,7 | failed | skipped | - | - |

### 4.3 10 大系列

| 系列 | 名稱 | EP 範圍 | 進度 |
|------|------|---------|------|
| S1 | 淨零基礎與碳盤查 | EP001-EP010 | 7完成 2進行中 1待辦 |
| S2 | 節能減碳技術 | EP011-EP020 | 2完成 2進行中 6待辦 |
| S3 | 再生能源與綠電 | EP021-EP030 | 全部待辦 |
| S4 | 碳交易與碳定價 | EP031-EP040 | 全部待辦 |
| S5 | 永續揭露與法規 | EP041-EP050 | 全部待辦 |
| S6 | 永續報告實務 | EP051-EP060 | 全部待辦 |
| S7 | 供應鏈碳管理 | EP061-EP070 | 全部待辦 |
| S8 | 前瞻減碳技術 | EP071-EP080 | 全部待辦 |
| S9 | AI × 永續管理 | EP081-EP090 | 全部待辦 |
| S10 | 永續策略與展望 | EP091-EP100 | 全部待辦 |

---

## 5. 已知問題

### 5.1 Critical

| # | 問題 | 影響 | 狀態 |
|---|------|------|------|
| 1 | ~~中文 Podcast 未部署到網站~~ | EP002-EP007 已部署 | ✅ 已修 (2026-02-20) |
| 2 | **Tracker 只下載 1 個音訊** | 新生成的集數沒有中文音訊 | 待修 |
| 3 | **EP001 中文 Podcast 0-byte** | 需重新生成 | 待修 |

### 5.2 Important

| # | 問題 | 影響 | 狀態 |
|---|------|------|------|
| 4 | EP008/EP010 缺 steps 2,3,4 | 需 requeue（>2天自動觸發） | 待 requeue |
| 5 | EP009/EP011/EP013 podcast=failed | 需重新生成 podcast | 待 requeue |
| 6 | EP007 中文 Podcast 14MB（偏小） | 品質可能不佳 | 待確認 |
| 7 | EP012 只有英文 podcast，無中文 | 需補生成中文版 | 待修 |
| 8 | Video Overview 全部 skipped | NotebookLM Video 未正確生成/下載 | 待查 |
| 9 | Step 5（逐字稿）未實作 | 無 transcript 功能 | 待開發 |

### 5.3 已修復（2026-02-20）

| # | 修復 | 說明 |
|---|------|------|
| A | CDP 下載行為 | 新增 `Browser.setDownloadBehavior` 才能下載 |
| B | More 按鈕選錯 | 用 JS 定位 audio_magic_eraser 旁的按鈕 |
| C | 檔案覆寫偵測 | 追蹤 mtime 而非只看檔名 |
| D | State 保存順序 | 先寫 state 再 deploy，deploy 用 try/except |
| E | git push timeout | 30s → 120s |
| F | requeue 邏輯 | 加 `topic["status"] = "pending"` |
| G | Slide retry | 3 次重試，30s/60s 退避 |
| H | File logging | pipeline/tracker/audit 都寫 /var/log/ai-hub/ |

---

## 6. 待開發功能

### 6.1 P0 — 立即

#### ~~6.1.1 中文 Podcast 部署（EP002-EP007）~~ ✅ 已完成 (2026-02-20)
- ✅ 已將 `podcast_zh.m4a` 複製到 `website/assets/audio/EPXXX/`
- ✅ 已在 front matter 加入 `podcast_zh: podcast_zh.m4a`
- ✅ git commit + push 完成

#### 6.1.2 Podcast Tracker 雙語下載
- Studio 中有多個 `audio_magic_eraser` 項目
- 需要下載**全部**音訊項目，根據檔名/語言分類
- 英文 → `podcast.m4a`，中文 → `podcast_zh.m4a`
- Deploy 函式需同時處理兩個檔案 + 更新 front matter

#### 6.1.3 EP001 中文 Podcast 重新生成
- 上次生成 0-byte（NotebookLM 額度耗盡）
- 需重新從 notebook 生成

### 6.2 P1 — 本週

#### 6.2.1 Video Overview 修復
- 目前全部 episode 的 video_overview_status = skipped
- NotebookLM 有生成 Video Overview 的能力（Step 7 in provider）
- 需確認 provider 是否正確觸發 Video 生成
- Tracker 需正確下載 Video（subscriptions 項目 + More → 下載）

#### 6.2.2 失敗 Episode 重新處理
- EP009, EP011, EP013: podcast=failed → 需 requeue
- EP008, EP010: steps 缺 2,3,4 → pipeline requeue（>2天自動觸發）
- 手動觸發或等待明日 pipeline 自動 requeue

### 6.3 P2 — 本月

#### 6.3.1 最新永續動態報導
- **目標**：在網站加入「最新動態」專區，自動抓取並摘要台灣/國際永續相關新聞
- **資料來源**：
  - 環境部公告、碳費相關法規更新
  - 國際碳市場動態（EU ETS、CBAM）
  - 台灣企業 ESG 新聞
  - SBTi、TCFD、ISSB 等框架更新
- **實作方向**：
  - 每日或每週自動抓取 RSS / 新聞源
  - LLM 摘要 + 分類（法規、市場、技術、企業）
  - 生成 Markdown 頁面部署到網站
  - 可選：搭配 AI 生成的 Podcast 動態摘要
- **狀態**：規劃中，尚未開始

#### 6.3.2 Step 5 逐字稿（Transcript）
- **方案 A**：Qwen3-TTS on ac-3090 — 將 research.md 轉為中文語音
- **方案 B**：Whisper — 將 podcast.m4a 轉為逐字稿文字
- **方案 C**：NotebookLM 本身的文字摘要
- ac-3090 目前 GPU 閒置（363 MiB / 24576 MiB），可部署 TTS/Whisper
- **狀態**：待評估

#### 6.3.3 研究品質提升
- 雙 LLM 交叉驗證（Groq + Gemini 對比）
- 事實查核自動化（EP003-EP007 已有 verification.json）
- 引用來源標注

#### 6.3.4 網站功能擴充
- 搜尋功能
- 系列導覽頁面
- RSS Feed（Podcast 標準格式）
- 訪客統計（Google Analytics）

---

## 7. 檔案結構

### 7.1 內容目錄結構
```
/usr/local/bin/ai-hub/content/sustainability100/
├── topics.json                    # 100 講主題定義
├── sustainability100.py           # 主 pipeline
├── EP001/
│   ├── state.json                 # 執行狀態
│   ├── research.md                # Step 1 研究報告
│   ├── verification.json          # 事實查核
│   ├── podcast.m4a                # EN podcast（或唯一版本）
│   ├── podcast_zh.m4a             # ZH podcast（若有）
│   ├── podcast_en.m4a             # EP001 特例
│   ├── video_script.txt           # Step 3 影片腳本
│   ├── slides.json                # Step 4 簡報定義
│   └── slides/
│       ├── slide1.png ~ slide4.png
│       └── slide1.txt ~ slide4.txt
├── EP002/ ...
└── EP100/ ...
```

### 7.2 網站 Repo 結構
```
/home/ac-mac/sustainability-100/
├── _config.yml
├── _layouts/
│   ├── default.html
│   ├── episode.html               # 支援雙語 podcast + video
│   └── home.html
├── _episodes/
│   ├── EP001.md ~ EP013.md        # 已生成的 episode 頁面
│   └── ...
├── assets/
│   ├── audio/EP001/ ~ EP015/      # podcast 音訊
│   ├── video/EP001/ ~ EP010/      # video overview
│   └── slides/EP001/ ~ EP013/     # 簡報圖片
└── index.html
```

### 7.3 state.json 欄位
```json
{
  "steps_completed": [1, 2, 3, 4, 6, 7],
  "job_ids": {"podcast": "uuid", "video": "uuid"},
  "podcast_status": "completed|generating|failed|download_failed|pending",
  "podcast_notebook_url": "https://notebooklm.google.com/notebook/...",
  "podcast_audio_path": "/path/to/podcast.m4a",
  "podcast_started_at": 1771596115.0,
  "video_overview_status": "completed|generating|skipped|download_failed",
  "video_overview_path": "/path/to/video_overview.mp4"
}
```

---

## 8. 操作指南

### 8.1 手動觸發 Pipeline
```bash
# 執行當日 pipeline（處理 2 集）
ssh ac-mac "sudo systemctl start ai-hub-pipeline.service"

# 查看進度
ssh ac-mac "python3 /usr/local/bin/ai-hub/content/sustainability100/sustainability100.py --check"

# 查看 log
ssh ac-mac "tail -50 /var/log/ai-hub/pipeline.log"
```

### 8.2 手動觸發 Podcast Tracker
```bash
# 檢查生成中的 podcast 並嘗試下載
ssh ac-mac "cd /usr/local/bin/ai-hub/automations && python3 podcast_tracker.py"

# 查看 log
ssh ac-mac "tail -30 /var/log/ai-hub/podcast-tracker.log"
```

### 8.3 手動觸發巡檢
```bash
ssh ac-mac "cd /usr/local/bin/ai-hub/automations && python3 pipeline_audit.py"
```

### 8.4 重設失敗 Episode
```python
# SSH 到 ac-mac 後執行
import json
state = json.loads(open("/usr/local/bin/ai-hub/content/sustainability100/EPXXX/state.json").read())
state["podcast_status"] = "pending"
state["podcast_done"] = False
open("/usr/local/bin/ai-hub/content/sustainability100/EPXXX/state.json", "w").write(
    json.dumps(state, ensure_ascii=False, indent=2))
```
