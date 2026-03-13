#!/usr/bin/env python3
"""
瀏覽器自動化模組
基於 Playwright
"""

import asyncio
from pathlib import Path
from datetime import datetime
from playwright.async_api import async_playwright


class BrowserAutomation:
    """瀏覽器自動化"""
    
    def __init__(self, headless=False, timeout=30000):
        self.headless = headless
        self.timeout = timeout
        self.browser = None
        self.context = None
        self.page = None
    
    async def start(self):
        """啟動瀏覽器"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=self.headless,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        self.page = await self.context.new_page()
        return self
    
    async def navigate(self, url: str):
        """導航到 URL"""
        await self.page.goto(url, wait_until='networkidle', timeout=self.timeout)
        return self
    
    async def search(self, query: str, engine='google'):
        """搜尋"""
        if engine == 'google':
            await self.navigate(f"https://www.google.com/search?q={query}")
        elif engine == 'bing':
            await self.navigate(f"https://www.bing.com/search?q={query}")
        return self
    
    async def click(self, selector: str):
        """點擊元素"""
        await self.page.click(selector)
        await self.page.wait_for_load_state('networkidle')
        return self
    
    async def type(self, selector: str, text: str):
        """輸入文字"""
        await self.page.fill(selector, text)
        return self
    
    async def screenshot(self, filename: str = None, full_page=False):
        """截圖"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        output_path = Path("screenshots") / filename
        output_path.parent.mkdir(exist_ok=True)
        
        await self.page.screenshot(
            path=str(output_path),
            full_page=full_page
        )
        return str(output_path)
    
    async def get_content(self, selector: str = None):
        """獲取內容"""
        if selector:
            element = await self.page.query_selector(selector)
            return await element.inner_text() if element else None
        else:
            return await self.page.content()
    
    async def extract_links(self):
        """提取所有連結"""
        links = await self.page.evaluate("""
            () => {
                return Array.from(document.querySelectorAll('a'))
                    .map(a => ({
                        text: a.innerText,
                        href: a.href
                    }))
                    .filter(link => link.text && link.href);
            }
        """)
        return links
    
    async def wait(self, seconds: float):
        """等待"""
        await asyncio.sleep(seconds)
        return self
    
    async def close(self):
        """關閉瀏覽器"""
        if self.browser:
            await self.browser.close()
    
    async def __aenter__(self):
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


async def demo():
    """演示"""
    print("🌐 瀏覽器自動化演示")
    print("=" * 60)
    
    async with BrowserAutomation(headless=False) as browser:
        # 演示 1：搜尋
        print("\n📍 任務 1: 搜尋新聞")
        await browser.search("今天的新聞")
        await browser.screenshot("news_search.png")
        print("✅ 已截圖保存：news_search.png")
        
        # 演示 2：導航
        print("\n📍 任務 2: 導航到 GitHub")
        await browser.navigate("https://github.com")
        await browser.wait(2)
        await browser.screenshot("github.png")
        print("✅ 已截圖保存：github.png")
        
        # 演示 3：提取內容
        print("\n📍 任務 3: 提取頁面標題")
        title = await browser.get_content("title")
        print(f"📄 頁面標題：{title}")
        
        # 演示 4：提取連結
        print("\n📍 任務 4: 提取前 5 個連結")
        links = await browser.extract_links()
        for i, link in enumerate(links[:5], 1):
            print(f"   {i}. {link['text'][:50]}...")
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！")


if __name__ == "__main__":
    asyncio.run(demo())
