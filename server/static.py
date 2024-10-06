# -*- coding: utf-8 -*-
from flask import send_from_directory
from common import constant

server_app = constant.server_app


@server_app.route('/<path:path>')
def static_file(path):
    return send_from_directory(server_app.static_folder, path)


@server_app.route('/')
def index():
    return send_from_directory(server_app.static_folder, 'index.html')
