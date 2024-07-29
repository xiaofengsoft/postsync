# -*- coding: utf-8 -*-
import asyncio
import re

from playwright._impl._async_base import AsyncEventContextManager
from playwright.async_api import FileChooser
import pyperclip
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
        self.origin_src = None

    async def async_post_new(self, title: str, digest: str, content: str, file_path: str = None, tags: list = None,
                             category: str = None, cover: str = None, columns: list = None, topic: str = None) -> str:

        await self.page.goto(Wechat.url_post_new)
        async with self.browser.expect_page() as new_page:
            await self.page.locator("#app > div.main_bd_new > div:nth-child(3) > div.weui-desktop-panel__bd > div > div:nth-child(2)").click()
        self.page = await new_page.value
        await self.page.get_by_role("listitem", name="文档导入").click()
        async with self.page.expect_file_chooser() as fc_info:
            await self.page.locator('#js_import_file_container label').click()
        file_chooser = await fc_info.value
        async with self.page.expect_response("https://mp.weixin.qq.com/advanced/mplog?action**") as response_info:
            await file_chooser.set_files(file_path.replace('.html','.docx'))
        response = await response_info.value
        # 填写作者
        await self.page.locator("#author").fill(config['default']['author'])
        # 上传封面
        # TODO 这里有问题
        async with self.page.expect_file_chooser() as fc_info:
            await self.page.locator("#js_cover_area").click()
            await self.page.locator("#js_cover_null > ul > li:nth-child(2) > a").click()
            await self.page.locator("#vue_app label").nth(1).click()
        file_chooser = await fc_info.value
        async with self.page.expect_response("https://mp.weixin.qq.com/cgi-bin/filetransfer?action=upload**") as response_info:
            await file_chooser.set_files(cover)
        await self.page.locator("#js_image_dialog_list_wrp > div > div:nth-child(1) > i").click()
        await self.page.locator("#vue_app > div:nth-child(3) > div.weui-desktop-dialog__wrp.weui-desktop-dialog_img-picker.weui-desktop-dialog_img-picker-with-crop > div > div.weui-desktop-dialog__ft > div:nth-child(1) > button").click()
        await self.page.locator("#vue_app > div:nth-child(3) > div.weui-desktop-dialog__wrp.weui-desktop-dialog_img-picker.weui-desktop-dialog_img-picker-with-crop > div > div.weui-desktop-dialog__ft > div:nth-child(2) > button").click()
        # 填写摘要
        await self.page.locator("#js_description").fill(digest)
        # 填写合集（标签）
        await self.page.locator("#js_article_tags_area > label > div > span").click()
        tags_input = self.page.locator("#vue_app > div:nth-child(3) > div.weui-desktop-dialog__wrp.article_tags_dialog.js_article_tags_dialog > div > div.weui-desktop-dialog__bd > div > form > div.weui-desktop-form__control-group > div > div.tags_input_wrap.js_not_hide_similar_tags > div:nth-child(1) > div > span > span.weui-desktop-form-tag__wrp > div > span > input")
        for tag in tags:
            await tags_input.fill(tag)
            await self.page.locator("#vue_app > div:nth-child(3) > div.weui-desktop-dialog__wrp.article_tags_dialog.js_article_tags_dialog > div > div.weui-desktop-dialog__bd > div > form > div.weui-desktop-form__control-group > div > div.tags_input_wrap.js_not_hide_similar_tags > div.weui-desktop-dropdown-menu.article_tags_sug > ul > li > div").click()
        await self.page.locator("#vue_app > div:nth-child(3) > div.weui-desktop-dialog__wrp.article_tags_dialog.js_article_tags_dialog > div > div.weui-desktop-dialog__ft > div:nth-child(1) > button").click()
        # 发布
        await self.page.locator("#js_send > button").click()
        await self.page.locator("#vue_app > div:nth-child(5) > div.new_mass_send_dialog > div.weui-desktop-dialog__wrp > div > div.weui-desktop-dialog__bd > div > div > form > div.mass-send__td > div.publish_container.mass_send__notify.weui-desktop-form__control-group > div > div.mass-send__timer-wrp > label > input").set_checked(checked=False)
        await self.page.locator("#vue_app > div:nth-child(5) > div.new_mass_send_dialog > div.weui-desktop-dialog__wrp > div > div.weui-desktop-dialog__ft > div > div > div:nth-child(1) > button").click()
        await self.page.locator("#vue_app > div:nth-child(5) > div.double_check_dialog > div.weui-desktop-dialog__wrp > div > div.weui-desktop-dialog__ft > div > div:nth-child(1) > button").click()
        async with self.page.expect_navigation(url="https://mp.weixin.qq.com/cgi-bin/home?**") as response_info:
            await response_info.value
        await self.page.locator("#list > div.publish_record_index > div > div:nth-child(1) > div:nth-child(1) > div > div.weui-desktop-mass-media.weui-desktop-mass-appmsg > div.weui-desktop-mass-appmsg__ft > div > div:nth-child(4) > div > div > span > button").click()
        await self.page.locator("#list > div.publish_record_index > div > div:nth-child(1) > div:nth-child(1) > div > div.weui-desktop-mass-media.weui-desktop-mass-appmsg > div.weui-desktop-mass-appmsg__ft > div > div:nth-child(4) > div > div > div > div > div > div > ul > li:nth-child(4)").click()
        # 获取链接
        return pyperclip.paste()


