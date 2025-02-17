# -*- coding: utf-8 -*-
import re
import typing as t
from utils.helper import wait_random_time
from common.constant import config
from common.core import Community
import json
from playwright.async_api import Browser, BrowserContext
from common.apis import Post, StorageType
from common.constant import config


class Wechat(Community):
    url_post_new = "https://mp.weixin.qq.com/"
    site_name = "公众号"
    site_alias = "wechat"
    url = "https://mp.weixin.qq.com/"
    login_url = "https://mp.weixin.qq.com/"
    desc = "微信公众号官方插件"

    conf = {
        "category": "科技",
        "columns": ["Python"],
        "cover": None,
        "tags": ["Python"],
        "timeout": 40000,
        "topic": None
    }

    def __init__(self, browser: "Browser", context: "BrowserContext", **kwargs):
        super().__init__(browser, context, **kwargs)
        self.origin_src = None

    async def upload(self, post: Post) -> t.AnyStr:
        if not config['default']['community'][self.site_alias] or not config['default']['community'][self.site_alias]['is_login']:
            return "未登录"
        await self.before_upload(post)
        await self.page.goto(Wechat.url_post_new)
        async with self.context.expect_page() as new_page:
            await self.page.locator('.new-creation__menu > div:nth-child(4)').click()
        await self.page.close()
        self.page = await new_page.value
        await self.page.get_by_role("listitem", name="文档导入").click()
        async with self.page.expect_file_chooser() as fc_info:
            await self.page.locator('#js_import_file_container label').click()
        file_chooser = await fc_info.value
        async with self.page.expect_response("https://mp.weixin.qq.com/advanced/mplog?action**") as response_info:
            await file_chooser.set_files(self.post['paths']['html'].replace('.html', '.docx'))
            await response_info.value
        # 填写作者
        await self.page.locator("#author").fill(config['default']['author'])
        # 上传封面
        async with self.page.expect_file_chooser() as fc_info:
            wait_random_time()
            await self.page.locator("#js_cover_area").scroll_into_view_if_needed()
            wait_random_time()
            await self.page.locator("#js_cover_area").hover()
            wait_random_time()
            await self.page.locator("#js_cover_null > ul > li:nth-child(2) > a").click()
            wait_random_time()
            await self.page.locator("#vue_app label").nth(1).click()
        file_chooser = await fc_info.value
        async with self.page.expect_response(
                "https://mp.weixin.qq.com/cgi-bin/filetransfer?action=upload**"):
            await file_chooser.set_files(self.post['cover'])
        if await self.page.locator(
                "#js_image_dialog_list_wrp > div > div:nth-child(2) > i > .image_dialog__checkbox").is_enabled():
            await self.page.locator("#js_image_dialog_list_wrp > div > div:nth-child(2)").click()
        await self.page.locator(
            "#vue_app > div:nth-child(3) > div.weui-desktop-dialog__wrp.weui-desktop-dialog_img-picker > div > div.weui-desktop-dialog__ft > div:nth-child(1) > button").click()
        wait_random_time()
        await self.page.locator(
            "#vue_app > div:nth-child(3) > div.weui-desktop-dialog__wrp > div > div.weui-desktop-dialog__ft > div:nth-child(2) > button").click()
        wait_random_time()
        # 填写摘要
        await self.page.locator("#js_description").fill(self.post['digest'])
        # 填写合集（标签）
        await self.page.locator("#js_article_tags_area > label > div > span").click()
        tags_input = self.page.locator(
            "#vue_app > div:nth-child(3) > div.weui-desktop-dialog__wrp.article_tags_dialog.js_article_tags_dialog > "
            "div > div.weui-desktop-dialog__bd > div > form > div.weui-desktop-form__control-group > div > "
            "div.tags_input_wrap.js_not_hide_similar_tags > div:nth-child(1) > div > span > "
            "span.weui-desktop-form-tag__wrp > div > span > input")
        for tag in self.post['tags']:
            await tags_input.fill(tag)
            await self.page.locator(
                "#vue_app > div:nth-child(3) > div.weui-desktop-dialog__wrp.article_tags_dialog"
                ".js_article_tags_dialog > div > div.weui-desktop-dialog__bd > div > form > "
                "div.weui-desktop-form__control-group > div > div.tags_input_wrap.js_not_hide_similar_tags > "
                "div.weui-desktop-dropdown-menu.article_tags_sug > ul > li > div").click()
        await self.page.locator(
            "#vue_app > div:nth-child(3) > div.weui-desktop-dialog__wrp.article_tags_dialog.js_article_tags_dialog > "
            "div > div.weui-desktop-dialog__ft > div:nth-child(1) > button").click()
        # 保存草稿
        await self.page.locator("#js_submit > button").click()
        async with self.page.expect_response("https://mp.weixin.qq.com/cgi-bin/masssend?**") as response_info:
            response = await response_info.value
        data_body = await response.body()
        data = json.loads(data_body.decode('utf-8'))
        if data['base_resp']['ret'] == 0:
            await self.page.locator("#js_preview > button").click()
            await self.page.wait_for_load_state()
            return self.page.url
        # 获取链接
        return "上传失败"
