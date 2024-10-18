# -*- coding: utf-8 -*-
from common.apis import StorageType, Post
from entity.community import Community
from bs4 import BeautifulSoup
import json
from utils.helper import wait_random_time
from utils.data import insert_html_content_to_frame
import re
import typing as t


class Cnblog(Community):
    site_name = '博客园'
    url_post_new = 'https://i.cnblogs.com/posts/edit'
    site_alias = 'cnblog'
    login_url = 'https://account.cnblogs.com/signin'
    url = 'https://www.cnblogs.com/'
    site_storage_mark: t.List[StorageType] = [{
        'type': 'cookie',
        'domain': 'cnblogs.com',
        'name': 'XSRF-TOKEN',
        'value': ''
    }]

    async def login(self, *args, **kwargs):
        return await super().login(
            self.login_url,
            re.compile(r"account\.cnblogs\.com/user/userinfo"),
            lambda login_data: login_data['spaceUserId'])  # 发送用户ID说明登录成功

    async def upload(self, post: Post) -> t.AnyStr:
        await self.before_upload(post)
        # 打开发布页面
        await self.page.goto(self.url_post_new, wait_until='domcontentloaded')
        wait_random_time()
        # 处理内容
        content = await self.convert_html_path(self.post['contents']['html'])
        # 处理标题
        wait_random_time()
        await self.page.locator("#post-title").fill(self.post['title'])
        wait_random_time(1, 2)
        await insert_html_content_to_frame(self.page, "#postBodyEditor_ifr", "#tinymce", content)
        await self.page.frame_locator("#postBodyEditor_ifr").locator("#tinymce").click()
        await self.page.locator("#summary").scroll_into_view_if_needed()
        # 处理合集（专栏）
        await self.page.locator("div").filter(has_text=re.compile(r"^添加到合集$")).click()
        column_selector = self.page.locator(
            "body > cnb-root > cnb-app-layout > div.main > as-split > as-split-area:nth-child(2) > div > div > "
            "cnb-spinner > div > cnb-posts-entry > cnb-post-editing-v2 > cnb-post-editor > div.panel.panel--main > "
            "cnb-collection-selector > cnb-collapse-panel > "
            "div.panel-content.ng-tns-c31-16.ng-trigger.ng-trigger-openClosePanel.cnb-panel-body")
        for column in self.post['columns']:
            await column_selector.locator("span", has_text=re.compile(column, re.IGNORECASE)).first.click()
        # 处理封面
        await self.page.locator(
            "body > cnb-root > cnb-app-layout > div.main > as-split > as-split-area:nth-child(2) > div > div > "
            "cnb-spinner > div > cnb-posts-entry > cnb-post-editing-v2 > cnb-post-editor > div.panel.panel--main > "
            "cnb-collapse-panel > div.panel-content.ng-tns-c31-6.ng-trigger.ng-trigger-openClosePanel.cnb-panel-body "
            "> cnb-description-input > div > span > label > cnb-feature-image-input > div > "
            "div.featured-image-input__actions > div > a").click()
        async with self.page.expect_file_chooser() as fc_info:
            await self.page.locator("#modal-upload-featured-image > div > div > div:nth-child(3) > button").click()
            file_chooser = await fc_info.value
            await file_chooser.set_files(self.post['cover'])
        wait_random_time()
        await self.page.locator(
            "#cdk-overlay-1 > nz-modal-container > div > div > div.ant-modal-footer.ng-tns-c59-19.ng-star-inserted > "
            "button.ant-btn.ant-btn-primary.ant-btn-sm.ng-star-inserted").scroll_into_view_if_needed()
        await self.page.locator(
            "#cdk-overlay-1 > nz-modal-container > div > div > div.ant-modal-footer.ng-tns-c59-19.ng-star-inserted > "
            "button.ant-btn.ant-btn-primary.ant-btn-sm.ng-star-inserted").click()
        # 处理摘要
        await self.page.locator("#summary").fill(self.post['digest'])

        # 处理分类

        async def inner_upload_category(category: str):
            await self.page.locator(
                "body > cnb-root > cnb-app-layout > div.main > as-split > as-split-area:nth-child(2) > div > div > "
                "cnb-spinner > div > cnb-posts-entry > cnb-post-editing-v2 > cnb-post-editor > "
                "div.panel.panel--main >"
                "cnb-category-select-panel > cnb-collapse-panel > "
                "div.panel-content.ng-tns-c31-9.ng-trigger.ng-trigger-openClosePanel.cnb-panel-body > div > div > "
                "cnb-post-category-select > cnb-tree-category-select > div > nz-tree-select > div").click()
            await self.page.locator(
                "body > cnb-root > cnb-app-layout > div.main > as-split > as-split-area:nth-child(2) > div > div > "
                "cnb-spinner > div > cnb-posts-entry > cnb-post-editing-v2 > cnb-post-editor > "
                "div.panel.panel--main >"
                "cnb-category-select-panel > cnb-collapse-panel > "
                "div.panel-content.ng-tns-c31-9.ng-trigger.ng-trigger-openClosePanel.cnb-panel-body > div > div > "
                "cnb-post-category-select > cnb-tree-category-select > div > nz-tree-select > div > "
                "nz-select-search >"
                "input").fill(
                category)
            await self.page.locator(
                ".cdk-overlay-connected-position-bounding-box").locator("nz-tree-node").first.click()
            await self.page.locator(
                "body > cnb-root > cnb-app-layout > div.main > as-split > as-split-area:nth-child(2) > div > div > "
                "cnb-spinner > div > cnb-posts-entry > cnb-post-editing-v2 > cnb-post-editor > "
                "div.panel.panel--main >"
                "cnb-site-category-selector > cnb-collapse-panel > "
                "div.cnb-panel-header.ng-tns-c31-11.cnb-panel-header-clickable > span:nth-child(2)").click()
            await self.page.locator(
                "body > cnb-root > cnb-app-layout > div.main > as-split > as-split-area:nth-child(2) > div > div "
                "> cnb-spinner > div > cnb-posts-entry > cnb-post-editing-v2 > cnb-post-editor > "
                "div.panel.panel--main > cnb-site-category-selector > cnb-collapse-panel > "
                "div.panel-content.ng-tns-c31-11.ng-trigger.ng-trigger-openClosePanel.cnb-panel-body > "
                "div").locator(
                "div", has_text=re.compile(category, re.IGNORECASE)).first.click()

        await self.double_try_single_data(
            'category',
            inner_upload_category,
            inner_upload_category
        )

        await self.page.locator(
            "#tags > div > div > nz-select > nz-select-top-control > nz-select-search > input").click()
        tag_selector = self.page.locator(".cdk-virtual-scroll-content-wrapper")

        # 处理标签

        async def inner_upload_tag(tag: str):
            await self.page.locator(
                "#tags > div > div > nz-select > nz-select-top-control > nz-select-search > input").fill(tag)
            await tag_selector.locator("span", has_text=re.compile(tag, re.IGNORECASE)).first.click()

        await self.double_try_data(
            'tags',
            inner_upload_tag,
            inner_upload_tag
        )
        wait_random_time()
        async with self.page.expect_response("https://i.cnblogs.com/api/posts") as response:
            submit_button = self.page.locator(
                "body > cnb-root > cnb-app-layout > div.main > as-split > as-split-area:nth-child(2) > div > div > "
                "cnb-spinner > div > cnb-posts-entry > cnb-post-editing-v2 > cnb-post-editor > div.panel--bottom > "
                "cnb-spinner > div > cnb-submit-buttons > "
                "button.cnb-button.d-inline-flex.align-items-center.ng-star-inserted"
            )
            await submit_button.dblclick()
            data = await response.value
            data = await data.body()
            data = json.loads(data.decode('utf-8'))
            return 'https:' + data['url']

    async def convert_html_path(self, content: str) -> str:
        await self.page.locator("#editor-switcher").click()
        await self.page.locator("#cdk-overlay-0 > div > ul > li:nth-child(2)").click()
        soup = BeautifulSoup(content, 'html.parser')
        img_tags = soup.find_all('img')
        for img in img_tags:
            img['src'] = await self.upload_img(img['src'])
        return str(soup)

    async def upload_img(self, img_path: str) -> str:
        await self.page.locator(
            "#editor-wrapper > cnb-tinymce5 > cnb-spinner > div > div.tox.tox-tinymce > div.tox-editor-container > "
            "div.tox-editor-header > div.tox-toolbar-overlord > div:nth-child(2) > div:nth-child(2) > "
            "button:nth-child(1) > span").click()
        await self.page.locator('div > div.tox-dialog__body-nav').locator('div', has_text='上传').click()
        async with self.page.expect_response("https://upload.cnblogs.com/imageuploader/CorsUpload") as first:
            async with self.page.expect_file_chooser() as fc_info:
                await self.page.locator("div > div.tox-dialog__body-content > div > div > div > div > button").click()
                file_chooser = await fc_info.value
                await file_chooser.set_files(img_path)
        resp = await first.value
        resp_body = await resp.body()
        data = json.loads(resp_body.decode('utf-8'))
        await self.page.locator(
            "body > div.tox.tox-silver-sink.tox-tinymce-aux > div > div.tox-dialog > div.tox-dialog__header > button "
            "> div").click()
        return data['message']
