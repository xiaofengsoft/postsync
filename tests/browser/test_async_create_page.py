from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
import asyncio
from common.core import config
from common.func import calculate_time
import time


async def create_more_than_one_browser():
    """
    测试创建多个浏览器上下文
    :return:
    """
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


@calculate_time
def test_async_create_more_than_one_browser():
    """
    测试创建多个浏览器上下文
    :return:
    """
    asyncio.run(create_more_than_one_browser())


def create_more_than_one_browser_sync():
    """
    测试同步创建多个浏览器上下文
    :return:
    """
    sp = sync_playwright()
    with sp as p:
        browser1 = p.chromium.launch_persistent_context(
            channel='msedge',
            user_data_dir=config['data']['user']['dir'],
            headless=False
        )
        page = browser1.pages[0]
        page2 = browser1.new_page()
        page3 = browser1.new_page()
        page.goto('https://www.google.com/')
        page2.goto('https://www.bing.com/')
        page3.goto('https://www.baidu.com/')
        browser1.close()


@calculate_time
def test_sync_create_more_than_one_browser():
    create_more_than_one_browser_sync()


def test_async_page_goto():
    async def run():
        asp = async_playwright()
        async with asp as ap:
            browser = await ap.chromium.launch_persistent_context(
                channel='msedge',
                user_data_dir=config['data']['user']['dir'],
                headless=False
            )
            page = await browser.new_page()
            await page.goto("https://baidu.com")
            # other actions...
            await browser.close()
    asyncio.run(run())
