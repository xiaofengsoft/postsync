from playwright.async_api import async_playwright
from typing import Dict, List
import asyncio
import json


class AsyncPageGroupManager:
    def __init__(self):
        self.page_groups: Dict[str, List] = {}
        self.playwright = None
        self.browser = None
        self.context = None

    async def create_page_group(self, group_id: str):
        if group_id in self.page_groups:
            raise ValueError(f"Page group with id '{
                             group_id}' already exists.")
        self.page_groups[group_id] = []

    async def add_page_to_group(self, group_id: str, page):
        if group_id not in self.page_groups:
            raise ValueError(f"Page group with id '{
                             group_id}' does not exist.")
        self.page_groups[group_id].append(page)

    async def get_pages_in_group(self, group_id: str) -> List:
        return self.page_groups.get(group_id, [])

    async def close_page_group(self, group_id: str):
        if group_id in self.page_groups:
            for page in self.page_groups[group_id]:
                if not page.is_closed():  # 检查页面是否已关闭
                    await page.close()
            del self.page_groups[group_id]

    async def close_all(self):
        for group_id in list(self.page_groups.keys()):
            await self.close_page_group(group_id)
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()


# 全局共享的页面组管理器实例
global_manager = AsyncPageGroupManager()


async def open_pages():
    # 初始化 Playwright 资源
    global_manager.playwright = await async_playwright().start()
    global_manager.browser = await global_manager.playwright.chromium.launch(headless=False)
    global_manager.context = await global_manager.browser.new_context()

    # 创建页面组并添加页面
    await global_manager.create_page_group("group1")
    page1 = await global_manager.context.new_page()
    await global_manager.add_page_to_group("group1", page1)
    await page1.goto("https://example.com", wait_until="load")  # 确保页面加载完成
    print(f"Opened page: {await page1.title()}")

    # 模拟设置一些 cookies 或本地存储
    await page1.evaluate("() => localStorage.setItem('key', 'value')")
    await page1.context.add_cookies([{
        "name": "test_cookie",
        "value": "12345",
        "url": "https://example.com"
    }])
    print("Added cookies and localStorage to page1")


async def save_context_state():
    # 等待一段时间，确保页面已经打开并设置了 cookies/localStorage
    await asyncio.sleep(5)

    # 保存上下文的状态（cookies 和 localStorage）
    if global_manager.context:
        storage_state = await global_manager.context.storage_state(path="state.json")
        print("Context state saved to state.json")
        print(json.dumps(storage_state, indent=2))  # 打印保存的状态

    # 关闭页面组和 Playwright 资源
    await global_manager.close_page_group("group1")
    await global_manager.close_all()


async def main():
    # 并行执行打开页面和保存上下文状态的任务
    open_task = asyncio.create_task(open_pages())
    save_task = asyncio.create_task(save_context_state())

    # 等待两个任务完成
    await asyncio.gather(open_task, save_task)

# 运行异步代码
asyncio.run(main())
