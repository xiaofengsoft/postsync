from playwright.async_api import async_playwright

import common.func
from common.func import (load_yaml)
from common.func import get_root_path
from common.func import get_file_name_ext
from common.func import convert_html_to_docx
from os.path import join
from common.result import Result
from common.func import convert_md_to_html
import asyncio
from importlib import import_module
from common.error import FileNotReferencedError, BrowserError
from common.error import CommunityNotExistError
from playwright.async_api import Error as PlaywrightError

def get_config() -> dict:
    return load_yaml(join(get_root_path(), 'config.yaml'))


config = get_config()
config['default']['cover'] = join(get_root_path(), config['default']['cover'])


def process_args(args) -> tuple[str, str, str, str, str, str, str, list, list, list]:
    """
    处理命令行参数
    :param args: 命令行参数
    :return: 返回处理后的参数
    """
    if args.file is None:
        raise FileNotReferencedError('请指定文件')
    file = args.file
    (title, ext) = get_file_name_ext(file)
    if ext == '.md' or ext == '.markdown' or ext == '.mdown' or ext == '':
        # 如果是markdown文件，则转换为html
        file = convert_md_to_html(file)
    # 生成docx文件
    docx_file = convert_html_to_docx(file)
    stream_file = open(file, 'r', encoding='utf-8')
    content = stream_file.read()
    stream_file.close()
    if args.title is not None:
        title = args.title
    digest = args.digest
    if digest is None:
        digest = content[:config['default']['digest']['length']]
    topic = args.topic
    if topic is None:
        topic = config['default']['topic']
    sites = args.site
    if sites is None or sites == [] or len(sites) == 0:
        sites = config['default']['community'].keys()
    for site in sites:
        if site not in config['default']['community'].keys():
            raise CommunityNotExistError('社区 {} 不存在'.format(site))
    return file, title, content, digest, args.category, args.cover, topic, sites, args.tag, args.column


async def async_post_file(file: str, title: str, content: str, digest: str, category: str, cover: str, topic: str,
                          sites: list,
                          tags: list,
                          columns: list) -> Result:
    """
    异步上传文件
    :param file: 文件路径
    :param title: 标题
    :param content: 内容
    :param digest: 摘要
    :param category: 分类
    :param cover: 封面
    :param topic: 话题
    :param sites: 站点列表
    :param tags: 标签列表
    :param columns: 栏目列表
    :return: Result对象 data为上传的文件链接数组
    """
    asp = async_playwright()
    ap = await asp.start()
    viewport = config['default']['no_viewport'] if config['default']['no_viewport'] else {
        'width': config['view']['width'], 'height': config['view']['height']}
    browser = await ap.chromium.launch_persistent_context(
        base_url=config['default']['url'],
        channel=config['default']['browser'],
        headless=config['default']['headless'],
        user_data_dir=config['data']['user']['dir'],
        no_viewport=viewport,
        args=['--start-maximized'],
        devtools=bool(config['default']['devtools'])
    )
    tasks = []
    for site in sites:
        task = async_post_text(browser, ap, asp, file, title, content, digest, site, category, cover, topic, tags,
                               columns
                               )
        tasks.append(task)
    result = await asyncio.gather(*tasks)
    await browser.close()
    await asp.__aexit__()
    return Result(code=1, message='上传成功！！！', data=result)


async def async_post_text(browser: object, ap: object, asp: object, file_path: str, title: str, content: str,
                          digest: str | object,
                          site: str,
                          category: str, cover: str,
                          topic: str,
                          tags: list,
                          columns: list) -> (
        str, str):
    """
    同步上传文本到指定站点
    通过反射技术，根据社区名称反射获取类名，调用接口相应方法上传
    :param browser: 浏览器对象
    :param ap: 异步playwright对象
    :param asp: 异步playwright启动对象
    :param file_path: 文件路径
    :param title: 标题
    :param content: 文本内容
    :param digest: 摘要内容
    :param site: 站点名称
    :param tags: 标签列表
    :param category: 分类名称
    :param cover: 封面路径
    :param topic: 话题名称
    :param columns: 栏目名称
    :return: 上传的文本链接
    """
    site_cls = import_module('entity.' + site.strip())
    site_instance = getattr(site_cls, site.strip().capitalize())
    site_instance = site_instance(browser=browser, ap=ap, asp=asp)
    try:
        post_new_url = await site_instance.async_post_new(file_path=file_path, title=title, content=content,
                                                          digest=digest,
                                                          tags=tags, category=category, cover=cover, topic=topic,
                                                          columns=columns)
    except PlaywrightError:
        if config['app']['debug']:
            raise
        else:
            return site_instance.site_name, "发生错误"
    else:
        return site_instance.site_name, post_new_url



