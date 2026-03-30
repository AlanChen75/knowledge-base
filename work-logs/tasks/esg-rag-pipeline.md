---
title: ESG RAG Pipeline — 完整任務追蹤
status: ✅ 完成 (API 上線)
priority: high
---

## 目標
建立台灣 ESG 永續報告書 RAG 查詢系統：PDF 下載 → OCR → 比對 → 向量化 → API

## 完成時間軸

### Phase 1: 資料收集 (3/11-3/16)
- esggenplus.twse.com.tw API 發現（公開，無需認證）
- 2024 年 1,893 份報告書 PDF 下載
- 2023 年 1,077 份報告書 PDF 下載
- 7 套永續標準下載 (472 份 PDF, 471MB)
  - GRI 39, IFRS 6, SASB 77, GHG 78+248會議記錄, SBTi 10, CDP 10, 台灣 4

### Phase 2: OCR Pipeline (3/15-3/21)
- 4 套 OCR 引擎: PaddleOCR, Surya v4, Marker, GOT-OCR v2
- ac-3090 (RTX 3090) + ac-4090 (RTX 4090 D) 平行處理
- 關鍵修復:
  - v2→v3: 假分批 (load_from_file 一次載入全部) → v4 真分批 (page_range)
  - Marker glibc corruption → jemalloc LD_PRELOAD
  - GOT AutoModel → AutoModelForImageTextToText
  - VRAM cleanup: gc.collect() + torch.cuda.empty_cache() 每 20 PDF
- 2024 結果: Paddle 1894, Surya 1894, Marker 1877 成功
- 2015-2022 結果: 每年 ~10% 成功 (舊 PDF 大多損壞)

### Phase 3: Cross-Compare (3/19-3/25)
- normalize + cross_compare_v2 + extract_disputes
- 2024: 1,893 merged, 13.7% conflict rate (452,780 爭議)
- 2015-2022: 204 merged

### Phase 4: RAG DB (3/21-3/25)
- Embedding: BAAI/bge-m3 (1024維) on GPU
- ChromaDB: 506,667 chunks
  - esg_reports: 441,710 (2015-2024)
  - esg_standards: 64,957 (472 份標準)
- 建置耗時: ~2.5hr on ac-3090 GPU

### Phase 5: API 上線 (3/25)
- FastAPI v4 on macmini2:8900
- bge-m3 CPU embedding (query ~4.5s)
- Gemini 2.0 Flash LLM
- 驗證: 台積電碳排放查詢成功

## 系統架構
```
[esggenplus API] → [PDF 下載] → [3 OCR engines] → [cross-compare]
                                                          ↓
[macmini2 API:8900] ← [ChromaDB 506K chunks] ← [bge-m3 向量化]
       ↓
  [Gemini Flash] → 自然語言回答
```

## 檔案位置
| 位置 | 路徑 |
|------|------|
| PDF 原檔 | ac-3090: ~/esg-reports/{year}/twse/*.pdf |
| OCR Paddle | ac-3090: ~/esg-reports/ocr_paddle/{year}/*.json |
| OCR Surya | ac-3090: ~/esg-reports/ocr/{year}/*.json |
| OCR Marker | ac-3090: ~/esg-reports/ocr_marker/{year}/*.md |
| OCR GOT | ac-3090: ~/esg-reports/ocr_got/2024/*.json (背景跑) |
| Merged | ac-3090: ~/esg-reports/ocr_merged/{year}/*.json |
| Disputes | ac-3090: ~/esg-reports/disputes/{year}/*.json |
| Standards | ac-3090: ~/esg-reports/standards/{gri,ifrs,sasb,ghg,...}/ |
| ChromaDB | macmini2: ~/esg-rag/chromadb/ (6.5GB) |
| API | macmini2: ~/esg-rag/rag_api.py |
| API 啟動 | macmini2: ~/esg-rag/start_rag.sh |
| 下載腳本 | ac-3090: ~/esg-reports/bulk_download.py |
| Smart 爬蟲 | ac-3090: ~/esg-reports/smart_download_v2.py |

## API 使用
```bash
# 健康檢查
curl http://100.118.162.26:8900/health

# 查詢 (不用 LLM，直接回傳檢索結果)
curl -X POST http://100.118.162.26:8900/query \
  -H "Content-Type: application/json" \
  -d '{"question":"台積電碳排放量","stock_id":"2330","top_k":5,"use_llm":false}'

# 查詢 (用 Gemini 生成回答)
curl -X POST http://100.118.162.26:8900/query \
  -H "Content-Type: application/json" \
  -d '{"question":"台積電碳排放量","stock_id":"2330","top_k":5}'

# 公司 vs 標準比對
curl -X POST http://100.118.162.26:8900/compare \
  -H "Content-Type: application/json" \
  -d '{"stock_id":"2330","standard":"GRI-305"}'
```

## 待處理
- [ ] Gemini 爭議仲裁 (452K disputes, macmini2 gemini_dispute_resolver.py)
- [ ] GOT-OCR 背景跑完 (~22天)
- [ ] 舊年份報告書更多來源 (Wayback Machine?)
- [ ] API systemd 服務化 (開機自動啟動)
- [ ] 2025 年報告書自動更新機制
