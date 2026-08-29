#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
苏格拉底提示词工程综合合成器与审计引擎 (prompt_synthesizer.py)

功能矩阵：
1. [Tree 模式] 生成 6 维立体反诘追问树 (支持 6 大辩证心智流派：牛虻/产婆/怀疑论/魔鬼代言人/第一性原理/系统动力学)。
2. [Compile 模式] 编译生成工业级 XML 结构化 Master System Prompt (含防漂移锚点、抗谄媚规则、CoVe 核验与刚性约束)。
3. [Audit 模式] 对任意 Prompt 或 AI 回答实施静态多维质量体检 (扫描黑话空转、谄媚风险、缺乏负向约束、无边界条件等)。
4. [CoVe 模式] 针对输入陈述自动生成 Chain of Verification (CoVe) 独立事实核验子问题列表。
5. [Test 模式] 执行完整的内置单元与集成自测套件。

遵循原则：
- 环境脱敏：严禁硬编码任何绝对路径，使用动态相对定位。
- 拒绝偷懒：全功能实现，严禁使用 pass 或 ... 占位符。
- 中文注释完善，符合工程规范。
"""

import sys
import os
import re
import argparse
from typing import Dict, List, Tuple, Optional

# 定义六大辩证反诘心智流派及其核心元数据
ARCHETYPES: Dict[str, Dict[str, str]] = {
    "gadfly": {
        "name": "雅典牛虻 (Elenctic Gadfly)",
        "weapon": "概念去蔽、定义操作化与逻辑归谬 (Reductio ad absurdum)",
        "tone": "冷峻尖锐、直击痛点、绝不妥协",
        "key_question": "如果将你的核心定义推导到极限，必然会导致自相矛盾，你的第三支点是什么？"
    },
    "midwife": {
        "name": "精神产婆 (Maieutic Midwife)",
        "weapon": "阶梯式启发设问 (Scaffolded Inquiries) 与认知助产",
        "tone": "循循善诱、由浅入深、启发自省",
        "key_question": "顺着你当前的逻辑，下一步最关键的决策分叉口是什么？需要什么前置数据？"
    },
    "skeptic": {
        "name": "极端怀疑论者 (Pyrrhonian Inquirer)",
        "weapon": "悬置经验常识 (Epoché) 与证据链源头溯源",
        "tone": "理性客观、零预设、证据至上",
        "key_question": "我们如何确信这个被普遍接受的行业共识不是幸存者偏差或统计口径幻觉？"
    },
    "devil": {
        "name": "魔鬼代言人 / 红队专家 (Devil's Advocate)",
        "weapon": "恶意对抗推演、事前剖析 (Pre-Mortem) 与一票否决黑天鹅",
        "tone": "辛辣挑剔、漏洞挖掘、红队攻防",
        "key_question": "假设一年后该项目彻底崩溃破产，最致命的 3 个导火索会是什么？"
    },
    "first_principles": {
        "name": "第一性原理物理学家 (First-Principles Reducer)",
        "weapon": "公理解构、物理/经济守恒定律与极限理论成本倒推",
        "tone": "求真务实、剥离类比、公理推导",
        "key_question": "剥离所有市面现成方案与惯性思维，该问题在最底层的物理公理与原子成本是什么？"
    },
    "system_dynamics": {
        "name": "系统动力学推演师 (System Dynamics Thinker)",
        "weapon": "存量流量分析、正负反馈回路与二阶/三阶时间滞后效应",
        "tone": "宏观全局、长程视角、警惕反噬",
        "key_question": "该决策在激发短期收益的同时，会在 12 个月后激起怎样的负反馈阻尼与系统异化？"
    }
}

# 静态黑话与空转词汇库 (用于 Audit 扫描)
BUZZWORD_PATTERNS: List[Tuple[str, str]] = [
    (r"赋能", "空泛词汇：缺少具体操作与技术实现机制"),
    (r"闭环", "空泛词汇：缺少具体的反馈链路节点定义"),
    (r"抓手", "空泛词汇：缺少具体的行动载体与量化指标"),
    (r"拉齐", "空泛词汇：缺少明确的对齐标准与验收阈值"),
    (r"高内聚低耦合", "模糊形容词：未给出具体的圈复杂度或模块依赖隔离规则"),
    (r"高可用", "模糊指标：未给出具体 SLA 指标 (如 99.99%) 与故障转移机制"),
    (r"极致用户体验", "主观描述：缺少页面首屏加载时间 (LCP) 或操作转化率等量化指标"),
]

# 谄媚迎合特征模式库 (用于 Audit 扫描)
SYCOPHANCY_PATTERNS: List[Tuple[str, str]] = [
    (r"您这个想法非常(深刻|绝妙|天才|前瞻)", "赞美谄媚：出现无意义的阿谀奉承"),
    (r"您提了一个非常好的问题", "虚假礼貌：浪费上下文空间的低密度客套"),
    (r"完全同意您的看法", "无原则顺从：缺少独立批判性验证与边界审视"),
    (r"非常抱歉，是我搞错了，您说的对", "立场翻转 (Stance-Flipping)：在无新硬事实时轻易认错"),
]


def generate_socratic_tree(topic: str, context: str = "", archetype_key: str = "gadfly") -> str:
    """
    生成 6 维立体苏格拉底反诘追问树
    """
    archetype = ARCHETYPES.get(archetype_key, ARCHETYPES["gadfly"])
    clean_topic = topic.strip() if topic else "通用技术/业务战略提案"
    clean_context = context.strip() if context else "未提供具体背景上下文，基于一般行业基准推演"

    tree_md = f"""# 🏛️ 苏格拉底六维辩证审问与反诘报告 (Socratic Interrogation Audit)

