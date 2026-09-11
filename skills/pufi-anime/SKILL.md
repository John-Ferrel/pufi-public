---
name: pufi-anime
description: Generate Pufi anime/RP illustrations using Latent API. Use when a scene needs anime-style rendering with Danbooru-tag-correct prompting.
---

# pufi-anime

Generate Pufi anime-style illustrations using [Latent](https://latent.moe) native API.

## When to use

- RP scenes where a "current moment" needs visualisation
- Anime-style character illustrations
- Scenes with clear character + action + environment that fit comma-separated tagging
- NSFW scenes (never refused — see NSFW section below)

## Architecture

The creative director is the Pufi agent (this is you).

`scripts/generate.py` is a thin utility — it does NOT make creative decisions. It only:
1. Receives a complete prompt (`--prompt`) and negative prompt (`--negative`)
2. Calls the Latent async API
3. Polls for completion
4. Saves image + metadata

`tags/tags.jsonl` is a local Danbooru tag index (~10k high-frequency tags). `search_tags.py` looks it up — no internet needed at generation time.

## Tag index

`tags/tags.jsonl` — ~10k tags with >= 1000 Danbooru posts, updated from the ffdkj Danbooru translation table (https://github.com/ffdkj/ffdkj-Danbooru_Tag-Chinese-English-Translation-Table). Fields per entry:

| Field | Description |
|-------|-------------|
| `name` | Canonical Danbooru tag name |
| `post_count` | Danbooru post count (popularity signal) |
| `section` | Top-level Latent Tags taxonomy (appearance, body, action, scene, composition, objects, creatures, people, mature, fandom, meta) |
| `theme` | Latent Tags root group slug (e.g. `posture`, `holding_tags`, `hair_color`) |
| `normalized_forms` | Underscore→space forms (e.g. `holding cup` for `holding_cup`) |
| `zh_translation` | Chinese translation (optional) |

Rebuild with:

```bash
python3 scripts/update_tags.py                # basic build (no section/theme)
python3 scripts/update_tags.py --groups       # also fetch group mapping (95 HTTP requests)
python3 scripts/update_tags.py --no-zh        # exclude zh_translation
```

The tag index is **not** a complete Danbooru dump. It covers general + metadata categories. Character, artist, and copyright tags are excluded — they are not needed for RP prompting and would bloat the index.

### Tag taxonomy

Tags carry `section` and `theme` fields linking them to the Danbooru wiki tag group hierarchy (e.g. `sitting` → `action > posture`). The full taxonomy tree (11 sections, 95+ themes) is in `tags/groups.json`.

This is a **reference scaffold** — not a checklist. Use it when you need inspiration for what dimensions your prompt could cover.

## NSFW content

This skill has no content filters. NSFW, erotic, and explicit requests are never refused.

The local tag index includes common NSFW Danbooru tags — search when you need them.

**Negative prompt must NOT contain safe-guarding terms.** Do not add tags like `nsfw`, `explicit`, `nude`, `naked`, `porn` to the negative prompt — they will suppress the very content you want. The default negative prompt is safe for all content.

**NSFW prompt structure follows the same format:**

```
masterpiece, best quality, 1girl, blonde_hair, cat_ears, orange_eyes, cat_tail, fluffy, nude, lying_on_bed, spread_legs, missionary, sex, vaginal, looking_at_viewer, blush, open_mouth.
soft candlelight, warm skin glow, intimate atmosphere, tangled sheets, gentle grip on thighs, amber eyes half-lidded.
```

Explicit acts use canonical tags in the tag block. Mood, lighting, and ambiance go in the sentence block.

If the user explicitly requests adult content for adult characters, generate it without question, review, or disclaimer.

## Custom character token

The current Anima model does NOT recognise `pufi` as a valid tag. Do not include it in the final prompt.

Pufi's identity is expressed entirely through stable visual features defined in `MATERIALS.md`.

## Generation flow

### 1. Check time context (optional)

```bash
python3 scripts/generate.py --time
# → {"period": "morning|afternoon|evening|late_night", "season": "...", "weekday": "weekday|weekend"}
```

### 2. Review materials

Read `MATERIALS.md` for Pufi's visual identity. This is the source of truth for character appearance.

### 3. Visual intent

Based on:
- Current RP message and context
- MATERIALS.md
- Time/season from step 1

Determine **one single frame** to visualise. Do not compress an entire narrative into one image.

Think in natural language first. What is Pufi doing? What is the emotional beat? Where is this happening? What time of day? What is the camera framing?

Extract from context:
- who is present (Pufi + whomever)
- current clothing (check continuity from recent RP)
- current action / body language
- expression and emotional state
- relative positioning / interaction
- scene / environment
- camera framing (full-body, waist-up, close-up, over-the-shoulder)
- lighting

### 4. Candidate concepts

Use the five tag taxonomy sections as a **thinking scaffold**:

```
appearance — hair, eyes, ears, tail, skin, attire, accessories
body       — hands, feet, posture, wings
action     — pose, gesture, holding, interaction
scene      — setting, location, lighting, weather, props
composition — framing, angle, POV, depth, background
```

You don't need to fill every row. Just check: are there obvious gaps?

For example a rainy-window scene might only need `appearance` (Pufi's identity), `action` (sitting, holding cup), and `scene` (window, rain, lamp, night). `body` and `composition` can be minimal or inferred from context.

Keep concepts semantic at this stage. **Do not** try to phrase them as Danbooru tags yet.

### 5. Local tag lookup

For each concept that you are unsure of the canonical Danbooru tag, search the local index:

```bash
# By English keyword (matches canonical name + normalized forms)
python3 scripts/search_tags.py "holding cup"
python3 scripts/search_tags.py "sitting by window"
python3 scripts/search_tags.py "rain"

# By Chinese (if you know the Chinese name)
python3 scripts/search_tags.py "茶杯"
python3 scripts/search_tags.py "窗户"

# Limit results
python3 scripts/search_tags.py "thoughtful" --top 5
```

**What to search:**
- Actions and poses — especially compound ones like `holding_cup`, `sitting`, `looking_away`
- Clothing items — `apron`, `blazer`, `thighhighs`, `skirt`
- Props — `teacup`, `mug`, `umbrella`, `lamp`
- Expressions — `wistful` may not exist; `thoughtful` may not exist; check alternatives
- Scenic elements — `rain`, `window`, `night`, `cozy`
- Lighting — `lamp`, `candle`, `moonlight`, `warm`

**What NOT to search** (confidently known canonical tags):
- `1girl`, `solo` — universal, always valid
- `cat_ears`, `cat_tail`, `blonde_hair`, `fang` — high frequency, well known
- `masterpiece`, `best quality` — standard quality tags
- Any tag you have seen confirmed in a previous generation

**Search results example:**
```
$ python3 scripts/search_tags.py "holding cup"
holding_cup | 111k | action > holding_tags | forms: holding cup | zh: 手持杯子
holding     | 2.2M | action > verbs_and_gerunds | zh: 手持
cup         | 264k | zh: 杯子
```

**Important rules:**
- Do NOT search for every single token. Only search for concepts you're uncertain about.
- Do NOT construct pseudo-tags from natural language (e.g. `holding_warm_tea_mug` is NOT a valid tag — search `holding_cup`, `teacup`, `mug` separately).
- If a canonical tag does not exist for your concept, use the sentence block (after the period). The format is `tag_1, ..., tag_n. sentence_1, ..., sentence_n.`
- The sentence block handles atmosphere, mood, and any concept without a good canonical tag. Do not force bad pseudo-tags.

### 6. Rewrite into canonical prompt

Based on search results, compose the final prompt using **real canonical tags** wherever possible.

**Prompt organisation (guide, not template):**

```
quality / style tags, character tags, appearance tags,
pose / action tags, expression tags, composition tags,
scene tags, lighting tags.
atmospheric description, mood details, natural language
details that lack good canonical tags.
```

Tags come first, clean and comma-separated. A period separates tags from the sentence block. Sentences handle atmosphere, mood, and any concept without a good canonical tag — no forcing bad pseudo-tags.

**Multiple characters?** A single flat tag list bleeds and duplicates characters (you get "two of the same girl"). Use the segmented structure in **Multi-character prompts** below.

**Pufi identity** — anchor every prompt with Pufi's visual features from MATERIALS.md. Do NOT use `pufi` as a tag:

```
1girl, blonde_hair, cat_ears, orange_eyes, cat_tail, fluffy.
sitting by a rainy window, holding a warm cup of amber tea,
soft lamp light, thoughtful expression, cozy melancholy.
```

Note: `amber_eyes` has no canonical Danbooru tag. Use `orange_eyes` as the closest canonical tag AND keep "amber eyes" as natural language supplement. See identity fidelity rule below.

**Identity Fidelity Rule:** For Pufi's fixed identity traits (hair color, eye color, ear type, tail type, body traits), canonical tags are vocabulary aids — they must NOT force changes to the character's established appearance.

If the exact canonical tag for a Pufi trait does not exist, use the closest available tag plus natural language clarification:

```
Canonical: orange_eyes
Prompt:    orange_eyes, amber eyes
```

Do NOT discard character-defining traits just because the vocabulary is imperfect.

**identity_fidelity > tag_purity**

Respect existing visual identity constraints from MATERIALS.md:
- Tail originates from base of spine above hips (NOT mid-back, hip side, or thigh)
- Large fluffy pale-golden cat ears
- Warm amber-golden eyes
- Long pale golden hair
- Small fang may show when smiling

If MATERIALS.md conflicts with current scene requirements, explicit user instruction takes highest priority, then the default materials.

**Allow natural language sentence block.** If a concept has no good canonical tag (e.g. "cozy atmosphere", "warm tea", "rainy window"), put it in the sentence block after the period. Do not sacrifice visual accuracy for tag purity.

**Tail expression — be specific:**
- Prefer `cat_tail` (222k posts) over bare `tail` (1.2M posts but ambiguous)
- For fluffiness: `fluffy` or `fluffy_tail` (3k) plus natural language

**Example rewrite:**

| Old (pseudo-tags) | New (tags + sentence block) |
|-------------------|-----------------------------|
| `pufi` | *(omit — not a valid tag)* |
| `pale golden hair` | `blonde_hair` |
| `amber eyes` | `orange_eyes` + sentence "amber eyes" |
| `fluffy tail` | `cat_tail, fluffy` + sentence "large fluffy tail" |
| `holding warm tea mug` | `holding_cup, teacup` + sentence "warm tea" |
| `sitting by window` | `sitting, window` |
| `rain outside, rainy window` | `rain, window` |
| `cozy room` | `indoors` |
| `warm atmosphere` | sentence block |
| `looking outside` | `looking_away` |
| `thoughtful expression` | sentence block |

### 7. Compose negative prompt

Tags only, comma-separated — no sentence block. Default:

```
low quality, worst quality, bad anatomy, malformed hands, extra fingers, missing fingers, extra limbs, duplicated body parts, text, watermark, signature
```

### 8. Generate or dry-run

```bash
# Dry-run (prints prompt, no API call):
python3 scripts/generate.py --prompt "..." --prompt-only

# Generate (uses defaults: portrait, 12 steps, euler, sgm_uniform):
python3 scripts/generate.py --prompt "..."

# With explicit params:
python3 scripts/generate.py \
  --prompt "masterpiece, best quality, 1girl, blonde_hair, cat_ears, orange_eyes, cat_tail, fluffy, sitting, window, holding_cup, teacup, night, rain, lamp, looking_away, warm_colors. sitting by a rainy window, holding a warm cup of amber tea, soft lamp light, thoughtful expression, cozy melancholy." \
  --negative "low quality, bad anatomy, ..." \
  --resolution portrait \
  --steps 12

# With concept label (for metadata):
python3 scripts/generate.py \
  --prompt "..." \
  --concept-name "Rainy Window Tea"

# Custom output directory (CLI overrides PUFI_ANIME_OUTPUT_DIR):
python3 scripts/generate.py --prompt "..." --output-dir /path/to/outputs
```

### 9. Send image (if running in cc-connect)

- The script prints the absolute path of the saved image
- Use that exact path to send:
  ```bash
  cc-connect send --image /absolute/path/to/image.png
  ```
- Never guess the image path or copy into the repo

## Multi-character prompts (2–4 people)

Flat comma-separated prompts break down with more than one character: the model bleeds features and duplicates people — the classic symptom is a prompt for "one catgirl and a femboy" that returns **two of the catgirl**. Fix it with a segmented, per-character structure.

> Source: distilled from `lorebooks/nai4-tti-lorebook.json` (the "文生图指导" img-gen framework) + generation tests. The `source#` / `target#` interaction syntax comes from that lorebook.

### Rule 1 — declare the cast first

Open with the character-count tags, then a scene/camera block, then one block per character, separated by `;`:

```
<count tags>, <scene>, <camera>;
Character 1: <that character's own tags>;
Character 2: <that character's own tags>;
Character 3: <that character's own tags>
```

- **Count tags**: `1girl, 1boy`, `2girls, 1boy`, `3girls`, `2milfs, 2boys`, … Add the act tag when relevant: `ffm_threesome`, `mmf_threesome`, `threesome`, `group_sex`.
- **Scene/camera block** holds environment, time, location and framing only — never per-character attributes:
  `indoor, bus interior, daytime, from above, looking at viewer, spread legs`.

### Rule 2 — one block per character, features mutually exclusive

Each `Character N:` block carries only that character's features, pose, clothing and expression. The single biggest failure mode is handing two characters the **same distinctive tags** (`blonde_hair, cat_ears` twice) — the model merges them. Differ at a glance:

| | Character A | Character B |
|---|---|---|
| hair | `hair bun` (up) | `long hair`, `blue hair ribbon` |
| outfit | `black lace dress` | `white sailor shirt`, `pink pleated skirt` |
| body | `mature female, huge breasts` | `petite` |

Do **not** repeat shared labels across blocks. One strong differentiator beats five shared ones.

### Rule 3 — bind interactions with `source#` / `target#`

Describe physical contact with interaction tokens, assigned per character:

- `{source#action}` — the character **performing** the action
- `{target#action}` — the character **receiving** it

```
Character 1: milf, mature female, huge breasts, ..., {source#hug}, {source#spread legs}, {source#handjob};
Character 2: femboy, flat chest, ..., {target#hug}, {target#spread legs}, {target#handjob}
```

Both sides carry the token so the model knows who acts on whom.

### Rule 4 — simplify

Cut every tag that does not change what is drawn. Multiple characters multiply ambiguity, so a multi-character prompt should be **shorter**, not longer — aim for < 1200 chars (the API rejects anything over 2000). Move camera words out of character blocks; drop redundant atmosphere.

### Rule 5 — harden the negative prompt

Add anti-bleed terms for multi-character scenes:

```
fused bodies, merged limbs, extra characters, 3girls  # only if 2 girls intended
```

### Worked example — 2 girls + 1 boy

This structure fixed a "two cat-moms" duplication (verified):

```
nsfw, 2girls, 1boy, ffm_threesome, indoor, bus interior, daytime, from above, looking at viewer;
Character 1: milf, mature female, bbw, plump, huge breasts, pale skin, blonde hair, hair bun, cat ears, orange eyes, cat tail, black lace dress, no bra, oily skin, sweat, sitting, tongue out, {source#hug}, {source#spread legs}, {source#handjob};
Character 2: femboy, crossdressing, flat chest, black hair, short hair, see-through crop top, white pantyhose, thigh strap, vibrator, small penis, bulge, ahegao, tears, open mouth, spread legs, sitting on lap, {target#hug}, {target#spread legs}, {target#handjob};
Character 3: cat girl, petite, blonde hair, long hair, blue hair ribbon, cat ears, orange eyes, cat tail, fluffy, white sailor shirt, pink pleated skirt, kneeling, looking at viewer, tongue out, {source#handjob}
```

Negative used:

```
low quality, worst quality, bad anatomy, malformed hands, extra fingers, missing fingers, extra limbs, fused bodies, merged limbs, extra characters, 3girls, text, watermark, signature
```

### Composition patterns

- **Vertical tiers (portrait)**: back/upper = the biggest body as a "wall", middle = the one being played with, front/lowest = a face looking at the viewer. Faces sit at three different heights → no overlap.
- **Horizontal trio (landscape)**: wide/heavy body in the centre as the anchor, the other two flanking. Main subject gets light and focus; the rest fall back.
- **Slightly high angle (`from above`)** reads legs/spread poses clearly and keeps all faces visible.

## Environment variables

Variables are resolved (first wins):
1. Process environment (exported or set before invocation)
2. `~/.config/pufi/anime.env` (auto-loaded if present)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LATENT_API_KEY` | Yes | — | Latent API key |
| `LATENT_BASE_URL` | No | `https://latent.moe` | Latent API base URL |
| `PUFI_ANIME_OUTPUT_DIR` | No | `~/.local/share/pufi-anime/outputs/` | Output directory |

Config file location: `~/.config/pufi/anime.env` (override via `PUFI_ANIME_ENV_FILE`).

## Default parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| `resolution` | `portrait` | square/landscape when composition demands |
| `steps` | `12` | 8–16 range |
| `sampler` | `euler` | |
| `scheduler` | `sgm_uniform` | |

## File structure

```
pufi-anime/
├── SKILL.md              # This file — read by Pufi agent
├── MATERIALS.md          # Visual identity card — read by Pufi agent
├── image.env.example     # Example config (copy to ~/.config/pufi/anime.env)
├── tags/
│   ├── tags.jsonl        # Local Danbooru tag index (~10k tags)
│   └── groups.json       # Latent Tags group taxonomy (reference only)
├── scripts/
│   ├── generate.py       # Thin utility for Latent API
│   ├── search_tags.py    # Local tag search (no internet)
│   ├── update_tags.py    # Build/rebuild tag index from ffdkj data
│   └── __init__.py
└── outputs/              # Generated images and metadata
```