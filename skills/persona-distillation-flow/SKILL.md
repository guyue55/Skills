---
name: "persona-distillation-flow"
description: "通用工作流：工业级七层深度人格蒸馏（7-Layer Universal Persona Architecture）SOP。当用户请求蒸馏、提炼、新建或升级任意动漫、游戏、影视、历史人物、现实名人或原创 IP 角色的人格 Skill 时激活使用。"
---

# 通用七层深度人格蒸馏 SOP (`persona-distillation-flow`)

> [!IMPORTANT]
> 本 SOP 抽取自实战炼化经验，是一套**领域无关（Domain-Agnostic）、抽象且全面**的工业级 7 层深度人格蒸馏工作流。它不依赖于任何特定题材（无论是动漫、游戏、影视、历史人物、现实名人还是原创 IP），能确保 Agent 在新会话中自动、完整输出最高品质的深度人设。

---

## ⚙️ 一、 核心能力模型 (Core Capabilities)

人格蒸馏不仅是收集台词，而是通过以下 6 维工程能力对角色进行逆向还原：

1. **知识与考据搜集能力 (Lore Intelligence)**：全网检索并提炼角色的生平履历、重大转折与名场面事实。
2. **心智与价值观逆向工程 (Mental Model & Values)**：提取其底层第一性原理、核心渴望、深层恐惧与防御机制。
3. **动态心理状态机建模 (FSM Behavioral Engine)**：将角色复杂的行为抽象为 5 大动态心理状态及其迁移逻辑。
4. **关系与交互矩阵建模 (Relational Dynamics Engine)**：定义角色面对知己、同伴、宿敌、生人时的态度差异。
5. **表达 DNA & 词汇光谱 (Linguistic Spectrum)**：提取角色的口头禅、标点呼吸节奏、句式长短与绝对禁忌光谱 (Anti-OOC)。
6. **跨平台导出与探针物理自检 (Export & Verification)**：导出 Tavern/OpenClaw JSON 角色卡并编写 Python 质量校验探针。

---

## 🏗️ 二、 通用七层深度人设结构 (Universal 7-Layer Architecture)

蒸馏输出的 `SKILL.md` 必须严格包含以下 7 层的抽象结构：

```
┌────────────────────────────────────────────────────────────────────────┐
│                   通用 7 层深度人设架构 (7-Layer)                      │
├────────────────────────────────────────────────────────────────────────┤
│ 一、 核心感知与心理画像 (Identity Profile) ：核心渴望/恐惧/防御机制/价值观  │
│ 二、 动态心理状态机 (FSM State Machine)  ：[基准态]➔[应激]➔[爆发]➔[决策]➔[重铸]│
│ 三、 关系动力学矩阵 (Relational Matrix)  ：针对不同交互对象的策略与示例      │
│ 四、 多维情境应激引擎 (Scenario Stress Engine)：绝境/重创/诱惑/低谷应对法则   │
│ 五、 回答工作流 (Agentic Protocol)       ：事实类问题先检索搜集真相再回答   │
│ 六、 表达 DNA 与词汇光谱 (Lexicon Spectrum)：高频专属词/呼吸节奏/防OOC禁忌词  │
│ 七、 诚实边界与物理验证 (System Verification)：考据文件全量检查与状态机自检 │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 三、 标准 5 步蒸馏流程 (Step-by-Step SOP)

### Step 1: 需求解析与脚手架初始化 (Scaffolding)
运行通用 CLI 脚手架，选择题材分类（`anime` / `gaming` / `fiction` / `history` / `real_person` / `original_oc`）：
```bash
./skills/persona-distillation-flow/scripts/scaffold_persona.py persona-<name> -d "<角色描述>" -c <category>
```

### Step 2: 双搜集引擎深度抓取 (Dual-Engine Research)
**⚠️ 结合 `mattpocock/skills@research` 与 `search_web` 搜集原始语料与事实：**
1. **01-writings-and-speech.md**：原生作品/现实中的直接演讲、对白与作品文本。
2. **02-conversations.md**：与其他核心人物的高博弈对白样本。
3. **03-expression-dna.md**：自称、口头禅、专业术语与句式长短习惯。
4. **04-external-views.md**：外界对该角色的评价、认知盲区与偏见。
5. **05-decisions.md**：生平重大转折抉择与悲剧/困境应对。
6. **06-timeline.md**：跨卷次/年代的完整人生弧光时间线。
7. **07-lore-and-world.md**：所处世界观规则、社会阶层与文化背景。
8. **series_01_*.md ~ series_N_*.md**：按阶段/季数/卷次划分的专属考据。

### Step 3: 7 层深度人设抽象与编译 (7-Layer Persona Compilation)
将研究考据整理并提炼为符合通用 7 层架构的 `SKILL.md`，重点完成**动态心理状态机**与**关系矩阵**的建模。

### Step 4: 跨平台标准卡片导出 (Character Card Generation)
在 `assets/character_card.json` 中导出标准 OpenClaw / Tavern 格式的跨平台 JSON 角色卡。

### Step 5: 物理自检与版本落盘 (Verification & Versioning)
1. 运行角色专有探针：`python3 skills/persona-<name>/scripts/quality_check.py` 确保输出 `100% 物理 PASS`。
2. 运行仓库合规校验：`./scripts/validate_skills.py` 确保全库校验通过。
3. 在根目录 `README.md` 中增加角色索引，并执行 Git 提交。

---

## 🎯 四、 蒸馏通用原则与防 OOC 红线 (Universal Principles)

1. **绝对中立原则**：蒸馏过程必须严守角色原有的领域背景，不得将某个领域的惯用套路（如武侠/科幻词汇）强加给其他题材的角色。
2. **动态解耦原则**：角色应激反应必须基于情境动态演纳，严禁硬编码单一死板的复读台词。
3. **单入口原则**：角色目录下绝不创建 `README.md`，唯一入口必须为 `SKILL.md`。

---
> 本工作流由 [女娲 · Skill造人术](https://github.com/alchaincyf/nuwa-skill) 抽象打磨生成
