# -*- coding: utf-8 -*-
import time

from common.config import config
from entity.community import Community
import json
import re
from bs4 import BeautifulSoup
from utils.domain import get_domain, join_url_paths


class Wordpress(Community):
    site_name = "Wordpress"
    site_alias = "wordpress"
    site_storage_mark = (
        get_domain(config['wordpress']['url']),
    )
    login_url = config['wordpress']['url'] + "/wp-login.php"

    def __init__(self, context, ap, asp):
        super().__init__(context, ap, asp)
        if not bool(config['wordpress']['enable']):
            return
        self.url = config['wordpress']['url'] + "/wp-admin/post-new.php"
        self.upload_url = config['wordpress']['url'] + "/wp-admin/upload.php"

    async def async_post_new(self, title: str, digest: str, content: str, file_path: str = None, tags: list = None,
                             category: str = None, cover: str = None, columns: list = None, topic: str = None) -> str:
        # 处理参数
        columns, tags, category, cover = super().process_args(columns, tags, category, cover)
        if not self.is_login:
            await self.login(
                self.login_url,
                join_url_paths(config['wordpress']['url'], ["wp-admin", "admin-ajax.php"])+"$",
                lambda login_data: 0 == 0,
            )
        await self.page.goto(self.url, wait_until='load', timeout=10000)
        # 处理参数
        md_file_path = file_path.replace('.html', '.md')
        md_content = await self.async_convert_html_img_path(content, file_path)
        await self.page.goto(self.url, wait_until='load', timeout=10000)
        await self.page.get_by_label("选项", exact=True).first.click()
        await self.page.locator(
            "body > div.components-popover__fallback-container > div > div > div > div:nth-child(2) > div:nth-child(2) > button:nth-child(2)").click()
        await self.page.get_by_label("选项", exact=True).first.click()
        time.sleep(0.1)
        await self.page.locator("#inspector-textarea-control-0").fill(title)
        await self.page.locator("#post-content-0").fill(md_content)
        await self.page.locator(
            "#editor > div.editor-editor-interface.edit-post-layout.is-mode-text.has-metaboxes.interface-interface-skeleton > div > div.interface-interface-skeleton__body > div.interface-navigable-region.interface-interface-skeleton__content > div.editor-text-editor > div.editor-text-editor__toolbar > button").click()
        # 处理目录
        await self.page.locator("#inspector-text-control-0").fill(category)
        time.sleep(0.1)
        elements = await self.page.query_selector_all(".components-checkbox-control__label")
        for element in elements:
            await element.click()
        # 设置封面
        await self.page.locator(
            r"#tabs-0-edit-post\/document-view > div.components-flex.components-h-stack.components-v-stack.editor-post-panel__section.editor-post-summary.css-1i2unhf.e19lxcc00 > div > div.editor-post-featured-image > div > button").click()
        await self.page.locator("#menu-item-upload").click()
        async with self.page.expect_file_chooser() as response_info:
            await self.page.locator("#__wp-uploader-id-1").click()
            filechooser = await response_info.value
            await filechooser.set_files(cover)
        await self.page.locator(
            "#__wp-uploader-id-0 > div.media-frame-toolbar > div > div.media-toolbar-primary.search-form > button").click()
        # 添加摘要
        await self.page.locator(
            r"#tabs-0-edit-post\/document-view > div.components-flex.components-h-stack.components-v-stack.editor-post-panel__section.editor-post-summary.css-1i2unhf.e19lxcc00 > div > div:nth-child(3) > div > button").click()
        await self.page.locator("#inspector-textarea-control-1").fill(digest)
        # 处理标签
        tag_input = self.page.locator("#components-form-token-input-0")
        for tag in tags:
            await tag_input.fill(tag)
            await tag_input.press("Enter")
        async with self.page.expect_response(re.compile(r"wp-json/wp/v2/posts")) as response_info:
            await self.page.locator(
                "#editor > div.editor-editor-interface.edit-post-layout.is-mode-visual.has-metaboxes.interface-interface-skeleton.has-footer > div.interface-interface-skeleton__editor > div.interface-navigable-region.interface-interface-skeleton__header > div > div.editor-header__settings > button.components-button.editor-post-publish-panel__toggle.editor-post-publish-button__button.is-primary.is-compact").click()
            await self.page.locator(
                "#editor > div.editor-editor-interface.edit-post-layout.is-mode-visual.has-metaboxes.interface-interface-skeleton.has-footer > div.interface-interface-skeleton__editor > div.interface-interface-skeleton__body > div.interface-navigable-region.interface-interface-skeleton__actions > div:nth-child(2) > div > div > div.editor-post-publish-panel__header > div.editor-post-publish-panel__header-publish-button > button").click()
            response = await response_info.value
            data = await response.json()
            return data['guid']['rendered']

    async def async_upload_img(self, img_path: str) -> str:
        async with self.page.expect_response(re.compile(r"admin-ajax\.php")) as response_info:
            async with self.page.expect_file_chooser() as fc_info:
                await self.page.locator("#__wp-uploader-id-1").click()
                filechooser = await fc_info.value
                await filechooser.set_files(img_path)
        response = await response_info.value
        data = await response.body()
        data = json.loads(data.decode('utf-8'))
        try:
            res = str(data['data']['url'])
        except Exception:
            res = str(data['data'][0]['url'])
        return res

    async def async_convert_html_img_path(self, content: str, file_path: str) -> str:
        # 处理图片
        await self.page.goto(self.upload_url)
        await self.page.locator("#wp-media-grid > a").click()
        soup = BeautifulSoup(content, 'html.parser')
        img_tags = soup.find_all('img')
        for img in img_tags:
            img['src'] = await self.async_upload_img(img['src'])
        return str(soup)
