# -*- coding: utf-8 -*-
import os

from flask import send_from_directory
from common import constant as c
from utils.load import get_path

server_app = c.server_app


@server_app.route('/temp/<path:path>')
def temp_file(path):
    """
    托管用户的临时图片文件
    """
    if not os.path.exists(get_path(c.config['data']['temp']['path'])):
        os.makedirs(get_path(c.config['data']['temp']['path']))
    return send_from_directory(get_path(c.config['data']['temp']['path']), path)


@server_app.route('/<path:path>')
def static_file(path):
    """
    托管静态文件
    """
    return send_from_directory(server_app.static_folder, path)


@server_app.route('/')
def index():
    """
    定义首页路由
    """
    return send_from_directory(server_app.static_folder, 'index.html')
