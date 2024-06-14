import unittest
from playwright.sync_api import sync_playwright as sync_pw
from common.core import config

class TestEdgeStart(unittest.TestCase):

    def test_edge_start(self):
        with sync_pw() as p:
            browser = p.chromium.launch(channel='msedge',headless=False)
            page = browser.new_page()
            page.goto('https://www.google.com/')
            print(page.title())
            browser.close()

    def test_have_ran_edge(self):
        """
        测试是否可以连接到已启动的Edge浏览器
        :return:
        """
        with sync_pw() as p:
            browser = p.chromium.connect("ws://localhost:9225")

            page = browser.new_page()
            page.goto('https://www.google.com/')
            print(page.title())
            # browser.close()

    def test_start_async_edge(self):
        import asyncio
        from playwright.async_api import async_playwright, Playwright

        async def run(playwright: Playwright):
            chromium = playwright.chromium  # or "firefox" or "webkit".
            browser = await chromium.launch_persistent_context(
                user_data_dir=config['data']['user']['dir'],
                headless=False,
                channel='msedge'
            )
            async def new_page(b):
                page = await b.new_page()
                await page.goto("https://www.baidu.com")
            await new_page(browser)
            await new_page(browser)
            # other actions...
            # await browser.close()

        async def main():
            async with async_playwright() as playwright:
                await run(playwright)

        asyncio.run(main())
        asyncio.run(main())