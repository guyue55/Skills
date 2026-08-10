#!/usr/bin/env python3
"""
persona-distillation-flow 自动化质量与合规校验探针
用于物理验证 persona-distillation-flow SKILL.md 是否符合通用 SOP 标准
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

    # 2. 检查通用 4 大核心 Section
    required_sections = [
        "## ⚙️ 一、 核心能力模型 (Core Capabilities)",
        "## 🏗️ 二、 通用七层深度人设结构 (Universal 7-Layer Architecture)",
        "## 📋 三、 标准 5 步蒸馏流程 (Step-by-Step SOP)",
        "## 🎯 四、 蒸馏通用原则与防 OOC 红线 (Universal Principles)"
    ]

    for section in required_sections:
        if section not in content:
            print(f"❌ 错误: 缺失核心 Section: {section}")
            return False

    print(f"🎉 [persona-distillation-flow] 通用 SOP 工作流合规校验 100% 物理 PASS！")
    return True

if __name__ == '__main__':
    success = check_skill()
    sys.exit(0 if success else 1)
