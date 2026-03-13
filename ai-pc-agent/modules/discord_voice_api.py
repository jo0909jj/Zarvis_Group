#!/usr/bin/env python3
"""
Discord 語音識別 - OpenAI API 版本 🎤
使用 OpenAI Whisper API 進行快速語音識別
"""

import discord
from discord.ext import commands
import aiohttp
import tempfile
import subprocess
import os
from pathlib import Path


class DiscordVoiceBot(commands.Bot):
    """Discord 語音機器人（OpenAI API）"""
    
    def __init__(self, prefix: str = "!"):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        
        super().__init__(command_prefix=prefix, intents=intents)
    
    async def on_ready(self):
        """機器人就緒"""
        print(f"✅ {self.user} 已登入")
        print(f"📊 在 {len(self.guilds)} 個伺服器")
        print("🎤 等待語音訊息...")
    
    async def on_message(self, message: discord.Message):
        """處理訊息"""
        # 忽略自己的訊息
        if message.author == self.user:
            return
        
        # 檢查是否有語音附件
        for attachment in message.attachments:
            if attachment.content_type and 'audio' in attachment.content_type:
                print(f"🎤 收到語音訊息 from {message.author}")
                
                # 識別語音（使用 OpenAI API）
                text = await self.transcribe_with_openai(attachment.url)
                
                if text:
                    print(f"📝 識別結果：{text}")
                    
                    # 回覆
                    await message.channel.send(f"🎤 你說的是：**{text}**")
                    
                    # 處理命令
                    await self.process_voice_command(message, text)
        
        # 處理一般訊息
        await self.process_commands(message)
    
    async def transcribe_with_openai(self, audio_url: str) -> str:
        """
        使用 OpenAI Whisper API 識別語音
        
        Args:
            audio_url: 音頻文件 URL
            
        Returns:
            識別的文字
        """
        try:
            # 下載音頻文件
            async with aiohttp.ClientSession() as session:
                async with session.get(audio_url) as response:
                    if response.status != 200:
                        print(f"❌ 下載失敗：{response.status}")
                        return None
                    
                    # 保存到臨時文件
                    file_ext = audio_url.split('.')[-1].split('?')[0] or 'webm'
                    with tempfile.NamedTemporaryFile(suffix=f'.{file_ext}', delete=False) as f:
                        temp_path = f.name
                        f.write(await response.read())
                    
                    # 使用 OpenAI Whisper API 腳本識別
                    result = subprocess.run(
                        [
                            'bash',
                            '~/.npm-global/lib/node_modules/openclaw/skills/openai-whisper-api/scripts/transcribe.sh',
                            temp_path
                        ],
                        capture_output=True,
                        text=True,
                        env={**os.environ, 'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY', '')}
                    )
                    
                    # 清理臨時文件
                    Path(temp_path).unlink()
                    
                    if result.returncode == 0:
                        # 讀取識別結果
                        output_file = result.stdout.strip()
                        with open(output_file, 'r', encoding='utf-8') as f:
                            text = f.read().strip()
                        return text
                    else:
                        print(f"❌ 識別失敗：{result.stderr}")
                        return None
                        
        except Exception as e:
            print(f"❌ 處理語音訊息失敗：{e}")
            return None
    
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
3. 我會自動識別並回覆（使用 OpenAI API，速度快！）
"""
            await message.channel.send(help_text)


def main():
    """主函數"""
    # 從環境變量獲取 token
    token = os.getenv("DISCORD_BOT_TOKEN")
    
    if not token:
        print("❌ 請設置 DISCORD_BOT_TOKEN 環境變量")
        print("   在 Discord Developer Portal 獲取：https://discord.com/developers/applications")
        return
    
    # 檢查 OpenAI API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ 請設置 OPENAI_API_KEY 環境變量")
        print("   在 https://platform.openai.com/api-keys 獲取")
        return
    
    # 創建機器人
    bot = DiscordVoiceBot(prefix="!")
    
    # 運行
    print("🚀 啟動 Discord 語音機器人（OpenAI API）...")
    bot.run(token)


if __name__ == "__main__":
    main()
