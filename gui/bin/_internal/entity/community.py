from abc import ABCMeta, abstractmethod

import asyncio
class Community(metaclass=ABCMeta):
    """
    社区方法接口
    """

    site_name = ''

    def __init__(self, browser, ap,asp):
        self.browser = browser
        self.ap = ap
        self.asp = asp
        self.page = asyncio.run(self.browser.new_page())



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
                 ) -> str:
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

    @abstractmethod
    async def async_upload_img(self, img_path: str) -> str:
        """
        上传图片
        :param img_path: 图片路径
        :return: 图片链接
        """
        ...

    @abstractmethod
    async def async_convert_html_img_path(self, content: str,file_path: str) -> str:
        """
        将HTML中的图片路径转换为社区上传图片的路径
        :param file_path: 文件路径
        :param content: HTML内容
        :return: 转换后的HTML内容
        """
        ...


