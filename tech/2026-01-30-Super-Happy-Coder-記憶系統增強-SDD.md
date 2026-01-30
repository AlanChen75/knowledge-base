---
title: Super Happy Coder 記憶系統增強 SDD
date: 2026-01-30
category: tech
tags: [super-happy-coder, memory, personalization, SDD, architecture, 使用者偏好]
source: 架構分析與 Clawdbot 對比研究
---

# Super Happy Coder 記憶系統增強 SDD

## Software Design Document

---

## 一、背景與動機

### 1.1 現狀分析

Super Happy Coder（以下簡稱 SHC）目前已實作 Clawdbot 風格的 Context Injection（SOUL.md + AGENTS.md + per-student MEMORY.md），但在使用者偏好追蹤和長期記憶方面存在明顯不足。

#### 現有記憶機制

| 機制 | 實作狀態 | 問題 |
|------|----------|------|
| SOUL.md | ✅ 已實作 | 全域，非個人化 |
| AGENTS.md | ✅ 已實作 | 全域，非個人化 |
| MEMORY.md (per-student) | ⚠️ 粗糙 | 只記任務摘要，不記偏好 |
| Conversation History | ⚠️ Redis 7天過期 | 超過 TTL 後遺失 |
| Feedback Collector | ⚠️ 有設計未產出 | feedback_store/ 空的 |
| USER.md | ❌ 缺少 | 不知道學員是誰 |
| 語意搜尋 | ❌ 缺少 | 舊記憶被截斷丟失 |
| 偏好自動萃取 | ❌ 缺少 | 自動記憶只記 prompt 前 100 字 |

#### 對標 Clawdbot 的差距

| 功能 | Clawdbot | SHC 現狀 | 本次目標 |
|------|----------|----------|----------|
| USER.md 使用者畫像 | ✅ | ❌ | ✅ 新增 |
| MEMORY.md 長期記憶 | ✅ 語意搜尋 | ⚠️ 截斷 50 行 | ✅ 增強 |
| 每日日誌 | ✅ YYYY-MM-DD.md | ❌ | ✅ 新增 |
| 語意向量搜尋 | ✅ SQLite-vec | ❌ | ✅ 新增 |
| 偏好自動萃取 | ✅ 壓縮前保存 | ❌ | ✅ 新增 |
| 對話歷史持久化 | ✅ JSONL 永久 | ⚠️ Redis 7天 | ✅ 延長 + 備份 |

### 1.2 相關文件

| 文件 | 路徑 | 內容 |
|------|------|------|
| OpenSpec v3 架構 | `~/agent-projects/openspec_tg_agent_system_v3/` | 系統架構規格 |
| 增強型設計文件 | `~/knowledge-base/tech/2026-01-28-增強型-Multi-Agent-系統設計.md` | Clawdbot 整合設計 |
| 架構對比分析 | `~/knowledge-base/tech/2026-01-28-AI-Agent-架構分析-Clawdbot-vs-Happy-Coder.md` | 三系統比較 |
| 回饋機制設計 | `~/knowledge-base/tech/2026-01-29-互動進度與回饋機制設計.md` | Feedback Loop |
| 模組編排設計 | `~/knowledge-base/tech/2026-01-28-模組編排系統設計.md` | Module Orchestrator |
| 最新測試報告 | `~/knowledge-base/tech/2026-01-30-Super-Happy-Coder-修復後完整測試報告.md` | 61.8% 通過率 |

---

## 二、架構增強設計

### 2.1 增強後的系統架構

