# -*- coding: utf-8 -*-
import pytest
import webview


def test_drag_and_drop():
    html = """
    <head>
        <style type="text/css">
            .pywebview-drag-region {
                width: 50px;
                height: 50px;
                margin-top: 50px;
                margin-left: 50px;
                background: orange;
            }
        </style>
    </head>
    <body>
        <div class="pywebview-drag-region">Drag me!</div>
        <div style="width: 50px; height: 50px; -webkit-drag-region: drag;background: blue;"></div>
    </body>
    """
    window = webview.create_window(
        'API example',
        html=html,
        frameless=True,
        easy_drag=False,
    )
    webview.start(debug=True)