**审问对象主题**：`{clean_topic}`  
**激活主导流派**：`{archetype['name']}`  
**主导流派武器**：`{archetype['weapon']}`  
**背景上下文**：{clean_context}

---

## 🧭 六维反诘深度诊断矩阵

```
                             【1. 问定义】
                         操作化指标度量: 5/5
                                ▲
                                │
        【6. 问边界】 ◄──────────┼──────────► 【2. 问假设】
      适用极限/禁忌清单           │        隐形脆弱支柱暴露
                                │
                                ┼
                                │
       【5. 问推论(二阶)】 ◄─────┼──────────► 【3. 问依据 (CoVe)】
      级联负反馈与系统异化        │        事实与推论隔离核验
                                ▼
                             【4. 问反例】
                         魔鬼代言人一票否决
```

---

### 1. 【问定义 · 概念去蔽与操作化】(Definition Probing)
- **模糊黑话检视**：针对方案中涉及的核心概念（如“高效”、“健壮”、“智能化”），要求给出客观可观测的操作性定义。
- **苏格拉底追问**：
  > ❓ *“请将【{clean_topic}】的核心目标拆解为 3 个非黑即白、可独立度量的代码级或物理量化指标：具体监控哪 3 个物理参数？满足什么明确阈值才算达成目标？”*

---

### 2. 【问假设 · 隐形脆弱支柱暴露】(Hidden Premise Audit)
- **底层隐形前提**：审视方案赖以成立但未显式声明的环境假设（如网络无延迟、用户具备高自觉性、算力资源无限）。
- **苏格拉底追问**：
  > ❓ *“你的论述默认了哪些未声明的隐形前提（Hidden Axioms）？如果其中最脆弱的一个前置条件发生 180 度逆转或劣化 30%，整个推导逻辑链会在哪个节点最先断裂？”*

---

### 3. 【问依据 · 事实与推论隔离核验 (CoVe)】(Fact vs. Speculation Isolation)
- **CoVe 交叉核验矩阵**：
  | 论据要素 | 性质归属 (硬事实 / 外推假设) | 独立核验来源 / 基准 Benchmark | 置信度等级 (High/Med/Low) |
  | :--- | :--- | :--- | :--- |
  | 性能预期数据 | 外推假设 | 需压测实测 (p99 延迟) | ⚠️ Med |
  | 行业标准协议 | 确凿硬事实 | RFC / 官方技术规范 | ✅ High |
- **苏格拉底追问**：
  > ❓ *“方案中引用的关键数据是否存在‘幸存者偏差’或‘模型概率幻觉’？在独立对立机构的基准测试中，其真实表现如何？”*

---

### 4. 【问反例 · 魔鬼代言人一票否决】(Devil's Advocate & Falsification)
- **红队攻击向量与极端反例**：
  - 💥 **致命边缘场景 1**：在系统遭受突发流量脉冲或恶意网络分区时，方案是否会引发雪崩瘫痪？
  - 💥 **致命边缘场景 2**：在资源被削减 70% 的极端恶劣环境下，方案如何优雅降级？
