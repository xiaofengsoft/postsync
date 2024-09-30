# -*- coding: utf-8 -*-
import os

import pytest


@pytest.mark.parametrize("startpath", [
    (r"D:\Python"),
])
def test_dir(startpath):
    """
    This function is used to test the directory structure of the given path.
    :param startpath:
    :return:
    """
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{subindent}{f}")
