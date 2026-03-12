#!/bin/bash
# DeskIn 喚醒 PC 腳本
# 喚醒指定設備並等待上線

set -e

# 配置（從環境變量或預設值）
DEVICE_NAME="${1:-JOESPC}"
TIMEOUT="${2:-120}"
INTERVAL="${3:-5}"

# 設備 MAC 地址配置
declare -A DEVICE_MACS=(
    ["JOESPC"]="00:11:22:33:44:55"  # 請修改為實際 MAC 地址
    # 添加更多設備...
)

# 檢查設備名稱
if [ -z "$DEVICE_NAME" ]; then
    echo "用法：$0 <設備名稱> [超時秒數] [檢查間隔]"
    echo "範例：$0 JOESPC 120 5"
    exit 1
fi

# 取得 MAC 地址
MAC_ADDRESS="${DEVICE_MACS[$DEVICE_NAME]}"
if [ -z "$MAC_ADDRESS" ]; then
    echo "❌ 找不到設備 $DEVICE_NAME 的 MAC 地址"
    echo "請在腳本中配置 DEVICE_MACS 陣列"
    exit 1
fi

echo "🔌 DeskIn 喚醒電腦"
echo "   設備名稱：$DEVICE_NAME"
echo "   MAC 地址：$MAC_ADDRESS"
echo "   超時時間：$TIMEOUT 秒"
echo "   檢查間隔：$INTERVAL 秒"
echo ""

# 發送 WoL 封包
SCRIPT_DIR="$(dirname "$0")"
python3 "$SCRIPT_DIR/wol.py" --mac "$MAC_ADDRESS" --count 3

echo ""
echo "⏳ 等待電腦啟動..."

# 等待電腦上線（可選：ping 測試）
START_TIME=$(date +%s)
while true; do
    CURRENT_TIME=$(date +%s)
    ELAPSED=$((CURRENT_TIME - START_TIME))
    
    if [ $ELAPSED -ge $TIMEOUT ]; then
        echo "⚠️ 超時（$TIMEOUT 秒）"
        echo "💡 請手動檢查電腦狀態"
        break
    fi
    
    # 這裡可以添加 ping 測試或其他在線檢查
    # if ping -c 1 -W 1 192.168.1.100 > /dev/null 2>&1; then
    #     echo "✅ 電腦已在線！"
    #     break
    # fi
    
    echo "   已等待 ${ELAPSED}s / ${TIMEOUT}s..."
    sleep $INTERVAL
done

echo ""
echo "✅ 喚醒流程完成"
echo ""
echo "📋 下一步:"
echo "   1. 等待電腦完全啟動（約 30-60 秒）"
echo "   2. 使用 DeskIn 連接或呼叫 ComfyUI"
echo "   3. 執行：bash ../comfyui/scripts/generate_image.sh \"提示詞\""
