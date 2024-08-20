from common.core import config
import asyncio
from playwright.async_api import Page
import typing as t


# TODO 将社区方法接口定义为抽象类，支持自定义每个默认信息
class Community(object):
    """
    社区方法接口
    """

    site_name = '未命名社区'
    site_alias = 'none'

    def __init__(self, browser, ap, asp):
        self.browser = browser
        self.ap = ap
        self.asp = asp
        self.page: "Page" = asyncio.run(self.browser.new_page())

    def process_args(self, columns: list = None, tags: list = None, category: str = None, cover: str = None) \
            -> t.Tuple[list, list, str, str]:
        """
        处理参数
        """
        return (
            columns or config['default'][self.site_alias]['columns'] or config['default']['columns'] or [],
            tags or config['default'][self.site_alias]['tags'] or config['default']['tags'] or [],
            category or config['default'][self.site_alias]['category'] or config['default']['category'],
            cover or config['default'][self.site_alias]['cover'] or config['default']['cover']
        )

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
        ...

    async def async_upload_img(self, img_path: str) -> str:
        """
        上传图片
        :param img_path: 图片路径
        :return: 图片链接
        """
        ...

    async def async_convert_html_img_path(self, content: str, file_path: str) -> str:
        """
        将HTML中的图片路径转换为社区上传图片的路径
        :param file_path: 文件路径
        :param content: HTML内容
        :return: 转换后的HTML内容
        """
        ...
