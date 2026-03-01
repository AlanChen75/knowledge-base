---
title: 永續100講 — 英文/中文 Podcast 逐字稿功能
status: pending
priority: medium
created: 2026-02-23
---

# 英文/中文 Podcast 逐字稿

## 需求
- 每集附上英文 podcast 逐字稿（EN transcript）
- 每集附上中文 podcast 逐字稿（ZH transcript）
- 發布到網站上，讓使用者可以閱讀

## 技術方案（待設計）

### 英文逐字稿
- 來源：NotebookLM 生成的 EN podcast (podcast.m4a)
- 方案 A：Whisper STT（ac-3090 本機，免費）
- 方案 B：Google Cloud Speech-to-Text API
- 方案 C：NotebookLM 是否自帶 transcript？（需確認）

### 中文逐字稿
- 來源：Qwen3-TTS 生成的中文 podcast (EP*.wav)
- 中文音檔直接由文字稿生成，所以逐字稿 = 原始 script
- 可直接使用 /tmp/podcast_scripts/EP*.txt 作為逐字稿
- 不需要 STT，只需要格式化並上傳

### 網站整合
- 在 _episodes/EP*.md front matter 加入 transcript_en / transcript_zh 欄位
- 網站 UI 新增逐字稿顯示區域（可折疊）
- 或獨立頁面 /episodes/EP001/transcript/

## 待決定
- [ ] 確認 NotebookLM 是否提供原生 transcript
- [ ] 選擇 STT 方案（Whisper vs API）
- [ ] 設計網站 UI 顯示方式
- [ ] 決定是否加入 pipeline 自動化（新 step 5）
