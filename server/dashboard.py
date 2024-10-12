# -*- coding: utf-8 -*-
import asyncio
import json
import os
from importlib import import_module
from flask import Blueprint, request
import utils.browser
from utils.file import get_file_name_without_ext
from common.constant import config
from common.error import BrowserExceptionGroup
from utils.data import convert_html_content_img_path_to_abs_path
from utils.file import convert_md_to_html, make_file_or_dir
from utils.load import get_path
from common.result import Result

dashboard_api = Blueprint('dashboard_api', __name__, url_prefix='/api/dashboard')


@dashboard_api.route('/login/check', methods=['GET'])
async def check_login():
    browser, context,asp = await utils.browser.create_context(headless=False)
    tasks = []

    async def one_check_task(one_site):
        site_cls = import_module('entity.' + one_site.strip())
        site_instance = getattr(site_cls, one_site.strip().capitalize())
        site_instance = site_instance(
            browser=browser,
            context=context,
            post=None,
            is_started=False
        )

        try:
            ret = await site_instance.check_login_state()
        except Exception:
            ret = True
        return {
            'name': site_instance.site_name,
            'alias': one_site,
            'status': ret
        }

    for site in config['default']['community'].keys():
        task = one_check_task(site)
        tasks.append(task)
    results = await asyncio.gather(*tasks, return_exceptions=False)
    await context.close()
    await asp.__aexit__()
    return Result.success(message='登录状态检查成功', data=results)


@dashboard_api.route('/login/once', methods=['POST'])
async def login_once():
    browser,context,asp = await utils.browser.create_context(headless=False)
    site = json.loads(request.get_data().decode('utf-8'))['name']
    site_cls = import_module('entity.' + site.strip())
    site_instance = getattr(site_cls, site.strip().capitalize())
    site_instance = site_instance(
        browser=browser,
        context=context,
        post=None,
        is_started=False
    )
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
            if not file.endswith('.md') and not file.endswith('.html') and not file.endswith('.docx'):
                continue
            file_paths.append(os.path.join(root, file))
    files = [get_file_name_without_ext(str(file_path)) for file_path in file_paths]
    data = [{'name': name, 'path': path} for name, path in zip(files, file_paths)]
    return Result.success(data=data)


@dashboard_api.route('/post/delete', methods=['POST'])
async def post_delete():
    file_path = json.loads(request.get_data().decode('utf-8'))['path']
    os.remove(file_path)
    return Result.success(message='删除成功')
