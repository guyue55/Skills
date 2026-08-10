#!/usr/bin/env python3
"""
Skill 创建脚手架工具

用法:
    python3 scripts/create_skill.py <skill-name> [--description "说明"] [--title "标题"]

示例:
    python3 scripts/create_skill.py code-refactor-helper --description "用于代码重构与优化的辅助工具"
"""

import argparse
import re
import sys
from pathlib import Path


def validate_skill_name(name: str) -> bool:
    """校验 Skill 名称格式 (只能包含小写字母、数字和连字符)"""
    pattern = r"^[a-z0-9]+(-[a-z0-9]+)*$"
    return bool(re.match(pattern, name))


def create_skill(name: str, description: str = "", title: str = "") -> Path:
    repo_root = Path(__file__).resolve().parent.parent
    template_path = repo_root / ".template" / "SKILL.md"
    target_dir = repo_root / "skills" / name
    target_skill_file = target_dir / "SKILL.md"

    if not validate_skill_name(name):
        print(f"❌ 错误: Skill 名称 '{name}' 不符合规范！")
        print("   必须使用小写英文字母、数字和连字符 (例如: code-reviewer, my-skill-1)")
        sys.exit(1)

    if target_dir.exists():
        print(f"❌ 错误: 目标目录已存在: {target_dir}")
        sys.exit(1)

    if not template_path.exists():
        print(f"❌ 错误: 找不到模板文件: {template_path}")
        sys.exit(1)

    # 默认值设置
    display_title = title if title else name.replace("-", " ").title()
    display_desc = description if description else f"{display_title} skill definition."

    # 读取模版并替换占位符
    template_content = template_path.read_text(encoding="utf-8")
    content = template_content.replace("{{SKILL_NAME}}", name)
    content = content.replace("{{SKILL_DESCRIPTION}}", display_desc)
    content = content.replace("{{SKILL_TITLE}}", display_title)

    # 创建目录结构与 .gitkeep 占位文件
    target_dir.mkdir(parents=True, exist_ok=True)
    for sub_dir in ["scripts", "references", "assets"]:
        d = target_dir / sub_dir
        d.mkdir(exist_ok=True)
        (d / ".gitkeep").touch()

    # 写入 SKILL.md
    target_skill_file.write_text(content, encoding="utf-8")

    print(f"✨ 成功创建 Skill: {name}")
    print(f"📂 目录路径: {target_dir}")
    print(f"📝 配置文件: {target_skill_file}")
    return target_dir


def main():
    parser = argparse.ArgumentParser(description="一键创建标准化 Skill 脚手架工具")
    parser.add_argument("name", help="Skill 名称 (小写字母、数字及连字符，如: my-cool-skill)")
    parser.add_argument("-d", "--description", default="", help="Skill 描述 (用于 YAML frontmatter)")
    parser.add_argument("-t", "--title", default="", help="Skill 显示标题")

    args = parser.parse_args()
    create_skill(args.name, args.description, args.title)


if __name__ == "__main__":
    main()
