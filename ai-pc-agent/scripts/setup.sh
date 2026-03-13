#!/bin/bash
# AI PC Agent - 安裝腳本

set -e

echo "🤖 AI PC Agent - 安裝程序"
echo "========================================"
echo ""

# 檢查 Python
echo "📍 檢查 Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python 3"
    exit 1
fi
python3 --version

# 創建虛擬環境
echo ""
echo "📦 創建虛擬環境..."
python3 -m venv venv
source venv/bin/activate

# 安裝依賴
echo ""
echo "📦 安裝依賴..."
pip install -r requirements.txt

# 安裝 Playwright
echo ""
echo "🌐 安裝 Playwright..."
playwright install chromium

# 創建必要目錄
echo ""
echo "📁 創建目錄結構..."
mkdir -p logs screenshots demos tests

# 複製配置範例
if [ ! -f config.yaml ]; then
    echo "📝 創建配置文件..."
    cp config.yaml.example config.yaml 2>/dev/null || true
fi

# 設定執行權限
echo ""
echo "🔧 設定執行權限..."
chmod +x scripts/*.sh

echo ""
echo "========================================"
echo "✅ 安裝完成！"
echo ""
echo "下一步:"
echo "1. 編輯 config.yaml 配置文件"
echo "2. 運行：python scripts/run_agent.py"
echo "3. 或啟動 Web 介面：python web/dashboard.py"
echo ""