```
┌─────────────────────────────────────────────────────────────────────┐
│                         TG Bot Gateway                               │
│              Identity Resolver: tg_user_id → student_id              │
└──────────────────────────────┬───────────────────────────────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Control Plane (Mac mini 2)                        │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │              Context Injection Layer (增強版)                   │ │
│  │                                                                │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌─────────────────┐  │ │
│  │  │ SOUL.md  │ │AGENTS.md │ │ USER.md  │ │   MEMORY.md     │  │ │
│  │  │ (全域)   │ │ (全域)   │ │(per-user)│ │  (per-user)     │  │ │
│  │  │ 系統身份 │ │ 行為規範 │ │ 使用者   │ │  長期記憶       │  │ │
│  │  │          │ │          │ │ 偏好畫像 │ │  + 每日日誌     │  │ │
│  │  └──────────┘ └──────────┘ └──────────┘ └─────────────────┘  │ │
│  │                                                  ▲             │ │
│  │                                    ┌─────────────┘             │ │
│  │                                    │                           │ │
│  │  ┌──────────────────────────────────────────────────────────┐ │ │
│  │  │            Memory Search Engine (新增)                    │ │ │
│  │  │  ┌────────────────┐  ┌───────────────────────────────┐  │ │ │
│  │  │  │ Embedding API  │  │ SQLite-vec 向量資料庫          │  │ │ │
│  │  │  │ (3090 / local) │  │ memory/{student_id}/index.db  │  │ │ │
│  │  │  └────────────────┘  └───────────────────────────────┘  │ │ │
│  │  │  混合搜尋: vector similarity + BM25 keyword             │ │ │
│  │  └──────────────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │            Preference Extractor (新增)                         │ │
│  │  對話結束時自動萃取使用者偏好 → 更新 USER.md + MEMORY.md      │ │
│  │  結合 FeedbackCollector 的參數萃取                             │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  ┌──────────────────────────────────────┐ ┌───────────────────────┐ │
│  │  Session Manager + Redis (增強)      │ │ Skills / Modules      │ │
│  │  - 對話歷史 TTL: 7天 → 90天         │ │ - coding-agent        │ │
│  │  - 過期前自動備份到 Markdown         │ │ - web-deploy          │ │
│  │  - Conversation JSONL 持久化         │ │ - rag-kb              │ │
│  └──────────────────────────────────────┘ │ - obsidian            │ │
│                                            │ - github              │ │
│  ┌──────────────────────────────────────┐ └───────────────────────┘ │
│  │  Router + Orchestrator              │                            │
│  │  Feedback Collector (現有)          │                            │
│  │  Progress Emitter (現有)            │                            │
│  └──────────────────────────────────────┘                            │
└──────────────────────────────────────────────────────────────────────┘
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  CLI Backend │  │  3090 APIs   │  │  External    │
│  Claude      │  │  LLM/Embed/  │  │  Cloud LLM   │
│              │  │  Rerank/OCR  │  │              │
└──────────────┘  └──────────────┘  └──────────────┘
```

### 2.2 增強後的目錄結構

```
super-happy-coder/
├── proxy.py                    # 主服務（修改）
├── preference_extractor.py     # 【新增】偏好萃取器
├── memory_search.py            # 【新增】語意搜尋引擎
├── feedback_collector.py       # 回饋收集（現有，整合強化）
├── agent_executor.py           # Agent 執行器（現有）
├── orchestrator.py             # 模組編排（現有）
├── compute_client.py           # Compute Plane 客戶端（現有）
├── progress_emitter.py         # 進度發射器（現有）
│
├── context/
│   ├── SOUL.md                 # 系統身份（現有）
│   └── AGENTS.md               # 行為規範（修改，加入偏好管理規則）
│
├── memory/
│   └── {student_id}/
│       ├── USER.md             # 【新增】使用者偏好畫像
│       ├── MEMORY.md           # 長期記憶（增強格式）
│       ├── daily/              # 【新增】每日日誌
│       │   ├── 2026-01-30.md
│       │   └── 2026-01-31.md
│       ├── conversations/      # 【新增】對話備份
│       │   └── 2026-01-30.jsonl
│       └── index.db            # 【新增】向量搜尋索引
│
├── skills/                     # 模組系統（現有）
│   ├── coding-agent/
│   ├── web-deploy/
│   ├── obsidian/
│   ├── rag-kb/
│   └── github/
│
├── feedback_store/             # 回饋記錄（現有目錄）
├── data/                       # 資料目錄
└── logs/                       # 日誌目錄
```

---

## 三、詳細設計

### 3.1 USER.md — 使用者偏好畫像

#### 檔案格式

```markdown
# 使用者資料

## 基本資訊
- 稱呼：{display_name}
- 語言偏好：繁體中文
- 時區：Asia/Taipei
- 加入日期：YYYY-MM-DD

## 技術背景
- 程式語言：{languages}
- 框架經驗：{frameworks}
- 技術等級：{beginner|intermediate|advanced}
- 目前專案：{current_projects}

## 使用偏好
- 回應風格：{detailed|concise|step-by-step}
- 程式碼風格：{with_comments|minimal_comments}
- 範例偏好：{with_examples|without_examples}
- 喜歡的框架：{preferred_frameworks}
- 主題偏好：{dark|light|auto}

## 學習紀錄
- 常見問題：{common_issues}
- 擅長領域：{strengths}
- 需要加強：{weaknesses}
- 最近學習主題：{recent_topics}

## 互動特徵
- 提問風格：{brief|detailed|code-first}
- 回饋頻率：{frequent_adjustments|rarely_adjusts}
- 常用模組：{most_used_modules}
```

