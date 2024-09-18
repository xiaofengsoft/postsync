# -*- coding: utf-8 -*-
from common.argument import PostArgumentParser
from common.config import config


def import_commands():
    parser = PostArgumentParser(
        prog=config['app']['name'],
        description=config['app']['description'],
        epilog=config['app']['epilog'],
        exit_on_error=True  # 禁止自动捕获异常
    )
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s ' + config['app']['version'],
                        help='查看版本号')

    parser.add_argument('-f', '--file',
                        help='需要同步的文件路径',
                        type=str,
                        required=True
                        )
    parser.add_argument('-ti', '--title',
                        help='文档标题',
                        type=str,
                        nargs='?'
                        )
    parser.add_argument('-d', '--digest',
                        help='文档的摘要',
                        type=str,
                        nargs='?'
                        )
    parser.add_argument('-s', '--site',
                        help='要上传的网站列表，必须从给定的网站列表中选择 %(choices)s，默认全部上传',
                        type=str,
                        choices=config['default']['community'].keys(),
                        nargs='*'
                        )
    parser.add_argument('-ca', '--category',
                        help='文档的分类',
                        type=str,
                        nargs='?'
                        )
    parser.add_argument('-co', '--cover',
                        help='文档的封面',
                        type=str,
                        nargs='?'
                        )
    parser.add_argument('-to', '--topic',
                        help='文档的话题',
                        type=str,
                        nargs='?'
                        )
    parser.add_argument('-t', '--tag',
                        help='文档的标签',
                        type=str,
                        nargs='*'
                        )
    parser.add_argument('-cl', '--column',
                        help='文档的专栏',
                        type=str,
                        nargs='*'
                        )
    args = parser.parse_args()
    return args

