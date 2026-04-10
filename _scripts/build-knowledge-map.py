#!/usr/bin/env python3
"""
SecondBrain 知識地圖建置腳本

功能：
1. 掃描所有 .md 筆記，讀取 frontmatter
2. 依概念主題分群，建立 compiled/ 下的概念索引檔
3. 每篇索引包含：Wiki Link + 路徑 + 一句話摘要
4. 記錄當前 Git SHA，供後續增量更新
5. 建立 compiled/_index.md 總覽

用法：
  python3 build-knowledge-map.py                # 首次全量建置
  python3 build-knowledge-map.py --update       # 增量更新（比對 Git SHA）
  python3 build-knowledge-map.py --dry-run      # 只顯示會做什麼，不寫檔
"""

import os
import re
import sys
import subprocess
import json
from datetime import datetime
from pathlib import Path

# ── 設定 ──
REPO_ROOT = Path(__file__).resolve().parent.parent
COMPILED_DIR = REPO_ROOT / "compiled"
STATE_FILE = COMPILED_DIR / ".map-state.json"
SKIP_DIRS = {'.git', 'node_modules', '_scripts', 'raw', 'compiled', 'shc-v5'}
SKIP_FILES = {'README.md', 'KNOWLEDGE_SCHEMA.md', 'DISPATCH_RULES.md'}

# ── 概念主題定義 ──
# 每個概念：name, slug, description, match_rules (tags, categories, title_keywords)
CONCEPTS = [
    {
        "name": "AI Agent 架構與實戰",
        "slug": "ai-agent",
        "description": "AI Agent 設計模式、多代理協作、OpenClaw/DesignClaw/MetaClaw 等框架",
        "match": {
            "tags": ["AI Agent", "AI-Agent", "agent", "multi-agent", "OpenClaw", "DesignClaw",
                     "MetaClaw", "Claude-Code", "claude-code", "super-happy-coder", "Super Happy Coder", "SHC"],
            "categories": ["tech/agent"],
            "title_keywords": ["agent", "Agent", "OpenClaw", "DesignClaw", "MetaClaw", "龍蝦",
                              "Claude Code", "claude-code", "SHC", "Super Happy Coder", "多代理"]
        }
    },
    {
        "name": "LLM 技術與模型",
        "slug": "llm-tech",
        "description": "LLM 模型比較、部署、微調、vLLM、量化、prompt engineering",
        "match": {
            "tags": ["LLM", "vLLM", "Gemini", "Claude", "GPT", "Qwen", "SDXL", "ComfyUI",
                     "模型", "token", "prompt", "fine-tune", "abliteration"],
            "categories": ["tech/ai-ml"],
            "title_keywords": ["LLM", "模型", "vLLM", "Gemini", "Claude", "token", "prompt",
                              "ComfyUI", "SDXL", "渲染", "Qwen"]
        }
    },
    {
        "name": "商業模式與策略",
        "slug": "business-strategy",
        "description": "商業分析、市場策略、創業案例、輕資產模式、AI 商業應用",
        "match": {
            "tags": ["SaaS", "商業模式", "strategy", "創業", "business-model", "MEDVi",
                     "market", "投資", "財報", "轉型"],
            "categories": ["business/strategy", "business/marketing", "business-model", "business-analysis"],
            "title_keywords": ["商業", "策略", "財報", "創業", "轉型", "投資", "MEDVi",
                              "Marriott", "Google財報", "StackOverflow"]
        }
    },
    {
        "name": "永續發展與 ESG",
        "slug": "sustainability-esg",
        "description": "ESG、碳管理、永續報告、企業永續轉型、sustainability-100",
        "match": {
            "tags": ["ESG", "永續", "sustainability", "碳管理", "碳盤查", "SDGs"],
            "categories": ["business/sustainability"],
            "title_keywords": ["永續", "ESG", "碳", "sustainability", "SDG"]
        }
    },
    {
        "name": "開發工具與工作流",
        "slug": "dev-tools",
        "description": "開發工具、CLI、自動化腳本、Discord/Telegram bot、DevOps",
        "match": {
            "tags": ["工具", "自動化", "DevOps", "CLI", "Discord", "Telegram", "bot",
                     "NotebookLM", "OCR", "Whisper"],
            "categories": ["tech/tools", "tech/devops", "tech/server-config"],
            "title_keywords": ["工具", "自動化", "bot", "Discord", "Telegram", "CLI",
                              "NotebookLM", "OCR", "Whisper", "部署", "伺服器"]
        }
    },
    {
        "name": "知識管理與第二大腦",
        "slug": "knowledge-management",
        "description": "知識庫架構、SecondBrain、Notion 同步、RAG、Obsidian",
        "match": {
            "tags": ["knowledge-management", "RAG", "SecondBrain", "Notion", "Obsidian",
                     "知識庫", "知識管理", "Qdrant", "向量"],
            "categories": [],
            "title_keywords": ["知識", "RAG", "SecondBrain", "Notion", "Obsidian", "知識庫",
                              "向量", "Qdrant"]
        }
    },
    {
        "name": "室內設計與 DesignClaw",
        "slug": "interior-design",
        "description": "室內設計自動化、DesignClaw pipeline、ComfyUI 渲染、危老都更",
        "match": {
            "tags": ["室內設計", "DesignClaw", "ComfyUI", "interior-design", "危老重建",
                     "都更", "全屋定制"],
            "categories": [],
            "title_keywords": ["室內設計", "DesignClaw", "ComfyUI", "渲染", "interior",
                              "危老", "都更", "傢俱"]
        }
    },
    {
        "name": "教育與學習",
        "slug": "education-learning",
        "description": "課程設計、AI 教育應用、學習方法、個人成長",
        "match": {
            "tags": ["教育", "課程", "學習", "教學", "workshop", "Teachify", "ClassClaw"],
            "categories": ["education/course", "education/workshop", "personal"],
            "title_keywords": ["教育", "課程", "學習", "教學", "青春期", "英語", "認知",
                              "心理", "遊戲開發", "Teachify"]
        }
    },
    {
        "name": "AI 安全與合規",
        "slug": "ai-safety",
        "description": "AI 安全、模型對齊、jailbreak、資安、開源風險",
        "match": {
            "tags": ["安全", "security", "jailbreak", "alignment", "abliteration",
                     "CC-BOS", "資安"],
            "categories": [],
            "title_keywords": ["安全", "security", "jailbreak", "洩漏", "abliterat",
                              "CC-BOS", "資安", "secret"]
        }
    },
    {
        "name": "基礎設施與硬體",
        "slug": "infra-hardware",
        "description": "伺服器配置、3090 GPU、Mac Mini、Raspberry Pi、網路架構",
        "match": {
            "tags": ["3090", "Mac Mini", "Raspberry Pi", "硬體", "server", "GPU",
                     "基礎設施", "Tailscale"],
            "categories": ["tech/server-config"],
            "title_keywords": ["3090", "Mac Mini", "伺服器", "硬體", "GPU", "部署",
                              "Compute Plane", "vLLM", "死當"]
        }
    }
]


