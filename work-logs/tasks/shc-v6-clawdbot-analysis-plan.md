---
title: SHC v6 增強計畫：Clawdbot 分析與任務完成度提升
created: 2026-01-31
status: pending
priority: high
---

# SHC v6 增強計畫：Clawdbot 分析與任務完成度提升

## 背景與目標

### 現況分析

**SHC v5 優勢**：
- ✅ 輕量可控：混合模式節省 70% 成本
- ✅ 彈性分配：動態規劃 + Agent Creator
- ✅ 高可用性：Circuit Breaker + 自動 fallback

**SHC v5 劣勢**：
- ❌ 任務完成度不足：模組執行經常不完整
- ❌ 缺乏深度推理：複雜任務分解能力弱
- ❌ 模組庫不足：新需求難以快速滿足

**Clawdbot/OpenClaw 優勢**（參考目標）：
- ✅ 任務完成度高：超乎用戶預期
- ✅ 多輪對話追蹤：session 管理完善
- ✅ 豐富 Skills 系統：開箱即用功能多
- ❌ Token 消耗大：缺乏成本控制

### 目標定位

**SHC v6 願景**：結合兩者優勢
- 保持輕量可控 + 成本優化（SHC v5）
- 提升任務完成度（學習 Clawdbot）
- 整合開源生態（GitHub + Skills）
- 適合個人/小型企業 MVP 快速部署

---

## Phase 1: Clawdbot 架構深度分析

### 1.1 GitHub 代碼分析

**分析目標**：
- [ ] Agent Runner 執行邏輯（claude-cli 整合方式）
- [ ] Session 管理機制（JSONL 格式、狀態追蹤）
- [ ] Context 處理策略（adaptive pruning、sub-agent trimming）
- [ ] Skills 系統架構（工具注入、依賴管理）
- [ ] 多輪對話處理（如何保持任務上下文）

**執行方式**：
```bash
# 在 ac-mac 上克隆 OpenClaw repo
cd ~/workshop
git clone https://github.com/clawdbot/clawdbot.git openclaw
cd openclaw

# 分析關鍵檔案
- src/agent/ — Agent 核心邏輯
- src/terminal/ — CLI 整合與輸出
- src/skills/ — Skills 系統
- src/session/ — Session 管理
- AGENTS.md — 架構文件
```

**分析重點**：
1. **Task Decomposition**：如何將複雜任務分解成子任務？
2. **Progress Tracking**：如何追蹤每個子任務的完成狀態？
3. **Error Recovery**：失敗時如何重試或調整策略？
4. **Context Management**：如何在多輪對話中保持上下文？
5. **Tool Injection**：Skills 如何動態注入到 Agent？

### 1.2 acmacmini2 Log 分析（可選）

如果部署 Clawdbot 到 acmacmini2：
```bash
# 安裝 OpenClaw
npm install -g openclaw

# 啟動 Gateway
openclaw gateway

# 執行測試任務並記錄
openclaw agent --task "建立一個簡單的 TODO API" --log-level debug

# 分析 session logs
cat ~/.openclaw/sessions/*.jsonl | jq '.'
```

**分析項目**：
- Input/Output 格式與結構
- 子任務分解邏輯
- Tool call 序列
- Token 使用模式
- 成功/失敗案例對比

---

## Phase 2: SHC v5 任務完成度問題診斷

### 2.1 現有問題分析

**問題 1：模組執行不完整**
- 症狀：M2 web-deploy 只執行部分步驟就結束
- 根因：MODULE.yaml 的 steps 是靜態列表，缺乏條件判斷與重試
- 影響：用戶需求未完全滿足

**問題 2：複雜任務分解能力弱**
- 症狀：DynamicPlanner 生成的 TodoList 過於簡化
- 根因：單次 LLM call 生成計劃，缺乏迭代細化
- 影響：實際執行時發現遺漏步驟

