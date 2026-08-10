---
name: "{{SKILL_NAME}}"
description: "{{SKILL_DESCRIPTION}}"
---

# {{SKILL_TITLE}}

> [!NOTE]
> 简要说明此 Skill 的作用、核心心智及适用场景。

## 触发条件与使用时机 (When to Use)
明确指出在什么情况下（例如用户提到哪些关键词、触发指令或需要完成何种任务时）应当激活此 Skill。

## 前置要求 (Prerequisites)
列出运行或使用此 Skill 所需的前置依赖、环境变量、工具或系统权限。

## 详细工作流 (Workflow & Instructions)
按步骤详细说明执行流程：
1. **步骤一：输入校验与环境探针**
   - 检查必要输入，探针准备。
2. **步骤二：核心逻辑执行**
   - 逐步完成核心任务，遵循渐进式披露。
3. **步骤三：输出验证与结果交付**
   - 物理验证，确保交付无瑕疵。

## 红线与禁忌 (Guardrails & Anti-Patterns)
> [!IMPORTANT]
> - **环境脱敏 (De-hardcoding)**: 严禁硬编码绝对个人路径（如 `/Users/...` 或 `/home/...`）。
> - **绝对真实 (Exhaustive Truth)**: 拒绝 `pass`、`...` 或占位符敷衍，代码需可运行。

## 示例 (Examples)
提供典型的使用示例或前后对比，方便参考。