#### 管理規則

| 規則 | 說明 |
|------|------|
| 建立時機 | 學員第一次互動時自動建立，填入基本資訊 |
| 更新時機 | 每次對話結束時，由 PreferenceExtractor 判斷是否更新 |
| 載入時機 | 每次 build_enhanced_prompt() 時載入（私人對話） |
| 隱私原則 | 只記錄與技術學習相關的偏好，不記個人隱私 |

### 3.2 Preference Extractor — 偏好自動萃取

#### 核心設計

```python
# preference_extractor.py

class PreferenceExtractor:
    """
    從對話中自動萃取使用者偏好

    萃取時機：
    1. 每次 CLI 執行完成後（從結果和調整中萃取）
    2. 使用者主動說「記住」「我喜歡」「以後都用」時
    3. FeedbackCollector 記錄調整時（整合萃取）

    萃取策略：
    - Phase 1（MVP）：規則式萃取（關鍵字匹配）
    - Phase 2：LLM 萃取（用小模型分析對話）
    """

    def __init__(self, memory_dir: str):
        self.memory_dir = memory_dir

    # ================================================================
    # 主要入口
    # ================================================================

    def extract_and_update(self, student_id: str,
                           user_msg: str,
                           assistant_msg: str,
                           skill_used: str = None):
        """
        從一輪對話中萃取偏好並更新 USER.md

        萃取維度：
        1. 技術偏好（語言、框架、工具）
        2. 風格偏好（暗色主題、簡約風格等）
        3. 互動偏好（詳細解釋 vs 簡潔回答）
        4. 學習狀態（正在學什麼、遇到什麼問題）
        """
        preferences = self._extract_preferences(user_msg, assistant_msg)

        if preferences:
            self._update_user_md(student_id, preferences)
            self._append_daily_log(student_id, user_msg, skill_used, preferences)

    # ================================================================
    # Phase 1: 規則式萃取
    # ================================================================

    def _extract_preferences(self, user_msg: str, assistant_msg: str) -> dict:
        """規則式偏好萃取"""
        prefs = {}
        msg = user_msg.lower()

        # 1. 主動記憶指令
        memory_triggers = ['記住', '以後都', '我喜歡', '我偏好', '我習慣',
                          'remember', '幫我記', '預設用']
        if any(t in msg for t in memory_triggers):
            prefs['explicit_preference'] = user_msg

        # 2. 技術偏好
        tech_keywords = {
            'python': ('language', 'Python'),
            'javascript': ('language', 'JavaScript'),
            'typescript': ('language', 'TypeScript'),
            'react': ('framework', 'React'),
            'vue': ('framework', 'Vue'),
            'fastapi': ('framework', 'FastAPI'),
            'tailwind': ('framework', 'TailwindCSS'),
            'docker': ('tool', 'Docker'),
        }
        for keyword, (category, value) in tech_keywords.items():
            if keyword in msg:
                prefs.setdefault('tech', []).append({category: value})

        # 3. 風格偏好（整合 FeedbackCollector 的萃取邏輯）
        style_map = {
            '暗色': ('theme', 'dark'), '深色': ('theme', 'dark'),
            'dark': ('theme', 'dark'), '亮色': ('theme', 'light'),
            '簡約': ('style', 'minimal'), '現代': ('style', 'modern'),
            '詳細': ('response_style', 'detailed'),
            '簡潔': ('response_style', 'concise'),
            '步驟': ('response_style', 'step-by-step'),
        }
        for keyword, (name, value) in style_map.items():
            if keyword in msg:
                prefs.setdefault('style', {})[name] = value

        # 4. 學習主題偵測
        learning_keywords = ['怎麼', '如何', '教我', '學習', '不懂', '什麼是']
        if any(k in msg for k in learning_keywords):
            # 從 assistant_msg 中提取主題
            prefs['learning_topic'] = user_msg[:100]

        return prefs

    # ================================================================
    # 更新 USER.md
    # ================================================================

    def _update_user_md(self, student_id: str, preferences: dict):
        """更新使用者偏好檔案"""
        user_md_path = os.path.join(self.memory_dir, student_id, 'USER.md')

        # 讀取現有內容
        existing = self._read_user_md(student_id)

        # 合併偏好（不覆蓋，追加或更新）
        merged = self._merge_preferences(existing, preferences)

        # 寫回
        self._write_user_md(student_id, merged)

    # ================================================================
    # 每日日誌
    # ================================================================

    def _append_daily_log(self, student_id: str, user_msg: str,
                          skill_used: str, preferences: dict):
        """追加每日日誌"""
        today = datetime.now().strftime('%Y-%m-%d')
        daily_dir = os.path.join(self.memory_dir, student_id, 'daily')
        os.makedirs(daily_dir, exist_ok=True)

        log_path = os.path.join(daily_dir, f'{today}.md')
        timestamp = datetime.now().strftime('%H:%M')

        entry = f"\n## {timestamp}\n"
        entry += f"- 請求：{user_msg[:150]}\n"
        if skill_used:
            entry += f"- 模組：{skill_used}\n"
        if preferences:
            entry += f"- 萃取偏好：{json.dumps(preferences, ensure_ascii=False)}\n"

        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(entry)
```

