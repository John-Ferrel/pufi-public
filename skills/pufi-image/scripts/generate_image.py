#!/usr/bin/env python3
"""
pufi-image: Image generation tool for Pufi.

This is a THIN TOOL. Creative decisions are made entirely by the Pufi agent —
the agent writes the full natural-language prompt and chooses technical
parameters (size / quality / background / output_format). This script never
injects identity, never rewrites or appends to the prompt, and never decides
content policy.

Usage:
    python scripts/generate_image.py --prompt "<full natural language prompt>" [options]
    python scripts/generate_image.py --prompt "..." --prompt-only      # dry-run
    python scripts/generate_image.py --time                            # UTC+8 context
    python scripts/generate_image.py --tags "<term>"                   # tag bank lookup (reference)

Options:
    --concept-name <label>      Metadata label / output file slug
    --size <WxH | 2k | 4k | auto>   Image size (agent decides). Default: omit → backend default.
    --quality <auto|low|medium|high>  Quality tier (agent decides). Default: omit → backend default.
    --background <opaque|transparent> Background handling (default: omit)
    --output-format <png|webp>  Output format (default: omit)
    --prompt-only               Print the prompt + params and exit (no API call)

Environment (first wins):
    1. Process environment
    2. ~/.config/pufi/image.env   (override via PUFI_IMAGE_ENV_FILE)

The tag bank (tags/tag_bank.json) is a REFERENCE ONLY: it maps uncommon
Chinese/English expressions to standard terms. The final prompt is always
natural language; tag strings are never dumped into it.
"""

import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

SKILL_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Config: load optional env file (~/.config/pufi/image.env)
# ---------------------------------------------------------------------------

def _load_env_file():
    path = os.environ.get("PUFI_IMAGE_ENV_FILE")
    if path:
        env_path = Path(path)
    else:
        env_path = Path.home() / ".config" / "pufi" / "image.env"

    if not env_path.is_file():
        return

    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            if len(value) > 1 and value[0] == value[-1] and value[0] in ('"', "'"):
                value = value[1:-1]
            if key and key not in os.environ:
                os.environ[key] = value

_load_env_file()

# ---------------------------------------------------------------------------
# Output directory
# ---------------------------------------------------------------------------

_output_dir_env = os.environ.get("PUFI_IMAGE_OUTPUT_DIR")
if _output_dir_env:
    OUTPUT_DIR = Path(_output_dir_env)
else:
    OUTPUT_DIR = Path.home() / ".local" / "share" / "pufi-image" / "outputs"

# ---------------------------------------------------------------------------
# Curated tag bank (reference only: expression → standard term)
# ---------------------------------------------------------------------------

TAG_BANK = SKILL_DIR / "tags" / "tag_bank.json"
_TAG_CACHE = None


def load_tag_bank():
    """Lazy-load curated tag list. Returns [] if unavailable."""
    global _TAG_CACHE
    if _TAG_CACHE is not None:
        return _TAG_CACHE
    if not TAG_BANK.is_file():
        _TAG_CACHE = []
        return _TAG_CACHE
    try:
        with open(TAG_BANK, encoding="utf-8") as f:
            _TAG_CACHE = json.load(f)
    except Exception:
        _TAG_CACHE = []
    return _TAG_CACHE


def _norm_token(s):
    return s.replace("_", " ").replace("-", " ").strip().lower()


def search_tags(query, top=8):
    """Search curated tag bank by name / zh / normalized forms.

    Returns a list of tags, best matches first. Use results to pick standard
    natural-language wording — do not paste tag strings into the prompt.
    """
    q = _norm_token(query)
    if not q:
        return []
    hits = []
    for tag in load_tag_bank():
        name = tag.get("t") or ""
        zh = (tag.get("zh") or "").strip().lower()
        forms = [_norm_token(a) for a in (tag.get("f") or [])]
        score = 0
        if _norm_token(name) == q:
            score = 100
        elif q in forms:
            score = 95
        elif zh == q:
            score = 90
        elif _norm_token(name).startswith(q):
            score = 80
        elif any(a.startswith(q) for a in forms):
            score = 75
        elif q in _norm_token(name):
            score = 60
        elif zh and q in zh:
            score = 50
        if score:
            hits.append((score, tag))
    hits.sort(key=lambda x: (-x[0], -(x[1].get("c") or 0)))
    return [h[1] for h in hits[:top]]


def tag_bank_query_cli(query, top=8):
    if not load_tag_bank():
        print("(tag bank unavailable — run scripts/build_tag_bank.py)")
        return
    for t in search_tags(query, top=top):
        forms = f"  forms: {', '.join(t['f'])}" if t.get("f") else ""
        print(f"  {t.get('t', '')}  zh: {t.get('zh', '')}{forms}")


# ---------------------------------------------------------------------------
# UTC+8 time context
# ---------------------------------------------------------------------------

