#!/usr/bin/env bash
#
# 本地 Git Pre-commit 钩子一键配置脚本
# 用途: 挂载 pre-commit 钩子，每次执行 `git commit` 前自动运行技能合规校验。
#

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOOK_FILE="${REPO_ROOT}/.git/hooks/pre-commit"

if [ ! -d "${REPO_ROOT}/.git" ]; then
    echo "❌ 错误: 当前目录不是 Git 仓库根目录，无法配置 Git Hook。"
    exit 1
fi

mkdir -p "${REPO_ROOT}/.git/hooks"

cat << 'EOF' > "${HOOK_FILE}"
#!/usr/bin/env bash
# Git Pre-commit Hook: 技能合规自动化校验

echo "🔍 [Pre-commit Hook] 正在运行 Agent Skills 合规校验..."
if ! ./scripts/validate_skills.py; then
    echo "❌ [Pre-commit Hook] 技能合规校验失败，已拦截提交！请修复上述问题后再重试。"
    exit 1
fi
EOF

chmod +x "${HOOK_FILE}"

echo "✨ 成功配置 Git Pre-commit 钩子: ${HOOK_FILE}"
echo "💡 现在每次执行 'git commit' 时都将自动触发合规校验。"
