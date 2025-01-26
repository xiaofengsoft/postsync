# -*- coding: utf-8 -*-
import queue
import os
from collections import defaultdict
from flask import Flask
from htmldocx import HtmlToDocx
from markdown import Markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from webview import Window
import typing as t
from utils.load import load_yaml
from utils.load import get_root_path
from html2text import html2text

# 全局常量

CONFIG_FILE_PATH = 'config.yaml'
FILE_ENCODING = 'utf-8'
INFINITE_TIMEOUT = 10000000
UNKNOWN_SITE_NAME = '未知社区'
UNKNOWN_SITE_ALIAS = 'unknown'
APP_PORT = 54188
APP_HOST = 'localhost'
APP_HTTP = 'http'
APP_URL = f'{APP_HTTP}://{APP_HOST}:{APP_PORT}'

SITE_ALIAS = (
    "bilibili",
    "juejin",
    "zhihu",
    "wechat",
    "csdn",
    "cnblog"
)
HTML_EXTENSIONS = (
    'html',
    'htm',
    'xhtml',
)
MD_EXTENSIONS = (
    'md',
    'markdown',
    'mdown'
)
DOC_EXTENSIONS = (
    'docx',
)
HTTP_SUCCESS_STATUS_CODES = (
    200, 201, 202, 203, 204,
    205, 206, 207, 208, 226
)

# 配置
config = load_yaml(os.path.join(get_root_path(), CONFIG_FILE_PATH))

# 全局工具类
md_html_parser = Markdown(extensions=[
    CodeHiliteExtension(),  # 代码高亮
    FencedCodeExtension()  # 允许代码块
])

html_docx_parser = HtmlToDocx()

html_md_parser = html2text

# 主窗口
main_window: t.Optional[Window] = None

# Flask应用
server_app: t.Optional[Flask] = None

# 社区实例
site_instances = defaultdict()

# 登录状态确认队列,收到-1表示结束
is_confirmed = queue.Queue()
