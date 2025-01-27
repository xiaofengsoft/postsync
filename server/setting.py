# -*- coding: utf-8 -*-
import json
import os

import yaml
from flask import Blueprint, request
from yaml.dumper import SafeDumper
from common import constant as c
from common.result import Result
from utils.file import get_root_path, load_yaml

setting_api = Blueprint('setting_api', __name__, url_prefix='/api/setting')


@setting_api.route('/read', methods=['GET'])
def read():
    return Result.success(c.config, '读取配置成功')


@setting_api.route('/save', methods=['POST'])
def save():
    # 转化相对的字符串为布尔值，否则后续读取会逻辑错误
    data = json.loads(request.get_data().decode('utf-8'))
    data['app']['debug'] = str(
        data['app']['debug']).strip("'").lower() == 'true'
    data['app']['installed'] = str(
        data['app']['installed']).strip("'").lower() == 'true'
    data['default']['headless'] = str(
        data['default']['headless']).strip("'").lower() == 'true'
    data['default']['devtools'] = str(
        data['default']['devtools']).strip("'").lower() == 'true'
    data['default']['no_viewport'] = str(
        data['default']['no_viewport']).strip("'").lower() == 'true'
    with open(get_root_path() + '/config.yaml', 'w', encoding='utf-8') as file:
        yaml.dump(data, file, default_flow_style=False, encoding='utf-8',
                  Dumper=SafeDumper, sort_keys=False, allow_unicode=True)
    c.config = load_yaml(os.path.join(get_root_path(), c.CONFIG_FILE_PATH))
    return Result.success(None, '更新配置成功')
