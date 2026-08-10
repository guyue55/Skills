---
name: "persona-distillation-flow"
description: "蒸馏流程：基于女娲（huashu-nuwa）核心造人术的人格蒸馏 SOP 工作流。以女娲思维提炼为引擎，辅以七层人设与动态状态机进行加固扩展，用于任意角色/人物/主题的极尽蒸馏与 Skill 建设。"
---

# 动态人格蒸馏工作流 SOP (`persona-distillation-flow`)

> [!IMPORTANT]
> **定位与哲学**：本 SOP **绝不绑定死板固定的格式**，而是以官方 **女娲造人术（`/huashu-nuwa`）** 为核心采集与提炼引擎。我们在实战中总结的“七层人设”、“动态 FSM 状态机”等架构，仅作为对女娲产物的**辅助加固与增强层（Reinforcement Layer）**。本流程具备极强的扩展性，方便未来随实践不断重构与演进。

---

## 🔄 核心引擎：以 `/huashu-nuwa` 为主干

```
┌────────────────────────────────────────────────────────────────────────┐
│                   核心蒸馏引擎：女娲造人术 (/huashu-nuwa)               │
├────────────────────────────────────────────────────────────────────────┤
│ Phase 0  : 路径分流与蒸馏档位确认 (快速 / 标准 / 深度)                 │
│ Phase 1  : 多源信息采集 Swarm (著作/对话/表达/他者/决策/时间线 6维度)   │
│ Phase 1.5: 🔴 调研 Review 检查点                                       │
│ Phase 2  : 框架提炼 (心智模型三重验证 / 决策启发式 / 表达 DNA / 张力)  │
│ Phase 2.5: 🔴 提炼确认检查点                                           │
│ Phase 3  : Skill 组装与架构加固 (注入 Agentic Protocol)                │
│ Phase 4  : 质量验证 (Known Test / Edge Case / Voice Check)             │
│ Phase 5  : 双 Agent 精炼与优化 (auto-skill-optimizer / skill-creator)   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ 辅助加固层 (Auxiliary Reinforcement Layers)

在女娲标准产物的基础之上，根据角色需求，可选择性叠加以下**扩展加固层**（随实践持续演进，不强行死板硬套）：

### 1. 动态心理状态机加固 (FSM State Machine Extension)
当角色用于深度角色扮演（RP）或复杂博弈对话时，在 SKILL.md 中加固 **5 大动态心理状态及其迁移规则**，防止长上下文中的“人格漂移”：
* `[日常/基准态]` ➔ `[应激/破局态]` ➔ `[情绪/爆发态]` ➔ `[理智/决策态]` ➔ `[重铸/觉醒态]`

### 2. 关系动力学矩阵加固 (Relational Dynamics Engine)
加固角色对待知己、手足、仇敌、生人/用户时的不同态度模式与示例对白。

### 3. 多维情境应激引擎加固 (Scenario Stress Engine)
加固角色在绝境被围逼、至亲伤亡、被诬陷离间、低谷失意时的两阶段应激路由（战术破局 ➔ 战略理智）。

---

## 📋 5 步 SOP 执行流程

### Step 1: 初始化与脚手架搭建
运行 CLI 脚本建立标准化目录结构：
```bash
./skills/persona-distillation-flow/scripts/scaffold_persona.py persona-<name> -d "<角色/主题描述>" -c <category>
```
结构严格遵循 Nuwa 规范：
```text
skills/persona-<name>/
├── SKILL.md                          # 最终 Skill 入口
├── scripts/quality_check.py          # 探针脚本
├── assets/character_card.json        # 跨平台角色卡
└── references/research/              # 13 维考据落盘目录 (01~07.md + 分卷文件)
```

### Step 2: 激活 `/huashu-nuwa` 驱动多源采集
**调用 `huashu-nuwa` + `mattpocock/skills@research` + `search_web`** 针对 6 大维度进行全面抓取并写入 `references/research/` 目录：
1. `01-writings-and-speech.md` (著作/发言)
2. `02-conversations.md` (即兴对话)
3. `03-expression-dna.md` (表达基因)
4. `04-external-views.md` (他者评价与负面批评)
5. `05-decisions.md` (真实决策)
6. `06-timeline.md` (时间线)

### Step 3: 框架提炼与 Skill 组装
遵循女娲 Phase 2 的**三重验证法**筛选心智模型，并在 Phase 3 组装 `SKILL.md`，按需叠加七层加固模块。

### Step 4: 导出角色卡与生成质量探针
导出 `assets/character_card.json`，并配置针对该 Skill 规范的 `scripts/quality_check.py` 物理自检探针。

### Step 5: 校验落盘与 Git 提交
1. 执行物理探针：`python3 skills/persona-<name>/scripts/quality_check.py`
2. 执行全库校验：`./scripts/validate_skills.py`
3. 更新 `README.md` 索引表格并提交 Git。

---

## 迭代与扩展指南 (Evolution & Refactoring)

由于经验积攒是动态演进的，本 SOP 允许后续：
- **增加新加固层**：如“信任度阶梯（Trust Ladder）”、“语言呼吸频率控制”。
- **重构研判库架构**：支持主题 Skill (`[topic]-framework`) 与人物 Skill (`[person]-perspective`) 的无缝切换。

---
> 本工作流作为 [女娲 · Skill造人术](huashu-nuwa) 的二次封装与流程编排 SOP  
