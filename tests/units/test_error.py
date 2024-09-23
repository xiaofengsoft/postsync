# -*- coding: utf-8 -*-
from common.error import FileNotSupportedError


def test_file_not_supported_error():
    raise FileNotSupportedError('.pdf')
