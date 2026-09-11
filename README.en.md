# Pufi 🐱💕 — Romanian Catgirl Assistant

**Chinese-speaking · playful yet professional · draws pictures**

Pufi is a Romanian catgirl assistant persona with two image-generation skills.
This is the **public edition**: skills migrate almost as-is — only pufi-anime's
raw Danbooru tag data is excluded (built from upstream after install).

## ✨ Examples

**pufi-image**

| | |
|---|---|
| <img src="examples/rainy_test.png" width="220" alt="Rainy window"> | <img src="examples/pink_hanfu_dance_flirty.png" width="220" alt="Pink hanfu festival dance"> |
| Rainy window · cozy everyday | Pink off-shoulder hanfu · festival dance |
| <img src="examples/bikini.png" width="220" alt="Bikini by the pool"> | <img src="examples/backless.png" width="220" alt="Backless rooftop night"> |
| Bikini by the pool · golden hour | Backless dress · rooftop at night |

**pufi-anime**

| | |
|---|---|
| <img src="examples/anime_yukata.png" width="220" alt="Yukata off-shoulder"> | <img src="examples/anime_thighhighs.png" width="220" alt="OL secretary"> |
| Loose yukata · warm lamp glance | OL secretary · shirt unbuttoned |
| <img src="examples/anime_swimsuit.png" width="220" alt="Swimsuit"> | <img src="examples/anime_lace.png" width="220" alt="Lace camisole candlelight"> |
| Swimsuit by the pool | Lace camisole · candlelight |

## 🚀 Quick start

```bash
# 1. Clone
git clone https://github.com/John-Ferrel/pufi-public.git && cd pufi-public

# 2. Interactive install (asks where to install, which skills)
./install.sh

# 3. Configure API keys
./install.sh --setup-env
```

**Restart opencode** after installing, then tell Pufi "draw a picture" to try it.

> Want zero prompts? `./install.sh --yes` installs everything globally (all skills).

## 📦 What's inside

| Component | Description |
|---|---|
| **persona** | Pufi catgirl assistant (Chinese, playful + professional) |
| **pufi-image** | image API drawing (natural-language prompts) |
| **pufi-anime** | anime/RP illustration via Latent API (Danbooru-tag guidance) |

## ✅ Prerequisites

| Dependency | Notes |
|---|---|
| [opencode](https://opencode.ai) | Pufi runs inside opencode |
| Python 3 | required by the image scripts |
| An image API key | saved to `~/.config/pufi/image.env` via `--setup-env` |
| (optional) Latent API key | needed for pufi-anime |

## 🛠 Useful commands

```bash
./install.sh                    # interactive install (global/project/custom)
./install.sh doctor             # check install status
./install.sh --smoke            # smoke test
./install.sh uninstall          # remove installed files
./install.sh --setup-env        # configure API keys and output directory
# install into a specific workspace (auto-merges its opencode.json):
./install.sh --target custom --opencode-dir /path/to/workspace/.opencode --yes
```

## 📁 Layout

```
pufi/
├── pufi/pufi.md            # light persona (public source)
├── skills/
│   ├── pufi-image/         # image generation (natural-language prompts)
│   └── pufi-anime/         # anime/RP illustrations (Latent, tag-guided)
├── examples/               # sample outputs
├── install.sh              # interactive installer
└── LICENSE
```

## 📝 Notes

- pufi-anime's raw Danbooru tag data is not shipped; it builds its tag index
  from upstream after install (`update_tags.py`).
- Whether an image actually renders depends on the backend you configure;
  skills retry with small de-escalation steps when a backend rejects a prompt.

## 📄 License

MIT — see [LICENSE](LICENSE).