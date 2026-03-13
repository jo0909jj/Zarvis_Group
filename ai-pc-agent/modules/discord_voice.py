#!/usr/bin/env python3
"""
Discord 語音識別模組
讓 AI 能夠聽懂 Discord 語音訊息並回覆
"""

import discord
from discord.ext import commands
import tempfile
from pathlib import Path
from typing import Optional
import subprocess


class DiscordVoiceRecognizer:
    """Discord 語音識別器"""
    
    def __init__(self, whisper_model: str = "base"):
        """
        初始化
        
        Args:
            whisper_model: Whisper 模型 (tiny, base, small, medium, large)
        """
        self.whisper_model = whisper_model
        self._whisper_available = self._check_whisper()
    
    def _check_whisper(self) -> bool:
        """檢查 Whisper 是否已安裝"""
        try:
            import whisper
            return True
        except ImportError:
            print("⚠️ Whisper 未安裝，請執行：pip install openai-whisper")
            return False
    
    def transcribe_audio_file(self, audio_path: str) -> Optional[str]:
        """
        識別音頻文件
        
        Args:
            audio_path: 音頻文件路徑（支持 mp3, wav, webm, m4a）
            
        Returns:
            識別的文字
        """
        if not self._whisper_available:
            return None
        
        try:
            import whisper
            
            # 載入模型
            model = whisper.load_model(self.whisper_model)
            
            # 識別（支援多種格式）
            result = model.transcribe(audio_path, language="zh-TW".split("-")[0])
            
            return result["text"].strip()
            
        except Exception as e:
            print(f"❌ 識別失敗：{e}")
            return None
    
    async def process_voice_message(self, attachment_url: str) -> Optional[str]:
        """
        處理 Discord 語音訊息附件
        
        Args:
            attachment_url: 附件 URL
            
        Returns:
            識別的文字
        """
        import aiohttp
        import io
        
        try:
            # 下載語音文件
            async with aiohttp.ClientSession() as session:
                async with session.get(attachment_url) as response:
                    if response.status != 200:
                        print(f"❌ 下載失敗：{response.status}")
                        return None
                    
                    # 保存到臨時文件
                    with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as f:
                        temp_path = f.name
                        f.write(await response.read())
                    
                    # 識別
                    text = self.transcribe_audio_file(temp_path)
                    
                    # 清理
                    Path(temp_path).unlink()
                    
                    return text
                    
        except Exception as e:
            print(f"❌ 處理語音訊息失敗：{e}")
            return None


class DiscordVoiceBot(commands.Bot):
    """Discord 語音機器人"""
    
    def __init__(self, prefix: str = "!"):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        
        super().__init__(command_prefix=prefix, intents=intents)
        self.voice_recognizer = DiscordVoiceRecognizer()
    
    async def on_ready(self):
        """機器人就緒"""
        print(f"✅ {self.user} 已登入")
        print(f"📊 在 {len(self.guilds)} 個伺服器")
    
    async def on_message(self, message: discord.Message):
        """處理訊息"""
        # 忽略自己的訊息
        if message.author == self.user:
            return
        
        # 檢查是否有語音附件
        for attachment in message.attachments:
            if attachment.content_type and 'audio' in attachment.content_type:
                print(f"🎤 收到語音訊息 from {message.author}")
                
                # 識別語音
                text = await self.voice_recognizer.process_voice_message(attachment.url)
                
                if text:
                    print(f"📝 識別結果：{text}")
                    
                    # 回覆
                    await message.channel.send(f"🎤 你說的是：**{text}**")
                    
                    # 處理命令
                    await self.process_voice_command(message, text)
        
        # 處理一般訊息
        await self.process_commands(message)
    
    async def process_voice_command(self, message: discord.Message, text: str):
        """
        處理語音命令
        
        Args:
            message: 原始訊息
            text: 識別的文字
        """
        text_lower = text.lower()
        
        # 打開應用程式
        if "打開" in text_lower or "開啟" in text_lower:
            if "chrome" in text_lower or "瀏覽器" in text_lower:
                await message.channel.send("🌐 正在打開 Chrome...")
                # 這裡可以添加實際的打開邏輯
        
        # 搜尋
        elif "搜尋" in text_lower or "搜索" in text_lower:
            await message.channel.send("🔍 正在搜尋...")
        
        # 系統狀態
        elif "系統" in text_lower or "狀態" in text_lower:
            await message.channel.send("📊 正在檢查系統狀態...")
        
        # 幫助
        elif "幫助" in text_lower or "help" in text_lower:
            help_text = """
🎤 **語音命令幫助**

我可以識別你的語音訊息並執行以下命令：

**基本命令：**
- "打開 Chrome/瀏覽器" - 打開瀏覽器
- "搜尋 [關鍵字]" - 搜尋內容
- "系統狀態" - 檢查系統狀態
- "截圖" - 截取螢幕
- "幫助" - 顯示這個幫助訊息

**使用方式：**
1. 在語音頻道說話並錄製
2. 發送語音訊息
3. 我會自動識別並回覆
"""
            await message.channel.send(help_text)


def main():
    """主函數"""
    import os
    
    # 從環境變量獲取 token
    token = os.getenv("DISCORD_BOT_TOKEN")
    
    if not token:
        print("❌ 請設置 DISCORD_BOT_TOKEN 環境變量")
        print("   在 Discord Developer Portal 獲取：https://discord.com/developers/applications")
        return
    
    # 創建機器人
    bot = DiscordVoiceBot(prefix="!")
    
    # 運行
    print("🚀 啟動 Discord 語音機器人...")
    bot.run(token)


if __name__ == "__main__":
    main()
