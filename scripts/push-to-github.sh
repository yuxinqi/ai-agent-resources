#!/bin/bash
# ============================================
# AI Agent Resources - GitHub 推送脚本
# ============================================
# 使用方法:
#   bash scripts/push-to-github.sh
# ============================================

set -e

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR"

echo "============================================"
echo "  AI Agent Resources - GitHub 推送"
echo "============================================"
echo ""

# 初始化 Git 仓库（如果没有）
if [ ! -d ".git" ]; then
  echo "→ 初始化 Git 仓库..."
  git init
  git checkout -b main
fi

# 配置远程仓库
if git remote get-url origin 2>/dev/null; then
  echo "✅ 远程仓库已配置"
  git remote set-url origin https://github.com/yuxinqi/ai-agent-resources.git
else
  echo "→ 添加远程仓库..."
  git remote add origin https://github.com/yuxinqi/ai-agent-resources.git
fi

echo ""
echo "→ 添加文件..."
git add docs/ verification/ visualization/ scripts/ .github/ \
  README.md INDEX.md CONTRIBUTING.md LICENSE \
  CODE_OF_CONDUCT.md SECURITY.md \
  .editorconfig .gitattributes .gitignore requirements.txt

echo "→ 提交..."
if git diff --cached --quiet; then
  echo "ℹ️  没有新的变更需要提交"
else
  git commit -m "🎉 AI Agent Resources — 结构化、可验真的 AI 知识库

- 核心概念、API 平台、提示词、Skills、工具、工作流文档
- 验真系统（方法论 + 验真模板）
- D3.js 可视化知识图谱
- CI 自动索引生成 + GitHub Pages 部署
- 社区标准（LICENSE、CONTRIBUTING、PR/Issue 模板）"
fi

echo ""
echo "→ 推送到 GitHub..."
echo ""

git push -u origin main

echo ""
echo "============================================"
echo "  ✅ 推送完成！"
echo "  访问: https://github.com/yuxinqi/ai-agent-resources"
echo "============================================"
