from importlib import import_module
import importlib
import common.constant as c
from common.core import Community
from common.error import BrowserError
import os
import inspect
from utils.load import get_path
import ast
from utils.file import get_file_name_without_ext
import shutil

from utils.storage import storage_config


def is_first_class_inherits_community(file_path):
    """判断文件中的第一个类是否继承自 Community"""
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            # 解析文件的 AST
            tree = ast.parse(f.read(), filename=file_path)
        except SyntaxError:
            print(f"Syntax error in file: {file_path}")
            return False

        # 遍历 AST 节点
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):  # 找到第一个类定义
                # 检查基类列表中是否有 Community
                for base in node.bases:
                    if isinstance(base, ast.Name) and base.id == "Community":
                        return True
                return False  # 第一个类不继承自 Community
        return False  # 文件中没有类定义


def get_plugins():
    # 获取插件列表
    module_names = []
    for root, dirs, files in os.walk(get_path('entity')):
        for file in files:
            if file.endswith(".py") and is_first_class_inherits_community(os.path.join(root, file)):
                module_name = get_file_name_without_ext(file)
                module = importlib.import_module(f"entity.{module_name}")
                community_class = next(
                    (cls for name, cls in inspect.getmembers(module, inspect.isclass)
                     if issubclass(cls, Community) and cls != Community),
                    None
                )
                desc = getattr(community_class, 'desc', '未知描述')
                name = getattr(community_class, 'site_name', '未知名称')
                module_names.append((module_name, {
                    "desc": desc,
                    "name": name
                }))
    return module_names


def plugin_uninstall(plugin_name: str) -> bool:
    try:
        # 获取插件文件路径
        plugin_path = os.path.join(get_path('entity'), f"{plugin_name}.py")
        # 检查文件是否存在
        if os.path.exists(plugin_path):
            # 删除文件
            os.remove(plugin_path)
            # 删除配置
            del c.config['default']['community'][plugin_name]
            storage_config()
            return True
        return False
    except Exception as e:
        print(f"Error uninstalling plugin: {str(e)}")
        return False


def plugin_install(file_path: str) -> bool:
    """
    安装插件到entity目录
    :param file_path: 插件文件临时路径
    :return: 是否安装成功
    """
    try:
        # 检查文件是否为Python文件
        if not file_path.endswith('.py'):
            return False

        # 检查文件是否包含继承自Community的类
        if not is_first_class_inherits_community(file_path):
            return False

        # 获取目标路径
        target_path = os.path.join(
            get_path('entity'), os.path.basename(file_path))

        # 复制文件到entity目录
        shutil.copy2(file_path, target_path)

        # 获取插件名称
        plugin_name = get_file_name_without_ext(target_path)

        # 获取插件模块第一个类中的 conf 字段
        module = import_module(f"entity.{plugin_name}")
        community_class = next(
            (cls for name, cls in inspect.getmembers(module, inspect.isclass)
             if issubclass(cls, Community) and cls != Community),
            None
        )
        conf = getattr(community_class, 'conf', None)
        # 将 conf 字段引入 config.yaml
        c.config['default']['community'][plugin_name] = conf
        # 将desc字段引入config.yaml
        desc = getattr(community_class, 'desc', '未知描述')
        name = getattr(community_class, 'site_name', '未知名称')
        c.config['default']['community'][plugin_name]['desc'] = name
        c.config['default']['community'][plugin_name]['is_login'] = False
        storage_config()
        return True
    except Exception as e:
        print(f"Error installing plugin: {str(e)}")
        return False
