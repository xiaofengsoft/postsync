# -*- coding: utf-8 -*-
import random
import time


def wait_random_time(begin_time: float = 0.2, end_time: float = 0.5):
    """
    等待随机时间
    :param begin_time: 开始时间
    :param end_time: 结束时间
    """
    wait_time = random.uniform(begin_time, end_time)
    time.sleep(wait_time)



