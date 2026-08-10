#!/usr/bin/env python3
"""
merge_research.py
自动扫描与汇总 references/research/ 目录下的 13 维考据文件
输出 Phase 1.5 调研 Review 检查点 Markdown 摘要表格
"""

import sys
import os

def merge_research(target_skill_dir):
    research_dir = os.path.join(target_skill_dir, "references/research")
    if not os.path.exists(research_dir):
        print(f"❌ 错误: 考据目录 {research_dir} 不存在")
        return False

    files = [f for f in os.listdir(research_dir) if f.endswith('.md')]
    files.sort()

    print(f"\n📊 [Phase 1.5 Review Checkpoint] 考据文件统计摘要 ({target_skill_dir})")
    print("=" * 60)
    print(f"| 文件名 | 大小 (字节) | 状态 |")
    print("| :--- | :--- | :--- |")

    total_size = 0
    valid_count = 0

    for f in files:
        fpath = os.path.join(research_dir, f)
        size = os.path.getsize(fpath)
        total_size += size
        status = "✅ 充沛" if size > 100 else "⚠️ 待填充"
        if size > 100:
            valid_count += 1
        print(f"| `{f}` | {size} | {status} |")

    print("=" * 60)
    print(f"📈 总结: 发现 {len(files)} 个考据文件，其中 {valid_count} 个有效填充，总数据量: {total_size} 字节。")
    return valid_count > 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 merge_research.py <skill目录路径>")
        sys.exit(1)
    
    success = merge_research(sys.argv[1])
    sys.exit(0 if success else 1)
