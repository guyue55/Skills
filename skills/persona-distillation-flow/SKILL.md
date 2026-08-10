---
name: "persona-distillation-flow"
description: "工作流：工业级七层深度人格蒸馏（7-Layer Deep Persona Architecture）工作流 SOP。当用户请求蒸馏、提炼、新建或升级任意动漫、游戏、影视、历史人物或原创 IP 角色的人格 Skill 时激活使用。"
---

# 工业级七层深度人格蒸馏 SOP (`persona-distillation-flow`)

> [!IMPORTANT]
> 本 SOP 是在《虹猫蓝兔》全系列实战中沉淀的**工业级 7 层深度人格蒸馏工作流**。当用户要求“蒸馏某个角色”、“新建角色人设”、“打造高保真角色 Skill”时，AI Agent 必须严格遵循本 SOP 的 5 步流程进行。

---

## 🛠️ 一键脚手架工具 (CLI Scaffolder)

在开始蒸馏新角色前，可优先使用脚手架自动生成标准目录与 13 维研判库：
```bash
./skills/persona-distillation-flow/scripts/scaffold_persona.py persona-<name> -d "<角色简短描述>"
```

---

## 📋 5 步极尽蒸馏标准 Sop

### Step 1: 物理脚手架搭建 (Scaffolding)
建立符合 AGENTS.md 规范的标准角色目录：
```text
skills/persona-<name>/
├── SKILL.md                          # [主入口] 包含 7 层深度人设架构
├── scripts/
│   └── quality_check.py              # [探针] 自动校验 7 层架构与档案完整性
├── assets/
│   └── character_card.json           # [跨平台] Tavern/OpenClaw JSON 角色卡
└── references/research/              # [13维全景研判档案库]
    ├── 01-writings.md ~ 07-franchise-lore.md
    └── series_01_*.md ~ series_06_*.md (各部剧集/卷次专属档案)
```

### Step 2: 全网深度考据与 13 维建档 (Deep Research)
**⚠️ 拒绝凭空想象！必须结合 `search_web` 与 `research` 获取真实事实：**
1. **01-writings.md**：生平台词、心法招式与名言考据。
2. **02-conversations.md**：原著经典对白与正邪博弈。
3. **03-expression-dna.md**：自称、尊称、高频口头禅与禁忌词。
4. **04-external-views.md**：他人视角评价与性格盲点/偏见。
5. **05-decisions.md**：重大转折抉择与悲剧/绝境处理。
6. **06-timeline.md**：角色全生平跨卷次时间线。
7. **07-franchise-lore.md**：所属 IP 宇宙的世界观与角色定位。
8. **series_01_*.md ~ series_N_*.md**：IP 每部作品/卷次中的专属高光档案。

### Step 3: 7 层深度人设 Markdown 编译 (7-Layer Engine)
将搜集到的事实，编译为符合 **工业级 7 层深度人设架构** 的 `SKILL.md`：
1. **一、 核心感知与心理画像**（核心渴望、深层恐惧、心理防御机制、价值观）。
2. **二、 动态心理状态机 (FSM)**（定义 5 大动态心理状态及其迁移触发条件）。
3. **三、 关系动力学矩阵**（定义对待知己、手足、仇敌、生人/用户等不同对象的交互策略）。
4. **四、 多维情境应激引擎**（定义绝境围攻、至亲受害、被诬陷离间、低谷失意等场景应激哲学）。
5. **五、 回答工作流 (Agentic Protocol)**（定义“事实类问题先搜集案情真相再回答”的检索机制）。
6. **六、 表达 DNA 与词汇光谱**（高频专属词、标点呼吸节奏与绝对禁忌光谱）。
7. **七、 诚实边界与物理验证**（记录 13 维档案与状态机自检勾选项）。

### Step 4: 跨平台 JSON 角色卡导出 (Character Card Export)
在 `assets/character_card.json` 中导出标准 JSON 格式角色卡，方便导入 Tavern / SillyTavern / OpenClaw 等前端平台使用。

### Step 5: 双重探针与 Git 提交 (Physical Verification & Git Commit)
1. 运行角色专有探针：`python3 skills/persona-<name>/scripts/quality_check.py` 确保输出 `100% 物理 PASS`。
2. 运行仓库合规校验：`./scripts/validate_skills.py` 确保全库校验通过。
3. 更新根目录 `README.md` 的 Skill 索引表格。
4. 执行 Git 提交：`git add . && git commit -m "feat(skill): 新增 persona-<name> 7层深度人格Skill"`。

---

## 🎯 蒸馏防 OOC 红线 (Guardrails)

1. **严禁抽象空话**：不能只写“性格温柔”，必须给出“外柔内刚”的具体事实证据与状态机规则。
2. **严禁机械套用硬编码台词**：阶段反应路由必须解耦，依据角色的表达 DNA 动态演纳，不得全局复读同一句台词。
3. **单入口原则**：角色目录下绝不得创建 `README.md`，唯一入口必须为 `SKILL.md`。

---
> 本工作流由 [女娲 · Skill造人术](https://github.com/alchaincyf/nuwa-skill) 与 Guyue 联合提炼生成
