# -*- coding: utf-8 -*-
import pytest
from utils.file import get_abs_path


def test_convert_html_to_docx():
    from utils.file import get_abs_path
    from common.func import convert_html_to_docx
    abs_path = get_abs_path("tests/assets/test.html")
    convert_html_to_docx(abs_path)


def test_convert_html_img_path_to_abs_path():
    from common.func import convert_html_img_path_to_abs_path
    abs_path = get_abs_path("tests/assets/test.html")
    convert_html_img_path_to_abs_path(abs_path)


@pytest.mark.parametrize("file_path",
                         [r"C:\Windows",
                          r"tests/assets/imgs/logo.png"])
def test_get_path(file_path):
    from utils.file import get_path
    path = get_path(file_path)
    print()
    print(path)


@pytest.mark.parametrize("file_path",
                         [r"tests/assets/jsons/test.json"])
def test_format_json_file(file_path):
    from utils.data import format_json_file
    print(format_json_file(file_path))
