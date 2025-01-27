# -*- coding: utf-8 -*-
from common import constant as c
from playwright.async_api import Page
import yaml
from utils.load import get_root_path
import os


def storage_config():
    with open(get_root_path() + '/config.yaml', 'w', encoding='utf-8') as file:
        yaml.dump(c.config, file, default_flow_style=False, encoding='utf-8',
                  Dumper=yaml.SafeDumper, sort_keys=False, allow_unicode=True)


async def get_page_local_storage(page: Page) -> dict:
    local_storage = await page.evaluate("""
            () => {
                const items = {};
                for (let i = 0; i < localStorage.length; i++) {
                    const key = localStorage.key(i);
                    items[key] = localStorage.getItem(key);
                }
                return items;
            }
    """)
    return local_storage


def setup_wizard():
    """
    安装向导
    """
    import tkinter as tk
    from tkinter import messagebox, filedialog
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    messagebox.showinfo("PostSync 安装向导", "欢迎使用PostSync！请选择数据存储目录。")
    storage_path = filedialog.askdirectory(title="选择数据存储目录")
    if not storage_path:
        messagebox.showerror("错误", "必须选择存储目录！")
        return False
    try:
        # 创建必要的目录结构
        os.makedirs(storage_path, exist_ok=True)
        # 更新配置
        c.config['app']['installed'] = True
        c.config['data']['path'] = storage_path
        c.config['data']['posts']['path'] = os.path.join(storage_path, 'posts')
        c.config['data']['storage']['path'] = os.path.join(
            storage_path, 'storage.json')
        c.config['data']['webview']['path'] = os.path.join(
            storage_path, 'webview')
        c.config['data']['temp']['path'] = os.path.join(
            storage_path, 'temp')
        c.config['data']['log']['path'] = os.path.join(
            storage_path, 'log')
        # 如果已经存在目录则不创建
        if not os.path.exists(c.config['data']['path']):
            # 创建目录
            os.makedirs(c.config['data']['posts']['path'], exist_ok=True)
            os.makedirs(c.config['data']['webview']['path'], exist_ok=True)
            os.makedirs(c.config['data']['temp']['path'], exist_ok=True)
            os.makedirs(c.config['data']['log']['path'], exist_ok=True)
            # 创建空的storage.json
            with open(c.config['data']['storage']['path'], 'w', encoding='utf-8') as file:
                file.write("{}")
        if c.config['data']['executable']['path'] is not None and not os.path.exists(c.config['data']['executable']['path']):
            # 选择浏览器
            messagebox.showinfo("选择浏览器", "请选择您的浏览器程序")
            browser_path = filedialog.askopenfilename(
                title="选择浏览器程序", filetypes=[("浏览器程序", "*.exe")])
            if not browser_path:
                messagebox.showerror("错误", "必须选择浏览器程序！")
            c.config['data']['executable']['path'] = browser_path
        # 保存配置
        storage_config()
        messagebox.showinfo("安装完成", f"PostSync数据目录将会安装到：\n{storage_path}")
        return True
    except Exception as e:
        messagebox.showerror("安装失败", f"发生错误：{str(e)}")
        return False
