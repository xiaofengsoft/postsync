from entity.community import Community
from bs4 import BeautifulSoup
import json
from common.core import config
import re
from common.func import wait_random_time
from common.error import BrowserTimeoutError


class Csdn(Community):
    site_name = 'CSDN'
    url_post_new = 'https://editor.csdn.net/md/'
    site_alias = 'csdn'

    async def async_post_new(self,
                             title: str,
                             digest: str,
                             content: str,
                             file_path: str = None,
                             tags: list = None,
                             category: str = None,
                             cover: str = None,
                             columns: list = None,
                             topic: str = None,
                             ) -> str:
        # 处理参数
        columns, tags, category, cover = super().process_args(columns, tags, category, cover)
        # 打开发布页面
        await self.page.goto(self.url_post_new)
        await self.page.locator(".editor__inner").fill("")
        wait_random_time()
        # TODO 换成MD输入 或者 优化md转html
        # 处理内容
        content = await self.async_convert_html_img_path(content, file_path)
        # 输入标题
        await self.page.locator(".article-bar__title").fill(title),
        # 输入内容
        await self.page.locator(".editor__inner").fill(content)
        await self.page.get_by_role("button", name="发布文章").click()
        cover_img = self.page.locator(
            "body > div.app.app--light > div.modal > div > div.modal__inner-2 > div.modal__content > div:nth-child(3) > div > div.preview-box > img"
            )
        cover_attr = await cover_img.get_attribute("src")
        if cover_attr.strip() != "":
            await cover_img.hover()
            await self.page.locator("body > div.app.app--light > div.modal > div > div.modal__inner-2 > div.modal__content > div:nth-child(3) > div > div.preview-box > a > i").click()
        # 封面处理
        async with self.page.expect_file_chooser() as fc_info:
            await self.page.locator(".upload-img-box").click()
            file_chooser = await fc_info.value
            await file_chooser.set_files(cover)
        # 输入摘要
        wait_random_time()
        await self.page.locator(".el-textarea__inner").fill(digest)
        # 标签处理
        wait_random_time()
        await self.page.locator(".mark_selection_title_el_tag > .tag__btn-tag").click()
        tag_input = self.page.locator(".el-input--suffix > .el-input__inner")
        column_selector = self.page.locator(".el-autocomplete-suggestion__list")
        for tag in tags:
            await tag_input.fill(tag)
            try:
                await column_selector.locator("li", has_text=re.compile(tag, re.IGNORECASE)).first.click()
            except BrowserTimeoutError:
                await column_selector.locator("li").first.click()
        await self.page.locator(".mark_selection_box_body > button").click()
        wait_random_time()
        # 专栏处理
        column_selector = self.page.locator(".tag__options-list")
        try:
            for column in columns:
                await self.page.locator(".tag__item-list > .tag__btn-tag").click()
                await column_selector.locator("span", has_text=re.compile(column, re.IGNORECASE)).first.click()
        except Exception as e:
            columns = config['default']['community']['csdn']['columns']
            for column in columns:
                await self.page.locator(".tag__item-list > .tag__btn-tag").click()
                await column_selector.locator("span", has_text=re.compile(column, re.IGNORECASE)).first.click()
        await self.page.locator("      .tag__options-txt > .modal__close-button").click()
        # 点击发布按钮
        wait_random_time()
        await self.page.get_by_label("Insert publishArticle").get_by_role("button", name="发布文章").click()
        # 文章链接
        wait_random_time()
        async with self.page.expect_response("**/saveArticle") as response_info:
            pass
        data = await response_info.value
        data_body = await data.body()
        data = json.loads(data_body.decode('utf-8'))
        post_url = data['data']['url']
        return post_url

    async def async_convert_html_img_path(self, content: str, file_path: str) -> str:
        soup = BeautifulSoup(content, 'html.parser')
        img_tags = soup.find_all('img')
        for img in img_tags:
            img['src'] = await self.async_upload_img(img['src'])
        return str(soup)

    async def async_upload_img(self, img_path: str) -> str:
        async with self.page.expect_response("https://csdn-img-blog.obs.cn-north-4.myhuaweicloud.com/") as first:
            async with self.page.expect_file_chooser() as fc_info:
                await self.page.get_by_role("button", name="图片 图片").click()
                await self.page.locator(".uploadPicture > input").click()
                file_chooser = await fc_info.value
                await file_chooser.set_files(img_path)
        resp = await first.value
        resp_body = await resp.body()
        data = json.loads(resp_body.decode('utf-8'))
        return data['data']['imageUrl']
