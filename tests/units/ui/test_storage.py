# -*- coding: utf-8 -*-
import webview
from webview.errors import JavascriptException

from utils.load import get_path


def test_storage_js():
    def evaluate_js(window):
        result = window.evaluate_js(
            r"""
            localStorage.setItem('test', 'test')
            localStorage.getItem('test')
            """
        )
        print(result)
    window = webview.create_window(
        'Run custom JavaScript',

        url='https://kimi.moonshot.cn/')
    webview.start(evaluate_js, window,gui="edgechromium")


def test_storage_dir():
    window = webview.create_window(
        'Storage Directory',
        url='https://kimi.moonshot.cn/'
    ),

    webview.start(debug=True,private_mode=False,gui="edgechromium",storage_path=get_path('data/webview'))
