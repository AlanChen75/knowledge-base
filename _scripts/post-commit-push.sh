#!/bin/bash
# Git post-commit hook: auto push after each commit
# 安裝方式: 此腳本會被 symlink 到 .git/hooks/post-commit

echo "🔄 自動推送到 GitHub..."
git push origin main --quiet 2>/dev/null &
