from importlib import import_module
import common.constant as c
from common.error import BrowserError
import os
from utils.load import get_path
import ast
from utils.file import get_file_name_without_ext


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
                if module_name in c.config['default']['community'].keys():
                    module_names.append(module_name)
    return module_names
