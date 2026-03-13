# AI PC Agent 🤖

**AI 驅動的個人電腦控制代理** - 通過自然語言控制你的電腦

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Enabled-green.svg)](https://openclaw.ai)

---

## 🎯 專案目標

創建一個**完全由 AI 控制的個人電腦代理**，能夠：

- 🗣️ **理解自然語言指令**
- ⚡ **自動執行系統命令**
- 🌐 **控制瀏覽器自動化**
- 📊 **實時監控系統狀態**
- 📁 **管理文件和資料夾**
- 🔔 **發送完成通知**

---

## ✨ 核心功能

### 1. 命令執行引擎
```python
# AI 理解指令並執行
"打開 Chrome 並搜尋今天的新聞" 
→ 啟動 Chrome
→ 導航到 Google
→ 執行搜尋
→ 截圖回傳
```

### 2. 瀏覽器自動化
- 打開網頁
- 填寫表單
- 點擊按鈕
- 截取網頁
- 提取數據

### 3. 系統監控
- CPU/記憶體/磁碟使用率
- 網路流量監控
- 程序列表
- 系統日誌

### 4. 文件管理
- 上傳/下載文件
- 整理資料夾
- 搜尋文件
- 批量處理

### 5. 智能通知
- Discord 通知
- Telegram 通知
- Email 報告
- 定時提醒

---

## 🏗️ 專案架構

```
ai-pc-agent/
├── README.md                      # 本文件
├── requirements.txt               # Python 依賴
├── config.yaml                    # 配置文件
│
├── agent/                         # AI 核心
│   ├── __init__.py
│   ├── core.py                   # AI 核心邏輯
│   ├── commands.py               # 命令執行器
│   ├── parser.py                 # 自然語言解析
│   └── context.py                # 上下文管理
│
├── modules/                       # 功能模組
│   ├── __init__.py
│   ├── system_monitor.py         # 系統監控
│   ├── browser_automation.py     # 瀏覽器自動化
│   ├── file_manager.py           # 文件管理
│   ├── screenshot.py             # 截圖功能
│   └── notification.py           # 通知系統
│
├── web/                           # Web 介面
│   ├── __init__.py
│   ├── dashboard.py              # Flask 儀表板
│   ├── api.py                    # REST API
│   └── templates/
│       ├── index.html
│       └── monitor.html
│
├── scripts/                       # 腳本工具
│   ├── setup.sh                  # 安裝腳本
│   ├── run_agent.py              # 啟動代理
│   ├── cron_update.sh            # Cron 更新腳本
│   └── demo_tasks.py             # 演示任務
│
├── demos/                         # 演示案例
│   ├── demo1_open_app.md
│   ├── demo2_browse_web.md
│   ├── demo3_system_report.md
│   └── demo4_auto_task.md
│
├── tests/                         # 測試
│   ├── test_commands.py
│   ├── test_browser.py
│   └── test_monitor.py
│
└── logs/                          # 日誌
    └── agent.log
```

---

## 🚀 快速開始

### 1. 安裝依賴

```bash
# 克隆倉庫
git clone https://github.com/jo0909jj/Zarvis_Group.git
cd Zarvis_Group/ai-pc-agent

# 安裝 Python 依賴
pip install -r requirements.txt

# 安裝 Playwright
playwright install chromium
```

### 2. 配置

編輯 `config.yaml`：

```yaml
agent:
  name: "AI PC Agent"
  version: "1.0.0"
  
browser:
  headless: false
  timeout: 30000

notification:
  discord_webhook: ""
  telegram_bot: ""

monitor:
  interval: 60  # 秒
  log_file: "logs/agent.log"
```

### 3. 運行

```bash
# 啟動代理
python scripts/run_agent.py

# 或啟動 Web 儀表板
python web/dashboard.py
```

---

## 💡 使用範例

### 範例 1：打開應用程式

```python
from agent.core import Agent

agent = Agent()
agent.execute("打開記事本")
agent.execute("打開 Chrome 瀏覽器")
```

### 範例 2：瀏覽器自動化

```python
from modules.browser_automation import Browser

browser = Browser()
browser.navigate("https://google.com")
browser.search("今天的新聞")
browser.screenshot("news.png")
```

### 範例 3：系統監控

```python
from modules.system_monitor import SystemMonitor

monitor = SystemMonitor()
report = monitor.get_report()
print(f"CPU: {report['cpu']}%")
print(f"Memory: {report['memory']}%")
print(f"Disk: {report['disk']}%")
```

### 範例 4：自然語言指令

```python
# AI 理解並執行複雜指令
agent.execute("幫我搜尋今天的科技新聞，然後截圖保存")
# → 打開瀏覽器
# → 搜尋「科技新聞」
# → 截取網頁
# → 保存到文件夾
```

---

## 📊 演示案例

### Demo 1：自動生成系統報告

```bash
python scripts/demo_tasks.py system_report
```

**輸出：**
- CPU/記憶體/磁碟使用率
- 已安裝程序列表
- 系統啟動時間
- 網路狀態
- 生成 PDF 報告

### Demo 2：自動新聞摘要

```bash
python scripts/demo_tasks.py news_summary
```

**輸出：**
- 抓取熱門新聞網站
- AI 摘要重點
- 生成簡報
- 發送到 Discord

### Demo 3：文件整理

```bash
python scripts/demo_tasks.py organize_files ~/Downloads
```

**輸出：**
- 掃描下載文件夾
- 按類型分類（圖片/文檔/影片）
- 移動到對應文件夾
- 生成整理報告

---

## 🔧 進階配置

### Cron 定時任務

編輯 crontab：

```bash
crontab -e
```

添加：

```cron
# 每小時更新系統狀態
0 * * * * cd /path/to/ai-pc-agent && bash scripts/cron_update.sh

# 每天早上 8 點生成報告
0 8 * * * python /path/to/ai-pc-agent/scripts/demo_tasks.py daily_report

# 每 30 分鐘監控系統
*/30 * * * * python /path/to/ai-pc-agent/modules/system_monitor.py --log
```

### Discord 整合

1. 創建 Discord Webhook
2. 在 `config.yaml` 配置：

```yaml
notification:
  discord_webhook: "https://discord.com/api/webhooks/..."
```

3. 啟用通知：

```python
from modules.notification import Notification

notif = Notification()
notif.send_discord("系統報告已生成", file="report.pdf")
```

---

## 📝 API 文檔

### Agent Core

```python
class Agent:
    def execute(self, command: str) -> dict
    def get_status(self) -> dict
    def stop(self)
```

### Browser Automation

```python
class Browser:
    def navigate(self, url: str)
    def search(self, query: str)
    def click(self, selector: str)
    def type(self, selector: str, text: str)
    def screenshot(self, filename: str)
    def get_content(self) -> str
```

### System Monitor

```python
class SystemMonitor:
    def get_cpu_usage(self) -> float
    def get_memory_usage(self) -> float
    def get_disk_usage(self) -> dict
    def get_network_stats(self) -> dict
    def get_report(self) -> dict
```

---

## 🧪 測試

```bash
# 運行所有測試
pytest tests/

# 運行特定測試
pytest tests/test_commands.py -v

# 測試覆蓋率
pytest --cov=agent tests/
```

---

## 🤝 貢獻指南

1. Fork 倉庫
2. 創建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

---

## 📄 授權

MIT License - 詳見 [LICENSE](LICENSE) 文件

---

## 📬 聯絡

- **GitHub Issues**: [提交問題](https://github.com/jo0909jj/Zarvis_Group/issues)
- **Discord**: [加入社群](https://discord.gg/...)
- **Email**: agent@example.com

---

## 🌟 特色亮點

- ✅ **自然語言控制** - 像跟人說話一樣控制電腦
- ✅ **跨平台支援** - Windows/Linux/macOS
- ✅ **模組化設計** - 輕鬆擴充功能
- ✅ **即時監控** - 隨時掌握系統狀態
- ✅ **自動化工作流** - 解放你的雙手
- ✅ **開源免費** - 完全免費使用

---

**Made with ❤️ by Zarvis AI Assistant**

*Last Updated: 2026-03-13*
