---
name: "example-skill"
description: "示例 Skill：展示如何在本仓库中规范定义与组织 Skill 模块"
---

# 示例 Skill (Example Skill)

## 概述
这是一个用于演示仓库结构的示例 Skill。本仓库用于集中收集、制作和管理各种 AI Agent Skill。

## 触发条件
当需要参考 Skill 的文件结构或验证校验工具时触发。

## 目录规范
标准的 Skill 包含以下结构：
- `SKILL.md`: 必需，定义名称、描述、Trigger 以及使用步骤。
- `scripts/`: 可选，包含该 Skill 依赖的可执行辅助脚本。
- `references/`: 可选，包含相关的参考文档、设计规范或 Schema。
- `assets/`: 可选，包含输出产物模板、图标或静态资源。

## 使用流程
1. 使用 `python3 scripts/create_skill.py <your-skill-name>` 建立新的 Skill 目录。
2. 编辑生成的 `skills/<your-skill-name>/SKILL.md` 填充业务逻辑。
3. 运行 `python3 scripts/validate_skills.py` 确保格式无误。
