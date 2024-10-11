# -*- coding: utf-8 -*-
from flask import jsonify, Blueprint, request
from common import constant
from common.result import Result
from utils.load import get_path

window_api = Blueprint('window_api', __name__, url_prefix='/api/window')
main_window = constant.main_window


@window_api.route('/minimize', methods=['GET'])
def minimize():
    main_window.minimize()
    return Result.success('Minimize window success!')


@window_api.route('/close', methods=['GET'])
def close():
    main_window.destroy()
    return Result.success('Close window success!')


@window_api.route('/maximize', methods=['GET'])
def maximize():
    main_window.maximize()
    return Result.success('Maximize window success!')


@window_api.route('/restore', methods=['GET'])
def restore():
    main_window.restore()
    return Result.success('Restore window success!')


@window_api.route('/storage/save',methods=['POST'])
def save():
    if request.method == 'POST':
        data = request.get_data().decode('utf-8')
        with open(get_path('data/webview.json'), 'w',encoding=constant.FILE_ENCODING) as f:
            f.write(data)
    return Result.success('保存取数据成功')


@window_api.route('/storage/load',methods=['GET'])
def load():
    with open(get_path('data/webview.json'), 'r',encoding=constant.FILE_ENCODING) as f:
        data = f.read()
    return Result.success(data)