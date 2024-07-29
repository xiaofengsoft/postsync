# -*- coding: utf-8 -*-
import asyncio
import re

from playwright._impl._async_base import AsyncEventContextManager
from playwright.async_api import FileChooser

from common.core import config
from common.func import get_file_dir
from entity.community import Community
from bs4 import BeautifulSoup
import os
import json

class Wechat(Community):
    url_post_new = "https://mp.weixin.qq.com/"
    site_name = "公众号"

    def __init__(self, browser, ap, asp):

        super().__init__(browser, ap, asp)
        self.pic_nums = 0  # 正在处理的图片数量
        self.origin_src = None

    async def async_post_new(self, title: str, digest: str, content: str, file_path: str = None, tags: list = None,
                             category: str = None, cover: str = None, columns: list = None, topic: str = None) -> str:
        await self.page.goto(Wechat.url_post_new)
        await self.page.locator("#app > div.main_bd_new > div:nth-child(3) > div.weui-desktop-panel__bd > div > div:nth-child(2)").click()
        await self.page.locator("#js_import_file").click()
        async with self.page.expect_file_chooser() as fc_info:
            await self.page.locator("#rt_rt_1i3u1b8ne5e4112mc4srb11qt11 > label").click()
        file_chooser = await fc_info.value
        file_chooser.set_files(file_path)

        return file_chooser



