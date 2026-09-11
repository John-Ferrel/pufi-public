#!/usr/bin/env python3
"""
Local Danbooru tag search for pufi-anime.

Loads tags/tags.jsonl and searches by name, normalized forms, and Chinese translation.

Results show: tag_name | post_count | section > theme | forms: … | zh: …

Usage:
    python3 scripts/search_tags.py "holding cup"
    python3 scripts/search_tags.py "茶杯"
    python3 scripts/search_tags.py "sitting" --top 3

Search order (first match wins by priority, ties broken by post_count):
  1. canonical exact (100)
  2. normalized form exact (95)
  3. zh exact (90)
  4. canonical prefix (80)
  5. normalized form prefix (75)
  6. zh prefix (70)
  7. canonical substring (60)
  8. normalized form substring (55)
  9. zh substring (50)
 10. word-in-canonical fallback (20)

No internet. No dependencies beyond stdlib.
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Optional

SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DB = SKILL_DIR / "tags" / "tags.jsonl"


def load_db(path: Optional[Path] = None) -> list[dict[str, Any]]:
    if path is None:
        path = DEFAULT_DB
    if not path.exists():
        print(f"[!] Tag database not found: {path}", file=sys.stderr)
        print("[!] Run scripts/update_tags.py first.", file=sys.stderr)
        sys.exit(1)
    tags = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                tags.append(json.loads(line))
    return tags


def normalize(name: str) -> str:
    """Underscore <-> space normalization."""
    return name.replace("_", " ").replace("-", " ").strip().lower()


def search(tags: list[dict], query: str, top: int = 10) -> list[dict]:
    """Search tags by query. Returns ordered results."""
    q_norm = normalize(query)
    q_lower = query.strip().lower()

    scored: list[tuple[int, dict]] = []
    seen_names = set()

    for tag in tags:
        name_norm = normalize(tag["name"])
        zh = (tag.get("zh_translation") or "").strip().lower()
        forms = [normalize(a) for a in (tag.get("normalized_forms") or [])]

        score = 0

        # 1. canonical exact
        if name_norm == q_norm or tag["name"].lower() == q_lower:
            score = 100
        # 2. normalized form exact
        elif any(a == q_norm for a in forms):
            score = 95
        # 3. zh exact
        elif zh == q_lower or zh == q_norm:
            score = 90
        # 4. canonical prefix
        elif name_norm.startswith(q_norm):
            score = 80
        # 5. normalized form prefix
        elif any(a.startswith(q_norm) for a in forms):
            score = 75
        # 6. zh prefix
        elif zh.startswith(q_lower) or zh.startswith(q_norm):
            score = 70
        # 7. canonical substring
        elif q_norm in name_norm:
            score = 60
        # 8. normalized form substring
        elif any(q_norm in a for a in forms):
            score = 55
        # 9. zh substring
        elif q_lower in zh or q_norm in zh:
            score = 50
        # word-in-canonical fallback
        elif any(w in name_norm for w in q_norm.split()):
            score = 20

        if score == 0:
            continue

        dedup_key = tag["name"]
        if dedup_key in seen_names:
            continue
        seen_names.add(dedup_key)

        scored.append((score, tag))

    scored.sort(key=lambda x: (-x[0], -x[1].get("post_count", 0)))
    return [s[1] for s in scored[:top]]


def fmt(tag: dict) -> str:
    parts = [tag["name"], _fmt_count(tag.get("post_count", 0))]
    section = tag.get("section")
    theme = tag.get("theme")
    if section and theme:
        parts.append(f"{section} > {theme}")
    forms = tag.get("normalized_forms")
    if forms:
        parts.append(f"forms: {', '.join(forms)}")
    zh = tag.get("zh_translation")
    if zh:
        parts.append(f"zh: {zh}")
    return " | ".join(parts)


def _fmt_count(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.0f}k"
    return str(n)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Search local Danbooru tag index")
    parser.add_argument("query", type=str, help="Search query")
    parser.add_argument("--top", type=int, default=10, help="Max results (default: 10)")
    parser.add_argument("--db", type=str, default=str(DEFAULT_DB), help=f"Database path (default: {DEFAULT_DB})")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    db_path = Path(args.db)
    tags = load_db(db_path)
    results = search(tags, args.query, top=args.top)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        if not results:
            print("(no results)")
        else:
            for r in results:
                print(fmt(r))


if __name__ == "__main__":
    main()