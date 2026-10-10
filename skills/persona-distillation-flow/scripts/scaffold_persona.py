#!/usr/bin/env python3
"""
scaffold_persona.py
通用 7 层深度人格 Skill 脚手架工具 (Universal 7-Layer Persona Scaffolder)
完全解耦题材偏见，支持动漫、游戏、影视、历史人物、现实名人、原创 IP、哲学顾问、以及文学作家与专栏创作者。

使用方式:
    ./scripts/scaffold_persona.py <skill-name> -d "<description>" [-c <category>] [--writing-dna]

示例:
    # 普通角色/虚构人物
    ./skills/persona-distillation-flow/scripts/scaffold_persona.py persona-tony-stark -d "钢铁侠 托尼·斯塔克" -c fiction
    
    # 文学作家/创作者 (自动开启 Writing DNA 扩展包)
    ./skills/persona-distillation-flow/scripts/scaffold_persona.py persona-wang-xiaobo -d "作家 王小波" -c author
"""

import sys
import os
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="一键生成通用 7 层深度人格 Skill 脚手架 (支持按需外挂 Writing DNA 写作引擎)")
    parser.add_argument("skill_name", help="Skill 模块名称 (如 persona-tony-stark 或 persona-wang-xiaobo)")
    parser.add_argument("-d", "--description", required=True, help="Skill 简短描述")
    parser.add_argument("-c", "--category", default="general", 
                        choices=["general", "anime", "gaming", "fiction", "history", "real_person", "original_oc", "topic_advisor", "author", "columnist"], 
                        help="角色题材类别")
    parser.add_argument("-w", "--writing-dna", action="store_true", help="显式挂载 Writing DNA 写作工程扩展包 (author/columnist 类别会自动启用)")
    
    args = parser.parse_args()
    skill_name = args.skill_name
    description = args.description
    category = args.category
    enable_writing_dna = args.writing_dna or (category in ["author", "columnist"])

    # 获取 Skills 仓库根目录 (script_dir 在 skills/persona-distillation-flow/scripts/ 下，向三级取根目录)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, "../../../"))
    target_dir = os.path.join(repo_root, "skills", skill_name)

    if os.path.exists(target_dir):
        print(f"❌ 错误: 目标目录 {target_dir} 已存在！")
        sys.exit(1)

    print(f"🚀 正在生成【{category.upper()}】类别通用 7 层深度人格 Skill: {skill_name} ...")
    if enable_writing_dna:
        print(f"✨ 检测到创作者类别/显式参数，已自动装载【Writing DNA 写作工程扩展包】！")

    # 1. 创建子目录
    os.makedirs(os.path.join(target_dir, "scripts"), exist_ok=True)
    os.makedirs(os.path.join(target_dir, "assets"), exist_ok=True)
    os.makedirs(os.path.join(target_dir, "references/research"), exist_ok=True)
    if enable_writing_dna:
        os.makedirs(os.path.join(target_dir, "references/writing-dna"), exist_ok=True)

    # 2. 生成 .gitkeep
    for sub in ["scripts", "assets", "references"]:
        with open(os.path.join(target_dir, sub, ".gitkeep"), "w", encoding="utf-8") as f:
            f.write("")

    # 3. 生成通用 13 维研判档案文件
    research_files = [
        '01-writings-and-speech.md',
        '02-conversations.md',
        '03-expression-dna.md',
        '04-external-views.md',
        '05-decisions.md',
        '06-timeline.md',
        '07-lore-and-world.md',
        'series_01_origin.md',
        'series_02_development.md',
        'series_03_climax.md',
        'series_04_resolution.md',
        'series_05_extended.md',
        'series_06_legacy.md'
    ]

    for rf in research_files:
        rf_path = os.path.join(target_dir, "references/research", rf)
        with open(rf_path, "w", encoding="utf-8") as f:
            f.write(f"# {rf} · {skill_name} 角色深度考据档案\n\n> 预留考据内容... 本档案用于记载 {skill_name} 在 [{category}] 语境下的真实事实、对话与考据。\n")

    # 4. 若启用 Writing DNA，生成特化写作资产模板
    if enable_writing_dna:
        wd_files = {
            "01-language-dna.md": f"# {skill_name} · L1 语言 DNA 刚性量化指标\n\n> 运行 `python3 ./skills/persona-distillation-flow/scripts/analyze_writing_dna.py <语料路径> -o references/writing-dna/01-language-dna.md` 提取。\n",
            "02-structure-patterns.md": f"# {skill_name} · L2 篇章骨架与转折模型\n\n- 开篇 Hook 模型：\n- 叙事推进与冲突加码：\n- 高潮蓄势与反高潮收束模板：\n",
            "03-cognitive-framework.md": f"# {skill_name} · L3-L5 创作哲学与底层世界观约束\n\n- 核心世界观与哲学假说：\n- 价值判断与题材禁忌：\n",
            "04-visual-or-pacing-guide.md": f"# {skill_name} · L6 视觉排版或小说分卷节拍指南\n\n- 长篇小说分卷节拍/短篇自媒体排版层级：\n",
            "Writing-DNA.md": f"# {skill_name} · 写作说明书 (Writing DNA Master Spec)\n\n> 整合 L1-L6 规则集，动笔创作前强制读取；并搭配 3~5 篇相关原著段落进行语感校准。\n"
        }
        for wd_name, wd_text in wd_files.items():
            wd_p = os.path.join(target_dir, "references/writing-dna", wd_name)
            with open(wd_p, "w", encoding="utf-8") as f:
                f.write(wd_text)

    # 5. 生成 SKILL.md 模板 (从 SKILL_template.md 读取或构建)
    template_file = os.path.join(script_dir, "../assets/SKILL_template.md")
    char_displayName = skill_name.replace("persona-", "").replace("-", " ").title()
    if os.path.exists(template_file):
        with open(template_file, "r", encoding="utf-8") as f:
            template_content = f.read()
        
        skill_content = template_content.format(
            SKILL_NAME=skill_name,
            IP_NAME=f"相关作品/背景({category})",
            CHARACTER_TITLE="核心",
            CHARACTER_NAME=char_displayName,
            MOTTO_PRIMARY="核心格言/座右铭 1",
            MOTTO_SECONDARY="核心格言/座右铭 2",
            CORE_DESIRE="追求核心目标与渴望",
            CORE_FEAR="避免最深的恐惧与失控",
            DEFENSE_MECHANISM="典型的心理防御机制与理性掩盖",
            CORE_VALUES="核心价值观优先级排序",
            HIGH_FREQ_TERMS="高频口头禅、专业黑话、特征称呼",
            OOC_FORBIDDEN_TERMS="严重违背背景风格的禁忌词汇"
        )
    else:
        skill_content = f"""---
name: "{skill_name}"
description: "{description}"
---

# {skill_name} · 通用深度角色人格

> [!NOTE]
> 本 Skill 基于**通用七层深度人设工程体系（7-Layer Universal Persona Architecture）**构建。

---

## 一、 核心感知与心理画像 (Core Identity & Psychological Profile)
## 二、 动态心理状态机 (Dynamic State Machine, FSM)
## 三、 关系动力学矩阵 (Relational Dynamics Matrix)
## 四、 多维情境应激引擎 (Multi-Scenario Stress Engine)
## 五、 回答工作流 (Agentic Protocol)
## 六、 表达 DNA 与词汇光谱 (Lexicon & Voice Rules)
## 七、 诚实边界与物理验证 (Honesty & System Verification)
"""

    skill_md_path = os.path.join(target_dir, "SKILL.md")
    with open(skill_md_path, "w", encoding="utf-8") as f:
        f.write(skill_content)

    # 6. 生成 assets/character_card.json (官方 chara_card_v2 2.0 规格)
    card_path = os.path.join(target_dir, "assets/character_card.json")
    card_data = {
        "spec": "chara_card_v2",
        "spec_version": "2.0",
        "data": {
            "name": char_displayName,
            "description": description,
            "personality": f"{char_displayName} 核心性格特征，遵从 7 层深度人设架构。",
            "scenario": f"角色扮演对话、背景({category})决策模拟。",
            "first_mes": f"你好，我是{char_displayName}。",
            "mes_example": f"<START>\n<user>: 你好\n<char>: 你好，我是{char_displayName}，请问有什么可以交流的？",
            "system_prompt": f"你现在扮演{char_displayName}。遵循 7 层深度人设架构，保持性格连贯与表达 DNA。",
            "post_history_instructions": "保持符合角色的动态状态机。",
            "alternate_greetings": [],
            "tags": [category, "deep-persona", "nuwa"] + (["writing-dna", "author"] if enable_writing_dna else []),
            "creator": "女娲 · Skill造人术 (persona-distillation-flow)",
            "character_version": "2.0",
            "creator_notes": "基于工业级 7 层深度人设架构编译。",
            "character_book": None,
            "extensions": {
                "nuwa_version": "7.0-deep-persona",
                "category": category,
                "writing_dna_enabled": enable_writing_dna
            }
        }
    }
    with open(card_path, "w", encoding="utf-8") as f:
        json.dump(card_data, f, ensure_ascii=False, indent=2)

    # 7. 生成 scripts/quality_check.py 校验探针
    qc_path = os.path.join(target_dir, "scripts/quality_check.py")
    qc_content = f"""#!/usr/bin/env python3
import sys
import os

def check_skill():
    skill_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../SKILL.md'))
    research_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../references/research'))

    if not os.path.exists(skill_path):
        print(f"❌ 错误: {{skill_path}} 不存在")
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
            print(f"❌ 错误: 缺失核心 Section: {{section}}")
            return False

    print(f"🎉 [{skill_name}] 工业级 7 层深度人设架构校验 100% 物理 PASS！")
    return True

if __name__ == '__main__':
    success = check_skill()
    sys.exit(0 if success else 1)
"""
    with open(qc_path, "w", encoding="utf-8") as f:
        f.write(qc_content)

    os.chmod(qc_path, 0o755)

    print(f"🎉 成功生成【{category}】通用 7 层深度人格 Skill (chara_card_v2 规格): {target_dir}")
    if enable_writing_dna:
        print(f"📝 写作增强已挂载: {target_dir}/references/writing-dna/")
    print(f"👉 下一步: 结合 research 工具补充 {target_dir}/references/research/ 中的考据，并编辑 SKILL.md 精提炼！")

if __name__ == '__main__':
    main()
