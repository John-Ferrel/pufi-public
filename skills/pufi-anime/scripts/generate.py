#!/usr/bin/env python3
"""
pufi-anime: Image generation for anime/RP scenes via Latent API.

Usage (creative decisions are made by the Pufi agent, not this script):
    python3 scripts/generate.py --prompt "<prompt>"                         # generate
    python3 scripts/generate.py --prompt "<prompt>" --prompt-only           # dry-run
    python3 scripts/generate.py --time                                      # UTC+8 time context
    python3 scripts/generate.py --prompt "..." --negative "..." \
        --resolution portrait --steps 15                                   # explicit params
"""

import json
import os
import re
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

SKILL_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Config: load optional env file (~/.config/pufi/anime.env)
# ---------------------------------------------------------------------------

PUFI_PREFIX = "PUFI_ANIME"


def _load_env_file():
    path = os.environ.get(f"{PUFI_PREFIX}_ENV_FILE")
    if path:
        env_path = Path(path)
    else:
        env_path = Path.home() / ".config" / "pufi" / "anime.env"

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

_output_dir_env = os.environ.get(f"{PUFI_PREFIX}_OUTPUT_DIR")
if _output_dir_env:
    OUTPUT_DIR = Path(_output_dir_env)
else:
    OUTPUT_DIR = Path.home() / ".local" / "share" / "pufi-anime" / "outputs"

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
# Latent API client
# ---------------------------------------------------------------------------

LATENT_BASE_URL = os.environ.get("LATENT_BASE_URL", "https://latent.moe").rstrip("/")
LATENT_API_KEY = os.environ.get("LATENT_API_KEY", "")

DEFAULT_RESOLUTION = os.environ.get("PUFI_ANIME_RESOLUTION", "portrait")
DEFAULT_STEPS = int(os.environ.get("PUFI_ANIME_STEPS", "12"))
DEFAULT_SAMPLER = os.environ.get("PUFI_ANIME_SAMPLER", "euler")
DEFAULT_SCHEDULER = os.environ.get("PUFI_ANIME_SCHEDULER", "sgm_uniform")

POLL_INTERVAL = 3  # seconds between polls
MAX_POLL_TIME = 180  # total max wait


def _latent_headers():
    if not LATENT_API_KEY:
        print("[!] LATENT_API_KEY not set.", file=sys.stderr)
        return None
    return {
        "Authorization": f"Bearer {LATENT_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "pufi-anime/1.0",
    }


def download_media(artwork_id, size="original"):
    """Download image bytes from /api/media/{artwork_id}. Return bytes or None."""
    url = f"{LATENT_BASE_URL}/api/media/{artwork_id}?size={size}"
    headers = {
        "Authorization": f"Bearer {LATENT_API_KEY}",
        "User-Agent": "pufi-anime/1.0",
    }
    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=120) as resp:
            return resp.read()
    except HTTPError as e:
        code = e.code
        try:
            detail = e.read().decode("utf-8", errors="replace")[:500]
        except Exception:
            detail = "(unreadable)"
        if code == 403:
            print(f"[!] Media download blocked (HTTP 403) — may be a Cloudflare challenge.", file=sys.stderr)
        else:
            print(f"[!] Media download HTTP {code}: {detail}", file=sys.stderr)
    except URLError as e:
        print(f"[!] Media download connection error: {e.reason}", file=sys.stderr)
    except Exception as e:
        print(f"[!] Media download error: {e}", file=sys.stderr)
    return None


def _dump_raw(suffix, data):
    """Save raw JSON for debugging when unexpected response shape."""
    ts = utc8_now().strftime("%Y%m%d_%H%M%S")
    path = OUTPUT_DIR / f"{ts}_{suffix}.raw.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")
    print(f"[!] Raw response saved: {path.resolve()}", file=sys.stderr)


def _http_request(method, url, data=None, headers=None):
    req = Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urlopen(req, timeout=120) as resp:
            body = resp.read().decode("utf-8")
            if body:
                return json.loads(body)
            return {}
    except HTTPError as e:
        code = e.code
        try:
            detail = e.read().decode("utf-8", errors="replace")[:1000]
        except Exception:
            detail = "(unreadable)"
        return {"_error": True, "_status": code, "_detail": detail}
    except URLError as e:
        return {"_error": True, "_status": 0, "_detail": str(e.reason)}
    except Exception as e:
        return {"_error": True, "_status": 0, "_detail": str(e)}


