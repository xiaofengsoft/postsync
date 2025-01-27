# -*- coding: utf-8 -*-
import os
from flask import jsonify, Blueprint, request
import webview
from werkzeug.utils import secure_filename
from common import constant
from common.result import Result
from utils.load import get_path
from utils.plugins import get_plugins, plugin_install, plugin_uninstall
plugins_api = Blueprint('plugins_api', __name__, url_prefix='/api/plugins')
main_window = constant.main_window


@plugins_api.route('', methods=['GET'])
def get():
    plugins = get_plugins()
    return Result.success(message='获取成功', data=plugins)


@plugins_api.route('/uninstall', methods=['POST'])
def uninstall():
    name = request.get_json().get('name')
    plugin_uninstall(name)
    return Result.success(message='卸载成功')


@plugins_api.route('/install', methods=['GET'])
def install():
    file_types = ('Py file (*.py)',)
    result = main_window.create_file_dialog(
        webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types
    )
    if not result:
        return Result.error(message='未选择文件')
    file_path = result[0]
    ret = plugin_install(file_path)
    return Result.success(data=result, message='安装成功') if ret else Result.error(message='安装失败')
