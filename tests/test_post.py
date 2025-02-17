# -*- coding: utf-8 -*-
import os
import subprocess

from utils.file import get_root_path
import pytest


def run_command(command):
    """运行命令并处理错误"""
    try:
        subprocess.run(command, shell=True, check=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e.cmd}")
        print(f"错误信息: {e.stderr.decode()}")


class TestPost:

    def setup_class(self):
        os.chdir(get_root_path())

    @pytest.mark.parametrize("site , test_file", [('zhihu', "tests/assets/posts/PostSync介绍.md")])
    def test_post_with_single_site(self, site, test_file):
        """
        单次测试各个网站的
        :param site:
        :return:
        """
        run_command(f'python app.py -f {test_file} -s {site}')

    @pytest.mark.parametrize(
        'file,category,columns,tags,sites,cover_img',
        [
            ('tests/assets/posts/PostSync介绍.docx', 'Python', '解决问题', 'python adguard',
             'bilibili', 'tests/assets/imgs/wp.png'),
            # (r'"C:\Users\xiaof\Desktop\module collections has no attribute Hashable PyDocx 库报错.md"', 'Python', '解决',
            #  'PyDocx Hash', 'cnblog', r'')
        ]
    )
    def test_post_all_args(self, file, category, columns, tags, sites, cover_img):
        """
        单次测试所有参数的发布
        :return:
        """
        order = f'python app.py -f {file} -s {sites} -ca {
            category} -co {cover_img} -cl {columns} -t {tags} '
        print(order)
        run_command(order)

    def test_help(self):
        run_command('python app.py --help')
