# 🚀 快速配置指南 - DeskIn + ComfyUI

## 目標
通過 DeskIn 喚醒桌機（JOESPC），然後呼叫 ComfyUI 生成圖片。

---

## 📋 步驟 1：取得桌機 MAC 地址

**在桌機（JOESPC）上執行：**

### Windows
```powershell
# 方法 1
ipconfig /all
# 找到「實體地址」格式：00-1A-2B-3C-4D-5E

# 方法 2
getmac /v
```

### 記錄以下資訊：
- ✅ MAC 地址：`00:1A:2B:3C:4D:5E`（範例）
- ✅ IP 地址：`192.168.1.100`（範例）
- ✅ 設備名稱：`JOESPC`

---

## 📋 步驟 2：配置 DeskIn WoL

**在桌機上：**

### 1. BIOS 設定
重啟電腦，進入 BIOS，啟用：
- ✅ `Wake-on-LAN`
- ✅ `Power On By PCI-E`
- ❌ `ERP Ready` = Disabled

### 2. Windows 網卡設定
```powershell
# 管理員 PowerShell
# 啟用 WoL
Set-NetAdapterAdvancedProperty -Name "Ethernet" -DisplayName "Wake on Magic Packet" -DisplayValue "Enabled"

# 允許網卡喚醒
powercfg /devicequery wake_armed
```

### 3. DeskIn 設定
- 開啟 DeskIn
- 確認設備名稱為 `JOESPC`
- 在設定中啟用 Wake-on-LAN

---

## 📋 步驟 3：配置 OpenClaw（WSL2）

```bash
cd ~/.openclaw/workspace/skills/deskin

# 複製配置
cp config.env.example config.env

# 編輯配置
nano config.env
```

**修改以下內容：**
```bash
DESKIN_DEVICE_NAME="JOESPC"
DESKIN_DEVICE_MAC="00:1A:2B:3C:4D:5E"  # 替換為實際 MAC
DESKIN_DEVICE_IP="192.168.1.100"       # 替換為實際 IP
COMFYUI_HOST="192.168.1.100"           # 同 IP
```

---

## 📋 步驟 4：測試連線

### 測試 WoL
```bash
cd ~/.openclaw/workspace/skills/deskin

# 發送 WoL 封包
python3 scripts/wol.py --mac "00:1A:2B:3C:4D:5E"
```

### 測試 ComfyUI 連線
```bash
cd ~/.openclaw/workspace/skills/comfyui/scripts

# 測試連線
bash test_connection.sh
```

---

## 📋 步驟 5：完整流程測試

```bash
# 1. 喚醒電腦
cd ~/.openclaw/workspace/skills/deskin
bash scripts/wake_pc.sh JOESPC

# 2. 等待啟動
sleep 30

# 3. 生成圖片
cd ../comfyui/scripts
bash generate_image.sh "A beautiful cat"
```

---

## 🔧 故障排除

### 問題：WoL 無效
**解決：**
1. 檢查 BIOS WoL 設定
2. 確認網卡 WoL 已啟用
3. 確認防火牆允許 UDP 9
4. 嘗試多次發送 WoL

### 問題：ComfyUI 無法連接
**解決：**
1. 確認 ComfyUI 使用 `--listen` 啟動
2. 檢查防火牆允許 8188 端口
3. 確認 IP 地址正確

### 問題：跨區網無法喚醒
**解決：**
1. WoL 預設僅限區網
2. 需要路由器支援定向廣播
3. 或使用 DeskIn 雲端喚醒功能

---

## 📝 一鍵執行腳本

創建 `~/wake_and_generate.sh`：

```bash
#!/bin/bash
# 一鍵喚醒並生成圖片

DEVICE="JOESPC"
PROMPT="$1"

cd ~/.openclaw/workspace/skills

echo "🔌 喚醒 $DEVICE..."
bash deskin/scripts/wake_pc.sh "$DEVICE"

echo "⏳ 等待啟動..."
sleep 30

echo "🎨 生成：$PROMPT"
bash comfyui/scripts/generate_image.sh "$PROMPT"

echo "✅ 完成！"
```

使用：
```bash
chmod +x ~/wake_and_generate.sh
~/wake_and_generate.sh "A beautiful cat"
```

---

**完成！** 🎉

現在你可以：
1. 從 WSL2 喚醒桌機
2. 自動呼叫 ComfyUI 生成圖片
3. 整合到 OpenClaw 工作流程
