import re
from utils.storage import storage_config
from playwright._impl._errors import TargetClosedError
from utils.storage import get_page_local_storage
from common.apis import StorageType
from common.error import BrowserTimeoutError
from utils.data import format_json_file
from utils.file import get_path
import json
from utils.helper import wait_random_time
from utils.data import insert_anti_detection_script
from common.error import ConfigNotConfiguredError, BrowserError
from common import constant
from playwright.async_api import BrowserContext, Browser, Response
from playwright.async_api import Page, Locator
from common.constant import config, INFINITE_TIMEOUT
from common.apis import Post, StorageData
from playwright._impl._async_base import AsyncEventInfo
from bs4 import BeautifulSoup
import time
from types import SimpleNamespace
import utils.browser
from utils.file import get_file_name_ext, convert_html_to_md, convert_md_to_docx, convert_docx_to_html, \
    convert_docx_to_md
from utils.file import convert_html_to_docx
from common.result import Result
from utils.file import convert_md_to_html
import asyncio
from importlib import import_module
from common.error import FileNotReferencedError, BrowserError, CommunityNotExistError, BrowserExceptionGroup, \
    FileNotSupportedError, ConfigurationLackError
from common import constant as c
from utils.data import convert_html_img_path_to_abs_path, convert_md_img_path_to_abs_path
from common.apis import Post, PostPaths, PostArguments, PostContents
from common.constant import *
import typing as t
from playwright.async_api import BrowserContext, Browser


# 执行所有操作的总流程


class ProcessCore(object):
    def __init__(self, args: PostArguments = None):
        # 加载配置
        self.context: t.Optional[BrowserContext] = None
        self.browser: t.Optional[Browser] = None
        self.results: t.Optional[Result] = None
        self.args = SimpleNamespace(**args)
        self.file_paths = self.process_files()
        self.args: PostArguments
        self.post = self.process_args()
        asyncio.run(self.init_browser())

    def process_args(self) -> Post:
        """
        处理命令行参数
        :return: 返回处理后的参数
        """
        contents: PostContents = {}
        if self.args.sites is None or self.args.sites == [] or len(self.args.sites) == 0:
            self.args.sites = config['default']['community'].keys()
        for site in self.args.sites:
            if site not in config['default']['community'].keys():
                raise CommunityNotExistError('社区 {} 不存在'.format(site))
        with open(self.file_paths['html'], 'r', encoding='utf-8') as f:
            contents['html'] = f.read()
        with open(self.file_paths['md'], 'r', encoding='utf-8') as f:
            contents['md'] = f.read()
        digest = self.args.digest or contents['md'][0:
                                                    config['default']['digest']['length']]
        return {
            'title': self.args.title,
            'paths': self.file_paths,
            'digest': digest,
            'category': self.args.category,
            'cover': self.args.cover,
            'topic': self.args.topic,
            'sites': self.args.sites,
            'tags': self.args.tags,
            'columns': self.args.columns,
            'contents': contents
        }

    def process_files(self) -> PostPaths:
        """
        处理文件
        :return:
        """
        if self.args.file is None:
            raise FileNotReferencedError()
        source_file = self.args.file.strip("'\"")  # 去除引号
        title, ext = get_file_name_ext(source_file)
        self.args.title = self.args.title or title  # 没有指定则使用文件名作为标题
        file_paths: PostPaths = {}
        if ext in HTML_EXTENSIONS:
            file_paths['html'] = source_file
            convert_html_img_path_to_abs_path(file_paths['html'])
            file_paths['docx'] = convert_html_to_docx(source_file)
            file_paths['md'] = convert_html_to_md(source_file)
        elif ext in MD_EXTENSIONS:
            file_paths['md'] = source_file
            convert_md_img_path_to_abs_path(file_paths['md'])
            file_paths['html'] = convert_md_to_html(source_file)
            file_paths['docx'] = convert_md_to_docx(source_file)
        elif ext in DOC_EXTENSIONS:
            file_paths['docx'] = source_file
            file_paths['html'] = convert_docx_to_html(source_file)
            file_paths['md'] = convert_docx_to_md(source_file)
        else:
            raise FileNotSupportedError(ext)
        return file_paths

    async def init_browser(self):
        """
        异步上传文件
        """
        self.browser, self.context, asp = await utils.browser.create_context(headless=config['default']['headless'])
        # 读取存储文件
        tasks = []
        for site in self.post['sites']:
            task = self.upload_post_one_site(site)
            tasks.append(task)
        results = await asyncio.gather(*tasks, return_exceptions=config['app']['debug'])
        exceptions = [
            result for result in results if isinstance(result, Exception)]
        if exceptions:
            raise BrowserExceptionGroup(exceptions)
        await self.context.close()
        await asp.__aexit__()
        self.results = Result(code=1, message='上传成功！！！', data=results)

    async def upload_post_one_site(self, site: str):
        """
        同步上传文本到指定站点
        通过反射技术，根据社区名称反射获取类名，调用接口相应方法上传
        如果已经有实例化的社区类，则直接调用实例化的类的方法上传
        :return: 上传的文本链接
        """
        site_instance = utils.browser.get_community_instance(
            site, self.browser, self.context)
        try:
            post_new_url = await site_instance.upload(self.post)
        except BrowserError:
            return site_instance.site_name, "发生错误"
        else:
            return site_instance.site_name, post_new_url


# TODO 单例模式


class Community(object):
    """
    根社区类
    """
    site_name: str = constant.UNKNOWN_SITE_NAME  # 站点名称
    site_alias: str = constant.UNKNOWN_SITE_ALIAS  # 站点别名
    url_post_new: str = ""  # 新建文章链接
    login_url: str = ""  # 登录链接
    url = ""  # 站点链接

    def __init__(self, browser: "Browser" = None, context: "BrowserContext" = None, **kwargs):
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

    async def check_login_state(self, *args, **kwargs) -> bool:
        """
        检查登录状态
        :return: 是否登录
        """
        return config['default']['community'][self.site_alias]['is_login']

    async def login_before_func(self):
        await self._abort_assets_route(['media', 'font'])
        await insert_anti_detection_script(self.page)

    async def login(self, *args, **kwargs) -> bool:
        """
        登录社区
        :return: 登录是否成功
        """
        await self.login_before_func()
        await self.page.goto(self.login_url, wait_until='networkidle')
        # 等待用户确认登录
        while True:
            if constant.is_confirmed.empty():
                await asyncio.sleep(1)
                continue
            confirmation = constant.is_confirmed.get()  # 获取确认值并删除
            if confirmation == -1:
                return False
            if confirmation == self.site_alias:
                constant.config['default']['community'][self.site_alias]['is_login'] = True
                storage_config()
                await self.storage_state(path=get_path(config['data']['storage']['path']))

                return True
            # 如果确认值不匹配，继续等待
            await asyncio.sleep(1)

    async def storage_state(self, path: str):
        """
        存储登录状态
        """
        await self.context.storage_state(path=path)

    async def close(self):
        """
        关闭
        :return:
        """
        await self.context.close()

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
