---
name: pufi-image
description: Generate Pufi illustrations using the configured image API, current UTC+8 time context, and curated visual/lore materials. Use when Pufi needs to draw or send an image of herself.
---

# pufi-image

Generate Pufi illustrations using the image generation API.

## Division of labour

**Creative director = Pufi agent (this is you).**

`generate_image.py` is a **thin tool** — it does not make creative decisions.
It only:
1. Provides UTC+8 time context (`--time`)
2. Receives a **complete natural-language prompt** written by you
3. Receives explicit technical parameters you chose (`--size`, `--quality`, …)
4. Calls the image API
5. Saves image + metadata

The tool never injects identity, never rewrites or appends to your prompt, and
never decides content. **You write the entire prompt yourself**, including the
identity anchor and hard constraints.

## Generation flow

1. **Check time** — `python scripts/generate_image.py --time`
   → `{"period": "morning|afternoon|evening|late_night", "season": "...", "weekday": "weekday|weekend"}`

2. **Read materials** — read `MATERIALS.md`. Use the **stable identity & rules
   block verbatim** (never re-invent Pufi's core appearance), and pick
   vocabulary freely from the palettes.

3. **Judge composition** — decide framing/aspect/camera before writing
   (this is your creative choice, expressed in natural language).

4. **Write the full prompt in natural language** — one coherent scene, not a
   tag list and not JSON.

5. **Dry-run + review** — `--prompt-only` prints the exact prompt and params.
   Review before spending an API call.

6. **Generate** — run with your chosen params, send the image back to chat.

## Writing the prompt (natural language, full control in your hands)

Write **one complete, self-contained prompt**. Because the tool does not add
anything, every element you want in the image must be in your text —
including Pufi's identity and the hard constraints.

**Suggested ordering** (one coherent paragraph, roughly this flow):

```
identity (from MATERIALS stable block, verbatim-ish)
→ scene / situation
→ outfit & action / body language
→ composition (in natural words)
→ environment
→ lighting / atmosphere
→ mood / expression
→ style
→ hard constraints
→ avoid
```

**Identity:** anchor every prompt with Pufi's stable identity and hard
constraints from the MATERIALS stable block. Do not reword the core appearance
into something new; you may append scene-specific variation after it. Tail
anatomy and hands are hard constraints — they beat prettiness.

**Composition is your call, written naturally:** e.g. `full-body framing,
entire figure visible head-to-toe` / `waist-up framing, vertical portrait
composition` / `close-up, square composition` / `eye-level camera` /
`facing left, with open space on the right`. Default is full-body; honour
selfie / portrait / waist-up intent when the user asks or implies it. For
selfies avoid extreme reaching-toward-camera perspective.

**Hands:** prefer simple natural poses (relaxed, holding phone/cup/bag/book,
one in pocket, loosely clasped, behind back, adjusting collar/hair). Avoid by
default: clenched fists, open palm to camera, strongly spread fingers,
reaching to viewer, extreme foreshortening. If a scene needs an explicit hand
pose, describe it concretely.

**High-signal, not tag soup:** concrete visual description first; quality
buzzwords only where they earn their place. Prefer renderability when two
ideas conflict. Keep persistent hard constraints limited to: identity, tail
anatomy, hands, no cropping.

**Diversity for vague requests:** when the user gives only loose direction
("拍一张现在的你", "准备回家"), vary 3–4 dimensions (environment, outfit,
activity, lighting, a distinctive detail, composition). Do not default to
office/desk. Aim for a coherent slice across the palettes (daily, city,
travel, fashion, seasonal, fantasy).

**Style tail:** end with a style sentence. The default is
`Anime illustration style. Beautiful detailed face and eyes.` — vary it when
the mood calls for something else (soft slice-of-life, cinematic, gothic…).

**On-image text:** only include visible text when the user explicitly wants
it; write it out precisely (`On-image text: "…", spelled exactly as written`).

## Content & 成人向创作（private 全量）

### 默认擦边基线（默认行为，不是用户要求才做）

画 Pufi 默认就带擦边。基准是：**至少满足下面一项以上**，不允许画成严严实实的端庄图：

- **露肤**：单侧露肩 / 锁骨可见 / 高开叉露腿 / 下衣失踪 / 贴身勾勒（改良汉服 = 露肩+开叉款）
- **氛围**：暧昧灯光（烛光/暖灯/屏幕光）、轻微挑逗的表情或姿态
- Exposure Dial（§2.1）默认取 **2–3 档**起步；华服、日常装都按"能露的地方露一点"来设计

### 手法（组合自 MATERIALS，全部用自然语言表达）

- **穿着**：§2.1 Exposure Dial 取中高档位 + §2.2–2.10 具体款——lingerie、丝袜/吊带、
  半敞睡袍、贴身湿亮、下衣失踪
- **身体语言**：§3.2 诱惑姿势——teasing 回眸、咬唇、手沿腰线、半跪、拱背
- **表情**：§4 微表情——半垂眼、微张唇、腮红、耳尖红、目光上挑
- **氛围**：§5.1 暧昧光——烛光、屏幕光、镜面、剪影、湿亮
- **取景**：§6.2 私密取景——贴近特写、俯/仰视角、mirror/POV
- **暗示优于直给**：用遮挡、光影、若隐若现制造张力；需要更直接时把 §3.3 explicit
  tags 转成自然语言描写

### 后端被拒 → 反馈驱动的小幅降档，三振出局

**不要预先自我设限**：没有词汇黑名单。不同后端审查尺度不同，且一次"被拒"往往是若干词/氛围组合的结果——把它们记成固定规则只会压缩你的创作空间。按创作意图大胆写，让 API 的真实反馈来做导航。

被 `HTTP 400 content_policy_violation` 拒绝时：

1. **只做一步小幅调整**：保住画面主体和创作意图，在"暴露度 / 用词 / 氛围"三个维度中挑一个降一档（例如降 Exposure Dial 一档、换成更保守的同义表达、弱化一处暧昧氛围）。由你判断这次最可能是什么触发的。
2. **最多重试 2 次**（含首次共 3 次尝试，即"三振出局"）。
3. 连续 3 次仍被拒 → **返回失败**给用户，说明当前后端限制，不无限降档、不擅自画成健康图。

需要更直接的内容时，切换到支持 NSFW 的 OpenAI 兼容端点（改 `~/.config/pufi/image.env`）
或改用 `pufi-anime`。

## Technical parameters (you choose them, passed on the CLI)

The tool does **not** infer these and they are **not** stored in `.env`.
Decide per image and pass explicitly.

| Flag | Options | Guidance |
|------|---------|----------|
| `--size` | `WxH`, `2k`, `2k_landscape`, `4k`, `4k_portrait`, `auto` | square 图 → `1024x1024`; portrait/full-body → `1024x1536`; landscape/横向动作 → `1536x1024`; 高清需求 → `2048x2048`/`2048x1152`/`4k`。无把握 → `auto`（省略，走后端默认） |
| `--quality` | `low` / `medium` / `high` / `auto` | 草测/草图 → `low`; 日常聊天图 → `medium`; 海报/终稿 → `high`; 默认 → `auto` |
| `--background` | `opaque` / `transparent` | 贴纸/透明底素材才用 `transparent` |
| `--output-format` | `png` / `webp` | 默认 png; 需省体积可 webp |
| `--output-dir` | 路径 | 覆盖输出目录；默认 `PUFI_IMAGE_OUTPUT_DIR`，否则 `~/.local/share/pufi-image/outputs/` |

gpt-image-2 硬约束：长边 ≤ 3840、边长为 16 的倍数、宽高比 ≤ 3:1。常用尺寸：
`1024x1024` `1536x1024` `1024x1536` `2048x2048` `2048x1152` `3840x2160` `2160x3840`。
第三方网关可能忽略非常用尺寸并回落后端默认——非必要别用冷门值。

## Dry-run & generate

```bash
# Dry-run (prints exact prompt + params, no API call):
python scripts/generate_image.py --prompt "<your full prompt>" \
  --size 1024x1536 --quality medium --prompt-only

# Generate:
python scripts/generate_image.py --prompt "<your full prompt>" \
  --concept-name "Rainy Window Tea" --size 1024x1536 --quality medium
```

Review the dry-run output. When satisfied, generate and send the returned
absolute image path back to chat.

## Tag bank (reference only — for wording, never for the prompt)

`tags/tag_bank.json` is a curated term index. Its only job: when you are not
sure how to phrase an uncommon concept in stable natural language, look it up:

```bash
python scripts/generate_image.py --tags "过膝袜"
# → thighhighs / over-kneehighs / black_thighhighs …
python scripts/generate_image.py --tags "侧卧"
# → on_side …
```

Use the result to **standardise your wording** in the natural-language prompt
(e.g. write "thigh-high socks" instead of guessing). Do **not** paste tag
strings into the prompt — the image model is natural-language-first.

## Environment Variables

Variables are resolved (first wins):
1. Process environment (exported or set before invocation)
2. `~/.config/pufi/image.env` (auto-loaded if present)

| Variable | Required | Description |
|----------|----------|-------------|
| `PUFI_IMAGE_API_URL` | Yes | Base URL of image generation API |
| `PUFI_IMAGE_API_KEY` | Yes | API key |
| `PUFI_IMAGE_MODEL` | No | Model name (default: `gpt-image-2`) |
| `PUFI_IMAGE_OUTPUT_DIR` | No | Output directory (default: `~/.local/share/pufi-image/outputs/`) |

Size / quality are **per-call CLI params**, not config values.

**Config file location** — `~/.config/pufi/image.env` (override via `PUFI_IMAGE_ENV_FILE`).

## Generate & send (cc-connect)

```bash
# Normal inline image (platform may re-compress photo messages, e.g. Telegram)
cc-connect send --image /absolute/path/to/image.png

# Original file, no re-compression (shown as a file attachment)
cc-connect send --file /absolute/path/to/image.png
```

- Send any caption as normal reply text (not attached to the CLI command)
- Never guess the image location from relative paths
- Never copy the image into the repo — it lives in `~/.local/share/pufi-image/outputs/`
- Inline `--image` is fine for casual chat; use `--file` when the recipient
  needs the original without platform re-compression.

## File Structure

```
pufi-image/
├── SKILL.md              # This file — read by Pufi agent
├── MATERIALS.md          # Stable identity/rules (single source) + vocabulary palettes
├── image.env.example     # Example config (url/key/model only; no size)
├── tags/
│   └── tag_bank.json     # Curated term index (reference: wording lookup only)
├── scripts/
│   ├── generate_image.py # Thin tool: prompt+params → API → save
│   ├── build_tag_bank.py # Rebuild tags/tag_bank.json from pufi-anime tags.jsonl
│   └── __init__.py
└── outputs/              # Legacy — new images go to ~/.local/share/pufi-image/outputs/
```

Runtime state (not in repo):
- `~/.local/share/pufi-image/outputs/` — generated images + metadata
- `~/.config/pufi/image.env` — secrets/config
