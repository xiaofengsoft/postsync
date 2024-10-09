# -*- coding: utf-8 -*-
import typing as t
from common.error import BrowserTimeoutError
from playwright.async_api import Browser, BrowserContext
from common.apis import Post, StorageType
from common.constant import config
from utils.helper import wait_random_time
from entity.community import Community
from urllib.parse import quote
import re
from bs4 import BeautifulSoup
from utils.domain import get_domain, join_url_paths
from utils.file import get_file_name_without_ext


class Wordpress(Community):
    site_name = "Wordpress"
    site_alias = "wordpress"
    site_storage_mark:t.List[StorageType] = [{
        "type": "cookie",
        "name": "wordpress_logged_in",
        "domain": get_domain(config['wordpress']['url']),
        "value": ""
    }]
    url = config['wordpress']['url']
    url_post_new = config['wordpress']['url'] + "/wp-admin/post-new.php"
    login_url = config['wordpress']['url'] + "/wp-login.php"
    url_redirect_login = config['wordpress']['url'] + "/user"

    def __init__(self, browser: "Browser", context: "BrowserContext", post: Post, **kwargs):
        super().__init__(browser, context, post, **kwargs)
        if not bool(config['wordpress']['enable']):
            return
        self.url = config['wordpress']['url'] + "/wp-admin/post-new.php"
        self.upload_url = config['wordpress']['url'] + "/wp-admin/upload.php"

    async def upload(self) -> t.AnyStr:
        if not self.is_login:
            await self.login(
                self.login_url,
                re.compile(
                    (join_url_paths(config['wordpress']['domain'],
                                    ["wp-admin", "admin-ajax.php"]) + "$")
                    .replace('.', r'\.')),
                lambda login_data: 0 == 0,
            )
        await self.page.goto(self.url, wait_until='domcontentloaded')
        # 处理参数
        md_content = await self.convert_html_path(self.post['contents']['html'])
        await self.page.goto(self.url, wait_until='load')
        await self.page.get_by_label("选项", exact=True).first.click()
        await self.page.locator(
            "body > div.components-popover__fallback-container > div > div > div > div:nth-child(2) > div:nth-child("
            "2) > button:nth-child(2)").click()
        await self.page.get_by_label("选项", exact=True).first.click()
        wait_random_time()
        await self.page.locator("#inspector-textarea-control-0").fill(self.post['title'])
        await self.page.locator("#post-content-0").fill(md_content)
        await self.page.locator(
            "#editor > div.editor-editor-interface.edit-post-layout.is-mode-text.has-metaboxes.interface-interface"
            "-skeleton > div > div.interface-interface-skeleton__body > "
            "div.interface-navigable-region.interface-interface-skeleton__content > div.editor-text-editor > "
            "div.editor-text-editor__toolbar > button").click()
        # 处理目录
        category_zone = self.page.locator(r"#tabs-0-edit-post\/document-view > div:nth-child(3) > div > "
                                          r"div.editor-post-taxonomies__hierarchical-terms-list")

        async def inner_upload_columns(column: str):
            await category_zone.locator("label", has_text=re.compile(column)).click()

        await self.double_try_data(
            'columns',
            inner_upload_columns,
            inner_upload_columns,
            BrowserTimeoutError,
            TypeError
        )
        # 设置封面
        await self.page.locator(
            r"#tabs-0-edit-post\/document-view > div.components-flex.components-h-stack.components-v-stack.editor"
            r"-post-panel__section.editor-post-summary.css-1i2unhf.e19lxcc00 > div > div.editor-post-featured-image > "
            r"div > button").click()
        await self.page.locator("#menu-item-upload").click()
        async with self.page.expect_file_chooser() as response_info:
            await self.page.locator("#__wp-uploader-id-1").click()
            filechooser = await response_info.value
            await filechooser.set_files(self.post['cover'])
        await self.page.locator(
            "#__wp-uploader-id-0 > div.media-frame-toolbar > div > div.media-toolbar-primary.search-form > button"
        ).click()
        # 添加摘要
        await self.page.locator(
            r"#tabs-0-edit-post\/document-view > div.components-flex.components-h-stack.components-v-stack.editor"
            r"-post-panel__section.editor-post-summary.css-1i2unhf.e19lxcc00 > div > div:nth-child(3) > div > "
            r"button").click()
        await self.page.locator("#inspector-textarea-control-1").fill(self.post['digest'])
        # 处理标签
        tag_input = self.page.locator("#components-form-token-input-0")
        for tag in self.post['tags']:
            await tag_input.fill(tag)
            await tag_input.press("Enter")
        async with self.page.expect_response(re.compile(r"wp-json/wp/v2/posts")) as response_info:
            await self.page.locator(
                "#editor > div.editor-editor-interface.edit-post-layout.is-mode-visual.has-metaboxes.interface"
                "-interface-skeleton.has-footer > div.interface-interface-skeleton__editor > "
                "div.interface-navigable-region.interface-interface-skeleton__header > div > "
                "div.editor-header__settings > "
                "button.components-button.editor-post-publish-panel__toggle.editor-post-publish-button__button.is"
                "-primary.is-compact").click()
            await self.page.locator(
                "#editor > div.editor-editor-interface.edit-post-layout.is-mode-visual.has-metaboxes.interface"
                "-interface-skeleton.has-footer > div.interface-interface-skeleton__editor > "
                "div.interface-interface-skeleton__body > "
                "div.interface-navigable-region.interface-interface-skeleton__actions > div:nth-child(2) > div > div "
                "> div.editor-post-publish-panel__header > div.editor-post-publish-panel__header-publish-button > "
                "button").click()
            response = await response_info.value
            data = await response.json()
            return data['guid']['rendered']

    async def upload_img(self, img_path: str) -> str:
        wait_random_time()
        file_name = get_file_name_without_ext(img_path)
        # 中文的话转化为Unicode编码
        if not re.match(r'^[a-zA-Z0-9_]+$', file_name):
            file_name = quote(file_name)
        file_name = f'-{file_name}-'
        async with self.page.expect_response(
                re.compile(file_name)
        ) as response_info:
            async with self.page.expect_file_chooser() as fc_info:
                await self.page.locator("#__wp-uploader-id-1").click()
                filechooser = await fc_info.value
                await filechooser.set_files(img_path)
        response = await response_info.value
        return response.url

    async def convert_html_path(self, content: str) -> str:
        # 处理图片
        await self.page.goto(self.upload_url)
        await self.page.locator("#wp-media-grid > a").click()
        soup = BeautifulSoup(content, 'html.parser')
        img_tags = soup.find_all('img')
        for img in img_tags:
            img['src'] = await self.upload_img(img['src'])
        return str(soup)

