# pufi-public

给个人 Agent 用的资源库：**人设正文、技能、harness 配置样例、一个能跑的工作区**。

没有安装器，没有服务，没有脚本。Agent 读文档、写文件，就是一个 Bot。

```
用户：照 pufi-public 建一个御姐体育教练，OpenCode + cc-connect 接飞书
Agent：读 docs/install-a-bot.md → 复制 personas/coach → 建工作区 → 完
```

## 一个 Bot 一个工作区

```
<ws>/
├── AGENTS.md                    规则
├── PERSONA.md                   人设 ← 唯一来源
├── VISUAL.md                    外观（可选）
├── STATUS.md                    当前状态（可选）
├── .opencode/agents/<name>.md → ../../PERSONA.md    软链，不是副本
├── .agents/skills/              技能（可选）
└── .bot/                        凭据与产物（gitignore）
```

- **Persona**：一段正文。没有格式要求，harness 能读进去就行。
- **Skill**：能力，不含人格。
- **Harness**：跑 agent 的东西（OpenCode / Codex / Claude Code / dsh）。
- **Bridge**：接 IM 的东西（cc-connect）。

## 目录

```
docs/          装 Bot / 人设 / 技能 / harness / 迁移
personas/      人设（pufi、coach、mira、模板）
skills/        能力（文生图 × 2）
harnesses/     各 harness 的配置样例
bridges/       IM 接入样例
workspaces/    一个能跑的工作区
legacy/        v1 安装器
docs/archive/  历史材料
```

## 快速开始

```bash
cp -r workspaces/example ~/bots/my-bot
cd ~/bots/my-bot
opencode            # default_agent = mira
```

## 人设放哪

| harness | 位置 |
|---|---|
| OpenCode | `.opencode/agents/<name>.md` → 软链到 `PERSONA.md` |
| Codex / Claude Code / dsh | 正文接进 `AGENTS.md` 的 `## 角色` |

## 旧版

v1 的 `install.sh` 在 `legacy/`，装到全局 `~/.config/opencode/`，与多工作区不兼容。

MIT，见 `LICENSE`。
