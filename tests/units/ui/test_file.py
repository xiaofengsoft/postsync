"""
测试打开文件对话框
并获取选择的文件路径
从而实现前端发起信号，后端处理对话框选择的文件并返回
"""
import webview


def open_file(window: webview.Window):
    file_path = window.create_file_dialog(webview.OPEN_DIALOG)
    print("Selected file:", file_path)
    if file_path:
        # 这里可以处理选中的文件
        pass


def test_file_dialog():
    window = webview.create_window('File Dialog Example')
    webview.start(open_file, window)
