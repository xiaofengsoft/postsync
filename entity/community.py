from playwright._impl._async_base import AsyncEventInfo
from common.apis import Post
from common.config import config
import asyncio
from playwright.async_api import Page, Locator
from playwright.async_api import BrowserContext, Browser, Response
import typing as t
from common import constant
from common.error import ConfigNotConfiguredError
from utils.data import retrieve_storage_data, insert_anti_detection_script
from common.func import wait_random_time
import json
from utils.file import get_path
from utils.data import format_json_file
from common.error import BrowserTimeoutError


class Community(object):
    """
    根社区类
    """
    site_name: str = constant.UNKNOWN_SITE_NAME
    site_alias: str = constant.UNKNOWN_SITE_ALIAS
    site_storage_mark: tuple = ()

    def __init__(self, browser: "Browser", context: "BrowserContext", post: Post):
        self.browser = browser
        self.context = context
        self.post = post
        self.page: "Page" = asyncio.run(self.context.new_page())
        self.is_login: bool = asyncio.run(self.check_login_state())
        self.process_args()

    def process_args(self):
        """
        处理参数
        """
        self.page.set_default_timeout(
            int(config['default']['community'][self.site_alias]['timeout'])
            or int(config['default']['timeout'])
        )
        self.post['columns'] = self.post['columns'] or config['default']["community"][self.site_alias]['columns']
        self.post['tags'] = self.post['tags'] or config['default']["community"][self.site_alias]['tags']
        self.post['category'] = self.post['category'] or config['default']["community"][self.site_alias]['category']
        self.post['cover'] = self.post['cover'] or config['default']["community"][self.site_alias]['cover']

    async def check_login_state(self) -> bool:
        """
        检查登录状态
        """
        if not config['data']['storage']['path']:
            raise ConfigNotConfiguredError("请设置存储路径")
        if retrieve_storage_data(self.site_storage_mark, get_path(config['data']['storage']['path'])):
            return True
        print(f"{self.site_name}尚未登录")
        return False

    async def login_before_func(self):
        await insert_anti_detection_script(self.page)

    async def login(
            self, login_url: str, resp_url: t.Union[t.Pattern, str],
            check_func: t.Callable[[t.AnyStr], bool],
            before_func: t.Callable = login_before_func
    ):
        """
        登录社区
        :param before_func:
        :param login_url: 登录链接
        :param resp_url: 登录响应链接,支持正则
        :param check_func: 登录成功的检查函数
        :return:
        """
        await before_func(self)
        await self.page.goto(login_url)
        response: t.Union[AsyncEventInfo["Response"], Response]
        wait_random_time()
        async with self.page.expect_response(
                resp_url,
                timeout=constant.INFINITE_TIMEOUT
        ) as response:
            data = await response.value
            code = data.status
            try:
                data = await data.body()
                data = json.loads(data.decode(constant.FILE_ENCODING))
            except Exception:
                # 说明没有返回信息
                pass
            if code in constant.HTTP_SUCCESS_STATUS_CODES and check_func(data):
                await self.context.storage_state(path=get_path(config['data']['storage']['path']))
                format_json_file(config['data']['storage']['path'])
                await self.page.close()
                print(f"{self.site_name}登录成功，已关闭{self.site_name}页面")

    async def upload(self) -> t.AnyStr:
        """
        异步上传新文章
        :return: 上传后的文章链接
        """
        raise NotImplementedError("请在子类中实现该方法")

    async def upload_img(self, img_path: str) -> str:
        """
        上传图片
        :param img_path: 图片路径
        :return: 图片链接
        """
        raise NotImplementedError("请在子类中实现该方法")

    async def convert_html_path(self, content: str) -> str:
        """
        将HTML中的图片路径转换为社区上传图片的路径
        :param content: HTML内容
        :return: 转换后的HTML内容
        """
        raise NotImplementedError("请在子类中实现该方法")

    async def convert_md_path(self, content: str) -> str:
        """
        将MD中的图片路径转换为社区上传图片的路径
        :param content: MD内容
        :return: 转换后的MD内容
        """
        raise NotImplementedError("请在子类中实现该方法")

    async def convert_docx_path(self, content: str) -> str:
        """
        将DOCX中的图片路径转换为社区上传图片的路径
        :param content: DOCX内容
        :return: 转换后的DOCX内容
        """
        raise NotImplementedError("请在子类中实现该方法")

    async def upload_tags(
            self, tag_selector: t.Union[Locator, Page],
            loop_mid_func: t.Callable[[str], t.Coroutine[t.Any, t.Any, None]],
    ):
        """
        上传标签
        :param loop_mid_func: 循环中间函数
        :param tag_selector:  标签选择器
        :return:
        """
        tags = self.post['tags']
        try:
            for tag in tags:
                wait_random_time()
                await loop_mid_func(tag)
                await tag_selector.first.click()
        except BrowserTimeoutError:
            tags = config['default']["community"][self.site_alias]['tags']
            for tag in tags:
                wait_random_time()
                await loop_mid_func(tag)
                await tag_selector.first.click()
