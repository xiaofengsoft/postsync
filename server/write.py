# -*- coding: utf-8 -*-
import webview
from flask import Blueprint

from common.constant import main_window
from common.result import Result

write_api = Blueprint('write_api', __name__, url_prefix='/api/write')


@write_api.route('image/select')
def upload_image():
    file_types = ('Image files (*.png;*.jpg;*.jpeg;*.gif)',)
    result = main_window.create_file_dialog(
        webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types
    )
    return Result.success(data=result, message='选择成功')

