# -*- coding: utf-8 -*-
import os
from common.func import get_root_path
import pytest


class TestPost:
    def setup_class(self):
        self.test_file = 'tests/assets/test.md'
        os.chdir(get_root_path())

    def test_post(self):
        os.chdir(get_root_path())
        os.system('python app.py  -co static/imgs/logo.png -t python,github')

    @pytest.mark.parametrize("site", ['zhihu', 'csdn', 'juejin'])
    def test_post_with_single_site(self, site):
        """
        单次测试各个网站的
        :param site:
        :return:
        """
        print(site)
        os.system(f'python app.py -f {self.test_file} -co static/imgs/logo.png -s {site}')

    @pytest.mark.parametrize("sites", ['csdn juejin zhihu'])
    def test_post_with_sites(self, sites):
        """
        单次测试多个网站的发布
        :return:
        """
        order = f'python app.py -f {self.test_file} -co static/imgs/logo.png -s {sites}'
        os.system(order)
        print(order)

    @pytest.mark.parametrize("tags", ['python github'])
    def test_post_with_sites_and_tags(self, tags):
        """
        单次测试各个网站的发布，并添加标签
        :return:
        """
        os.system(f'python app.py -f {self.test_file} -co static/imgs/logo.png -s juejin csdn -t {tags}')
