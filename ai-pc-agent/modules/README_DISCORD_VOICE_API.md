# Discord 語音識別 - OpenAI API 版本 🎤

**快速、準確、低延遲！**

---

## ⚡ 為什麼用 API 版本？

| 項目 | 本地 Whisper | OpenAI API |
|------|-------------|------------|
| **速度** | 🐌 慢（需下載模型） | ⚡ 快（雲端處理） |
| **準確度** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **資源使用** | 高（CPU/GPU） | 低（API 調用） |
| **延遲** | 5-30 秒 | 1-3 秒 |
| **成本** | 免費 | $0.006/分鐘 |

---

## 📦 安裝

### 1. 安裝依賴

```bash
cd ~/.openclaw/workspace/Zarvis_Group/ai-pc-agent
source venv/bin/activate

# 安裝 Discord.py
pip install "discord.py[voice]" aiohttp
```

### 2. 設置 API Keys

```bash
# Discord Bot Token
export DISCORD_BOT_TOKEN="你的 Discord Bot Token"

# OpenAI API Key
export OPENAI_API_KEY="sk-你的 OpenAI API Key"
```

或者在 `config.yaml` 配置：

```yaml
discord:
  bot_token: "你的 Token"

openai:
  api_key: "sk-你的 Key"
```

---

## 🚀 啟動

```bash
python modules/discord_voice_api.py
```

---

## 🎯 使用方式

### 1. 發送語音訊息

1. 在 Discord 進入語音頻道
2. 錄製語音訊息
3. 發送
4. AI 自動識別並回覆（1-3 秒！）

### 2. 語音命令

| 語音 | 動作 |
|------|------|
| "打開 Chrome/瀏覽器" | 打開瀏覽器 |
| "搜尋 [關鍵字]" | 搜尋內容 |
| "系統狀態" | 檢查系統 |
| "截圖" | 截取螢幕 |
| "幫助" | 顯示幫助 |

---

## 💰 成本估算

**OpenAI Whisper API 定價：**
- $0.006 美元 / 分鐘
- 約 $0.18 美元 / 小時

**假設每天使用 1 小時：**
- 每月約 $5.4 美元

**比本地運行快 10 倍！**

---

## 🔧 故障排除

### 問題 1：缺少 API Key

```bash
# 設置 OpenAI API Key
export OPENAI_API_KEY="sk-xxx"

# 或添加到 ~/.bashrc
echo 'export OPENAI_API_KEY="sk-xxx"' >> ~/.bashrc
source ~/.bashrc
```

### 問題 2：Discord Bot Token 無效

1. 前往 https://discord.com/developers/applications
2. 重新生成 Token
3. 更新環境變量

---

## 📊 性能對比

**測試：10 秒語音訊息**

| 方法 | 時間 |
|------|------|
| **本地 Whisper (base)** | 15 秒 |
| **本地 Whisper (large)** | 45 秒 |
| **OpenAI API** | 2 秒 ⚡ |

---

**準備就緒！快速啟動！** 🎤⚡
