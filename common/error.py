# -*- coding: utf-8 -*-

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