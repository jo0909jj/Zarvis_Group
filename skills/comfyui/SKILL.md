---
name: comfyui
description: 通過區網呼叫 ComfyUI 生成圖片。使用桌機上的 ComfyUI 服務，發送提示詞並獲取生成的圖片。支援文字生圖、圖生圖、ControlNet 等功能。
---

# ComfyUI 區網生圖技能

通過 HTTP API 呼叫區網內的 ComfyUI 服務生成圖片。

## 設定

### 1. ComfyUI 桌機配置

在桌機上啟動 ComfyUI 時添加 `--listen` 參數：

```bash
# Windows
python main.py --listen 0.0.0.0 --port 8188
```

### 2. 防火牆設定

確保桌機防火牆允許 8188 端口：

```powershell
# Windows PowerShell (管理員)
New-NetFirewallRule -DisplayName "ComfyUI" -Direction Inbound -LocalPort 8188 -Protocol TCP -Action Allow
```

### 3. 取得桌機 IP

```bash
ipconfig
# 找到 IPv4 Address，例如：192.168.1.100
```

## 使用方法

### 基本生圖

```bash
python scripts/comfyui_generate.py \
  --host 192.168.1.100 \
  --port 8188 \
  --prompt "A beautiful landscape" \
  --output output.png
```

### 使用工作流

```bash
python scripts/comfyui_generate.py \
  --host 192.168.1.100 \
  --port 8188 \
  --workflow workflow_api.json \
  --output output.png
```

## API 端點

| 端點 | 說明 |
|------|------|
| `GET /system_stats` | 查看系統狀態 |
| `GET /queue` | 查看佇列 |
| `POST /prompt` | 提交生成請求 |
| `GET /history/{id}` | 獲取生成歷史 |
| `GET /view?filename=xxx.png` | 下載圖片 |

## 範例工作流

### 文字生圖 (SDXL)

```json
{
  "3": {
    "class_type": "KSampler",
    "inputs": {
      "cfg": 8,
      "denoise": 1,
      "latent_image": ["5", 0],
      "model": ["4", 0],
      "negative": ["7", 0],
      "positive": ["6", 0],
      "sampler_name": "euler",
      "scheduler": "normal",
      "seed": 42,
      "steps": 20
    }
  },
  "4": {
    "class_type": "CheckpointLoaderSimple",
    "inputs": {
      "ckpt_name": "sd_xl_base_1.0.safetensors"
    }
  },
  "5": {
    "class_type": "EmptyLatentImage",
    "inputs": {
      "batch_size": 1,
      "height": 1024,
      "width": 1024
    }
  },
  "6": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "clip": ["4", 1],
      "text": "A beautiful landscape"
    }
  },
  "7": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "clip": ["4", 1],
      "text": "ugly, blurry, low quality"
    }
  },
  "8": {
    "class_type": "VAEDecode",
    "inputs": {
      "samples": ["3", 0],
      "vae": ["4", 2]
    }
  },
  "9": {
    "class_type": "SaveImage",
    "inputs": {
      "filename_prefix": "ComfyUI",
      "images": ["8", 0]
    }
  }
}
```

## 腳本範例

### comfyui_generate.py

```python
#!/usr/bin/env python3
"""
ComfyUI 圖片生成腳本
"""

import requests
import json
import time
import argparse
from pathlib import Path

def get_comfyui_url(host, port):
    return f"http://{host}:{port}"

def queue_prompt(url, prompt):
    """提交生成請求"""
    response = requests.post(f"{url}/prompt", json={"prompt": prompt})
    return response.json()

def get_history(url, prompt_id):
    """獲取生成歷史"""
    response = requests.get(f"{url}/history/{prompt_id}")
    return response.json()

def get_image(url, filename, subfolder, folder_type):
    """下載圖片"""
    params = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    response = requests.get(f"{url}/view", params=params)
    return response.content

def wait_for_generation(url, prompt_id, timeout=300):
    """等待生成完成"""
    start_time = time.time()
    while True:
        try:
            history = get_history(url, prompt_id)
            if prompt_id in history:
                return history[prompt_id]
        except Exception as e:
            print(f"等待中... ({e})")
        
        if time.time() - start_time > timeout:
            raise TimeoutError("生成超時")
        
        time.sleep(1)

def generate(host, port, prompt, workflow=None, output="output.png"):
    """
    生成圖片
    
    Args:
        host: ComfyUI 主機 IP
        port: ComfyUI 端口
        prompt: 提示詞（字串或工作流字典）
        workflow: 工作流 JSON 文件路徑
        output: 輸出文件路徑
    """
    url = get_comfyui_url(host, port)
    
    # 檢查連線
    try:
        stats = requests.get(f"{url}/system_stats")
        print(f"✅ ComfyUI 連線成功：{stats.json()}")
    except Exception as e:
        print(f"❌ 無法連接 ComfyUI: {e}")
        return
    
    # 載入工作流或使用預設
    if workflow:
        with open(workflow, 'r') as f:
            workflow_data = json.load(f)
    else:
        # 使用預設工作流（需要根據實際節點 ID 調整）
        workflow_data = {
            "3": {"class_type": "KSampler", "inputs": {"seed": 42}},
            "6": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt}},
        }
    
    # 提交請求
    print(f"📤 提交生成請求...")
    result = queue_prompt(url, workflow_data)
    prompt_id = result.get("prompt_id")
    print(f"📋 Prompt ID: {prompt_id}")
    
    # 等待完成
    print(f"⏳ 等待生成完成...")
    history = wait_for_generation(url, prompt_id)
    
    # 獲取圖片
    print(f"📥 下載圖片...")
    outputs = history.get("outputs", {})
    for node_id, node_output in outputs.items():
        if "images" in node_output:
            for image in node_output["images"]:
                image_data = get_image(
                    url,
                    image["filename"],
                    image.get("subfolder", ""),
                    image.get("type", "output")
                )
                
                # 保存圖片
                output_path = Path(output)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'wb') as f:
                    f.write(image_data)
                
                print(f"✅ 圖片已保存：{output_path}")
                return str(output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ComfyUI 圖片生成")
    parser.add_argument("--host", required=True, help="ComfyUI 主機 IP")
    parser.add_argument("--port", default=8188, type=int, help="ComfyUI 端口")
    parser.add_argument("--prompt", default="", help="提示詞")
    parser.add_argument("--workflow", help="工作流 JSON 文件")
    parser.add_argument("--output", default="output.png", help="輸出文件")
    
    args = parser.parse_args()
    generate(args.host, args.port, args.prompt, args.workflow, args.output)
```

## OpenClaw 整合

### 在 OpenClaw 中使用

創建一個 wrapper 腳本讓 OpenClaw 可以直接呼叫：

```bash
#!/bin/bash
# scripts/generate_image.sh

HOST="192.168.1.100"  # 桌機 IP
PORT="8188"
PROMPT="$1"
OUTPUT="/tmp/comfy_output.png"

python scripts/comfyui_generate.py \
  --host $HOST \
  --port $PORT \
  --prompt "$PROMPT" \
  --output $OUTPUT

# 回傳圖片路徑
echo $OUTPUT
```

## 故障排除

### 無法連接

```bash
# 測試連線
curl http://192.168.1.100:8188/system_stats

# 檢查防火牆
telnet 192.168.1.100 8188
```

### 生成超時

增加 timeout 參數或檢查 ComfyUI 佇列：
```bash
curl http://192.168.1.100:8188/queue
```

### 圖片無法下載

檢查 ComfyUI 輸出目錄權限，確認 `output/` 文件夾可讀取。

---

**Last Updated:** 2026-03-12
**Author:** Zarvis
