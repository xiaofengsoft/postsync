# -*- coding: utf-8 -*-
import pytest
from utils.file import convert_md_to_html
from utils.file import get_abs_path


@pytest.mark.parametrize('md_file', [
    r"C:\Users\xiaof\Desktop\PlayWright检测用户登录保存Cookie.md"
])
def test_md(md_file):
    """
    测试markdown转html
    :return:
    """
    convert_md_to_html(md_file)


def test_bs_html():
    """
    测试bs4的html解析，转换图片链接
    :return:
    """
    from bs4 import BeautifulSoup
    with (open(get_abs_path('tests/os/readme.html'), 'r', encoding='utf-8') as f):
        soup = BeautifulSoup(f.read(), 'html.parser')
        img_tags = soup.find_all("img")
        for img in img_tags:
            img['src'] = 'aaa.png'
        with open(get_abs_path('tests/os/readme_new.html'), 'w', encoding='utf-8') as f:
            f.write(str(soup))


def test_yaml_load():
    from utils.file import load_yaml
    from utils.file import get_root_path
    print()
    print(load_yaml(get_root_path() + '/config.yaml'))
