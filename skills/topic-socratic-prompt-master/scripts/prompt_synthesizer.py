#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
苏格拉底提示词生成与深度反诘辅助引擎 (prompt_synthesizer.py)

功能说明：
1. 【反诘追问生成】：根据用户给出的 AI 初始回答或核心议题，自动生成五维苏格拉底追问树（问定义/问假设/问依据/问反例/问边界）。
2. 【黄金 Prompt 编译】：将结构化业务意图编译为符合现代前沿 LLM 规范的标准 XML Master System Prompt。
3. 【Prompt 质量体检】：静态审计提示词中是否存在抽象黑话、缺少负向约束、缺乏格式契约等典型漏洞。
4. 【内置物理自测套件】：支持 --test 模式进行全功能自动化单元验证。
"""

import argparse
import json
import re
import sys
from typing import Dict, List, Optional

# 常见模糊泛化黑话与动词词库（用于提示词质量静态审计）
VAGUE_BUZZWORDS = [
    "赋能", "闭环", "抓手", "矩阵", "颗粒度", "底层逻辑", "顶层设计",
    "打通", "拉通", "对齐", "串联", "沉淀", "聚焦", "解耦", "组合拳",
    "深入浅出", "合理优化", "妥善处理", "有效提升", "高质量", "全方位"
]

def generate_socratic_tree(
    topic: str,
    ai_output: Optional[str] = None,
    abstract_terms: Optional[List[str]] = None,
    assumptions: Optional[List[str]] = None,
    edge_cases: Optional[List[str]] = None
) -> str:
    """
    生成针对特定议题或 AI 回答的苏格拉底五维深度追问树。

    :param topic: 核心议题或分析对象 (例如: "茶饮行业健康化趋势分析")
    :param ai_output: AI 的第一轮回答摘要 (可选)
    :param abstract_terms: 需要拆解的抽象黑话/概念列表 (可选)
    :param assumptions: 待暴露的隐含假设列表 (可选)
    :param edge_cases: 待验证的边缘反例场景 (可选)
    :return: 格式化的 Markdown 追问决策树文本
    """
    terms_str = "、".join(abstract_terms) if abstract_terms else "核心定义与关键术语"
    assump_str = "、".join(assumptions) if assumptions else "结论依赖的底层未声明假设"
    edge_str = "、".join(edge_cases) if edge_cases else "极端负载、小样本或逆向竞争环境"

    lines = [
        f"# 针对「{topic}」的苏格拉底五维深度反诘决策树",
        "",
        "> [!IMPORTANT]",
        "> 本反诘树基于苏格拉底精神助产术，用于破除未验证假设与模型讨好偏误，逼近第一性物理真值。",
        ""
    ]

    if ai_output:
        lines.extend([
            "## 📌 AI 首轮回答要点回顾",
            f"```text\n{ai_output.strip()}\n```",
            ""
        ])

    lines.extend([
        "## 🧭 五维深度追问清单 (Copy & Send to AI)",
        "",
        "### 1. 【问定义 · 概念去蔽与操作化】",
        f"- 在当前论断中，关于「**{terms_str}**」的最严格操作性定义是什么？",
        "- 请将其拆解为至少 3 个客观可观测、可量化落地的判定指标。",
        "",
        "### 2. 【问假设 · 暴露隐藏支柱】",
        f"- 你的结论建立在哪些未经显式声明的关键前置假设（如「**{assump_str}**」）之上？",
        "- 如果其中最关键的 1 个假设被推翻或发生逆转，整套推论会出现哪些结构性崩溃？",
        "",
        "### 3. 【问依据 · 事实与推论物理隔离】",
        "- 请将你输出中的所有陈述制作成一张对比表格，严格区分为两类：",
        "  - **【确凿事实栏】**：具备明确权威数据源、第三方审计报告或同行评审支持的论据（须注明出处口径）。",
        "  - **【外推推测栏】**：基于常识推理或逻辑演进的主观判断（须注明推导逻辑链）。",
        "",
        "### 4. 【问反例 · 魔鬼代言人证伪】",
        f"- 请作为反方最严厉的行业批判者，在「**{edge_str}**」等极端场景下寻找 2 个彻底推翻你方案的典型反例。",
        "- 在行业历史上，是否存在满足你给出的所有成功条件但最终仍遭遇惨败的案例？其致命死因是什么？",
        "",
        "### 5. 【问边界 · 适用范围与禁忌清单】",
        "- 该方案的有效性受限于哪些具体边界条件（团队规模、预算下限、技术成熟度、业务生命周期）？",
        "- 请明确列出 3 条【绝对禁止适用本方案的反模式场景清单 (Anti-Patterns)】。"
    ])

    return "\n".join(lines)

def compile_master_prompt(
    role_title: str,
    domain_desc: str,
    goal: str,
    workflow_steps: Optional[List[str]] = None,
    negative_constraints: Optional[List[str]] = None
) -> str:
    """
    将业务意图编译为符合现代前沿 LLM 规范的标准 XML Master System Prompt。

    :param role_title: 角色名称 (例如: "资深分布式系统架构师")
    :param domain_desc: 领域背景描述
    :param goal: 第一性原则核心目标
    :param workflow_steps: 操作步骤列表 (可选)
    :param negative_constraints: 负向约束与红线规则 (可选)
    :return: 编译后的 XML 提示词字符串
    """
    if not workflow_steps:
        workflow_steps = [
            "概念解构与前提审查：拆解用户输入，指出任何未验证的脆弱假设。",
            "多维推演与反例压力测试：结合第一性原理推演核心方案，主动寻找破绽。",
            "方案结构化输出与边界标定：交付高质量方案并明确适用阈值与禁忌清单。"
        ]

    if not negative_constraints:
        negative_constraints = [
            "严禁使用泛化空洞的行业黑话，所有动作必须具有可操作性与衡量标准。",
            "严禁盲目迎合用户的错误预设；若用户输入包含逻辑漏洞，须在首段明确警示。",
            "严格区分【确凿事实】与【推论推测】，禁止编造不存在的数据源或指标。"
        ]

    steps_xml = "\n".join([
        f'    <step index="{idx + 1}">{step}</step>'
        for idx, step in enumerate(workflow_steps)
    ])

    constraints_xml = "\n".join([
        f'    <rule index="{idx + 1}">{rule}</rule>'
        for idx, rule in enumerate(negative_constraints)
    ])

    prompt_xml = f"""<system_prompt>
  <role_definition>
    <title>{role_title}</title>
    <profile>
      你是一位顶级{role_title}。你秉持苏格拉底式的严谨思辨与第一性原理，拒绝表面文章与伪逻辑。你的核心职责是通过精准概念界定、深层逻辑推演与严密边界约束，协助用户完成最高水准的任务交付。
    </profile>
    <tone_and_style>
      客观、专业、冷峻、高密度、直击本质，杜绝虚假客套与讨好偏误。
    </tone_and_style>
  </role_definition>

  <context_and_intent>
    <domain_background>
      {domain_desc}
    </domain_background>
    <first_principles_goal>
      {goal}
    </first_principles_goal>
  </context_and_intent>

  <execution_workflow>
{steps_xml}
  </execution_workflow>

  <negative_constraints>
{constraints_xml}
  </negative_constraints>

  <input_schema>
    {{{{USER_INPUT}}}}
  </input_schema>

  <output_contract>
    输出必须遵循以下结构：
    ## 一、 概念解构与前置假设风险审查
    ## 二、 核心方案与第一性原理推演
    ## 三、 魔鬼代言人：反例与压力测试
    ## 四、 适用边界与禁止适用场景清单 (Anti-Patterns)
  </output_contract>
