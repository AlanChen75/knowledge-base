# AI100 新聞 Pipeline v2 技術筆記

## 架構
```
RSS Sources (7個) → 時間排序 → Gemini 思考型分析+驗證 → 圖片生成 → Jekyll post → Git push → TG 通知
```

## 摘要生成
- **Provider**: Gemini Chat (思考型模型)，非 Groq
- **Chrome profile**: gemini-chat (port 9226)
- **思考型切換**: `_ensure_thinking_model()` 透過 JS evaluate 找 button text
- **Timeout**: 180s（思考型較慢，30-40s/篇）
- **驗證指令**: Prompt 要求「請先用搜尋能力驗證新聞真實性」
- **verified 欄位**: true/false，false 觸發 log WARNING + TG ⚠️

## 圖片生成
- **Provider**: Gemini Image (思考型模型)
- **Prompt 語言**: 中文（含繁體中文標題）
- **參數**: `title_zh` 傳入完整中文標題
- **queue_timeout**: 120s（避免 Chrome 佔用衝突）

## RSS 來源排序
- `articles.sort(key=parse_pub_time, reverse=True)` 最新優先
- `parse_pub_time()` 支援 RFC 2822 + ISO 8601 雙格式
- `parsedate_to_datetime` 不支援 ISO 8601，需 `datetime.fromisoformat` fallback

## 排程
- Cron: `5 9,13,18 * * *`
- 每次最多 3 篇，每天最多 9 篇
- Cron 需 `set -a && . /usr/local/bin/ai-hub/.env && set +a` 載入環境變數

## 已知限制
- Gemini 思考型查證不完美：會自我矛盾（先寫錯數據再自己糾正）
- 不能 100% 信任 verified=true，需人工抽查
- gemini-chat Chrome 重啟後需等 ~10s 才能 CDP 連線
- Chrome 「正於現有瀏覽器工作階段中開啟」= 另一個 Chrome 已佔用 profile，需先 pkill

## 監控
- Log: `/var/log/ai-hub/ai100-news.log`
- 巡檢: `grep '未驗證' /var/log/ai-hub/ai100-news.log`
- TG 通知: 每次 pipeline 完成後自動發送，含 ✅/⚠️ 標記
