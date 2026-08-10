#!/usr/bin/env python3
"""
Skill 合规性校验脚本

校验内容:
1. skills/ 下各目录必须包含 SKILL.md
2. SKILL.md 必须包含标准的 YAML Frontmatter 元数据 (--- 包包裹)
3. Frontmatter 必须包含 name 与 description 字段
4. name 必须与所在的文件夹名称完全一致
"""

import sys
from pathlib import Path


def parse_frontmatter(content: str) -> dict:
    """简单解析 Markdown 的 YAML Frontmatter Header"""
    lines = content.strip().splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    frontmatter = {}
    end_idx = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break

    if end_idx == -1:
        return {}

    for line in lines[1:end_idx]:
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip('"\'')
            frontmatter[key] = val

    return frontmatter


def validate_skills() -> bool:
    repo_root = Path(__file__).resolve().parent.parent
    skills_dir = repo_root / "skills"

    if not skills_dir.exists():
        print("⚠️  警告: skills 目录不存在！")
        return True

    skill_folders = [p for p in skills_dir.iterdir() if p.is_dir() and not p.name.startswith(".")]

    if not skill_folders:
        print("ℹ️  skills 目录下当前没有 Skill 模块。")
        return True

    has_error = False
    print(f"🔍 检查 {len(skill_folders)} 个 Skill 模块...\n")

    for folder in sorted(skill_folders, key=lambda x: x.name):
        skill_file = folder / "SKILL.md"
        folder_name = folder.name

        if not skill_file.exists():
            print(f"❌ [{folder_name}] 缺失 SKILL.md 文件")
            has_error = True
            continue

        try:
            content = skill_file.read_text(encoding="utf-8")
            metadata = parse_frontmatter(content)

            if not metadata:
                print(f"❌ [{folder_name}] SKILL.md 格式错误: 缺少或格式不正确的 YAML Frontmatter (需用 --- 包裹)")
                has_error = True
                continue

            name = metadata.get("name")
            desc = metadata.get("description")

            if not name:
                print(f"❌ [{folder_name}] YAML Frontmatter 缺失 'name' 字段")
                has_error = True
            elif name != folder_name:
                print(f"❌ [{folder_name}] 'name' 字段 ({name}) 与文件夹名称 ({folder_name}) 不一致")
                has_error = True

            if not desc:
                print(f"❌ [{folder_name}] YAML Frontmatter 缺失 'description' 字段")
                has_error = True

            if name and desc and name == folder_name:
                print(f"✅ [{folder_name}] 校验通过")

        except Exception as e:
            print(f"❌ [{folder_name}] 读取或解析失败: {e}")
            has_error = True

    print("\n" + ("=" * 40))
    if has_error:
        print("❌ Skill 校验未通过，请根据提示修复错误。")
        return False
    else:
        print("🎉 所有 Skill 模块校验通过！")
        return True


def main():
    success = validate_skills()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
