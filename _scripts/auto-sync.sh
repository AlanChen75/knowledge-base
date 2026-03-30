#!/bin/bash
# auto-sync.sh — ac-mac 用：git pull → Notion sync → git push (如果有 TG Bot 產生的新內容)
# 設計給 cron 呼叫：*/30 * * * * /home/ac-mac/knowledge-base/_scripts/auto-sync.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
KB_DIR="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$SCRIPT_DIR/.sync.log"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"; }

cd "$KB_DIR"

# 1. Pull latest from MacBook (or other machines)
log "Starting sync..."
git pull --rebase --quiet origin main 2>>"$LOG_FILE" || {
    log "ERROR: git pull failed"
    exit 1
}

# 2. Commit any local changes (from TG Bot, etc.)
if [ -n "$(git status --porcelain)" ]; then
    git add -A
    git commit -m "chore: auto-sync from $(hostname) ($(date +%Y-%m-%d))" --quiet
    git push --quiet origin main
    log "Pushed local changes"
else
    log "No local changes"
fi

# 3. Sync to Notion (if credentials exist)
if [ -f "$KB_DIR/.env" ] && grep -q "NOTION_TOKEN" "$KB_DIR/.env" 2>/dev/null; then
    cd "$SCRIPT_DIR"
    python3 notion-sync.py >> "$LOG_FILE" 2>&1 || log "WARNING: Notion sync had errors"
    log "Notion sync completed"
else
    log "Notion credentials not configured, skipping"
fi

log "Sync done"