</system_prompt>"""

    return prompt_xml

def audit_prompt_quality(prompt_text: str) -> Dict[str, any]:
    """
    静态审计提示词文本的质量，检查潜在的黑话空洞、缺少约束或缺乏结构等问题。

    :param prompt_text: 待检测的提示词文本
    :return: 包含评分、问题列表及优化建议的审计字典
    """
    issues = []
    score = 100

    # 1. 检测模糊黑话
    found_buzzwords = [bw for bw in VAGUE_BUZZWORDS if bw in prompt_text]
    if found_buzzwords:
        issues.append(f"发现模糊黑话/泛化词: {', '.join(found_buzzwords)} (建议替换为具体操作指标)")
        score -= min(30, len(found_buzzwords) * 5)

    # 2. 检测结构化标签 (XML / Markdown)
    has_xml = bool(re.search(r"<[a-zA-Z_]+>.*?</[a-zA-Z_]+>", prompt_text, re.DOTALL))
    has_markdown_headers = bool(re.search(r"^#{1,4}\s+", prompt_text, re.MULTILINE))
    if not has_xml and not has_markdown_headers:
        issues.append("缺少清晰的层级结构（建议采用 XML 标签或规范 Markdown 标题）")
        score -= 20

    # 3. 检测是否包含负向约束 (Negative Constraints / 红线)
    has_negative_rules = any(kw in prompt_text for kw in ["严禁", "禁止", "不能", "避免", "negative", "forbidden", "constraints"])
    if not has_negative_rules:
        issues.append("未发现负向约束与红线规则（大模型容易失控泛滥，建议补充严禁事项）")
        score -= 20

    # 4. 检测是否包含输出格式契约 (Output Contract)
    has_output_contract = any(kw in prompt_text for kw in ["输出格式", "output", "契约", "schema", "JSON", "Markdown"])
    if not has_output_contract:
        issues.append("未显式定义输出格式契约（可能导致模型返回随意格式）")
        score -= 15

    # 5. 检测字数与信息密度
    if len(prompt_text.strip()) < 50:
        issues.append("提示词长度过短（不足 50 字），缺乏必要的上下文与推理引导")
        score -= 20

    score = max(0, score)
    return {
        "score": score,
        "is_healthy": score >= 80,
        "issues": issues,
        "summary": "优秀" if score >= 85 else ("良好" if score >= 70 else "亟需优化")
    }

def self_test_suite() -> bool:
    """
    运行完整的内置单元自测逻辑，确保所有核心函数正常运行且输出合规。
    """
    print("  🧪 [Self-Test] 测试 generate_socratic_tree 生成逻辑...")
    tree = generate_socratic_tree(
        topic="企业 AI 转型战略",
        ai_output="建议全面引入大模型自动化客服与代码助手，实现降本增效。",
        abstract_terms=["降本增效", "全场景覆盖"],
        assumptions=["员工能迅速无缝适应 AI 工作流", "数据质量与安全性已就绪"],
        edge_cases=["网络离线环境", "高合规金融审计场景"]
    )
    assert "五维深度追问清单" in tree, "反诘树标题缺失"
    assert "问定义" in tree and "问假设" in tree and "问依据" in tree, "五维维度缺失"
    assert "企业 AI 转型战略" in tree, "主题内容未注入"

    print("  🧪 [Self-Test] 测试 compile_master_prompt XML 编译逻辑...")
    compiled = compile_master_prompt(
        role_title="数据安全合规审计师",
        domain_desc="跨境电商数据传输与隐私合规场景",
        goal="评估并输出零疏漏的数据安全风险评估报告"
    )
    assert "<system_prompt>" in compiled and "</system_prompt>" in compiled, "XML 根节点缺失"
    assert "<negative_constraints>" in compiled, "负向约束节点缺失"
    assert "数据安全合规审计师" in compiled, "角色名称未正确注入"

    print("  🧪 [Self-Test] 测试 audit_prompt_quality 静态审计逻辑...")
    bad_prompt = "帮我合理优化一下代码，深度赋能业务，打通底层逻辑。"
    bad_report = audit_prompt_quality(bad_prompt)
    assert bad_report["score"] < 70, "劣质 Prompt 评分未按预期扣分"
    assert len(bad_report["issues"]) > 0, "未能检出黑话与结构问题"

    good_prompt = compiled
    good_report = audit_prompt_quality(good_prompt)
    assert good_report["score"] >= 80, f"编译生成的标准 Prompt 未达到优秀标准: {good_report}"

    print("  ✅ [Self-Test] 内置所有单元自测全部通过！")
    return True

def main():
    """CLI 命令行交互主逻辑"""
    parser = argparse.ArgumentParser(
        description="苏格拉底提示词生成与深度反诘辅助引擎 (prompt_synthesizer.py)"
    )
    parser.add_argument(
        "--mode",
        choices=["tree", "compile", "audit", "test"],
        default="test",
        help="执行模式: tree (生成反诘树), compile (编译系统提示词), audit (审计提示词), test (运行自测)"
    )
    parser.add_argument("--topic", type=str, default="通用议题分析", help="议题主题或任务目标")
    parser.add_argument("--role", type=str, default="领域专家", help="角色名称 (用于 compile 模式)")
    parser.add_argument("--domain", type=str, default="业务与技术决策", help="领域背景 (用于 compile 模式)")
    parser.add_argument("--prompt", type=str, default="", help="待审计提示词文本或文件路径 (用于 audit 模式)")

    args = parser.parse_args()

    if args.mode == "test":
        success = self_test_suite()
        sys.exit(0 if success else 1)
    elif args.mode == "tree":
        res = generate_socratic_tree(topic=args.topic)
        print(res)
    elif args.mode == "compile":
        res = compile_master_prompt(
            role_title=args.role,
            domain_desc=args.domain,
            goal=args.topic
        )
        print(res)
    elif args.mode == "audit":
        content = args.prompt
        if not content:
            print("❌ 请使用 --prompt 参数提供待审计的提示词文本。")
            sys.exit(1)
        report = audit_prompt_quality(content)
        print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