def get_git_sha():
    """取得當前 Git HEAD SHA"""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, cwd=REPO_ROOT
        )
        return result.stdout.strip() if result.returncode == 0 else "unknown"
    except:
        return "unknown"


def get_changed_files_since(sha):
    """取得指定 SHA 之後變更的 .md 檔案"""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", sha, "HEAD", "--", "*.md"],
            capture_output=True, text=True, cwd=REPO_ROOT
        )
        if result.returncode == 0:
            return set(result.stdout.strip().split('\n')) if result.stdout.strip() else set()
    except:
        pass
    return None  # None = 無法比對，走全量


def load_state():
    """讀取上次建置狀態"""
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_sha": None, "last_build": None, "note_count": 0}


def save_state(sha, note_count):
    """儲存建置狀態"""
    COMPILED_DIR.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump({
            "last_sha": sha,
            "last_build": datetime.now().isoformat(),
            "note_count": note_count
        }, f, indent=2, ensure_ascii=False)


def parse_frontmatter(filepath):
    """解析 .md 檔案的 YAML frontmatter"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return None, ""

    m = re.match(r'^---\n(.*?)\n---\n?(.*)', content, re.DOTALL)
    if not m:
        return None, content

    try:
        import yaml
        fm = yaml.safe_load(m.group(1))
        return fm or {}, m.group(2)
    except:
        return {}, m.group(2)


def extract_summary_line(fm, body, filepath):
    """從 frontmatter 或 body 提取一句話摘要"""
    # 優先用 frontmatter 的 summary
    if fm and fm.get('summary'):
        s = fm['summary']
        return s.split('\n')[0][:100] if isinstance(s, str) else str(s)[:100]

    # 嘗試從 title 取
    if fm and fm.get('title'):
        return str(fm['title'])[:100]

    # 從檔名推斷
    name = Path(filepath).stem
    # 移除日期前綴
    name = re.sub(r'^\d{4}-\d{2}-\d{2}[-_]?', '', name)
    return name.replace('-', ' ').replace('_', ' ')[:100]


def match_note_to_concepts(fm, body, filepath):
    """判斷筆記屬於哪些概念"""
    matched = []
    tags = set(str(t).lower() for t in (fm.get('tags') or []))
    category = str(fm.get('category', '')).lower()
    title = str(fm.get('title', '')).lower()
    filename = Path(filepath).name.lower()

    for concept in CONCEPTS:
        score = 0
        rules = concept['match']

        # tag 匹配
        for t in rules.get('tags', []):
            if t.lower() in tags:
                score += 2

        # category 匹配
        for c in rules.get('categories', []):
            if c.lower() == category or category.startswith(c.lower()):
                score += 3

        # title/filename 關鍵字匹配
        for kw in rules.get('title_keywords', []):
            if kw.lower() in title or kw.lower() in filename:
                score += 1

        if score >= 2:
            matched.append((concept, score))

    # 按分數排序
    matched.sort(key=lambda x: -x[1])
    return [m[0] for m in matched]


def make_wiki_link(filepath, title):
    """建立 Obsidian Wiki Link 格式"""
    name = Path(filepath).stem
    if title and title != name:
        return f"[[{name}|{title}]]"
    return f"[[{name}]]"


def scan_all_notes():
    """掃描所有筆記"""
    notes = []
    for root, dirs, files in os.walk(REPO_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if not f.endswith('.md') or f in SKIP_FILES:
                continue
            filepath = os.path.join(root, f)
            relpath = os.path.relpath(filepath, REPO_ROOT)

            fm, body = parse_frontmatter(filepath)
            if fm is None:
                fm = {}

            title = fm.get('title', Path(f).stem)
            summary = extract_summary_line(fm, body, filepath)
            concepts = match_note_to_concepts(fm, body, filepath)
            date = str(fm.get('date', ''))

            notes.append({
                'path': relpath,
                'title': title,
                'summary': summary,
                'wiki_link': make_wiki_link(filepath, title),
                'concepts': concepts,
                'date': date,
                'tags': fm.get('tags', []),
                'category': fm.get('category', ''),
            })
    return notes


def build_concept_index(concept, notes):
    """為單一概念建立索引頁"""
    slug = concept['slug']
    name = concept['name']
    desc = concept['description']

    # 篩選屬於此概念的筆記，按日期倒序
    matched = [n for n in notes if any(c['slug'] == slug for c in n['concepts'])]
    matched.sort(key=lambda n: n['date'], reverse=True)

    lines = [
        f"---",
        f'title: "{name}"',
        f"date: {datetime.now().strftime('%Y-%m-%d')}",
        f"type: index",
        f"content_layer: L2",
        f'summary: "{desc}"',
        f"last_compiled: {datetime.now().strftime('%Y-%m-%d')}",
        f"_skip_sync: true",
        f"---",
        f"",
        f"# {name}",
        f"",
        f"> {desc}",
        f"",
        f"共收錄 **{len(matched)}** 篇筆記",
        f"",
        f"---",
        f"",
    ]

    if matched:
        lines.append("| 筆記 | 路徑 | 摘要 | 日期 |")
        lines.append("|------|------|------|------|")
        for n in matched:
            wiki = n['wiki_link']
            path = f"`{n['path']}`"
            summary = n['summary'][:60]
            date = n['date'][:10] if n['date'] else ''
            lines.append(f"| {wiki} | {path} | {summary} | {date} |")

    lines.append("")
    return '\n'.join(lines), len(matched)


def build_master_index(concept_counts, current_sha):
    """建立 compiled/_index.md 總覽"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    total = sum(concept_counts.values())

    lines = [
        "---",
        'title: "SecondBrain 知識地圖"',
        f"date: {datetime.now().strftime('%Y-%m-%d')}",
        "type: index",
        "content_layer: L2",
        "_skip_sync: true",
        "---",
        "",
        "# 🗺️ SecondBrain 知識地圖",
        "",
        f"> 最後更新：{now} | Git SHA：`{current_sha[:8]}` | 總收錄：**{total}** 篇",
        "",
        "---",
        "",
    ]

    for concept in CONCEPTS:
        slug = concept['slug']
        name = concept['name']
        desc = concept['description']
        count = concept_counts.get(slug, 0)
        if count > 0:
            lines.append(f"### [[{slug}|{name}]]")
            lines.append(f"> {desc}")
            lines.append(f"> 📄 {count} 篇筆記")
            lines.append("")

    # 未歸類
    unmatched_count = concept_counts.get('_unmatched', 0)
    if unmatched_count > 0:
        lines.append(f"### 未歸類")
        lines.append(f"> 尚未被分類到任何概念的筆記")
        lines.append(f"> 📄 {unmatched_count} 篇筆記")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 使用方式")
    lines.append("")
    lines.append("1. 看此知識地圖 → 找到相關概念")
    lines.append("2. 進入概念索引頁 → 看各筆記的一句話摘要")
    lines.append("3. 點進具體筆記 → 看頂部的 3-5 句要點")
    lines.append("")
    lines.append("## 更新方式")
    lines.append("")
    lines.append("```bash")
    lines.append("cd SecondBrain && python3 _scripts/build-knowledge-map.py --update")
    lines.append("```")
    lines.append("")

    return '\n'.join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='SecondBrain 知識地圖建置')
    parser.add_argument('--update', action='store_true', help='增量更新（比對 Git SHA）')
    parser.add_argument('--dry-run', action='store_true', help='只顯示不寫檔')
    args = parser.parse_args()

    state = load_state()
    current_sha = get_git_sha()

    if args.update and state.get('last_sha'):
        changed = get_changed_files_since(state['last_sha'])
        if changed is not None and len(changed) == 0:
            print(f"✅ 沒有新的變更（last SHA: {state['last_sha'][:8]}）")
            return
        print(f"📝 偵測到 {len(changed) if changed else '?'} 個變更檔案（since {state['last_sha'][:8]}）")
    else:
        print("🔄 全量建置知識地圖...")

    # 掃描所有筆記
    notes = scan_all_notes()
    print(f"📚 掃描到 {len(notes)} 篇筆記")

    # 建立概念索引
    COMPILED_DIR.mkdir(parents=True, exist_ok=True)
    concept_counts = {}

    for concept in CONCEPTS:
        content, count = build_concept_index(concept, notes)
        concept_counts[concept['slug']] = count
        outpath = COMPILED_DIR / f"{concept['slug']}.md"

        if not args.dry_run:
            with open(outpath, 'w', encoding='utf-8') as f:
                f.write(content)
        print(f"  📁 {concept['name']}: {count} 篇 → compiled/{concept['slug']}.md")

    # 計算未歸類
    classified = set()
    for n in notes:
        if n['concepts']:
            classified.add(n['path'])
    unmatched = [n for n in notes if n['path'] not in classified]
    concept_counts['_unmatched'] = len(unmatched)

    if unmatched:
        # 也輸出未歸類列表
        lines = [
            "---",
            'title: "未歸類筆記"',
            f"date: {datetime.now().strftime('%Y-%m-%d')}",
            "type: index",
            "content_layer: L2",
            "_skip_sync: true",
            "---",
            "",
            "# 未歸類筆記",
            "",
            f"共 **{len(unmatched)}** 篇筆記尚未被分類到任何概念主題。",
            "",
            "| 筆記 | 路徑 | 摘要 | 日期 |",
            "|------|------|------|------|",
        ]
        for n in sorted(unmatched, key=lambda x: x['date'], reverse=True):
            wiki = n['wiki_link']
            path = f"`{n['path']}`"
            summary = n['summary'][:60]
            date = n['date'][:10] if n['date'] else ''
            lines.append(f"| {wiki} | {path} | {summary} | {date} |")

        if not args.dry_run:
            with open(COMPILED_DIR / "_unmatched.md", 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))
        print(f"  ⚠️  未歸類: {len(unmatched)} 篇 → compiled/_unmatched.md")

    # 建立總索引
    master = build_master_index(concept_counts, current_sha)
    if not args.dry_run:
        with open(COMPILED_DIR / "_index.md", 'w', encoding='utf-8') as f:
            f.write(master)
    print(f"\n🗺️  知識地圖總覽 → compiled/_index.md")

    # 儲存狀態
    if not args.dry_run:
        save_state(current_sha, len(notes))
        print(f"\n✅ 完成！Git SHA: {current_sha[:8]}, 共 {len(notes)} 篇, {len(CONCEPTS)} 個概念")
    else:
        print(f"\n🔍 DRY RUN 完成，未寫入任何檔案")


if __name__ == '__main__':
    main()
