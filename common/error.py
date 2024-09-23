# -*- coding: utf-8 -*-
from playwright.async_api import Error as BrowserError
from playwright.async_api import TimeoutError as BrowserTimeoutError
import traceback


class FileNotReferencedError(Exception):
    """
    Exception raised when a file is not referenced
    """

    def __str__(self):
        return "请指定文件"


class FileNotSupportedError(Exception):
    """
    Exception raised when a file is not supported
    """
    def __init__(self, file_type: str):
        self.file_type = file_type

    def __str__(self):
        return f"不支持的文件类型: {self.file_type}"


class CommunityNotExistError(Exception):
    """
    Exception raised when a community does not exist
    """
    def __str__(self):
        return "社区不存在"


class ConfigurationLackError(Exception):
    """
    Exception raised when configuration lacks
    """
    def __str__(self):
        return "配置文件缺失"


class ConfigNotConfiguredError(Exception):
    """
    Exception raised when config is not configured
    """
    def __str__(self):
        return "未配置相关配置文件"


def format_exception(exception):
    """
    Format exception traceback
    :param exception:
    :return:
    """
    tb = traceback.format_exception(type(exception), exception, exception.__traceback__)
    return ''.join(tb)


class BrowserExceptionGroup(Exception):
    def __init__(self, exceptions):
        self.exceptions = exceptions
        super().__init__(f"发生{len(exceptions)}个错误:")

    def __str__(self):
        return '\n'.join([f"\nException {i + 1}:\n{format_exception(e)}" for i, e in enumerate(self.exceptions)])
