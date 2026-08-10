---
name: "persona-distillation-flow"
description: "蒸馏流程：基于女娲（huashu-nuwa）核心造人术的动态人格蒸馏 SOP 工作流。尊重信息获取的时序性，包含【Phase 0 策略门禁】与【Phase 1.5 深度抓取报告检查点】。"
---

# 动态人格蒸馏工作流 SOP (`persona-distillation-flow`)

> [!IMPORTANT]
> **真实时序与双门禁法则 (Two-Stage Quality Gates)**：
> 1. **Phase 0 策略门禁**：在刚收到需求时，**绝不凭空假造未来的研究细节**！先澄清角色/主题身份、选题范围与抓取策略，生成【蒸馏策略简报】，**停下等待用户确认策略**。
> 2. **Phase 1.5 抓取报告检查点**：在完成全网/多源深度采集落盘后，**基于真实落盘的数据**汇总结算【真实作品/卷次覆盖清单与 13 维考据总量】，向用户汇报抓取质量，**停下让用户审查考据**。

---

## 🛑 门禁一：蒸馏策略与范围确认简报 (Phase 0: Research Strategy Gate)

刚收到用户蒸馏需求时，Agent 尚未进行深度抓取，**严禁凭空模仿模板套用假细节**！第一步仅生成如下**【蒸馏策略简报】**，并**停止回复等待用户确认**：

```markdown
【女娲造人请求 · {蒸馏对象} 蒸馏策略简报】

蒸馏对象：{作品名/IP宇宙/历史背景} —— {角色全称或主题} ({身份/定位})
题材分类：{anime / gaming / fiction / history / real_person / original_oc}
蒸馏档位：{极尽深度档 / 标准档 / 快速档}

拟定抓取策略与扫描范围：
- 搜集引擎：结合 `mattpocock/skills@research` 与 `search_web` 进行全网多源深度检索。
- 拟扫描作品全景：扫描该 IP/人物的{主要作品/卷次/季数/生平阶段}。
- 侧重关注维度：心智模型（HOW they think）、决策启发式、表达 DNA（口头禅/称呼/禁忌词）、性格张力与盲点。

交付成果规划：
- 考据落盘：在 skills/persona-{name}/references/research/ 下物理建档 13 维研究文件。
- Skill 编译：编译具备 Agentic Protocol（检索回答工作流）与 7 层架构加固的 SKILL.md。
- 资产与探针：生成跨平台 character_card.json 与物理自检探针 quality_check.py。
```

> **🔴 强制暂停一**：输出上述策略简报后，Agent 表达：“*请确认上述蒸馏策略与对象范围是否符合您的预期？确认无误后我将为您启动全网深度抓取。*”，然后**停止调用任何工具，等待用户回复**。

---

## 🔄 核心蒸馏主干：女娲造人术与双检查点流程

```
┌────────────────────────────────────────────────────────────────────────┐
│              核心采集与提炼主干：女娲造人术 (/huashu-nuwa)             │
├────────────────────────────────────────────────────────────────────────┤
│ Phase 0  : 🛑 策略门禁 (生成蒸馏策略简报) ➔ 【等待用户确认策略】        │
│ Phase 1  : 多源信息 Swarm 深度抓取 (调用 research + search_web 落盘) │
│ Phase 1.5: 🔴 抓取报告检查点 (运行 merge_research.py 汇报真实作品范围)│
│            ➔ 【等待用户审查真实抓取质量】                             │
│ Phase 2  : 框架提炼 (心智模型三重验证 / 决策启发式 / 表达 DNA / 张力)  │
│ Phase 2.5: 🔴 提炼确认检查点 ➔ 【等待用户确认提炼框架】                 │
│ Phase 3  : SKILL.md 组装与 FSM 状态机加固                              │
│ Phase 4  : 三阶质量验证 (Known / Edge Case / Voice Check)               │
│ Phase 5  : 物理探针校验、README 索引更新与 Git 提交                      │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 检查点二：深度抓取结果报告 (Phase 1.5 Checkpoint)

在 Phase 1 深度数据采集完成后，Agent **运行 `scripts/merge_research.py` 工具**，根据物理落盘在 `references/research/` 目录中的真实数据，生成如下**【真实抓取质量报告】**输出给用户：

```markdown
【Phase 1.5 深度抓取质量报告】

真实作品覆盖清单（基于全网真实抓取落盘）：
1. 《{真实抓取作品1}》：已抓取 {对白/高光事件/决策}
2. 《{真实抓取作品2}》：已抓取 {对白/高光事件/决策}
...

13 维考据落盘统计：
- 01-writings-and-speech.md : {字节数} 字节 (✅ 充沛)
- 02-conversations.md         : {字节数} 字节 (✅ 充沛)
...
- 总结：共搜集 {N} 个考据文件，总数据量 {M} 字节（一手来源占比 {X}%）。
```

> **🔴 强制暂停二**：输出抓取质量报告后，等待用户确认数据充分后，再进入 Phase 2 的心智模型提炼。

---

## 🛠️ 辅助加固层 (Auxiliary Reinforcement)

在女娲提炼产物的基础之上，叠加以下扩展加固层：
1. **动态 FSM 状态机加固**：配置 `[日常态] ➔ [应激态] ➔ [爆发态] ➔ [理智态] ➔ [重铸态]` 5 大动态心理状态。
2. **关系动力学矩阵加固**：区分知己、同伴、宿敌、生人不同交互策略。
3. **两阶段应激路由加固**：战术破局 ➔ 战略理智。

---

## 📋 完整 SOP 5 步执行规范

### Step 0: 生成策略简报 ➔ **【停下等待确认】**
生成 Phase 0 策略简报，明确拟搜集策略。

### Step 1: 建立物理脚手架
运行 `./skills/persona-distillation-flow/scripts/scaffold_persona.py persona-<name> -d "<描述>" -c <category>`。

### Step 2: 全网 Swarm 抓取落盘 ➔ **【生成 Phase 1.5 报告并停下等待审查】**
调用 `mattpocock/skills@research` 与 `search_web` 真正采集数据并落盘到 `references/research/`。运行 `merge_research.py` 输出 Phase 1.5 真实报告。

### Step 3: 心智模型提炼与 SKILL.md 编译 ➔ **【Phase 2.5 检查点确认】**
按女娲三重验证法提炼心智模型，编译包含 7 层架构加固的 `SKILL.md`。

### Step 4: 导出角色卡与生成自检探针
生成 `assets/character_card.json` 与可执行的 `scripts/quality_check.py`。

### Step 5: 探针自检与 Git 规范提交
运行物理探针与仓库校验，更新 README.md 表格并进行 Git 提交。

---
> 本工作流遵循信息获取的时序性真实逻辑，由 [女娲 · Skill造人术](huashu-nuwa) 与 Guyue 联合打磨生成