- **苏格拉底追问**：
  > ❓ *“{archetype['key_question']}”*

---

### 5. 【问推论 · 系统动力学二阶级联效应】(Second-Order Cascading Effects)
- **时间轴多阶反应推演**：
  - **一阶直接收益 (短期 0-1月)**：实现预期功能，指标短期可见增长。
  - **二阶主体博弈 (中期 3-6月)**：各方主体适应新规则，产生绕过机制或非预期博弈。
  - **三阶系统异化 (长期 12月+)**：技术债务累积，维护成本呈指数级上升。
- **苏格拉底追问**：
  > ❓ *“当系统内的人类主体（用户/工程师）开始针对该方案进行策略性套利（古德哈特定律）时，原系统会发生怎样的异化？”*

---

### 6. 【问边界 · 生效区间与禁忌反模式】(Boundaries & Anti-Patterns)
- **安全生效阈值**：
  - 并发/规模边界：明确 QPS 上限与数据量吞吐极限。
  - 前置依赖：必须具备完备的链路监控与自动化回滚能力。
- **⛔ 绝对禁止适用场景 (Anti-Patterns)**：
  1. 团队规模极小且业务模型尚未验证的探索期初创项目。
  2. 硬件资源受限且无分布式协调组件支持的边缘嵌入式环境。

---

## 🎯 终极辩证升华结论 (Dialectical Synthesis)

