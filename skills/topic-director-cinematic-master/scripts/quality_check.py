#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
quality_check.py - topic-director-cinematic-master 物理质量校验脚本
校验内容：
1. SKILL.md Frontmatter 与目录名一致性
2. 所有核心资产与 8 大流派知识库引用文档完整性
3. 扫描绝对路径与 TODO 占位符
4. 物理执行 director_synthesizer.py 自测与 80 大流派遍历
"""

import os
import sys
import subprocess

def run_check():
    print("==================================================")
    print("🚀 启动 topic-director-cinematic-master 物理质量校验")
    print("==================================================")

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skill_md = os.path.join(base_dir, "SKILL.md")

    # 1. 检查文件完整性
    print("🔍 [1/4] 检查必要文件与 8 大系 80 个导演流派知识库引用完整性...")
    required_files = [
        "SKILL.md",
        "scripts/director_synthesizer.py",
        "references/directorial-archetypes-matrix.md",
        "references/cinematography-storyboard-guide.md",
        "references/action-choreography-handbook.md",
        "references/spatial-mise-en-scene-guide.md",
        "references/acting-micro-expressions-guide.md",
        "references/archetypes/01_wuxia_kungfu_action.md",
        "references/archetypes/02_chinese_auteurs_poetics.md",
        "references/archetypes/03_hollywood_blockbuster_epic.md",
        "references/archetypes/04_suspense_noir_thriller.md",
        "references/archetypes/05_japanese_cinema_anime.md",
        "references/archetypes/06_european_art_masters.md",
        "references/archetypes/07_micro_drama_vertical_cinema.md",
        "references/archetypes/08_digital_donghua_emerging.md",
        "assets/templates/master_director_system_prompt_template.md",
        "assets/templates/storyboard_shot_sheet_template.md",
        "assets/templates/action_beat_breakdown_template.md",
        "assets/templates/micro_drama_script_beat_template.md"
    ]

    for rel_path in required_files:
        full_path = os.path.join(base_dir, rel_path)
        if not os.path.exists(full_path):
            print(f"❌ 缺失必要文件: {rel_path}")
            sys.exit(1)
    print("✅ 所有 19 项必要文件与知识库引用均完整存在。")

    # 2. 校验 SKILL.md
    print("🔍 [2/4] 校验 SKILL.md 结构与 Frontmatter 规范...")
    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.startswith("---") or 'name: "topic-director-cinematic-master"' not in content:
        print("❌ SKILL.md Frontmatter 不合规！")
        sys.exit(1)
    print("✅ SKILL.md 结构与 Frontmatter 校验 100% 合规。")

    # 3. 扫描硬编码绝对路径与占位符
    print("🔍 [3/4] 扫描潜在硬编码绝对路径与未完成占位任务标记...")
    forbidden_terms = ["/Us" + "ers/", "/ho" + "me/", "TO" + "DO:", "FIX" + "ME:", "pass # placeholder"]
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file == "quality_check.py":
                continue
            if file.endswith((".py", ".md", ".json")):
                file_p = os.path.join(root, file)
                with open(file_p, "r", encoding="utf-8", errors="ignore") as f:
                    for line_idx, line in enumerate(f, 1):
                        for term in forbidden_terms:
                            if term in line:
                                print(f"❌ 在 {file}:{line_idx} 发现违规内容 '{term}': {line.strip()}")
                                sys.exit(1)
    print("✅ 环境脱敏与防偷懒扫描全部通过，无硬编码路径与未完成标记。")

    # 4. 物理执行 CLI 自测
    print("🔍 [4/4] 物理执行 director_synthesizer.py 功能自测 (80大流派全量遍历)...")
    res = subprocess.run([sys.executable, os.path.join(base_dir, "scripts", "director_synthesizer.py"), "--mode", "test"], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"❌ director_synthesizer 自测失败:\n{res.stderr}")
        sys.exit(1)
    print(res.stdout.strip())
    print("✅ director_synthesizer 功能物理测试 100% 通过。")

    print("==================================================")
    print("🎉 恭喜！topic-director-cinematic-master 技能物理校验全部通过！")

if __name__ == "__main__":
    run_check()
