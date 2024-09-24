# -*- coding: utf-8 -*-
import os
import typing as t
from docx import Document
from htmldocx import HtmlToDocx
from common.constant import *
from pydocx import PyDocX


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
    with open(path, 'r', encoding='utf-8') as f:
        yaml_data = yaml.load(stream=f, Loader=yaml.FullLoader)
        return yaml_data


def convert_md_to_html(md_file_path: str, html_file_path: str = None) -> str:
    """
    将Markdown文件转换为HTML
    :param md_file_path: Markdown文件路径
    :param html_file_path: HTML文件路径，默认为Markdown文件路径
    :return: HTML文件路径
    """
    if html_file_path is None:
        dst_file_path = check_file_same_name_exists(md_file_path, HTML_EXTENSIONS)
        if dst_file_path:
            return dst_file_path
        else:
            dst_file_path = get_path(get_file_path_without_ext(md_file_path)+".html")
    else:
        dst_file_path = html_file_path
    from markdown import Markdown
    md = Markdown()
    md.convertFile(md_file_path, dst_file_path, "utf-8")
    return dst_file_path


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
            dst_file_path = get_file_path_without_ext(html_file_path)+".docx"
    else:
        dst_file_path = docx_file_path
    from utils.data import convert_html_img_path_to_abs_path
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    # 转换图片路径为绝对路径
    convert_html_img_path_to_abs_path(html_file_path)
    document = Document()
    new_parser = HtmlToDocx()
    new_parser.add_html_to_document(html_content, document)
    document.save(dst_file_path)
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
            dst_file_path = get_path(get_file_path_without_ext(md_file_path)+".docx")
    else:
        dst_file_path = docx_file_path
    html_file_path = check_file_same_name_exists(md_file_path, HTML_EXTENSIONS)
    if not html_file_path:
        html_file_path = convert_md_to_html(md_file_path, docx_file_path)
    convert_html_to_docx(html_file_path, docx_file_path)
    return dst_file_path


def convert_docx_to_html(md_file_path: str, docx_file_path: str = None) -> str:
    """
    将DOCX文件转换为HTML
    :param md_file_path:
    :param docx_file_path:
    :return: HTML内容
    """
    if docx_file_path is None:
        dst_file_path = check_file_same_name_exists(md_file_path, DOC_EXTENSIONS)
        if dst_file_path:
            return dst_file_path
        else:
            dst_file_path = get_path(get_file_path_without_ext(md_file_path)+".html")
    else:
        dst_file_path = docx_file_path
    html_content = PyDocX.to_html(get_path(md_file_path))
    with open(dst_file_path, 'w', encoding="utf-8") as f:
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
            dst_file_path = get_file_path_without_ext(html_file_path)+".md"
    else:
        dst_file_path = md_file_path
    from html2text import html2text
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    md_content = html2text(html_content)
    with open(dst_file_path, 'w', encoding="utf-8") as f:
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
            dst_file_path = get_file_path_without_ext(docx_file_path)+".md"
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
