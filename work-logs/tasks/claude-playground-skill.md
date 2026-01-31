---
title: Claude Playground Skill 開發
created: 2026-01-31
status: pending
priority: medium
---

# Claude Playground Skill 開發

## 目標
建立一個 Claude Code Skill，用於快速測試 Claude API 互動、實驗不同 prompt 策略、驗證模型回應品質。

## 背景
Claude Code Skills 提供專門化的功能模組，可透過 `/skill-name` 指令快速啟用。Playground Skill 將成為開發與測試 Claude API 的互動式工具。

## 進度
- [ ] 研究 Claude Playground 功能與使用場景
- [ ] 分析現有 Skills 架構（參考 knowledge-base、work-log 等）
- [ ] 設計 Skill 介面與參數
- [ ] 實作 SKILL.md 規格檔案
- [ ] 開發支援腳本（如需要）
- [ ] 撰寫使用範例與文件
- [ ] 測試與除錯
- [ ] 部署到 ~/.claude/skills/

## 功能需求分析

### 1. 核心功能
- **即時 API 測試**: 快速測試 Claude API 呼叫
- **Prompt 實驗**: 比較不同 prompt 的回應品質
- **參數調整**: 實驗 temperature、max_tokens、system prompt
- **回應分析**: 評估回應品質、token 使用量、成本

### 2. 使用場景
- 開發新的 Agent 系統時測試 prompt
- 驗證 Claude 模型對特定任務的理解
- 比較不同模型（Sonnet、Opus、Haiku）的效能
- 實驗 system prompt 對回應的影響
- 測試 Tool Use（Function Calling）功能

### 3. 可能的介面設計
```bash
# 基本測試
/playground "解釋量子糾纏"

# 指定模型與參數
/playground --model opus --temp 0.7 "寫一首詩"

# 比較模式
/playground --compare "同一個問題" # 同時測試 Sonnet/Opus/Haiku

# System prompt 實驗
/playground --system "你是物理學家" "解釋相對論"

# Tool use 測試
/playground --tools "weather,calculator" "計算明天的天氣溫度平方根"
```

### 4. 輸出格式
- **回應內容**: 完整的 Claude 回應
- **後設資料**:
  - 模型名稱與版本
  - Token 使用量（input/output/cache）
  - 成本估算
  - 回應時間
  - 品質評分（可選）

### 5. 進階功能（可選）
- **歷史記錄**: 保存測試結果到知識庫
- **A/B 測試**: 批次測試多個 prompt 變體
- **成本分析**: 累積成本追蹤
- **品質評分**: 自動評估回應品質
- **範本庫**: 常用 prompt 範本

## 技術架構

### Skill 檔案結構
```
~/.claude/skills/playground/
├── SKILL.md              # Skill 規格與指引
├── playground.py         # Python 腳本（如需要）
├── templates/            # Prompt 範本庫（可選）
└── results/              # 測試結果暫存（可選）
```

### SKILL.md 基本結構
```markdown
---
name: playground
description: Claude API 互動式測試與 Prompt 實驗工具
version: 1.0.0
author: Alan Chen
---

# Claude Playground Skill

## 功能
快速測試 Claude API、實驗 prompt 策略、驗證模型回應品質

## 使用方式
...

## 參數
...

## 範例
...
```

## 參考資源

### 現有 Skills
```bash
ls ~/.claude/skills/
# - conversation-search
# - daily-report
# - knowledge-base
# - service-deploy
# - system-check
# - work-log
```

### Claude API 文件
- Anthropic API Reference
- Model capabilities (Sonnet/Opus/Haiku)
- Tool Use (Function Calling)
- Prompt Engineering Guide

## 實作計劃

### Phase 1: 基礎版本（P0）
- [ ] 建立 SKILL.md 基本結構
- [ ] 實作單次 API 呼叫功能
- [ ] 顯示回應與 token 使用量
- [ ] 基本錯誤處理

### Phase 2: 參數化（P1）
- [ ] 支援 --model 參數
- [ ] 支援 --temp, --max-tokens 參數
- [ ] 支援 --system prompt
- [ ] 儲存測試結果

### Phase 3: 比較模式（P2）
- [ ] --compare 功能（多模型並行測試）
- [ ] 成本對比分析
- [ ] 品質評分機制

### Phase 4: 進階功能（P3）
- [ ] 範本庫整合
- [ ] 歷史記錄查詢
- [ ] A/B 測試批次執行
- [ ] Tool Use 測試支援

## 預期產出

1. **Skill 主檔案**: `~/.claude/skills/playground/SKILL.md`
   - 完整的 Skill 規格與使用指引
   - 支援多種測試模式

2. **支援腳本** (如需要): `~/.claude/skills/playground/playground.py`
   - API 呼叫邏輯
   - 結果解析與格式化

3. **使用文件**: `~/knowledge-base/tech/tools/claude-playground-skill-guide.md`
   - 完整使用指南
   - 最佳實踐與範例
   - 故障排除

4. **測試範例**: `~/knowledge-base/tech/tools/claude-playground-examples.md`
   - 各種使用場景範例
   - Prompt 工程技巧

## 整合考量

### 與現有系統整合
- **TG Bot**: 可透過 TG Bot 呼叫測試
- **Happy Coder**: 在 Claude Code Session 中使用
- **知識庫**: 測試結果可存入知識庫
- **成本追蹤**: 整合到 daily-claude-report

### 安全性
- API Key 管理（使用現有 .env）
- 成本上限控制（避免意外高額費用）
- 輸出清理（避免洩漏敏感資訊）

## 成功標準

- [ ] 可快速測試 Claude API（<10 秒執行）
- [ ] 支援至少 3 種模型（Sonnet/Opus/Haiku）
- [ ] 清晰顯示 token 使用量與成本
- [ ] 錯誤處理完善（API 失敗、超時等）
- [ ] 文件完整可供他人使用

## 工作紀錄

### 2026-01-31 Session c44476a7
- [15:12] 建立任務追蹤檔案
- [15:12] 規劃功能需求與實作計劃

## 備註
- 此 Skill 主要用於開發與測試，非正式生產工具
- 需注意 API 呼叫成本，避免無限制測試
- 可考慮整合到 SHC v5 作為 debug 工具
