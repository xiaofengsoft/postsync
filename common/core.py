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
            if config['app']['debug']:
                raise
            else:
                return site_instance.site_name, "发生错误"
        else:
            return site_instance.site_name, post_new_url
