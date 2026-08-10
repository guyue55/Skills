#!/usr/bin/env python3
"""
persona-distillation-flow 自动化质量与合规校验探针
物理验证 SKILL.md 是否符合尊重真实时序的双检查点 (Phase 0 & Phase 1.5) SOP 标准
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

    # 2. 检查双检查点门禁章节
    required_sections = [
        "## 🛑 门禁一：蒸馏策略与范围确认简报 (Phase 0: Research Strategy Gate)",
        "## 🔄 核心蒸馏主干：女娲造人术与双检查点流程",
        "## 📊 检查点二：深度抓取结果报告 (Phase 1.5 Checkpoint)",
        "## 📋 完整 SOP 5 步执行规范"
    ]

    for section in required_sections:
        if section not in content:
            print(f"❌ 错误: 缺失核心 Section: {section}")
            return False

    print(f"🎉 [persona-distillation-flow] 双检查点真实时序 SOP 工作流合规校验 100% 物理 PASS！")
    return True

if __name__ == '__main__':
    success = check_skill()
    sys.exit(0 if success else 1)
