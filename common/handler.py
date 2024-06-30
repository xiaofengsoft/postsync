# -*- coding: utf-8 -*-
from common.error import *


def handle_global_exception(exc_type, exc_value, exc_traceback):
    """
    Global exception handler
    To be used with try-except block
    TODO: 捕获所有异常
    """
    print("全局异常信息：")
    print("异常类型：", exc_type)
    print("异常值：", exc_value)
    print("异常追踪：", exc_traceback)
    if exc_type is FileNotReferencedError:
        print("没有指定文件")
    if exc_type is FileNotFoundError:
        print("文件不存在")


