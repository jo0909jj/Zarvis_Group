#!/bin/bash
# ComfyUI 圖片生成 Wrapper
# 供 OpenClaw 直接呼叫

set -e

# 配置 - 請根據實際情況修改
COMFYUI_HOST="${COMFYUI_HOST:-192.168.1.100}"
COMFYUI_PORT="${COMFYUI_PORT:-8188}"
OUTPUT_DIR="${COMFYUI_OUTPUT_DIR:-/home/joechiang/.openclaw/workspace/comfyui_output}"

# 參數
PROMPT="$1"
NEGATIVE="${2:-ugly, blurry, low quality, deformed}"
SEED="${3:-}"
OUTPUT_NAME="${4:-$(date +%Y%m%d-%H%M%S).png}"

if [ -z "$PROMPT" ]; then
    echo "用法：$0 <提示詞> [負面提示詞] [種子] [輸出檔名]"
    echo "範例：$0 \"A beautiful cat\" \"ugly, blurry\" 42 my-cat.png"
    exit 1
fi

# 確保輸出目錄存在
mkdir -p "$OUTPUT_DIR"

OUTPUT_PATH="$OUTPUT_DIR/$OUTPUT_NAME"

echo "🎨 ComfyUI 圖片生成"
echo "   主機：$COMFYUI_HOST:$COMFYUI_PORT"
echo "   提示詞：$PROMPT"
echo "   輸出：$OUTPUT_PATH"
echo ""

# 執行生成
python3 "$(dirname "$0")/comfyui_generate.py" \
    --host "$COMFYUI_HOST" \
    --port "$COMFYUI_PORT" \
    --prompt "$PROMPT" \
    --negative "$NEGATIVE" \
    --output "$OUTPUT_PATH" \
    ${SEED:+--seed $SEED}

if [ $? -eq 0 ] && [ -f "$OUTPUT_PATH" ]; then
    echo ""
    echo "✅ 生成成功！"
    echo "📁 $OUTPUT_PATH"
    echo "$OUTPUT_PATH"
else
    echo ""
    echo "❌ 生成失敗"
    exit 1
fi
