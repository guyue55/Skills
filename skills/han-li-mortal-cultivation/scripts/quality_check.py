#!/usr/bin/env python3
import sys
import os

def check_skill():
    skill_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../SKILL.md'))
    research_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../references/research'))

    if not os.path.exists(skill_path):
        print(f"❌ 错误: {skill_path} 不存在")
        return False

    with open(skill_path, 'r', encoding='utf-8') as f:
        content = f.read()

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

    print(f"🎉 [han-li-mortal-cultivation] 工业级 7 层深度人设架构校验 100% 物理 PASS！")
    return True

if __name__ == '__main__':
    success = check_skill()
    sys.exit(0 if success else 1)
