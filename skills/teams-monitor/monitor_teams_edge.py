#!/usr/bin/env python3
"""
Teams 訊息讀取器 - Windows 版本
通過 Playwright 連接已登入的 Edge 瀏覽器

使用前請確保：
1. 已在 Edge 登入 Teams
2. Edge 允許遠程調試
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

# 配置
OUTPUT_FILE = Path(__file__).parent / "teams_messages.json"
TEAMS_URL = "https://teams.microsoft.com/"

class TeamsEdgeMonitor:
    def __init__(self):
        self.last_message_id = None
        self.messages = []
        
    async def load_existing_messages(self):
        """載入已處理的訊息記錄"""
        if OUTPUT_FILE.exists():
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.last_message_id = data.get("last_message_id")
                self.messages = data.get("messages", [])[-100:]
    
    async def save_message(self, message: dict):
        """保存訊息"""
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
        
        print(f"💾 訊息已保存：{message.get('sender', 'Unknown')} - {message.get('text', '')[:50]}")
    
    async def connect_to_edge(self):
        """連接到已開啟的 Edge 瀏覽器"""
        print("🔍 嘗試連接 Edge 瀏覽器...")
        
        # Edge 的調試端口預設是 9222
        # 需要先啟動 Edge 時添加 --remote-debugging-port=9222
        
        try:
            # 方法 1：連接到現有的 Edge 實例
            browser = await async_playwright().start()
            
            # 嘗試連接
            edge_browser = await browser.chromium.connect_over_cdp(
                "http://localhost:9222",
                timeout=10000
            )
            
            print("✅ 成功連接到 Edge！")
            return edge_browser
            
        except Exception as e:
            print(f"❌ 連接 Edge 失敗：{e}")
            print("\n💡 請先啟動 Edge 時添加遠程調試端口:")
            print('   msedge.exe --remote-debugging-port=9222')
            return None
    
    async def extract_messages_from_page(self, page):
        """從 Teams 頁面提取訊息"""
        messages = []
        
        try:
            # 等待 Teams 載入
            await page.wait_for_load_state("networkidle", timeout=30000)
            print("✅ Teams 頁面已載入")
            
            # 等待訊息區域
            try:
                await page.wait_for_selector("div[data-message-id], [role='listitem']", timeout=5000)
            except:
                print("⚠️ 未找到訊息元素，可能不在聊天視圖")
                return messages
            
            # 獲取所有訊息元素
            message_elements = await page.query_selector_all(
                "div[data-message-id]"
            )
            
            print(f"📊 找到 {len(message_elements)} 則訊息")
            
            # 提取最近 20 則訊息
            for elem in message_elements[-20:]:
                try:
                    msg_id = await elem.get_attribute("data-message-id")
                    if not msg_id:
                        continue
                    
                    # 提取發送者
                    sender_elem = await elem.query_selector("span[title]")
                    sender = await sender_elem.inner_text() if sender_elem else "Unknown"
                    
                    # 提取內容
                    content_elem = await elem.query_selector("div[contenteditable='false']")
                    content = await content_elem.inner_text() if content_elem else ""
                    
                    # 提取時間
                    time_elem = await elem.query_selector("time")
                    timestamp = await time_elem.get_attribute("datetime") if time_elem else datetime.now().isoformat()
                    
                    messages.append({
                        "id": msg_id,
                        "sender": sender.strip(),
                        "text": content.strip(),
                        "timestamp": timestamp
                    })
                    
                except Exception as e:
                    print(f"提取訊息失敗：{e}")
                    continue
        
        except Exception as e:
            print(f"頁面提取失敗：{e}")
        
        return messages
    
    async def monitor(self):
        """主監控循環"""
        print("🚀 Teams 監控啟動")
        print(f"   輸出文件：{OUTPUT_FILE}")
        print("")
        
        await self.load_existing_messages()
        
        while True:
            try:
                # 嘗試連接 Edge
                browser = await self.connect_to_edge()
                
                if browser:
                    # 獲取第一個分頁
                    context = browser.contexts[0]
                    pages = context.pages
                    
                    # 尋找 Teams 分頁
                    teams_page = None
                    for page in pages:
                        if "teams.microsoft.com" in page.url:
                            teams_page = page
                            break
                    
                    if teams_page:
                        print(f"📍 Teams 分頁：{teams_page.url}")
                        
                        # 提取訊息
                        messages = await self.extract_messages_from_page(teams_page)
                        
                        # 處理新訊息
                        for msg in reversed(messages):
                            if msg["id"] != self.last_message_id:
                                print(f"\n📨 新訊息！")
                                print(f"   發送者：{msg.get('sender', 'Unknown')}")
                                print(f"   內容：{msg.get('text', '')[:100]}")
                                
                                await self.save_message(msg)
                                self.last_message_id = msg["id"]
                    else:
                        print("⚠️ 未找到 Teams 分頁，請在 Edge 中開啟 Teams")
                    
                    await browser.close()
                else:
                    print("⚠️ 無法連接 Edge，請確認已啟動遠程調試")
                
            except Exception as e:
                print(f"❌ 監控錯誤：{e}")
            
            # 每 30 秒檢查一次
            print("\n⏳ 等待 30 秒後再次檢查...")
            await asyncio.sleep(30)


async def main():
    monitor = TeamsEdgeMonitor()
    await monitor.monitor()


if __name__ == "__main__":
    asyncio.run(main())
