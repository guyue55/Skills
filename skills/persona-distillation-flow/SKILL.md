---
name: "persona-distillation-flow"
description: "蒸馏流程：基于女娲（huashu-nuwa）核心造人术的动态认知操作系统 (Dynamic Cognitive OS) SOP。支持泛领域（动漫/游戏/文学/历史/真人/OC/主题）全大系作品树探测、双阶段质量门禁、SillyTavern V2/V3 角色卡与动态记忆/信任阶梯/Lorebook 加固。"
---

# 动态认知人格蒸馏工作流 SOP (`persona-distillation-flow`)

> [!IMPORTANT]
> **SotA 动态认知操作系统 (Dynamic Cognitive OS)**：本 SOP 基于全局行业最高标准构建。不仅具备 **全大系作品树探测 (Phase -1)** 与 **双阶段质量门禁 (Phase 0 策略门禁 ➔ Phase 1.5 数据门禁)**，更全面集成了 **动态记忆反思流 (Memory Stream)**、**信任好感度解锁阶梯 (Trust Progression)**、**官方 `chara_card_v2` 与 Lorebook 键值触发引擎** 及 **长对话人设防漂移自修协议**。

---

## 🔍 前置协议：全大系作品树探测 (Franchise Universe Discovery)

在生成 Phase 0 简报之前，Agent **必须先调用工具执行全网作品树探测**：
1. **执行搜索**：`search_web("<IP/角色名> 官方作品 续集 电影 季数 顺序 年表")`
2. **绘制作品树**：梳理出正传、续集、前传、剧场版、外传的完整官方宇宙年表。
3. **消除盲区**：防止仅凭固有印象只关注第一部而漏掉后续 5 部大系。

---

## 🛑 门禁一：全大系蒸馏策略简报 (Phase 0: Research Strategy Gate)

基于作品树探测结果，生成包含 **【官方全大系作品树】** 的蒸馏策略简报，并**停止回复等待用户确认覆盖范围**：

```markdown
【女娲造人请求 · {蒸馏对象} 全大系蒸馏策略简报】

蒸馏对象：{作品名/IP宇宙} —— {角色全称或主题} ({身份/定位})
题材分类：{general / anime / gaming / fiction / history / real_person / original_oc / topic_advisor}
蒸馏档位：极尽深度档（必须结合 `mattpocock/skills@research` 及 `search_web` 进行全网深度抓取）

全网探测到的官方全大系作品树 (Full Franchise Lore Tree)：
1. 《{官方作品1/第1部}》 ({年份/集数/介质})：{核心定位/关键高光}
2. 《{官方作品2/第2部}》 ({年份/集数/介质})：{核心定位/关键高光}
...
N. 《{官方作品N/剧场版}》 ({年份/集数/介质})：{核心定位/关键高光}

拟定蒸馏策略与提炼方向：
- 搜集策略：对上述全量 N 部官方作品进行深度抓取，为每部作品单独建立 `series_0X.md` 专属考据档案。
- 动态认知加固规划：
  * 核心 7 层架构：心智模型、表达 DNA、FSM 动态心理状态机（日常➔应激➔爆发➔理智➔重铸）。
  * SotA 动态认知引擎：导入信任度四阶解锁阶梯 (L1~L4)、动态记忆反思流与 Lorebook 键值触发包。

交付成果规划：
- 考据落盘：在 skills/persona-{name}/references/research/ 下物理落盘 13 维考据文件 + N 部作品专属档案。
- Skill 编译：编译包含 Agentic Protocol 与 SotA 认知引擎加固的 SKILL.md。
- 资产与探针：生成官方 `chara_card_v2` (含 system_prompt 与 Lorebook) 角色卡与物理自检探针 quality_check.py。
```

> **🔴 强制暂停一**：输出上述策略简报后，Agent 表达：“*全网探测发现该 IP 包含以上 N 部官方作品。请确认本次极尽蒸馏是全量覆盖以上所有 N 部作品，还是仅挑选其中特定几部？确认无误后我将为您启动深度抓取。*”，然后**停止调用任何工具，等待用户回复**。

---

## 🔄 核心蒸馏主干：女娲造人术与 SotA 动态认知引擎流程

