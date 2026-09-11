#!/usr/bin/env python3
"""
Build the local tag index for pufi-anime.

Downloads the ffdkj Danbooru translation SQLite, filters high-frequency
tags (>= 1000 posts), and writes tags/tags.jsonl.

Data sources:
- ffdkj Danbooru Tag 中英文对照表 (no license declared upstream):
  https://github.com/ffdkj/ffdkj-Danbooru_Tag-Chinese-English-Translation-Table
- Latent Tags group pages for tag-to-group mapping (public, no auth)

Usage:
    python3 scripts/update_tags.py                # basic build
    python3 scripts/update_tags.py --groups       # also fetch group mapping
    python3 scripts/update_tags.py --no-zh        # exclude zh_translation
"""

import json
import sqlite3
import sys
import tempfile
import time
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TAGS_DIR = SKILL_DIR / "tags"
DEFAULT_OUTPUT = TAGS_DIR / "tags.jsonl"
GROUPS_FILE = TAGS_DIR / "groups.json"
FFDKJ_URL = (
    "https://raw.githubusercontent.com/ffdkj/"
    "ffdkj-Danbooru_Tag-Chinese-English-Translation-Table/main/tag.sqlite"
)

INCLUDE_CATEGORIES = {0, 5}
LATENT_TAGS_BASE = "https://tags.latent.moe"
UA = "pufi-anime/1.0"


class TagLinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = set()

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        href = None
        for name, val in attrs:
            if name == "href":
                href = val
                break
        if href and href.startswith("/en/t/") and not href.startswith("/en/t/?"):
            self.tags.add(href[6:].split("?")[0])


def fetch_group_tags(slug: str) -> set[str]:
    url = f"{LATENT_TAGS_BASE}/en/g/{slug}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read().decode("utf-8", errors="replace")
        parser = TagLinkParser()
        parser.feed(html)
        return parser.tags
    except Exception as e:
        print(f"  [!] {slug}: {e}", file=sys.stderr)
        return set()


def build_group_map() -> dict[str, list[str]]:
    with open(GROUPS_FILE) as f:
        groups = json.load(f)

    root_slugs = set()
    for section in groups["sections"]:
        for root in section["roots"]:
            root_slugs.add(root["slug"])

    print(f"[*] Fetching {len(root_slugs)} group pages for tag-to-group mapping ...")

    tag_to_groups: dict[str, list[str]] = {}
    for i, slug in enumerate(sorted(root_slugs), 1):
        tags = fetch_group_tags(slug)
        for t in tags:
            tag_to_groups.setdefault(t, []).append(slug)
        if i % 10 == 0:
            print(f"  [{i}/{len(root_slugs)}] {slug} -> {len(tags)} tags")
        time.sleep(0.3)

    print(f"[+] Group map: {len(tag_to_groups)} unique tags mapped")
    return tag_to_groups


def download_ffdkj(path: Path) -> bool:
    print(f"[*] Downloading from {FFDKJ_URL} ...")
    try:
        req = urllib.request.Request(FFDKJ_URL, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=120) as resp:
            total = int(resp.headers.get("Content-Length", 0))
            downloaded = 0
            with open(path, "wb") as f:
                while True:
                    chunk = resp.read(65536)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total:
                        print(f"\r  {downloaded * 100 // total}% ({downloaded // 1048576} MiB)", end="", flush=True)
            print()
        print(f"[+] Downloaded {downloaded // 1048576} MiB")
        return True
    except Exception as e:
        print(f"[!] Download failed: {e}", file=sys.stderr)
        return False


def extract_tags(sqlite_path: Path, min_posts: int, output: Path, no_zh: bool,
                 group_map: dict[str, list[str]] | None, section_of_root: dict[str, str] | None):
    print(f"[*] Reading {sqlite_path} ...")
    conn = sqlite3.connect(str(sqlite_path))
    cur = conn.cursor()
    cur.execute("SELECT name, category, cn_name, post_count FROM tags WHERE post_count >= ?", (min_posts,))
    rows = cur.fetchall()
    conn.close()
    print(f"[*] {len(rows)} tags with >= {min_posts} posts")

    written = 0
    skipped_cat = 0
    mapped = 0
    with open(output, "w", encoding="utf-8") as f:
        for name, category, cn_name, post_count in rows:
            if category not in INCLUDE_CATEGORIES:
                skipped_cat += 1
                continue
            record = {"name": name, "post_count": post_count}
            # section/theme from group mapping
            if group_map and name in group_map:
                roots = group_map[name]
                if section_of_root:
                    # use first root's section
                    first = roots[0]
                    if first in section_of_root:
                        record["section"] = section_of_root[first]
                        record["theme"] = first
                        mapped += 1
            if "_" in name:
                record["normalized_forms"] = [name.replace("_", " ")]
            if not no_zh and cn_name:
                record["zh_translation"] = cn_name
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            written += 1

    print(f"[+] Written: {written} tags to {output}")
    print(f"[ ] Skipped (category): {skipped_cat}")
    if group_map:
        print(f"[+] Tags with section/theme: {mapped}")


def build_section_map() -> dict[str, str]:
    """Build root_slug -> section_name mapping from groups.json."""
    with open(GROUPS_FILE) as f:
        groups = json.load(f)
    root_to_section = {}
    for section in groups["sections"]:
        sec_name = section["section"]
        for root in section["roots"]:
            root_to_section[root["slug"]] = sec_name
    return root_to_section


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Build local tag index for pufi-anime")
    parser.add_argument("--min-posts", type=int, default=1000)
    parser.add_argument("--ffdkj-path", type=str, default=None)
    parser.add_argument("--output", type=str, default=str(DEFAULT_OUTPUT))
    parser.add_argument("--no-zh", action="store_true", help="Exclude zh_translation")
    parser.add_argument("--groups", action="store_true", help="Fetch tag-to-group mapping (95 HTTP requests)")
    args = parser.parse_args()

    TAGS_DIR.mkdir(parents=True, exist_ok=True)
    output = Path(args.output)

    group_map = None
    section_map = None
    if args.groups:
        if not GROUPS_FILE.exists():
            print(f"[!] groups.json not found", file=sys.stderr)
            sys.exit(1)
        section_map = build_section_map()
        group_map = build_group_map()

    if args.ffdkj_path:
        sqlite_path = Path(args.ffdkj_path)
        if not sqlite_path.exists():
            print(f"[!] Not found: {sqlite_path}", file=sys.stderr)
            sys.exit(1)
    else:
        tmp = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False)
        sqlite_path = Path(tmp.name)
        tmp.close()
        try:
            if not download_ffdkj(sqlite_path):
                sys.exit(1)
        except Exception:
            sqlite_path.unlink(missing_ok=True)
            raise

    try:
        extract_tags(sqlite_path, args.min_posts, output, args.no_zh, group_map, section_map)
    finally:
        if not args.ffdkj_path and sqlite_path.exists():
            sqlite_path.unlink()


if __name__ == "__main__":
    main()