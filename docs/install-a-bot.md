# 装一个 Bot

**读者是 Agent。** 用户说一句需求，你按这份文档写文件。

一个 **Bot = 一个工作区目录**。所有状态都在文件里，`cp -r` 能搬走。

---

## 目标形态

```
<ws>/
├── AGENTS.md                    规则（不含人设）
├── PERSONA.md                   人设正文 ← 唯一来源
├── VISUAL.md                    外观（可选；图像 Skill 读它）
├── STATUS.md                    当前状态（可选）
├── opencode.json                OpenCode 配置（default_agent）
├── .opencode/agents/<name>.md → ../../PERSONA.md   软链，不是副本
├── .agents/skills/<skill>/      技能（可选）
└── .bot/{*.env,outputs/}        凭据与产物，gitignore
```

人设只有 **`PERSONA.md` 一份**。OpenCode 的 agent 文件是指向它的软链，
所以不存在第二份副本，也不会不同步。

---

## 1. 选人设

```bash
sed -n '1,6p' personas/*/PERSONA.md      # 看 description 像不像
```

判定：身份、语气、亲密尺度三者都对。只有一个维度像，就改一份新的。

## 2. 建工作区

```bash
mkdir -p <ws>/.opencode/agents <ws>/.bot/outputs <ws>/.agents/skills
cp personas/<name>/PERSONA.md <ws>/PERSONA.md
cp personas/<name>/STATUS.md  <ws>/STATUS.md          # 有的话
cp personas/<name>/VISUAL.md  <ws>/VISUAL.md          # 有的话
cp workspaces/example/AGENTS.md <ws>/AGENTS.md
cp workspaces/example/.gitignore <ws>/.gitignore
```

## 3. 接进 harness

### OpenCode

```bash
ln -s ../../PERSONA.md <ws>/.opencode/agents/<name>.md
```

`<ws>/opencode.json`：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "default_agent": "<name>",
  "instructions": ["AGENTS.md"]
}
```

`default_agent` 必须等于软链文件名，否则启动时用的不是这个 Bot。

### Codex / Claude Code / dsh

这些 harness 不能切主 agent，人设直接进 `AGENTS.md`：

```markdown
## 角色

<PERSONA.md 正文>
```

然后把 `## Persona` 一节改成"见 `## 角色`"。

> Claude Code：用了 `AGENTS.md` 就不要再放 `CLAUDE.md`。

## 4. 技能（可选）

```bash
cp -r skills/<skill> <ws>/.agents/skills/
cp skills/<skill>/*.env.example <ws>/.bot/<name>.env    # 让用户自己填，chmod 600
```

图像 Skill 会读 `<ws>/VISUAL.md` 拿角色外观——所以 `VISUAL.md` 要放在工作区根目录。

## 5. IM 接入（可选）

| bridge | 抄 | 目标 |
|---|---|---|
| cc-connect | `bridges/cc-connect/config.toml.example` | 用户的 `~/.cc-connect/config.toml` |

`[[projects]]` 的 `work_dir` 指向 `<ws>`。bridge 不是 harness，只负责收发消息。

## 6. 自检

```bash
ls <ws>/PERSONA.md <ws>/STATUS.md <ws>/AGENTS.md
readlink <ws>/.opencode/agents/<name>.md      # 应指向 ../../PERSONA.md
cd <ws> && opencode debug agents | grep <name>   # agent 能被发现
```

- [ ] `default_agent` == 软链文件名
- [ ] `PERSONA.md` 只有一份，工作区里没有第二个副本
- [ ] `.gitignore` 含 `.bot/*.env` 与 `.bot/outputs/`
- [ ] 没有真实密钥写进被跟踪文件

## 汇报

```
已创建：~/bots/coach-vic/
harness：OpenCode，default_agent = coach
人设：coach（周漾）
技能：无

你需要手动做：
1. ~/.cc-connect/config.toml 加 [[projects]]，work_dir = ~/bots/coach-vic
2. 重启 cc-connect
```
