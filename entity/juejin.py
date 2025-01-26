import json
import re
import typing as t
from common.apis import StorageType, Post
from utils.helper import wait_random_time
from common.core import Community


class Juejin(Community):
    """
    Juejin Community
    """

    site_name = "稀土掘金"
    site_alias = "juejin"
    url_post_new = "https://juejin.cn/editor/drafts/new"
    url_redirect_login = "https://juejin.cn/login"
    login_url = "https://juejin.cn/login"
    url = "https://www.juejin.cn"
    desc = "稀土掘金官方插件"

    async def upload(self, post: Post) -> t.AnyStr:
        await self.before_upload(post)
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
        async def inner_upload_category(category: str):
            await (self.page.locator(".category-list")
                   .locator(
                "div",
                has_text=re.compile(category, re.IGNORECASE)
            ).click())

        await self.double_try_single_data(
            'category',
            inner_upload_category,
            inner_upload_category
        )

        # 选择标签
        await self.page.get_by_text("请搜索添加标签").click()
        tag_input = self.page.get_by_role(
            "banner").get_by_role("textbox").nth(1)

        # 逐个搜索添加标签

        tag_zone = self.page.locator(
            "body > div.byte-select-dropdown.byte-select-dropdown--multiple.tag-select-add-margin > div"
        )

        async def inner_upload_tag(inner_tag: str):
            await tag_input.fill(inner_tag)
            wait_random_time()
            await tag_zone.locator("li").first.click()

        await self.double_try_data(
            'tags',
            inner_upload_tag,
            inner_upload_tag
        )
        # 输入摘要
        await self.page.get_by_role("banner").locator("textarea").fill(self.post['digest'])
        wait_random_time()
        # 选择封面
        await choose_cover()
        # 点击空白处防止遮挡
        # 选择专栏
        column_selector = self.page.locator(".byte-select-dropdown").last
        column_input = self.page.get_by_role(
            "banner").get_by_role("textbox").nth(2)

        async def inner_upload_column(column: str):
            await column_input.fill(column)
            await column_selector.locator("li", has_text=re.compile(column, re.IGNORECASE)).first.click()

        await self.double_try_data(
            'columns',
            inner_upload_column,
            inner_upload_column
        )

        # 选择话题
        if self.post['topic']:
            topic_selector = self.page.locator(".topic-select-dropdown")
            topic_input = self.page.get_by_role(
                "banner").get_by_role("textbox").nth(3)
            await topic_input.fill(self.post['topic'])
            await topic_selector.locator("span", has_text=re.compile(self.post['topic'], re.IGNORECASE)).first.click()
        # 点击发布按钮
        wait_random_time()

        async def inner_click_publish():
            await self.page.locator(
                "#juejin-web-editor > div.edit-draft > div > header > div.right-box > "
                "div.publish-popup.publish-popup.with-padding.active > div > div.footer > div > "
                "button.ui-btn.btn.primary.medium.default"
            ).click()

        await self.double_try(
            inner_click_publish,
            inner_click_publish
        )
        await self.page.wait_for_url(re.compile(r"\/published"))
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