def utc8_now():
    return datetime.now(timezone(timedelta(hours=8)))


def time_context():
    now = utc8_now()
    h = now.hour
    if 5 <= h < 12:
        period = "morning"
    elif 12 <= h < 17:
        period = "afternoon"
    elif 17 <= h < 21:
        period = "evening"
    else:
        period = "late_night"
    return {
        "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "period": period,
        "weekday": "weekend" if now.weekday() >= 5 else "weekday",
        "season": _guess_season(now),
    }


def _guess_season(d):
    m = d.month
    if m in (12, 1, 2):
        return "winter"
    elif m in (3, 4, 5):
        return "spring"
    elif m in (6, 7, 8):
        return "summer"
    else:
        return "autumn"


# ---------------------------------------------------------------------------
# Parameter helpers (agent passes explicit values; thin validation only)
# ---------------------------------------------------------------------------

_SIZE_ALIASES = {
    "2k": "2048x2048",
    "2k_square": "2048x2048",
    "2k_landscape": "2048x1152",
    "2k_wide": "2048x1152",
    "4k": "3840x2160",
    "4k_landscape": "3840x2160",
    "4k_portrait": "2160x3840",
}

# gpt-image-2 popular sizes for reference (agent picks, tool does not decide).
POPULAR_SIZES = (
    "1024x1024", "1536x1024", "1024x1536",
    "2048x2048", "2048x1152",
    "3840x2160", "2160x3840",
)


def resolve_size(raw):
    """Map an explicit size value to a concrete WxH string, or None to omit."""
    if raw is None:
        return None
    s = raw.strip().lower().replace("×", "x").replace(" ", "")
    if not s or s == "auto":
        return None
    if s in _SIZE_ALIASES:
        return _SIZE_ALIASES[s]
    if re.fullmatch(r"\d{3,5}x\d{3,5}", s):
        return s
    print(f"[!] Unrecognized size '{raw}' — omit or use WxH / "
          f"{', '.join(_SIZE_ALIASES)} / 'auto'.", file=sys.stderr)
    return None


# ---------------------------------------------------------------------------
# Image API call (OpenAI-compatible)
# ---------------------------------------------------------------------------

