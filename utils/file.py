# -*- coding: utf-8 -*-
import os


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
    获取文件名和扩展名
    """
    return os.path.splitext(os.path.basename(path))


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
    from utils.data import convert_html_img_path_to_abs_path
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

