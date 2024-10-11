# -*- coding: utf-8 -*-
from utils.data import convert_html_content_images_base64_to_local
import typing as t
from pydocx import PyDocX
from common.constant import *
import os
from utils.data import convert_md_img_path_to_abs_path,convert_html_img_path_to_abs_path


def get_path(path: str) -> str:
    """
    给出可用路径
    如果参数是项目相对路径，则返回项目根目录路径加上参数路径
    如果参数是绝对路径，则直接返回参数路径
    :param path: 路径
    :return: 可用路径
    """
    if os.path.isabs(path):
        return os.path.normpath(path)
    else:
        return os.path.normpath(os.path.join(get_root_path(), path))


def replace_file_ext(path: str, new_ext: str) -> str:
    """
    替换文件扩展名
    """
    if path.endswith('.' + new_ext):
        return path
    return os.path.splitext(path)[0] + '.' + new_ext


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
    获取文件名和扩展名(去除.号)
    """
    name_ext = os.path.splitext(os.path.basename(get_path(path)))
    return name_ext[0], name_ext[1][1:]


def get_file_dir(path: str) -> str:
    """
    获取文件所在目录
    """
    return os.path.dirname(path)


def load_yaml(path: str) -> dict:
    """
    加载YAML文件
    """
    import yaml
    with open(path, 'r', encoding=FILE_ENCODING) as f:
        yaml_data = yaml.load(stream=f, Loader=yaml.FullLoader)
        return yaml_data


def make_file_or_dir(path: str, is_dir: bool = False, func: t.Callable[[t.IO], None] = None) -> bool:
    """
    创建文件或目录，如果不存在则创建，如果存在则不做任何操作
    :param path: 文件或目录路径
    :param is_dir: 是否为目录
    :param func: 创建文件后需要执行的函数
    :return: 是否已经存在
    """
    if is_dir:
        if os.path.exists(path):
            return True
        else:
            os.makedirs(path)
    else:
        if os.path.exists(path):
            return True
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding=FILE_ENCODING) as f:
                f.write('')
                if func:
                    func(f)
    return False


def convert_md_to_html(md_file_path: str, html_file_path: str = None,is_written:bool=True) -> str:
    """
    将Markdown文件转换为HTML
    :param md_file_path: Markdown文件路径
    :param html_file_path: HTML文件路径，默认为Markdown文件路径
    :param is_written: 是否写入文件
    :return: HTML文件路径或者HTML内容
    """
    if html_file_path is None:
        dst_file_path = check_file_same_name_exists(md_file_path, HTML_EXTENSIONS)
        if dst_file_path:
            return dst_file_path
        else:
            dst_file_path = get_path(replace_file_ext(md_file_path, 'html'))
    else:
        dst_file_path = html_file_path
    if is_written:
        md_html_parser.convertFile(md_file_path, dst_file_path, FILE_ENCODING)
        return dst_file_path
    else:
        with open(md_file_path, 'r', encoding=FILE_ENCODING) as f:
            md_content = f.read()
        html_content = md_html_parser.convert(md_content)
        return html_content


def convert_md_content_to_html(md_content: str) -> str:
    """
    将Markdown内容转换为HTML
    :param md_content: Markdown内容
    :return: HTML内容
    """
    return md_html_parser.convert(md_content)


def convert_html_to_docx(html_file_path: str, docx_file_path: t.Optional[str] = None) -> str:
    """
    将HTML文件转换为DOCX
    :param html_file_path: HTML文件路径
    :param docx_file_path: DOCX文件路径，默认为HTML文件路径
    :return: DOCX文件路径
    """
    if docx_file_path is None:
        dst_file_path = check_file_same_name_exists(html_file_path, DOC_EXTENSIONS)
        if dst_file_path:
            return dst_file_path
        else:
            dst_file_path = replace_file_ext(html_file_path, 'docx')
    else:
        dst_file_path = docx_file_path
    # 转换图片路径为绝对路径
    convert_html_img_path_to_abs_path(html_file_path)
    html_docx_parser.parse_html_file(html_file_path, get_file_path_without_ext(dst_file_path))
    return dst_file_path


def convert_md_to_docx(md_file_path: str, docx_file_path: str = None) -> str:
    """
    将Markdown文件转换为DOCX
    :param md_file_path: Markdown文件路径
    :param docx_file_path: DOCX文件路径，默认为Markdown文件路径
    :return: DOCX文件内容
    """
    if docx_file_path is None:
        dst_file_path = check_file_same_name_exists(md_file_path, DOC_EXTENSIONS)
        if dst_file_path:
            return dst_file_path
        else:
            dst_file_path = get_path(replace_file_ext(md_file_path, 'docx'))
    else:
        dst_file_path = docx_file_path
    html_file_path = check_file_same_name_exists(md_file_path, HTML_EXTENSIONS)
    if not html_file_path:
        html_file_path = convert_md_to_html(md_file_path, docx_file_path)
    convert_md_img_path_to_abs_path(html_file_path)
    convert_md_to_html(md_file_path, html_file_path)
    convert_html_to_docx(html_file_path, docx_file_path)
    return dst_file_path


def convert_docx_to_html(docx_file_path: str, html_file_path: str = None) -> str:
    """
    将DOCX文件转换为HTML
    DOCX文件转换为HTML后，文档中附带的图片将自动转换为本地图片
    :param docx_file_path: DOCX文件路径
    :param html_file_path: HTML文件路径，默认为DOCX文件路径
    :return: HTML文件路径
    """
    if html_file_path is None:
        dst_file_path = check_file_same_name_exists(docx_file_path, HTML_EXTENSIONS)
        if dst_file_path:
            return dst_file_path
        else:
            dst_file_path = get_path(replace_file_ext(docx_file_path, 'html'))
    else:
        dst_file_path = html_file_path

    html_content = PyDocX.to_html(get_path(docx_file_path))

    with open(dst_file_path, 'w', encoding=FILE_ENCODING) as f:
        convert_html_content_images_base64_to_local(html_content, os.path.dirname(dst_file_path))
        f.write(html_content)
    return dst_file_path


def convert_html_to_md(html_file_path: str, md_file_path: str = None) -> str:
    """
    将HTML文件转换为Markdown
    :param html_file_path: HTML文件路径
    :param md_file_path: Markdown文件路径，默认为HTML文件路径
    :return: Markdown内容
    """
    if md_file_path is None:
        dst_file_path = check_file_same_name_exists(html_file_path, MD_EXTENSIONS)
        if dst_file_path:
            return dst_file_path
        else:
            dst_file_path = replace_file_ext(html_file_path, 'md')
    else:
        dst_file_path = md_file_path
    with open(html_file_path, 'r', encoding=FILE_ENCODING) as f:
        html_content = f.read()
    md_content = html_md_parser(html_content)
    with open(dst_file_path, 'w', encoding=FILE_ENCODING) as f:
        f.write(md_content)
    return dst_file_path


def convert_docx_to_md(docx_file_path: str, md_file_path: str = None) -> str:
    """
    将DOCX文件转换为Markdown
    :param docx_file_path: DOCX文件路径
    :param md_file_path: Markdown文件路径，默认为DOCX文件路径
    :return: Markdown文件路径
    """
    if md_file_path is None:
        dst_file_path = check_file_same_name_exists(docx_file_path, MD_EXTENSIONS)
        if dst_file_path:
            return dst_file_path
        else:
            dst_file_path = replace_file_ext(docx_file_path, 'md')
    else:
        dst_file_path = md_file_path
    html_file_path = check_file_same_name_exists(docx_file_path, HTML_EXTENSIONS)
    if not html_file_path:
        html_file_path = convert_docx_to_html(docx_file_path, md_file_path)
    convert_html_to_md(html_file_path, md_file_path)
    return dst_file_path


def get_file_path_without_ext(path: str):
    """
    获取文件路径（不含扩展名）
    :param path: 文件路径
    :return:
    """
    return os.path.splitext(str(path))[0]


def check_file_same_name_exists(path: str, exts: t.Union[str, t.List[str]]) -> t.Union[str, bool]:
    """
    检查文件是否存在,如果相关扩展名有一个存在则返回该文件路径，否则返回False
    :param exts:  文件扩展名
    :param path: 文件路径
    :return:
    """
    if isinstance(exts, str):
        exts = [exts]
    for ext in exts:
        real_path_with_ext = get_path(".".join([get_file_path_without_ext(path), ext]))
        if os.path.exists(real_path_with_ext):
            return real_path_with_ext
    return False
