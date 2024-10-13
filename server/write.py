# -*- coding: utf-8 -*-
import json
import os.path
import webview
from flask import Blueprint,request
import shutil
from common import constant as c
from utils.file import get_file_name_without_ext
from common.result import Result
from utils.load import get_path

write_api = Blueprint('write_api', __name__, url_prefix='/api/write')


@write_api.route('image/select')
def upload_image():
    file_types = ('Image files (*.png;*.jpg;*.jpeg;*.gif)',)
    result = c.main_window.create_file_dialog(
        webview.OPEN_DIALOG, allow_multiple=True, file_types=file_types
    )
    if not result:
        return Result.error(message='未选择文件')
    result = list(result)
    for index, file_path in enumerate(result):
        copy_path = get_path(c.config['data']['temp']['path'] + f'/{os.path.basename(file_path)}')
        shutil.copy(file_path, copy_path)
        result[index] = c.APP_URL+'/temp/'+os.path.basename(file_path)
    return Result.success(data=result, message='选择成功')


@write_api.route('load', methods=['POST'])
def load_post():
    data = json.loads(request.get_data().decode('utf-8'))
    file_path = data.get('path')
    if not os.path.exists(file_path):
        return Result.error(message='文件不存在')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace(c.config['data']['temp']['path'],c.APP_URL+'/temp')
    return Result.success(data={'title': get_file_name_without_ext(file_path), 'content': content}, message='加载成功')
