# -*- coding: utf-8 -*-
from urllib.parse import urlparse
import pytest
import requests
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
from common.config import config
import asyncio

@pytest.mark.parametrize("url", ["https://zhuanlan.zhihu.com/api/articles/drafts"])
def test_valid_url(url):
    result = urlparse(url)
    print()
    print(result)
    print(result.scheme)
    return all([result.scheme, result.netloc])


@pytest.mark.parametrize("url",
                         ["https://zhuanlan.zhihu.com/api/articles/drafts"
                          ])
def test_request_post(url):
    response = requests.post(url, data={
        "content": "test content",
        "del_time": "0",
        "table_of_contents": "false"
    }, headers={
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        "credentials": "include",
        "content-type": "application/json",
        "x-requested-with": "fetch",
        "x-xsrftoken": "4c454b91-6f84-490b-96c7-1c1a73c0c762",
        "x-zst-81": "3_2.0aR_sne90QR2VMhnyT6Sm2JLBkhnun820XM20cL_1kwxYUqwT16P0EiUZST2x-LOmwhp1tD_I-JOfgGXTzJO1ADRZ0cHsTJXII820Eer0c4nVDJH8zGCBADwMuukRe8tKIAtqS_L1VufXQ6P0mRPCyDQMovNYEgSCPRP0E4rZUrN9DDom3hnynAUMnAVPF_PhaueTFTLOLqOsDGtynqCqoexL6LVfTgg1svXB609fSMtfNUgCzcLMEULOtgwpYbeTVeHGjq9MkUemEDoVgUCfJiCLZcOfFvxYbDgm0JVf8vSM6vSqfT2L_hVqe8x8Nh30M6NKOJOm8UpLrbLy-JNCLBe0bipm0bXf88LMOgg8cePs0CL_dUY0Og_zoBSLbHxYnreqjCVYN92XcwCMpCSBBwSLfUHBNCwOwwOqBbrqkH3KOBLfzDXO0U90oipstC3mYuYMeqr9BrOKAvwB_JXOyhx0ywOskhNOp7c0Q7OLQ8ws"
    })
    print(response.text)
    pass


def test_persisted_cookies():
    """
    测试知乎的上传内容功能
    :return:
    """
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            channel=config['default']['browser'],
            headless=False,
            user_data_dir=config['data']['user']['dir'],
            no_viewport=True,
            args=['--start-maximized'],
            devtools=True
        )
        page = browser.new_page()
        page.goto("https://zhuanlan.zhihu.com/write")
        resp = page.request.fetch(
            "https://zhuanlan.zhihu.com/api/articles/drafts",
            method="POST",
            data={
                "content": "test content66666666666666",
                "del_time": "0",
                "table_of_contents": "false"
            },
            headers={
                "credentials": "include",
                "content-type": "application/json",
                "x-requested-with": "fetch",
                "x-xsrftoken": "4c454b91-6f84-490b-96c7-1c1a73c0c762",
                "x-zst-81": "3_2.0aR_sne90QR2VMhnyT6Sm2JLBkhnun820XM20cL_1kwxYUqwT16P0EiUZST2x-LOmwhp1tD_I-JOfgGXTzJO1ADRZ0cHsTJXII820Eer0c4nVDJH8zGCBADwMuukRe8tKIAtqS_L1VufXQ6P0mRPCyDQMovNYEgSCPRP0E4rZUrN9DDom3hnynAUMnAVPF_PhaueTFTLOLqOsDGtynqCqoexL6LVfTgg1svXB609fSMtfNUgCzcLMEULOtgwpYbeTVeHGjq9MkUemEDoVgUCfJiCLZcOfFvxYbDgm0JVf8vSM6vSqfT2L_hVqe8x8Nh30M6NKOJOm8UpLrbLy-JNCLBe0bipm0bXf88LMOgg8cePs0CL_dUY0Og_zoBSLbHxYnreqjCVYN92XcwCMpCSBBwSLfUHBNCwOwwOqBbrqkH3KOBLfzDXO0U90oipstC3mYuYMeqr9BrOKAvwB_JXOyhx0ywOskhNOp7c0Q7OLQ8ws"
            },
            ignore_https_errors=True
        )
        print(resp.body())


async def test_persisted_cookies_async(browser,ap):
    """
    测试知乎的上传请求功能
    :return:
    """
    page = await browser.new_page()
    await page.goto("https://zhuanlan.zhihu.com/write")
    resp = await page.request.fetch(
        "https://zhuanlan.zhihu.com/api/articles/drafts",
        method="POST",
        data={
            "content": "test content66666666666666",
            "del_time": "0",
            "table_of_contents": "false"
        },
        headers={
            "credentials": "include",
            "content-type": "application/json",
            "x-requested-with": "fetch",
            "x-xsrftoken": "4c454b91-6f84-490b-96c7-1c1a73c0c762",
            "x-zst-81": "3_2.0aR_sne90QR2VMhnyT6Sm2JLBkhnun820XM20cL_1kwxYUqwT16P0EiUZST2x-LOmwhp1tD_I-JOfgGXTzJO1ADRZ0cHsTJXII820Eer0c4nVDJH8zGCBADwMuukRe8tKIAtqS_L1VufXQ6P0mRPCyDQMovNYEgSCPRP0E4rZUrN9DDom3hnynAUMnAVPF_PhaueTFTLOLqOsDGtynqCqoexL6LVfTgg1svXB609fSMtfNUgCzcLMEULOtgwpYbeTVeHGjq9MkUemEDoVgUCfJiCLZcOfFvxYbDgm0JVf8vSM6vSqfT2L_hVqe8x8Nh30M6NKOJOm8UpLrbLy-JNCLBe0bipm0bXf88LMOgg8cePs0CL_dUY0Og_zoBSLbHxYnreqjCVYN92XcwCMpCSBBwSLfUHBNCwOwwOqBbrqkH3KOBLfzDXO0U90oipstC3mYuYMeqr9BrOKAvwB_JXOyhx0ywOskhNOp7c0Q7OLQ8ws"
        },
        ignore_https_errors=True
    )
    print(await resp.body())
    await ap.__aexit__(None, None, None)

@pytest.mark.asyncio
async def test_persisted_much_async():
    tasks = []
    ap = async_playwright()
    p = await ap.start()
    browser = await p.chromium.launch_persistent_context(
        channel=config['default']['browser'],
        headless=False,
        user_data_dir=config['data']['user']['dir'],
        no_viewport=True,
        args=['--start-maximized'],
        devtools=True
    )
    tasks.append(test_persisted_cookies_async(browser,ap))
    await asyncio.gather(*tasks)
    pass