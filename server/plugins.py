# -*- coding: utf-8 -*-
from flask import jsonify, Blueprint, request
from common import constant
from common.result import Result
from utils.load import get_path
from utils.plugins import get_plugins
plugins_api = Blueprint('plugins_api', __name__, url_prefix='/api/plugins')
main_window = constant.main_window


@plugins_api.route('', methods=['GET'])
def get():
    plugins = get_plugins()
    return Result.success(message='获取成功', data=plugins)
