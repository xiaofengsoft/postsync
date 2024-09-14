# -*- coding: utf-8 -*-
from common.func import wait_random_time
from common.core import config
from entity.community import Community
import json


class Wechat(Community):
    url_post_new = "https://mp.weixin.qq.com/"
    site_name = "公众号"
    site_alias = "wechat"

    def __init__(self, browser, ap, asp):

        super().__init__(browser, ap, asp)
        self.origin_src = None

    async def async_post_new(self, title: str, digest: str, content: str, file_path: str = None, tags: list = None,
                             category: str = None, cover: str = None, columns: list = None, topic: str = None) -> str:
        # 处理参数
        columns, tags, category, cover = super().process_args(columns, tags, category, cover)
        await self.page.goto(Wechat.url_post_new)
        async with self.browser.expect_page() as new_page:
            await self.page.locator("#app > div.main_bd_new > div:nth-child(3) > div.weui-desktop-panel__bd > div > div:nth-child(3) > div").click()
        await self.page.close()
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
        async with self.page.expect_file_chooser() as fc_info:
            wait_random_time()
            await self.page.locator("#js_cover_area").scroll_into_view_if_needed()
            wait_random_time()
            await self.page.locator("#js_cover_area").hover()
            await self.page.locator("#js_cover_null > ul > li:nth-child(2) > a").click()
            await self.page.locator("#vue_app label").nth(1).click()
        file_chooser = await fc_info.value
        async with self.page.expect_response("https://mp.weixin.qq.com/cgi-bin/filetransfer?action=upload**") as response_info:
            await file_chooser.set_files(cover)
        if await self.page.locator("#js_image_dialog_list_wrp > div > div:nth-child(2) > i > .image_dialog__checkbox").is_enabled():
            await self.page.locator("#js_image_dialog_list_wrp > div > div:nth-child(2)").click()
        await self.page.locator("#vue_app > div:nth-child(3) > div.weui-desktop-dialog__wrp.weui-desktop-dialog_img-picker.weui-desktop-dialog_img-picker-with-crop > div > div.weui-desktop-dialog__ft > div:nth-child(1) > button").click()
        wait_random_time()
        await self.page.locator("#vue_app > div:nth-child(3) > div.weui-desktop-dialog__wrp.weui-desktop-dialog_img-picker.weui-desktop-dialog_img-picker-with-crop > div > div.weui-desktop-dialog__ft > div:nth-child(2) > button").click()
        wait_random_time()
        # 填写摘要
        await self.page.locator("#js_description").fill(digest)
        # 填写合集（标签）
        await self.page.locator("#js_article_tags_area > label > div > span").click()
        tags_input = self.page.locator("#vue_app > div:nth-child(3) > div.weui-desktop-dialog__wrp.article_tags_dialog.js_article_tags_dialog > div > div.weui-desktop-dialog__bd > div > form > div.weui-desktop-form__control-group > div > div.tags_input_wrap.js_not_hide_similar_tags > div:nth-child(1) > div > span > span.weui-desktop-form-tag__wrp > div > span > input")
        for tag in tags:
            await tags_input.fill(tag)
            await self.page.locator("#vue_app > div:nth-child(3) > div.weui-desktop-dialog__wrp.article_tags_dialog.js_article_tags_dialog > div > div.weui-desktop-dialog__bd > div > form > div.weui-desktop-form__control-group > div > div.tags_input_wrap.js_not_hide_similar_tags > div.weui-desktop-dropdown-menu.article_tags_sug > ul > li > div").click()
        await self.page.locator("#vue_app > div:nth-child(3) > div.weui-desktop-dialog__wrp.article_tags_dialog.js_article_tags_dialog > div > div.weui-desktop-dialog__ft > div:nth-child(1) > button").click()
        # 保存草稿
        await self.page.locator("#js_submit > button").click()
        async with self.page.expect_response("https://mp.weixin.qq.com/cgi-bin/masssend?**") as response_info:
            response = await response_info.value
        data_body = await response.body()
        data = json.loads(data_body.decode('utf-8'))
        print(data['base_resp']['ret'])
        if data['base_resp']['ret'] == 0:
            await self.page.locator("#js_preview > button").click()
            await self.page.wait_for_load_state()
            return self.page.url
        # 获取链接
        return "上传失败"