### 3.3 Memory Search Engine — 語意搜尋

#### 核心設計

```python
# memory_search.py

class MemorySearchEngine:
    """
    語意搜尋引擎

    支援兩種搜尋模式：
    1. 向量搜尋（Embedding similarity）
    2. 混合搜尋（Vector + BM25 keyword）

    Embedding 來源（按優先級）：
    1. 3090 Compute Plane Embedding API（如果可用）
    2. 外部 API（OpenAI text-embedding-3-small）
    3. 本地小模型（fallback）
    """

    def __init__(self, memory_dir: str, compute_client=None,
                 embedding_provider: str = 'compute'):
        self.memory_dir = memory_dir
        self.compute_client = compute_client
        self.embedding_provider = embedding_provider

    # ================================================================
    # 搜尋介面
    # ================================================================

    def search(self, student_id: str, query: str,
               top_k: int = 5, mode: str = 'hybrid') -> list:
        """
        搜尋學員的記憶

        Args:
            student_id: 學員 ID
            query: 搜尋查詢
            top_k: 返回前 N 個結果
            mode: 'vector' | 'keyword' | 'hybrid'

        Returns:
            list of {content, source, score, line_range}
        """
        if mode == 'hybrid':
            return self._hybrid_search(student_id, query, top_k)
        elif mode == 'vector':
            return self._vector_search(student_id, query, top_k)
        else:
            return self._keyword_search(student_id, query, top_k)

    # ================================================================
    # 索引管理
    # ================================================================

    def index_student_memory(self, student_id: str):
        """
        為學員建立/更新搜尋索引

        索引範圍：
        - USER.md
        - MEMORY.md
        - daily/*.md（最近 30 天）
        - conversations/*.jsonl（最近 7 天）
        """
        memory_path = os.path.join(self.memory_dir, student_id)
        chunks = self._collect_and_chunk(memory_path)
        embeddings = self._batch_embed(chunks)
        self._store_index(student_id, chunks, embeddings)

    def _collect_and_chunk(self, memory_path: str) -> list:
        """
        收集並切分記憶檔案為搜尋用的 chunks

        切分策略：
        - 每個 chunk 約 400 tokens
        - 按 ## 標題分段
        - 保留來源檔案和行號資訊
        """
        chunks = []

        # USER.md
        user_md = os.path.join(memory_path, 'USER.md')
        if os.path.exists(user_md):
            chunks.extend(self._chunk_file(user_md, 'USER.md'))

        # MEMORY.md
        memory_md = os.path.join(memory_path, 'MEMORY.md')
        if os.path.exists(memory_md):
            chunks.extend(self._chunk_file(memory_md, 'MEMORY.md'))

        # 每日日誌（最近 30 天）
        daily_dir = os.path.join(memory_path, 'daily')
        if os.path.isdir(daily_dir):
            cutoff = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            for f in sorted(os.listdir(daily_dir)):
                if f >= cutoff and f.endswith('.md'):
                    chunks.extend(self._chunk_file(
                        os.path.join(daily_dir, f), f'daily/{f}'))

        return chunks

    # ================================================================
    # 混合搜尋
    # ================================================================

    def _hybrid_search(self, student_id: str, query: str, top_k: int) -> list:
        """
        混合搜尋：向量相似度 + BM25 關鍵字

        finalScore = vector_weight × vector_score + text_weight × text_score

        預設權重：vector=0.7, text=0.3
        """
        vector_results = self._vector_search(student_id, query, top_k * 2)
        keyword_results = self._keyword_search(student_id, query, top_k * 2)

        # 合併計分
        VECTOR_WEIGHT = 0.7
        TEXT_WEIGHT = 0.3

        scored = {}
        for r in vector_results:
            key = (r['source'], r['line_range'])
            scored[key] = {
                **r,
                'final_score': VECTOR_WEIGHT * r['score']
            }

        for r in keyword_results:
            key = (r['source'], r['line_range'])
            if key in scored:
                scored[key]['final_score'] += TEXT_WEIGHT * r['score']
            else:
                scored[key] = {
                    **r,
                    'final_score': TEXT_WEIGHT * r['score']
                }

        # 排序返回
        results = sorted(scored.values(), key=lambda x: -x['final_score'])
        return results[:top_k]

    # ================================================================
    # Embedding
    # ================================================================

    def _get_embedding(self, text: str) -> list:
        """
        取得文本的 embedding 向量

        優先使用 3090 Compute Plane 的 Embedding API
        """
        if self.compute_client and self.embedding_provider == 'compute':
            try:
                return self.compute_client.embed(text)
            except Exception:
                pass  # fallback

        # Fallback: 使用簡單的 TF-IDF 向量（不需要外部服務）
        return self._tfidf_embedding(text)
```

