#!/usr/bin/env python3
"""
persona-hongmao 自动化质量与合规校验探针
用于物理验证 persona-hongmao SKILL.md 是否满足女娲深度档标准
"""

import sys
import os
import re

def check_skill():
    skill_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../SKILL.md'))
    research_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../references/research'))

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
        "## 触发条件与使用时机",
        "## 回答工作流 (Agentic Protocol)",
        "## 核心心智模型",
        "## 表达 DNA 与角色扮演规范",
        "## 内在张力与性格盲点",
        "## 红线与禁忌",
        "## 诚实边界与深度档验证"
    ]

    for section in required_sections:
        if section not in content:
            print(f"❌ 错误: 缺失核心 Section: {section}")
            return False

    # 3. 检查 Research 6维档案库
    expected_research_files = [
        '01-writings.md',
        '02-conversations.md',
        '03-expression-dna.md',
        '04-external-views.md',
        '05-decisions.md',
        '06-timeline.md',
        '07-franchise-lore.md'
    ]

    for rf in expected_research_files:
        rf_path = os.path.join(research_dir, rf)
        if not os.path.exists(rf_path):
            print(f"❌ 错误: 缺失调研文件 {rf}")
            return False
        if os.path.getsize(rf_path) < 200:
            print(f"⚠️ 警告: 调研文件 {rf} 体积过小 ({os.path.getsize(rf_path)} 字节)")

    print("🎉 [persona-hongmao] 女娲深度档质量与合规校验物理 PASS！")
    return True

if __name__ == '__main__':
    success = check_skill()
    sys.exit(0 if success else 1)
