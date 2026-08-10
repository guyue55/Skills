# Agent Skills 汇总与制作仓库

本仓库为个人/团队的 **AI Agent Skills** 集中存储、制作与管理项目。用于沉淀各类可复用的 Agent 技能（Skills）、工作流模版以及自动化脚本。

> [!IMPORTANT]
> **AI Agent 强制遵照指令 (For All AI Tools & Agents)**:
> 本仓库的所有 AI 工具与 Agent（如 Antigravity、Codex、Claude Code、Cursor、Windsurf、Copilot 等）在进入本项目后，**必须严格遵循 [`AGENTS.md`](AGENTS.md) 中定义的项目地图、操作 SOP 与刚性红线**。

---

## 🤖 AI 工具指引与规范入口

- 📘 **通用 AI 操作指南**：[`AGENTS.md`](AGENTS.md)（定义了完整的地图、步骤 SOP 与刚性红线，所有 AI 工具统一遵照）
- 🤝 **贡献与邀请指南**：[`CONTRIBUTING.md`](CONTRIBUTING.md)（规范 Skill 的贡献、审核与邀请流程）

---

## 📂 仓库结构

```
Skills/
├── README.md                   # 本主文档（Skill 目录与概览）
├── AGENTS.md                   # 通用 AI Agent 指南与操作地图（唯一真理源）
├── CONTRIBUTING.md             # 贡献、提交与邀请协作指南
├── .github/                    # GitHub 自动化 CI 流水线
│   └── workflows/
│       └── skill-ci.yml       # PR / Push 自动校验工作流
├── .gitignore                  # Git 忽略配置
├── .template/                  # Skill 标准定义模板
│   ├── SKILL.md                # 规范模板文件
│   └── README.md               # 模板使用说明
├── skills/                     # 所有 Skill 模块汇总存储目录
│   └── example-skill/          # 示例 Skill 模块
│       └── SKILL.md
└── scripts/                    # 仓库维护与自动化脚手架 (+x)
    ├── create_skill.py         # 脚手架：一键创建新 Skill 模版
    ├── validate_skills.py      # 校验器：检查所有 Skill 格式、脱敏与红线
    └── setup_hooks.sh          # Git Hook 挂载：一键配置本地 pre-commit 自动校验
```

---

## 🗂️ 已收录 Skill 目录

| Skill 名称 | 描述 | 路径 |
| :--- | :--- | :--- |
| `example-skill` | 示例 Skill：展示如何在本仓库中规范定义与组织 Skill 模块 | [`skills/example-skill/SKILL.md`](skills/example-skill/SKILL.md) |
| `persona-hongmao` | 角色人格：扮演《虹猫蓝兔七侠传》中的七剑之首虹猫，包含其心智模型、豪侠表达风格与长虹剑法 | [`skills/persona-hongmao/SKILL.md`](skills/persona-hongmao/SKILL.md) |

*(随着新增 Skill 的加入，请同步更新上表)*

---

## 🚀 如何添加或制作新的 Skill

### 方式一：使用脚手架快速新建（推荐）

直接在根目录下运行 Python 脚手架脚本：

```bash
./scripts/create_skill.py <skill-name> -d "<Skill功能描述与触发条件>"
```

**示例：**
```bash
./scripts/create_skill.py git-workflow-helper -d "自动化管理分支和 Git 提交规范的 Skill"
```

该命令将自动在 `skills/git-workflow-helper/` 目录下生成包含标准 YAML Frontmatter 的 `SKILL.md`，并创建 `scripts/`、`references/` 与 `assets/` 子目录（均含 `.gitkeep`）。

---

### 方式二：手动添加已有的 Skill

若要将现有的 Skill 存入本仓库：

1. 在 `skills/` 目录下新建对应名称的文件夹，例如 `skills/my-awesome-skill/`。
2. 将该 Skill 的 `SKILL.md` 以及关联资源复制到该目录下。
3. 确保 `SKILL.md` 顶部包含合规的 YAML Frontmatter：

```yaml
---
name: "my-awesome-skill"
description: "清晰说明此 Skill 的作用以及触发场景"
---
```

---

## 🔍 合规性校验

在提交或 Push 到 GitHub 前，请运行校验脚本确保所有 Skill 均符合规范：

```bash
./scripts/validate_skills.py
```

校验内容包括：
- 是否包含 `SKILL.md`
- YAML Frontmatter 是否存在且格式正确
- `name` 是否与文件夹名称完全一致
- `description` 是否完整
- 是否存在绝对路径硬编码（De-hardcoding）
- 是否存在未完成的 `TODO:` / `FIXME:` / `pass` 占位符
- 子 Skill 目录下是否包含多余的 `README.md`

详见 [`CONTRIBUTING.md`](CONTRIBUTING.md) 及 [`AGENTS.md`](AGENTS.md)。
