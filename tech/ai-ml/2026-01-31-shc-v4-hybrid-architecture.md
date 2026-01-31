---
title: SHC v4 混合架構設計 — 固定模組 + 動態規劃 + Agent-Creator
date: 2026-01-31
category: tech/ai-ml
tags: [SHC, architecture, hybrid-agent, module-creation, token-optimization]
source: 內部分析
---

# SHC v4 混合架構設計

## 背景

SHC v330 使用純靜態 MODULE.yaml 管線，優點是確定性高、token 消耗低，但缺點是無法處理模組庫中不存在的任務。Happy Coder 的 Claude Code 使用純動態 TodoWrite 驅動，靈活但 token 消耗大。

**目標**：結合兩者優勢，建立三層混合架構：
1. **優先使用固定模組**（低成本、高確定性）
2. **缺乏模組時啟用動態 LLM 規劃**（TodoWrite 模式）
3. **Agent-Creator 將成功的動態任務轉化為新模組**（擴充能力、降低未來成本）

## 架構總覽

```
用戶請求
    │
    ▼
┌─────────────────────────────┐
│   HybridOrchestrator        │
│                             │
│  1. ModuleRegistry.match()  │ ─── 命中 ──▶ AgentExecutor（固定管線）
│     觸發詞 + 語義匹配       │              ↓ 低 token 消耗
│                             │              ↓ MODULE.yaml 步驟
│  2. 未命中？                │              ↓ ProgressEmitter
│     ↓                       │
│  3. DynamicPlanner          │ ─── 啟用 ──▶ LLM TodoWrite 模式
│     LLM 生成任務清單         │              ↓ 高 token 消耗
│     動態執行 + 即時更新      │              ↓ 可中途重新規劃
│     ↓                       │
│  4. 任務完成後              │
│     ↓                       │
│  5. AgentCreator            │ ─── 評估 ──▶ 自動生成 MODULE.yaml
│     分析執行紀錄             │              ↓ 寫入 skills/ 目錄
│     萃取為模組定義           │              ↓ 下次同類任務直接走固定管線
│                             │
└─────────────────────────────┘
```

## 組件一：HybridOrchestrator（改造 orchestrator.py）

### 新增路由邏輯

```python
class HybridOrchestrator:
    """混合編排器 — 固定模組優先，動態規劃兜底"""

    def __init__(self, skills_dir, llm_router, cli_executor, emitter, feedback):
        self.agent_executor = AgentExecutor(skills_dir, cli_executor,
                                            llm_router, emitter, feedback)
        self.dynamic_planner = DynamicPlanner(llm_router, cli_executor, emitter)
        self.agent_creator = AgentCreator(skills_dir, llm_router)
        self.llm_router = llm_router

    async def execute(self, request, student_id, context=None):
        # 第一層：嘗試匹配固定模組
        agent = self.agent_executor.registry.match_agent(request)

        if agent:
            # 固定管線執行
            logger.info(f"模組命中: {agent.id} - {agent.name}")
            result = await self.agent_executor.execute(
                agent.id, request, student_id
            )
            return HybridResult(mode='fixed', execution=result)

        # 第二層：語義匹配（可選，用 LOW tier LLM 判斷）
        semantic_match = await self._semantic_match(request)
        if semantic_match:
            logger.info(f"語義匹配: {semantic_match.id}")
            result = await self.agent_executor.execute(
                semantic_match.id, request, student_id
            )
            return HybridResult(mode='semantic', execution=result)

        # 第三層：動態 LLM 規劃
        logger.info("無匹配模組，啟用動態規劃")
        result = await self.dynamic_planner.execute(request, student_id, context)

        # 第四層：評估是否值得建立新模組
        if result.state == 'completed' and result.quality_score >= 0.8:
            await self.agent_creator.evaluate_and_create(
                request, result, student_id
            )

        return HybridResult(mode='dynamic', execution=result)

    async def _semantic_match(self, request):
        """使用 LOW tier LLM 做語義匹配"""
        modules = self.agent_executor.registry.list_agents()
        if not modules:
            return None

        prompt = f"""以下是可用的模組列表：
{json.dumps(modules, ensure_ascii=False, indent=2)}

用戶請求：{request}

如果有匹配的模組，回覆其 id。如果沒有，回覆 "NONE"。
只回覆 id 或 NONE，不要其他文字。"""

        resp = self.llm_router.generate(tier='LOW', prompt=prompt, max_tokens=50)
        if resp.success and resp.text.strip() != 'NONE':
            return self.agent_executor.registry.get_agent(resp.text.strip())
        return None
```

