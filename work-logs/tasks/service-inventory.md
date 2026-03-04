---
title: 全系統服務盤點與清理
status: in_progress
priority: high
created: 2026-03-03
---

# 全系統服務盤點與清理

## 一、ac-3090 服務盤點

### 保留的服務
| 服務 | Port | GPU | 說明 | 狀態 |
|------|------|-----|------|------|
| qwen3-tts | 3003 (Tailscale) | 9842MiB | Qwen3-TTS 語音合成 API | running, enabled |
| fail2ban | — | — | SSH 入侵防護 | running, enabled |
| tailscaled | — | — | Tailscale VPN | running, enabled |
| ssh-monitor | — | — | SSH 登入監控 + TG 通知 | running, enabled |
| redis-server | 6379 (localhost) | — | Redis 快取 | running, enabled |
| anydesk | — | — | 遠端桌面 | running, enabled |

### 已停止/廢棄的服務
| 服務 | Port | 原用途 | 廢棄原因 | 處理日期 |
|------|------|--------|----------|----------|
| vllm | 8000 | Qwen2.5-7B LLM API | 被 Groq + Gemini Chat 取代 | 2/17 停止, 3/3 正式廢棄 |
| edit-banana | 8000 | Image/PDF→DrawIO/PPTX | 無開發價值，佔用 port 8000 | 3/3 停止 |
| comfyui | 8188 | Stable Diffusion 圖片生成 | 未成功上線，被 Gemini Image 取代 | 3/3 停止 |
| diagram-service | 8189 | Diagram 渲染 API | 未成功上線，被 Gemini Image 取代 | 3/3 停止 |
| compute-plane | 9000 | SHC GPU 推論 API | SHC 已停，無繼續價值 | 3/3 停止 |

### Cron 排程 (保留)
| 排程 | 說明 |
|------|------|
| 0 8 * * * | 每日系統報告 (daily-report.sh) |
| */5 * * * * | Tailscale 新裝置偵測 (tailscale-monitor.sh) |

---

## 二、ac-mac (AI Hub) 服務盤點

### AI Hub 核心 (保留)
| 服務 | Port | 說明 | 狀態 |
|------|------|------|------|
| ai-hub | 8760 | AI Service Hub 閘道 (FastAPI)，統一 image/video/LLM/TTS/STT/podcast/vision/web | running, enabled |
| ai-hub-funnel | — | Tailscale Funnel HTTPS 對外入口 | running, enabled |

### AI Hub Provider 模組 (活躍)
| Provider | 類型 | 後端 |
|----------|------|------|
| gemini_image_ff | 圖片生成 | Firefox cookie 注入 |
| gemini_chat_ff | LLM 對話 + Vision | Firefox cookie 注入 |
| gemini_video_ff | Veo 影片生成 | Firefox cookie 注入 |
| notebooklm_ff | Podcast 音訊 | Firefox cookie 注入 |
| notebooklm_video_ff | Podcast 影片 | Firefox cookie 注入 |
| web_fetcher_ff | 網頁擷取 (browser) | Firefox cookie 注入 |
| groq_llm | LLM (Llama 70B) | Groq API |
| google_tts | 文字轉語音 | Google TTS API |
| qwen3_tts | 語音合成 | ac-3090:3003 API |

### AI Hub Fallback Chains
| 類型 | Chain |
|------|-------|
| Image | gemini_image |
| Video | notebooklm_video -> gemini_video |
| LLM | groq_llm -> gemini_chat |

### AI Hub Automations
| 模組 | 說明 |
|------|------|
| podcast_tracker_ff | Podcast 完成追蹤 (timer 觸發) |
| sustainability_news | 永續新聞管線 |
| daily_news_digest | 每日新聞摘要 |
| daily_health_report | 每日健康報告 |
| pipeline_audit | 管線稽核 |
| s100_news_backfill | S100 新聞回補 |
| social_post_generator | 社群貼文生成 |

### 已停止/廢棄的服務 (ac-mac)
| 服務 | Port | 原用途 | 廢棄原因 | 處理日期 |
|------|------|--------|----------|----------|
| gemini-image-api | 8765 | 獨立 Gemini 生圖 API | 功能已被 AI Hub /api/image 完全涵蓋 | 3/3 停止 |
| chrome-ai@gemini | 9222 | Chrome Gemini profile | AI Hub v2.3.0 遷移到 Firefox | 3/3 停止 |
| chrome-ai@gemini-chat | 9226 | Chrome Gemini Chat profile | AI Hub v2.3.0 遷移到 Firefox | 3/3 停止 |
| chrome-ai@notebooklm | 9225 | Chrome NotebookLM profile | AI Hub v2.3.0 遷移到 Firefox | 3/3 停止 |

### 已棄用的 Provider (保留檔案不刪除)
| Provider | 說明 |
|----------|------|
| gemini_image/chat/video (Chrome 版) | 被 _ff 版取代 |
| notebooklm/notebooklm_video (Chrome 版) | 被 _ff 版取代 |
| bing_image, kling_video, vidu_video | v2.2.0 移除第三方 |

### ac-mac 其他保留服務
| 服務 | 說明 |
|------|------|
| tg-monitor-bot | Telegram Bot 監控中心 |
| tg-claude-bot | Telegram 知識庫 Bot |
| happy-coder | Happy Coder AI 助手 |
| n8n | 工作流自動化平台 |
| comfyui-tg-bot | ComfyUI TG Bot (待確認是否仍需要) |
| power-on-ac | 來電自動開機 |
| fail2ban | SSH 入侵防護 |
| tailscaled | Tailscale VPN |
| docker | Docker 容器引擎 |

### ac-mac Cron 排程
| 排程 | 說明 |
|------|------|
| 0 8 * * * | 每日系統報告 |

---

## 三、acmacmini2 服務盤點

### 保留的服務
| 服務 | 說明 |
|------|------|
| happy-coder | Happy Coder AI 助手 |
| ssh-monitor | SSH 登入監控 |
| fail2ban | SSH 入侵防護 |
| tailscaled | Tailscale VPN |

### 已停止的服務
| 服務 | 原用途 | 處理日期 |
|------|--------|----------|
| super-happy-coder | SHC Proxy (LLM Router + HealthMonitor) | 3/3 停止 |
| ssh-tunnel-3090-vllm | SSH tunnel localhost:8000 -> ac-3090:8000 | 3/3 停止 |
| ssh-tunnel-3090-compute | SSH tunnel localhost:9000 -> ac-3090:9000 | 3/3 停止 |

### Cron 排程
| 排程 | 說明 |
|------|------|
| 0 10 * * 2 | 法拍地圖週二更新 |

---

## 四、ac-rpi5 服務盤點

### 保留的服務
| 服務 | 說明 |
|------|------|
| fail2ban | SSH 入侵防護 |
| tailscaled | Tailscale VPN |
| docker | Docker (Workshop AI 教學平台) |