def call_image_api(prompt, params):
    """Call image generation API with the agent-authored prompt + explicit params.

    Current format: OpenAI-compatible POST /v1/images/generations
      Body: {"model": str, "prompt": str, "n": 1,
             "size": str, "quality": str, "background": str, "output_format": str}
      Response: {"created": int, "data": [{"url"|"b64_json": ...}]}

    Adapt this function if your provider uses a different format.
    """
    base_url = os.environ.get("PUFI_IMAGE_API_URL", "").rstrip("/")
    api_key = os.environ.get("PUFI_IMAGE_API_KEY", "")
    model = os.environ.get("PUFI_IMAGE_MODEL", "gpt-image-2")

    if not base_url:
        print("[!] PUFI_IMAGE_API_URL not set.", file=sys.stderr)
        return None
    if not api_key:
        print("[!] PUFI_IMAGE_API_KEY not set.", file=sys.stderr)
        return None

    url = f"{base_url}/v1/images/generations"
    body = {"model": model, "prompt": prompt, "n": 1}
    for k in ("size", "quality", "background", "output_format"):
        v = params.get(k)
        if v:
            body[k] = v

    req = Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        },
    )

    try:
        with urlopen(req, timeout=180) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        code = e.code
        try:
            detail = e.read().decode("utf-8", errors="replace")[:500]
        except Exception:
            detail = "(unreadable)"
        print(f"[!] API HTTP {code}: {detail}", file=sys.stderr)
    except URLError as e:
        print(f"[!] API connection error: {e.reason}", file=sys.stderr)
    except Exception as e:
        print(f"[!] API error: {e}", file=sys.stderr)
    return None


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def save_output(prompt, api_response, tctx, label, params):
    """Save image + metadata to outputs/."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = utc8_now().strftime("%Y%m%d_%H%M%S")
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", (label or "pufi").lower()).strip("_")
    fmt = (params.get("output_format") or "png").lower()
    ext = ".webp" if fmt == "webp" else ".png"
    base = f"{ts}_{slug}"

    img_bytes = None
    if api_response and "data" in api_response and api_response["data"]:
        item = api_response["data"][0]
        if "b64_json" in item:
            import base64
            img_bytes = base64.b64decode(item["b64_json"])
        elif "url" in item:
            img_url = item["url"]
            try:
                req = Request(img_url)
                with urlopen(req, timeout=60) as resp:
                    img_bytes = resp.read()
            except Exception as e:
                print(f"[!] Download failed: {e}", file=sys.stderr)

    img_path = OUTPUT_DIR / f"{base}{ext}"
    if img_bytes:
        img_path.write_bytes(img_bytes)
        print(f"[+] Image: {img_path.resolve()}")
    else:
        print(f"[!] No image data in response.", file=sys.stderr)
        img_path = None

    meta = {
        "timestamp": tctx["datetime"],
        "period": tctx["period"],
        "season": tctx["season"],
        "weekday": tctx["weekday"],
        "label": label,
        "prompt": prompt,
        "params": params,
        "api_model": os.environ.get("PUFI_IMAGE_MODEL", ""),
    }
    if img_path:
        meta["output_path"] = str(img_path.resolve())

    meta_path = OUTPUT_DIR / f"{base}.meta.json"
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), "utf-8")
    print(f"[+] Metadata: {meta_path}")
    return meta


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Pufi image generation tool (thin).")
    parser.add_argument("--prompt", type=str, default=None,
                        help="Full natural-language prompt written by the agent (required to generate)")
    parser.add_argument("--concept-name", type=str, default=None,
                        help="Metadata label / output file slug")
    parser.add_argument("--size", type=str, default=None,
                        help=f"Explicit size: WxH, alias ({'/'.join(_SIZE_ALIASES)}), or 'auto'")
    parser.add_argument("--quality", type=str, default=None,
                        choices=["auto", "low", "medium", "high"],
                        help="Explicit quality tier (default: omit → backend default)")
    parser.add_argument("--background", type=str, default=None,
                        choices=["opaque", "transparent"],
                        help="Background handling (default: omit → backend default)")
    parser.add_argument("--output-format", type=str, default=None,
                        choices=["png", "webp"],
                        help="Output format (default: omit → backend default)")
    parser.add_argument("--output-dir", type=str, default=None,
                        help="Override output directory (default: PUFI_IMAGE_OUTPUT_DIR "
                             "or ~/.local/share/pufi-image/outputs)")
    parser.add_argument("--prompt-only", action="store_true",
                        help="Print prompt + params and exit (no API call)")
    parser.add_argument("--time", action="store_true",
                        help="Print UTC+8 time context as JSON and exit")
    parser.add_argument("--tags", type=str, default=None,
                        help="Query curated tag bank (expression → standard term) and exit")
    parser.add_argument("--top", type=int, default=8,
                        help="Max tag-bank results (default: 8)")
    args = parser.parse_args()

    if args.output_dir:
        global OUTPUT_DIR
        OUTPUT_DIR = Path(args.output_dir).expanduser()

    # Tag bank lookup mode (reference tool)
    if args.tags:
        print(f"tag bank: {TAG_BANK}")
        tag_bank_query_cli(args.tags, top=args.top)
        return

    # Time context mode
    tctx = time_context()
    if args.time:
        print(json.dumps(tctx, ensure_ascii=False))
        return

    # Generation mode requires an agent-authored prompt
    if not args.prompt:
        print("Usage:")
        print("  python scripts/generate_image.py --prompt \"<natural language prompt>\" [options]")
        print("  python scripts/generate_image.py --prompt \"...\" --prompt-only")
        print("  python scripts/generate_image.py --time")
        print("  python scripts/generate_image.py --tags '<term>' [--top N]")
        print()
        print("Options: --concept-name <label>  --size <WxH|2k|4k|auto>")
        print("         --quality <auto|low|medium|high>  --background <opaque|transparent>")
        print("         --output-format <png|webp>")
        print()
        print("Creative decisions (including size/quality) are made by the Pufi agent.")
        print("See SKILL.md for the full flow.")
        return

    label = args.concept_name or "pufi"
    params = {}
    size = resolve_size(args.size)
    if size:
        params["size"] = size
    if args.quality and args.quality != "auto":
        params["quality"] = args.quality
    if args.background and args.background != "auto":
        params["background"] = args.background
    if args.output_format and args.output_format != "auto":
        params["output_format"] = args.output_format

    if args.prompt_only:
        print("=" * 70)
        print("Pufi Image Prompt")
        print("=" * 70)
        print(args.prompt)
        print("=" * 70)
        print(f"Label:  {label}")
        print(f"Params: {json.dumps(params, ensure_ascii=False) or '(all defaults — omitted)'}")
        print(f"Time:   {tctx['period']}, {tctx['season']}, {tctx['weekday']}")
        print(f"Output: {OUTPUT_DIR}")
        return

    print(f"[*] Generating image ...")
    print(f"[*] Time:  {tctx['period']}, {tctx['season']}, {tctx['weekday']}")
    print(f"[*] Params: {json.dumps(params, ensure_ascii=False) or '(all defaults — omitted)'}")
    print(f"[*] Output: {OUTPUT_DIR}")
    resp = call_image_api(args.prompt, params)
    if resp is None:
        sys.exit(1)

    save_output(args.prompt, resp, tctx, label, params)


if __name__ == "__main__":
    main()
