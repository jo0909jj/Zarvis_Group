---
name: deskin
description: 通過 DeskIn 遠程桌面軟體控制遠程電腦。支援喚醒電腦（Wake-on-LAN）、遠程桌面連接、文件傳輸等功能。可與區網內的 ComfyUI 或其他服務整合。
---

# DeskIn 遠程控制技能

通過 DeskIn API 和 Wake-on-LAN 協議控制遠程電腦。

## 功能

- 🔌 **Wake-on-LAN** - 遠程喚醒關機中的電腦
- 🖥️ **遠程桌面** - 建立遠程桌面連接
- 📁 **文件傳輸** - 上傳/下載文件
- 💻 **設備管理** - 查看在線設備狀態

## 設定

### 1. DeskIn 帳號配置

在 DeskIn 應用程式中：
1. 登入你的帳號
2. 確保目標電腦（JOESPC）已添加到設備清單
3. 啟用 Wake-on-LAN 功能

### 2. 取得設備資訊

在 DeskIn 應用程式中查看：
- 設備名稱：`JOESPC`
- 設備 ID：在設備詳情中找到
- MAC 地址：用於 WoL

### 3. 配置環境變量

創建 `~/.openclaw/workspace/skills/deskin/config.env`：

```bash
# DeskIn 帳號
DESKIN_USERNAME="your_email@example.com"
DESKIN_PASSWORD="your_password"

# 目標設備
DESKIN_DEVICE_NAME="JOESPC"
DESKIN_DEVICE_ID="device_id_here"
DESKIN_DEVICE_MAC="00:11:22:33:44:55"

# 可選：DeskIn API 端點
DESKIN_API_URL="https://api.deskin.io"
```

## 使用方法

### 喚醒電腦

```bash
# 通過 WoL 喚醒
bash wake_pc.sh JOESPC

# 或指定 MAC 地址
python deskin_wol.py --mac "00:11:22:33:44:55"
```

### 檢查設備狀態

```bash
python deskin_status.py --device "JOESPC"
```

### 建立遠程連接

```bash
# 啟動 DeskIn 連接
deskin connect --device "JOESPC"
```

## Wake-on-LAN 原理

WoL 通過發送「魔法封包」（Magic Packet）到目標設備的 MAC 地址來喚醒電腦。

**魔法封包格式：**
- 6 字節的 `FF`（同步信號）
- 16 次重複的目標 MAC 地址（共 96 字節）

**發送方式：**
1. **區網內** - 直接廣播到 `255.255.255.255:9`
2. **跨區網** - 需要路由器支援定向廣播
3. **通過 DeskIn** - 使用 DeskIn 的遠程喚醒 API

## 腳本說明

### deskin_wol.py

發送 Wake-on-LAN 魔法封包。

```bash
python deskin_wol.py \
    --mac "00:11:22:33:44:55" \
    [--ip "255.255.255.255"] \
    [--port "9"]
```

### deskin_status.py

檢查 DeskIn 設備在線狀態。

```bash
python deskin_status.py \
    --username "your_email@example.com" \
    --password "your_password" \
    --device "JOESPC"
```

### wake_pc.sh

整合腳本，自動喚醒並等待電腦上線。

```bash
bash wake_pc.sh \
    "JOESPC" \
    [--timeout 120] \
    [--interval 5]
```

## 完整工作流程

### 1. 喚醒 PC 並呼叫 ComfyUI

```bash
# 喚醒電腦
bash wake_pc.sh "JOESPC"

# 等待 30 秒讓電腦完全啟動
sleep 30

# 呼叫 ComfyUI 生成圖片
bash ../comfyui/scripts/generate_image.sh "A beautiful cat"
```

### 2. 自動化腳本範例

```bash
#!/bin/bash
# 完整自動化流程

DEVICE="JOESPC"
COMFYUI_HOST="192.168.1.100"
PROMPT="A beautiful landscape"

echo "🔌 喚醒 $DEVICE..."
bash wake_pc.sh "$DEVICE"

echo "⏳ 等待電腦啟動..."
sleep 30

echo "🎨 生成圖片..."
bash ../comfyui/scripts/generate_image.sh "$PROMPT"

echo "✅ 完成！"
```

## 故障排除

### 電腦無法喚醒

1. **檢查 BIOS 設定**
   - 進入 BIOS/UEFI
   - 啟用 `Wake-on-LAN` 或 `Power On By PCI-E`
   - 啟用 `ERP Ready` 或 `Deep Sleep` 為 Disabled

2. **檢查 Windows 設定**
   ```powershell
   # 查看網卡 WoL 設定
   Get-NetAdapter | Select-Object Name, Status
   
   # 啟用 WoL（需要管理員權限）
   Set-NetAdapterAdvancedProperty -Name "Ethernet" -DisplayName "Wake on Magic Packet" -DisplayValue "Enabled"
   ```

3. **檢查防火牆**
   ```powershell
   # 允許 WoL 端口（UDP 9）
   New-NetFirewallRule -DisplayName "WoL" -Direction Inbound -LocalPort 9 -Protocol UDP -Action Allow
   ```

### DeskIn 無法連接

1. 確認帳號密碼正確
2. 檢查設備是否在 DeskIn 應用程式中顯示
3. 確認網路連線正常

### 跨區網喚醒失敗

跨區網 WoL 需要：
1. 路由器支援並啟用定向廣播
2. 或使用 DeskIn 的雲端喚醒功能
3. 或在目標區網內設置 WoL 中繼服務

## 安全注意事項

- ⚠️ **不要將密碼明文存儲** - 使用環境變量或加密存儲
- ⚠️ **WoL 僅在區網內有效** - 跨區網需要額外配置
- ⚠️ **防火牆規則** - 確保 UDP 端口 9 開放

---

**Last Updated:** 2026-03-12
**Author:** Zarvis
