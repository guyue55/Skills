#!/usr/bin/env python3
"""
persona-distillation-flow 自动化质量与合规校验探针
物理验证 SKILL.md 是否包含全大系作品树自动探测协议 (Franchise Discovery Protocol)
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

    # 2. 检查全大系作品树探测与双检查点章节
    required_sections = [
        "## 🔍 前置协议：全大系作品树探测 (Franchise Universe Discovery)",
        "## 🛑 门禁一：全大系蒸馏策略简报 (Phase 0: Research Strategy Gate)",
        "## 🔄 核心蒸馏主干：女娲造人术与双检查点流程",
        "## 📊 检查点二：全大系深度抓取结果报告 (Phase 1.5 Checkpoint)"
    ]

    for section in required_sections:
        if section not in content:
            print(f"❌ 错误: 缺失核心 Section: {section}")
            return False

    print(f"🎉 [persona-distillation-flow] 全大系作品树探测与 SOP 合规校验 100% 物理 PASS！")
    return True

if __name__ == '__main__':
    success = check_skill()
    sys.exit(0 if success else 1)
