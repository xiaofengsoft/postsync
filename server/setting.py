# -*- coding: utf-8 -*-
import json
import yaml
from flask import Blueprint,request
from yaml import Dumper

from common import constant as c
from common.result import Result
from utils.file import get_root_path


setting_api = Blueprint('setting_api', __name__, url_prefix='/api/setting')


@setting_api.route('/read', methods=['GET'])
def read():
    return Result.success(c.config, '读取配置成功')


@setting_api.route('/save', methods=['POST'])
def save():
    data = json.loads(request.get_data().decode('utf-8'))
    with open(get_root_path() + '/config.yaml', 'w', encoding='utf-8') as file:
        yaml.dump(data, file, default_flow_style=False, encoding='utf-8',Dumper=Dumper,sort_keys=False,allow_unicode=True)
    print(data)
    return Result.success(None, '更新配置成功')



