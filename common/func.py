import os
import random
import time
from functools import wraps
import ctypes
import typing as t


def get_abs_path(path: str) -> str:
    """
    获取一个文件的绝对路径
    """
    return os.path.join(get_root_path(), path)


def get_root_path() -> str:
    """
    获取项目根目录路径
    """
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_yaml(path: str) -> dict:
    """
    加载YAML文件
    """
    import yaml
    with open(path, 'r', encoding='utf-8') as f:
        yaml_data = yaml.load(stream=f, Loader=yaml.FullLoader)
        return yaml_data


def get_file_name_without_ext(path: str) -> str:
    """
    获取文件名（不含扩展名）
    """
    return os.path.splitext(os.path.basename(path))[0]


def get_file_ext(path: str) -> str:
    """
    获取文件扩展名
    """
    return os.path.splitext(path)[1]


def get_file_name_ext(path: str) -> (str, str):
    """
    获取文件名和扩展名
    """
    return os.path.splitext(os.path.basename(path))


def get_file_dir(path: str) -> str:
    """
    获取文件所在目录
    """
    return os.path.dirname(path)


def calculate_time(func):
    """
    计算函数执行时间的装饰器
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # 记录函数开始执行的时间
        result = func(*args, **kwargs)  # 执行函数
        end_time = time.time()  # 记录函数执行结束的时间
        execution_time = end_time - start_time  # 计算执行时间
        print(f"Function {func.__name__} took {execution_time} seconds to execute")
        return result

    return wrapper


def get_real_resolution():
    """
    获取屏幕真实分辨率
    :return: 屏幕真实分辨率的宽和高
    """
    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32
    dc = user32.GetDC(None)

    width = gdi32.GetDeviceCaps(dc, 118)  # 原始分辨率的宽度
    height = gdi32.GetDeviceCaps(dc, 117)  # 原始分辨率的高度
    return width, height


def get_scale_resolution():
    """
    获取屏幕缩放分辨率
    :return: 屏幕缩放分辨率的宽和高
    """
    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32
    dc = user32.GetDC(None)
    widthScale = gdi32.GetDeviceCaps(dc, 8)  # 分辨率缩放后的宽度
    heightScale = gdi32.GetDeviceCaps(dc, 10)  # 分辨率缩放后的高度
    return widthScale, heightScale


def convert_md_to_html(md_file_path: str, html_file_path: str = None, file_path_without_ext: str = None) -> str:
    """
    将Markdown文件转换为HTML
    :param md_file_path: Markdown文件路径
    :param html_file_path: HTML文件路径，默认为Markdown文件路径
    :return: HTML文件路径
    """
    from markdown import Markdown
    md = Markdown()
    if not html_file_path:
        html_file_path = md_file_path.replace('.md', '.html')
    md.convertFile(md_file_path, html_file_path, "utf-8")
    return html_file_path


def convert_html_to_docx(html_file_path: str, docx_file_path: str = None) -> str:
    """
    将HTML文件转换为DOCX
    :param html_file_path: HTML文件路径
    :param docx_file_path: DOCX文件路径，默认为HTML文件路径
    :return: DOCX文件路径
    """
    from docx import Document
    from htmldocx import HtmlToDocx
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    if not docx_file_path:
        docx_file_path = html_file_path.replace('.html', '.docx')
    # 转换图片路径为绝对路径
    convert_html_img_path_to_abs_path(html_file_path)
    document = Document()
    new_parser = HtmlToDocx()
    new_parser.add_html_to_document(html_content, document)
    document.save(docx_file_path)
    return docx_file_path


def convert_html_content_to_md(html_content: str) -> str:
    """
    将HTML内容转换为Markdown
    :param html_content:
    :return:
    """
    from tomd import Tomd
    markdown_content = Tomd(html_content).markdown
    return markdown_content


def convert_html_img_path_to_abs_path(html_file_path: str):
    """
    将HTML文件中图片的路径转换为绝对路径
    :param html_file_path: HTML文件路径
    """
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    img_tags = soup.find_all('img')
    for img_tag in img_tags:
        img_src = img_tag.get('src')
        if not img_src.startswith('http'):
            img_tag['src'] = os.path.join(get_file_dir(html_file_path), img_src)
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))


def analyse_var(var: t.Any, retract: t.Optional[int] = 0):
    """
    解析变量
    :param var:
    :param retract:
    :return:
    """
    print(f"{' ' * retract}type: {type(var)}")
    print(f"{' ' * retract}var: {var}")
    if isinstance(var, (int, float, str, bool)):
        print(f"{' ' * retract}length: {len(str(var))}")
    elif isinstance(var, (list, tuple)):
        for i, item in enumerate(var):
            print(f"{' ' * retract}[{i}]")
            analyse_var(item, retract + 2)
    elif isinstance(var, dict):
        for key, value in var.items():
            print(f"{' ' * retract}{key}:")
            analyse_var(value, retract + 2)


async def scroll_to_element(page, selector):
    while True:
        # 检查元素是否在视口中可见
        is_visible = await page.is_visible(selector)
        if is_visible:
            break

        # 如果不可见，执行滚动操作
        await page.evaluate('window.scrollBy(0, window.innerHeight / 2);')

        # 添加一个小的延迟，防止滚动速度过快
        time.sleep(0.1)


def wait_random_time(begin_time: float = 0.2, end_time: float = 0.5):
    """
    等待随机时间
    :param begin_time: 开始时间
    :param end_time: 结束时间
    """
    wait_time = random.uniform(begin_time, end_time)
    time.sleep(wait_time)


async def insert_html_to_website(page, tag_id: str, html_content: str):
    await page.evaluate("""
    ([tag_id,html_content]) => 
    {
        console.log(tag_id,html_content);
        document.querySelector(tag_id).innerHTML = html_content;    
    }
    
    """,
                        [tag_id, html_content])
