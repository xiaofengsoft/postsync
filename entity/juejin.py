import json
import re
import time
import typing as t
from bs4 import BeautifulSoup
from common.apis import Post
from common.config import config
from common.error import BrowserTimeoutError
from common.func import wait_random_time
from entity.community import Community


class Juejin(Community):
    """
    Juejin Community
    """

    site_name = "稀土掘金"
    site_alias = "juejin"
    site_storage_mark = (
        'api.juejin.cn'
    )
    url_post_new = "https://juejin.cn/editor/drafts/new"
    url_redirect_login = "https://juejin.cn/login"
    login_url = "https://juejin.cn/login"
    url = "https://www.juejin.cn"

    async def upload(self) -> t.AnyStr:
        if not self.is_login:
            await self.login(self.login_url,
                             re.compile(r"^https?:\/\/api\.juejin\.cn\/user_api\/v1\/sys\/token"),
                             lambda login_data: 0 == 0)
        # 打开发布页面
        await self.page.goto(self.url_post_new)
        # 处理图片路径
        content = await self.convert_html_path(self.post['contents']['html'])
        # 输入标题
        await self.page.locator(".title-input").fill(self.post['title'])
        # 选中内容输入框
        await self.page.get_by_role("textbox").nth(1).fill(content)

        async def choose_cover():
            async with self.page.expect_file_chooser() as fc_info:
                await self.page.get_by_role("button", name="上传封面").click()
                file_chooser = await fc_info.value
                await file_chooser.set_files(self.post['cover'])

        # 点击发布按钮
        await self.page.locator("button", has_text="发布").first.click()
        # 选择分类
        try:
            await (self.page.locator(".category-list")
                   .locator(
                "div",
                has_text=re.compile(self.post['category'], re.IGNORECASE)
            ).click(timeout=5000))
        except BrowserTimeoutError:
            await (self.page.locator(".category-list")
                   .locator("div", has_text=re.compile(config['default']['community']['juejin']['category'],
                                                       re.IGNORECASE)).click(timeout=5000))
        # 选择标签
        await self.page.get_by_text("请搜索添加标签").click(),
        tag_selector = self.page.locator('.tag-select-add-margin')
        tag_input = self.page.get_by_role("banner").get_by_role("textbox").nth(1)
        # 逐个搜索添加标签
        for tag in self.post['tags']:
            wait_random_time()
            await tag_input.fill(tag)
            await tag_input.press('Enter')
            try:
                await tag_selector.locator("li").first.click(timeout=config['default']['timeout'])
            except BrowserTimeoutError:
                continue
        # 输入摘要
        await self.page.get_by_role("banner").locator("textarea").fill(self.post['digest'])
        time.sleep(0.1)
        # 选择封面
        await choose_cover()
        # 点击空白处防止遮挡
        # await self.page.locator("//div[@class='title' and text()='发布文章']").click()
        # 选择专栏
        column_selector = self.page.locator(".byte-select-dropdown").last
        column_input = self.page.get_by_role("banner").get_by_role("textbox").nth(2)
        try:
            for column in self.post['columns']:
                await column_input.fill(column)
                await column_selector.locator("li", has_text=re.compile(column, re.IGNORECASE)).first.click()
        except BrowserTimeoutError:
            columns = config['default']['community']['juejin']['columns']
            for column in columns:
                await column_input.fill(column)
                await column_selector.locator("li", has_text=re.compile(column, re.IGNORECASE)).first.click()
        # 选择话题
        if self.post['topic']:
            topic_selector = self.page.locator(".topic-select-dropdown")
            topic_input = self.page.get_by_role("banner").get_by_role("textbox").nth(3)
            await topic_input.fill(self.post['topic'])
            await topic_selector.locator("span", has_text=re.compile(self.post['topic'], re.IGNORECASE)).first.click()
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

    async def upload_img(self, img_path: str) -> str:
        async with self.page.expect_response("**/get_img_url*") as first:
            async with self.page.expect_file_chooser() as fc_info:
                await self.page.locator("div:nth-child(6) > svg").first.click()
                file_chooser = await fc_info.value
                await file_chooser.set_files(img_path)
        resp = await first.value
        resp_body = await resp.body()
        data = json.loads(resp_body.decode('utf-8'))
        return data['data']['main_url']

    async def convert_html_path(self, content: str) -> str:
        soup = BeautifulSoup(content, 'html.parser')
        img_tags = soup.find_all('img')
        for img in img_tags:
            img['src'] = await self.upload_img(img['src'])
        return str(soup)

    async def check_login_state(self) -> bool:
        if not await super().check_login_state():
            return False
        try:
            await self.page.goto(self.url_post_new)
            await self.page.wait_for_url(
                url=re.compile(self.url_redirect_login),
                timeout=config['default']['login_timeout'])
            print(f"{self.site_name} 未登录")
            return False
        except BrowserTimeoutError:
            return True



