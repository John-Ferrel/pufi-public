# AGENTS.md · 本仓库

个人 Bot 的资源库：人设正文、技能、harness 样例、工作区样例。
给在这个仓库里干活的 Agent 读。

## 改动前先读

| 要做的事 | 先读 |
|---|---|
| 改人设 | `docs/persona.md` |
| 改技能 | `docs/skill.md` |
| 装一个 Bot | `docs/install-a-bot.md` |
| 换 harness | `docs/harnesses.md` |

## 三条规则

1. 线上部署物（`~/.config/opencode/`、`~/.cc-connect/`、运行中的工作区）由用户显式迁移，仓库改动不碰它们。
2. 凭据只出现在 `*.env.example`。
3. 新目录要能被两个以上 Bot 用到，否则放进现有目录。

## Pufi 的私有段

`personas/pufi/PRIVATE.local.md` 不进仓库（`*.local.md` 已 gitignore）。
仓库只放公开人设，私有扩展本地追加。

## 验证

```bash
# skill 能否干跑
cd skills/image-openai && IMAGE_API_URL=https://example.com IMAGE_API_KEY=x \
  python3 scripts/generate_image.py --time
cd skills/image-latent && LATENT_API_KEY=x python3 scripts/generate.py --time
```
