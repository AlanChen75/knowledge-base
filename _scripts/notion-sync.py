#!/usr/bin/env python3
"""
notion-sync.py — 將 SecondBrain 的 .md 檔案同步到 Notion Database

用法:
  python3 notion-sync.py                    # 同步所有未同步的檔案
  python3 notion-sync.py --full             # 強制全量同步
  python3 notion-sync.py --dry-run          # 只顯示會同步什麼，不實際執行

環境變數 (放在 ~/SecondBrain/.env):
  NOTION_TOKEN=ntn_xxx
  NOTION_DATABASE_ID=xxx
"""

import os
import sys
import json
import re
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError

# ─── Config ───
SECOND_BRAIN = Path(os.environ.get("SECOND_BRAIN", Path.home() / "SecondBrain"))
if not SECOND_BRAIN.exists():
    # ac-mac uses ~/knowledge-base
    SECOND_BRAIN = Path.home() / "knowledge-base"

ENV_FILE = SECOND_BRAIN / ".env"
SYNC_STATE_FILE = SECOND_BRAIN / "_scripts" / ".notion-sync-state.json"
NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

# Directories to skip
SKIP_DIRS = {"_scripts", "_index", ".git", "resources", "node_modules"}

# ─── Load .env ───
def load_env():
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ.setdefault(key.strip(), val.strip())

    token = os.environ.get("NOTION_TOKEN", "")
    db_id = os.environ.get("NOTION_DATABASE_ID", "")
    if not token or not db_id:
        print("❌ 缺少 NOTION_TOKEN 或 NOTION_DATABASE_ID")
        print(f"   請設定在 {ENV_FILE}")
        sys.exit(1)
    return token, db_id


# ─── Notion API helpers ───
def notion_request(method, path, token, body=None):
    url = f"{NOTION_API}{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
    data = json.dumps(body).encode() if body else None
    req = Request(url, data=data, headers=headers, method=method)
    try:
        with urlopen(req) as resp:
            return json.loads(resp.read())
    except HTTPError as e:
        error_body = e.read().decode()
        print(f"❌ Notion API error {e.code}: {error_body}")
        return None


def find_page_by_filepath(token, db_id, filepath):
    """Check if a page with this FilePath already exists."""
    body = {
        "filter": {
            "property": "FilePath",
            "rich_text": {"equals": filepath}
        }
    }
    result = notion_request("POST", f"/databases/{db_id}/query", token, body)
    if result and result.get("results"):
        return result["results"][0]["id"]
    return None


def create_or_update_page(token, db_id, metadata, content_blocks, page_id=None):
    """Create a new page or update existing one."""
    properties = {
        "Title": {"title": [{"text": {"content": metadata.get("title", "Untitled")}}]},
        "FilePath": {"rich_text": [{"text": {"content": metadata.get("filepath", "")}}]},
        "SyncedAt": {"date": {"start": datetime.now(timezone.utc).isoformat()}},
    }

    if metadata.get("category"):
        properties["Category"] = {"select": {"name": metadata["category"]}}

    if metadata.get("tags"):
        properties["Tags"] = {
            "multi_select": [{"name": t.strip()} for t in metadata["tags"][:10]]
        }

    if metadata.get("source") and metadata["source"].startswith("http"):
        properties["Source"] = {"url": metadata["source"]}

    if metadata.get("date"):
        properties["Date"] = {"date": {"start": metadata["date"]}}

    if metadata.get("type"):
        properties["Type"] = {"select": {"name": metadata["type"]}}

    if page_id:
        # Update existing page properties
        notion_request("PATCH", f"/pages/{page_id}", token, {"properties": properties})
        # Clear existing content and re-add
        # (Notion API doesn't support bulk block replace easily, so we just update properties)
        return page_id
    else:
        body = {
            "parent": {"database_id": db_id},
            "properties": properties,
            "children": content_blocks[:100],  # Notion limit: 100 blocks per request
        }
        result = notion_request("POST", "/pages", token, body)
        return result["id"] if result else None


