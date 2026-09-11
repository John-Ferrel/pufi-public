#!/usr/bin/env python3
"""
build_tag_bank.py — Build a curated, high-value tag subset for pufi-image.

Source: pufi-anime's tags/tags.jsonl (local Danbooru index, ~10k entries).
Output: pufi-image's tags/tag_bank.json (compact curated subset).

WHY curate at all? pufi-image's final prompt stays NATURAL LANGUAGE. Tags are
a helper for:
    1. term normalization (zh / synonym lookup)
    2. composition / pose / attire term standardization
    3. anatomy-risk detection
    4. auto-adding hard constraints
We never dump long tag strings into the image2 prompt.

SCOPE: the source is already a filtered index (~10k, all visual). We therefore
keep almost everything visual and only drop:
    - section: meta, fandom, people (metadata / franchise noise)
    - clearly non-visual themes: audio_tags, metatags, locations of meta type
    - object-level meta spamming text/signatures/usernames
    - non-visual words (commentary, translated, id/bad_id, request, etc.)
Anatomy-risk tags are always kept regardless of section/theme.

Usage:
    python3 scripts/build_tag_bank.py --source <tags.jsonl> [--out tag_bank.json]
"""

import argparse
import json
import sys
from pathlib import Path
from collections import Counter

SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = SKILL_DIR.parent / "pufi-anime" / "tags" / "tags.jsonl"
DEFAULT_OUT = SKILL_DIR / "tags" / "tag_bank.json"

# Sections that carry visual/prompt-relevant vocabulary. meta/fandom/people dropped.
INCLUDE_SECTIONS = {
    "composition", "action", "body", "scene", "appearance", "mature",
    "creatures", "objects",
}

# Themes that are clearly NOT visual prompt vocabulary (dropped even if in a
# kept section). Kept explicit so the logic is reviewable.
DROP_THEMES = {
    "audio_tags", "metatags", "commentary", "translation",
    "symbols", "logos", "text", "signature", "watermark",
    "fandom", "franchise", "artist_name", "character_name",
}

# Words that mark a tag as an anatomy-risk sentinel (always kept).
RISK_KEYWORDS = (
    "extra_", "missing_", "malformed", "deformed", "wrong_", "too_many",
    "out_of_frame", "cropped", "crop", "anatomy", "feet", "hand", "hands",
    "tail", "fingers", "toes", "toenail", "finger", "paw", "claw", "floating",
    "barefoot", "no_shoes", "foot", "bare_legs", "bare_arms", "midriff", "navel",
)

# Meta / non-visual terms that match RISK_KEYWORDS but are NOT anatomy risks.
RISK_EXCLUDE = {
    "bad_id", "bad_pixiv_id", "bad_twitter_id", "commentary_request",
    "commentary", "translated", "original", "slim_arms", "fingers_crossed",
}

# Explicitly risky tags to always keep.
RISK_CANONICAL = {
    "bad_feet", "barefoot", "no_shoes", "feet_out_of_frame", "foot_focus",
    "spread_toes", "toe_scrunch", "pigeon-toed", "plantar_flexion",
    "extra_ears", "extra_arms", "tail", "cat_tail", "multiple_tails",
    "hand_on_own_hip", "hand_in_pocket", "arms_behind_back", "crossed_arms",
    "outstretched_leg", "leg_up", "spread_legs", "on_side", "lying",
    "from_below", "from_above", "cowboy_shot", "upper_body", "full_body",
    "crop_top", "midriff", "bare_legs", "navel",
}

# Non-visual / metadata-ish tokens: if a word is in the name (with sectionless
# or object/meta context) we drop it.
NON_VISUAL_TOKENS = (
    "commentary", "translated", "request", "bad_", "_id", "english_",
    "username", "signature", "watermark", "logo", "logo_", "company_name",
    "character_name", "artist_name", "speech_bubble", "dated", "year",
    "score", "rating", "revision", "official_", "alternate_costume",
    "photo_", "photoshop", "source", "url", "ref", "sketch_", "fanart",
)

# Base appearance tokens: common/generic descriptors with NO lookup value for
# image2 (Pufi identity is fixed: pale golden hair, amber eyes; generic
# expressions are written naturally, not looked up). Dropped from appearance.
BASE_APPEARANCE_TOKENS = (
    "hair", "eyes", "eye_", "mouth", "blush", "smile", "cheek", "lash",
    "brow", "teeth", "fang", "tongue", "lip", "ear", "nose", "neck",
    "skin", "skin_", "face", "expression", "breast", "nipple", "thigh",
    "leg", "arm", "hand", "finger", "foot", "toe", "ass", "butt", "hip",
)

# Base single-word appearance tokens (uninformative alone).
BASE_SINGLE_APPEARANCE = {
    "smile", "blush", "grin", "teeth", "fang", "tongue", "sweat",
    "breasts", "nipples", "collarbone", "ahoge", "sidelocks", "braid",
    "thighs", "ass", "armpits", "stomach", "mole", "tears", "eyelashes",
    "legs", "expressionless", "profile", "chibi", ":d", ":3", "hetero",
}

