import asyncio
import multiprocessing
import threading

from webview import Window

from common.core import ProcessCore
from common.handler import handle_global_exception
import nest_asyncio
# 加载配置
from flask import Flask
from common import constant as c
import webview

from utils.load import get_path


def flask_run():
    app = Flask(__name__, static_folder='ui/dist', static_url_path='')
    c.server_app = app
    from server.window import window_api
    app.register_blueprint(window_api)
    from server import static  # 静态文件托管，不可删除
    app.run(
        debug=c.config['app']['debug'],
        port=c.APP_PORT,
        host=c.APP_HOST,
        use_reloader=False
    )


if __name__ == "__main__":
    main_window = webview.create_window(
        "PostSync",
        url=f'{c.APP_HTTP}://{c.APP_HOST}:{c.APP_PORT}',
        frameless=True,
        zoomable=True,
        draggable=True,
        resizable=True,
        width=c.config['view']['width'],
        height=c.config['view']['height'],

    )
    c.main_window = main_window
    threading.Thread(target=flask_run,daemon=True).start()
    webview.start(debug=c.config['app']['debug'])

# def main():
#     try:
#         # 允许嵌套协程
#         nest_asyncio.apply()
#         # 初始化
#         process_core = ProcessCore()
#         print(process_core.results.message)
#         for one_res in process_core.results.data:
#             print(one_res[0] + ":" + one_res[1])
#     except BaseException as e:
#         if 'True' == str(config['app']['debug']):
#             raise e
#         else:
#             handle_global_exception(e)
