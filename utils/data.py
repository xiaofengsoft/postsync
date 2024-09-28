# -*- coding: utf-8 -*-
import json
import re

from utils.helper import wait_random_time
from utils.load import get_path
import os
from playwright.async_api import Page
import base64
from PIL import Image
import io


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
            img_tag['src'] = os.path.join(os.path.dirname(html_file_path), img_src)
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))


def convert_md_img_path_to_abs_path(md_file_path: str):
    """
    将MD文件中图片的路径转换为绝对路径
    :param md_file_path: MD文件路径
    """
    convert_html_img_path_to_abs_path(md_file_path)
    image_pattern = re.compile(r'!\[.*?\]\((.*?)\)')
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    img_paths = re.findall(image_pattern, md_content)
    for img_path in img_paths:
        if not img_path.startswith('http'):
            if not os.path.isabs(img_path):
                md_content = md_content.replace(img_path, os.path.join(os.path.dirname(md_file_path), img_path))
    with open(md_file_path, 'w', encoding='utf-8') as f:
        f.write(md_content)


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


def convert_base64_to_local_img(base64_content: str, img_path: str, img_format: str = "PNG"):
    """
    将HTML内容中的base64图片转换为本地图片
    :param base64_content: base64字符串
    :param img_path: 本地图片路径
    :param img_format: 图片格式
    """
    # 将base64字符串解码成二进制数据
    image_data = base64.b64decode(base64_content)
    # 使用PIL库将二进制数据转换为图片
    image = Image.open(io.BytesIO(image_data))
    # 保存图片到本地
    image.save(img_path, img_format)


def convert_html_content_images_base64_to_local(html_content: str, img_dir_path: str, img_format: str = "PNG") -> str:
    """
    将HTML内容中的base64图片转换为本地图片
    如果不包含图片则不转化直接返回原内容
    :param html_content: HTML内容
    :param img_dir_path: 本地图片保存路径
    :param img_format: 图片格式
    :return: 转换后的HTML内容
    """
    # 将base64编码的图片转化为本地图片
    base64_strings = re.findall(r'<img.*?src="data:image\/png;base64,(.*?)"', html_content, re.DOTALL)
    if base64_strings:
        for index, base64_string in enumerate(base64_strings):
            img_dir_path = os.path.join(img_dir_path, 'imgs')
            if not os.path.exists(img_dir_path):
                os.makedirs(img_dir_path)
            img_path = img_dir_path + f"{os.path.sep}img{index}.png"
            convert_base64_to_local_img(base64_string, img_path, img_format)
            html_content = html_content.replace(f'src="data:image/png;base64,{base64_string}"', f'src="{img_path}"')
            return html_content


async def insert_html_to_element(page: Page, element_selector: str, html_content: str):
    """
    将HTML内容插入到元素中
    :param page:
    :param element_selector:
    :param html_content:
    :return:
    """
    await page.evaluate("""
    ([element_selector,html_content]) => {
    const element = document.querySelector(element_selector);
    element.innerHTML = html_content;
    }
    """, [element_selector, html_content])


async def insert_html_content_to_frame(page: Page, frame_selector: str, content_selector: str, html_content: str):
    """
    将HTML内容插入到Frame中
    :param page:  Page对象
    :param frame_selector:  Frame选择器
    :param content_selector:  内容选择器
    :param html_content:  HTML内容
    :return:
    """
    await page.evaluate("""
    ([frame_selector,content_selector,html_content]) => {
    const frameElement = document.querySelector(frame_selector);
    frameElement.contentDocument.querySelector(content_selector).innerHTML = html_content;
    }
    """, [frame_selector, content_selector, html_content])


async def scroll_to_element(page: Page, selector: str):
    while True:
        # 检查元素是否在视口中可见
        is_visible = await page.is_visible(selector)
        if is_visible:
            break
        # 如果不可见，执行滚动操作
        await page.evaluate('window.scrollBy(0, window.innerHeight / 2);')
        # 添加一个小的延迟，防止滚动速度过快
        wait_random_time()


async def delete_blank_tags(page: Page, selector: str):
    """
    删除元素中的所有标签
    :param page:
    :param selector:
    :return:
    """
    await page.evaluate("""
        ([selector]) => {
            const tags = document.querySelectorAll(selector);
            tags.forEach(e => {
                if(e.innerHTML.trim() === '' && e.children.length <= 0){
                    e.remove();
                }
            });
        }
        """, [selector])
