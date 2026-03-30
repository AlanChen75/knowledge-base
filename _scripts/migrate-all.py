#!/usr/bin/env python3
"""
migrate-all.py — 整合所有 Notion 資料庫到 SecondBrain
1. 重新分類現有 172 筆 (加 Group + Origin)
2. 遷移 知識學習 147 筆
3. 遷移 想法捕捉 96 筆
4. 遷移 Felo.ai 17 筆
"""

import json
import re
import sys
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import HTTPError

TOKEN = ""
SECONDBRAIN_DB = "333bff7031e3813e9540e0913cc3d634"
KNOWLEDGE_DB = "117bff70-31e3-80bc-853f-fd132644743a"
IDEAS_DB = "12bbff70-31e3-81cf-a23a-f442cc77bf3f"
FELO_DB = "1654783c-b4f3-814b-936c-dbbcb35c8f73"

# Load token from .env
import os
from pathlib import Path
env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    for line in env_file.read_text().splitlines():
        if line.strip() and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())
TOKEN = os.environ.get("NOTION_TOKEN", "")
if not TOKEN:
    print("❌ Missing NOTION_TOKEN"); sys.exit(1)


# ─── Notion API ───
import time

def notion_request(method, path, body=None, retries=3):
    for attempt in range(retries):
        req = Request(
            f"https://api.notion.com/v1{path}",
            data=json.dumps(body).encode() if body else None,
            headers={
                "Authorization": f"Bearer {TOKEN}",
                "Notion-Version": "2022-06-28",
                "Content-Type": "application/json",
            },
            method=method,
        )
        try:
            result = json.loads(urlopen(req).read())
            # Rate limit: ~3 requests/sec for Notion API
            time.sleep(0.35)
            return result
        except HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                wait = 2 ** (attempt + 1)
                print(f"\n  ⏳ Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            err = e.read().decode()[:300]
            print(f"  ❌ API {e.code}: {err}")
            return None
    return None


def get_all_pages(db_id):
    all_items = []
    has_more = True
    cursor = None
    while has_more:
        body = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        result = notion_request("POST", f"/databases/{db_id}/query", body)
        if not result:
            break
        all_items.extend(result.get("results", []))
        has_more = result.get("has_more", False)
        cursor = result.get("next_cursor")
    return all_items


def get_page_body_text(page_id, max_blocks=5):
    """Get first few blocks of text from a page."""
    result = notion_request("GET", f"/blocks/{page_id}/children?page_size={max_blocks}")
    if not result:
        return ""
    texts = []
    for b in result.get("results", []):
        btype = b["type"]
        if btype in ("paragraph", "heading_1", "heading_2", "heading_3",
                      "bulleted_list_item", "numbered_list_item", "quote", "callout"):
            rt = b.get(btype, {}).get("rich_text", [])
            for t in rt:
                texts.append(t.get("text", {}).get("content", ""))
        elif btype == "bookmark":
            url = b.get("bookmark", {}).get("url", "")
            if url:
                texts.append(url)
    return " ".join(texts)[:300]


# ─── Classification ───
GROUP_RULES = [
    # (group, keywords)  — checked in order, first match wins
    ("投資", [
        "投資", "股票", "基金", "理財", "ETF", "資產", "巴菲特", "芒格", "蒙格",
        "殖利率", "股災", "熊市", "本金", "成長股", "存股", "賠錢", "漲", "跌",
        "創投", "天使投資", "VC", "估值", "融資", "IPO",
    ]),
    ("紀錄", [
        "工作日誌", "工作計畫", "work-log", "session", "測試報告", "部署紀錄",
        "測試紀錄", "進度", "盤點",
    ]),
    ("研究", [
        "論文", "paper", "研究", "NILM", "學術", "arxiv", "DOI", "期刊",
        "芝加哥大學論文", "芝加哥大学论文",
    ]),
    ("技術", [
        "AI", "ML", "GPT", "Claude", "LLM", "vLLM", "GPU", "API", "DevOps",
        "程式", "開發", "python", "javascript", "docker", "ComfyUI",
        "MCP", "agent", "bot", "deploy", "coding", "code", "自動化",
        "伺服器", "server", "3090", "telegram", "GitHub", "nginx",
        "RAG", "NAS", "OCR", "安全", "fail2ban", "SSH",
        "deepseek", "gemini", "openai", "qwen", "whisper",
        "SHC", "Happy Coder", "Super Happy", "Clawdbot",
    ]),
    ("商業", [
        "創業", "CEO", "商業", "策略", "行銷", "零售", "管理", "領導",
        "企業", "品牌", "產品", "公司", "營銷", "客戶", "市場",
        "新零售", "電商", "拼多多", "ZARA", "阿里", "京東",
        "李翔", "得到", "知识内参", "戰略", "團隊", "組織",
        "马云", "张勇", "刘强东", "李开复", "傅盛", "周航",
        "馬斯克", "Musk", "貝索斯", "Bezos", "賈伯斯", "Jobs",
        "销售", "廣告", "SEO", "PDCA", "OKR",
        "人力", "員工", "績效", "KPI", "考核",
    ]),
    ("學習", [
        "學習", "成長", "思維", "教育", "閱讀", "寫作", "名言",
        "心得", "修養", "人生", "哲學", "心理", "健康", "運動",
        "養生", "英文", "英語", "語言", "筆記", "自律",
        "金庸", "哲人", "幸福", "習慣", "批判性思維",
        "丹佐", "金凱瑞", "洛克菲勒", "蓋茲",
    ]),
    ("創意", [
        "dispatch", "靈感", "想法", "brainstorm", "草案", "規劃",
    ]),
]

def classify_group(title, category="", filepath=""):
    """Classify into one of the 7 groups."""
    combined = f"{title} {category} {filepath}".lower()

    # Direct path-based rules (highest priority for git-sync items)
    if filepath:
        fp = filepath.lower()
        if "work-logs/" in fp or "work-log" in fp:
            return "紀錄"
        if "dispatch-outputs/" in fp:
            return "創意"
        if "research/" in fp:
            return "研究"
        if "shc-v5/" in fp:
            return "技術"

    for group, keywords in GROUP_RULES:
        for kw in keywords:
            if kw.lower() in combined:
                return group

    return "學習"  # default fallback


def classify_subcategory(title, group):
    """Infer sub-category within a group."""
    t = title.lower()
    if group == "商業":
        if any(kw in t for kw in ["創業", "创业", "融资", "startup"]):
            return "entrepreneurship"
        if any(kw in t for kw in ["行銷", "營銷", "广告", "SEO", "品牌"]):
            return "marketing"
        if any(kw in t for kw in ["管理", "領導", "领导力", "團隊", "员工"]):
            return "management"
        if any(kw in t for kw in ["零售", "電商", "拼多多", "ZARA"]):
            return "retail"
        return "strategy"
    if group == "技術":
        if any(kw in t for kw in ["AI", "ML", "GPT", "LLM", "claude", "gemini", "deepseek"]):
            return "ai-ml"
        if any(kw in t for kw in ["工具", "tool", "whisper", "notebooklm"]):
            return "tools"
        if any(kw in t for kw in ["devops", "docker", "deploy", "server", "3090"]):
            return "devops"
        return "general"
    if group == "學習":
        if any(kw in t for kw in ["思維", "思考", "哲"]):
            return "mindset"
        if any(kw in t for kw in ["教育", "孩子", "學校"]):
            return "education"
        if any(kw in t for kw in ["健康", "運動", "養生", "醫"]):
            return "health"
        return "growth"
    return ""


# ─── Phase 1: Re-classify existing SecondBrain items ───
def phase1_reclassify():
    print("\n" + "=" * 60)
    print("Phase 1: Re-classify existing 172 items")
    print("=" * 60)

    pages = get_all_pages(SECONDBRAIN_DB)
    print(f"Found {len(pages)} items")

    updated = 0
    for page in pages:
        props = page.get("properties", {})
        title_arr = props.get("Title", {}).get("title", [])
        title = title_arr[0]["text"]["content"] if title_arr else ""
        category = props.get("Category", {}).get("select", {})
        cat_name = category.get("name", "") if category else ""
        filepath_arr = props.get("FilePath", {}).get("rich_text", [])
        filepath = filepath_arr[0]["text"]["content"] if filepath_arr else ""

        # Skip if already has Group
        existing_group = props.get("Group", {}).get("select")
        if existing_group:
            continue

        group = classify_group(title, cat_name, filepath)

        update_body = {
            "properties": {
                "Group": {"select": {"name": group}},
                "Origin": {"select": {"name": "git-sync"}},
            }
        }

        result = notion_request("PATCH", f"/pages/{page['id']}", update_body)
        if result:
            updated += 1
            sys.stdout.write(f"\r  Updated {updated}...")
            sys.stdout.flush()

    print(f"\n  ✅ Phase 1 done: {updated} items classified")


# ─── Phase 2: Migrate 知識學習 ───
def phase2_knowledge():
    print("\n" + "=" * 60)
    print("Phase 2: Migrate 知識學習 (147 items)")
    print("=" * 60)

    pages = get_all_pages(KNOWLEDGE_DB)
    print(f"Found {len(pages)} items")

    migrated = 0
    skipped = 0
    failed = 0

    for page in pages:
        props = page.get("properties", {})

        # Get title
        name_arr = props.get("Name", {}).get("title", [])
        title = name_arr[0]["text"]["content"][:200] if name_arr else ""
        if not title:
            title = "(untitled)"

        # Get URL
        url = props.get("URL", {}).get("url", "")

        # Get category label
        label = props.get("Label", {}).get("select")
        label_name = label["name"] if label else ""

        # Classify
        group = classify_group(title, label_name)
        subcategory = classify_subcategory(title, group)

        # Check if already migrated (by title match)
        check = notion_request("POST", f"/databases/{SECONDBRAIN_DB}/query", {
            "filter": {"property": "Title", "title": {"equals": title[:200]}},
            "page_size": 1,
        })
        if check and check.get("results"):
            skipped += 1
            continue

        # Create in SecondBrain
        new_page = {
            "parent": {"database_id": SECONDBRAIN_DB},
            "properties": {
                "Title": {"title": [{"text": {"content": title[:200]}}]},
                "Group": {"select": {"name": group}},
                "Origin": {"select": {"name": "notion-知識學習"}},
                "SyncedAt": {"date": {"start": datetime.now(timezone.utc).isoformat()}},
            }
        }
        if subcategory:
            new_page["properties"]["Category"] = {"select": {"name": subcategory}}
        if url:
            new_page["properties"]["Source"] = {"url": url}

        # Get page body content and add as blocks
        body_text = get_page_body_text(page["id"], max_blocks=3)
        if body_text:
            new_page["children"] = [{
                "type": "paragraph",
                "paragraph": {"rich_text": [{"text": {"content": body_text[:2000]}}]}
            }]

        result = notion_request("POST", "/pages", new_page)
        if result:
            migrated += 1
            sys.stdout.write(f"\r  Migrated {migrated}...")
            sys.stdout.flush()
        else:
            failed += 1

    print(f"\n  ✅ Phase 2 done: {migrated} migrated, {skipped} skipped, {failed} failed")


# ─── Phase 3: Migrate 想法捕捉 ───
def phase3_ideas():
    print("\n" + "=" * 60)
    print("Phase 3: Migrate 想法捕捉 (96 items)")
    print("=" * 60)

    pages = get_all_pages(IDEAS_DB)
    print(f"Found {len(pages)} items")

    migrated = 0
    skipped = 0
    failed = 0

    for page in pages:
        props = page.get("properties", {})
        created = page.get("created_time", "")[:10]

        # Title is usually empty, extract from body
        topic_arr = props.get("內容主題", {}).get("title", [])
        title = topic_arr[0]["text"]["content"][:200] if topic_arr else ""

        # Get body text for title extraction and content
        body_text = get_page_body_text(page["id"], max_blocks=5)

        if not title or title.strip() == "":
            # Extract title from first meaningful line of body
            if body_text:
                # Take first sentence or first 60 chars
                first_line = body_text.split("\n")[0].strip()
                # Remove common prefixes
                for prefix in ["今天，我将从两个话题出发", "精挑细淘，得到头条"]:
                    first_line = first_line.replace(prefix, "").strip("。，.、 ")
                title = first_line[:80] if first_line else f"想法捕捉 {created}"
            else:
                title = f"想法捕捉 {created}"

        # Skip if empty
        if not body_text and title.startswith("想法捕捉"):
            skipped += 1
            continue

        # Get URL
        url = props.get("網址連結", {}).get("url", "")

        # Get notes
        notes_arr = props.get("Notes", {}).get("rich_text", [])
        notes = notes_arr[0]["text"]["content"][:500] if notes_arr else ""

        # Get why
        why_arr = props.get("為什麼我想捕捉這個資訊？", {}).get("rich_text", [])
        why = why_arr[0]["text"]["content"][:200] if why_arr else ""

        # Classify
        combined_text = f"{title} {body_text[:200]}"
        group = classify_group(combined_text)
        subcategory = classify_subcategory(combined_text, group)

        # Create in SecondBrain
        new_page = {
            "parent": {"database_id": SECONDBRAIN_DB},
            "properties": {
                "Title": {"title": [{"text": {"content": title[:200]}}]},
                "Group": {"select": {"name": group}},
                "Origin": {"select": {"name": "notion-想法捕捉"}},
                "Date": {"date": {"start": created}} if created else {},
                "SyncedAt": {"date": {"start": datetime.now(timezone.utc).isoformat()}},
            }
        }
        if subcategory:
            new_page["properties"]["Category"] = {"select": {"name": subcategory}}
        if url:
            new_page["properties"]["Source"] = {"url": url}

        # Build content blocks
        children = []
        if why:
            children.append({
                "type": "callout",
                "callout": {
                    "rich_text": [{"text": {"content": f"為什麼捕捉：{why}"}}],
                    "icon": {"emoji": "💡"},
                }
            })
        if body_text:
            children.append({
                "type": "paragraph",
                "paragraph": {"rich_text": [{"text": {"content": body_text[:2000]}}]}
            })
        if notes:
            children.append({
                "type": "paragraph",
                "paragraph": {"rich_text": [{"text": {"content": f"筆記：{notes[:2000]}"}}]}
            })
        if children:
            new_page["children"] = children[:100]

        result = notion_request("POST", "/pages", new_page)
        if result:
            migrated += 1
            sys.stdout.write(f"\r  Migrated {migrated}...")
            sys.stdout.flush()
        else:
            failed += 1

    print(f"\n  ✅ Phase 3 done: {migrated} migrated, {skipped} skipped, {failed} failed")


# ─── Phase 4: Migrate Felo.ai ───
def phase4_felo():
    print("\n" + "=" * 60)
    print("Phase 4: Migrate Felo.ai (17 items)")
    print("=" * 60)

    pages = get_all_pages(FELO_DB)
    print(f"Found {len(pages)} items")

    migrated = 0
    failed = 0

    for page in pages:
        props = page.get("properties", {})

        # Query is the title
        query_arr = props.get("Query", {}).get("title", [])
        title = query_arr[0]["text"]["content"][:200] if query_arr else ""
        if not title:
            title = "Felo search"

        # Tags
        tags = props.get("Tags", {}).get("multi_select", [])
        tag_names = [t["name"] for t in tags[:10]]

        # Thread (rich text content)
        thread_arr = props.get("Thread", {}).get("rich_text", [])
        thread = thread_arr[0]["text"]["content"][:2000] if thread_arr else ""

        # Date
        date_prop = props.get("Date", {}).get("date")
        date_str = date_prop["start"] if date_prop else ""

        # Classify
        group = classify_group(title)
        if group == "學習" and any(kw in title for kw in ["論文", "paper", "期刊", "研究"]):
            group = "研究"
        subcategory = classify_subcategory(title, group)

        new_page = {
            "parent": {"database_id": SECONDBRAIN_DB},
            "properties": {
                "Title": {"title": [{"text": {"content": title[:200]}}]},
                "Group": {"select": {"name": group}},
                "Origin": {"select": {"name": "notion-felo"}},
                "Type": {"select": {"name": "note"}},
                "SyncedAt": {"date": {"start": datetime.now(timezone.utc).isoformat()}},
            }
        }
        if subcategory:
            new_page["properties"]["Category"] = {"select": {"name": subcategory}}
        if tag_names:
            new_page["properties"]["Tags"] = {
                "multi_select": [{"name": t} for t in tag_names]
            }
        if date_str:
            new_page["properties"]["Date"] = {"date": {"start": date_str[:10]}}

        if thread:
            new_page["children"] = [{
                "type": "paragraph",
                "paragraph": {"rich_text": [{"text": {"content": thread[:2000]}}]}
            }]

        result = notion_request("POST", "/pages", new_page)
        if result:
            migrated += 1
            print(f"  ✅ {title[:50]}")
        else:
            failed += 1

    print(f"\n  ✅ Phase 4 done: {migrated} migrated, {failed} failed")


# ─── Main ───
def main():
    print("🧠 SecondBrain 大整合")
    print(f"Target: {SECONDBRAIN_DB}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    if "--phase" in sys.argv:
        phase = int(sys.argv[sys.argv.index("--phase") + 1])
        if phase == 1: phase1_reclassify()
        elif phase == 2: phase2_knowledge()
        elif phase == 3: phase3_ideas()
        elif phase == 4: phase4_felo()
    else:
        phase1_reclassify()
        phase2_knowledge()
        phase3_ideas()
        phase4_felo()

    print("\n" + "=" * 60)
    print("🎉 整合完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
