#!/usr/bin/env python3
"""
語音識別模組
使用 OpenAI Whisper 進行語音轉文字
"""

import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Dict


class SpeechRecognizer:
    """語音識別器"""
    
    def __init__(self, model: str = "base", language: str = "zh-TW", device: str = "cpu"):
        """
        初始化語音識別器
        
        Args:
            model: Whisper 模型 (tiny, base, small, medium, large)
            language: 語言代碼
            device: 運行設備 (cpu 或 cuda)
        """
        self.model = model
        self.language = language
        self.device = device
        self._whisper_available = self._check_whisper()
    
    def _check_whisper(self) -> bool:
        """檢查 Whisper 是否已安裝"""
        try:
            import whisper
            return True
        except ImportError:
            print("⚠️ Whisper 未安裝，請執行：pip install openai-whisper")
            return False
    
    def transcribe_audio(self, audio_path: str) -> Optional[str]:
        """
        識別音頻文件
        
        Args:
            audio_path: 音頻文件路徑
            
        Returns:
            識別的文字，失敗返回 None
        """
        if not self._whisper_available:
            return None
        
        try:
            import whisper
            
            # 載入模型
            model = whisper.load_model(self.model)
            
            # 識別
            result = model.transcribe(
                audio_path,
                language=self.language.split("-")[0] if self.language else None
            )
            
            return result["text"].strip()
            
        except Exception as e:
            print(f"❌ 識別失敗：{e}")
            return None
    
    def listen_and_transcribe(self, duration: int = 5, device_index: int = None) -> Optional[str]:
        """
        從麥克風錄音並識別
        
        Args:
            duration: 錄音時長（秒）
            device_index: 麥克風設備索引
            
        Returns:
            識別的文字，失敗返回 None
        """
        if not self._whisper_available:
            return None
        
        try:
            import pyaudio
            import wave
            
            # 錄音參數
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 16000
            
            # 初始化 PyAudio
            p = pyaudio.PyAudio()
            
            # 選擇設備
            if device_index is None:
                device_index = p.get_default_input_device_info()['index']
            
            print(f"🎤 開始錄音 {duration} 秒...")
            
            # 開始錄音
            stream = p.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=CHUNK
            )
            
            frames = []
            for _ in range(0, int(RATE / CHUNK * duration)):
                data = stream.read(CHUNK)
                frames.append(data)
            
            print("✅ 錄音完成，正在識別...")
            
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            # 保存為 WAV 文件
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
                temp_path = f.name
                
                wf = wave.open(temp_path, 'wb')
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
                wf.close()
                
                # 識別
                text = self.transcribe_audio(temp_path)
                
                # 清理臨時文件
                Path(temp_path).unlink()
                
                return text
                
        except ImportError as e:
            print(f"❌ 缺少依賴：{e}")
            print("   請執行：pip install pyaudio")
            return None
        except Exception as e:
            print(f"❌ 錄音失敗：{e}")
            return None
    
    def recognize_command(self, text: str) -> Dict:
        """
        識別語音命令
        
        Args:
            text: 語音轉文字的內容
            
        Returns:
            命令字典 {action, params}
        """
        text = text.lower()
        
        # 打開應用程式
        if "打開" in text or "開啟" in text:
            if "chrome" in text or "瀏覽器" in text:
                return {"action": "open_app", "app": "chrome"}
            elif "記事本" in text:
                return {"action": "open_app", "app": "notepad"}
            elif "終端" in text or "terminal" in text:
                return {"action": "open_app", "app": "terminal"}
        
        # 搜尋
        if "搜尋" in text or "搜索" in text:
            # 提取搜尋關鍵字
            keywords = text.replace("搜尋", "").replace("搜索", "").strip()
            return {"action": "search", "query": keywords}
        
        # 截圖
        if "截圖" in text:
            return {"action": "screenshot"}
        
        # 系統狀態
        if "系統狀態" in text or "系統檢查" in text:
            return {"action": "system_status"}
        
        # 預設
        return {"action": "unknown", "text": text}


def demo():
    """演示"""
    print("🎤 語音識別演示")
    print("=" * 60)
    
    recognizer = SpeechRecognizer(model="base")
    
    if not recognizer._whisper_available:
        print("\n❌ Whisper 未安裝")
        print("   請執行：pip install openai-whisper")
        return
    
    print("\n✅ Whisper 已就緒")
    print("\n請選擇測試模式:")
    print("1. 從文件識別")
    print("2. 從麥克風錄音")
    print("3. 測試語音命令")
    
    choice = input("\n選擇 (1/2/3): ").strip()
    
    if choice == "1":
        audio_path = input("輸入音頻文件路徑: ").strip()
        text = recognizer.transcribe_audio(audio_path)
        print(f"\n識別結果：{text}")
        
    elif choice == "2":
        duration = int(input("錄音時長（秒）: ").strip() or "5")
        text = recognizer.listen_and_transcribe(duration=duration)
        print(f"\n識別結果：{text}")
        
    elif choice == "3":
        print("\n測試語音命令識別:")
        test_commands = [
            "幫我打開 Chrome",
            "搜尋今天的新聞",
            "截圖",
            "檢查系統狀態"
        ]
        
        for cmd in test_commands:
            result = recognizer.recognize_command(cmd)
            print(f"   '{cmd}' → {result}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    demo()