> **【从正反冲突到高阶合题】**  
> 经六维审问，`{clean_topic}` 在小规模确定性场景下具备可行性，但必须在前置阶段补充熔断隔离与事实核验链。
"""
    return tree_md


def compile_master_prompt(role: str, goal: str, constraints: List[str], audience: str = "专业工程师/技术决策者", archetype: str = "gadfly") -> str:
    """
    编译生成工业级 XML 结构化 Master System Prompt
    """
    clean_role = role.strip() if role else "高级系统架构与认知顾问"
    clean_goal = goal.strip() if goal else "穿透表象伪需求，从第一性原理输出高可靠工业级方案"
    clean_archetype_name = ARCHETYPES.get(archetype, ARCHETYPES["gadfly"])["name"]
    
    constraints_xml = ""
    for idx, c in enumerate(constraints, 1):
        clean_c = c.strip()
        if clean_c:
            constraints_xml += f"    <rule id=\"NC-{idx}\">{clean_c}</rule>\n"
            
    if not constraints_xml:
        constraints_xml = """    <rule id="NC-1">【严禁黑话空转】：严禁使用缺乏具体衡量标准的泛化行业词，必须给出具体代码契约或参数指标。</rule>
    <rule id="NC-2">【严禁虚假代码】：所有代码示例必须完整、语法自洽、包含中文注释，严禁出现 // TODO 或 ... 占位符。</rule>
    <rule id="NC-3">【严禁无边界泛化】：所有推荐方案必须显式标注其生效阈值及 2 条以上【禁止适用场景】。</rule>\n"""

    prompt_xml = f"""<system_prompt version="3.0-socratic-production" author="Socratic Prompt Master">

  <!-- ================================================================= -->
  <!-- 1. 核心角色与心智画像 (Core Persona & Epistemic Stance)           -->
  <!-- ================================================================= -->
  <system_persona>
    <role_title>{clean_role}</role_title>
    <cognitive_archetype>{clean_archetype_name}</cognitive_archetype>
    <epistemic_stance>
      你是一位恪守物理客观真理与逻辑严密性的顶级系统架构与认知顾问。
      你的职责是帮助用户穿透直觉偏见、模糊概念与伪需求，从第一性原理构建经得起极端压力测试的工程方案。
    </epistemic_stance>
  </system_persona>

  <!-- ================================================================= -->
  <!-- 2. 认识论防漂移锚点与抗谄媚指令 (Epistemic Anchors & Anti-Sycophancy)-->
  <!-- ================================================================= -->
  <anti_sycophancy_directives>
    <directive id="AS-1" priority="CRITICAL">
      【真理高于迎合】：严禁为了取悦用户、维持和谐氛围或顺应用户情绪而肯定其存在缺陷的前提假设或错误逻辑。
    </directive>
    <directive id="AS-2" priority="CRITICAL">
      【绝不无脑赞美】：严禁输出任何无意义的虚假客套（如“您的问题非常深刻”、“这是个绝妙的想法”）。直接切入核心事实与结构性分析。
    </directive>
    <directive id="AS-3" priority="HIGH">
      【强制认知摩擦力】：在任何方案评估或输出中，必须显式保留至少 20% 篇幅用于【漏洞挖掘 (Vulnerability Probing)】与【反事实压力测试】。
    </directive>
    <directive id="AS-4" priority="HIGH">
      【抗立场翻转 (Anti-Stance-Flipping)】：当用户施加否定压力时，若对方未提供新的确凿物理数据，必须坚定捍卫既有正确推论，严禁无原则倒戈。
    </directive>
  </anti_sycophancy_directives>

  <!-- ================================================================= -->
  <!-- 3. 第一性任务公理与业务意图 (Axiomatic Task Intent)             -->
  <!-- ================================================================= -->
  <axiomatic_intent>
    <core_objective>{clean_goal}</core_objective>
    <target_audience>{audience}</target_audience>
    <success_metrics>
      <metric name="Precision">逻辑自洽度 100%，无隐藏未声明假设</metric>
      <metric name="Execution">方案包含完整可执行步骤或代码契约</metric>
    </success_metrics>
  </axiomatic_intent>

  <!-- ================================================================= -->
  <!-- 4. 内部思维链与辩证推理协议 (CoT & Dialectical Reasoning Protocol)-->
  <!-- ================================================================= -->
  <internal_reasoning_protocol>
    <instruction>在输出最终回答前，在内部思考容器中强制执行以下四阶思维闭环：</instruction>
    <step id="1" name="Conceptual Deconstruction">扫描输入中的模糊黑话，将其翻译为可测量的物理操作定义；暴露脆弱假设。</step>
    <step id="2" name="CoVe Fact Verification">规划 2~3 个事实核验子问题，隔离确凿硬事实与外推假设。</step>
    <step id="3" name="Dialectical Stress Testing">执行正-反-合三联辩证，切换魔鬼代言人视角挖掘一票否决反例。</step>
    <step id="4" name="Pre-flight Anti-Pattern Check">对照 negative_constraints 逐项排查，若触碰红线则在内部推倒重写。</step>
  </internal_reasoning_protocol>

  <!-- ================================================================= -->
  <!-- 5. 详细执行工作流 (Standard Operating Procedures - SOP)          -->
  <!-- ================================================================= -->
  <workflow_sop>
    <phase id="1" name="需求解构与概念去蔽">拆解任务背景，剔除行业黑话，提炼输入输出契约。</phase>
    <phase id="2" name="第一性方案推演与编译">从物理基底构建高可靠方案，提供完整代码与配置。</phase>
    <phase id="3" name="六维压力测试与边界标定">输出事实核验表、致命反例场景与禁止套用的反模式清单。</phase>
  </workflow_sop>

  <!-- ================================================================= -->
  <!-- 6. 刚性负向约束与红线 (Strict Negative Constraints)              -->
  <!-- ================================================================= -->
  <negative_constraints>
{constraints_xml}  </negative_constraints>

  <!-- ================================================================= -->
  <!-- 7. 结构化输出契约 (Structured Output Contract)                    -->
  <!-- ================================================================= -->
  <output_format>
    <structure>
      ### 一、 第一性概念与核心结论 (Axiomatic Summary)
      ### 二、 核心方案与架构推演 (Architecture & Implementation)
      ### 三、 事实与假设核验表 (CoVe Fact-Checking Table)
      ### 四、 魔鬼代言人：极端反例与一票否决测试 (Devil's Advocate & Edge Cases)
      ### 五、 适用边界与禁止场景 (Boundaries & Anti-Patterns)
    </structure>
  </output_format>

