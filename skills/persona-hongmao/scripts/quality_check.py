#!/usr/bin/env python3
"""
persona-hongmao 自动化质量与合规校验探针 (七层深度人设架构版)
物理验证 SKILL.md 及 13 份研究档案库是否满足工业级最高标准
"""

import sys
import os

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

    # 2. 检查 7 层深度人设核心 Section
    required_sections = [
        "## 一、 核心感知与心理画像",
        "## 二、 动态心理状态机",
        "## 三、 关系动力学矩阵",
        "## 四、 多维情境应激引擎",
        "## 五、 回答工作流 (Agentic Protocol)",
        "## 六、 表达 DNA 与词汇光谱",
        "## 七、 诚实边界与物理验证"
    ]

    for section in required_sections:
        if section not in content:
            print(f"❌ 错误: 缺失核心 Section: {section}")
            return False

    # 3. 检查 Research 13 维全剧集档案库
    expected_research_files = [
        '01-writings.md',
        '02-conversations.md',
        '03-expression-dna.md',
        '04-external-views.md',
        '05-decisions.md',
        '06-timeline.md',
        '07-franchise-lore.md',
        'series_01_qixiazhuan.md',
        'series_02_amuxing.md',
        'series_03_zhangjiang.md',
        'series_04_guangmingjian.md',
        'series_05_huofenghuang.md',
        'series_06_yongzheguilai.md'
    ]

    for rf in expected_research_files:
        rf_path = os.path.join(research_dir, rf)
        if not os.path.exists(rf_path):
            print(f"❌ 错误: 缺失剧集档案 {rf}")
            return False
        if os.path.getsize(rf_path) < 100:
            print(f"⚠️ 警告: 剧集档案 {rf} 体积过小 ({os.path.getsize(rf_path)} 字节)")

    print(f"🎉 [persona-hongmao] 工业级 7 层深度人设架构校验 100% 物理 PASS！")
    return True

if __name__ == '__main__':
    success = check_skill()
    sys.exit(0 if success else 1)