#### SQLite 索引結構

```sql
-- memory/{student_id}/index.db

CREATE TABLE IF NOT EXISTS chunks (
    chunk_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,          -- 來源檔案 (USER.md, MEMORY.md, daily/2026-01-30.md)
    line_start INTEGER,
    line_end INTEGER,
    content TEXT NOT NULL,
    embedding BLOB,                -- 向量 (float32 array)
    updated_at TEXT NOT NULL
);

CREATE INDEX idx_source ON chunks(source);

-- BM25 全文搜尋
CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts
USING fts5(content, source, content=chunks, content_rowid=chunk_id);
```

### 3.4 Redis TTL 延長 + 對話持久化

#### 變更項目

```python
# proxy.py 修改

# ====== 變更 1: Redis TTL 從 7天延長到 90天 ======
def save_conversation(student_id: str, user_msg: str, assistant_msg: str):
    key = f'conversation:{student_id}'
    entry = json.dumps({
        'timestamp': datetime.now().isoformat(),
        'user': user_msg,
        'assistant': assistant_msg,
        'backend': CLI_BACKEND
    }, ensure_ascii=False)
    r.rpush(key, entry)
    r.expire(key, 86400 * 90)  # 改為 90 天（原 7 天）

# ====== 變更 2: 定期備份到 JSONL 檔案 ======
def backup_conversations_to_file(student_id: str):
    """
    將 Redis 中的對話備份到 JSONL 檔案

    每日執行一次（由 heartbeat 觸發）
    確保即使 Redis TTL 過期，對話紀錄仍保留
    """
    key = f'conversation:{student_id}'
    entries = r.lrange(key, 0, -1)

    if not entries:
        return

    today = datetime.now().strftime('%Y-%m-%d')
    backup_dir = os.path.join(MEMORY_DIR, student_id, 'conversations')
    os.makedirs(backup_dir, exist_ok=True)

    backup_path = os.path.join(backup_dir, f'{today}.jsonl')

    with open(backup_path, 'a', encoding='utf-8') as f:
        for entry in entries:
            f.write(entry.decode() if isinstance(entry, bytes) else entry)
            f.write('\n')

# ====== 變更 3: Heartbeat 觸發備份 ======
# 在 heartbeat loop 中加入：
# - 每日凌晨 3:00 執行 backup_conversations_to_file
# - 清理超過 90 天的 JSONL 備份檔
```

### 3.5 自動記憶增強 — 偏好萃取整合

#### 現有流程（proxy.py:593-596）

```python
# 現有：只記任務和 skill
if final_message and len(final_message) > 100:
    summary = f"- 任務：{original_prompt[:100]}\n- 使用 Skill：{session.active_skill}"
    self.memory_manager.update_memory(session.student_id, summary)
```

#### 增強後流程

