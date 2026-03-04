---
title: SHC (Super Happy Coder) 服務盤點與規劃
status: pending
priority: medium
created: 2026-03-03
---

# SHC 服務盤點與規劃

## 背景
SHC 原先配置的基礎設施已大幅變動，需要重新盤點服務架構再做完整規劃。

## 現況 (2026-03-03)

### 已停止的服務 (acmacmini2)
- [x] super-happy-coder.service — stopped + disabled
- [x] ssh-tunnel-3090-vllm.service — stopped + disabled (localhost:8000 → ac-3090:8000)
- [x] ssh-tunnel-3090-compute.service — stopped + disabled (localhost:9000 → ac-3090:9000)

### 停止原因
- ac-3090 vLLM (Qwen2.5-7B-Instruct) 自 2/17 已停，port 8000 被 Edit-Banana 佔用
- SHC HealthMonitor 每 30s 打到錯誤服務，導致 healthy↔degraded 反覆切換
- 持續發送假警報 Telegram 通知

### ac-3090 GPU 現況
- qwen3-tts.service: active, 9842MiB GPU
- ComfyUI: active, 256MiB GPU
- vllm.service: failed + disabled

### SHC 相關檔案 (acmacmini2)
- 服務定義: /etc/systemd/system/super-happy-coder.service
- 程式碼: /home/ac-macmini2/workshop/super-happy-coder/proxy.py
- SSH tunnel 定義:
  - /etc/systemd/system/ssh-tunnel-3090-vllm.service
  - /etc/systemd/system/ssh-tunnel-3090-compute.service

### SHC 功能模組 (需盤點)
- [ ] LLM Router (hybrid mode: vLLM + OpenAI fallback)
- [ ] HealthMonitor (vLLM 健康檢查 + Circuit Breaker)
- [ ] Compute Plane 整合 (ac-3090 GPU 推論)
- [ ] API endpoints (/api/v1/chat, /api/v1/compute/*)
- [ ] Telegram 告警回調

## 待辦
- [ ] 盤點 SHC proxy.py 完整功能清單
- [ ] 評估哪些功能仍需要、哪些已被 AI Hub 取代
- [ ] 確認 ac-3090 vLLM 是否需要重啟（vs Qwen3-TTS 共存）
- [ ] 決定 SHC 未來方向：重構 / 整合到 AI Hub / 淘汰
- [ ] 如需保留，更新 HealthMonitor 配置指向正確服務