### 路由決策的 Token 成本

| 階段 | LLM 呼叫 | 預估 Token | 說明 |
|------|----------|-----------|------|
| 觸發詞匹配 | 無 | 0 | 純字串比對，零成本 |
| 語義匹配 | LOW tier × 1 | ~200 | 僅在觸發詞未命中時 |
| 動態規劃 | HIGH tier × N | ~2000-8000 | 完整 TodoWrite 循環 |
| Agent-Creator | LOW tier × 1 | ~1500 | 僅在動態執行成功後 |

## 組件二：DynamicPlanner（新增）

模擬 Claude Code 的 TodoWrite 驅動模式：

```python
class DynamicPlanner:
    """動態 LLM 規劃器 — TodoWrite 模式"""

    def __init__(self, llm_router, cli_executor, emitter):
        self.llm_router = llm_router
        self.cli_executor = cli_executor
        self.emitter = emitter

    async def execute(self, request, student_id, context=None):
        # 1. 初始規劃：LLM 生成任務清單
        todo_list = await self._create_plan(request, context)

        execution = DynamicExecution(
            request=request,
            student_id=student_id,
            todo_list=todo_list
        )

        # 2. 逐步執行
        while execution.has_pending_tasks():
            task = execution.next_task()
            task.state = 'in_progress'

            # 推送進度
            if self.emitter:
                self.emitter.step_started(
                    student_id, task.index, task.description,
                    len(todo_list), ''
                )

            # 執行任務
            result = await self._execute_task(execution, task)

            if result.success:
                task.state = 'completed'
                task.output = result.output
            else:
                # 3. 失敗時重新規劃（TodoWrite 的核心優勢）
                updated_list = await self._replan(
                    execution, task, result.error
                )
                execution.update_todo_list(updated_list)

            # 推送進度
            if self.emitter:
                self.emitter.step_completed(
                    student_id, task.index, task.description,
                    len(execution.todo_list), task.output[:80], 0
                )

        execution.state = 'completed'
        execution.quality_score = self._assess_quality(execution)
        return execution

    async def _create_plan(self, request, context):
        """LLM 生成初始任務清單"""
        prompt = f"""你是一個任務規劃器。分析用戶請求，產生執行步驟清單。

用戶請求：{request}

輸出 JSON 格式：
[
  {{"id": 1, "description": "步驟描述", "action_type": "llm|shell|code", "details": "具體操作"}}
]

原則：
- 步驟要具體可執行
- 每步只做一件事
- 總步驟數控制在 3-8 步
"""
        resp = self.llm_router.generate(tier='HIGH', prompt=prompt, max_tokens=1024)
        return json.loads(resp.text)

    async def _replan(self, execution, failed_task, error):
        """失敗後重新規劃剩餘步驟"""
        prompt = f"""任務執行中遇到錯誤，需要重新規劃。

原始請求：{execution.request}
已完成步驟：{json.dumps(execution.completed_tasks(), ensure_ascii=False)}
失敗步驟：{failed_task.description}
錯誤訊息：{error}

請重新規劃剩餘步驟，解決上述錯誤。輸出 JSON 格式同上。"""

        resp = self.llm_router.generate(tier='HIGH', prompt=prompt, max_tokens=1024)
        return json.loads(resp.text)
```

## 組件三：AgentCreator（新增）

將成功的動態執行轉化為新的 MODULE.yaml：

