#!/usr/bin/env python3
"""
SecondBrain 知識 Wiki 編譯器

功能：
1. 讀取 .map-state.json 取得上次編譯 SHA
2. 用 git diff 找出新增/修改的筆記，判斷影響哪些主題
3. 對每個受影響主題，收集所有筆記的 frontmatter + 前 500 字
4. 產出 prompt 檔到 compiled/.prompts/，供 Claude Code session 處理
5. 處理完成後更新 .map-state.json

用法：
  python3 compile.py --topic ai-agent          # 只編譯指定主題
  python3 compile.py --full                    # 全部主題重編
  python3 compile.py --dry-run                 # 只顯示會做什麼
  python3 compile.py --dry-run --topic ai-agent
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

# ── 匯入 build-knowledge-map 的共用邏輯 ──
sys.path.insert(0, str(Path(__file__).resolve().parent))
from importlib import import_module

_bkm = import_module("build-knowledge-map")

CONCEPTS = _bkm.CONCEPTS
REPO_ROOT = _bkm.REPO_ROOT
COMPILED_DIR = _bkm.COMPILED_DIR
STATE_FILE = _bkm.STATE_FILE
SKIP_DIRS = _bkm.SKIP_DIRS
SKIP_FILES = _bkm.SKIP_FILES
get_git_sha = _bkm.get_git_sha
get_changed_files_since = _bkm.get_changed_files_since
parse_frontmatter = _bkm.parse_frontmatter
match_note_to_concepts = _bkm.match_note_to_concepts
scan_all_notes = _bkm.scan_all_notes

PROMPTS_DIR = COMPILED_DIR / ".prompts"
CONCEPT_SLUGS = {c["slug"] for c in CONCEPTS}


def load_state():
    """讀取編譯狀態"""
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_sha": None, "last_build": None, "note_count": 0}


def save_state(state, sha):
    """更新編譯狀態（追加 compile 欄位，不覆蓋 build 欄位）"""
    state["last_compile_sha"] = sha
    state["last_compile"] = datetime.now().isoformat()
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def find_affected_topics(state, force_full):
    """找出需要重新編譯的主題 slug 集合"""
    if force_full:
        return {c["slug"] for c in CONCEPTS}

    last_sha = state.get("last_compile_sha") or state.get("last_sha")
    if not last_sha:
        print("  ℹ️  無上次編譯記錄，走全量")
        return {c["slug"] for c in CONCEPTS}

    changed = get_changed_files_since(last_sha)
    if changed is None:
        print("  ⚠️  git diff 失敗，走全量")
        return {c["slug"] for c in CONCEPTS}
    if not changed:
        print(f"  ✅ 沒有變更（since {last_sha[:8]}）")
        return set()

    print(f"  📝 {len(changed)} 個檔案變更（since {last_sha[:8]}）")

    # 對每個變更的 .md 檔案，判斷它屬於哪些主題
    affected = set()
    for relpath in changed:
        if not relpath.endswith(".md"):
            continue
        filepath = REPO_ROOT / relpath
        if not filepath.exists():
            continue
        fm, body = parse_frontmatter(str(filepath))
        if fm is None:
            fm = {}
        concepts = match_note_to_concepts(fm, body, str(filepath))
        for c in concepts:
            affected.add(c["slug"])

    return affected


def gather_topic_notes(slug, all_notes):
    """收集某主題下所有筆記的 frontmatter + 前 500 字內容"""
    matched = [n for n in all_notes if any(c["slug"] == slug for c in n["concepts"])]
    matched.sort(key=lambda n: n["date"], reverse=True)

    entries = []
    for note in matched:
        filepath = REPO_ROOT / note["path"]
        fm, body = parse_frontmatter(str(filepath))
        if fm is None:
            fm = {}

        # 取前 500 字（字元），保留結構
        snippet = body.strip()[:500]
        if len(body.strip()) > 500:
            snippet += "\n(...截斷)"

        entries.append({
            "filename": Path(note["path"]).stem,
            "path": note["path"],
            "title": note["title"],
            "date": note["date"],
            "tags": note.get("tags", []),
            "category": note.get("category", ""),
            "snippet": snippet,
        })

    return entries


def build_prompt(slug, concept, entries):
    """為一個主題產生 LLM prompt"""
    name = concept["name"]
    desc = concept["description"]
    count = len(entries)

    lines = [
        f"# 任務：編譯「{name}」知識 Wiki 頁",
        "",
        f"你是 SecondBrain 知識編譯器。以下是「{name}」主題下的 {count} 篇筆記摘要。",
        f"主題描述：{desc}",
        "",
        "## 要求",
        "",
        "請根據以下筆記內容，產出一篇結構化的知識 Wiki 頁，格式如下：",
        "",
        "```",
        "---",
        f'title: "{name} — 知識 Wiki"',
        f"date: {datetime.now().strftime('%Y-%m-%d')}",
        "type: wiki",
        "content_layer: L3",
        f"topic: {slug}",
        f"source_count: {count}",
        f"last_compiled: {datetime.now().strftime('%Y-%m-%d')}",
        "_skip_sync: true",
        "---",
        "",
        "# {主題名稱} — 知識 Wiki",
        "",
        "## 主題概述",
        "(2-3 段，概括此主題的核心範圍、為何重要、目前發展階段)",
        "",
        "## 核心概念",
        "(列出 5-10 個核心概念，每個用 ### 小節，2-3 句說明 + Wiki Link 引用來源筆記)",
        "",
        "## 關鍵發現",
        "(從筆記中提煉的重要洞見，每條用 > blockquote + 來源 Wiki Link)",
        "",
        "## 跨筆記關聯",
        "(不同筆記之間的連結、矛盾、演進關係)",
        "",
        "## 待探索方向",
        "(筆記中提到但尚未深入的議題，供未來研究)",
        "```",
        "",
        "## 引用規則",
        "",
        "- 每個段落都必須用 `[[note-filename]]` 或 `[[note-filename|顯示名稱]]` Wiki Link 引用來源筆記",
        "- filename 就是下方每篇筆記的 `filename` 欄位（不含 .md）",
        "- 不要虛構不存在的筆記名稱",
        "",
        "---",
        "",
        f"## 筆記清單（共 {count} 篇）",
        "",
    ]

    for i, e in enumerate(entries, 1):
        tags_str = ", ".join(str(t) for t in e["tags"]) if e["tags"] else "(無)"
        lines.append(f"### [{i}/{count}] {e['title']}")
        lines.append(f"- **filename**: `{e['filename']}`")
        lines.append(f"- **path**: `{e['path']}`")
        lines.append(f"- **date**: {e['date']}")
        lines.append(f"- **category**: {e['category']}")
        lines.append(f"- **tags**: {tags_str}")
        lines.append("")
        lines.append("**內容摘要：**")
        lines.append("")
        lines.append(e["snippet"])
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="SecondBrain 知識 Wiki 編譯器")
    parser.add_argument("--topic", type=str, help="只編譯指定主題 slug（如 ai-agent）")
    parser.add_argument("--full", action="store_true", help="全部主題重編")
    parser.add_argument("--dry-run", action="store_true", help="只顯示會做什麼，不寫檔")
    args = parser.parse_args()

    # 驗證 --topic
    if args.topic and args.topic not in CONCEPT_SLUGS:
        print(f"❌ 未知主題: {args.topic}")
        print(f"   可用主題: {', '.join(sorted(CONCEPT_SLUGS))}")
        sys.exit(1)

    state = load_state()
    current_sha = get_git_sha()

    # ── Step 1: 判斷哪些主題需要編譯 ──
    print("📋 判斷需要編譯的主題...")
    if args.topic:
        affected = {args.topic}
        print(f"  🎯 指定主題: {args.topic}")
    elif args.full:
        affected = {c["slug"] for c in CONCEPTS}
        print(f"  🔄 全量重編: {len(affected)} 個主題")
    else:
        affected = find_affected_topics(state, force_full=False)

    if not affected:
        print("\n✅ 沒有主題需要編譯")
        return

    print(f"\n📚 掃描所有筆記...")
    all_notes = scan_all_notes()
    print(f"  找到 {len(all_notes)} 篇筆記")

    # ── Step 2: 對每個受影響主題，收集筆記 + 產生 prompt ──
    PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
    summary = []

    for concept in CONCEPTS:
        slug = concept["slug"]
        if slug not in affected:
            continue

        entries = gather_topic_notes(slug, all_notes)
        if not entries:
            print(f"  ⏭️  {concept['name']}: 0 篇，跳過")
            continue

        prompt = build_prompt(slug, concept, entries)
        prompt_path = PROMPTS_DIR / f"{slug}-prompt.md"

        if not args.dry_run:
            with open(prompt_path, "w", encoding="utf-8") as f:
                f.write(prompt)

        # 估算 prompt 字元數
        char_count = len(prompt)
        print(f"  📝 {concept['name']}: {len(entries)} 篇, ~{char_count:,} 字元 → .prompts/{slug}-prompt.md")
        summary.append({
            "slug": slug,
            "name": concept["name"],
            "note_count": len(entries),
            "char_count": char_count,
            "prompt_path": str(prompt_path),
        })

    # ── Step 3: 產出摘要 ──
    if not summary:
        print("\n⚠️  所有主題都沒有筆記，無需編譯")
        return

    summary_path = PROMPTS_DIR / "_compile-plan.json"
    if not args.dry_run:
        with open(summary_path, "w") as f:
            json.dump({
                "created": datetime.now().isoformat(),
                "git_sha": current_sha,
                "topics": summary,
            }, f, indent=2, ensure_ascii=False)

    print(f"\n{'🔍 DRY RUN — 未寫入任何檔案' if args.dry_run else '✅ Prompt 檔已產出'}")
    print(f"   Git SHA: {current_sha[:8]}")
    print(f"   主題數: {len(summary)}")
    total_notes = sum(s["note_count"] for s in summary)
    total_chars = sum(s["char_count"] for s in summary)
    print(f"   總筆記: {total_notes} 篇")
    print(f"   總字元: {total_chars:,}")
    print(f"\n📌 下一步：讀取 compiled/.prompts/{{topic}}-prompt.md 餵給 Claude Code 產出 wiki 頁")

    # ── Step 4: 更新狀態（非 dry-run） ──
    if not args.dry_run:
        save_state(state, current_sha)
        print(f"   狀態已更新: last_compile_sha = {current_sha[:8]}")


if __name__ == "__main__":
    main()
