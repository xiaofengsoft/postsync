# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify
import webview

from common import constant as c

post_api = Blueprint('post_api', __name__, url_prefix='/api/post')
main_window = c.main_window


@post_api.route('/choose')
def chooses_post():
    file_types = ('All files (*.*)',)
    result = main_window.create_file_dialog(
        webview.OPEN_DIALOG, allow_multiple=True, file_types=file_types
    )
    # TODO 可以使用Result类，重写str方法，返回json格式数据
    return jsonify({"code": 0, "data": result})
