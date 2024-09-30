from common.core import ProcessCore
from common.handler import handle_global_exception
import nest_asyncio
# 加载配置
from flask import Flask, send_from_directory
from common.constant import config
import webbrowser

app = Flask(__name__, static_folder='ui/dist', static_url_path='')


@app.route('/')  # 启动页面地址
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>')  # 托管所有静态文件
def static_proxy(path):
    return send_from_directory(app.static_folder, path)


if __name__ == "__main__":
    webbrowser.open(f'http://{config["app"]["host"]}:{config["app"]["port"]}/')
    app.run(
        debug=config['app']['debug'],
        port=config['app']['port'],
    )

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
