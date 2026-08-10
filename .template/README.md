# Skill 模板说明

本目录包含了新建 Skill 时使用的标准模板。

## 目录文件
- `SKILL.md`: Skill 主定义模板，包含必须的 YAML Frontmatter 元数据区及推荐的内容结构。

## 使用方式
推荐使用根目录下的脚手架工具自动生成：

```bash
python3 scripts/create_skill.py <skill-name> --description "<skill说明>"
```

该工具会自动读取 `.template/SKILL.md` 并替换占位符，在 `skills/<skill-name>/` 目录下生成标准化结构。
