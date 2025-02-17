import typing as t

from common.apis import StorageType, Post
from common.core import Community
from bs4 import BeautifulSoup
import json
import re
from utils.helper import wait_random_time
from common.error import BrowserTimeoutError
from utils.file import get_path
from utils.data import on_click_by_selector
from common.constant import config


class Csdn(Community):
    site_name = 'CSDN'
    url_post_new = 'https://editor.csdn.net/md/'
    url_redirect_login = 'https://passport.csdn.net/login'
    site_alias = 'csdn'
    url = "https://www.csdn.net/"
    login_url = "https://passport.csdn.net/login?code=applets"
    desc = 'CSDN官方插件'

    conf = {
        "category": "科技",
        "columns": ["Python"],
        "cover": None,
        "tags": ["Python"],
        "timeout": 40000,
        "topic": None,
    }

    async def upload(self, post: Post) -> t.AnyStr:
        if not config['default']['community'][self.site_alias] or not config['default']['community'][self.site_alias]['is_login']:
            return ("未登录")
        await self.before_upload(post)
        # 打开发布页面
        await self.page.goto(self.url_post_new)
        await self.page.locator(".editor__inner").fill("")
        wait_random_time()
        # 处理内容
        content = await self.convert_html_path(self.post['contents']['html'])
        # 输入标题
        await self.page.locator(".article-bar__title").fill(self.post['title']),
        # 输入内容
        await self.page.locator(".editor__inner").fill(content)
        await self.page.get_by_role("button", name="发布文章").click()
        cover_img = self.page.locator(
            "body > div.app.app--light > div.modal > div > div.modal__inner-2 > div.modal__content > div:nth-child(3) "
            "> div > div.preview-box > img"
        )
        cover_attr = await cover_img.get_attribute("src")
        if cover_attr.strip() != "":
            await on_click_by_selector(self.page, ".btn-remove-coverimg")
        # 封面处理
        async with self.page.expect_file_chooser() as fc_info:
            try:
                await self.page.locator(".preview-box").click()
            except BrowserTimeoutError:
                await on_click_by_selector(self.page, ".btn-remove-coverimg")
                await self.page.locator(".preview-box").click()
            file_chooser = await fc_info.value
            await file_chooser.set_files(self.post['cover'])
        # 输入摘要
        wait_random_time()
        await self.page.locator(".el-textarea__inner").fill(self.post['digest'])
        # 标签处理
        wait_random_time()
        await self.page.locator(".mark_selection_title_el_tag > .tag__btn-tag").click()
        tag_input = self.page.locator(".el-input--suffix > .el-input__inner")
        column_selector = self.page.locator(
            ".el-autocomplete-suggestion__list")

        for tag in self.post['tags']:
            await tag_input.fill(tag)
            try:
                await column_selector.locator("li", has_text=re.compile(tag, re.IGNORECASE)).first.click()
            except BrowserTimeoutError:
                await column_selector.locator("li").first.click()
        await self.page.locator(".mark_selection_box_body > button").click()
        wait_random_time()
        # 专栏处理
        column_selector = self.page.locator(".tag__options-list")

        async def inner_upload_column(column: str):
            await self.page.locator(".tag__item-list > .tag__btn-tag").click()
            await column_selector.locator("span", has_text=re.compile(column, re.IGNORECASE)).first.click()

        await self.double_try_data(
            'columns',
            inner_upload_column,
            inner_upload_column,
        )

        await self.page.locator(".tag__options-txt > .modal__close-button").click()
        # 点击发布按钮
        wait_random_time()
        await self.page.get_by_label("Insert publishArticle").get_by_role("button", name="发布文章").click()
        # 文章链接
        wait_random_time()
        async with self.page.expect_response("**/saveArticle") as response_info:
            pass
        wait_random_time()
        data = await response_info.value
        data_body = await data.body()
        data = json.loads(data_body.decode('utf-8'))
        post_url = data['data']['url']
        return post_url

    async def convert_html_path(self, content: str) -> str:
        soup = BeautifulSoup(content, 'html.parser')
        img_tags = soup.find_all('img')
        for img in img_tags:
            img['src'] = await self.upload_img(img['src'])
        return str(soup)

    async def upload_img(self, img_path: str) -> str:
        img_path = get_path(img_path)
        async with self.page.expect_response("https://csdn-img-blog.obs.cn-north-4.myhuaweicloud.com/") as first:
            async with self.page.expect_file_chooser() as fc_info:
                await self.page.get_by_role("button", name="图片 图片").dblclick()
                await self.page.locator(".uploadPicture > input").dblclick()
                file_chooser = await fc_info.value
                await file_chooser.set_files(img_path)
        resp = await first.value
        resp_body = await resp.body()
        data = json.loads(resp_body.decode('utf-8'))
        return data['data']['imageUrl']
