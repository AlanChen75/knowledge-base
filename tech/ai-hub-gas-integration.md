# AI Service Hub — GAS 整合指南

## 基本資訊

- **Hub URL (內網)**: `http://100.116.154.40:8760`
- **Hub URL (外網/GAS)**: `https://acmac-macmini.tail9feef3.ts.net`
- **API Key**: `G2WC***（見 ~/.env）`
- **認證方式**: Header `X-API-Key` 或 Query `?api_key=...`

## API 端點

| 端點 | 方法 | 說明 | 回應方式 |
|------|------|------|---------|
| `/api/image/generate` | POST | 圖片生成 (Gemini/Bing) | 同步 |
| `/api/video/generate` | POST | 影片生成 (Veo/Kling) | 非同步 (job_id) |
| `/api/tts/generate` | POST | 文字轉語音 | 同步 |
| `/api/stt/transcribe` | POST | 語音轉文字 | 同步 |
| `/api/podcast/generate` | POST | Podcast 生成 | 非同步 (job_id) |
| `/api/job/{job_id}` | GET | 查詢非同步任務 | — |
| `/api/status` | GET | 服務狀態 | — |
| `/api/quota` | GET | 額度查詢 | — |
| `/api/health` | GET | 健康檢查 (免驗證) | — |
| `/api/files/{cat}/{file}` | GET | 下載生成的檔案 | — |

## GAS 呼叫範例

### 共用 Helper

```javascript
var AI_HUB = "https://acmac-macmini.tail9feef3.ts.net";
var API_KEY = "G2WC***"; // 實際 key 見 ~/.env 的 AI_HUB_API_KEY

function aiHubRequest(endpoint, method, payload) {
  var options = {
    method: method || "get",
    headers: { "X-API-Key": API_KEY },
    contentType: "application/json",
    muteHttpExceptions: true,
  };
  if (payload) {
    options.payload = JSON.stringify(payload);
  }
  var resp = UrlFetchApp.fetch(AI_HUB + endpoint, options);
  return JSON.parse(resp.getContentText());
}
```

### 文字轉語音 (TTS)

```javascript
function textToSpeech(text, lang) {
  var data = aiHubRequest("/api/tts/generate", "post", {
    text: text,
    lang: lang || "zh-TW",
  });
  if (data.success) {
    Logger.log("音檔路徑: " + data.audio_path);
    // 如需取得音檔 binary:
    // var audioResp = UrlFetchApp.fetch(
    //   AI_HUB + "/api/files/audio/" + data.audio_path.split("/").pop(),
    //   { headers: { "X-API-Key": API_KEY } }
    // );
    // var blob = audioResp.getBlob();
  }
  return data;
}
```

### 圖片生成

```javascript
function generateImage(prompt) {
  // provider: "auto" (預設), "gemini", "bing"
  var data = aiHubRequest("/api/image/generate", "post", {
    prompt: prompt,
    provider: "auto",
    timeout: 90,
  });
  if (data.success) {
    Logger.log("圖片: " + data.image_path + " (" + data.provider_used + ")");
    // 下載圖片:
    // var imgResp = UrlFetchApp.fetch(
    //   AI_HUB + "/api/files/images/" + data.image_path.split("/").pop(),
    //   { headers: { "X-API-Key": API_KEY } }
    // );
    // var blob = imgResp.getBlob();
  }
  return data;
}
```

### 影片生成 (非同步)

```javascript
function generateVideo(prompt) {
  // 步驟 1: 提交任務
  var job = aiHubRequest("/api/video/generate", "post", {
    prompt: prompt,
    provider: "auto",
    timeout: 300,
  });
  Logger.log("Job ID: " + job.job_id);

  // 步驟 2: 輪詢結果 (影片需 2-5 分鐘)
  // 注意: GAS 有 6 分鐘執行限制，建議用 trigger 輪詢
  for (var i = 0; i < 20; i++) {
    Utilities.sleep(15000); // 每 15 秒查一次
    var status = aiHubRequest("/api/job/" + job.job_id, "get");
    Logger.log("Status: " + status.status);
    if (status.status === "completed") {
      Logger.log("影片: " + status.output_path);
      return status;
    } else if (status.status === "failed") {
      Logger.log("失敗: " + status.message);
      return status;
    }
  }
  return { status: "polling_timeout", job_id: job.job_id };
}
```

### Podcast 生成 (非同步)

```javascript
function generatePodcast(urls, topic) {
  var job = aiHubRequest("/api/podcast/generate", "post", {
    sources: urls, // 最多 3 個 URL
    topic: topic || "",
    timeout: 600,
  });
  Logger.log("Podcast Job: " + job.job_id);
  // 輪詢方式同 generateVideo，但 interval 建議 20s，timeout 更長
  return job;
}
```

### 查詢服務狀態

```javascript
function checkAIStatus() {
  var data = aiHubRequest("/api/status", "get");
  for (var name in data) {
    var info = data[name];
    var status = info.busy ? "BUSY" : info.healthy ? "READY" : "OFFLINE";
    Logger.log(name + ": " + status + " | " + info.today_used + "/" + info.daily_limit);
  }
  return data;
}
```

### 查詢額度

```javascript
function checkQuota() {
  return aiHubRequest("/api/quota", "get");
}
```

## 非同步任務處理建議

GAS 單次執行限制 6 分鐘，影片/Podcast 生成可能超過此限制。建議方案：

1. **觸發器輪詢**: 提交任務後存 job_id 到 PropertiesService，建立 time-based trigger 每分鐘檢查
2. **Webhook 回調**: 未來可在 Hub 加入 callback URL 支援

```javascript
// 範例: 用 PropertiesService + Trigger 處理非同步任務
function submitVideoJob() {
  var job = aiHubRequest("/api/video/generate", "post", {
    prompt: "a sunset timelapse over mountains",
  });
  PropertiesService.getScriptProperties().setProperty("pending_job", job.job_id);
  ScriptApp.newTrigger("checkPendingJob")
    .timeBased()
    .everyMinutes(1)
    .create();
}

function checkPendingJob() {
  var jobId = PropertiesService.getScriptProperties().getProperty("pending_job");
  if (!jobId) return;
  var status = aiHubRequest("/api/job/" + jobId, "get");
  if (status.status === "completed" || status.status === "failed") {
    Logger.log("Job done: " + JSON.stringify(status));
    PropertiesService.getScriptProperties().deleteProperty("pending_job");
    // 刪除 trigger
    ScriptApp.getProjectTriggers().forEach(function (t) {
      if (t.getHandlerFunction() === "checkPendingJob") {
        ScriptApp.deleteTrigger(t);
      }
    });
  }
}
```

## 每日額度

| 服務 | 每日限制 |
|------|---------|
| Gemini Image | 50 |
| Bing Image | 100 (15 快速 + 慢速無限) |
| Gemini Video | 10 |
| Kling Video | 6 |
| NotebookLM Podcast | 3 |
| Google TTS | 無限 |
| Whisper STT | 無限 |
