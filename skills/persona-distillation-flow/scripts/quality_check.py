#!/usr/bin/env python3
"""
persona-distillation-flow 自动化质量与合规校验探针
用于物理验证 persona-distillation-flow SKILL.md 是否符合标准
"""

import sys
import os

def check_skill():
    skill_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../SKILL.md'))

    print(f"🔍 检查目标: {skill_path}")

    if not os.path.exists(skill_path):
        print(f"❌ 错误: {skill_path} 不存在")
        return False

    with open(skill_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 检查 YAML Frontmatter
    if not content.startswith('---'):
        print("❌ 错误: 缺失 YAML Frontmatter")
        return False

    # 2. 检查必须的核心 Section
    required_sections = [
        "## 🛠️ 一键脚手架工具 (CLI Scaffolder)",
        "## 📋 5 步极尽蒸馏标准 Sop",
        "## 🎯 蒸馏防 OOC 红线 (Guardrails)"
    ]

    for section in required_sections:
        if section not in content:
            print(f"❌ 错误: 缺失核心 Section: {section}")
            return False

    print(f"🎉 [persona-distillation-flow] SOP 工作流合规校验 100% 物理 PASS！")
    return True

if __name__ == '__main__':
    success = check_skill()
    sys.exit(0 if success else 1)
