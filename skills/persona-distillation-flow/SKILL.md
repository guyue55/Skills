---
name: "persona-distillation-flow"
description: "蒸馏流程：基于女娲（huashu-nuwa）核心造人术的人格蒸馏 SOP 工作流。包含【蒸馏简报与提示词门禁 (Prompt Brief Gate)】，支持任意角色/主题的极尽蒸馏与 Skill 建设。"
---

# 动态人格蒸馏工作流 SOP (`persona-distillation-flow`)

> [!IMPORTANT]
> **核心门禁规则 (Quality Gate)**：在执行任何代码改动、脚手架创建或深度搜索之前，AI Agent **必须先根据用户输入生成结构化的【女娲造人请求·极尽蒸馏简报】，并停下来等待用户显式确认**。未经用户确认，绝对不得擅自开启后置执行步骤！

---

## 🛑 门禁步骤：生成蒸馏简报并等待确认 (Phase 0: Prompt Brief Gate)

收到用户的蒸馏需求后，Agent **第一步**必须对目标 IP/角色进行全局扫描，生成如下结构的**【蒸馏造人简报】**输出给用户，并**停止回复等待用户确认**：

```markdown
【女娲造人请求 · {角色/主题}全大系极尽深度蒸馏简报】

目标角色：{作品名/IP宇宙} —— {角色全称} ({身份/称号/定位})
蒸馏档位：极尽深度档（必须结合 mattpocock/skills@research 及 search_web 进行全网深度抓取）

核心覆盖范围（必须全量覆盖官方 N 部大系/作品/卷次）：
1. 《{作品1}》：{关键事件/高光对白/转折点}
2. 《{作品2}》：{关键事件/高光对白/转折点}
...
N. 《{作品N}》：{关键事件/高光对白/转折点}

核心侧重点与提炼要求：
1. 心智模型：提炼{3-5个核心心智模型与决策启发式}。
2. 表达 DNA：还原{称呼习惯、语气停顿、高频口头禅、经典名言与战斗/逻辑战吼}。
3. 防 OOC 红线：严格禁止出现{现代流行语/违背性格与时代背景的降智言行}。
4. 物理落盘与探针要求：
   - 必须在 skills/persona-{name}/references/research/ 下物理落盘 13 维调研文件及单作品专属档案。
   - 必须包含 Agentic Protocol（回答工作流，遇到事实问题先搜索研究）。
   - 在 skills/persona-{name}/assets/ 下生成跨平台 character_card.json 角色卡。
   - 必须编写并物理运行 skills/persona-{name}/scripts/quality_check.py 校验探针，确保 100% PASS。

输出目标：存入当前仓库的 skills/persona-{name}/SKILL.md，并同步更新项目 README.md 的 Skill 目录与进行 Git 规范提交。
```

> **🔴 强制暂停**：输出上述简报后，Agent 必须表达：“*请确认上述蒸馏简报与范围是否符合您的预期？确认无误后我将为您开启脚手架与全网深度抓取。*”，然后**停止调用任何工具，等待用户回复**。

---

## 🔄 核心引擎：以 `/huashu-nuwa` 为主干

用户确认简报后，启动标准女娲蒸馏引擎：

```
┌────────────────────────────────────────────────────────────────────────┐
│              核心采集与提炼引擎：女娲造人术 (/huashu-nuwa)             │
├────────────────────────────────────────────────────────────────────────┤
│ Phase 0  : 🛑 蒸馏简报与提示词门禁 (Prompt Brief Gate) ➔ 用户确认     │
│ Phase 1  : 6 维多源信息采集 Swarm (著作/对话/表达/他者/决策/时间线)    │
│ Phase 1.5: 🔴 调研 Review 检查点 (运行 merge_research.py 审查数据量)  │
│ Phase 2  : 框架提炼 (心智模型三重验证 / 决策启发式 / 表达 DNA / 张力)  │
│ Phase 2.5: 🔴 提炼确认检查点                                           │
│ Phase 3  : Skill 组装与架构加固                                        │
│ Phase 4  : 质量验证 (Known Test / Edge Case / Voice Check)             │
│ Phase 5  : 双 Agent 精炼与优化 (auto-skill-optimizer / skill-creator)   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ 辅助加固层 (Auxiliary Reinforcement Layers)

在女娲标准产物的基础之上，根据角色需求，选择性叠加以下**扩展加固层**：

### 1. 动态心理状态机加固 (FSM State Machine Extension)
在 SKILL.md 中配置 **5 大动态心理状态及其迁移规则**：
* `[日常/基准态]` ➔ `[应激/破局态]` ➔ `[情绪/爆发态]` ➔ `[理智/决策态]` ➔ `[重铸/觉醒态]`

### 2. 关系动力学矩阵加固 (Relational Dynamics Engine)
加固角色对待知己、手足、仇敌、生人/用户时的不同态度模式与示例对白。

### 3. 多维情境应激引擎加固 (Scenario Stress Engine)
加固角色在绝境被围逼、至亲伤亡、被诬陷离间、低谷失意时的两阶段应激路由（战术破局 ➔ 战略理智）。

---

## 📋 5 步 SOP 执行流程

### Step 0: 简报门禁与用户确认 (Prompt Brief)
生成结构化蒸馏简报，**停下等待用户确认**。

### Step 1: 物理脚手架搭建 (Scaffolding)
用户确认后，运行 CLI 脚本建立标准化目录结构：
```bash
./skills/persona-distillation-flow/scripts/scaffold_persona.py persona-<name> -d "<角色/主题描述>" -c <category>
```

### Step 2: 激活 `/huashu-nuwa` 驱动多源采集
调用 `huashu-nuwa` + `mattpocock/skills@research` + `search_web` 针对简报中的作品范围进行全量抓取，并在 `references/research/` 目录下建档。

### Step 3: 框架提炼与 Skill 组装
遵循女娲 Phase 2 的**三重验证法**筛选心智模型，在 Phase 3 组装 `SKILL.md`，并叠加 FSM 状态机加固模块。

### Step 4: 导出角色卡与生成质量探针
导出 `assets/character_card.json`，并配置针对该 Skill 规范的 `scripts/quality_check.py` 物理自检探针。

### Step 5: 校验落盘与 Git 提交
1. 执行物理探针：`python3 skills/persona-<name>/scripts/quality_check.py`
2. 执行全库校验：`./scripts/validate_skills.py`
3. 更新 `README.md` 索引表格并提交 Git。

---
> 本工作流由 [女娲 · Skill造人术](huashu-nuwa) 与 Guyue 联合提炼生成