**問題 3：錯誤處理不足**
- 症狀：步驟失敗後直接停止，不嘗試修復
- 根因：缺乏 OutputAnalyzer 的自動修復機制
- 影響：小錯誤導致整個任務失敗

**問題 4：上下文傳遞斷裂**
- 症狀：後續步驟無法使用前面步驟的輸出
- 根因：steps 之間缺乏變數傳遞機制
- 影響：無法執行依賴前置結果的任務

### 2.2 數據收集

**執行基準測試**：
```bash
cd ~/super-happy-tests
python3 test_task_completion.py

# 測試案例（20 個，分 4 類）
# A 類：簡單任務（預期 100%）
#   - 建立檔案、修改設定、查詢資訊
# B 類：中等任務（預期 80%）
#   - 多步驟配置、簡單部署
# C 類：複雜任務（預期 60%）
#   - 完整專案建立、多服務整合
# D 類：超複雜任務（預期 40%）
#   - 需要多輪對話、動態調整策略
```

**記錄指標**：
- 完成率（各類別）
- 平均步驟數 vs 實際需要步驟數
- 失敗原因分類（步驟遺漏、錯誤未修復、上下文斷裂）
- Token 使用量

---

## Phase 3: SHC v6 核心增強設計

### 3.1 任務編排引擎升級（TaskOrchestrator）

**設計目標**：多輪迭代式任務執行

```python
class TaskOrchestrator:
    """任務編排引擎 - 多輪迭代直到完成"""

    def __init__(self, llm_router, max_iterations=10):
        self.llm_router = llm_router
        self.max_iterations = max_iterations

    async def execute_task(self, user_request: str, student_id: str):
        """
        主執行流程：
        1. 初始規劃：生成詳細 TodoList
        2. 執行循環：
           while not all_complete and iterations < max:
               - 執行下一個 pending 任務
               - 驗證輸出品質
               - 如果失敗：診斷問題 → 調整計劃
               - 如果成功：更新狀態 → 繼續
               - 檢查是否需要新增步驟
        3. 最終驗證：檢查用戶需求是否完全滿足
        4. 交付成果：產出物 + 執行報告
        """

        # Phase 1: 詳細規劃
        plan = await self._create_detailed_plan(user_request)

        # Phase 2: 迭代執行
        for iteration in range(self.max_iterations):
            # 執行下一個待處理任務
            result = await self._execute_next_task(plan)

            # 驗證結果
            if result.success:
                self._mark_complete(result.task_id)
            else:
                # 錯誤分析與修復
                await self._handle_failure(result)

            # 檢查是否全部完成
            if self._all_tasks_complete(plan):
                break

            # 動態調整計劃（可能新增步驟）
            await self._refine_plan(plan, result)

        # Phase 3: 最終驗證
        verification = await self._verify_completion(user_request, plan)

        return ExecutionReport(
            plan=plan,
            results=self.results,
            verification=verification,
            iterations=iteration + 1
        )
```

**關鍵特性**：
1. **多輪迭代**：不是一次性執行，而是持續到任務真正完成
2. **動態調整**：執行中發現問題可以修改計劃
3. **品質驗證**：每個步驟完成後檢查輸出是否符合預期
4. **錯誤恢復**：失敗後診斷問題並嘗試修復
5. **完成度檢查**：最終驗證用戶需求是否滿足

### 3.2 深度規劃器（DeepPlanner）

**問題**：現有 DynamicPlanner 單次 call LLM，計劃過於粗糙

**解決方案**：多輪對話細化計劃

