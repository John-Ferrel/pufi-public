# 从 v1 迁移

v1 是一键安装到全局 `~/.config/opencode/` 的安装包。v2 是「一个 Bot 一个工作区」。
两者不冲突：v2 不碰现有部署，迁移是显式动作。

## 概念对应

| v1 | v2 |
|---|---|
| `~/.config/opencode/agents/pufi.md` | 工作区里的 `PERSONA.md`（软链成 agent 文件） |
| `~/.config/opencode/skills/pufi-image` | `skills/image-openai` → 复制进 `<ws>/.agents/skills/` |
| `~/.config/opencode/skills/pufi-anime` | `skills/image-latent` → 同上 |
| `~/.config/pufi/*.env` | `<ws>/.bot/*.env`（旧路径仍被读取） |
| `install.sh` | `legacy/install.sh`（保留，不再是主路径） |

## 安全前提

当前服务器的 cc-connect `work_dir` 就是仓库目录，所以**在仓库里切换分支会直接改变运行中的 Bot**。
迁移在独立工作区里做，仓库本身不动。

```bash
# 0. 备份
cp -a ~/.config/opencode/agents/pufi.md ~/pufi-agent.bak.md
cp -a ~/.config/opencode/skills/pufi-image ~/.bak-image
cp -a ~/.config/opencode/skills/pufi-anime ~/.bak-anime

# 1. 建工作区（不覆盖旧仓库）
mkdir -p ~/bots/pufi/{.opencode/agents,.bot/outputs}
cp <repo>/personas/pufi/PERSONA.md ~/bots/pufi/PERSONA.md
cp <repo>/personas/pufi/STATUS.md  ~/bots/pufi/STATUS.md
cp <repo>/personas/pufi/VISUAL.md  ~/bots/pufi/VISUAL.md
cp <repo>/workspaces/example/AGENTS.md ~/bots/pufi/AGENTS.md
ln -s ../../PERSONA.md ~/bots/pufi/.opencode/agents/pufi.md

# 2. 凭据沿用
cp ~/.config/pufi/image.env ~/bots/pufi/.bot/image.env
cp ~/.config/pufi/anime.env ~/bots/pufi/.bot/latent.env
chmod 600 ~/bots/pufi/.bot/*.env

# 3. 切换 cc-connect（先停服务）
#    ~/.cc-connect/config.toml → work_dir = "/home/<user>/bots/pufi"
```

`opencode.json` 里设 `"default_agent": "pufi"`，与软链文件名一致。

## 私有段

如果之前用的是带私有扩展的版本，把那段追到
`~/bots/pufi/.opencode/agents/pufi.md` 的末尾——注意软链会写到 `PERSONA.md`，
所以更稳的做法是复制一份 `PERSONA.md`（含私有段）再软链。

## 校验

```bash
readlink ~/bots/pufi/.opencode/agents/pufi.md     # → ../../PERSONA.md
cd ~/bots/pufi && opencode debug agents | grep pufi
```

## 回滚

把 cc-connect 的 `work_dir` 改回原值即可。旧的全局 agent 与 skill 一直没被删。
