# -*- coding: utf-8 -*-
import json
import os.path

import nest_asyncio
from flask import Blueprint, request
import webview

from common.apis import PostArguments
from common.constant import config
from common.core import ProcessCore
from common.handler import handle_global_exception
from common.result import Result
from common import constant as c
from utils.file import get_path

post_api = Blueprint('post_api', __name__, url_prefix='/api/post')
main_window = c.main_window


@post_api.route('/choose')
def chooses_post():
    file_types = ('Document files (*.md;*.html;*.docx)',)
    result = main_window.create_file_dialog(
        webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types
    )
    return Result.success(data=result, message='选择成功')


@post_api.route('/choose/cover')
def chooses_cover():
    file_types = ('Image files (*.png;*.jpg;*.jpeg;*.gif)',)
    result = main_window.create_file_dialog(
        webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types
    )
    return Result.success(data=result, message='选择成功')


@post_api.route('/save/file', methods=['POST'])
def save_file():
    data = json.loads(request.get_data().decode('utf-8'))
    if not data.get('content') or not data.get('title'):
        return Result.error(message='标题或者内容不能为空')
    file_path = os.path.join(get_path(config['data']['posts']['path']), data['title']+'.'+data['type'])
    # 创建文件夹
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(data['content'])
    return Result.success(message='保存成功',data={'path':file_path})


@post_api.route('/upload', methods=['POST'])
def upload_post():
    data = json.loads(request.get_data().decode('utf-8'))
    data: PostArguments
    # 允许嵌套协程
    try:
        nest_asyncio.apply()
        # 初始化
        process_core = ProcessCore(
            is_pass_args_by_cmd=False,
            args=data
        )
        # 处理数据
        return Result.success(
            [one_res for one_res in process_core.results.data],
            process_core.results.message
        )
    except BaseException as e:
        if 'True' == str(config['app']['debug']):
            raise e
        else:
            ret = handle_global_exception(e)
            return Result.build(ret['code'], ret['data'], ret['message'])
