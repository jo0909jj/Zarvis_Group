# ComfyUI 區網生圖技能 🎨

通過區網呼叫桌機上的 ComfyUI 生成圖片。

## 📋 需求

- 桌機安裝 ComfyUI
- 桌機與 OpenClaw 在同一區網
- Python 3.8+
- `requests` 套件

## 🚀 快速開始

### 1. 桌機配置

**Windows PowerShell (管理員):**

```powershell
# 1. 啟動 ComfyUI 時添加 --listen 參數
cd path\to\ComfyUI
python main.py --listen 0.0.0.0 --port 8188

# 2. 允許防火牆
New-NetFirewallRule -DisplayName "ComfyUI" -Direction Inbound -LocalPort 8188 -Protocol TCP -Action Allow
```

### 2. 取得桌機 IP

```powershell
ipconfig
# 找到 IPv4 Address，例如：192.168.1.100
```

### 3. 測試連線

在 WSL2 測試：

```bash
cd ~/.openclaw/workspace/skills/comfyui/scripts
bash test_connection.sh
```

或手動測試：

```bash
curl http://192.168.1.100:8188/system_stats
```

### 4. 生成圖片

```bash
# 簡單用法
bash generate_image.sh "A beautiful cat"

# 完整用法
bash generate_image.sh "A beautiful cat" "ugly, blurry" 42 my-cat.png
```

或使用 Python：

```bash
python comfyui_generate.py \
    --host 192.168.1.100 \
    --port 8188 \
    --prompt "A beautiful cat" \
    --output cat.png
```

## 📖 使用說明

### 環境變量

可以在 `~/.bashrc` 或腳本中配置：

```bash
export COMFYUI_HOST="192.168.1.100"
export COMFYUI_PORT="8188"
export COMFYUI_OUTPUT_DIR="/home/joechiang/.openclaw/workspace/comfyui_output"
```

### Python 腳本參數

```bash
python comfyui_generate.py \
    --host 192.168.1.100 \      # ComfyUI 主機 IP（必需）
    --port 8188 \               # 端口（預設：8188）
    --prompt "提示詞" \          # 提示詞（必需）
    --negative "負面提示詞" \    # 負面提示詞
    --workflow workflow.json \  # 自訂工作流
    --output output.png \       # 輸出路徑
    --seed 42 \                 # 隨機種子
    --steps 30 \                # 採樣步數（預設：20）
    --cfg 7.5 \                 # CFG Scale（預設：8）
    --width 1024 \              # 寬度（預設：1024）
    --height 1024 \             # 高度（預設：1024）
    --timeout 300               # 超時時間（預設：300 秒）
```

## 🔧 故障排除

### 無法連接

```bash
# 測試連線
curl http://192.168.1.100:8188/system_stats

# 檢查端口
telnet 192.168.1.100 8188

# 檢查防火牆（Windows）
Get-NetFirewallRule | Where-Object {$_.DisplayName -like "*ComfyUI*"}
```

### 生成超時

- 增加 `--timeout` 參數
- 檢查 ComfyUI 佇列：`curl http://192.168.1.100:8188/queue`
- 確認顯存充足

### 圖片無法下載

- 檢查 ComfyUI `output/` 目錄權限
- 確認輸出目錄可寫入

## 📁 文件結構

```
comfyui/
├── SKILL.md                    # 技能說明
├── README.md                   # 使用說明
└── scripts/
    ├── comfyui_generate.py     # Python 生成腳本
    ├── generate_image.sh       # Shell Wrapper
    └── test_connection.sh      # 連線測試
```

## 🎯 OpenClaw 整合

在 OpenClaw 中使用：

```python
# 通過 exec 呼叫
exec("bash ~/.openclaw/workspace/skills/comfyui/scripts/generate_image.sh 'A cat'")
```

或創建自動化腳本整合到工作流程中。

## 📝 範例

### 生成風景圖

```bash
bash generate_image.sh \
    "A serene mountain landscape at sunset, golden hour, photorealistic" \
    "ugly, blurry, low quality" \
    12345 \
    landscape.png
```

### 生成動漫角色

```bash
bash generate_image.sh \
    "anime girl with blue hair, school uniform, cherry blossoms, detailed eyes" \
    "ugly, deformed, low quality" \
    42 \
    anime_girl.png
```

### 使用自訂工作流

```bash
python comfyui_generate.py \
    --host 192.168.1.100 \
    --port 8188 \
    --workflow my_workflow.json \
    --output result.png
```

---

**Last Updated:** 2026-03-12
**Author:** Zarvis
