import os
import time
from functools import wraps
import ctypes




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
