#!/bin/bash
# ComfyUI 快速測試腳本
# 測試與桌機 ComfyUI 的連線

set -e

# 配置
COMFYUI_HOST="${COMFYUI_HOST:-192.168.1.100}"
COMFYUI_PORT="${COMFYUI_PORT:-8188}"

echo "🔍 測試 ComfyUI 連線..."
echo "   主機：$COMFYUI_HOST"
echo "   端口：$COMFYUI_PORT"
echo ""

# 測試連線
echo "📡 發送請求..."
if curl -s --connect-timeout 5 "http://$COMFYUI_HOST:$COMFYUI_PORT/system_stats" | jq .; then
    echo ""
    echo "✅ ComfyUI 連線成功！"
    echo ""
    echo "📋 下一步:"
    echo "   1. 確認 ComfyUI 使用 --listen 啟動"
    echo "   2. 檢查防火牆是否允許端口 $COMFYUI_PORT"
    echo "   3. 使用 generate_image.sh 生成圖片"
else
    echo ""
    echo "❌ 無法連接 ComfyUI"
    echo ""
    echo "🔧 故障排除:"
    echo "   1. 確認桌機 IP 正確：ipconfig (Windows) 或 ifconfig (Linux)"
    echo "   2. 確認 ComfyUI 已啟動且使用 --listen 參數"
    echo "   3. 檢查防火牆："
    echo "      New-NetFirewallRule -DisplayName \"ComfyUI\" -Direction Inbound -LocalPort $COMFYUI_PORT -Protocol TCP -Action Allow"
    echo "   4. 測試 telnet: telnet $COMFYUI_HOST $COMFYUI_PORT"
fi