```python
class DeepPlanner:
    """深度規劃器 - 多輪對話細化任務計劃"""

    async def create_plan(self, user_request: str) -> DetailedPlan:
        """
        多輪細化流程：
        1. 初步分解：大方向的步驟列表
        2. 可行性分析：檢查每個步驟的前置條件
        3. 細節補充：為每個步驟生成詳細執行指令
        4. 依賴梳理：建立步驟間的依賴關係
        5. 資源評估：估算 token/時間/成本
        """

        # Round 1: 初步分解
        initial_steps = await self._decompose_task(user_request)

        # Round 2: 為每個步驟細化
        detailed_steps = []
        for step in initial_steps:
            refined = await self._refine_step(step, context={
                'user_request': user_request,
                'previous_steps': detailed_steps,
                'available_skills': self.skills_catalog
            })
            detailed_steps.append(refined)

        # Round 3: 建立依賴關係
        dependency_graph = await self._build_dependencies(detailed_steps)

        # Round 4: 風險評估
        risks = await self._assess_risks(detailed_steps)

        return DetailedPlan(
            steps=detailed_steps,
            dependencies=dependency_graph,
            risks=risks,
            estimated_tokens=self._estimate_cost(detailed_steps)
        )
```

**與 Clawdbot 對比**：
- Clawdbot：多輪對話自然演進，高度依賴 claude-cli
- SHC v6：結構化多輪規劃，明確分解與細化階段

### 3.3 智慧重試與修復（SmartRecovery）

**問題**：步驟失敗後直接停止，浪費前面的工作

**解決方案**：分類錯誤並自動修復

```python
class SmartRecovery:
    """智慧錯誤恢復系統"""

    async def handle_failure(self, task: Task, error: Exception) -> RecoveryAction:
        """
        錯誤分類與處理：
        1. 暫時性錯誤（網路超時）→ 重試 3 次
        2. 配置錯誤（路徑不存在）→ 診斷並修正配置
        3. 邏輯錯誤（程式碼 bug）→ 用 HIGH tier LLM 修復
        4. 前置條件未滿足 → 補充缺少的步驟
        5. 不可恢復錯誤 → 標記失敗，繼續其他任務
        """

        error_type = self._classify_error(error)

        if error_type == "TRANSIENT":
            return RetryAction(max_attempts=3, backoff=True)

        elif error_type == "CONFIG":
            fix = await self._diagnose_config(task, error)
            return FixAndRetryAction(fix)

        elif error_type == "LOGIC":
            # 使用 HIGH tier LLM 修復程式碼
            fixed_code = await self.llm_router.call(
                tier="HIGH",
                prompt=f"修復以下錯誤：\n{error}\n\n程式碼：\n{task.code}"
            )
            return ReplaceAndRetryAction(fixed_code)

        elif error_type == "PREREQUISITE":
            # 補充缺少的前置步驟
            missing_steps = await self._identify_missing_prereqs(task, error)
            return InsertStepsAction(missing_steps, before=task)

        else:
            return SkipAction(reason=str(error))
```

### 3.4 上下文橋接（ContextBridge）

**問題**：步驟間無法共享變數與輸出

**解決方案**：建立執行上下文，類似 Clawdbot 的 session state

```python
class ExecutionContext:
    """任務執行上下文 - 步驟間資料共享"""

    def __init__(self):
        self.variables = {}  # 變數存儲
        self.outputs = {}    # 步驟輸出
        self.files = {}      # 產生的檔案

    def set(self, key: str, value: Any):
        """設定變數"""
        self.variables[key] = value

    def get(self, key: str) -> Any:
        """取得變數"""
        return self.variables.get(key)

    def store_output(self, step_id: str, output: Any):
        """儲存步驟輸出"""
        self.outputs[step_id] = output

    def get_output(self, step_id: str) -> Any:
        """取得前面步驟的輸出"""
        return self.outputs.get(step_id)

    def register_file(self, path: str, purpose: str):
        """記錄產生的檔案"""
        self.files[path] = {
            'created_at': datetime.now(),
            'purpose': purpose
        }

    def render_template(self, template: str) -> str:
        """支援步驟中的變數替換"""
        # 例如：執行 "git commit -m '{{commit_message}}'"
        return template.format(**self.variables)
```

