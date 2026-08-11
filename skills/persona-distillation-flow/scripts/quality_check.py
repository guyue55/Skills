#!/usr/bin/env python3
"""
persona-distillation-flow 自动化质量与合规校验探针
物理验证 SKILL.md 是否包含泛领域通用规范 (Universal Special Categories)
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

    # 2. 检查全大系作品树探测、双门禁与 SotA 认知引擎及泛领域章节
    required_sections = [
        "## 🛡️ 前置防幻觉红线：信息源分级与去噪机制 (Information Source Tiering)",
        "## 🔍 前置协议：全大系作品树探测与百科核验 (Franchise Discovery & Baike Pre-Check)",
        "## 🛑 门禁一：三层自适应高密度蒸馏策略简报 (Phase 0: 3-Layer Adaptive Strategy Gate)",
        "## 🔄 核心蒸馏主干",
        "## 🛠️ SotA 四大动态认知加固引擎 (Dynamic Cognitive Engines)",
        "## 🌐 泛领域特殊类别处理规范 (Universal Special Categories)"
    ]

    for section in required_sections:
        if section not in content:
            print(f"❌ 错误: 缺失核心 Section: {section}")
            return False

    print(f"🎉 [persona-distillation-flow] 泛领域通用 SotA 认知操作系统 SOP 校验 100% 物理 PASS！")
    return True

if __name__ == '__main__':
    success = check_skill()
    sys.exit(0 if success else 1)
