# Harness 与 Bridge

## 两条规则

| harness | 人设放哪 |
|---|---|
| OpenCode（可切主 agent） | `.opencode/agents/<name>.md` → 软链到 `PERSONA.md` |
| Codex / Claude Code / dsh / 其他 | `AGENTS.md` |

Bridge（如 cc-connect）不在此列：它只把 IM 消息转给 harness。

```
IM 平台 → bridge → harness → 工作区
```

## 四家对照

| | OpenCode | Codex | Claude Code | dsh |
|---|---|---|---|---|
| 人设 | `.opencode/agents/<n>.md` | `AGENTS.md` | `AGENTS.md` | `AGENTS.md` |
| 切主 agent | ✅ Tab / `default_agent` | — | — | — |
| 项目规则 | `AGENTS.md` | `AGENTS.md` | `AGENTS.md` | `AGENTS.md` + `AGENTS.local.md` |
| 全局规则 | `~/.config/opencode/AGENTS.md` | `~/.codex/AGENTS.md` | `~/.claude/CLAUDE.md` | `~/.dsh/AGENTS.md` |
| Skills | `.agents/skills/`、`.opencode/skills/`、`.claude/skills/` | `.agents/skills/` | `.claude/skills/` | 未确认 |
| 配置 | `opencode.json` | `~/.codex/config.toml` | `.claude/settings.json` | `$DSH_HOME/profiles/` |

## OpenCode

- agent 文件：`.opencode/agents/<file>.md`，文件名即 agent 名，正文即 system prompt
- 指向 `../../PERSONA.md` 的软链可以用，实测有效（`opencode debug agents` 能发现）
- `opencode.json` 的 `default_agent` 决定启动时用谁
- 规则：`AGENTS.md`，从 cwd 向上查找；`opencode.json` 的 `instructions` 可追加文件
- skills：`name` 必须与目录名一致，匹配 `^[a-z0-9]+(-[a-z0-9]+)*$`；`description` 1–1024
- 改完 skills 要重开会话
- 实测（v2.2.1）：agent 文件能被发现，工作区 `opencode.json` 与全局合并；
  skill 运行时加载未验证

## Codex

- `AGENTS.md`：从仓库根逐层到 cwd，每层取**一个**（`AGENTS.override.md` 优先于 `AGENTS.md`）
- 合并上限 32 KiB（`project_doc_max_bytes`），超了截断
- skills：`.agents/skills/`（含父目录与仓库根）、`~/.agents/skills/`；支持软链
- 未实测

## Claude Code

- **有 `CLAUDE.md`（或 `CLAUDE.local.md`）时就不读 `AGENTS.md`**，二选一
- skills：`.claude/skills/`，支持软链
- 未实测

## dsh（DeepSeek Harness）

- 指令链：`~/.dsh/AGENTS.md` → 项目根到 cwd 每层 `AGENTS.md`（找不到用 `CLAUDE.md`）
  → 同目录 `AGENTS.local.md` / `CLAUDE.local.md`
- 单文件 > 1 MiB 忽略；每条链有字节预算（默认 65536）
- 没有 agent profile，人设只能进 `AGENTS.md`；`profile` 是插件配置栈
- 这段是 guidance，不是沙箱；硬约束用 `DSH_PERMISSION_MODE`
- `$DSH_HOME/AGENTS.md` 同时可能是"全局"和"项目根"，别用软链绕（官方 issue #3285）
- 未实测

## 样例

| 文件 | 用途 |
|---|---|
| `harnesses/opencode/opencode.json` | 最小工作区配置 |
| `harnesses/opencode/agents/example.md` | agent 文件写法 |
| `harnesses/codex/config.toml.example` | 指令预算与 fallback 名 |
| `harnesses/claude-code/settings.example.json` | settings 骨架 |
| `bridges/cc-connect/config.toml.example` | IM 接入 |
