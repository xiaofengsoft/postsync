# -*- coding: utf-8 -*-
from playwright.async_api import Error as BrowserError
from playwright.async_api import TimeoutError as BrowserTimeoutError


class FileNotReferencedError(Exception):
    """
    Exception raised when a file is not referenced
    """

    def add_note(self, __note):
        super().add_note(__note)
        super().add_note("没有指定文件")


class CommunityNotExistError(Exception):
    """
    Exception raised when a community does not exist
    """
    pass

