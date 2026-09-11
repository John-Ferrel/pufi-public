# Pufi 🐱💕 罗马尼亚猫娘助手

**中文交流 · 撒娇与专业并存 · 会画画**

Pufi 是一个罗马尼亚猫娘助手 persona，附两个画图 skill。这是**公开版**：skill 几乎原样迁移，
仅 pufi-anime 的原始 Danbooru tag 数据不随仓库发布（安装后从上游构建）。

## ✨ 示例

**pufi-image**

| | |
|---|---|
| <img src="examples/rainy_test.png" width="220" alt="雨天窗边"> | <img src="examples/pink_hanfu_dance_flirty.png" width="220" alt="粉色汉服园游会"> |
| 雨天窗边 · 温馨日常 | 粉色改良汉服 · 园游会起舞 |
| <img src="examples/bikini.png" width="220" alt="泳装池畔"> | <img src="examples/backless.png" width="220" alt="露背裙天台"> |
| 泳装池畔 · 金色黄昏 | 露背裙 · 天台夜景 |

**pufi-anime**

| | |
|---|---|
| <img src="examples/anime_yukata.png" width="220" alt="浴衣半敞"> | <img src="examples/anime_thighhighs.png" width="220" alt="OL 秘书"> |
| 浴衣半敞 · 暖灯回眸 | OL 秘书 · 白衬衫半解 |
| <img src="examples/anime_swimsuit.png" width="220" alt="泳装"> | <img src="examples/anime_lace.png" width="220" alt="蕾丝内衣烛光"> |
| 泳装池畔 | 蕾丝内衣 · 烛光 |

## 🚀 快速开始（三行）

```bash
# 1. 下载
git clone https://github.com/John-Ferrel/pufi-public.git && cd pufi-public

# 2. 一键安装（交互式，会问你装到哪、装哪些）
./install.sh

# 3. 配置 API key
./install.sh --setup-env
```

装完**重启 opencode**，然后对 Pufi 说"画一张图"试试～

> 想跳过交互？`./install.sh --yes` 一行完成（默认 global + 全部 skill）。

## 📦 包含什么

| 组件 | 说明 |
|---|---|
| **persona** | Pufi 猫娘助手（中文，撒娇+专业） |
| **pufi-image** | 图像 API 画 Pufi（自然语言 prompt） |
| **pufi-anime** | Latent API 画动漫/RP 场景（Danbooru tag 引导） |

## ✅ 你需要准备

| 依赖 | 说明 |
|---|---|
| [opencode](https://opencode.ai) | Pufi 运行在 opencode 里 |
| Python 3 | 画图脚本依赖 |
| 图像 API key | 填入 `~/.config/pufi/image.env`（`--setup-env` 引导） |
| （可选）Latent API key | 用 pufi-anime 时需要 |

## 🛠 常用命令

```bash
./install.sh                    # 交互安装（global/project/custom 可选）
./install.sh doctor             # 检查安装状态
./install.sh --smoke            # 冒烟测试
./install.sh uninstall          # 卸载
./install.sh --setup-env        # 配置 API key 和输出目录
# 装到指定工作区（会自动合并该工作区的 opencode.json）：
./install.sh --target custom --opencode-dir /path/to/workspace/.opencode --yes
```

## 📁 目录结构

```
pufi/
├── pufi/pufi.md            # 轻度 persona（public 源）
├── skills/
│   ├── pufi-image/         # 图像生成（自然语言 prompt）
│   └── pufi-anime/         # 动漫/RP 图（Latent，tag 引导）
├── examples/               # 示例图
├── install.sh              # 交互式安装器
└── LICENSE
```

## 📝 说明

- pufi-anime 的原始 Danbooru tag 数据不随仓库发布；安装后运行 `update_tags.py` 从上游构建。
- 图像能否渲染取决于你配置的后端；被拒绝时会按 skill 内置规则小幅降档重试。

## 📄 License

MIT —— 见 [LICENSE](LICENSE)。