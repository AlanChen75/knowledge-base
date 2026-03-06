# AI Hub Firefox Session Management

## 版本說明 (2026-03-05 更新)

### 兩個 Firefox

| Firefox | 版本 | 用途 | 路徑 |
|---------|------|------|------|
| **Snap Firefox** (桌面版) | 148.0 | 用戶手動登入 Google 帳號 | `/snap/firefox/current/usr/lib/firefox/firefox` |
| **Playwright Firefox** (自動化) | 146.0.1 | AI Hub 自動操作 Gemini / NotebookLM | `~/.cache/ms-playwright/firefox-1509/firefox/firefox` |

### 關鍵限制

1. **Playwright 不能控制 Snap Firefox** — Snap Firefox 148 不支援 Playwright 的 juggler-pipe 協議
2. **Playwright Firefox 不能直接手動登入** — 它是 headless-first 設計，無法像普通瀏覽器操作
3. **兩者的 profile 格式不完全相容** — 不能直接複製整個 profile（會出現「舊版 Firefox」錯誤）
4. **但 cookies 檔案是相容的** — 可以從 Snap Firefox 複製 cookies.sqlite 等檔案到 Playwright profile

## Session 工作流程

### 正常運作流程

```
Snap Firefox 148 ──手動登入──> Google 帳號 (d11351004@gmail.com)
        |
        | 複製 session 檔案
        v
Playwright Firefox 146 ──自動操作──> Gemini Pro / NotebookLM
        |
        | launch_persistent_context()
        v
AI Hub Firefox Profile ──持久化──> /usr/local/bin/ai-hub/state/firefox-profiles/
```

### 何時需要重新登入

- **系統重開機後** — Snap Firefox 的 Google session 會過期
- **Idle shutdown 後** — FirefoxManager 在閒置 1200 秒 (20 分鐘) 後關閉 Firefox，session 可能失效
- **Cookie 過期** — Google cookies 有效期不定，通常幾小時到幾天

### 重新登入步驟

1. **在 Snap Firefox 中手動登入 Google**
   - 開啟桌面 Snap Firefox（需要 AnyDesk 遠端桌面或 DISPLAY=:0）
   - 前往 https://gemini.google.com/app
   - 使用 .env 中的帳號密碼登入：
     - Email: GOOGLE_EMAIL (d11351004@gmail.com)
     - Password: GOOGLE_PASSWORD
   - 確認已登入（看到 PRO 標誌）

2. **停止 AI Hub**
   ```bash
   sudo systemctl stop ai-hub
   ```

3. **複製 session 檔案到所有 Firefox profiles**
   ```bash
   SNAP_PROFILE="/home/ac-mac/snap/firefox/common/.mozilla/firefox/8oxk9x2z.default"
   PROFILES_DIR="/usr/local/bin/ai-hub/state/firefox-profiles"
   FILES="cookies.sqlite cookies.sqlite-wal cookies.sqlite-shm webappsstore.sqlite webappsstore.sqlite-wal webappsstore.sqlite-shm cert9.db key4.db"

   for profile in firefox-gemini firefox-gemini-chat firefox-gemini-audio firefox-notebooklm; do
       DEST="$PROFILES_DIR/$profile"
       for f in $FILES; do
           [ -f "$SNAP_PROFILE/$f" ] && sudo cp "$SNAP_PROFILE/$f" "$DEST/$f"
       done
       [ -d "$SNAP_PROFILE/storage" ] && sudo rsync -a "$SNAP_PROFILE/storage/" "$DEST/storage/"
       sudo rm -f "$DEST/lock" "$DEST/.parentlock"
       sudo chown -R ac-mac:ac-mac "$DEST"
   done
   ```

4. **啟動 AI Hub**
   ```bash
   sudo systemctl start ai-hub
   ```

5. **驗證**
   ```bash
   curl -s -X POST http://localhost:8760/api/image/generate \
     -H 'Content-Type: application/json' \
     -d '{"prompt": "test blue circle", "timeout": 90}'
   ```

## Firefox Profile 清單

| Profile | Queue Key | 用途 | 共用 |
|---------|-----------|------|------|
| firefox-gemini | firefox-gemini | 生圖 (gemini_image) + 生影片 (gemini_video) | 同一 Firefox |
| firefox-gemini-chat | firefox-gemini-chat | LLM 對話 + Vision 分析 | 獨立 |
| firefox-gemini-audio | firefox-gemini-audio | 音樂生成 (gemini_audio) | 獨立 |
| firefox-notebooklm | firefox-notebooklm | Podcast + Video Overview | 同一 Firefox |

## Cookie 注入機制 (自動)

FirefoxManager 在建立 persistent context 時自動注入 cookies：

```python
# firefox_manager.py get_instance()
context = await pw.firefox.launch_persistent_context(profile_dir, ...)
cookies = self.load_google_cookies()  # 從 Snap Firefox cookies.sqlite 讀取
if cookies:
    await context.add_cookies(cookies)
```

- `load_google_cookies()` 讀取 Snap Firefox 的 `cookies.sqlite`
- 只讀取 `%google%` 域名的 cookies
- 跳過已過期的 cookies
- 如果 Snap Firefox 的 session 過期，注入的 cookies 也無效

## 重要注意事項

- **只複製 session 檔案，不要複製整個 profile** — Playwright Firefox 146 和 Snap Firefox 148 的 profile 格式不完全相容
- **複製前必須停止 AI Hub** — 否則 Firefox 持有 lock，檔案會衝突
- **刪除 lock 和 .parentlock** — 複製後要刪除這兩個檔案，否則 Playwright 無法啟動
- **Snap Firefox 必須處於登入狀態** — cookies 來源是 Snap Firefox，如果它沒登入，cookies 就無效

## 已知問題

1. **gemini_audio 在 Pro 帳號上無法完成生成** — 停止按鈕一直顯示，但從不產生音訊預覽。免費帳號可以正常使用。可能是 Pro 帳號的 UI 差異或限制。狀態：待調查。

2. **Playwright 不能控制 Snap Firefox** — executable_path 參數無效。Snap Firefox 148 不支援 -juggler-pipe 協議。意味著無法用 Playwright 自動登入 Snap Firefox。

3. **Profile 版本不相容** — 不能複製整個 profile 目錄。只能複製 cookies/session 相關檔案。複製整個 profile 會導致「舊版 Firefox」對話框。
