# -*- coding: utf-8 -*-
import json
from utils.file import get_path, get_file_dir
import os
from playwright.async_api import Page


def get_storage_data(path: str) -> str:
    """
    获取存储数据
    :param path:
    :return:
    """
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data


def format_json_file(path: str) -> str:
    """
    格式化JSON文件
    在每次写入JSON数据时，都调用此函数格式化JSON文件
    :param path:
    :return: 格式化后的JSON字符串
    """
    path = get_path(path)
    with open(path, 'r+', encoding='utf-8') as file:
        data = json.load(file)
        json_str = json.dumps(data, indent=4, ensure_ascii=False)
        file.seek(0)
        file.write(json_str)
        file.truncate()
        return json_str


def retrieve_storage_data(marks: tuple | str, path: str) -> bool:
    """
    检索存储数据是否存在含有标志
    检索的JSON数据必须格式化
    :param marks:
    :param path:
    :return:
    """
    path = get_path(path)
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
        for mark in marks:
            if mark not in content:
                return False
    return True


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


async def insert_anti_detection_script(page: Page):
    """
    在页面中插入防检测脚本
    :param page:
    """
    await page.evaluate("""() => {
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                }""")
    with open(get_path('data/scripts/stealth.min.js')) as f:
        js = f.read()
    await page.add_init_script(js)