def check_error(data):
    if data.get("_error"):
        status = data.get("_status", 0)
        detail = data.get("_detail", "")
        if status == 409:
            print("[!] A generation job is already in progress for this account.", file=sys.stderr)
        elif status == 429:
            print("[!] Weekly quota exhausted or queue full. Try again later.", file=sys.stderr)
        elif status == 503:
            print("[!] Service unavailable (queue full). Try again later.", file=sys.stderr)
        elif status == 404:
            print(f"[!] Not found: {detail}", file=sys.stderr)
        elif status == 401:
            print("[!] Authentication failed. Check your LATENT_API_KEY.", file=sys.stderr)
        elif status == 0:
            print(f"[!] Connection error: {detail}", file=sys.stderr)
        else:
            print(f"[!] API error (HTTP {status}): {detail}", file=sys.stderr)
        return True
    return False


def submit_generation(prompt, negative, seed, resolution, steps, sampler, scheduler):
    url = f"{LATENT_BASE_URL}/api/generate"
    body = {
        "prompt": prompt,
        "resolution": resolution,
        "steps": steps,
        "sampler": sampler,
        "scheduler": scheduler,
    }
    if negative:
        body["negativePrompt"] = negative
    if seed is not None:
        body["seed"] = seed

    headers = _latent_headers()
    if not headers:
        return None

    data = _http_request("POST", url, data=json.dumps(body).encode("utf-8"), headers=headers)
    if check_error(data):
        return None

    job_id = data.get("id")
    if not job_id:
        print(f"[!] Could not extract job id from response: {json.dumps(data, ensure_ascii=False)[:300]}", file=sys.stderr)
        return None

    return job_id


