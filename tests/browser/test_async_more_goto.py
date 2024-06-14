from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
import asyncio
from common.core import config
from common.func import calculate_time

async def create_default_async_context(url=''):
    asp = async_playwright()
    async with asp as ap:
        browser1 = await ap.chromium.launch_persistent_context(
            channel='msedge',
            user_data_dir=config['data']['user']['dir'],
            headless=False
        )
        page = browser1.pages[0]
        page2 = await browser1.new_page()
        page3 = await browser1.new_page()
        await asyncio.gather(
            page.goto('https://www.google.com/'),
            page2.goto('https://www.bing.com/'),
            page3.goto('https://www.baidu.com/')
        )
        await browser1.close()


async  def with_goto_page():
    asp = async_playwright()
    async with asp as ap:
        browser1 = await ap.chromium.launch_persistent_context(
            channel='msedge',
            user_data_dir=config['data']['user']['dir'],
            headless=False
        )
        page = browser1.pages[0]
        page2 = await browser1.new_page()
        page3 = await browser1.new_page()
        await asyncio.gather(
            goto_page(page2),
            goto_page(page3)
        )
        await browser1.close()

def test_goto_page():
    asyncio.run(with_goto_page())


async def goto_page(page):
    await page.goto("https://www.baidu.com")
