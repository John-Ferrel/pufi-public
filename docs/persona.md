# 人设

**没有格式要求。** 一段文字，harness 能读进去就行。

这个仓库里的人设长得都不太一样，那是故意的：

| | 形态 |
|---|---|
| `personas/pufi/` | 表格、清单、词汇库，带 frontmatter |
| `personas/coach/` | 叙述为主，一大段一大段 |
| `personas/mira/` | 更短，几乎没有小节 |

它们都工作。写成人设、写成信、写成日记、写成规则清单，都可以。

## 唯一的硬约束来自 harness

| harness | 要求 |
|---|---|
| OpenCode | agent 文件**必须有 `description`**（frontmatter），文件名即 agent 名 |
| Claude Code | subagent 文件有 `name` / `description` |
| Codex | 无（人设直接进 `AGENTS.md`） |
| dsh | 无（同上） |

除此之外，`name`、`status`、`temperature`、分节方式——都是**我们这个样本的习惯**，不是规矩。

## 写的时候值得注意的三件事

不是规范，是经验。

**一、具体。** 抽象的特质记不住。

> ❌ 她有个故乡
> ✅ 特兰西瓦尼亚一个发音拗口的小镇，连她自己都念不对

**二、有张力。** 两边都要真的。

> 教所有人别硬撑；自己腰疼到站不直还在数最后一组。

**三、她得让人想继续聊。** 这一点最难，也最没有公式。
一个只有设定的角色，读十行就腻；一个会做丢人的事、会嫉妒、会被夸到呛住的角色，才活得下去。

写完自己读一遍：**想不想再跟她说一句话？** 不想，就还没成。

## STATUS

可选。想让人设有"关系状态"就用，不想用就不写。

- 位置：工作区根目录 `STATUS.md`（和 `PERSONA.md` 同级）
- 四个维度，不增不减：`affection` / `trust` / `desire` / `mood`
- `affection` / `trust` / `desire` 是 0–100 整数，`mood` 是短字符串
- 只存当前值，不写历史
- 只在有意义的互动后更新，每次最多 2 个字段，幅度 ≤ 15
- 人设里要写清"数值 → 行为"的分档，否则数字只是装饰

## 放进 harness

各家的位置见 [`docs/harnesses.md`](harnesses.md)。

**没有转换，也没有第二份副本。** 工作区根目录的 `PERSONA.md` 就是唯一来源，
OpenCode 的 agent 文件是指向它的软链：

```bash
ln -s ../../PERSONA.md <ws>/.opencode/agents/<name>.md
```

`description` 是 OpenCode 唯一硬性要求的字段，人设文件里已经带着。

## 私有扩展（可选）

想在公开人设上叠加只给自己看的内容（额外设定、平台级指令），放
`personas/<name>/PRIVATE.local.md`——`*.local.md` 已被 gitignore，不进仓库。
用的时候追加到 agent 文件末尾。
