# -*- coding: utf-8 -*-
"""
加载项目需要的工具库
此文件不可以依赖配置文件
"""
import os


def load_yaml(path: str, encoding='utf-8') -> dict:
    """
    加载YAML文件
    """
    import yaml
    with open(path, 'r', encoding=encoding) as f:
        yaml_data = yaml.load(stream=f, Loader=yaml.FullLoader)
        return yaml_data


def get_root_path() -> str:
    """
    获取项目根目录路径
    """
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_path(path: str) -> str:
    """
    给出可用路径
    如果参数是项目相对路径，则返回项目根目录路径加上参数路径
    如果参数是绝对路径，则直接返回参数路径
    :param path: 路径
    :return: 可用路径
    """
    if os.path.isabs(path):
        return os.path.normpath(path)
    else:
        return os.path.normpath(os.path.join(get_root_path(), path))