```python
# 增強版：萃取偏好 + 更新 USER.md + 寫入每日日誌
if final_message:
    # 1. 偏好萃取 + USER.md 更新 + 每日日誌
    self.preference_extractor.extract_and_update(
        student_id=session.student_id,
        user_msg=original_prompt,
        assistant_msg=final_message[:500],
        skill_used=session.active_skill
    )

    # 2. 長期記憶更新（增強格式）
    if len(final_message) > 100:
        summary = (
            f"- 任務：{original_prompt[:150]}\n"
            f"- 模組：{session.active_skill}\n"
            f"- 結果：{'成功' if exit_code == 0 else '失敗'}\n"
        )
        self.memory_manager.update_memory(session.student_id, summary)

    # 3. 更新搜尋索引（非同步）
    threading.Thread(
        target=self.memory_search.index_student_memory,
        args=(session.student_id,),
        daemon=True
    ).start()

    # 4. 儲存對話到 Redis（延長 TTL）
    save_conversation(session.student_id, original_prompt, final_message)
```

### 3.6 build_enhanced_prompt 增強

#### 現有流程

```
SOUL.md → AGENTS.md → MEMORY.md (最近50行) → Skill → History (5輪) → User Prompt
```

#### 增強後流程

```
SOUL.md → AGENTS.md → USER.md (偏好畫像) → MEMORY.md (語意搜尋相關段落)
→ 每日日誌 (今天+昨天) → Skill → History (5輪) → User Prompt
```

```python
def build_enhanced_prompt(self, student_id: str, prompt: str,
                          skill: Optional[Skill] = None) -> str:
    parts = []

    # 1. System Context（不變）
    system_context = self.context_manager.build_system_context()
    if system_context:
        parts.append(system_context)

    # 2.【新增】USER.md — 使用者偏好畫像
    user_profile = self._read_user_md(student_id)
    if user_profile:
        parts.append(f"<user-profile>\n{user_profile}\n</user-profile>")

    # 3.【增強】MEMORY.md — 語意搜尋取代截斷
    relevant_memories = self.memory_search.search(
        student_id, prompt, top_k=5, mode='hybrid'
    )
    if relevant_memories:
        memory_text = '\n\n'.join(
            f"[{m['source']}] {m['content']}" for m in relevant_memories
        )
        parts.append(f"<relevant-memories>\n{memory_text}\n</relevant-memories>")

    # 4.【新增】每日日誌（今天+昨天）
    daily_context = self._get_recent_daily_logs(student_id, days=2)
    if daily_context:
        parts.append(f"<recent-activity>\n{daily_context}\n</recent-activity>")

    # 5. Skill Content（不變）
    if skill:
        parts.append(f"<active-skill name=\"{skill.name}\">\n{skill.content}\n</active-skill>")

    # 6. Conversation History（不變）
    history = get_conversation_history(student_id, limit=5)
    if history:
        history_text = []
        for entry in history:
            history_text.append(f"Human: {entry['user']}")
            history_text.append(f"Assistant: {entry['assistant'][:300]}...")
        parts.append(f"<conversation-history>\n" + "\n".join(history_text) + "\n</conversation-history>")

    # 7. User Prompt（不變）
    parts.append(f"<user-request>\n{prompt}\n</user-request>")

    full_prompt = "\n\n".join(parts)
    full_prompt += "\n\n請根據以上資訊，使用繁體中文回應學員的請求。如果學員有偏好設定，請優先遵循。"

    return full_prompt
```

### 3.7 AGENTS.md 更新 — 加入偏好管理規則

在現有 `context/AGENTS.md` 中新增以下區塊：

```markdown
## 偏好管理

### 偵測使用者偏好
當學員表達以下意圖時，視為偏好設定：
- 「記住…」「以後都…」「我喜歡…」「預設用…」
- 重複的調整請求（同類型出現 2 次以上）
- 明確的技術選擇（「用 React」「我習慣 Python」）

### 更新原則
- 偏好變更需記錄到學員的 USER.md
- 不覆蓋現有偏好，除非學員明確要求
- 記錄變更理由和時間

### 查詢記憶
如果需要回顧過去的對話或決定：
- 使用 memory_search 搜尋相關記憶
- 優先查看 USER.md 中的偏好設定
- 參考最近的每日日誌
```

---

## 四、修改檔案清單

### 新增檔案

