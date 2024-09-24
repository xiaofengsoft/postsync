import asyncio
import re
import typing as t

from common.apis import Post, StorageType
from common.config import config
from common.func import wait_random_time
from entity.community import Community
from bs4 import BeautifulSoup
from common.error import BrowserTimeoutError
import json
from playwright.async_api import Browser, BrowserContext


class Zhihu(Community):
    url_post_new = "https://zhuanlan.zhihu.com/write"
    login_url = "https://www.zhihu.com/signin"
    url_redirect_login = "https://www.zhihu.com/signin"
    site_name = "知乎"
    site_alias = "zhihu"
    site_storage_mark:t.List[StorageType] = [{
        "type": "local",
        "domain": "www.zhihu.com",
        "name": "uhiuhvk_wrnhq",
        "value": ""
    },{
        "type": "cookie",
        "domain": "zhihu.com",
        "name": "z_c0",
        "value": ""
    }]
    url = "https://www.zhihu.com"

    def __init__(self, browser: "Browser", context: "BrowserContext", post: Post):
        super().__init__(browser, context, post)
        self.pic_nums = 0  # 正在处理的图片数量
        self.origin_src = None

    async def upload(self) -> t.AnyStr:
        if not self.is_login:
            await self.login(
                self.login_url,
                re.compile(r"www\.zhihu\.com\/api\/v3\/oauth\/sign_in"),
                lambda login_data: 0 == 0
            )
        await self.page.goto(self.url_post_new)
        # 上传图片
        await self.page.get_by_label("图片").click()
        content = await self.convert_html_path(self.post['contents']['html'])
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
        await self.page.goto("https://zhuanlan.zhihu.com/p/" + str(data['id']) + "/edit")
        # 输入标题
        await self.page.get_by_placeholder("请输入标题（最多 100 个字）").fill(self.post['title'])
        # 上传封面
        async with self.page.expect_file_chooser() as fc_info:
            await self.page.locator("label").filter(has_text="添加文章封面").click()
            file_chooser = await fc_info.value
            await file_chooser.set_files(self.post['cover'])
        # 这里的分类当作问题投稿
        await self.page.locator(".ddLajxN_Q0AuobBZjX9m > button").first.click()
        await self.page.get_by_placeholder("请输入关键词查找问题").click()
        await self.page.get_by_placeholder("请输入关键词查找问题").fill(self.post['category'])
        wait_random_time(1, 2)
        try:
            await self.page.locator(".Creator-SearchBar-searchIcon").dblclick()
            await self.page.locator(".css-1335jw2 > div > .Button").first.click()
            await self.page.get_by_role("button", name="确定").click()
        except BrowserTimeoutError:
            await self.page.locator(".Creator-SearchBar-searchIcon").dblclick()
            await self.page.locator(".css-1335jw2 > div > .Button").first.click()
            await self.page.get_by_role("button", name="确定").click()

        # 标签当作文章话题
        for tag in self.post['tags']:
            await self.page.get_by_role("button", name="添加话题").click()
            await self.page.get_by_placeholder("搜索话题").fill(tag)
            await self.page.locator(".css-ogem9c > button").first.click()
        # 选择专栏
        await self.page.locator("label").filter(has_text=re.compile(r"^发布到专栏$")).click()
        try:
            column = self.post['columns'][0]
            await self.page.locator("#Popover22-toggle").click()
            await self.page.locator(f"//button[contains(text(),'{column}')]").first.click()
        except BrowserTimeoutError:
            column = config['default']['community'][self.site_alias]['columns'][0]
            await self.page.locator("#Popover22-toggle").click()
            await self.page.locator(f"//button[contains(text(),'{column}')]").first.click()
        # 发布文章
        await self.page.get_by_role("button", name="发布", exact=True).click()
        await self.page.wait_for_url("https://zhuanlan.zhihu.com/p/*")
        return self.page.url

    async def check_response(self, response):
        if response.url.startswith("https://api.zhihu.com/images/"):
            resp_body = await response.body()
            data = json.loads(resp_body.decode('utf-8'))
            if data['status'] == 'success':
                self.origin_src = data['original_src']

    async def upload_img(self, img_path: str) -> str:
        self.page.on("response", self.check_response)
        async with self.page.expect_response("https://api.zhihu.com/images"):
            async with self.page.expect_file_chooser() as fc_info:
                if self.pic_nums != 0:
                    await self.page.locator("body > div:nth-child(28) > div > div > div > "
                                            "div.Modal.Modal--default.css-zelv4t > div > div > div > div.css-1jf2703 "
                                            "> div.css-s3axrf > div > div").first.click()
                else:
                    await self.page.locator(".css-n71hcb").click()
                file_chooser = await fc_info.value
                await file_chooser.set_files(img_path)
                self.pic_nums += 1
            while self.origin_src is None:
                await asyncio.sleep(0.1)
            self.origin_src: str
            return self.origin_src

    async def convert_html_path(self, content: str) -> str:
        soup = BeautifulSoup(content, 'html.parser')
        img_tags = soup.find_all('img')
        for img in img_tags:
            img['src'] = await self.upload_img(img['src'])
        return str(soup)