**MODULE.yaml 範例（支援變數）**：
```yaml
name: web-deploy
steps:
  - id: clone_repo
    command: git clone {{repo_url}} /tmp/project
    outputs:
      - project_path: /tmp/project

  - id: install_deps
    command: cd {{project_path}} && npm install
    depends_on: [clone_repo]

  - id: build
    command: cd {{project_path}} && npm run build
    depends_on: [install_deps]
    outputs:
      - build_path: "{{project_path}}/dist"

  - id: deploy
    command: rsync -av {{build_path}} server:/var/www/
    depends_on: [build]
```

---

## Phase 4: 開源生態整合（GitHub Skills Hub）

### 4.1 設計目標

**願景**：Skills + Agent + 開源專案庫 = 快速 MVP 部署

**核心概念**：
1. **Skills 標準化**：與 Clawdbot/OpenClaw Skills 格式相容
2. **GitHub 整合**：自動從開源專案生成 Skills
3. **一鍵部署**：用戶只需描述需求，系統自動組裝方案

### 4.2 GitHub Skills Hub 架構

```
SHC v6 Skills 生態
├── Core Skills (內建)
│   ├── M1-M6 (現有模組)
│   └── M-SYS (助教 agent)
│
├── Community Skills (GitHub 導入)
│   ├── awesome-selfhosted/ → 200+ 自架服務 skills
│   ├── free-for-dev/ → 免費開發工具整合
│   └── project-based-learning/ → 學習專案模板
│
├── Auto-Generated Skills (AgentCreator++)
│   ├── 從 GitHub repo 自動分析生成
│   └── 支援 Dockerfile、docker-compose、scripts
│
└── Custom Skills (用戶自建)
    └── 個人/企業專屬模組
```

### 4.3 SkillsHub Agent

```python
class SkillsHubAgent:
    """Skills 生態管理與自動生成"""

    async def search_github_skills(self, requirement: str) -> List[Skill]:
        """
        從 GitHub 搜尋符合需求的開源專案

        步驟：
        1. 語義搜尋：將需求轉為關鍵字
        2. GitHub API：搜尋 repo (stars > 100, updated in 1y)
        3. 分析 README：提取功能描述
        4. 評估適配度：計算與需求的匹配分數
        5. 回傳 Top 5 候選
        """
        pass

    async def generate_skill_from_repo(self, repo_url: str) -> Skill:
        """
        從 GitHub repo 自動生成 Skill

        分析項目：
        1. Dockerfile/docker-compose → 容器化部署
        2. package.json/requirements.txt → 依賴安裝
        3. README.md → 使用說明與配置
        4. scripts/ → 啟動/停止/健康檢查腳本
        5. .env.example → 環境變數配置

        輸出：
        - MODULE.yaml (自動生成)
        - setup.sh (部署腳本)
        - README.md (使用指南)
        """
        pass

    async def compose_mvp_solution(self, user_need: str) -> MVPSolution:
        """
        組裝 MVP 方案

        例如：用戶需求「建立一個部落格系統」

        自動組裝：
        1. 搜尋 GitHub → 找到 Ghost/Hugo/Hexo
        2. 生成 Skills → ghost-deploy.yaml
        3. 整合現有 → M2 (web-deploy) + nginx
        4. 組合方案 → 完整部署腳本
        5. 一鍵執行 → 30 分鐘內上線
        """
        pass
```

### 4.4 整合示範：awesome-selfhosted

