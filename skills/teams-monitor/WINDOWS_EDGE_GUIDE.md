# Teams 監控 - Windows Edge 連接指南 🎯

## 📋 方案說明

由於你已經在 **Windows Edge** 登入 Teams，我們通過 Playwright 連接現有的 Edge 瀏覽器來讀取訊息。

---

## 🚀 使用步驟

### 步驟 1：在 Windows 上準備 Edge

**1. 關閉所有 Edge 視窗**

**2. 以遠程調試模式啟動 Edge**

按 `Win + R`，輸入：

```
msedge.exe --remote-debugging-port=9222 --user-data-dir="C:\EdgeDebug"
```

或創建快捷方式：
1. 右鍵 Edge 快捷方式 → 內容
2. 在「目標」後面添加：
   ```
   --remote-debugging-port=9222 --user-data-dir="C:\EdgeDebug"
   ```

**3. 登入 Teams**
- 在新開啟的 Edge 中訪問 https://teams.microsoft.com/
- 登入你的公司帳號
- 進入想要監控的聊天或頻道

---

### 步驟 2：在 WSL2 執行監控腳本

```bash
cd ~/.openclaw/workspace/skills/teams-monitor

# 安裝依賴（如果還沒安裝）
pip install playwright
playwright install chromium

# 執行 Edge 連接腳本
python monitor_teams_edge.py
```

---

### 步驟 3：查看訊息

監控腳本會保存訊息到：
```
~/.openclaw/workspace/skills/teams-monitor/teams_messages.json
```

查看最新訊息：
```bash
cat teams_messages.json | jq '.messages[-1]'
```

---

## 🔧 故障排除

### 問題：無法連接 Edge

**錯誤訊息：**
```
❌ 連接 Edge 失敗: TimeoutError
```

**解決方法：**

1. **確認 Edge 已啟動遠程調試**
   ```
   msedge.exe --remote-debugging-port=9222
   ```

2. **檢查端口是否開放**
   ```bash
   # 在 WSL2 測試
   curl http://localhost:9222/json
   ```

3. **Windows 防火牆允許**
   ```powershell
   # 管理員 PowerShell
   New-NetFirewallRule -DisplayName "Edge Debug" -Direction Inbound -LocalPort 9222 -Protocol TCP -Action Allow
   ```

---

### 問題：找不到 Teams 分頁

**錯誤訊息：**
```
⚠️ 未找到 Teams 分頁，請在 Edge 中開啟 Teams
```

**解決：**
在 Edge 中手動開啟 https://teams.microsoft.com/ 並登入

---

### 問題：訊息提取失敗

**可能原因：**
- Teams DOM 結構改變
- 不在聊天視圖

**解決：**
1. 確保在聊天或頻道視圖（不是日曆、檔案等）
2. 更新選擇器（需要修改腳本）

---

## 💡 簡化方案：使用通知轉發

如果上述方法太複雜，可以使用更簡單的通知轉發：

### 方案 A：使用 Pushbullet

**1. 安裝 Pushbullet（Windows + 手機）**

**2. 設定 Teams 通知轉發**

**3. OpenClaw 讀取 Pushbullet API**

### 方案 B：使用 Windows 通知監聽

創建 PowerShell 腳本監聽通知：

```powershell
# save_teams_notifications.ps1
# 監聽 Teams 通知並保存到文件

$outputFile = "C:\temp\teams_notifications.json"

# 使用 Windows 通知 API 監聽
# ...（需要額外開發）
```

---

## 📁 輸出格式

`teams_messages.json` 範例：

```json
{
  "last_message_id": "1234567890",
  "last_updated": "2026-03-12T15:30:00",
  "messages": [
    {
      "id": "1234567890",
      "sender": "John Doe",
      "text": "下午 3 點開會",
      "timestamp": "2026-03-12T15:00:00"
    }
  ]
}
```

---

## 🔗 整合 OpenClaw

在 OpenClaw 中讀取訊息：

```python
import json
from pathlib import Path

def get_latest_teams_message():
    path = Path("~/.openclaw/workspace/skills/teams-monitor/teams_messages.json").expanduser()
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if data['messages']:
                return data['messages'][-1]
    return None

# 使用
msg = get_latest_teams_message()
if msg:
    print(f"Teams: {msg['sender']} - {msg['text']}")
```

---

## ⚠️ 注意事項

1. **公司政策** - 確認允許自動化監控
2. **隱私** - 不要監控敏感訊息
3. **Edge 必須保持開啟** - 關閉後需要重新啟動
4. **WSL2 需要能訪問 localhost** - 確認網路配置

---

## 📝 快速測試

**Windows（PowerShell）：**
```powershell
# 啟動 Edge 遠程調試
msedge.exe --remote-debugging-port=9222 --user-data-dir="C:\EdgeDebug"
```

**WSL2：**
```bash
# 測試連接
curl http://localhost:9222/json

# 執行監控
cd ~/.openclaw/workspace/skills/teams-monitor
python monitor_teams_edge.py
```

---

**完成！** 🎉

現在 OpenClaw 可以讀取 Teams 訊息了！
