import asyncio
import re

from common.core import config
from common.func import get_file_dir
from entity.community import Community
from bs4 import BeautifulSoup
import os
import json


class Zhihu(Community):
    url_post_new = "https://zhuanlan.zhihu.com/write"
    site_name = "知乎"

    def __init__(self, browser, ap, asp):
        super().__init__(browser, ap, asp)
        self.pic_nums = 0  # 正在处理的图片数量
        self.origin_src = None

    async def async_post_new(self, title: str, digest: str, content: str, file_path: str = None, tags: list = None,
                             category: str = None, cover: str = None, columns: list = None, topic: str = None) -> str:
        """
        先保存到草稿，借助Patch请求，借助草稿发布文章，在这之前需要先上传图片
        有个post请求 drafts
        还有个patch请求 draft
        同步的请求可以成功post drafts
        但是这里不知道为什么不能，可能是异步的原因
        """
        # 处理参数
        category = category or config['default']['community']['zhihu']['category']
        tags = tags or [config['default']['community']['zhihu']['tag']]
        cover = cover or config['default']['cover']
        columns = columns or [config['default']['community']['zhihu']['column']]
        await self.page.goto(self.url_post_new)
        # 上传图片
        await self.page.get_by_label("图片").click()
        content = await self.async_convert_html_img_path(content, file_path)
        await self.page.get_by_label("关闭").click()
        # 上传内容
        resp = await self.page.request.fetch(
            "https://zhuanlan.zhihu.com/api/articles/drafts",
            method="POST",
            data={
                "content": content,
                "del_time": "0",
                "table_of_contents": "false"
            },
            ignore_https_errors=True
        )
        resp_body = await resp.body()
        data = json.loads(resp_body.decode('utf-8'))
        await self.page.goto("https://zhuanlan.zhihu.com/p/"+str(data['id'])+"/edit")
        # 输入标题
        await self.page.get_by_placeholder("请输入标题（最多 100 个字）").fill(title)
        # 上传封面
        async with self.page.expect_file_chooser() as fc_info:
            await self.page.locator("label").filter(has_text="添加文章封面").click()
            file_chooser = await fc_info.value
            await file_chooser.set_files(cover)

        # 这里的分类当作问题投稿
        await self.page.locator(".ddLajxN_Q0AuobBZjX9m > button").first.click()
        await self.page.get_by_placeholder("请输入关键词查找问题").click()
        await self.page.get_by_placeholder("请输入关键词查找问题").fill(category)
        await asyncio.sleep(0.2)
        await self.page.locator(".Creator-SearchBar-searchIcon").click()
        await self.page.locator(".css-1335jw2 > div > .Button").first.click()
        await self.page.get_by_role("button", name="确定").click()
        # 标签当作文章话题
        for tag in tags:
            await self.page.get_by_role("button", name="添加话题").click()
            await self.page.get_by_placeholder("搜索话题").fill(tag)
            await self.page.locator(".css-ogem9c > button").first.click()
        # 选择专栏
        await self.page.locator("label").filter(has_text=re.compile(r"^发布到专栏$")).click()
        for column in columns:
            await self.page.locator("#Popover22-toggle").click()
            await self.page.locator(f"//button[contains(text(),'{column}')]").first.click()
        # 发布文章
        await self.page.get_by_role("button", name="发布",exact=True).click()
        await self.page.wait_for_url("https://zhuanlan.zhihu.com/p/*")
        return self.page.url

    async def check_response(self,response):
        if response.url.startswith("https://api.zhihu.com/images/"):
            resp_body =  await response.body()
            data = json.loads(resp_body.decode('utf-8'))
            if data['status'] == 'success':
                self.origin_src = data['original_src']

    async def async_upload_img(self, img_path: str) -> str:
        self.page.on("response", self.check_response)
        async with self.page.expect_response("https://api.zhihu.com/images") as first:
            async with self.page.expect_file_chooser() as fc_info:
                if self.pic_nums != 0:
                    await self.page.get_by_role("button", name="本地上传").click()
                else:
                    await self.page.locator(".css-n71hcb").click()
                file_chooser = await fc_info.value
                await file_chooser.set_files(img_path)
            while self.origin_src is None:
                await asyncio.sleep(0.1)
            origin_src = self.origin_src
            self.origin_src = None
            return origin_src

    async def async_convert_html_img_path(self, content: str, file_path: str) -> str:
        soup = BeautifulSoup(content, 'html.parser')
        img_tags = soup.find_all('img')
        img_dir = get_file_dir(file_path)
        for img in img_tags:
            img['src'] = await self.async_upload_img(os.path.join(img_dir, img['src']))
        return str(soup)
