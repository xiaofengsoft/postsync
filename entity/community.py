from common.config import config
import asyncio
from playwright.async_api import Page
from playwright.async_api import BrowserContext
import typing as t
from common import constant
from common.error import ConfigNotConfiguredError
from utils.data import retrieve_storage_data
import re
import json
from utils.file import get_path
from utils.data import format_json_file


class Community(object):
    """
    根社区类
    """
    site_name: str = constant.UNKNOWN_SITE_NAME
    site_alias: str = constant.UNKNOWN_SITE_ALIAS
    site_storage_mark: tuple = ()

    def __init__(self, context, ap, asp):
        self.context: "BrowserContext" = context
        self.browser: "BrowserContext" = context
        self.ap = ap
        self.asp = asp
        self.page: "Page" = asyncio.run(self.browser.new_page())
        self.is_login: bool = self.check_login_state()

    def process_args(self, columns: list = None, tags: list = None, category: str = None, cover: str = None) \
            -> t.Tuple[list, list, str, str]:
        """
        处理参数
        """
        self.page.set_default_timeout(config['default']['timeout'])
        return (
            columns or config['default']["community"][self.site_alias]['columns'] or config['default']['columns'] or [],
            tags or config['default']["community"][self.site_alias]['tags'] or config['default']['tags'] or [],
            category or config['default']["community"][self.site_alias]['category'] or config['default']['category'],
            cover or config['default']["community"][self.site_alias]['cover'] or config['default']['cover']
        )

    def check_login_state(self) -> bool:
        """
        检查登录状态
        """
        if not config['data']['storage']['path']:
            raise ConfigNotConfiguredError("请设置存储路径")
        if retrieve_storage_data(self.site_storage_mark):
            return True
        return False

    async def login_before_func(self):
        await self.page.evaluate("""() => {
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        }""")
        with open(get_path('data/scripts/stealth.min.js')) as f:
            js = f.read()
        await self.page.add_init_script(js)

    async def login(self, login_url: str, resp_url: str, check_func: t.Callable[[t.AnyStr], bool],
                    before_func: t.Callable = login_before_func):
        """
        登录社区
        :param before_func:
        :param login_url: 登录链接
        :param resp_url: 登录响应链接
        :param check_func: 登录成功的检查函数
        :return: 登录成功返回True，否则返回False
        """
        await before_func(self)
        await self.page.goto(login_url)
        async with self.page.expect_response(re.compile(resp_url),
                                             timeout=constant.INFINITE_TIMEOUT
                                             ) as response:
            data = await response.value
            try:
                data = await data.body()
                data = json.loads(data.decode(constant.FILE_ENCODING))
            except Exception:
                # 说明没有返回信息
                pass
            if check_func(data):
                await self.context.storage_state(path=get_path(config['data']['storage']['path']))
                format_json_file(config['data']['storage']['path'])

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
                             ) -> t.AnyStr:
        """
        异步上传新文章
        :param title: 标题
        :param digest: 摘要
        :param content: 内容
        :param file_path: 文件路径
        :param tags: 标签
        :param category: 分类
        :param cover: 封面
        :param columns: 专栏
        :param topic: 话题
        :return: 上传后的文章链接
        """

    async def async_upload_img(self, img_path: str) -> str:
        """
        上传图片
        :param img_path: 图片路径
        :return: 图片链接
        """
        raise NotImplementedError("请在子类中实现该方法")

    async def async_convert_html_img_path(self, content: str, file_path: str) -> str:
        """
        将HTML中的图片路径转换为社区上传图片的路径
        :param file_path: 文件路径
        :param content: HTML内容
        :return: 转换后的HTML内容
        """
        raise NotImplementedError("请在子类中实现该方法")
