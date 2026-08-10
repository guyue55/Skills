#!/usr/bin/env python3
"""
Skill 合规性校验脚本

校验内容:
1. skills/ 下各目录必须包含 SKILL.md
2. SKILL.md 必须包含标准的 YAML Frontmatter 元数据 (--- 包包裹)
3. Frontmatter 必须包含 name 与 description 字段
4. name 必须与所在的文件夹名称完全一致
"""

import re
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

    current_key = None
    for line in lines[1:end_idx]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" in line and not line.startswith(" ") and not line.startswith("\t"):
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip('"\'')
            frontmatter[key] = val
            current_key = key
        elif current_key and (line.startswith(" ") or line.startswith("\t")):
            frontmatter[current_key] += " " + stripped.strip('"\'')

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

        # skill-creator 规范: 单个 Skill 目录下不应包含 README.md 等冗余文档（以 SKILL.md 为唯一入口）
        if (folder / "README.md").exists():
            print(f"⚠️  [{folder_name}] 提示: 根据 skill-creator 规范，子 Skill 目录下不应包含 README.md，所有导引请整合至 SKILL.md 中。")

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

            # 绝对路径检查 (De-hardcoding / Zero-Leakage)
            if "/Users/" in content or "/home/" in content:
                print(f"⚠️  [{folder_name}] 警告: 发现可能硬编码的绝对个人路径 (/Users/ 或 /home/)，请使用相对路径或环境变量。")

            # 敏感密钥与隐私信息防护检查 (Sensitive Credentials & Secrets Scanner)
            sensitive_patterns = [
                (r"sk-[a-zA-Z0-9_-]{20,}", "OpenAI/Anthropic API Key"),
                (r"AIzaSy[a-zA-Z0-9_-]{33}", "Google API Key"),
                (r"ghp_[a-zA-Z0-9]{36}", "GitHub Personal Access Token"),
                (r"-----BEGIN (RSA|EC|OPENSSH|PRIVATE) KEY-----", "Private Key 密钥"),
            ]
            for pattern, pattern_name in sensitive_patterns:
                if re.search(pattern, content):
                    print(f"❌ [{folder_name}] 敏感信息红线拦截: 发现明文敏感凭据 ({pattern_name})，绝对禁止提交！")
                    has_error = True

            # AI 占位符与懒惰词检查
            if "TODO:" in content or "FIXME:" in content:
                print(f"⚠️  [{folder_name}] 提示: 包含 TODO/FIXME 未完成项，建议完善后再提交。")

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