| 檔案 | 說明 | 優先級 |
|------|------|--------|
| `preference_extractor.py` | 偏好自動萃取器 | P0 |
| `memory_search.py` | 語意搜尋引擎 | P1 |
| `memory/{student_id}/USER.md` | 使用者偏好畫像（動態生成） | P0 |
| `memory/{student_id}/daily/*.md` | 每日日誌（動態生成） | P0 |
| `memory/{student_id}/conversations/*.jsonl` | 對話備份（動態生成） | P1 |
| `memory/{student_id}/index.db` | 搜尋索引（動態生成） | P1 |

### 修改檔案

| 檔案 | 修改內容 | 優先級 |
|------|----------|--------|
| `proxy.py` | Redis TTL 延長、build_enhanced_prompt 增強、自動記憶增強、對話備份、新 API 端點 | P0 |
| `context/AGENTS.md` | 加入偏好管理規則 | P0 |
| `feedback_collector.py` | 整合 PreferenceExtractor 呼叫 | P1 |

### 不修改的檔案

| 檔案 | 原因 |
|------|------|
| `context/SOUL.md` | 全域身份，不涉及個人化 |
| `agent_executor.py` | 記憶整合在 proxy 層處理 |
| `orchestrator.py` | 模組編排邏輯不變 |
| `progress_emitter.py` | 進度顯示邏輯不變 |
| `compute_client.py` | Compute Plane 介面不變 |

---

## 五、新增 API 端點

| 端點 | 方法 | 說明 |
|------|------|------|
| `/api/v1/user/{student_id}` | GET | 取得使用者偏好畫像 |
| `/api/v1/user/{student_id}` | PUT | 更新使用者偏好 |
| `/api/v1/memory/{student_id}/search` | POST | 語意搜尋記憶 |
| `/api/v1/memory/{student_id}/daily` | GET | 取得每日日誌 |

---

## 六、實作階段計畫

### Phase A: 偏好基礎（P0 必要）

```
目標：USER.md + 偏好萃取 + Redis TTL 延長

修改：
1. 建立 preference_extractor.py
   - 規則式偏好萃取
   - USER.md 讀寫
   - 每日日誌寫入

2. 修改 proxy.py
   - Redis TTL: 7天 → 90天
   - build_enhanced_prompt() 注入 USER.md
   - 自動記憶增強（加入偏好萃取呼叫）
   - 每日日誌載入

3. 更新 context/AGENTS.md
   - 加入偏好管理規則

驗證：
- 第一次對話自動建立 USER.md
- 偏好關鍵字被正確萃取
- build_enhanced_prompt 包含 user-profile 標籤
- Redis TTL 確認為 90 天
```

### Phase B: 對話持久化（P1 重要）

```
目標：對話備份 + JSONL 持久化

修改：
1. proxy.py 新增 backup_conversations_to_file()
2. heartbeat 加入每日備份觸發
3. build_enhanced_prompt 加入每日日誌

驗證：
- conversations/ 目錄有 JSONL 檔案
- heartbeat 定時觸發備份
- 90 天後仍可透過 JSONL 查詢歷史對話
```

### Phase C: 語意搜尋（P1 重要）

```
目標：向量搜尋引擎 + 混合搜尋

修改：
1. 建立 memory_search.py
   - SQLite 索引建立
   - 向量搜尋（使用 3090 Embedding API 或 TF-IDF fallback）
   - BM25 關鍵字搜尋
   - 混合搜尋合併計分

2. 修改 proxy.py
   - build_enhanced_prompt: MEMORY.md 截斷 → 語意搜尋
   - CLI 執行後觸發索引更新
   - 新增 /api/v1/memory/{student_id}/search 端點

依賴：
- 3090 Embedding API（可選，有 TF-IDF fallback）
- sqlite3（Python 內建）

驗證：
- 搜尋 "React" 能找到相關記憶
- 舊的記憶（超過 50 行）仍可被搜尋到
- 混合搜尋分數正確合併
```

### Phase D: FeedbackCollector 整合（P2 優化）

```
目標：將 feedback_collector 的參數萃取整合進 PreferenceExtractor

修改：
1. feedback_collector.py
   - record_adjustment 時呼叫 PreferenceExtractor
   - 高頻參數自動更新 USER.md

2. 新增 /api/v1/user/{student_id} API

驗證：
- 使用者調整「改暗色主題」→ USER.md 自動記錄 theme=dark
- 同一偏好出現 3 次 → 標記為 suggested_default
```

---

## 七、風險與限制

### 技術風險

