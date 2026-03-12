#!/usr/bin/env python3
"""
Teams 網頁版監控腳本
使用 Playwright 監控 Teams 網頁版新訊息

依賴:
    pip install playwright
    playwright install chromium
"""

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

# 配置
TEAMS_URL = "https://teams.microsoft.com/"
CHECK_INTERVAL = 30  # 秒
OUTPUT_FILE = Path(__file__).parent / "teams_messages.json"
DISCORD_WEBHOOK = ""  # 可選：Discord Webhook URL

class TeamsMonitor:
    def __init__(self, email: str = None):
        self.email = email
        self.last_message_id = None
        self.messages = []
        
    async def load_existing_messages(self):
        """載入已處理的訊息記錄"""
        if OUTPUT_FILE.exists():
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.last_message_id = data.get("last_message_id")
                self.messages = data.get("messages", [])[-100:]  # 保留最近 100 則
    
    async def save_message(self, message: dict):
        """保存訊息到記錄"""
        self.messages.append(message)
        if len(self.messages) > 100:
            self.messages = self.messages[-100:]
        
        data = {
            "last_message_id": self.last_message_id,
            "last_updated": datetime.now().isoformat(),
            "messages": self.messages
        }
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    async def send_to_discord(self, message: dict):
        """轉發到 Discord（可選）"""
        if not DISCORD_WEBHOOK:
            return
        
        try:
            import requests
            content = f"**{message.get('sender', 'Unknown')}**: {message.get('text', '')}"
            requests.post(DISCORD_WEBHOOK, json={"content": content})
        except Exception as e:
            print(f"Discord 轉發失敗：{e}")
    
    async def monitor_teams(self, browser):
        """監控 Teams 頁面"""
        print("🔍 連接 Teams...")
        
        # 使用持久化上下文（保持登入狀態）
        context = await browser.new_context(
            storage_state=None,  # 首次需要手動登入
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        
        page = await context.new_page()
        
        # 導航到 Teams
        await page.goto(TEAMS_URL, wait_until="networkidle", timeout=60000)
        print("✅ Teams 頁面已載入")
        
        # 等待登入（首次需要手動）
        print("⏳ 等待登入...（首次使用需要手動登入）")
        await page.wait_for_timeout(10000)
        
        # 主監控循環
        while True:
            try:
                # 嘗試獲取新訊息
                messages = await self.extract_messages(page)
                
                for msg in messages:
                    if msg["id"] != self.last_message_id:
                        print(f"\n📨 新訊息！")
                        print(f"   發送者：{msg.get('sender', 'Unknown')}")
                        print(f"   內容：{msg.get('text', '')[:100]}")
                        print(f"   時間：{msg.get('timestamp', 'Unknown')}")
                        
                        # 保存並轉發
                        await self.save_message(msg)
                        await self.send_to_discord(msg)
                        
                        self.last_message_id = msg["id"]
                
            except Exception as e:
                print(f"❌ 提取訊息失敗：{e}")
            
            await asyncio.sleep(CHECK_INTERVAL)
    
    async def extract_messages(self, page):
        """從 Teams 頁面提取訊息"""
        messages = []
        
        try:
            # Teams 訊息選擇器（可能需要根據實際 DOM 調整）
            message_elements = await page.query_selector_all(
                "div[data-message-id], [role='listitem']"
            )
            
            for elem in message_elements[-10:]:  # 最近 10 則
                try:
                    msg_id = await elem.get_attribute("data-message-id")
                    if not msg_id:
                        continue
                    
                    # 提取發送者
                    sender_elem = await elem.query_selector(
                        "span[title], .message-sender"
                    )
                    sender = await sender_elem.inner_text() if sender_elem else "Unknown"
                    
                    # 提取內容
                    content_elem = await elem.query_selector(
                        "div[contenteditable='false'], .message-content"
                    )
                    content = await content_elem.inner_text() if content_elem else ""
                    
                    # 提取時間
                    time_elem = await elem.query_selector(
                        "time, .message-timestamp"
                    )
                    timestamp = await time_elem.get_attribute("datetime") if time_elem else datetime.now().isoformat()
                    
                    messages.append({
                        "id": msg_id,
                        "sender": sender.strip(),
                        "text": content.strip(),
                        "timestamp": timestamp
                    })
                    
                except Exception as e:
                    print(f"提取單則訊息失敗：{e}")
                    continue
        
        except Exception as e:
            print(f"查詢訊息失敗：{e}")
        
        return messages


async def main():
    print("🚀 Teams 網頁版監控啟動")
    print(f"   監控間隔：{CHECK_INTERVAL}秒")
    print(f"   記錄文件：{OUTPUT_FILE}")
    print("")
    
    monitor = TeamsMonitor()
    await monitor.load_existing_messages()
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,  # 顯示瀏覽器（首次需要手動登入）
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox"
            ]
        )
        
        try:
            await monitor.monitor_teams(browser)
        except KeyboardInterrupt:
            print("\n👋 監控已停止")
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
