---
title: 增強型 Multi-Agent 系統設計 - Super Happy Coder
date: 2026-01-28
category: tech
tags: [AI, agent, clawdbot, happy-coder, multi-agent, 架構設計]
---

# 增強型 Multi-Agent 系統設計

整合 Clawdbot 中介層設計 + OpenSpec TG Agent 規格 + RPI5 多學員 Proxy，打造高度整合的教學用 AI Agent 系統。

---

## 1. 現有系統分析

### 1.1 Clawdbot 的優勢（學習點）

| 機制 | 功能 | 價值 |
|------|------|------|
| **SOUL.md** | 身份定義、個性、邊界 | AI 有一致的行為模式 |
| **AGENTS.md** | 行為規範、安全規則 | 標準化的執行流程 |
| **MEMORY.md** | 長期記憶 | 跨 Session 的上下文續接 |
| **Skills 系統** | 每個工具有說明文件 | AI 可查閱說明書正確使用工具 |
| **PTY + Background** | 偽終端 + 背景執行 | 支援複雜的互動式任務 |
| **Heartbeat** | 定期喚醒 | 主動檢查任務、自動工作 |

### 1.2 RPI5 Proxy 的基礎（現有能力）

```python
# 核心架構
- SessionManager: 管理多學員獨立 Session
- TrackedSession: 追蹤 PID、狀態、活動時間
- ThreadPoolExecutor: 並行處理請求
- Heartbeat: 清理死掉/閒置 Session
- Redis: 配額、使用量、對話歷史、即時進度

# 已實現
- 多學員隔離（by student_id）
- 工作目錄隔離（/tmp/workshop-sessions/{student_id}）
- 對話上下文續接（thread_id）
- 即時進度回報（thinking/responding/completed）
- 配額管理（每日 token 限制）
- 支援 Codex/Claude/Gemini 三種後端
```

### 1.3 OpenSpec 的目標（設計願景）

```
┌─────────────────────────────────────────────────────────────┐
│                    TG Bot（學員入口）                        │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                Mac mini Control Plane                        │
│  - Gateway/Router/Queue                                      │
│  - Module Orchestrator                                       │
│  - Audit/Tracing                                            │
└────────────────────────┬────────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                3090 Compute Plane                            │
│  - LLM API（Planner/Tool-calling）                          │
│  - Embedding API                                             │
│  - Rerank API                                                │
│  - OCR API                                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 整合設計：Super Happy Coder

### 2.1 系統架構

```
┌─────────────────────────────────────────────────────────────────────┐
│                         TG Bot Gateway                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────────┐  │
│  │  Telegram   │  │   Discord   │  │  Web UI（講師用）            │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────────────┘  │
│         └────────────────┼─────────────────────┘                     │
│                          ▼                                           │
│              ┌───────────────────────┐                               │
│              │   Identity Resolver   │ ◄── tg_user_id → student_id  │
│              └───────────┬───────────┘                               │
└──────────────────────────┼───────────────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Control Plane (Mac mini)                          │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                    Context Injection Layer                      │ │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐│ │
│  │  │  SOUL.md     │ │  AGENTS.md   │ │  MEMORY.md (per student) ││ │
│  │  │  (系統身份)  │ │  (行為規範)  │ │  (長期記憶)              ││ │
│  │  └──────────────┘ └──────────────┘ └──────────────────────────┘│ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                    Skills / Modules System                      │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │ │
│  │  │ M1: CLI  │ │ M2: Web  │ │ M3: RAG  │ │ M4: OCR  │  ...     │ │
│  │  │ Agent    │ │ Deploy   │ │ KB       │ │ KB       │          │ │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘          │ │
│  │  每個模組有 SKILL.md 說明文件                                   │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                    Session Manager (Enhanced)                   │ │
│  │  - TrackedSession per student                                   │ │
│  │  - PTY allocation for interactive CLI                          │ │
│  │  - Background process management                                │ │
│  │  - Heartbeat (60s) for auto-cleanup + proactive tasks          │ │
│  │  - Task Queue (concurrent execution)                           │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                    Router + Orchestrator                        │ │
│  │  - Intent classification                                        │ │
│  │  - Module selection                                             │ │
│  │  - Risk assessment → local vs cloud                            │ │
│  │  - Tool calling decision                                        │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                    Audit + Observability                        │ │
│  │  - Redis: usage, quota, progress, conversation                 │ │
│  │  - Structured logs (per student_id, task_id)                   │ │
│  │  - Instructor dashboard                                         │ │
│  └────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  CLI Backend │  │  3090 APIs   │  │  External    │
│  Codex/Claude│  │  LLM/Embed/  │  │  Cloud LLM   │
│  /Gemini     │  │  Rerank/OCR  │  │  (overflow)  │
└──────────────┘  └──────────────┘  └──────────────┘
```

### 2.2 核心增強：Context Injection

**從 Clawdbot 學到的最重要機制**

```python
# 每個請求前，注入 Context Files
def build_enhanced_prompt(student_id: str, prompt: str) -> str:
    """
    注入三層 Context：
    1. SOUL.md - 系統身份（全局）
    2. AGENTS.md - 行為規範（全局）
    3. MEMORY.md - 學員個人記憶
    4. SKILL.md - 當前模組的使用說明（如需要）
    """

    context_parts = []

    # 系統身份
    soul = read_file('context/SOUL.md')
    context_parts.append(f"<system-identity>\n{soul}\n</system-identity>")

    # 行為規範
    agents = read_file('context/AGENTS.md')
    context_parts.append(f"<behavior-rules>\n{agents}\n</behavior-rules>")

    # 學員個人記憶（如果存在）
    memory_path = f"memory/{student_id}/MEMORY.md"
    if os.path.exists(memory_path):
        memory = read_file(memory_path)
        context_parts.append(f"<student-memory>\n{memory}\n</student-memory>")

    # 根據意圖選擇模組，注入對應的 SKILL.md
    intent = classify_intent(prompt)
    if intent.module:
        skill = read_file(f"skills/{intent.module}/SKILL.md")
        context_parts.append(f"<module-skill>\n{skill}\n</module-skill>")

    # 組合完整 prompt
    full_prompt = "\n\n".join(context_parts) + f"\n\n{prompt}"
    return full_prompt
