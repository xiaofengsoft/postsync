import os
import random
import time
from functools import wraps
import ctypes
import typing as t
from playwright.async_api import Page


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




