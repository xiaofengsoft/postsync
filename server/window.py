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
