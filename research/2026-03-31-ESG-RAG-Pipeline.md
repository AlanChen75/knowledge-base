---
title: 台灣 ESG 永續報告書 RAG 查詢系統 — 從 PDF 到 AI 問答
date: 2026-03-31
source: AI Sustainability Platform 專案
category: research
tags: ESG, OCR, RAG, ChromaDB, bge-m3, Gemini, 永續報告書, Taiwan
---

## 系統概述

建立台灣上市櫃公司 ESG 永續報告書的 RAG (Retrieval-Augmented Generation) 查詢系統。
涵蓋 2015-2024 年共 ~7,300 份報告書 + 472 份國際永續標準文件。

## 架構

```
[esggenplus.twse.com.tw API] → [PDF 批量下載]
         ↓
[3 套 OCR 引擎: PaddleOCR + Surya + Marker]
         ↓
[Cross-Compare 三引擎比對] → [爭議清單]
         ↓
[bge-m3 Embedding 向量化] → [ChromaDB 506K chunks]
         ↓
[FastAPI on macmini2:8900] → [Gemini 2.0 Flash 回答]
```

## 關鍵數據

| 指標 | 數值 |
|------|------|
| PDF 報告書 | 2015-2024 年共 ~7,300 份 |
| 有效 OCR | 2024: 1,893 份 (100%), 2015-2022: ~204 份 (~10%) |
| 永續標準 | 472 份 (GRI 39, IFRS 6, SASB 77, GHG 78+248, SBTi 10, CDP 10, 台灣 4) |
| 向量 DB | 506,667 chunks (441,710 reports + 64,957 standards) |
| Embedding | BAAI/bge-m3 (1024維, 多語言) |
| 查詢延遲 | ~4.5 秒 (CPU embedding + ChromaDB search) |

## API 使用方式

```bash
# 基本查詢
curl -X POST http://100.118.162.26:8900/query \
  -H "Content-Type: application/json" \
  -d '{"question":"台積電碳排放量","stock_id":"2330","top_k":5}'

# 公司 vs 標準比對
curl -X POST http://100.118.162.26:8900/compare \
  -H "Content-Type: application/json" \
  -d '{"stock_id":"2330","standard":"GRI-305"}'
```

## 技術發現

### esggenplus API 是公開的
- `esggenplus.twse.com.tw/api/api/MopsSustainReport/data` — 無需認證
- 2023+ 用 FileStream 直接下載 PDF (100% 成功率)
- 2022 以前用公司網站連結 (大量失效，~10% 成功率)

### OCR 引擎比對
- PaddleOCR: 最快 (~51/hr), 但有 VRAM leak
- Surya: 最穩 (~40/hr), 需要分批載入 (page_range)
- Marker: PDF→Markdown, 結構最好, 但 glibc corruption 需用 jemalloc
- GOT-OCR: 最慢 (~7/hr), autoregressive 模型限制

### VRAM 管理教訓
- 必須 gc.collect() + torch.cuda.empty_cache() 每 20-50 PDF
- 超大 PDF (200+ 頁) 必須用 load_from_file(page_range=) 真正分批載入
- Marker 必須用 LD_PRELOAD=libjemalloc.so 避免 glibc double-linked list corruption
- 3090 (31GB RAM) 容易 OOM, 4090 (91GB RAM) 穩定得多

## 機器分工

| 機器 | 角色 |
|------|------|
| ac-3090 (RTX 3090) | OCR 引擎 + cross-compare + RAG build |
| ac-4090 (RTX 4090 D) | Marker OCR + embedding proxy |
| macmini2 | RAG DB 存放 + API 服務 (ChromaDB + Gemini) |

## 待處理

- Gemini 爭議仲裁 (452K disputes)
- GOT-OCR 背景跑完 (~22天)
- 舊年份報告書更多來源
- API systemd 服務化
- 2025 年報告書自動更新
