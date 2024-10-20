from types import SimpleNamespace
from playwright.async_api import async_playwright

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
from utils.file import get_path
from utils.data import convert_html_img_path_to_abs_path, convert_md_img_path_to_abs_path
import argparse
from typing import List
from common.apis import Post, PostPaths, PostArguments, PostContents
from common.constant import *
import typing as t
from playwright.async_api import BrowserContext, Browser


# 执行所有操作的总流程

class ProcessCore(object):
    def __init__(self, is_pass_args_by_cmd: bool = True, args: PostArguments = None):
        # 加载配置
        self.context: t.Optional[BrowserContext] = None
        self.browser: t.Optional[Browser] = None
        self.results: t.Optional[Result] = None
        if is_pass_args_by_cmd:
            parser = PostArgumentParser()
            self.args = parser.parse_args()
        else:
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
        try:
            self.args.topic = config['default']['topic'] if not self.args.topic else self.args.topic
            self.args.category = config['default']['category'] if not self.args.category else self.args.category
            self.args.cover = config['default']['cover'] if not self.args.cover else self.args.cover
            self.args.tags = config['default']['tags'] if not self.args.tags else self.args.tags
            self.args.columns = config['default']['columns'] if not self.args.columns else self.args.columns
        except KeyError as e:
            raise ConfigurationLackError('缺少配置项 {}'.format(e))
        if self.args.sites is None or self.args.sites == [] or len(self.args.sites) == 0:
            self.args.sites = config['default']['community'].keys()
        for site in self.args.sites:
            if site not in config['default']['community'].keys():
                raise CommunityNotExistError('社区 {} 不存在'.format(site))
        with open(self.file_paths['html'], 'r', encoding='utf-8') as f:
            contents['html'] = f.read()
        with open(self.file_paths['md'], 'r', encoding='utf-8') as f:
            contents['md'] = f.read()
        digest = self.args.digest or contents['md'][0:config['default']['digest']['length']]
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
        self.browser, self.context,asp = await utils.browser.create_context(headless=config['default']['headless'])
        # 读取存储文件
        tasks = []
        for site in self.post['sites']:
            task = self.upload_post_one_site(site)
            tasks.append(task)
        results = await asyncio.gather(*tasks, return_exceptions=config['app']['debug'])
        exceptions = [result for result in results if isinstance(result, Exception)]
        if exceptions:
            raise BrowserExceptionGroup(exceptions)
        await self.context.close()
        await asp.__aexit__()
        self.results = Result(code=1, message='上传成功！！！', data=results)

    async def upload_post_one_site(self, site: str):
        """
        同步上传文本到指定站点
        通过反射技术，根据社区名称反射获取类名，调用接口相应方法上传
        :return: 上传的文本链接
        """
        site_cls = import_module('entity.' + site.strip())
        site_instance = getattr(site_cls, site.strip().capitalize())
        site_instance = site_instance(
            browser=self.browser,
            context=self.context,
            post=self.post,
        )
        try:
            post_new_url = await site_instance.upload()
        except BrowserError:
            if config['app']['debug']:
                raise
            else:
                return site_instance.site_name, "发生错误"
        else:
            return site_instance.site_name, post_new_url


class PostArgumentParser(argparse.ArgumentParser):
    """
    继承自argparse.ArgumentParser，重写exit方法，防止打印额外内容
    """

    def __init__(self, **kwargs):
        super().__init__(
            prog=config['app']['name'],
            description=config['app']['description'],
            epilog=config['app']['epilog'],
            exit_on_error=True,
            **kwargs)  # 禁止自动捕获异常
        self.add_optional_arguments([
            ('-ti', '--title', '文档标题', str),
            ('-d', '--digest', '文档的摘要', str),
            ('-ca', '--category', '文档的分类', str),
            ('-co', '--cover', '文档的封面', str),
            ('-to', '--topic', '文档的话题', str)
        ])
        self.add_number_arguments([
            ('-t', '--tags', '文档的标签', str),
            ('-cl', '--columns', '文档的专栏', str)
        ])
        self.add_argument(
            '-f', '--file',
            help='需要同步的文件路径',
            type=str,
            required=True
        )
        self.add_argument(
            '-s', '--sites',
            help='要上传的网站列表，必须从给定的网站列表中选择 %(choices)s，默认全部上传',
            type=str,
            choices=config['default']['community'].keys(),
            nargs='*'
        )
        self.add_argument(
            '-v', '--version',
            action='version',
            version='%(prog)s ' + config['app']['version'],
            help='查看版本号'
        )

    def add_optional_arguments(self, optional_arguments: List[tuple[str, str, str, type]]):
        """
        批量添加可选参数
        :param optional_arguments: 可选参数列表
        :return:
        """
        self.add_arguments(optional_arguments, nargs='?')

    def add_number_arguments(self, arguments: List[tuple[str, str, str, type]]):
        """
        批量添加参数
        :param arguments: 参数列表
        :return:
        """
        self.add_arguments(arguments, nargs='*')

    def add_arguments(self, arguments: List[tuple[str, str, str, type]], **kwargs):
        """
        批量添加参数
        :param arguments: 参数列表
        :param kwargs: 参数字典
        :return:
        """
        for arg in arguments:
            self.add_argument(arg[0], arg[1], help=arg[2], type=arg[3], **kwargs)

    def error(self, message: str):
        if config['app']['debug']:
            super().error(message)
        else:
            print(message)
        self.exit()