def poll_job(job_id):
    url = f"{LATENT_BASE_URL}/api/generate/{job_id}"
    headers = _latent_headers()
    if not headers:
        return None

    deadline = time.time() + MAX_POLL_TIME
    while time.time() < deadline:
        data = _http_request("GET", url, headers=headers)
        if check_error(data):
            return None

        status = (data.get("status") or "").lower()

        if status == "succeeded":
            artwork_id = data.get("artworkId")
            if not artwork_id:
                _dump_raw("artwork_id_missing", data)
                print("[!] Job succeeded but no artworkId in response.", file=sys.stderr)
                return None
            seed = data.get("seed")
            return {
                "job_id": job_id,
                "artwork_id": artwork_id,
                "seed": seed,
            }

        if status in ("failed", "error", "timeout"):
            error_msg = data.get("errorCode") or data.get("error") or data.get("message") or "generation failed"
            print(f"[!] {error_msg}", file=sys.stderr)
            return None

        time.sleep(POLL_INTERVAL)

    print(f"[!] Generation timed out after {MAX_POLL_TIME}s.", file=sys.stderr)
    return None


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def save_output(prompt, negative, metadata, img_bytes, tctx, label):
    """Save image + metadata to outputs/."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = utc8_now().strftime("%Y%m%d_%H%M%S")
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", (label or "pufi").lower()).strip("_")
    base = f"{ts}_{slug}"

    img_path = OUTPUT_DIR / f"{base}.png"
    if img_bytes:
        img_path.write_bytes(img_bytes)
        print(f"[+] Image: {img_path.resolve()}")
    else:
        print(f"[!] No image data.", file=sys.stderr)
        img_path = None

    meta = {
        "timestamp": tctx["datetime"],
        "period": tctx["period"],
        "season": tctx["season"],
        "weekday": tctx["weekday"],
        "label": label,
        "prompt": prompt,
        "negative_prompt": negative,
        "job_id": metadata.get("job_id"),
        "artwork_id": metadata.get("artwork_id"),
        "seed": metadata.get("seed"),
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

    parser = argparse.ArgumentParser(description="Pufi anime image generation (Latent API).")
    parser.add_argument("--prompt", type=str, default=None, help="Full image prompt (required for generation)")
    parser.add_argument("--negative", type=str, default=None, help="Negative prompt")
    parser.add_argument("--seed", type=int, default=None, help="Random seed (omit for random)")
    parser.add_argument("--resolution", type=str, default=DEFAULT_RESOLUTION, choices=["square", "portrait", "landscape"], help=f"Resolution (default: {DEFAULT_RESOLUTION})")
    parser.add_argument("--steps", type=int, default=DEFAULT_STEPS, help=f"Steps 8-16 (default: {DEFAULT_STEPS})")
    parser.add_argument("--sampler", type=str, default=DEFAULT_SAMPLER, choices=["euler", "euler_ancestral", "dpmpp_2s_ancestral", "dpmpp_2m", "dpmpp_sde", "dpmpp_2m_sde", "ddim"], help=f"Sampler (default: {DEFAULT_SAMPLER})")
    parser.add_argument("--scheduler", type=str, default=DEFAULT_SCHEDULER, choices=["sgm_uniform", "beta", "beta57", "linear_quadratic"], help=f"Scheduler (default: {DEFAULT_SCHEDULER})")
    parser.add_argument("--concept-name", type=str, default=None, help="Label for metadata (creative decision by agent)")
    parser.add_argument("--output-dir", type=str, default=None, help="Override output directory (default: PUFI_ANIME_OUTPUT_DIR or ~/.local/share/pufi-anime/outputs)")
    parser.add_argument("--job-id", type=str, default=None, help="Re-poll an existing job instead of submitting a new one")
    parser.add_argument("--prompt-only", action="store_true", help="Print prompt and exit (no API call)")
    parser.add_argument("--time", action="store_true", help="Print UTC+8 time context as JSON and exit")
    args = parser.parse_args()

    if args.output_dir:
        global OUTPUT_DIR
        OUTPUT_DIR = Path(args.output_dir).expanduser()

    tctx = time_context()

    if args.time:
        print(json.dumps(tctx, ensure_ascii=False))
        return

    if not args.prompt and not args.job_id:
        print("Usage: python3 generate.py --prompt \"...\" [options]")
        print("       python3 generate.py --job-id <uuid>")
        print("       python3 generate.py --time")
        print("       python3 generate.py --prompt \"...\" --prompt-only")
        print("\nCreative decisions are made by the Pufi agent. See SKILL.md for the full flow.")
        return

    label = args.concept_name or "custom"

    if args.prompt_only:
        print("=" * 60)
        print("Pufi Anime Prompt")
        print("=" * 60)
        print(f"Prompt:     {args.prompt}")
        if args.negative:
            print(f"Negative:   {args.negative}")
        print(f"Resolution: {args.resolution}")
        print(f"Steps:      {args.steps}")
        print(f"Sampler:    {args.sampler}")
        print(f"Scheduler:  {args.scheduler}")
        if args.seed is not None:
            print(f"Seed:       {args.seed}")
        print("=" * 60)
        print(f"Label: {label}")
        print(f"Time:  {tctx['period']}, {tctx['season']}, {tctx['weekday']}")
        print(f"Output: {OUTPUT_DIR}")
        return

    print(f"[*] Submitting to Latent API ...")
    print(f"[*] Resolution: {args.resolution}, Steps: {args.steps}, Sampler: {args.sampler}, Scheduler: {args.scheduler}")
    print(f"[*] Time: {tctx['period']}, {tctx['season']}, {tctx['weekday']}")
    print(f"[*] Output: {OUTPUT_DIR}")

    job_id = args.job_id
    if job_id:
        print(f"[*] Re-polling existing job: {job_id}")
    else:
        job_id = submit_generation(
            prompt=args.prompt,
            negative=args.negative,
            seed=args.seed,
            resolution=args.resolution,
            steps=args.steps,
            sampler=args.sampler,
            scheduler=args.scheduler,
        )
        if job_id is None:
            sys.exit(1)
        print(f"[*] Job submitted: {job_id}")

    print(f"[*] Waiting ...")

    metadata = poll_job(job_id)
    if metadata is None:
        sys.exit(1)

    artwork_id = metadata.get("artwork_id")
    seed = metadata.get("seed")
    print(f"[*] Seed: {seed}")
    print(f"[*] Artwork ID: {artwork_id}")

    img_bytes = download_media(artwork_id)
    if img_bytes is None:
        sys.exit(1)

    save_output(args.prompt, args.negative, metadata, img_bytes, tctx, label)
    print(f"[+] Job: {job_id}")
    print(f"[+] Seed: {seed}")
    print(f"[+] Artwork: {artwork_id}")


if __name__ == "__main__":
    main()