**目標**：將 [awesome-selfhosted](https://github.com/awesome-selfhosted/awesome-selfhosted) 的 200+ 服務自動轉為 Skills

**流程**：
```bash
# 1. 克隆資料庫
git clone https://github.com/awesome-selfhosted/awesome-selfhosted.git

# 2. 解析 Markdown
python3 parse_awesome_selfhosted.py
# 輸出：services.json (200+ 服務元數據)

# 3. 批次生成 Skills
python3 batch_generate_skills.py services.json
# 輸出：skills/analytics/, skills/cms/, skills/monitoring/ ...

# 4. 部署到 SHC
rsync -av skills/ acmacmini2:~/workshop/super-happy-coder/skills/community/

# 5. 測試
curl -X POST http://localhost:8081/api/v1/chat/direct \
  -d '{"student_id": "test", "message": "幫我部署 Grafana 監控系統"}'
# 預期：自動找到 skills/monitoring/grafana/ 並部署
```

**產出範例**：
```yaml
# skills/community/monitoring/grafana/MODULE.yaml
name: grafana-deploy
category: monitoring
description: 部署 Grafana 監控系統
source: https://github.com/grafana/grafana
tags: [monitoring, visualization, dashboard]

steps:
  - id: create_docker_compose
    template: docker-compose.yml.j2
    variables:
      - grafana_port: 3000
      - grafana_admin_password: admin

  - id: start_grafana
    command: docker-compose up -d

  - id: health_check
    command: curl http://localhost:3000/api/health
    retry: 10
    interval: 3s

  - id: output_credentials
    message: |
      Grafana 已部署成功！
      URL: http://localhost:3000
      用戶: admin
      密碼: {{grafana_admin_password}}
```

---

## Phase 5: 實作計劃與時程

### 5.1 Phase 1: Clawdbot 分析（Week 1）

**Day 1-2: GitHub 代碼分析**
- [ ] 克隆 OpenClaw repo 到 ac-mac
- [ ] 分析 Agent Runner 核心邏輯
- [ ] 研究 Session 管理與 Context 處理
- [ ] 記錄關鍵設計模式

**Day 3-4: 可選 - 實際部署測試**
- [ ] 在 acmacmini2 安裝 OpenClaw
- [ ] 執行 10 個測試任務（簡單→複雜）
- [ ] 記錄 session logs 並分析
- [ ] 對比 token 使用與完成度

**Day 5-7: 總結報告**
- [ ] 撰寫技術分析報告
- [ ] 列出可借鑑的設計模式
- [ ] 識別不適合 SHC 的部分
- [ ] 提出 v6 設計方案

### 5.2 Phase 2: SHC v5 診斷（Week 2）

**Day 1-2: 基準測試**
- [ ] 建立 test_task_completion.py（20 測試案例）
- [ ] 執行測試並記錄結果
- [ ] 分析失敗原因分類

**Day 3-4: 問題根因分析**
- [ ] 追蹤執行日誌找出斷點
- [ ] 識別缺失功能（變數傳遞、錯誤恢復）
- [ ] 量化問題影響（完成度 vs token）

**Day 5-7: 設計改進方案**
- [ ] TaskOrchestrator 詳細設計
- [ ] DeepPlanner 流程設計
- [ ] SmartRecovery 錯誤分類
- [ ] ContextBridge 介面設計

### 5.3 Phase 3: 核心增強實作（Week 3-4）

**Week 3: TaskOrchestrator + DeepPlanner**
- [ ] 實作 TaskOrchestrator 基礎框架
- [ ] 實作 DeepPlanner 多輪細化
- [ ] 整合到 HybridOrchestrator
- [ ] 單元測試（20+ cases）

**Week 4: SmartRecovery + ContextBridge**
- [ ] 實作錯誤分類與恢復邏輯
- [ ] 實作 ExecutionContext
- [ ] 更新 MODULE.yaml 支援變數
- [ ] 整合測試（end-to-end）

### 5.4 Phase 4: GitHub Skills Hub（Week 5-6）

**Week 5: SkillsHub Agent**
- [ ] GitHub API 整合（搜尋、分析）
- [ ] Repo 解析器（Dockerfile、README、scripts）
- [ ] Skill 自動生成器
- [ ] 測試：從 3 個 repo 生成 skills

**Week 6: awesome-selfhosted 整合**
- [ ] 解析 awesome-selfhosted Markdown
- [ ] 批次生成 50+ 常用服務 skills
- [ ] 部署到 SHC community skills/
- [ ] 端對端測試：用戶一句話部署服務

### 5.5 Phase 5: 整合測試與優化（Week 7-8）

**Week 7: 完成度測試**
- [ ] 重跑 test_task_completion.py
- [ ] 目標：A 類 100%、B 類 90%、C 類 80%、D 類 70%
- [ ] Token 使用量對比（vs v5 baseline）
- [ ] 成本分析（混合模式優化）

**Week 8: 使用者測試與調優**
- [ ] 邀請 3-5 位測試用戶
- [ ] 真實場景測試（部署專案、建立 API、配置服務）
- [ ] 收集反饋並調整
- [ ] 撰寫 v6 完整文件

---

## Phase 6: 成功指標

### 6.1 任務完成度（核心指標）

| 任務類別 | v5 Baseline | v6 目標 | Clawdbot 參考 |
|---------|------------|---------|--------------|
| A 類（簡單） | 85% | 100% | ~100% |
| B 類（中等） | 65% | 90% | ~95% |
| C 類（複雜） | 40% | 80% | ~90% |
| D 類（超複雜） | 20% | 70% | ~85% |
| **綜合平均** | **52.5%** | **85%** | **92.5%** |

### 6.2 成本效益

| 指標 | v5 | v6 目標 | Clawdbot |
|-----|-----|---------|----------|
| 平均 Token/任務 | 8,000 | 15,000 | 30,000 |
| 任務完成度 | 52.5% | 85% | 92.5% |
| **Token/完成任務** | **15,238** | **17,647** | **32,432** |
| 每月成本（100 任務） | $24 | $45 | $90 |
| **完成任務成本** | **$45.7** | **$52.9** | **$97.3** |

**結論**：v6 在保持成本優勢的同時，大幅提升完成度

### 6.3 Skills 生態

- [ ] Core Skills: 15+ 個（M1-M6 + 新增 9 個）
- [ ] Community Skills: 50+ 個（awesome-selfhosted）
- [ ] Auto-Generated: 用戶平均每月新建 5 個
- [ ] 覆蓋場景：Web 部署、監控、資料庫、CI/CD、通訊、儲存

### 6.4 用戶體驗

- [ ] MVP 部署時間：從 2 小時 → 30 分鐘
- [ ] 平均對話輪數：從 5 輪 → 2 輪（更聰明規劃）
- [ ] 錯誤恢復率：從 20% → 80%
- [ ] 用戶滿意度：>4.0/5.0

---

## Phase 7: 技術風險與對策

### 7.1 風險評估

| 風險 | 機率 | 影響 | 對策 |
|------|-----|------|------|
| DeepPlanner token 消耗過高 | 中 | 高 | 設定 max_rounds 上限，用 LOW tier 初步規劃 |
| AgentCreator 生成 skill 品質不穩 | 高 | 中 | 嚴格品質門檻 + 人工審核機制 |
| Context 管理記憶體溢出 | 低 | 高 | 限制 context size，舊資料自動歸檔 |
| GitHub API rate limit | 中 | 中 | 本地快取 + API key rotation |
| 社群 skills 安全性風險 | 中 | 高 | 沙盒執行 + 權限控制 + 程式碼審計 |

### 7.2 降級方案

如果 v6 開發超出預期：
- **Plan A**：Phase 3 優先（核心增強），Phase 4 延後
- **Plan B**：僅實作 TaskOrchestrator，其他功能 v6.1 再加
- **Plan C**：v5 基礎上微調，v7 再大改

---

## Phase 8: 預期產出

### 8.1 程式碼

**新增模組**（acmacmini2）：
- `task_orchestrator.py` (~500 行)
- `deep_planner.py` (~400 行)
- `smart_recovery.py` (~300 行)
- `context_bridge.py` (~200 行)
- `skills_hub_agent.py` (~600 行)
- `github_analyzer.py` (~400 行)

**修改模組**：
- `hybrid_orchestrator.py` (整合 TaskOrchestrator)
- `dynamic_planner.py` (升級為 DeepPlanner)
- `agent_creator.py` (整合 SkillsHub)

### 8.2 Skills 庫

- `skills/core/` — 15+ 核心模組
- `skills/community/` — 50+ 社群模組
- `skills/_templates/` — 自動生成模板

### 8.3 測試

- `test_task_orchestrator.py` (30+ tests)
- `test_deep_planner.py` (20+ tests)
- `test_smart_recovery.py` (25+ tests)
- `test_skills_hub.py` (15+ tests)
- `test_shc_v6_full.py` (100+ tests)

### 8.4 文件

- **技術文件**：
  - `~/knowledge-base/tech/ai-ml/2026-01-31-clawdbot-architecture-analysis.md`
  - `~/knowledge-base/tech/ai-ml/2026-02-XX-shc-v6-design-doc.md`
  - `~/knowledge-base/tech/ai-ml/2026-02-XX-shc-v6-implementation-report.md`

- **OpenSpec 更新**：
  - `openspec-v6/specs/10-vision.md`
  - `openspec-v6/specs/25-task-orchestration.md`
  - `openspec-v6/specs/30-skills-hub.md`

- **用戶指南**：
  - `openspec-v6/guides/quick-start.md`
  - `openspec-v6/guides/custom-skills.md`
  - `openspec-v6/guides/github-integration.md`

---

## 總結

### 核心策略

1. **學習而非複製**：分析 Clawdbot 優勢，設計適合 SHC 的方案
2. **迭代增強**：TaskOrchestrator 多輪執行，而非單次規劃
3. **智慧恢復**：錯誤分類與自動修復，提升完成度
4. **生態整合**：GitHub Skills Hub，快速滿足用戶需求
5. **成本可控**：混合模式 + 分層規劃，保持經濟優勢

### 競爭優勢

**vs Clawdbot**：
- ✅ 成本更低（45% 節省）
- ✅ 可控性更強（混合模式、強制模式）
- ✅ 適合企業（多租戶、配額管理）
- ⚖️ 完成度略低（85% vs 92.5%）

**vs 傳統 Chatbot**：
- ✅ 任務完成度高（85% vs <50%）
- ✅ 開源生態整合（一鍵部署）
- ✅ 自動化程度高（減少人工干預）

### 目標用戶

- **個人開發者**：快速搭建個人專案（部落格、工具、API）
- **小型企業**：低成本 MVP 部署（<$100/月）
- **教育機構**：程式設計教學助手（自動批改、專案指導）
- **自架愛好者**：一鍵部署自架服務（NAS、監控、媒體中心）

### 下一步行動

1. **用戶確認**：是否認同此計劃？優先順序調整？
2. **資源分配**：預計投入時間？需要額外資源？
3. **啟動 Phase 1**：開始 Clawdbot 分析，預計 7 天完成

---

## 附錄

### A. Clawdbot 參考資料

- [OpenClaw GitHub](https://github.com/clawdbot/clawdbot)
- [AGENTS.md Architecture](https://github.com/clawdbot/clawdbot/blob/main/AGENTS.md)
- [Clawdbot Complete Guide 2026](https://www.godofprompt.ai/blog/clawdbot-guide-2026)
- [Clawdbot AI Features & Setup](https://pub.towardsai.net/clawdbot-ai-the-revolutionary-open-source-personal-assistant-transforming-productivity-in-2026-6ec5fdb3084f)

### B. 相關開源專案

- [awesome-selfhosted](https://github.com/awesome-selfhosted/awesome-selfhosted) — 200+ 自架服務
- [free-for-dev](https://github.com/ripienaar/free-for-dev) — 免費開發資源
- [project-based-learning](https://github.com/practical-tutorials/project-based-learning) — 專案式學習

### C. SHC 現有文件

- `~/super-happy-tests/` — 測試套件
- `acmacmini2:~/workshop/super-happy-coder/openspec-v4/` — v5 規格
- `~/knowledge-base/tech/ai-ml/2026-01-31-shc-v5-hybrid-implementation.md` — v5 實作紀錄