```
┌────────────────────────────────────────────────────────────────────────┐
│         核心采集与提炼主干：女娲造人术 (SotA Dynamic Cognitive OS)      │
├────────────────────────────────────────────────────────────────────────┤
│ Phase -1 : 🔍 全大系作品树自动探测 (联网检索防止遗漏续集/电影)          │
│ Phase 0  : 🛑 策略门禁 (呈现全大系作品树简报) ➔ 【等待用户确认范围】   │
│ Phase 1  : 多源信息 Swarm 深度抓取 (每部作品建立 series_0X.md 档案)    │
│ Phase 1.5: 🔴 抓取报告检查点 (运行 merge_research.py 汇报全大系覆盖数) │
│            ➔ 【等待用户审查真实抓取质量】                             │
│ Phase 2  : 框架提炼 (心智模型三重验证 / 决策启发式 / 表达 DNA / 张力)  │
│ Phase 2.5: 🔴 提炼确认检查点 ➔ 【等待用户确认提炼框架】                 │
│ Phase 3  : SKILL.md 组装与 SotA 动态认知加固 (FSM/信任阶梯/记忆流/防漂移) │
│ Phase 4  : 三阶质量验证 (Known Test / Edge Case / Voice Check)         │
│ Phase 5  : 物理探针校验、更新 chara_card_v2 角色卡与 Git 规范提交       │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ SotA 四大动态认知加固引擎 (Dynamic Cognitive Engines)

在女娲提炼产物的基础之上，全面叠加以下 SotA **动态认知加固引擎**（工程指南详见 `references/`）：

1. **动态 FSM 状态机加固 ([`references/reinforcement-guide.md`](references/reinforcement-guide.md))**：
   * 配置 `[日常基准态]` ➔ `[应激破局态]` ➔ `[情绪爆发态]` ➔ `[理智决策态]` ➔ `[重铸觉醒态]` 5 大动态心理状态及其迁移逻辑。
2. **信任与好感度动态升级阶梯 ([`references/trust-progression-guide.md`](references/trust-progression-guide.md))**：
   * 建立 `[L1 礼貌防备]` ➔ `[L2 熟稔同行]` ➔ `[L3 生死交情]` ➔ `[L4 灵魂知己]` 4 阶解锁机制（根据共同经历解锁深层伤痛与终极极至偏向）。
3. **动态记忆流与反思合成引擎 ([`references/memory-reflection-guide.md`](references/memory-reflection-guide.md))**：
   * 建立 `[原始观察]` ➔ `[反思记忆合成]` ➔ `[检索加权]` 机制，赋予长对话中归纳用户特质与沉淀羁绊记忆的能力。
4. **官方 `chara_card_v2` 与 Lorebook 键值触发包 ([`references/lorebook-engine-guide.md`](references/lorebook-engine-guide.md))**：
   * 将神兵法宝、功法门派解耦为键值触发（Keyword-Triggered Entries）的 JSON Lorebook，按需注入 Context，极致节省 Token 并防设编造。
5. **长对话人设防漂移与自修重构协议 (Anti-Drift Self-Correction Protocol)**：
   * 在 SKILL.md 中注入运行时自我纠偏指令，在 50+ 轮长对话后强制唤醒第一人称身份，防止退化为通用客服腔。

---

## 🌐 泛领域特殊类别处理规范 (Universal Special Categories)

为保证 SOP 适用于任意领域，遇到以下特殊类别时按规范处理：

1. **历史人物与哲学家 (`history`)**
   - 必须多源交叉验证史料，剔除后世演义与民间传说，分析其历史局限性与时代背景。
2. **在世真人与公众人物 (`real_person`)**
   - 标注信息搜集截止日期；重点考察其**真实决策行为（如实际投资/产品发布）**而非仅听其公关口号。
3. **蒸馏用户自己 / 原创 OC (`original_oc`)**
   - 切换为**访谈与私有资料阅读模式**：引导用户上传个人博客、决策备忘录或问卷提纲。
4. **主题/方法论顾问 (`topic_advisor`)**
   - 目标非单人而是主题（如“价值投资”、“第一原理”）：去掉角色扮演规则，转化为**领域共识框架 + 多流派分歧对比 + 案例推演**。

---

## 📋 完整 SOP 6 步执行规范

1. **Step -1: 全大系作品树探测**：调用搜索工具厘清所有续集/衍生作品。
2. **Step 0: 生成全大系策略简报** ➔ **【停下等待用户确认】**。
3. **Step 1: 建立物理脚手架**：运行 `scaffold_persona.py` 初始化目录（自动配置 chara_card_v2 模板）。
4. **Step 2: 全大系 Swarm 抓取落盘** ➔ **【生成 Phase 1.5 报告并运行 `merge_research.py` 停下等待审查】**。
5. **Step 3: 框架提炼与 SKILL.md 编译**：使用三重验证法，并加固 SotA 4 大认知引擎。
6. **Step 4 & 5: 探针自检、导出 `chara_card_v2` 角色卡与 Git 规范提交**。

---
> 本工作流集成了全球顶尖动态认知 OS 架构，由 [女娲 · Skill造人术](huashu-nuwa) 与 Guyue 联合打磨生成