```

### 2.3 Context Files 設計

#### SOUL.md（系統身份）
```markdown
# 我是誰

你是 Super Happy Coder，一個專為教學設計的 AI 助理。

## 核心能力
- 程式碼生成與解釋
- 網站部署
- 知識庫問答
- 文件 OCR 處理

## 個性特質
- 耐心解釋，適合教學
- 鼓勵學習，不直接給答案
- 用繁體中文回應
- 保持專業但友善

## 邊界
- 不執行危險操作
- 不洩漏其他學員資料
- 不超出授權範圍
```

#### AGENTS.md（行為規範）
```markdown
# 行為規範

## 執行流程
1. 理解學員意圖
2. 選擇適當模組
3. 評估風險等級
4. 執行並回報進度
5. 記錄重要發現到 MEMORY.md

## 記憶管理
- 每次對話結束後，更新學員的 MEMORY.md
- 記錄：學習進度、偏好、常見錯誤
- 格式：日期 + 摘要

## 安全規則
- 只操作學員自己的 workspace
- 不執行 rm -rf、format 等危險指令
- API key 等敏感資訊不外洩
```

#### skills/web-deploy/SKILL.md（模組說明）
```markdown
# 網站部署模組

## 用途
將學員的專案部署到 Cloudflare Pages

## 使用方式
1. 確認專案已在 workspace
2. 建立 GitHub repo
3. 連結 Cloudflare Pages
4. 回傳部署 URL

## 工具呼叫
- `gh repo create` - 建立 repo
- `gh secret set` - 設定 secrets
- `wrangler pages deploy` - 部署

