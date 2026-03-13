#!/bin/bash
# AI PC Agent - Cron 自動更新腳本
# 添加到 crontab: */20 * * * * /path/to/cron_update.sh
# 每 20 分鐘更新一次

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

echo "🤖 AI PC Agent - 自動更新"
echo "時間：$(date)"
echo ""

# 1. 拉取最新代碼
echo "📥 拉取最新代碼..."
git pull origin main || echo "⚠️ Git 拉取失敗"

# 2. 安裝依賴
echo "📦 檢查依賴..."
pip install -r requirements.txt --quiet || echo "⚠️ 依賴安裝失敗"

# 3. 運行系統監控
echo "📊 生成系統報告..."
python modules/system_monitor.py > logs/system_report.txt 2>&1 || echo "⚠️ 監控失敗"

# 4. 截圖（可選）
echo "📸 截取螢幕..."
# python modules/screenshot.py || echo "⚠️ 截圖失敗"

# 5. 提交報告（如果有變更）
echo "💾 保存報告..."
git add logs/ 2>/dev/null || true
git commit -m "Auto-update: $(date '+%Y-%m-%d %H:%M')" 2>/dev/null || true
git push origin main 2>/dev/null || echo "⚠️ Git 推送失敗"

echo ""
echo "✅ 更新完成！"
echo "========================================"
