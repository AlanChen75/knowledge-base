# SHC v5.0.1 系統狀態總結

> 最後更新：2026-01-31

## 系統版本

| 組件 | 版本 | 位置 |
|------|------|------|
| proxy.py | v5.0.1 | acmacmini2:/home/ac-macmini2/workshop/super-happy-coder/ |
| hybrid_orchestrator.py | v5.0.1 | 同上 |
| agent_creator.py | v5.0.1 | 同上（含 YAML retry + auto-approve） |
| output_analyzer.py | v1.0 | 同上 |
| output_delivery.py | v1.0 | 同上（GitHub + TG 推送） |
| dynamic_planner.py | v1.0 | 同上 |

## 已安裝依賴（acmacmini2）

| 套件 | 版本 | 用途 |
|------|------|------|
| Quarto | 1.6.42 | QMD → PPTX 渲染 |
| LibreOffice | 7.3.7.2 | PPTX → PDF → PNG 品質驗證 |
| python-pptx | latest | PPTX 後處理 |
| lxml | latest | XML 處理 |
| pdftoppm (poppler) | system | PDF → per-page PNG |

## 模組狀態

### 核心模組（手動維護）

| ID | 名稱 | 版本 | 狀態 | 備註 |
|----|------|------|------|------|
| M2 | 網站生成與部署 | 2.0 | ✅ 驗證通過 | 絕對路徑 + `. ~/.env` POSIX fix |
| M6 | 簡報製作（Quarto PPTX） | 2.0 | ✅ 驗證通過 | 3-Phase pipeline + 品質驗證 |
| M-SYS | 系統助教 Agent | 1.0 | ✅ 已部署 | 6 步驟自動修復 |

### 自動生成模組（AgentCreator）

| 模組 | 來源 | 狀態 |
|------|------|------|
| complex-query-automation | 模擬測試 | skills/ (auto-approved) |
| ecommerce-db-schema | 模擬測試 | skills/ (auto-approved) |
| express-rate-limit-module | 模擬測試 | skills/ (auto-approved) |
| flask-model-predictor | 模擬測試 | skills/ (auto-approved) |
| generate-openapi-yaml | 模擬測試 | skills/ (auto-approved) |
| google-sheet-error-handler | 模擬測試 | skills/ (auto-approved) |
| monthly-report-summary | 模擬測試 | skills/ (auto-approved) |
| nodejs-week1-automation | 模擬測試 | skills/ (auto-approved) |
| online-voting-system | 模擬測試 | skills/ (auto-approved) |
| restful-api-doc-generator | 模擬測試 | skills/ (auto-approved) |
| reusable-chat-system-architecture | 模擬測試 | skills/ (auto-approved) |
| sre-interview-prep | 模擬測試 | skills/ (auto-approved) |
| system-design-interview | 模擬測試 | skills/ (auto-approved) |

## M6 PPTX Pipeline 詳情

### 管線步驟
1. **plan_deck** (llm_structure) — 規劃簡報大綱 + 選擇模板
2. **generate_qmd** (coding_agent) — 生成 Quarto QMD 檔案
3. **compile** (shell) — 3-Phase 編譯：
   - Phase 1: build_template.py（建構模板）
   - Phase 2: quarto render --reference-doc（渲染）
   - Phase 3: postprocess.py（修補 Pandoc 遺漏）
4. **quality_check** (shell) — PPTX → PDF → PNG（per-page）
5. **llm_spot_check** (llm_classify) — LLM 抽檢品質
6. **deliver** (llm_summarize) — 回報結果

### 模板庫
- base-template.pptx（基礎模板）
- template-basic.pptx（一般簡報）
- template-rich.pptx（產品/技術）
- template-roadmap.pptx（時程規劃）
- template-01-corporate-navy.pptx（企業報告）

### 品質驗證流程
```
PPTX → LibreOffice(headless) → PDF → pdftoppm → per-page PNG → LLM 抽檢 2 頁
```
注意：LibreOffice --convert-to png 只匯出第一頁，必須走 PDF 中間格式

## M2 Web Deploy 詳情

### 修復歷程
1. `source ~/.env` → `. ~/.env`（POSIX 相容）
2. 相對路徑 → 絕對路徑 `/home/ac-macmini2/workshop/super-happy-coder/skills/web-deploy/deploy.sh`
3. 驗證從 agent executor cwd `/tmp/workspace-{id}` 成功部署

### 網站模板
- personal（HTML5 UP Dimension）
- company（Bootstrap Agency）
- product（Landing Page）
- portfolio（Freelancer）
- project（Editorial）
- event（Conference）

### 部署目標
- GitHub Pages: `https://ai-cooperation.github.io/workshop/{project-name}/`

## v5.0.1 新增功能

### P0: 固定→動態 Fallback
- 固定模組步驟失敗時，M-SYS 嘗試修復
- 修復仍失敗則 fallback 到 DynamicPlanner（攜帶已完成步驟 context）

### P1: 輸出交付（output_delivery.py）
- 執行產出 → git push 到 `ai-cooperation/workshop` repo
- 呼叫 Telegram Bot API 發送檔案連結
- 支援 PPTX、HTML、PDF 等任意檔案類型

### P2a: YAML 驗證重試
- AgentCreator 生成 YAML 後驗證格式
- 失敗時用 HIGH tier LLM 修正（最多 2 次重試）

### P2b: 高品質自動核准
- quality_score >= 0.9 自動核准到 skills/（跳過 _pending/）
- 核准後立即熱重載 AgentRegistry + 清除語義快取

## 測試結果

| 測試 | 日期 | 結果 |
|------|------|------|
| API 整合測試 | 2026-01-31 | 59/59 (100%) |
| 模擬測試 v1 | 2026-01-31 | 34/46 (73.9%) |
| 模擬測試 v2（P0/P1/P2 修復後）| 2026-01-31 | 46/46 (100%) |

## Git Commits

| 機器 | Hash | 訊息 |
|------|------|------|
| acmacmini2 | 4f857b7 | P0/P1/P2 fixes |
| acmacmini2 | fd03607 | v5.0.1: M6 Quarto PPTX pipeline + M2 absolute paths |
| ac-mac KB | 0655161 | work logs and KB |
| ac-mac KB | 9c1ea5c | static systems analysis + session 2 |
| ac-mac tests | c020e4a | test reports |

## 待辦事項

1. 重新跑模擬測試驗證 M6 新 pipeline 端到端
2. 部署 Phase 1 靜態開源系統作為教學案例
3. 設計真實交付物測試場景（網站+簡報+系統部署）
4. PPTX LLM 品質抽檢整合到 agent_executor
5. Telegram Bot /happy 命令整合

## ac-mac SSH Key 設定（2026-02-01）

### 雙帳號 SSH 設定

| Host alias | Key 檔案 | GitHub 帳號 | 用途 |
|-----------|----------|------------|------|
| github.com | ~/.ssh/id_ed25519 | AlanChen75 | 個人 repo（knowledge-base 等）|
| github-org | ~/.ssh/id_ed25519_github | ai-cooperation | 組織 repo（workshop 等）|

### SSH config (~/.ssh/config)
```
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes

Host github-org
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_github
    IdentitiesOnly yes
```

### 使用方式
- AlanChen75 repo: `git@github.com:AlanChen75/xxx.git`（預設）
- ai-cooperation repo: `git@github-org:ai-cooperation/xxx.git`
- 不需要 token，SSH key 認證無過期問題
