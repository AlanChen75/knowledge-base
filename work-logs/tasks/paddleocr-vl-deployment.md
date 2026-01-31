---
title: PaddleOCR-VL-1.5 部署到 ac-3090
created: 2026-01-31
status: pending
priority: medium
machine: ac-3090
---

# PaddleOCR-VL-1.5 部署任務

## 目標
在 ac-3090 (RTX 3090) 上部署百度最新發布的 PaddleOCR-VL-1.5 文件視覺語言模型

## 模型資訊

### 基本規格
- **模型大小**: 0.9B 參數
- **架構**: NaViT 動態高解析度視覺編碼器 + ERNIE-4.5-0.3B 語言模型
- **準確率**: OmniDocBench v1.5 達 94.5%，Real5-OmniDocBench 達 92.05%
- **語言支援**: 111 種語言
- **輸出格式**: 結構化 Markdown 與 JSON

### 核心能力
- 文字辨識（OCR）
- 表格解析
- 數學公式辨識
- 圖表分析
- 印章識別
- 文字定位
- 兩階段流程：版面分析（PP-DocLayoutV3）→ 元素識別

### 效能對比
- 推理速度比 MinerU 2.5 快 14%
- 推理速度比 dots.ocr 快 2 倍以上
- 在文件解析任務上不遜於 Qwen3-VL (235B)

### 真實場景支援（Real5-OmniDocBench）
1. 掃描瑕疵
2. 傾斜文件
3. 彎曲文件
4. 螢幕翻拍
5. 光照不均

## 進度

- [ ] 查找官方模型發布頁面與 GitHub repo
- [ ] 下載模型檔案與依賴
- [ ] 在 ac-3090 上建立 Python 環境
- [ ] 安裝 PaddlePaddle 與相關套件
- [ ] 下載測試文件樣本
- [ ] 執行基準測試
- [ ] 與現有 OCR 方案（MinerU、Tesseract）對比
- [ ] 記錄效能數據與使用心得

## 工作紀錄

### 2026-01-31 Session c44476a7
- [13:31] 建立任務追蹤檔案
- 待開始：查找官方資源

## 相關檔案
- （待補充部署後的設定檔路徑）

## 資源連結
- **官方發布**:（待補充）
- **GitHub**:（待補充）
- **論文/Blog**:（待補充）

## 注意事項
- RTX 3090 (24GB VRAM) 應足夠運行 0.9B 模型
- 需確認是否支援 CUDA 11.x / 12.x
- 可能需要安裝特定版本的 PaddlePaddle
