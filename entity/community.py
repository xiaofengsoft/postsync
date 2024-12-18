import re
from bs4 import BeautifulSoup
from playwright._impl._async_base import AsyncEventInfo
from common.apis import Post, StorageData
from common.constant import config, INFINITE_TIMEOUT
import asyncio
from playwright.async_api import Page, Locator
from playwright.async_api import BrowserContext, Browser, Response
import typing as t
from common import constant
from common.error import ConfigNotConfiguredError, BrowserError
from utils.data import insert_anti_detection_script
from utils.helper import wait_random_time
import json
from utils.file import get_path
from utils.data import format_json_file
from common.error import BrowserTimeoutError
from common.apis import StorageType
from utils.storage import get_page_local_storage


# TODO 单例模式
class Community(object):
    """
    根社区类
    """
    site_name: str = constant.UNKNOWN_SITE_NAME  # 站点名称
    site_alias: str = constant.UNKNOWN_SITE_ALIAS  # 站点别名
    url_post_new: str = ""  # 新建文章链接
    check_login_expect_str: t.Pattern | str = ""  # 检测登录跳转URL
    url = ""  # 站点链接

    def __init__(self, browser: "Browser", context: "BrowserContext", **kwargs):
        """
        初始化
        可以用来按照模板步骤上传文章
        也可以判断是否已经登录
        :param browser:
        :param context:
        """
        self.post = None
        self.browser = browser
        self.context = context
        self.page: "Page" = asyncio.run(
            self.context.new_page()
        )

    async def check_login_state(self, abort_assets: t.List[str] = [
        "image", "font", "media"
    ], check_login_expect_str: str | t.Pattern = None) -> bool:
        """
        检查登录状态
        """
        check_login_expect_str = check_login_expect_str or self.check_login_expect_str
        await self._abort_assets_route(abort_assets)
        try:
            async with self.page.expect_navigation(
                url=re.compile(check_login_expect_str),
            ):
                await self.page.goto(self.url_post_new)
            return False
        except BrowserTimeoutError as e:
            return True

    async def login_before_func(self):
        await self._abort_assets_route(['media', 'font'])
        await insert_anti_detection_script(self.page)

    async def login(
            self, login_url: str, resp_url: t.Union[t.Pattern, str],
            check_func: t.Callable[[t.AnyStr], bool],
            before_func: t.Callable = login_before_func
    ) -> bool:
        """
        登录社区
        :param before_func:
        :param login_url: 登录链接
        :param resp_url: 登录响应链接,支持正则
        :param check_func: 登录成功的检查函数
        :return: 是否登录成功
        """
        await before_func(self)
        self.page.set_default_timeout(
            INFINITE_TIMEOUT
        )
        await self.page.goto(login_url, wait_until='commit')
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
                data = json.loads(data.decode(encoding=constant.FILE_ENCODING))
            except json.JSONDecodeError as e:
                return False
            except BrowserError as e:
                pass
            if code in constant.HTTP_SUCCESS_STATUS_CODES and check_func(data):
                await self.context.storage_state(path=get_path(config['data']['storage']['path']))
                format_json_file(config['data']['storage']['path'])
                await self.page.close()
                return True
        return False

    async def before_upload(self, post: Post):
        """
        处理参数
        """
        self.post = post
        self.page.set_default_timeout(
            int(config['default']['community'][self.site_alias]['timeout'])
            or int(config['default']['timeout'])
        )
        self.post['columns'] = self.post['columns'] or config['default']["community"][self.site_alias]['columns'] or config['default']['columns']
        self.post['tags'] = self.post['tags'] or config['default']["community"][self.site_alias]['tags'] or config['default']['tags']
        self.post['category'] = self.post['category'] or config['default']["community"][self.site_alias]['category'] or config['default'][
            'category']
        self.post['cover'] = self.post['cover'] or config['default']["community"][self.site_alias]['cover'] or config['default']['cover']
        await self._abort_assets_route(['image', 'font', 'media'])

    async def upload(self, post: Post) -> t.AnyStr:
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
        soup = BeautifulSoup(content, 'html.parser')
        img_tags = soup.find_all('img')
        for img in img_tags:
            img['src'] = await self.upload_img(img['src'])
        return str(soup)

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

    async def double_try_data[T: t.Callable](
            self,
            index: t.Literal['columns', 'tags'],
            main_func: T, other_func: T,
            first_error: t.Type[Exception] = BrowserTimeoutError,
            second_error: t.Type[Exception] = BrowserTimeoutError):
        """
        双重尝试数据
        :param index:
        :param main_func:
        :param other_func:
        :param first_error:
        :param second_error:
        :return:
        """
        items = self.post[index]
        try:
            for item in items:
                await main_func(item)
        except first_error:
            items = config['default']["community"][self.site_alias][index]
            try:
                for item in items:
                    await other_func(item)
            except second_error:
                pass

    async def double_try_first_index[T: t.Callable](
            self,
            index: t.Literal['columns', 'tags'],
            main_func: T, other_func: T,
            first_error: t.Type[Exception] = BrowserTimeoutError,
            second_error: t.Type[Exception] = BrowserTimeoutError
    ):
        try:
            item = self.post[index][0]
            await main_func(item)
        except first_error:
            try:
                item = config['default']["community"][self.site_alias][index][0]
                await other_func(item)
            except second_error:
                pass

    async def double_try_single_data[T: t.Callable](
            self,
            index: t.Literal['category', 'topic'],
            main_func: T, other_func: T,
            first_error: t.Type[Exception] = BrowserTimeoutError,
            second_error: t.Type[Exception] = BrowserTimeoutError
    ):
        """
        双重尝试单条记录的数据
        :param index:
        :param main_func:
        :param other_func:
        :param first_error:
        :param second_error:
        :return:
        """
        try:
            item = self.post[index]
            await main_func(item)
        except first_error:
            try:
                item = config['default']["community"][self.site_alias][index]
                await other_func(item)
            except second_error:
                pass

    async def double_try(
            self,
            main_func: t.Callable,
            other_func: t.Callable,
            first_error: t.Type[Exception] = BrowserTimeoutError,
            second_error: t.Type[Exception] = BrowserTimeoutError
    ):
        try:
            await main_func()
        except first_error:
            try:
                await other_func()
            except second_error:
                pass

    async def _abort_assets_route(self, abort_assets: t.List[str] = [
        "image", "stylesheet", "font", "media"
    ]):
        """_summary_: 处理图片、样式、字体等资源请求

        Args:
            abort_assets (t.List[str], optional): 需要abort的资源类型. Defaults to ["image", "stylesheet", "font", "media"].
        """
        async def route_abort(route, request):
            if request.resource_type in abort_assets:
                await route.abort()
            else:
                await route.continue_()
            return route
        await self.page.route("**/*", route_abort)
