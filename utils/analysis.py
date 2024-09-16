# -*- coding: utf-8 -*-
import typing as t
from functools import wraps
import time


def calculate_time(func):
    """
    计算函数执行时间的装饰器
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # 记录函数开始执行的时间
        result = func(*args, **kwargs)  # 执行函数
        end_time = time.time()  # 记录函数执行结束的时间
        execution_time = end_time - start_time  # 计算执行时间
        print(f"Function {func.__name__} took {execution_time} seconds to execute")
        return result

    return wrapper


def analyse_var(var: t.Any, retract: t.Optional[int] = 0):
    """
    解析变量
    :param var:
    :param retract:
    :return:
    """
    print(f"{' ' * retract}type: {type(var)}")
    print(f"{' ' * retract}var: {var}")
    if isinstance(var, (int, float, str, bool)):
        print(f"{' ' * retract}length: {len(str(var))}")
    elif isinstance(var, (list, tuple)):
        for i, item in enumerate(var):
            print(f"{' ' * retract}[{i}]")
            analyse_var(item, retract + 2)
    elif isinstance(var, dict):
        for key, value in var.items():
            print(f"{' ' * retract}{key}:")
            analyse_var(value, retract + 2)