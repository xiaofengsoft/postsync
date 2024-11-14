import ctypes
from ctypes import wintypes

# 定义回调函数的类型
EnumWindowsProc = ctypes.WINFUNCTYPE(
    ctypes.c_bool, wintypes.HWND, wintypes.LPARAM
)

# 获取Windows API中所需函数的引用
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
windows = []


def test_list_all_windows():
    def foreach_window(hwnd, lParam):
        """回调函数：列出窗口句柄和标题"""
        length = user32.GetWindowTextLengthW(hwnd)  # 获取窗口标题长度
        if length > 0:  # 忽略无标题的窗口
            title = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, title, length + 1)  # 获取窗口标题
            windows.append((hwnd, title.value))  # 保存句柄和标题
        return True  # 返回True以继续枚举下一个窗口
    """列出所有窗口句柄和标题"""
    windows.clear()  # 清空窗口列表
    user32.EnumWindows(EnumWindowsProc(foreach_window), 0)  # 开始枚举

    # 打印所有窗口句柄和标题
    for hwnd, title in windows:
        print(f"句柄: {hwnd}, 标题: {title}")


def test_window():
    hwnd = user32.FindWindowW(None, 'ChatGPT - Google Chrome')
    if hwnd != 0:
        user32.ShowWindow(hwnd, 0)  # 0 表示隐藏窗口
        print("窗口已隐藏")


def test_show_window():
    hwnd = user32.FindWindowW(None, 'ChatGPT - Google Chrome')
    if hwnd != 0:
        user32.ShowWindow(hwnd, 1)  # 1 表示显示窗口
        print("窗口已显示")