# ─── Markdown parsing ───
def parse_frontmatter(text):
    """Extract YAML frontmatter from markdown."""
    metadata = {}
    content = text

    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', text, re.DOTALL)
    if match:
        fm_text = match.group(1)
        content = match.group(2)

        for line in fm_text.splitlines():
            if ":" in line:
                key, val = line.split(":", 1)
                key = key.strip().lower()
                val = val.strip()

                if key == "tags":
                    # Handle [tag1, tag2] or - tag1 format
                    val = val.strip("[]")
                    metadata["tags"] = [t.strip().strip("'\"") for t in val.split(",") if t.strip()]
                else:
                    metadata[key] = val.strip("'\"")

    return metadata, content


def md_to_notion_blocks(content):
    """Convert markdown content to Notion block objects (simplified)."""
    blocks = []
    lines = content.strip().split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]

        # Heading
        if line.startswith("### "):
            blocks.append({
                "type": "heading_3",
                "heading_3": {"rich_text": [{"text": {"content": line[4:].strip()}}]}
            })
        elif line.startswith("## "):
            blocks.append({
                "type": "heading_2",
                "heading_2": {"rich_text": [{"text": {"content": line[3:].strip()}}]}
            })
        elif line.startswith("# "):
            blocks.append({
                "type": "heading_1",
                "heading_1": {"rich_text": [{"text": {"content": line[2:].strip()}}]}
            })
        # Bullet list
        elif line.strip().startswith("- "):
            text = line.strip()[2:]
            blocks.append({
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"text": {"content": text[:2000]}}]}
            })
        # Numbered list
        elif re.match(r'^\d+\.\s', line.strip()):
            text = re.sub(r'^\d+\.\s', '', line.strip())
            blocks.append({
                "type": "numbered_list_item",
                "numbered_list_item": {"rich_text": [{"text": {"content": text[:2000]}}]}
            })
        # Code block
        elif line.strip().startswith("```"):
            lang = line.strip().lstrip("`").strip().lower() or "plain text"
            lang = LANG_ALIASES.get(lang, lang)
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            blocks.append({
                "type": "code",
                "code": {
                    "rich_text": [{"text": {"content": "\n".join(code_lines)[:2000]}}],
                    "language": lang if lang in NOTION_LANGUAGES else "plain text"
                }
            })
        # Empty line → skip
        elif not line.strip():
            pass
        # Regular paragraph
        else:
            # Collect consecutive non-special lines
            para_lines = [line]
            while (i + 1 < len(lines)
                   and lines[i + 1].strip()
                   and not lines[i + 1].startswith("#")
                   and not lines[i + 1].strip().startswith("- ")
                   and not lines[i + 1].strip().startswith("```")
                   and not re.match(r'^\d+\.\s', lines[i + 1].strip())):
                i += 1
                para_lines.append(lines[i])

            text = " ".join(l.strip() for l in para_lines)
            if text:
                blocks.append({
                    "type": "paragraph",
                    "paragraph": {"rich_text": [{"text": {"content": text[:2000]}}]}
                })

        i += 1

    return blocks


NOTION_LANGUAGES = {
    "python", "javascript", "typescript", "bash", "shell", "json", "yaml",
    "html", "css", "sql", "java", "c", "c++", "c#", "go", "rust", "ruby",
    "plain text", "markdown", "docker", "toml", "kotlin", "swift", "r",
    "php", "scala", "dart", "lua", "perl", "xml", "graphql", "mermaid",
}

# Common aliases → Notion's expected language name
LANG_ALIASES = {
    "dockerfile": "docker",
    "js": "javascript",
    "ts": "typescript",
    "py": "python",
    "rb": "ruby",
    "rs": "rust",
    "sh": "shell",
    "zsh": "shell",
    "cpp": "c++",
    "csharp": "c#",
    "yml": "yaml",
}


