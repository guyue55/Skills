# Agent Skills 汇总与制作仓库

本仓库为个人/团队的 **AI Agent Skills** 集中存储、制作与管理项目。用于沉淀各类可复用的 Agent 技能（Skills）、工作流模版以及自动化脚本。

---

## 📂 仓库结构

```
Skills/
├── README.md                   # 本主文档（Skill 目录与制作指南）
├── .gitignore                  # Git 忽略配置
├── .template/                  # Skill 标准定义模板
│   ├── SKILL.md                # 规范模板文件
│   └── README.md               # 模板使用说明
├── skills/                     # 所有 Skill 模块汇总存储目录
│   └── example-skill/          # 示例 Skill 模块
│       └── SKILL.md
└── scripts/                    # 仓库维护与自动化脚手架
    ├── create_skill.py         # 脚手架：一键创建新 Skill 模版
    └── validate_skills.py      # 校验器：检查所有 Skill 格式与合规性
```

---

## 🗂️ 已收录 Skill 目录

| Skill 名称 | 描述 | 路径 |
| :--- | :--- | :--- |
| `example-skill` | 示例 Skill：展示如何在本仓库中规范定义与组织 Skill 模块 | [`skills/example-skill/SKILL.md`](skills/example-skill/SKILL.md) |

*(随着新增 Skill 的加入，请同步更新上表)*

---

## 🚀 如何添加或制作新的 Skill

### 方式一：使用脚手架快速新建（推荐）

直接在根目录下运行 Python 脚手架脚本：

```bash
python3 scripts/create_skill.py <skill-name> -d "<Skill功能描述>"
```

**示例：**
```bash
python3 scripts/create_skill.py git-workflow-helper -d "自动化管理分支和 Git 提交规范的 Skill"
```

该命令将自动在 `skills/git-workflow-helper/` 目录下生成包含标准 YAML Frontmatter 的 `SKILL.md`，并创建 `scripts/` 与 `references/` 子目录。

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
python3 scripts/validate_skills.py
```

校验内容包括：
- 是否包含 `SKILL.md`
- YAML Frontmatter 是否存在且格式正确
- `name` 是否与文件夹名称完全一致
- `description` 是否完整

---

## 💡 Skill 编写规范提示

- **单一职责**：每个 Skill 专注解决某一类特定问题或工作流。
- **触发明确**：在 `SKILL.md` 的“触发条件”中清晰列出 Agent 何时应激活此 Skill。
- **自包含**：若 Skill 包含辅助 Python/Bash 脚本或文档，请统一放在其子目录下的 `scripts/` 或 `references/` 中。
