# -*- coding: utf-8 -*-
from flask import Blueprint
from utils.load import get_path
from common.result import Result
from common import constant as c

dashboard_api = Blueprint('dashboard_api', __name__, url_prefix='/api/dashboard')


@dashboard_api.route('/readme', methods=['GET'])
def readme():
    with open(get_path('Readme.md'), 'r', encoding=c.FILE_ENCODING) as f:
        data = f.read()
    return Result.success(message='返回成功', data=data)