| 風險 | 影響 | 緩解措施 |
|------|------|----------|
| 3090 Embedding API 不穩定 | 向量搜尋降級 | TF-IDF fallback，不依賴外部服務 |
| SQLite 並發寫入衝突 | 索引更新失敗 | WAL 模式 + 寫入鎖 + 重試 |
| 偏好萃取誤判 | USER.md 寫入錯誤偏好 | 規則式保守萃取，只記高信心偏好 |
| Redis 記憶體壓力（TTL 延長） | Redis OOM | 設定 maxmemory-policy + JSONL 備份後可清理 |

### 設計限制

| 限制 | 說明 |
|------|------|
| Phase 1 為規則式萃取 | 無法捕捉隱含偏好，需後續升級 LLM 萃取 |
| 語意搜尋精度受 Embedding 品質影響 | TF-IDF fallback 精度有限 |
| USER.md 無版本控制 | 偏好變更歷史需透過 git 或每日日誌追蹤 |
| 不支援跨學員偏好分析 | 每位學員獨立，無法做群體偏好統計 |

---

## 八、驗收標準

### 功能驗收

| # | 驗收項目 | 預期結果 |
|---|----------|----------|
| 1 | 新學員首次對話 | 自動建立 `memory/{student_id}/USER.md` |
| 2 | 學員說「我喜歡暗色主題」 | USER.md 更新 theme=dark |
| 3 | 查詢 30 天前的對話內容 | 語意搜尋找到相關記憶 |
| 4 | Redis 重啟後 | JSONL 備份檔仍保留對話紀錄 |
| 5 | build_enhanced_prompt 輸出 | 包含 user-profile + relevant-memories 標籤 |
| 6 | /api/v1/memory/{student_id}/search | 返回語意相關的記憶片段 |
| 7 | 每日日誌 | `daily/YYYY-MM-DD.md` 記錄每次互動 |
| 8 | 連續 3 次要求暗色主題 | USER.md 中 theme=dark 標記為強偏好 |

### 非功能驗收

| # | 驗收項目 | 預期結果 |
|---|----------|----------|
| 1 | 偏好萃取延遲 | < 100ms（規則式，不影響回應時間） |
| 2 | 語意搜尋延遲 | < 500ms（含 embedding） |
| 3 | 索引更新 | 非同步執行，不阻塞主流程 |
| 4 | 記憶檔案大小 | 單一學員 < 10MB |

---

## 九、與 OpenSpec v3 的對應關係

本次增強在 OpenSpec v3 架構中的位置：

| OpenSpec v3 組件 | 本次增強 | 對應 |
|-----------------|----------|------|
| Ingress Step 1: Identify | USER.md 載入 | 身份識別後立即載入使用者偏好 |
| Ingress Step 2: Session | Redis TTL 延長 + JSONL 備份 | Session 持久化增強 |
| Ingress Step 7: Planner Decision | build_enhanced_prompt 增強 | Planner 收到完整使用者上下文 |
| Ingress Step 10: Audit | 每日日誌 + 偏好變更紀錄 | 可追蹤的使用者行為記錄 |
| Data Model: StudentProfile | USER.md | 使用者偏好畫像的檔案實作 |

---

## 十、附錄

### A. 現有程式碼參考位置

| 功能 | 檔案 | 行號/函數 |
|------|------|-----------|
| MemoryManager 類別 | proxy.py | ~131-167 |
| build_enhanced_prompt | proxy.py | ~369-418 |
| 自動記憶更新 | proxy.py | ~593-596 |
| save_conversation（Redis TTL） | proxy.py | ~724-735 |
| FeedbackCollector | feedback_collector.py | 全檔 |
| classify_adjustment | feedback_collector.py | ~27-40 |
| extract_params | feedback_collector.py | ~54-100 |

### B. 相關服務狀態

| 服務 | 位置 | 狀態 |
|------|------|------|
| super-happy-coder (proxy) | macmini2 | 運行中 |
| 3090 Compute Plane | ac-3090 | 運行中（Embedding API 可用） |
| Redis | macmini2 localhost:6379 | 運行中 |
| TG Student Bot | macmini2 | 運行中 |
| TG Admin Bot | macmini2 | 運行中 |

---

## 變更日誌

| 日期 | 版本 | 說明 |
|------|------|------|
| 2026-01-30 | v1.0 | 初版 SDD，含 USER.md、語意搜尋、偏好萃取、Redis TTL 延長 |
