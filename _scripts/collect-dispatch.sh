#!/bin/bash
# collect-dispatch.sh — 收集桌面上 Claude Dispatch 產生的檔案到 SecondBrain
# 用法: ./collect-dispatch.sh [--auto-commit]

SECOND_BRAIN="$HOME/SecondBrain"
DISPATCH_DIR="$SECOND_BRAIN/dispatch-outputs"
DESKTOP="$HOME/Desktop"
DATE=$(date +%Y-%m-%d)
MOVED=0

# 收集桌面上的 .md 檔案（排除已知專案目錄）
for f in "$DESKTOP"/*.md; do
    [ -f "$f" ] || continue

    filename=$(basename "$f")

    # 跳過已知的非 dispatch 檔案（可自行添加）
    case "$filename" in
        README.md|CHANGELOG.md) continue ;;
    esac

    # 加上日期前綴（如果沒有的話）
    if [[ ! "$filename" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2} ]]; then
        new_name="${DATE}_${filename}"
    else
        new_name="$filename"
    fi

    mv "$f" "$DISPATCH_DIR/$new_name"
    echo "✓ $filename → dispatch-outputs/$new_name"
    MOVED=$((MOVED + 1))
done

if [ "$MOVED" -eq 0 ]; then
    echo "桌面沒有新的 .md 檔案"
    exit 0
fi

echo ""
echo "共移動 $MOVED 個檔案到 $DISPATCH_DIR"

# 自動 commit + push
if [ "$1" = "--auto-commit" ]; then
    cd "$SECOND_BRAIN"
    git add dispatch-outputs/
    git commit -m "feat: collect $MOVED dispatch outputs ($DATE)"
    git push
    echo "✓ 已推送到 GitHub"
fi
