# -*- coding: utf-8 -*-
import webview
from webview.errors import JavascriptException
def test_storage():
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
