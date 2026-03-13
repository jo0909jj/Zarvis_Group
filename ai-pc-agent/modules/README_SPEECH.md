# 語音識別模組 - Speech Recognition 🎤

使用 OpenAI Whisper 進行語音轉文字

---

## 📦 安裝

```bash
cd ~/.openclaw/workspace/Zarvis_Group/ai-pc-agent
source venv/bin/activate

# 安裝 Whisper
pip install openai-whisper

# 安裝 PyAudio (錄音用)
pip install pyaudio

# Linux/WSL2 可能需要系統依賴
sudo apt-get install portaudio19-dev python3-pyaudio
```

---

## 🎯 功能

### 1. 語音轉文字
```python
from modules.speech_recognition import SpeechRecognizer

recognizer = SpeechRecognizer()

# 從文件識別
text = recognizer.transcribe_audio("recording.wav")

# 從麥克風錄音並識別
text = recognizer.listen_and_transcribe()
```

### 2. 語音命令
```python
# 識別語音命令
command = recognizer.recognize_command("打開 Chrome")
# 返回：{"action": "open_app", "app": "chrome"}
```

---

## 🔧 配置

編輯 `config.yaml`：

```yaml
speech:
  enabled: true
  model: "base"  # tiny, base, small, medium, large
  language: "zh-TW"  # 語言
  device: "cpu"  # cpu 或 cuda
```

---

## 📝 使用範例

### 範例 1：語音輸入
```python
from modules.speech_recognition import SpeechRecognizer

recognizer = SpeechRecognizer()

print("請說話...")
text = recognizer.listen_and_transcribe(duration=5)
print(f"你說了：{text}")
```

### 範例 2：語音命令
```python
# 語音控制電腦
command = recognizer.recognize_command("幫我打開 Chrome 並搜尋今天的新聞")

if command['action'] == 'open_app':
    subprocess.Popen(['google-chrome', command['url']])
```

---

## 🎤 模型選擇

| 模型 | 大小 | 速度 | 準確度 | 推薦用途 |
|------|------|------|--------|----------|
| **tiny** | 39M | ⚡⚡⚡ | ⭐⭐ | 快速測試 |
| **base** | 74M | ⚡⚡ | ⭐⭐⭐ | 一般用途 |
| **small** | 244M | ⚡ | ⭐⭐⭐⭐ | 高準確度 |
| **medium** | 769M | 🐌 | ⭐⭐⭐⭐⭐ | 生產環境 |
| **large** | 1550M | 🐌🐌 | ⭐⭐⭐⭐⭐ | 最佳效果 |

---

## 🚀 整合到 AI PC Agent

### 添加到 `agent/core.py`：

```python
from modules.speech_recognition import SpeechRecognizer

class Agent:
    def __init__(self):
        self.speech = SpeechRecognizer()
    
    def process_voice_command(self):
        """處理語音命令"""
        text = self.speech.listen_and_transcribe()
        return self.process_text_command(text)
```

---

## 📊 狀態檢查

```bash
# 測試 Whisper 安裝
python -c "import whisper; print(whisper.__version__)"

# 測試麥克風
python -c "import pyaudio; print('PyAudio OK')"
```

---

**準備就緒！等待安裝！** 🎤📡
