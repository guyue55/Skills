#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
苏格拉底提示词大师 Skill 质量检查探针脚本 (quality_check.py)

功能说明：
1. 校验 SKILL.md 的存在性、Frontmatter 规范及 7 层认知架构完备性。
2. 校验 references/ 核心知识库与 assets/ 模板的完整性。
3. 检查代码及文档中是否包含绝对路径泄露或未完成占位任务标记 (TODO:, FIXME:)。
4. 运行 prompt_synthesizer.py 的自检逻辑，实现全流程物理测试闭环。
"""

import os
import sys
import re
from pathlib import Path

# 获取当前技能根目录 (使用相对动态路径，严禁硬编码绝对路径)
SKILL_ROOT = Path(__file__).resolve().parent.parent

# 必须存在的关键文件清单
REQUIRED_FILES = [
    "SKILL.md",
    "references/socratic-5-dimensions.md",
    "references/sota-prompt-frameworks.md",
    "references/anti-sycophancy-guide.md",
    "assets/templates/master_system_prompt_template.md",
    "assets/templates/socratic_interrogation_tree.md",
    "scripts/quality_check.py",
    "scripts/prompt_synthesizer.py",
]

# SKILL.md 必须包含的 7 层核心章节标题或关键字
REQUIRED_SECTIONS = [
    "核心感知与心智画像",
    "动态心智状态机",
    "关系动力学与咨询矩阵",
    "多维情境应激引擎",
    "详细工作流与实战 SOP",
    "表达 DNA 与词汇光谱",
    "红线与禁忌",
    "示例与实战对照",
    "诚实边界与物理验证",
]

def check_required_files():
    """检查必要文件与引用资产是否存在"""
    print("🔍 [1/4] 检查必要文件与知识库引用完整性...")
    missing_files = []
    for rel_path in REQUIRED_FILES:
        target = SKILL_ROOT / rel_path
        if not target.exists():
            missing_files.append(rel_path)
    
    if missing_files:
        print(f"❌ 缺少以下必要文件: {missing_files}")
        return False
    print("✅ 所有必要文件与知识库引用均完整存在。")
    return True

def check_skill_markdown():
    """检查 SKILL.md 的 Frontmatter 与章节完整性"""
    print("🔍 [2/4] 校验 SKILL.md 结构与 Frontmatter 规范...")
    skill_file = SKILL_ROOT / "SKILL.md"
    content = skill_file.read_text(encoding="utf-8")
    
    # 1. 检查 Frontmatter
    frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not frontmatter_match:
        print("❌ SKILL.md 缺少有效的 YAML Frontmatter 头部！")
        return False
    
    fm_text = frontmatter_match.group(1)
    if 'name: "topic-socratic-prompt-master"' not in fm_text and "name: 'topic-socratic-prompt-master'" not in fm_text and "name: topic-socratic-prompt-master" not in fm_text:
        print("❌ Frontmatter 中的 name 字段与技能目录名称不匹配！")
        return False
    
    if "description:" not in fm_text:
        print("❌ Frontmatter 缺少 description 描述字段！")
        return False

    # 2. 检查 7 层架构章节
    missing_sections = []
    for sec in REQUIRED_SECTIONS:
        if sec not in content:
            missing_sections.append(sec)
            
    if missing_sections:
        print(f"❌ SKILL.md 缺少以下关键章节: {missing_sections}")
        return False

    print("✅ SKILL.md 结构与 7 层架构校验 100% 合规。")
    return True

def check_forbidden_patterns():
    """检查全目录是否包含硬编码绝对路径、未完成占位任务等违规内容"""
    print("🔍 [3/4] 扫描潜在硬编码绝对路径与未完成占位任务标记...")
    forbidden_patterns = [
        (re.compile(r"/Users/[a-zA-Z0-9_-]+/"), "硬编码 macOS 用户主目录路径"),
        (re.compile(r"/home/[a-zA-Z0-9_-]+/"), "硬编码 Linux 用户主目录路径"),
        (re.compile(r"TO" + r"DO:"), "未完成任务标记 (TO" + "DO:)"),
        (re.compile(r"FIX" + r"ME:"), "未完成修复标记 (FIX" + "ME:)"),
    ]
    
    violations = []
    for root, _, files in os.walk(SKILL_ROOT):
        for file in files:
            # 排除自检脚本自身，避免规则描述误匹配
            if file == "quality_check.py":
                continue
            # 仅扫描文本与脚本文件
            if file.endswith((".md", ".py", ".sh", ".json", ".yaml", ".yml")):
                file_path = Path(root) / file
                try:
                    text = file_path.read_text(encoding="utf-8")
                    for pattern, desc in forbidden_patterns:
                        if pattern.search(text):
                            violations.append(f"{file_path.relative_to(SKILL_ROOT)} -> 包含 {desc}")
                except Exception as err:
                    print(f"⚠️ 读取文件 {file_path} 异常: {err}")
    
    if violations:
        print(f"❌ 发现违规内容:\n" + "\n".join(violations))
        return False
    
    print("✅ 环境脱敏与防偷懒扫描全部通过，无硬编码路径与未完成标记。")
    return True

def run_synthesizer_self_test():
    """执行 prompt_synthesizer.py 自检测试"""
    print("🔍 [4/4] 物理执行 prompt_synthesizer.py 功能自测...")
    try:
        from prompt_synthesizer import self_test_suite
        success = self_test_suite()
        if not success:
            print("❌ prompt_synthesizer 自测试套件执行失败！")
            return False
    except Exception as err:
        print(f"❌ 运行 prompt_synthesizer 测试时发生异常: {err}")
        return False
    
    print("✅ prompt_synthesizer 功能物理测试 100% 通过。")
    return True

def main():
    """主执行入口"""
    print("==================================================")
    print("🚀 启动 topic-socratic-prompt-master 物理质量校验")
    print("==================================================")
    
    step1 = check_required_files()
    step2 = check_skill_markdown()
    step3 = check_forbidden_patterns()
    step4 = run_synthesizer_self_test()
    
    print("==================================================")
    if step1 and step2 and step3 and step4:
        print("🎉 恭喜！topic-socratic-prompt-master 技能物理校验全部通过！")
        return 0
    else:
        print("❌ 校验未全部通过，请根据上方日志进行修复。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