```python
class AgentCreator:
    """Agent 創建器 — 從動態執行紀錄生成新模組"""

    def __init__(self, skills_dir, llm_router):
        self.skills_dir = skills_dir
        self.llm_router = llm_router

    async def evaluate_and_create(self, request, execution, student_id):
        """評估是否值得建立新模組"""

        # 1. 判斷是否為可重複的任務模式
        evaluation = await self._evaluate_reusability(request, execution)

        if not evaluation['should_create']:
            logger.info(f"任務不適合建立模組: {evaluation['reason']}")
            return None

        # 2. 生成 MODULE.yaml
        module_yaml = await self._generate_module(request, execution, evaluation)

        # 3. 寫入檔案
        module_id = evaluation['suggested_id']
        module_dir = Path(self.skills_dir) / module_id
        module_dir.mkdir(parents=True, exist_ok=True)

        module_path = module_dir / 'MODULE.yaml'
        with open(module_path, 'w', encoding='utf-8') as f:
            f.write(module_yaml)

        # 4. 熱重載 Registry
        # AgentExecutor 的 registry.reload() 會重新載入

        logger.info(f"新模組已建立: {module_id} at {module_path}")
        return module_id

    async def _evaluate_reusability(self, request, execution):
        """用 LOW tier LLM 評估任務是否可重複"""
        prompt = f"""分析以下任務是否值得建立為可重複使用的自動化模組：

任務：{request}
執行步驟：{json.dumps(execution.step_log(), ensure_ascii=False)}
品質分數：{execution.quality_score}

評估標準：
1. 是否為可重複的任務模式？（一次性任務不需要模組化）
2. 步驟是否可參數化？（能否抽象為模板）
3. 是否有明確的觸發詞？

輸出 JSON：
{{
  "should_create": true/false,
  "reason": "原因",
  "suggested_id": "module-id",
  "suggested_name": "模組名稱",
  "suggested_triggers": ["觸發詞1", "觸發詞2"],
  "parameterizable_inputs": ["input1", "input2"]
}}"""

        resp = self.llm_router.generate(tier='LOW', prompt=prompt, max_tokens=512)
        return json.loads(resp.text)

    async def _generate_module(self, request, execution, evaluation):
        """從執行紀錄生成 MODULE.yaml"""
        prompt = f"""根據以下成功執行的任務紀錄，生成一個 MODULE.yaml 定義。

任務：{request}
執行步驟和結果：{json.dumps(execution.step_log(), ensure_ascii=False)}
模組資訊：
- ID: {evaluation['suggested_id']}
- 名稱: {evaluation['suggested_name']}
- 觸發詞: {evaluation['suggested_triggers']}
- 可參數化輸入: {evaluation['parameterizable_inputs']}

參考現有模組格式（M1 coding-agent）：
```yaml
id: M1
name: CLI Agent 控制器
version: '1.1'
triggers: [程式, code, coding, 開發]
inputs:
  task_description:
    type: string
    required: true
steps:
- id: understand
  name: 理解任務
  action: llm_analyze
  prompt: "..."
  output: task_analysis
- id: execute
  name: 執行任務
  action: coding_agent
  depends_on: [understand]
quality_criteria:
  execution:
    completed: true
timeout: 180
```

請輸出完整的 YAML 內容，步驟要具體，prompt 要能正確替換變數。"""

        resp = self.llm_router.generate(tier='HIGH', prompt=prompt, max_tokens=2048)
        # 提取 YAML 內容
        yaml_match = re.search(r'```yaml\n(.*?)```', resp.text, re.DOTALL)
        if yaml_match:
            return yaml_match.group(1)
        return resp.text
```

## Token 消耗分析與優化策略

### 三種模式的 Token 成本對比

| 模式 | 每次任務 Token 估算 | 適用場景 |
|------|-------------------|---------|
| 固定模組 | 500-2,000 | 已有 MODULE.yaml 的重複任務 |
| 語義匹配 + 固定模組 | 700-2,200 | 觸發詞未命中但語義匹配到 |
| 動態規劃 | 3,000-10,000 | 全新任務類型 |
| 動態規劃 + Agent-Creator | 4,500-12,000 | 全新任務 + 模組化（僅首次） |

### Token 優化策略

#### 1. 分層 LLM 路由（已有，強化）
```
HIGH tier: Claude Sonnet / GPT-4o  → 規劃、coding_agent、模組生成
LOW tier:  Gemini Flash / GPT-4o-mini → 語義匹配、評估、摘要、結果分析
```

#### 2. 快取機制
- **模組匹配快取**：相同觸發詞組合的匹配結果快取 1 小時
- **語義匹配快取**：相似請求（cosine > 0.9）直接返回上次匹配結果
- **Prompt 模板快取**：MODULE.yaml 的 prompt 預編譯，避免重複解析

