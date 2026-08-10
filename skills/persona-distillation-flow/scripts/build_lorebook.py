#!/usr/bin/env python3
"""
build_lorebook.py
自动考据抽取与 SillyTavern Character Book (Lorebook) 编译工具
将角色技能中的 references/research 考据自动扫描抽取并编译嵌入 assets/character_card.json 的 character_book 字段中。

使用方式:
    python3 build_lorebook.py <target-skill-dir>

示例:
    python3 skills/persona-distillation-flow/scripts/build_lorebook.py skills/persona-zhangxiaofan
"""

import sys
import os
import json
import re

def parse_lore_file(file_path):
    """解析考据 Markdown 文件，抽取带【专有名词】的条目作为 Lorebook 项"""
    if not os.path.exists(file_path):
        return []

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    entries = []
    current_title = None
    current_text = []

    for line in lines:
        line_str = line.strip()
        # 匹配标题或加粗/方括号名词，如【功法·天书】或 - **噬魂法宝**
        m = re.search(r'【([^】]+)】|\*\*([^*]+)\*\*', line_str)
        if m:
            keyword = m.group(1) or m.group(2)
            if keyword and len(keyword) > 1:
                # 抽取纯名称作为触发 key
                clean_key = re.sub(r'^(法宝|功法|门派|人物|地点|绝学)·', '', keyword).strip()
                if current_title and current_text:
                    entries.append({
                        "keys": [clean_key],
                        "content": " ".join(current_text),
                        "enabled": True,
                        "insertion_order": 100
                    })
                current_title = clean_key
                current_text = [line_str]
        elif current_title and line_str and not line_str.startswith('#'):
            current_text.append(line_str)

    if current_title and current_text:
        clean_key = re.sub(r'^(法宝|功法|门派|人物|地点|绝学)·', '', current_title).strip()
        entries.append({
            "keys": [clean_key],
            "content": " ".join(current_text),
            "enabled": True,
            "insertion_order": 100
        })

    return entries

def main():
    if len(sys.argv) < 2:
        print("用法: python3 build_lorebook.py <target-skill-dir>")
        sys.exit(1)

    skill_dir = os.path.abspath(sys.argv[1])
    card_path = os.path.join(skill_dir, "assets/character_card.json")
    research_dir = os.path.join(skill_dir, "references/research")

    if not os.path.exists(card_path):
        print(f"❌ 错误: 未找到角色卡 {card_path}")
        sys.exit(1)

    print(f"🔍 正在为 {skill_dir} 扫描考据库并编译 Lorebook...")

    all_entries = []
    if os.path.exists(research_dir):
        for rf in sorted(os.listdir(research_dir)):
            if rf.endswith('.md'):
                rf_path = os.path.join(research_dir, rf)
                entries = parse_lore_file(rf_path)
                all_entries.extend(entries)

    print(f"📚 提取到 {len(all_entries)} 条 Lorebook 键值条目。")

    # 读取原有 character_card.json
    with open(card_path, 'r', encoding='utf-8') as f:
        card_data = json.load(f)

    # 兼容 chara_card_v2 数据结构
    if "data" in card_data:
        target_obj = card_data["data"]
    else:
        target_obj = card_data

    target_obj["character_book"] = {
        "name": f"{target_obj.get('name', 'Persona')} Lorebook",
        "description": "由女娲 · Skill造人术 (persona-distillation-flow) 编译的考据键值触发图谱",
        "entries": all_entries
    }

    # 写入更新
    with open(card_path, 'w', encoding='utf-8') as f:
        json.dump(card_data, f, ensure_ascii=False, indent=2)

    print(f"🎉 成功将 {len(all_entries)} 条 Lorebook 编译嵌入至 {card_path}！")

if __name__ == '__main__':
    main()
