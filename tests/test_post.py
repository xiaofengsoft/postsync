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

    @pytest.mark.parametrize("site", ['wordpress'])
    def test_post_with_single_site(self, site):
        """
        单次测试各个网站的
        :param site:
        :return:
        """
        print(site)
        os.system(f'python app.py -f {self.test_file} -co static/imgs/logo.png -s {site}')

    @pytest.mark.parametrize("sites", ['csdn juejin zhihu wechat cnblog wordpress'])
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

    @pytest.mark.parametrize(
        'file,title,category,columns,tags,sites,cover_img',
        [
            # ('tests/assets/posts/WordPress加载流程的解读分析.md', 'title', 'PHP', 'PHP文章', 'php github', 'csdn juejin wordpress zhihu cnblog wechat bilibili','tests/assets/imgs/wp.png'),
            # ('tests/assets/posts/WordPress加载流程的解读分析.md', 'title', 'PHP', 'PHP文章', 'php github', 'zhihu cnblog wechat','tests/assets/imgs/wp.png'),
            ('tests/assets/posts/WordPress加载流程的解读分析.md', 'title', 'PHP', 'PHP文章', 'php github', 'cnblog','tests/assets/imgs/wp.png'),
        ]
    )
    def test_post_all_args(self,file,title, category, columns, tags, sites, cover_img):
        """
        单次测试所有参数的发布
        :return:
        """
        os.system(f'python app.py -f {file} -t {tags} -s {sites} -ca {category} -co {cover_img} -cl {columns}')