# ─── Sync state management ───
def load_sync_state():
    if SYNC_STATE_FILE.exists():
        return json.loads(SYNC_STATE_FILE.read_text())
    return {}


def save_sync_state(state):
    SYNC_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    SYNC_STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False))


def file_hash(path):
    return hashlib.md5(path.read_bytes()).hexdigest()


# ─── Main sync ───
def collect_md_files(root):
    """Collect all .md files, excluding skip dirs."""
    files = []
    for p in sorted(root.rglob("*.md")):
        # Skip hidden and excluded dirs
        parts = p.relative_to(root).parts
        if any(part.startswith(".") or part in SKIP_DIRS for part in parts):
            continue
        files.append(p)
    return files


def infer_category(filepath, metadata):
    """Infer category from filepath or frontmatter."""
    if metadata.get("category"):
        return metadata["category"]

    parts = filepath.parts
    if len(parts) >= 2:
        return parts[0]  # top-level directory name
    return "uncategorized"


def sync_file(token, db_id, md_path, root, dry_run=False):
    """Sync a single .md file to Notion."""
    rel_path = str(md_path.relative_to(root))
    text = md_path.read_text(encoding="utf-8", errors="replace")
    metadata, content = parse_frontmatter(text)

    # Enrich metadata
    metadata["filepath"] = rel_path
    metadata.setdefault("title", md_path.stem.replace("-", " ").replace("_", " "))
    metadata["category"] = infer_category(md_path.relative_to(root), metadata)

    # Infer date from filename if not in frontmatter
    if not metadata.get("date"):
        date_match = re.match(r'(\d{4}-\d{2}-\d{2})', md_path.name)
        if date_match:
            metadata["date"] = date_match.group(1)

    if dry_run:
        tags_str = ", ".join(metadata.get("tags", []))
        print(f"  📄 {rel_path}")
        print(f"     title: {metadata['title']}")
        print(f"     category: {metadata['category']}, tags: [{tags_str}]")
        return True

    # Convert content to Notion blocks
    blocks = md_to_notion_blocks(content)

    # Check if page exists
    page_id = find_page_by_filepath(token, db_id, rel_path)

    if page_id:
        create_or_update_page(token, db_id, metadata, blocks, page_id=page_id)
        print(f"  ♻️  更新: {rel_path}")
    else:
        new_id = create_or_update_page(token, db_id, metadata, blocks)
        if new_id:
            print(f"  ✅ 新增: {rel_path}")
        else:
            print(f"  ❌ 失敗: {rel_path}")
            return False

    return True


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Sync SecondBrain to Notion")
    parser.add_argument("--full", action="store_true", help="Force full sync")
    parser.add_argument("--dry-run", action="store_true", help="Show what would sync")
    args = parser.parse_args()

    load_env()
    token, db_id = os.environ["NOTION_TOKEN"], os.environ["NOTION_DATABASE_ID"]

    print(f"📂 Knowledge base: {SECOND_BRAIN}")

    md_files = collect_md_files(SECOND_BRAIN)
    print(f"📝 找到 {len(md_files)} 個 .md 檔案")

    # Load sync state
    state = load_sync_state()
    synced = 0
    skipped = 0
    failed = 0

    for md_path in md_files:
        rel = str(md_path.relative_to(SECOND_BRAIN))
        current_hash = file_hash(md_path)

        # Skip if unchanged (unless --full)
        if not args.full and state.get(rel) == current_hash:
            skipped += 1
            continue

        ok = sync_file(token, db_id, md_path, SECOND_BRAIN, dry_run=args.dry_run)

        if ok and not args.dry_run:
            state[rel] = current_hash
            synced += 1
        elif not ok:
            failed += 1

    if not args.dry_run:
        save_sync_state(state)

    print(f"\n{'[DRY RUN] ' if args.dry_run else ''}完成: {synced} 同步, {skipped} 跳過, {failed} 失敗")


if __name__ == "__main__":
    main()
