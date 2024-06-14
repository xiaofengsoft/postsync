# -*- coding: utf-8 -*-
import argparse
from common.core import config


def import_commands():
    parser = argparse.ArgumentParser(

        prog=config['app']['name'],
        description=config['app']['description'],
        epilog=config['app']['epilog']
    )
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s ' + config['app']['version'],
                        help='查看版本号'
                        )

    parser.add_argument('filepaths',
                        help='需要同步的文件路径，可以是列表',
                        type=str,
                        nargs='+'
                        )
    parser.add_argument('-d', '--digests',
                        help='文档的摘要，可以是列表，请和文件列表一一对应',
                        type=str,
                        nargs='*'
                        )
    parser.add_argument('-s', '--sites',
                        help='要上传的网站列表，必须从给定的网站列表中选择 [%(choices)s)，默认全部上传，请用空格分隔',
                        type=str,
                        choices=config['default']['community'].keys(),
                        nargs='*'
                        )
    parser.add_argument('-t', '--tags',
                        help='文档的标签，可以是列表，请和文件列表一一对应，对于每一个文档的标签，请用英文,分隔',
                        type=str,
                        nargs='*'
                        )
    parser.add_argument('-ca', '--categories',
                        help='文档的分类，可以是列表，请和文件列表一一对应',
                        type=str,
                        nargs='*'
                        )
    parser.add_argument('-co', '--covers',
                        help='文档的封面，可以是列表，请和文件列表一一对应',
                        type=str,
                        nargs='*'
                        )
    parser.add_argument('-to', '--topics',
                        help='文档的主题，可以是列表，请和文件列表一一对应',
                        type=str,
                        nargs='*'
                        )
    parser.add_argument('-cl', '--columns',
                        help='文档的专栏，可以是列表，请和文件列表一一对应, 对于每一个文档的专栏，请用英文,分隔',
                        type=str,
                        nargs='*'
                        )
    args = parser.parse_args()
    return args
