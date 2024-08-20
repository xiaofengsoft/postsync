# -*- coding: utf-8 -*-
import os
from common.func import get_root_path

def test_arguments_no_f_exception():
    os.chdir(get_root_path())
    os.system('python app.py')


def test_arguments_with_f_without_file_exception():
    os.chdir(get_root_path())
    os.system('python app.py -f ')