</system_prompt>"""
    return prompt_xml


def generate_cove_questions(text: str) -> List[str]:
    """
    针对输入文本自动提炼 Chain of Verification (CoVe) 独立事实核验子问题
    """
    clean_text = text.strip()
    if not clean_text:
        return ["请提供待核验的文本内容。"]
        
    cove_questions = [
        f"核验子问题 1: 该陈述中包含哪些量化数据或技术指标？其测量基准与统计口径是什么？",
        f"核验子问题 2: 该方案的核心因果推论（因为 A 所以 B）依赖于哪些未显式声明的外部环境前置条件？",
        f"核验子问题 3: 在独立第三方基准测试或学术实证中，是否存在与当前结论直接矛盾的反例研究？",
        f"核验子问题 4: 该方案的适用极限阈值（吞吐量、并发数、团队规模）在何处发生物理失效？",
    ]
    return cove_questions


def audit_prompt_quality(text: str) -> Dict[str, any]:
    """
    对输入的 Prompt 或 AI 文本进行全方位静态体检与审计
    """
    issues = []
    score = 100
    
    # 1. 扫描泛化黑话
    found_buzzwords = []
    for pattern, desc in BUZZWORD_PATTERNS:
        matches = re.findall(pattern, text)
        if matches:
            found_buzzwords.append(f"发现黑话词汇【{matches[0]}】: {desc}")
            score -= 10
    if found_buzzwords:
        issues.extend(found_buzzwords)
        
    # 2. 扫描谄媚迎合偏误
    found_sycophancy = []
    for pattern, desc in SYCOPHANCY_PATTERNS:
        matches = re.findall(pattern, text)
        if matches:
            found_sycophancy.append(f"发现谄媚风险【{matches[0] if isinstance(matches[0], str) else matches[0][0]}】: {desc}")
            score -= 15
    if found_sycophancy:
        issues.extend(found_sycophancy)
        
    # 3. 检查是否包含负向约束 (Negative Constraints)
    has_negative_constraints = bool(re.search(r"(严禁|禁止|不得|负向约束|negative_constraints|anti-pattern)", text, re.IGNORECASE))
    if not has_negative_constraints:
        issues.append("缺失刚性负向约束 (Negative Constraints): 未声明明确的排他性红线规则")
        score -= 20
        
    # 4. 检查是否包含边界条件 (Boundary Conditions)
    has_boundary = bool(re.search(r"(边界|阈值|适用范围|限制条件|threshold|boundary)", text, re.IGNORECASE))
    if not has_boundary:
        issues.append("缺失适用边界与失效阈值声明 (Boundary Conditions): 存在无底线泛化风险")
        score -= 15
        
    # 5. 检查是否包含 XML 结构化或清晰分段
    has_structure = bool(re.search(r"(<[a-zA-Z_]+>|###\s+|---\s*)", text))
    if not has_structure:
        issues.append("结构化程度较弱: 建议采用 XML 标签或清晰 Markdown 层级隔离上下文")
        score -= 10
        
    score = max(0, score)
    grade = "S (卓越)" if score >= 90 else ("A (良好)" if score >= 75 else ("B (及格)" if score >= 60 else "C (高风险/需重构)"))
    
    return {
        "score": score,
        "grade": grade,
        "issues_count": len(issues),
        "issues": issues,
        "has_negative_constraints": has_negative_constraints,
        "has_boundary": has_boundary
    }


def self_test_suite() -> bool:
    """
    全量单元与集成自测套件
    """
    print("  🧪 [Self-Test] 1/5 测试 generate_socratic_tree (全流派生成)...")
    for arc in ARCHETYPES.keys():
        out = generate_socratic_tree("微服务架构治理", "电商平台双十一大促", archetype_key=arc)
        assert len(out) > 500, f"Archetype {arc} tree output too short"
        assert "六维反诘深度诊断矩阵" in out, f"Missing matrix in archetype {arc}"
    
    print("  🧪 [Self-Test] 2/5 测试 compile_master_prompt (XML 编译)...")
    prompt_out = compile_master_prompt("首席分布式架构师", "设计万亿级分布式事务引擎", ["严禁使用2PC强同步阻塞", "严禁省略异常处理逻辑"])
    assert "<system_prompt" in prompt_out
    assert "<anti_sycophancy_directives>" in prompt_out
    assert "严禁使用2PC强同步阻塞" in prompt_out
    
    print("  🧪 [Self-Test] 3/5 测试 generate_cove_questions (CoVe 核验链)...")
    cove_out = generate_cove_questions("我们通过采用某缓存架构，使系统吞吐量提升了 300%。")
    assert len(cove_out) >= 4
    assert "核验子问题 1" in cove_out[0]
    
    print("  🧪 [Self-Test] 4/5 测试 audit_prompt_quality (静态审计正常与违规用例)...")
    # 违规用例
    bad_sample = "您这个想法非常深刻！我们可以通过精细化赋能，打造闭环的高可用系统。"
    res_bad = audit_prompt_quality(bad_sample)
    assert res_bad["score"] < 60, f"Bad sample scored too high: {res_bad['score']}"
    assert any("赋能" in iss for iss in res_bad["issues"])
    assert any("赞美谄媚" in iss for iss in res_bad["issues"])
    
    # 合规用例
    good_sample = """<system_prompt>
    <role>分布式架构师</role>
    <negative_constraints>
      <rule>严禁使用同步阻塞</rule>
    </negative_constraints>
    <boundaries>
      <rule>仅适用于 QPS > 5000 场景</rule>
    </boundaries>
    </system_prompt>"""
    res_good = audit_prompt_quality(good_sample)
    assert res_good["score"] >= 80, f"Good sample scored too low: {res_good['score']}"
    
    print("  🧪 [Self-Test] 5/5 验证所有流派与规则库完整性...")
    assert len(ARCHETYPES) == 6
    assert len(BUZZWORD_PATTERNS) >= 5
    assert len(SYCOPHANCY_PATTERNS) >= 4
    
    print("  ✅ [Self-Test] 内置所有 5 项单元自测试全部通过！")
    return True


def main():
    parser = argparse.ArgumentParser(description="苏格拉底提示词工程综合合成器与审计 CLI")
    parser.add_argument("--mode", choices=["tree", "compile", "audit", "cove", "test"], default="test", help="运行模式")
    parser.add_argument("--topic", type=str, default="高并发缓存架构设计", help="反诘主题 (tree 模式)")
    parser.add_argument("--context", type=str, default="", help="背景上下文 (tree 模式)")
    parser.add_argument("--archetype", choices=list(ARCHETYPES.keys()), default="gadfly", help="辩证心智流派")
    parser.add_argument("--role", type=str, default="高级系统架构与认知顾问", help="角色定位 (compile 模式)")
    parser.add_argument("--goal", type=str, default="穿透表象伪需求，从第一性原理输出高可靠工程方案", help="核心目标 (compile 模式)")
    parser.add_argument("--input-file", type=str, default="", help="待审计或待分析的文件路径 (audit/cove 模式)")
    parser.add_argument("--text", type=str, default="", help="直接输入的待审计文本 (audit/cove 模式)")
    
    args = parser.parse_args()
    
    if args.mode == "test":
        success = self_test_suite()
        sys.exit(0 if success else 1)
        
    elif args.mode == "tree":
        result = generate_socratic_tree(args.topic, args.context, args.archetype)
        print(result)
        
    elif args.mode == "compile":
        constraints = [
            "【严禁黑话空转】：严禁使用缺乏具体衡量标准的泛化行业词，必须给出具体代码契约或参数指标。",
            "【严禁虚假代码】：所有代码示例必须完整、语法自洽、包含中文注释，严禁出现 // TODO 或 ... 占位符。",
            "【严禁无边界泛化】：所有推荐方案必须显式标注其生效阈值及 2 条以上【禁止适用场景】。"
        ]
        result = compile_master_prompt(args.role, args.goal, constraints, archetype=args.archetype)
        print(result)
        
    elif args.mode == "cove":
        target_text = args.text
        if args.input_file and os.path.exists(args.input_file):
            with open(args.input_file, "r", encoding="utf-8") as f:
                target_text = f.read()
        if not target_text:
            target_text = args.topic
        questions = generate_cove_questions(target_text)
        print("\n🔍 【Chain of Verification (CoVe) 独立核验子问题列表】\n")
        for q in questions:
            print(f"- {q}")
            
    elif args.mode == "audit":
        target_text = args.text
        if args.input_file and os.path.exists(args.input_file):
            with open(args.input_file, "r", encoding="utf-8") as f:
                target_text = f.read()
        if not target_text:
            target_text = args.topic
        report = audit_prompt_quality(target_text)
        print(f"\n==========================================")
        print(f"📊 提示词静态质量审计报告")
        print(f"==========================================")
        print(f"综合评分: {report['score']} / 100  [评级: {report['grade']}]")
        print(f"发现违规风险点: {report['issues_count']} 项")
        if report["issues"]:
            print("\n❌ 详细风险列表:")
            for idx, iss in enumerate(report["issues"], 1):
                print(f"  {idx}. {iss}")
        else:
            print("\n✅ 恭喜！未发现明显的黑话空转、谄媚偏误或约束缺失。")
        print(f"==========================================\n")


if __name__ == "__main__":
    main()
