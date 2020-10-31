#!/bin/bash
BASEDIR=$(dirname "$0")
DOT_ENV="${BASEDIR}/../conf/.env"
export "$(grep -v '#.*' "$DOT_ENV" | xargs)"
cd "$BASEDIR/../" || exit
LOG_FILE=${LOGGING_DIR}/tgfp_update_all.log
exec &> >(tee -a "$LOG_FILE")

echo ''
echo "=============================================="
date
echo "=============================================="
echo "Backing up mongo DB"
bin/mongo_backup.sh
echo "Updating scores..."
env/bin/python bin/tgfp_update_scores.py
echo "Updating win/loss..."
env/bin/python bin/tgfp_update_win_loss.py
echo "Restarting bot"
bin/discord_bot_service.sh restart
