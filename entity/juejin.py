import os.path
import time
from entity.community import Community
from common.core import config
from bs4 import BeautifulSoup
import json
import re


class Juejin(Community):
    """
    Juejin Community
    """

    site_name = "稀土掘金"
    site_alias = "juejin"
    url_post_new = "https://juejin.cn/editor/drafts/new"
    url = "https://juejin.cn"

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
        # 处理图片路径
        content = await self.async_convert_html_img_path(content, file_path)
        # 输入标题
        await self.page.locator(".title-input").fill(title)
        # 选中内容输入框
        await self.page.get_by_role("textbox").nth(1).fill(content)

        async def choose_cover():
            async with self.page.expect_file_chooser() as fc_info:
                await self.page.get_by_role("button", name="上传封面").click()
                file_chooser = await fc_info.value
                await file_chooser.set_files(cover)

        # 点击发布按钮
        await self.page.locator("button", has_text="发布").first.click()
        # 选择分类
        try:
            await self.page.locator(".category-list").locator("div", has_text=re.compile(category, re.IGNORECASE)).click(timeout=5000)
        except Exception as e:
            await (self.page.locator(".category-list")
                   .locator("div", has_text=re.compile(config['default']['community']['juejin']['category'], re.IGNORECASE)).click(timeout=5000))
        # 选择标签
        await self.page.get_by_text("请搜索添加标签").click(),
        tag_selector = self.page.locator('.tag-select-add-margin')
        tag_input = self.page.get_by_role("banner").get_by_role("textbox").nth(1)
        # 逐个搜索添加标签
        time.sleep(0.1)
        try:
            for tag in tags:
                await tag_input.fill(tag)
                await tag_selector.locator("li", has_text=re.compile(tag, re.IGNORECASE)).first.click()
        except Exception as e:
            tags = config['default']['community']['juejin']['tags']
            for tag in tags:
                await tag_input.fill(tag)
                await tag_selector.locator("li", has_text=re.compile(tag, re.IGNORECASE)).first.click()
        # 输入摘要
        await self.page.get_by_role("banner").locator("textarea").fill(digest)
        time.sleep(0.1)
        # 选择封面
        await choose_cover()
        # 点击空白处防止遮挡
        # await self.page.locator("//div[@class='title' and text()='发布文章']").click()
        # 选择专栏
        column_selector = self.page.locator(".byte-select-dropdown").last
        column_input = self.page.get_by_role("banner").get_by_role("textbox").nth(2)
        try:
            for column in columns:
                await column_input.fill(column)
                await column_selector.locator("li", has_text=re.compile(column, re.IGNORECASE)).first.click()
        except Exception as e:
            columns = config['default']['community']['juejin']['columns']
            for column in columns:
                await column_input.fill(column)
                await column_selector.locator("li", has_text=re.compile(column, re.IGNORECASE)).first.click()
        # 选择话题
        if topic:
            topic_selector = self.page.locator(".topic-select-dropdown")
            topic_input = self.page.get_by_role("banner").get_by_role("textbox").nth(3)
            await topic_input.fill(topic)
            await topic_selector.locator("span", has_text=re.compile(topic, re.IGNORECASE)).first.click()
        # 点击发布按钮
        await self.page.get_by_role("button", name="确定并发布").click()
        await self.page.wait_for_url("**/published")
        # 获取文章链接
        res = self.page.expect_response("**/article/detail*")
        first = await res.__aenter__()
        resp = await first.value
        resp_body = await resp.body()
        data = json.loads(resp_body.decode('utf-8'))
        await res.__aexit__(None, None, None)
        return 'https://juejin.cn/post/' + data['data']['article_id']

    async def async_upload_img(self, img_path: str) -> str:
        async with self.page.expect_response("**/get_img_url*") as first:
            async with self.page.expect_file_chooser() as fc_info:
                await self.page.locator("div:nth-child(6) > svg").first.click()
                file_chooser = await fc_info.value
                await file_chooser.set_files(img_path)
        resp = await first.value
        resp_body = await resp.body()
        data = json.loads(resp_body.decode('utf-8'))
        return data['data']['main_url']

    async def async_convert_html_img_path(self, content: str, file_path: str) -> str:
        soup = BeautifulSoup(content, 'html.parser')
        img_tags = soup.find_all('img')
        for img in img_tags:
            img['src'] = await self.async_upload_img(img['src'])
        return str(soup)
