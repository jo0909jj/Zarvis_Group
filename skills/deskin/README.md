# DeskIn 遠程控制技能 🖥️

通過 DeskIn 遠程桌面軟體控制遠程電腦，支援 Wake-on-LAN 喚醒、遠程連接等功能。

## 📋 功能

- 🔌 **Wake-on-LAN** - 遠程喚醒關機中的電腦
- 🖥️ **設備狀態檢查** - 查看設備在線狀態
- 💻 **遠程桌面整合** - 與 DeskIn 應用程式配合使用
- 🎨 **ComfyUI 整合** - 喚醒後自動呼叫 ComfyUI 生圖

## 🚀 快速開始

### 1. 取得設備 MAC 地址

**在目標電腦（JOESPC）上執行：**

```powershell
# Windows PowerShell
ipconfig /all
# 找到「實體地址」或「Physical Address」

# 或
getmac /v
```

記錄 MAC 地址，格式如：`00:1A:2B:3C:4D:5E`

### 2. 配置 DeskIn

**在目標電腦上：**

1. 安裝並登入 DeskIn
2. 記錄設備名稱（例如：`JOESPC`）
3. 啟用 Wake-on-LAN 功能（在 DeskIn 設定中）

**BIOS 設定（重要！）：**

重啟電腦進入 BIOS，確保啟用：
- `Wake-on-LAN`
- `Power On By PCI-E`
- `ERP Ready` = Disabled

### 3. 配置技能

```bash
cd ~/.openclaw/workspace/skills/deskin

# 複製配置範本
cp config.env.example config.env

# 編輯配置文件
nano config.env
```

修改以下內容：
```bash
DESKIN_DEVICE_NAME="JOESPC"
DESKIN_DEVICE_MAC="00:1A:2B:3C:4D:5E"  # 替換為實際 MAC
DESKIN_DEVICE_IP="192.168.1.100"       # 替換為實際 IP
```

### 4. 測試喚醒

```bash
# 測試 WoL 發送
python3 scripts/wol.py --mac "00:1A:2B:3C:4D:5E"

# 或使用整合腳本
bash scripts/wake_pc.sh JOESPC
```

## 📖 使用說明

### 喚醒單一設備

```bash
# 基本用法
bash scripts/wake_pc.sh JOESPC

# 指定超時時間（120 秒）和檢查間隔（5 秒）
bash scripts/wake_pc.sh JOESPC 120 5
```

### 發送 WoL 封包

```bash
# 基本 WoL
python3 scripts/wol.py --mac "00:1A:2B:3C:4D:5E"

# 指定廣播 IP 和端口
python3 scripts/wol.py \
    --mac "00:1A:2B:3C:4D:5E" \
    --ip "192.168.1.255" \
    --port 9

# 發送多次（提高成功率）
python3 scripts/wol.py \
    --mac "00:1A:2B:3C:4D:5E" \
    --count 5 \
    --interval 2
```

### 完整工作流程（喚醒 + 生圖）

```bash
#!/bin/bash
# 喚醒 JOESPC 並生成圖片

DEVICE="JOESPC"
PROMPT="A beautiful landscape"

echo "🔌 喚醒 $DEVICE..."
bash scripts/wake_pc.sh "$DEVICE"

echo "⏳ 等待電腦啟動..."
sleep 30

echo "🎨 生成圖片..."
bash ../comfyui/scripts/generate_image.sh "$PROMPT"

echo "✅ 完成！"
```

## 🔧 故障排除

### 電腦無法喚醒

**1. 檢查 BIOS 設定**
- 重啟進入 BIOS/UEFI
- 啟用 `Wake-on-LAN` 或 `Power On By PCI-E`
- 禁用 `Deep Sleep` 或 `ERP Ready`

**2. 檢查 Windows 網卡設定**

```powershell
# 管理員 PowerShell
# 查看網卡進階設定
Get-NetAdapterAdvancedProperty -Name "Ethernet"

# 啟用 WoL
Set-NetAdapterAdvancedProperty -Name "Ethernet" -DisplayName "Wake on Magic Packet" -DisplayValue "Enabled"

# 允許網卡喚醒電腦
powercfg /devicequery wake_armed
```

**3. 檢查防火牆**

```powershell
# 允許 WoL 端口（UDP 9）
New-NetFirewallRule -DisplayName "WoL" -Direction Inbound -LocalPort 9 -Protocol UDP -Action Allow
```

**4. 測試區網連通性**

```bash
# 從 WSL2 ping 測試
ping 192.168.1.100

# 如果 ping 不通，檢查網路設定
```

### DeskIn 連接問題

1. **確認帳號登入** - 在 DeskIn App 中確認設備在線
2. **檢查網路** - 確保兩台電腦在同一區網
3. **重啟 DeskIn 服務** - 在目標電腦重啟 DeskIn

### 跨區網喚醒

WoL 預設只能在區網內運作。跨區網需要：

1. **路由器設定** - 啟用定向廣播（Directed Broadcast）
2. **WoL 中繼** - 在區網內設置中繼服務
3. **DeskIn 雲端喚醒** - 使用 DeskIn 的雲端喚醒功能（如有）

## 📁 文件結構

```
deskin/
├── SKILL.md                  # 技能說明
├── README.md                 # 使用指南
├── config.env.example        # 配置範本
└── scripts/
    ├── wol.py                # WoL 發送腳本
    ├── wake_pc.sh            # 喚醒整合腳本
    └── check_status.py       # 設備狀態檢查（TODO）
```

## 🔗 與 ComfyUI 整合

喚醒電腦後自動呼叫 ComfyUI：

```bash
# 配置環境變量
export COMFYUI_HOST="192.168.1.100"
export COMFYUI_PORT="8188"

# 喚醒並生圖
bash scripts/wake_pc.sh JOESPC
sleep 30
bash ../comfyui/scripts/generate_image.sh "A cat"
```

## ⚠️ 安全注意事項

- **不要提交 config.env** - 包含敏感資訊
- **使用 App Token** - 如果支援，使用 App Token 而非密碼
- **區網限制** - WoL 僅在區網內有效

## 📝 取得 MAC 地址範例

**Windows:**
```
C:\> ipconfig /all

乙太網路卡 乙太網路:

   實體地址. . . . . . . . . : 00-1A-2B-3C-4D-5E
```

**Linux:**
```bash
$ ip link show
2: eth0: <BROADCAST,MULTICAST,UP> ...
    link/ether 00:1a:2b:3c:4d:5e ...
```

---

**Last Updated:** 2026-03-12
**Author:** Zarvis
