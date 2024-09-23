# -*- coding: utf-8 -*-
import pytest
from utils.file import get_file_path_without_ext
from utils.file import check_file_same_name_exists


@pytest.mark.parametrize("file_path, expected_result", [
    (r"D:\Python\Projects\MyGitProjects\PostSync\Readme.md", r"D:\Python\Projects\MyGitProjects\PostSync\Readme"),
    (r"D:\Python\Projects\MyGitProjects\PostSync\Readme.en.md", r"D:\Python\Projects\MyGitProjects\PostSync\Readme.en"),
    (r"tests\data\test.txt",r"tests\data\test"),
])
def test_get_file_path_without_ext(file_path, expected_result):
    print("file_path:", file_path)
    print("expected_result:", expected_result)
    assert get_file_path_without_ext(file_path) == expected_result


@pytest.mark.parametrize("file_path, expected_path, ext", [
    (r"tests\assets\posts\PostSync介绍.md",r"tests\assets\posts\PostSync介绍.html",'html'),
])
def test_check_file_same_name_exists(file_path, expected_path, ext):
    print("file_path:", file_path)
    print("expected_path:", expected_path)
    print("ext:", ext)
    print(check_file_same_name_exists(file_path, ext))
    assert check_file_same_name_exists(file_path, ext)
