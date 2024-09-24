# -*- coding: utf-8 -*-
import typing as t

from common.apis import StorageType
from entity.community import Community
from common.config import config
from bs4 import BeautifulSoup
import json
import re
from common.func import wait_random_time
from common.func import insert_html_to_element
from common.error import BrowserTimeoutError


class Bilibili(Community):
    """
    Bilibili社区
    """

    site_name = "B站"
    site_alias = "bilibili"
    url_post_new = "https://member.bilibili.com/read/editor/#/web"
    url_redirect_login = "https://passport.bilibili.com/login"
    url_post_manager = "https://member.bilibili.com/platform/upload-manager/opus"
    url = "https://www.bilibili.com/"
    site_storage_mark: t.List[StorageType] = [{
        "type": "cookie",
        "domain": "bilibili.com",
        "name": "DedeUserID",
        "value": ""
    }]

    async def upload(self) -> t.AnyStr:
        if not self.is_login:
            await self.login(
                self.url,
                "https://passport.bilibili.com/x/passport-login/web/login",
                lambda login_data: login_data['code'] == 0)
        # 打开发布页面
        await self.page.goto(self.url_post_new, wait_until='load')
        wait_random_time()
        # 填写标题
        await self.page.locator(
            '#app > div > div.web-editor__wrap > div.b-read-editor > div.b-read-editor__title.mt-l > div > textarea'
        ).fill(self.post['title'])
        wait_random_time()
        # 处理内容
        content = await self.convert_html_path(self.post['contents']['html'])
        wait_random_time()
        await insert_html_to_element(
            self.page,
            "#app > div > div.web-editor__wrap > div.b-read-editor > div.b-read-editor__content.mt-m > "
            "div.b-read-editor__input.mb-l > div.b-read-editor__field > div > div.ql-editor",
            content)
        await self.page.locator(
            "#app > div > div.web-editor__wrap > div.b-read-editor > div.b-read-editor__settings.mt-m > div > div > "
            "div.bre-settings__sec__tit.mb-s.more"
        ).click()
        # 处理分类，选择大分类第一个
        category_zone = self.page.locator(
            "#app > div > div.web-editor__wrap > div.b-read-editor > div.b-read-editor__settings.mt-m > div > "
            "div:nth-child(1) > div.bre-settings__sec__ctn > div.bre-settings__categories"
        )
        try:
            button = category_zone.locator("div", has_text=re.compile(self.post['category']))
            await button.click()
            await category_zone.locator("li:nth-child(1)").click()
        except BrowserTimeoutError:
            button = category_zone.locator("div", has_text=re.compile(
                config['default']['community'][self.site_alias]['category']))
            await button.click()
            await category_zone.locator("li:nth-child(1)").click()
        # 处理封面
        async with self.page.expect_file_chooser() as select_file:
            await self.page.locator(
                "#app > div > div.web-editor__wrap > div.b-read-editor > div.b-read-editor__settings.mt-m > div > "
                "div:nth-child(2) > div.bre-settings__sec__ctn > div.bre-settings__coverbox.cardbox > "
                "div.bre-settings__coverbox__img.skeleton.img"
            ).click()
        file_chooser = await select_file.value
        await file_chooser.set_files(self.post['cover'])
        await self.page.locator(
            "body > div.bre-modal.bre-img-corpper-modal > div > div.bre-modal__content > "
            "div.bre-img-corpper-modal__footer > button.bre-btn.primary").click()
        # 处理话题
        if self.post['topic']:
            await self.page.locator(
                "#app > div > div.web-editor__wrap > div.b-read-editor > div.b-read-editor__settings.mt-m > div > "
                "div:nth-child(3) > div.bre-settings__sec__ctn > div > div > div.bili-topic-selector__search > div > "
                "div > div.bili-topic-search__input > span"
            ).click()
            try:
                await self.page.locator(
                    "#app > div > div.web-editor__wrap > div.b-read-editor > div.b-read-editor__settings.mt-m > div > "
                    "div:nth-child(3) > div.bre-settings__sec__ctn > div > div > div.bili-topic-selector__search > "
                    "div > div > div.bili-topic-search__input > input"
                ).fill(self.post['topic'])
                wait_random_time()
                await self.page.locator(
                    "#app > div > div.web-editor__wrap > div.b-read-editor > div.b-read-editor__settings.mt-m > div > "
                    "div:nth-child(3) > div.bre-settings__sec__ctn > div > div > div.bili-topic-selector__search > "
                    "div > div > div.bili-topic-search__result > div.bili-topic-search__list > div:nth-child(1)"
                ).click()
            except BrowserTimeoutError:
                await self.page.locator(
                    "#app > div > div.web-editor__wrap > div.b-read-editor > div.b-read-editor__settings.mt-m > div > "
                    "div:nth-child(3) > div.bre-settings__sec__ctn > div > div > div.bili-topic-selector__search > "
                    "div > div > div.bili-topic-search__input > input"
                ).fill(config['default']['community'][self.site_alias]['topic'])
                wait_random_time()
                await self.page.locator(
                    "#app > div > div.web-editor__wrap > div.b-read-editor > div.b-read-editor__settings.mt-m > div > "
                    "div:nth-child(3) > div.bre-settings__sec__ctn > div > div > div.bili-topic-selector__search > "
                    "div > div > div.bili-topic-search__result > div.bili-topic-search__list > div:nth-child(1)"
                ).click()

        # 处理标签
        tag_input = self.page.locator(
            "#app > div > div.web-editor__wrap > div.b-read-editor > div.b-read-editor__settings.mt-m > div > "
            "div:nth-child(6) > div.bre-settings__sec__ctn > div > form > div.bre-input.medium > input"
        )
        for tag in self.post['tags']:
            await tag_input.fill(tag)
            await tag_input.press('Enter')
        # 处理专栏
        await self.page.locator(
            "#app > div > div.web-editor__wrap > div.b-read-editor > div.b-read-editor__settings.mt-m > div > "
            "div:nth-child(7) > div.bre-settings__sec__ctn > div.bre-settings__list > button").click()
        column_zone = self.page.locator(
            "body > div.bre-modal.bre-list-modal > div > div.bre-modal__content > div.bre-list-modal__content.mt-m > "
            "div.bre-radio-group.bre-list-modal__items"
        )
        try:
            column = self.post['columns'][0]
            await column_zone.locator("div", has_text=re.compile(column)).first.click()
        except BrowserTimeoutError:
            column = config['default']['community'][self.site_alias]['columns'][0]
            await column_zone.locator("div", has_text=re.compile(column)).first.click()
        await self.page.locator(
            "body > div.bre-modal.bre-list-modal > div > div.bre-modal__content > div.bre-list-modal__footer > button"
        ).click()
        # 发布文章
        async with self.page.expect_response(re.compile("https://data.bilibili.com/v2/log/web")) as resp:
            await self.page.locator(
                "#app > div > div.web-editor__wrap > div.b-read-editor > div.b-read-editor__btns.mt-m.mb-m > "
                "button.bre-btn.primary.size--large"
            ).click()
        data = await resp.value
        data_body = await data.body()
        if data_body.decode('utf-8') != 'ok':
            raise Exception("发布失败")
        await self.page.goto(self.url_post_manager, wait_until='load')
        async with self.context.expect_page() as page_info:
            await self.page.frame_locator(
                "#cc-body > div.cc-content-body.upload-manage > div.opus.content > div > div > iframe").locator(
                "#app > div.opus-list > div.opus-list-cards > div:nth-child(1) > div.opus-card-meta > "
                "div.opus-card-meta__title > div"
            ).click()
        page_value = await page_info.value
        return page_value.url

    async def upload_img(self, img_path: str) -> str:
        async with self.page.expect_response(
                re.compile("https://api.bilibili.com/x/article/creative/article/upcover")) as first:
            async with self.page.expect_file_chooser() as fc_info:
                await self.page.locator(
                    "#app > div > div.web-editor__wrap > div.b-read-editor > div.b-read-editor__content.mt-m > "
                    "div.b-read-editor__toolbar > div > div:nth-child(13)").hover()
                await self.page.locator(
                    "#app > div > div.web-editor__wrap > div.b-read-editor > div.b-read-editor__content.mt-m > "
                    "div.b-read-editor__toolbar > div > div:nth-child(13) > div.tlbr-btn__more > div > ul > "
                    "li:nth-child(1) > div").click()
            file_chooser = await fc_info.value
            await file_chooser.set_files(img_path)
        resp = await first.value
        resp_body = await resp.body()
        data = json.loads(resp_body.decode('utf-8'))
        return data['data']['url']

    async def convert_html_path(self, content: str) -> str:
        soup = BeautifulSoup(content, 'html.parser')
        img_tags = soup.find_all('img')
        for img in img_tags:
            img['src'] = await self.upload_img(img['src'])
        return str(soup)

