# -*- coding: utf-8 -*-
import asyncio
import json
import os
from flask import Blueprint, request
from utils.browser import get_community_instance, create_context

from utils.file import get_file_name_without_ext
from common.constant import config
from common.error import BrowserExceptionGroup
from common.result import Result

dashboard_api = Blueprint('dashboard_api', __name__,
                          url_prefix='/api/dashboard')


@dashboard_api.route('/login/check', methods=['GET'])
async def check_login():
    browser, context, asp = await create_context(headless=True)
    tasks = []
    if os.path.exists(config['data']['states']['path']):
        with open(config['data']['states']['path'], 'r') as f:
            states = json.load(f)
        return Result.success(data=states)

    async def one_check_task(one_site):
        site_instance = get_community_instance(
            one_site, browser, context)
        try:
            ret = await site_instance.check_login_state()
        except Exception:
            ret = False
        return {
            'name': site_instance.site_name,
            'alias': one_site,
            'status': ret
        }

    for site in config['default']['community'].keys():
        task = one_check_task(site)
        tasks.append(task)
    results = await asyncio.gather(*tasks, return_exceptions=False)
    with open(config['data']['states']['path'], 'w') as f:
        json.dump(results, f)
    await context.close()
    await asp.__aexit__()
    return Result.success(message='登录状态检查成功', data=results)


@dashboard_api.route('/login/once', methods=['POST'])
async def login_once():
    browser, context, asp = await create_context(headless=False)
    site = json.loads(request.get_data().decode('utf-8'))['name']
    site_instance = get_community_instance(
        site, browser, context)
    try:
        ret = await site_instance.login()
    except BrowserExceptionGroup as e:
        await asp.__aexit__()
        return Result.error(message=str(e))
    await asp.__aexit__()
    return Result.success(message='登录成功', data=ret)


@dashboard_api.route('/post/list', methods=['GET'])
async def post_list():
    file_paths = []
    for root, dirs, files_in_dir in os.walk(config['data']['posts']['path']):
        for file in files_in_dir:
            if not file.endswith('.md'):
                continue
            file_paths.append(os.path.join(root, file))
    files = [get_file_name_without_ext(str(file_path))
             for file_path in file_paths]
    data = [{'name': name, 'path': path}
            for name, path in zip(files, file_paths)]
    return Result.success(data=data)


@dashboard_api.route('/post/delete', methods=['POST'])
async def post_delete():
    file_path = json.loads(request.get_data().decode('utf-8'))['path']
    os.remove(file_path)
    return Result.success(message='删除成功')
