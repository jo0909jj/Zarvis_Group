#!/usr/bin/env python3
"""
ComfyUI 圖片生成腳本
通過區網呼叫桌機上的 ComfyUI 生成圖片
"""

import requests
import json
import time
import argparse
from pathlib import Path

DEFAULT_WORKFLOW = {
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
            "text": ""
        }
    },
    "7": {
        "class_type": "CLIPTextEncode",
        "inputs": {
            "clip": ["4", 1],
            "text": "ugly, blurry, low quality, deformed"
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

def get_comfyui_url(host, port):
    return f"http://{host}:{port}"

def queue_prompt(url, prompt):
    """提交生成請求"""
    response = requests.post(f"{url}/prompt", json={"prompt": prompt})
    response.raise_for_status()
    return response.json()

def get_history(url, prompt_id):
    """獲取生成歷史"""
    response = requests.get(f"{url}/history/{prompt_id}")
    response.raise_for_status()
    return response.json()

def get_image(url, filename, subfolder, folder_type):
    """下載圖片"""
    params = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    response = requests.get(f"{url}/view", params=params)
    response.raise_for_status()
    return response.content

def wait_for_generation(url, prompt_id, timeout=300, poll_interval=1):
    """等待生成完成"""
    start_time = time.time()
    while True:
        try:
            history = get_history(url, prompt_id)
            if prompt_id in history:
                return history[prompt_id]
        except Exception as e:
            print(f"⏳ 等待 ComfyUI 回應... ({e})")
        
        if time.time() - start_time > timeout:
            raise TimeoutError(f"生成超時 ({timeout}秒)")
        
        time.sleep(poll_interval)

def check_connection(url):
    """檢查 ComfyUI 連線"""
    try:
        stats = requests.get(f"{url}/system_stats", timeout=5)
        stats.raise_for_status()
        return True, stats.json()
    except Exception as e:
        return False, str(e)

def generate(host, port, prompt, negative_prompt=None, workflow=None, 
             output="output.png", seed=None, steps=20, cfg=8, 
             width=1024, height=1024, timeout=300):
    """
    生成圖片
    
    Args:
        host: ComfyUI 主機 IP
        port: ComfyUI 端口
        prompt: 提示詞
        negative_prompt: 負面提示詞
        workflow: 工作流 JSON 文件路徑
        output: 輸出文件路徑
        seed: 隨機種子
        steps: 採樣步數
        cfg: CFG scale
        width: 圖片寬度
        height: 圖片高度
        timeout: 超時時間（秒）
    """
    url = get_comfyui_url(host, port)
    
    # 檢查連線
    print(f"🔍 檢查 ComfyUI 連線 ({host}:{port})...")
    connected, result = check_connection(url)
    if not connected:
        print(f"❌ 無法連接 ComfyUI: {result}")
        print(f"\n請確認:")
        print(f"  1. ComfyUI 已啟動且使用 --listen 參數")
        print(f"  2. 防火牆允許端口 {port}")
        print(f"  3. IP 位置正確：{host}")
        return None
    
    print(f"✅ ComfyUI 連線成功")
    if "system_stats" in result:
        stats = result["system_stats"]
        print(f"   顯存：{stats.get('mem', {}).get('free', 'N/A')} / {stats.get('mem', {}).get('total', 'N/A')}")
    
    # 載入或創建工作流程
    if workflow:
        print(f"📄 載入工作流：{workflow}")
        with open(workflow, 'r', encoding='utf-8') as f:
            workflow_data = json.load(f)
    else:
        print(f"🎨 使用預設工作流")
        workflow_data = DEFAULT_WORKFLOW.copy()
        
        # 更新提示詞
        if "6" in workflow_data:
            workflow_data["6"]["inputs"]["text"] = prompt
        
        if negative_prompt and "7" in workflow_data:
            workflow_data["7"]["inputs"]["text"] = negative_prompt
        
        # 更新參數
        if "3" in workflow_data:
            if seed is not None:
                workflow_data["3"]["inputs"]["seed"] = seed
            workflow_data["3"]["inputs"]["steps"] = steps
            workflow_data["3"]["inputs"]["cfg"] = cfg
        
        if "5" in workflow_data:
            workflow_data["5"]["inputs"]["width"] = width
            workflow_data["5"]["inputs"]["height"] = height
    
    # 提交請求
    print(f"📤 提交生成請求...")
    print(f"   提示詞：{prompt[:50]}{'...' if len(prompt) > 50 else ''}")
    result = queue_prompt(url, workflow_data)
    prompt_id = result.get("prompt_id")
    print(f"📋 Prompt ID: {prompt_id}")
    
    # 等待完成
    print(f"⏳ 等待生成完成 (超時：{timeout}秒)...")
    try:
        history = wait_for_generation(url, prompt_id, timeout=timeout)
    except TimeoutError as e:
        print(f"❌ {e}")
        return None
    
    # 獲取圖片
    print(f"📥 下載圖片...")
    outputs = history.get("outputs", {})
    image_paths = []
    
    for node_id, node_output in outputs.items():
        if "images" in node_output:
            for image in node_output["images"]:
                try:
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
                    image_paths.append(str(output_path))
                except Exception as e:
                    print(f"❌ 下載圖片失敗：{e}")
    
    return image_paths if image_paths else None

def main():
    parser = argparse.ArgumentParser(description="ComfyUI 圖片生成")
    parser.add_argument("--host", required=True, help="ComfyUI 主機 IP")
    parser.add_argument("--port", default=8188, type=int, help="ComfyUI 端口 (預設：8188)")
    parser.add_argument("--prompt", required=True, help="提示詞")
    parser.add_argument("--negative", default="", help="負面提示詞")
    parser.add_argument("--workflow", help="工作流 JSON 文件")
    parser.add_argument("--output", default="output.png", help="輸出文件路徑")
    parser.add_argument("--seed", type=int, help="隨機種子")
    parser.add_argument("--steps", default=20, type=int, help="採樣步數")
    parser.add_argument("--cfg", default=8, type=float, help="CFG Scale")
    parser.add_argument("--width", default=1024, type=int, help="圖片寬度")
    parser.add_argument("--height", default=1024, type=int, help="圖片高度")
    parser.add_argument("--timeout", default=300, type=int, help="超時時間（秒）")
    
    args = parser.parse_args()
    
    image_paths = generate(
        host=args.host,
        port=args.port,
        prompt=args.prompt,
        negative_prompt=args.negative,
        workflow=args.workflow,
        output=args.output,
        seed=args.seed,
        steps=args.steps,
        cfg=args.cfg,
        width=args.width,
        height=args.height,
        timeout=args.timeout
    )
    
    if image_paths:
        print(f"\n🎉 生成完成！共 {len(image_paths)} 張圖片")
        for path in image_paths:
            print(f"   📁 {path}")
    else:
        print(f"\n❌ 生成失敗")

if __name__ == "__main__":
    main()