#### 3. 漸進式規劃（減少動態模式 token）
```
第一次動態執行：完整 TodoWrite 循環（~8000 tokens）
同類第二次：Agent-Creator 已建立模組，走固定管線（~1500 tokens）
同類第三次起：直接命中觸發詞（~500 tokens）
```

#### 4. Context 壓縮
- 動態規劃時，已完成步驟的輸出只保留摘要（前 200 字）
- 重新規劃（replan）時，只傳失敗步驟和摘要，不傳完整歷史

#### 5. Agent-Creator 門檻控制
- 品質分數 >= 0.8 才觸發
- 同類任務出現 2 次以上才建立模組（用 FeedbackCollector 追蹤）
- 生成的模組經人工確認後才啟用（可選）

## 實作優先順序

### Phase 1：HybridOrchestrator 路由（最小改動）
- [ ] 修改 `orchestrator.py`，加入三層路由邏輯
- [ ] 新增 `_semantic_match()` 方法
- [ ] 觸發詞未命中時的 fallback 邏輯
- **改動量**：~50 行，只改 orchestrator.py
- **風險**：低，現有固定管線完全不變

### Phase 2：DynamicPlanner（新增檔案）
- [ ] 建立 `dynamic_planner.py`
- [ ] 實作 TodoWrite 式任務清單管理
- [ ] 實作中途重新規劃（replan）
- [ ] 整合 ProgressEmitter 推送動態步驟進度
- **改動量**：~200 行新檔案
- **風險**：中，需要處理 LLM 輸出解析的穩定性

### Phase 3：AgentCreator（新增檔案）
- [ ] 建立 `agent_creator.py`
- [ ] 實作可重複性評估
- [ ] 實作 MODULE.yaml 自動生成
- [ ] 整合 AgentRegistry 熱重載
- [ ] 加入 FeedbackCollector 的頻率追蹤
- **改動量**：~250 行新檔案
- **風險**：中高，生成的 YAML 需要驗證

### Phase 4：Token 優化
- [ ] 語義匹配快取（Redis）
- [ ] Context 壓縮策略
- [ ] Agent-Creator 門檻控制（頻率追蹤）
- [ ] 監控儀表板：每種模式的 token 使用量

## 與現有架構的整合點

| 現有組件 | 整合方式 | 改動量 |
|---------|---------|--------|
| `agent_executor.py` | 不改動，HybridOrchestrator 調用它 | 0 |
| `orchestrator.py` | 改造為 HybridOrchestrator | ~50 行 |
| `llm_router.py` | 不改動，DynamicPlanner 直接使用 | 0 |
| `progress_emitter.py` | 不改動，DynamicPlanner 直接使用 | 0 |
| `feedback_collector.py` | 新增頻率追蹤欄位 | ~20 行 |
| `output_analyzer.py` | 不改動 | 0 |
| `proxy.py` | 改用 HybridOrchestrator | ~5 行 |
| MODULE.yaml 檔案 | 不改動，Agent-Creator 只新增 | 0 |

## 關鍵設計決策

### Q: 為什麼不直接全面改用動態規劃？
**A**: Token 成本。固定模組每次任務 ~1000 tokens，動態規劃 ~6000 tokens。對於已知的 4 種模組（coding、web-deploy、PPTX、RAG），固定管線每月可節省約 80% 的 token 消耗。

### Q: Agent-Creator 生成的模組品質如何保證？
**A**: 三道防線：
1. 品質分數門檻（>= 0.8）
2. YAML schema 驗證（載入時自動檢查）
3. 可選的人工審核模式（生成到 `skills/_pending/` 目錄）

### Q: 動態規劃失敗怎麼辦？
**A**: DynamicPlanner 內建 replan 機制（最多 3 次），如果仍然失敗，記錄到 FeedbackCollector 並通知用戶。不會自動建立模組（品質分數 < 0.8）。

### Q: 語義匹配是否會增加延遲？
**A**: 使用 LOW tier LLM（Gemini Flash），延遲約 200-500ms，只在觸發詞未命中時才呼叫。對於命中觸發詞的請求，零額外延遲。
