# Skill 规范

Skill 回答一个问题：**能做什么，怎么调用。** 身份由 Persona 提供。

## 标准

本项目遵循 [Agent Skills](https://agentskills.io/specification) 开放标准，
因为 **OpenCode、Codex、Claude Code 都读它**。

```
skills/<name>/
├── SKILL.md           必需：能力、调用方式、边界
├── scripts/           可选：可直接跑的脚本
├── references/        可选：长文档、词表
├── assets/            可选：模板、素材
└── <name>.env.example 可选：配置样例（不含真实密钥）
```

### frontmatter（三边都认的字段）

```yaml
---
name: image-openai          # 必须与目录名一致
description: >-             # 1–1024 字符，写清"什么时候该用/不该用"
  Generate or edit images through an OpenAI-compatible images API.
  Use when a bot needs to produce a picture from a natural-language description.
license: MIT                # 可选
compatibility: opencode, codex, claude-code   # 可选
---
```

硬性要求（OpenCode 会校验）：

- `name` 匹配 `^[a-z0-9]+(-[a-z0-9]+)*$`
- `name` == 目录名
- `description` 1–1024 字符，把**主要用途放最前**——模型靠它决定要不要加载

## 写什么

| 章节 | 内容 |
|---|---|
| 能力边界 | 这个 skill 做什么、**不做什么** |
| 调用契约 | 命令、参数、输入输出路径 |
| 配置 | 环境变量、默认值、文件位置 |
| 流程 | 一个典型任务的步骤 |
| 坑 | 会踩的地方、失败怎么退 |

Skill 里不写角色设定、语气、某个 Bot 的偏好。

## 身份从哪来

Skill 需要角色外观时，**读工作区的文件**，而不是自带一份：

```markdown
生成前读取 `<workspace>/PERSONA.md` 与 `VISUAL.md`。
`VISUAL.md` 是外观的唯一来源。
```

这样同一个 skill 能给猫娘用，也能给体育教练用。

## 与工作区的关系

**复制**，不是引用：工作区要能 `cp -r` 搬走，不依赖这个仓库还在不在。

```
skills/<name>/             库
<ws>/.agents/skills/<name>/ 工作区实体（OpenCode + Codex 都读）
<ws>/.claude/skills/<name> → 软链，给 Claude Code
```

## 检查清单

- [ ] `name` 等于目录名，符合正则
- [ ] `description` 说清了触发场景（而不只是"这是一个画图工具"）
- [ ] 没有任何具体人格
- [ ] 脚本支持 `--prompt-only` / `--time` 这类不联网的 dry-run
- [ ] 凭据只出现在 `*.env.example`
- [ ] 输出路径默认落在工作区内（`.bot/outputs/`），不写到用户主目录