## 範例
學員：「幫我把這個網站部署上線」
→ 執行 M2 網站部署流程
→ 回傳：https://xxx.pages.dev
```

### 2.4 Enhanced Session Manager

```python
@dataclass
class EnhancedSession(TrackedSession):
    """增強版 Session"""

    # 繼承原有欄位
    # + 新增 Clawdbot 風格的功能

    # 個人記憶路徑
    memory_file: str = ''

    # 當前執行的模組
    active_module: Optional[str] = None

    # 背景任務列表
    background_tasks: list[dict] = field(default_factory=list)

    # PTY session（用於互動式 CLI）
    pty_session: Optional[object] = None

    def __post_init__(self):
        super().__post_init__()
        self.memory_file = f"memory/{self.student_id}/MEMORY.md"
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)

    def update_memory(self, entry: str):
        """追加記憶到 MEMORY.md"""
        with open(self.memory_file, 'a', encoding='utf-8') as f:
            f.write(f"\n## {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(entry + "\n")

    def get_memory(self) -> str:
        """讀取學員記憶"""
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
```

### 2.5 Heartbeat 增強（主動任務）

```python
def _enhanced_heartbeat_loop(self):
    """
    增強版心跳（學習自 Clawdbot）

    不只清理 Session，還主動檢查：
    1. 背景任務是否完成
    2. 是否需要通知學員
    3. 是否需要更新記憶
    """
    while self.heartbeat_running:
        time.sleep(HEARTBEAT_INTERVAL)

        for student_id, session in self.sessions.items():
            # 檢查背景任務
            for task in session.background_tasks:
                if task['status'] == 'running':
                    result = self.check_background_task(task)
                    if result['completed']:
                        # 通知學員（透過 TG Bot）
                        self.notify_student(student_id, f"任務完成: {task['name']}")
                        task['status'] = 'completed'

                        # 記錄到記憶
                        session.update_memory(f"- 完成任務: {task['name']}")

            # 清理過期 Session
            if session.is_expired() and session.status == 'idle':
                self._cleanup_session(student_id)
```

---

## 3. 實作路線圖

### Phase 1: 基礎增強（在 RPI5 Proxy 上）

```
目標：加入 Context Injection
工作量：~2 天

1. 建立 context/ 目錄
   - SOUL.md
   - AGENTS.md

2. 修改 build_prompt_with_context()
   - 加入 Context Files 注入

3. 建立 memory/{student_id}/ 結構
   - 每個學員有獨立記憶檔

4. 測試：確認 AI 行為一致性提升
```

### Phase 2: Skills 系統

```
目標：模組化工具使用
工作量：~3 天

1. 建立 skills/ 目錄結構
   skills/
   ├── cli-agent/SKILL.md
   ├── web-deploy/SKILL.md
   ├── rag-kb/SKILL.md
   └── ocr-kb/SKILL.md

2. Intent Classifier
   - 根據學員輸入，選擇適當模組
   - 注入對應的 SKILL.md

3. 測試：M2 網站部署端到端
```

### Phase 3: 3090 Compute APIs 整合

```
目標：本地 LLM 推理
工作量：~5 天

1. 在 3090 上部署
   - LLM API（vLLM + Qwen2.5）
   - Embedding API（BGE-M3）
   - Rerank API（BGE-reranker）

2. Router 整合
   - 簡單任務 → 本地 LLM
   - 複雜任務 → Cloud API

3. 測試：RAG 問答流程
```

### Phase 4: PTY + Background

```
目標：互動式任務
工作量：~3 天

1. 加入 PTY 支援
   - 使用 pty.spawn() 或 pexpect
   - 支援需要確認的指令

2. Background Task Manager
   - 支援長時間任務
   - 定期回報進度

3. 測試：複雜的多步驟任務
```

---

## 4. 檔案結構

```
super-happy-coder/
├── README.md
├── docker-compose.yml
│
├── control-plane/                 # Mac mini 服務
│   ├── proxy.py                   # 主服務（增強版）
│   ├── router.py                  # 意圖分類 + 模組選擇
│   ├── session_manager.py         # 增強版 Session 管理
│   │
│   ├── context/                   # Context Files
│   │   ├── SOUL.md
│   │   └── AGENTS.md
│   │
│   ├── skills/                    # 模組說明
│   │   ├── cli-agent/SKILL.md
│   │   ├── web-deploy/SKILL.md
│   │   ├── rag-kb/SKILL.md
│   │   └── ocr-kb/SKILL.md
│   │
│   └── memory/                    # 學員記憶
│       ├── student-001/MEMORY.md
│       └── student-002/MEMORY.md
│
├── tg-bot/                        # Telegram Bot
│   └── bot.py
│
└── compute-apis/                  # 3090 服務
    ├── llm-api/
    ├── embedding-api/
    ├── rerank-api/
    └── ocr-api/
```

---

## 5. 關鍵差異比較

| 特性 | RPI5 Proxy (現有) | Super Happy Coder (增強) |
|------|-------------------|-------------------------|
| Context Injection | ❌ 只有對話歷史 | ✅ SOUL + AGENTS + MEMORY + SKILL |
| 模組系統 | ❌ 無 | ✅ Skills 目錄 + SKILL.md |
| 記憶持久化 | ⚠️ Redis 7天 | ✅ MEMORY.md 永久 |
| 意圖分類 | ❌ 直接轉發 | ✅ Router 選擇模組 |
| 本地 LLM | ❌ 無 | ✅ 3090 Compute APIs |
| PTY 支援 | ❌ subprocess.Popen | ✅ pty.spawn / pexpect |
| 背景任務 | ⚠️ 基本 | ✅ + 主動通知 |
| Heartbeat | ✅ 清理用 | ✅ + 主動任務檢查 |

---

## 6. 結論

整合三個系統的精華：

1. **Clawdbot** → Context Injection（SOUL/AGENTS/MEMORY）+ Skills 系統
2. **RPI5 Proxy** → Multi-Session 管理 + Redis 狀態追蹤
3. **OpenSpec** → 架構願景 + 3090 Compute APIs + TG Bot 入口

最終產出：**Super Happy Coder** - 一個可以多學員同時使用、有持久記憶、能查閱說明書、支援複雜任務的教學用 AI Agent 系統。
