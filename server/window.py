# -*- coding: utf-8 -*-
from flask import jsonify,Blueprint
from common import constant


window_api = Blueprint('window_api', __name__, url_prefix='/api/window')
main_window = constant.main_window


@window_api.route('/minimize', methods=['GET'])
def minimize():
    main_window.minimize()
    return jsonify({'code': 0, 'data': 'Minimize window success!'})


@window_api.route('/close', methods=['GET'])
def close():
    main_window.destroy()
    return jsonify({'code': 0, 'data': 'Close window success!'})


@window_api.route('/maximize', methods=['GET'])
def maximize():
    main_window.maximize()
    return jsonify({'code': 0, 'data': 'Maximize window success!'})


@window_api.route('/restore', methods=['GET'])
def restore():
    main_window.restore()
    return jsonify({'code': 0, 'data': 'Restore window success!'})
