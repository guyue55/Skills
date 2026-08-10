# Skill 贡献与邀请指南 (CONTRIBUTING.md)

欢迎参与 **Agent Skills 汇总与制作仓库** 的建设！本指南适用于人类开发者与 AI Agent 协同贡献新的 Skill。

---

## 🤝 如何贡献一个新的 Skill

无论是新建 Skill，还是将已有 Skill 导入/合并到本仓库，请按以下步骤操作：

### 1. 确认 Skill 定位与单一职责
- 每个 Skill 应专注解决一个明确的问题或工作流（One skill, one job）。
- Skill 名称必须使用小写英文字母、数字和连字符（例如 `git-workflow-helper`）。

### 2. 使用脚手架生成标准结构
请在根目录下使用脚手架创建模版：

```bash
./scripts/create_skill.py <your-skill-name> -d "<功能描述与触发词>"
```

这将自动生成如下标准的解剖结构：
```
skills/<your-skill-name>/
├── SKILL.md            # [必需] 主定义文件
├── scripts/            # [可选] 可执行辅助脚本
│   └── .gitkeep
├── references/         # [可选] Schema 或参考文档
│   └── .gitkeep
└── assets/             # [可选] 静态资源或输出模版
    └── .gitkeep
```

> [!CAUTION]
> **禁忌提示**：请勿在 `skills/<your-skill-name>/` 目录下添加 `README.md`，所有导引请统一整合至 `SKILL.md` 正文中。

### 3. 编写 `SKILL.md` 正文
确保 `SKILL.md` 包含标准的 YAML Frontmatter 头部：

```yaml
---
name: "<your-skill-name>"
description: "清晰说明此 Skill 的功能，以及 Agent 何时应激活此 Skill 的触发条件"
---
```

规范结构建议：
- `# Skill 标题`
- `> [!NOTE]` 概述
- `## 触发条件与使用时机 (When to Use)`
- `## 详细工作流 (Workflow & Instructions)`
- `## 红线与禁忌 (Guardrails & Anti-Patterns)`
- `## 示例 (Examples)`

### 4. 运行合规性校验
提交 Pull Request (PR) 前，必须运行校验脚本：

```bash
./scripts/validate_skills.py
```

必须确保输出 `🎉 所有 Skill 模块校验通过！` 方可提交。

### 5. 更新主索引
在仓库根目录下的 [`README.md`](README.md) 中更新技能目录表格，记录新 Skill 的名称、描述与链接。

---

## 📋 Skill 质量审核清单 (Quality Checklist)

在审核或提交 PR 时，请按以下清单进行检查：

- [ ] **名称匹配**：`skills/<name>/` 目录名称与 `SKILL.md` 中的 `name` 字段完全一致。
- [ ] **触发明确**：Frontmatter 中的 `description` 同时包含“功能”与“明确的触发场景”。
- [ ] **绝无硬编码 (De-hardcoding)**：正文及脚本中绝无绝对路径（如 `/Users/username/...` 或 `/home/username/...`）。
- [ ] **拒绝虚假占位符 (Anti-Laziness)**：无未完成的 `TODO:`、`pass` 或 `...` 占位符号。
- [ ] **文件极简**：子 Skill 目录下无 `README.md`，只有 `SKILL.md` 及关联资源。
- [ ] **版本追踪**：空的 `scripts/`、`references/`、`assets/` 目录保留 `.gitkeep` 占位文件。

---

## 📩 社区邀请与协同

如果您发现了优质的开源 Skill，欢迎通过 Issue 或 PR 邀请将其整理并合并入本仓库。合力打造高质量的 AI Agent 技能库！