# Garment / accessory vocabulary: appearance tags containing any of these are
# useful lookup words (e.g. white_shirt, black_thighhighs, red_bow). Everything
# else in the appearance bucket (hair/eye/skin/expression/action/scene noise)
# has little lookup value for image2 and is dropped.
GARMENT_TOKENS = (
    "shirt", "blouse", "dress", "skirt", "shorts", "pants", "jean",
    "jacket", "coat", "sweater", "hoodie", "cardigan", "tank", "top",
    "camisole", "bodysuit", "underwear", "lingerie", "bra", "panties",
    "stockings", "thighhighs", "socks", "boots", "shoes", "heels",
    "sandals", "slippers", "gloves", "mittens", "hat", "cap", "beret",
    "hood", "scarf", "collar", "tie", "ribbon", "bow", "belt", "suspenders",
    "strap", "lace", "frill", "ruffle", "sleeve", "kimono", "yukata",
    "sailor", "uniform", "apron", "maid", "nurse", "swimsuit", "bikini",
    "pajamas", "nightgown", "robe", "toga", "armor", "plate", "vest",
    "blazer", "suit", "trench", "parka", "puffer", "gilet", "cuirass",
)


def is_risk_tag(tag: dict) -> bool:
    name = tag.get("name", "")
    if name in RISK_EXCLUDE:
        return False
    if name in RISK_CANONICAL:
        return True
    return any(k in name for k in RISK_KEYWORDS)


def is_non_visual(tag: dict) -> bool:
    """Drop metadata-ish / text / franchise / generic-appearance noise."""
    name = tag.get("name", "")
    section = tag.get("section") or ""
    theme = tag.get("theme") or ""
    if theme in DROP_THEMES:
        return True
    if section == "meta" or section == "fandom":
        return True
    if section == "objects":
        if any(tok in name for tok in NON_VISUAL_TOKENS):
            return True
    if not section or not theme:
        if any(tok in name for tok in NON_VISUAL_TOKENS):
            return True
        if name in ("hetero", "yuri", "yaoi", "harem", "1boy", "1girl",
                    "solo", "multiple_girls", "multiple_boys", "comic",
                    "pov", "from_behind", "no_humans"):
            return False
        if name in ("d", "id", "request", "ratio", "commentary"):
            return True
    # Generic appearance terms: keep only garment/accessory-specific words
    # (or risk tags handled by is_risk_tag); drop hair/eye/expression/action noise.
    if classify(tag) == "appearance" and not is_risk_tag(tag):
        if any(tok in name for tok in GARMENT_TOKENS):
            pass  # keep
        else:
            return True
    return False


def classify(tag: dict) -> str:
    """Assign a mixin label (nature) for the pufi-image helper."""
    theme = tag.get("theme") or ""
    section = tag.get("section") or ""
    name = tag.get("name", "")
    if section == "composition" or theme in ("image_composition", "character_count"):
        return "composition"
    if theme in ("posture", "gestures", "hands", "legs", "gait"):
        return "pose"
    if theme in ("attire", "hosiery", "footwear", "handwear", "headwear",
                 "sleeves", "neck_and_neckwear", "shirts", "legwear", "misc_lingerie",
                 "accessories", "breasts_tags", "nudity"):
        return "attire"
    if section == "scene" or theme in ("backgrounds", "lighting", "locations"):
        return "scene"
    if is_risk_tag(tag):
        return "anatomy_risk"
    return "appearance"


def build(source: Path) -> list[dict]:
    if not source.is_file():
        print(f"[!] Source not found: {source}", file=sys.stderr)
        print("    Run pufi-anime's update_tags.py first, or pass --source.", file=sys.stderr)
        sys.exit(1)

    seen = set()
    out = []
    with open(source, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            name = d.get("name")
            if not name or name in seen:
                continue
            if is_risk_tag(d):
                keep = True
            elif is_non_visual(d):
                keep = False
            else:
                section = d.get("section") or ""
                keep = section in INCLUDE_SECTIONS or not section
            if not keep:
                continue
            seen.add(name)
            out.append({
                "t": name,
                "n": classify(d),
                "c": d.get("post_count", 0),
                "f": d.get("normalized_forms") or [],
                "zh": d.get("zh_translation") or "",
            })
    # Sort: risk first (by count desc), then by count desc.
    out.sort(key=lambda x: (0 if x["n"] == "anatomy_risk" else 1, -x["c"]))
    return out


def main():
    parser = argparse.ArgumentParser(description="Build curated tag bank for pufi-image.")
    parser.add_argument("--source", type=str, default=str(DEFAULT_SOURCE))
    parser.add_argument("--out", type=str, default=str(DEFAULT_OUT))
    args = parser.parse_args()

    tags = build(Path(args.source))
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(tags, ensure_ascii=False), encoding="utf-8")
    natures = Counter(x["n"] for x in tags)
    print(f"[+] Wrote {len(tags)} tags -> {out_path}")
    print("    nature breakdown:", dict(natures))


if __name__ == "__main__":
    main()