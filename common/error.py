# -*- coding: utf-8 -*-
from playwright.async_api import Error as BrowserError
from playwright.async_api import TimeoutError as BrowserTimeoutError
import traceback


class FileNotReferencedError(Exception):
    """
    Exception raised when a file is not referenced
    """

    def add_note(self, __note):
        super().add_note(__note)
        super().add_note("没有指定文件")


class FileNotSupportedError(Exception):
    """
    Exception raised when a file is not supported
    """

    def add_note(self, __note):
        super().add_note(__note)
        super().add_note("不支持的文件类型")


class CommunityNotExistError(Exception):
    """
    Exception raised when a community does not exist
    """
    pass


class ConfigurationLackError(Exception):
    """
    Exception raised when configuration lacks
    """
    pass


class ConfigNotConfiguredError(Exception):
    """
    Exception raised when config is not configured
    """
    pass


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
        super().__init__(f"Multiple exceptions occurred: {len(exceptions)}")

    def __str__(self):
        return '\n'.join([f"\nException {i + 1}:\n{format_exception(e)}" for i, e in enumerate(self.exceptions)])
