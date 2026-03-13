# AI PC Agent - 快速測試指南 🧪

## 🚀 快速開始

### 1. 安裝依賴

```bash
cd ai-pc-agent

# 創建虛擬環境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安裝依賴
pip install -r requirements.txt

# 安裝 Playwright 瀏覽器
playwright install chromium
```

### 2. 測試系統監控

```bash
python modules/system_monitor.py
```

**預期輸出：**
```
============================================================
🖥️  系統監控報告
============================================================
📅 時間：2026-03-13T08:46:00
💻 系統：Linux 6.6.87.2-microsoft-standard-WSL2
🐍 Python: 3.12.3
⏱️  運行時間：0:00:01

📊 CPU: 12.5%
📊 記憶體：4.2/16.0 GB (26.3%)
📊 磁碟：120.5/500.0 GB (24.1%)
📊 網路：上傳 125.3 MB | 下載 890.2 MB

🔝 Top 5 程序:
   1. chrome (CPU: 5.2%, Mem: 8.1%)
   2. python (CPU: 2.1%, Mem: 3.5%)
   ...
============================================================
```

### 3. 測試命令執行

```bash
python agent/commands.py
```

**預期輸出：**
```
⚡ 命令執行器演示
============================================================

📍 任務 1: 獲取系統資訊
✅ Hello from AI PC Agent!

📍 任務 2: 列出當前目錄
   README.md
   requirements.txt
   ...

📍 任務 3: 創建測試文件
✅ 文件已創建：test_demo.txt

📍 任務 4: 測試安全性檢查
❌ 命令不被允許：sudo rm -rf /

============================================================
✅ 演示完成！
```

### 4. 測試瀏覽器自動化

```bash
python modules/browser_automation.py
```

**預期輸出：**
```
🌐 瀏覽器自動化演示
============================================================

📍 任務 1: 搜尋新聞
✅ 已截圖保存：screenshots/news_search.png

📍 任務 2: 導航到 GitHub
✅ 已截圖保存：screenshots/github.png

📍 任務 3: 提取頁面標題
📄 頁面標題：GitHub: Let's build from here

📍 任務 4: 提取前 5 個連結
   1. Product
   2. Solutions
   ...

============================================================
✅ 演示完成！
```

### 5. 啟動 Agent

```bash
python scripts/run_agent.py
```

### 6. 啟動 Web 儀表板（可選）

```bash
python web/dashboard.py
```

然後在瀏覽器打開：http://localhost:5000

---

## ⏰ Cron 自動更新

### 設置 Cron Job

```bash
# 編輯 crontab
crontab -e

# 添加（每 2 小時更新）：
0 */2 * * * cd /path/to/ai-pc-agent && bash scripts/cron_update.sh >> logs/cron.log 2>&1

# 添加（每天早上 8 點報告）：
0 8 * * * cd /path/to/ai-pc-agent && python modules/system_monitor.py >> logs/daily_report.txt 2>&1
```

### 驗證 Cron

```bash
# 查看已設置的 cron
crontab -l

# 查看日誌
tail -f logs/cron.log
```

---

## 📊 檢查清單

- [ ] Python 3.8+ 已安裝
- [ ] 依賴已安裝 (`pip install -r requirements.txt`)
- [ ] Playwright 瀏覽器已安裝
- [ ] 系統監控測試通過
- [ ] 命令執行測試通過
- [ ] 瀏覽器自動化測試通過
- [ ] Cron Job 已設置

---

## 🐛 常見問題

### 問題：ModuleNotFoundError

**解決：**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 問題：Playwright 瀏覽器無法啟動

**解決：**
```bash
playwright install chromium
playwright install-deps chromium  # Linux only
```

### 問題：Cron 不執行

**解決：**
```bash
# 檢查 cron 服務
sudo systemctl status cron

# 查看 cron 日誌
grep CRON /var/log/syslog
```

---

**Last Updated:** 2026-03-13
**Author:** Zarvis AI Assistant
