# -*- coding: utf-8 -*-
"""
用来处理浏览器相关的操作
"""
import os
import platform
import typing as t

import yaml
from playwright.async_api import async_playwright, Browser,BrowserContext, PlaywrightContextManager
import nest_asyncio
from yaml import Dumper

import utils.file
from common import constant as c
from utils.file import get_path


def find_browser_executable() -> t.Optional[t.List[tuple[str, str]]]:
    system = platform.system()
    # Chrome 可执行文件可能的位置
    chrome_paths = {
        'Windows': [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ],
        'Darwin': [  # macOS
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        ],
        'Linux': [
            "/usr/bin/google-chrome",
            "/usr/local/bin/google-chrome",
        ]
    }
    # Firefox 可执行文件可能的位置
    firefox_paths = {
        'Windows': [
            r"C:\Program Files\Mozilla Firefox\firefox.exe",
            r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
        ],
        'Darwin': [  # macOS
            "/Applications/Firefox.app/Contents/MacOS/firefox"
        ],
        'Linux': [
            "/usr/bin/firefox",
            "/usr/local/bin/firefox",
        ]
    }
    # Edge 可执行文件可能的位置
    edge_paths = {
        'Windows': [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
        ],
        'Darwin': [  # macOS
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
        ],
        'Linux': [
            "/usr/bin/microsoft-edge",
            "/usr/local/bin/microsoft-edge",
        ]
    }
    # 使用 shutil.which 查找路径

    def find_browser_in_paths(paths):
        for path in paths:
            if os.path.exists(path):
                return path
        return None
    # 查找浏览器
    browser_executable = {
        'Chrome': find_browser_in_paths(chrome_paths.get(system, [])),
        'Firefox': find_browser_in_paths(firefox_paths.get(system, [])),
        'Edge': find_browser_in_paths(edge_paths.get(system, [])),
    }
    # 输出找到的浏览器路径
    ret = []
    for browser, executable in browser_executable.items():
        if executable:
            ret.append((browser, executable))
    return ret if ret else None


async def create_context(headless:bool=False,**kwargs) -> t.Tuple[Browser, BrowserContext,PlaywrightContextManager]:
    """
    创建浏览器上下文
    :param headless:
    :param kwargs:
    :return:
    """
    nest_asyncio.apply()
    asp = async_playwright()
    ap = await asp.start()
    if os.path.exists(c.config['data']['executable']['path']):
        executable = c.config['data']['executable']['path'].lower()
    else:
        executable = find_browser_executable()[0][1]
        # 写入配置文件
        with open(get_path('/config.yaml'), 'w', encoding=c.FILE_ENCODING) as file:
            yaml.dump(
                c.config, file, default_flow_style=False,
                encoding='utf-8', Dumper=Dumper, sort_keys=False,
                allow_unicode=True
            )
    executable = utils.file.get_file_path_without_ext(executable)
    if 'chrome' in executable or 'chromium' in executable or 'edge' in executable:
        browser = await ap.chromium.launch(
            channel='msedge' if 'edge' in executable else 'chrome',
            headless=headless,
            args=['--start-maximized --disable-blink-features=AutomationControlled'],
            devtools=bool(c.config['default']['devtools']),
            timeout=int(c.config['default']['timeout']),
            **kwargs
        )
    elif 'firefox' in executable:
        browser = await ap.firefox.launch(
            headless=headless,
            args=['--start-maximized --disable-blink-features=AutomationControlled'],
            devtools=bool(c.config['default']['devtools']),
            timeout=int(c.config['default']['timeout']),
            **kwargs
        )
    viewport = c.config['default']['no_viewport'] if c.config['default']['no_viewport'] else {
        'width': c.config['view']['width'], 'height': c.config['view']['height']}
    utils.file.make_file_or_dir(c.config['data']['storage']['path'], is_dir=False, func=lambda x: x.write('{ }'))
    context = await browser.new_context(
        storage_state=get_path(c.config['data']['storage']['path']),
        no_viewport=viewport,
        user_agent=c.config['default']['user_agent'],
    )
    return browser, context, asp
