# -*- coding: utf-8 -*-
import pytest
from utils.file import get_path
from utils.data import convert_md_img_path_to_abs_path


@pytest.mark.parametrize("path", [
    "tests/assets/posts/PostSync介绍.md"
])
def test_convert_md_img_path_to_abs_path(path: str):
    convert_md_img_path_to_abs_path(get_path(path))