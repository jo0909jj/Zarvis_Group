# Teams 網頁版監控技能 📱

通過瀏覽器自動化監控 Teams 網頁版新訊息，並轉發到 OpenClaw 可讀取的頻道。

## 📋 需求

- Python 3.8+
- Playwright
- 已登入 Teams 的瀏覽器會話

## 🚀 快速開始

### 1. 安裝依賴

```bash
cd ~/.openclaw/workspace/skills/teams-monitor

# 安裝 Playwright
pip install playwright

# 安裝瀏覽器
playwright install chromium
```

### 2. 首次運行（手動登入）

```bash
python monitor_teams.py
```

**首次運行會：**
1. 打開瀏覽器
2. 導航到 teams.microsoft.com
3. **你需要手動登入 Teams**
4. 登入後腳本會自動開始監控

### 3. 配置（可選）

編輯 `monitor_teams.py`：

```python
CHECK_INTERVAL = 30  # 監控間隔（秒）
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/..."  # 轉發到 Discord
```

---

## 📖 使用說明

### 基本監控

```bash
python monitor_teams.py
```

輸出範例：
```
🚀 Teams 網頁版監控啟動
   監控間隔：30 秒
   記錄文件：teams_messages.json

🔍 連接 Teams...
✅ Teams 頁面已載入
⏳ 等待登入...

📨 新訊息！
   發送者：John Doe
   內容：下午 3 點開會別忘了
   時間：2026-03-12T15:00:00
```

### 背景運行

```bash
# 使用 nohup
nohup python monitor_teams.py > teams_monitor.log 2>&1 &

# 或使用 systemd（Linux）
sudo systemctl start teams-monitor
```

### 查看記錄

```bash
# 查看監控日誌
tail -f teams_monitor.log

# 查看訊息記錄
cat teams_messages.json | jq .
```

---

## 🔧 進階配置

### 1. 轉發到 Discord

```python
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/YOUR_WEBHOOK"
```

### 2. 轉發到 OpenClaw 工作區

修改 `save_message` 方法，寫入 OpenClaw 可讀取的文件：

```python
async def save_message(self, message: dict):
    # 寫入 OpenClaw 工作區
    output_path = Path("/home/joechiang/.openclaw/workspace/teams_inbox.md")
    with open(output_path, 'a', encoding='utf-8') as f:
        f.write(f"\n## {message['sender']} - {message['timestamp']}\n")
        f.write(f"{message['text']}\n")
        f.write("---\n")
```

### 3. 關鍵字過濾

只監控特定關鍵字：

```python
KEYWORDS = ["@我", "緊急", "重要"]

async def extract_messages(self, page):
    messages = await self._extract_messages_impl(page)
    
    # 過濾關鍵字
    filtered = []
    for msg in messages:
        if any(kw in msg['text'] for kw in KEYWORDS):
            filtered.append(msg)
    
    return filtered
```

---

## 📁 文件結構

```
teams-monitor/
├── monitor_teams.py        # 主監控腳本
├── README.md               # 使用說明
├── requirements.txt        # Python 依賴
└── teams_messages.json     # 訊息記錄（自動生成）
```

---

## 🔍 故障排除

### 問題：無法登入 Teams

**解決：**
1. 確保網路可以訪問 teams.microsoft.com
2. 檢查公司防火牆是否允許
3. 可能需要公司 VPN

### 問題：訊息提取失敗

**解決：**
Teams 的 DOM 結構可能改變，需要調整選擇器：

```python
# 在瀏覽器開發者工具檢查實際選擇器
# F12 → Elements → 找到訊息元素

# 修改 extract_messages 中的選擇器
message_elements = await page.query_selector_all(
    "div[data-message-id]"  # 替換為實際選擇器
)
```

### 問題：瀏覽器被偵測為自動化

**解決：**
添加更多隱身參數：

```python
browser = await p.chromium.launch(
    headless=False,
    args=[
        "--disable-blink-features=AutomationControlled",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-web-security"
    ]
)

# 添加隱身腳本
await page.add_init_script("""
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    });
""")
```

---

## 💡 整合 OpenClaw

### 方法 1：文件監控

讓 OpenClaw 監控 `teams_messages.json`：

```python
# 在 OpenClaw 心跳中檢查
import json
from pathlib import Path

def check_teams_messages():
    path = Path("~/.openclaw/workspace/skills/teams-monitor/teams_messages.json").expanduser()
    if path.exists():
        with open(path, 'r') as f:
            data = json.load(f)
            last_msg = data['messages'][-1]
            return f"Teams: {last_msg['sender']} - {last_msg['text']}"
```

### 方法 2：Discord 轉發

設定 Discord Webhook，OpenClaw 從 Discord 讀取：

```python
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/..."
# OpenClaw 監聽 Discord 頻道
```

### 方法 3：直接整合

在 OpenClaw 技能中添加 Teams 讀取功能：

```python
# ~/.openclaw/workspace/skills/teams-reader/SKILL.md
```

---

## ⚠️ 注意事項

- **公司政策** - 確認公司允許自動化監控
- **隱私** - 不要監控敏感訊息
- **登入會話** - 定期檢查登入狀態
- **資源使用** - 背景運行注意記憶體使用

---

## 📝 首次使用檢查清單

- [ ] 安裝 Python 3.8+
- [ ] 安裝 Playwright: `pip install playwright`
- [ ] 安裝瀏覽器：`playwright install chromium`
- [ ] 測試登入 Teams 網頁版
- [ ] 運行監控腳本
- [ ] 確認訊息提取正常
- [ ] （可選）配置 Discord 轉發

---

**Last Updated:** 2026-03-12
**Author:** Zarvis
