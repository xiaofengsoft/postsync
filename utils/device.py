# -*- coding: utf-8 -*-
import ctypes


def get_real_resolution():
    """
    获取屏幕真实分辨率
    :return: 屏幕真实分辨率的宽和高
    """
    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32
    dc = user32.GetDC(None)

    width = gdi32.GetDeviceCaps(dc, 118)  # 原始分辨率的宽度
    height = gdi32.GetDeviceCaps(dc, 117)  # 原始分辨率的高度
    return width, height


def get_scale_resolution():
    """
    获取屏幕缩放分辨率
    :return: 屏幕缩放分辨率的宽和高
    """
    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32
    dc = user32.GetDC(None)
    widthScale = gdi32.GetDeviceCaps(dc, 8)  # 分辨率缩放后的宽度
    heightScale = gdi32.GetDeviceCaps(dc, 10)  # 分辨率缩放后的高度
    return widthScale, heightScale
