# Discord 語音識別整合 🎤

讓 AI 能夠聽懂 Discord 語音訊息並自動回覆！

---

## 🎯 功能

**你可以：**
1. 在 Discord 發送語音訊息
2. AI 自動識別成文字
3. AI 理解並回覆
4. 支援語音命令

**例如：**
```
你：[發送語音訊息] "幫我搜尋今天的新聞"
AI：🔍 正在搜尋... [執行搜尋並回覆結果]
```

---

## 📦 安裝

### 1. 安裝依賴

```bash
cd ~/.openclaw/workspace/Zarvis_Group/ai-pc-agent
source venv/bin/activate

# 安裝 Whisper（語音識別）
pip install openai-whisper

# 安裝 Discord.py（語音支援）
pip install "discord.py[voice]"

# 安裝 aiohttp（下載語音文件）
pip install aiohttp
```

### 2. 系統依賴（WSL2/Linux）

```bash
sudo apt-get update
sudo apt-get install -y \
    ffmpeg \
    libnacl-dev \
    python3-dev \
    portaudio19-dev
```

---

## 🔑 Discord Bot 設置

### 1. 創建 Discord 應用

1. 前往 https://discord.com/developers/applications
2. 點擊 "New Application"
3. 輸入名稱（例如：AI Voice Bot）

### 2. 創建 Bot

1. 左側選單選擇 "Bot"
2. 點擊 "Add Bot"
3. 點擊 "Reset Token" 獲取 Token
4. **保存 Token（只顯示一次）**

### 3. 設置權限

在 "Bot" 頁面，啟用：
- ✅ Message Content Intent
- ✅ Voice Channel Permissions

### 4. 邀請 Bot 到伺服器

1. 左側選單 "OAuth2" → "URL Generator"
2. 選擇 scopes：
   - ✅ `bot`
3. 選擇 permissions：
   - ✅ `Send Messages`
   - ✅ `Attach Files`
   - ✅ `Use Voice Activity`
4. 複製生成的 URL
5. 在瀏覽器打開並邀請到伺服器

---

## ⚙️ 配置

### 方法 1：環境變量

```bash
export DISCORD_BOT_TOKEN="你的 Bot Token"
```

### 方法 2：配置文件

編輯 `config.yaml`：

```yaml
discord:
  enabled: true
  bot_token: "你的 Bot Token"
  voice:
    enabled: true
    whisper_model: "base"
    language: "zh-TW"
```

---

## 🚀 啟動

### 測試模式

```bash
python modules/discord_voice.py
```

### 生產模式（整合到 AI PC Agent）

```bash
# 添加到 AI PC Agent 核心
python scripts/run_agent.py --enable-voice
```

---

## 🎤 使用方式

### 1. 語音訊息識別

**步驟：**
1. 在 Discord 進入語音頻道
2. 按住說話或語音活動錄製
3. 發送語音訊息
4. AI 自動識別並回覆

**範例：**
```
你：[語音] "今天天氣如何"
AI：📝 識別結果：今天天氣如何
   🌤️ 正在查詢天氣...
```

### 2. 語音命令

**支援的命令：**

| 語音 | 動作 |
|------|------|
| "打開 Chrome/瀏覽器" | 打開瀏覽器 |
| "搜尋 [關鍵字]" | 搜尋內容 |
| "系統狀態" | 檢查系統 |
| "截圖" | 截取螢幕 |
| "幫助" | 顯示幫助 |

---

## 📊 工作流程

```
Discord 語音訊息
    ↓
下載語音文件（webm/m4a）
    ↓
Whisper 識別成文字
    ↓
AI 理解文字內容
    ↓
執行命令或回覆
    ↓
發送到 Discord
```

---

## 🔧 故障排除

### 問題 1：Whisper 安裝失敗

```bash
# 使用 pip 安裝
pip install --upgrade pip
pip install openai-whisper

# 或使用 conda
conda install -c conda-forge openai-whisper
```

### 問題 2：Discord.py 語音失敗

```bash
# 重新安裝語音依賴
pip uninstall discord.py
pip install "discord.py[voice]"
```

### 問題 3：ffmpeg 找不到

```bash
# WSL2/ Linux
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# 下載：https://ffmpeg.org/download.html
# 添加到 PATH
```

---

## 🎯 進階功能

### 自定義命令

編輯 `modules/discord_voice.py`：

```python
async def process_voice_command(self, message, text):
    # 添加自定義命令
    if "我的命令" in text.lower():
        # 執行你的邏輯
        await message.channel.send("執行完成！")
```

### 多語言支援

```yaml
voice:
  languages:
    - "zh-TW"  # 繁體中文
    - "en-US"  # 英文
    - "ja-JP"  # 日文
```

---

## 📝 測試清單

- [ ] Discord Bot 已創建
- [ ] Token 已設置
- [ ] Bot 已邀請到伺服器
- [ ] Whisper 已安裝
- [ ] 語音訊息可以識別
- [ ] 語音命令可以執行

---

**準備就緒！等待啟動！** 🎤📡
