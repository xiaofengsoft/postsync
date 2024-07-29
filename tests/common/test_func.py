# -*- coding: utf-8 -*-
from common.func import *

def test_convert_html_to_docx():
    abs_path = get_abs_path("tests/assets/test.html")

    convert_html_to_docx(abs_path)


def test_convert_html_img_path_to_abs_path():
    abs_path = get_abs_path("tests/assets/test.html")
    convert_html_img_path_to_abs_path(abs_path)