# -*- coding: utf-8 -*-
import markdown
from common.func import get_abs_path

def test_md():
    """
    测试markdown转html
    :return:
    """
    md = markdown.Markdown()
    md.convertFile(get_abs_path('/README.md'), 'readme.html',"utf-8")


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

    from common.func import load_yaml
    from common.func import get_root_path
    print()
    print(load_yaml(get_root_path() + '/config.yaml'))
