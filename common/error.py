# -*- coding: utf-8 -*-

class FileNotReferencedError(Exception):
    """
    Exception raised when a file is not referenced
    """
    pass


class CommunityNotExistError(Exception):
    """
    Exception raised when a community does not exist
    """
    pass