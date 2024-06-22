from playwright.async_api import async_playwright
from common.func import (load_yaml)
from common.func import get_root_path
from common.func import get_abs_path
from common.func import get_file_name_ext
from os.path import join
from common.result import Result
from common.func import convert_md_to_html
import asyncio
from importlib import import_module


def get_config() -> dict:
    return load_yaml(join(get_root_path(), 'config.yaml'))


config = get_config()
config['default']['cover'] = join(get_root_path(), config['default']['cover'])



async def create_default_async_context(url=''):
    """
    异步创建默认的浏览器上下文，包括浏览器和页面对象
    :param url:
    :return:
    """
    asp = async_playwright()
    ap = await asp.start()
    browser = await ap.chromium.launch_persistent_context(
        base_url=url,
        channel=config['default']['browser'],
        headless=False,
        user_data_dir=config['data']['user']['dir'],
        no_viewport=True,  # TODO 这里默认全屏模式，需要改成可配置
        args=['--start-maximized'],
        devtools=False
    )
    page = browser.pages[0]
    return browser, page, ap, asp

async def async_post_files(files: list, digests=None, sites=None, tags=None, categories=None, covers=None,
                     topics=None, columns=None) -> Result:
    """
    异步上传文件
    :param files: 文件路径数组
    :param digests: 文件摘要路径数组
    :param sites: 站点名称数组
    :param tags: 标签数组
    :param categories: 分类数组
    :param covers: 封面路径数组
    :param topics: 话题数组
    :param columns: 栏目数组
    :return: Result对象 data为上传的文件链接数组
    """
    if sites is None:
        sites = []
    if digests is None:
        digests = []
    if tags is None:
        tags = []
    if categories is None:
        categories = []
    if covers is None:
        covers = []
    if topics is None:
        topics = []
    if columns is None:
        columns = []
    if sites == []:
        # 如果没有站点，则使用默认站点列表
        sites = config['default']['community'].keys()

    asp = async_playwright()
    ap = await asp.start()
    viewport = config['default']['no_viewport'] if config['default']['no_viewport'] else {'width': config['view']['width'], 'height': config['view']['height']}

    browser = await ap.chromium.launch_persistent_context(
        base_url=config['default']['url'],
        channel=config['default']['browser'],
        headless=config['default']['headless'],
        user_data_dir=config['data']['user']['dir'],
        no_viewport=config['default']['no_viewport'],
        args=['--start-maximized'],
        devtools=bool(config['default']['devtools'])
    )

    tasks = []
    for (index, file) in enumerate(files):
        (title, ext) = get_file_name_ext(file)
        if ext == '.md' or ext == '.markdown' or ext == '.mdown' or ext == '':
            # 如果是markdown文件，则转换为html
            file = convert_md_to_html(file)
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            if covers == [] or index >= len(covers):
                # 没有指定封面使用默认封面
                covers.append(get_abs_path(config['default']['cover']))
            if tags == [] or index >= len(tags):
                # 没有指定标签使用默认标签,这里是列表形式
                tags.append([config['default']['tags']])
            else:
                # 标签字符串转列表
                tags[index] = tags[index].split(',')
            if columns == [] or index >= len(columns):
                # 没有指定栏目使用默认栏目
                columns.append([config['default']['columns']])
            else:
                # 栏目字符串转列表
                columns[index] = columns[index].split(',')
            if categories == [] or index >= len(categories):
                # 没有指定分类使用默认分类
                categories.append(config['default']['category'])
            if topics == [] or index >= len(topics):
                # 没有指定话题使用默认话题
                topics.append(config['default']['topic'])
            if digests == [] or index >= len(digests):
                # 没有指定摘要使用文件内容
                digests.append(content[:config['default']['digest']['length']])
            for site in sites:
                # 遍历站点列表
                if site not in config['default']['community']:
                    continue
                task = async_post_text(browser,ap,asp, file, title, content, digests[index], site, tags[index], categories[index],
                                       covers[index],
                                       topics[index], columns[index])
                tasks.append(task)
    result = await asyncio.gather(*tasks)
    await browser.close()
    await asp.__aexit__()
    return Result(code=1, message='上传成功！！！', data=result)


async def async_post_text(browser: object,ap: object,asp: object, file_path: str, title: str, content: str, digest: str | object = None,
                          site: str = None,
                          tags: list = None,
                          category: str = None, cover: str = None, topic: str = None, columns: list = None) -> (str,str):
    """
    同步上传文本到指定站点
    通过反射技术，根据社区名称反射获取类名，调用接口相应方法上传
    :param page: 页面对象
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
    post_new_url = await site_instance.async_post_new(file_path=file_path, title=title, content=content, digest=digest,
                                                      tags=tags, category=category, cover=cover, topic=topic,
                                                      columns=columns)
    return site_instance.site_name, post_new_url
