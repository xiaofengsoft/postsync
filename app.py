import threading
from flask import Flask
from common import constant as c
import webview
from utils.storage import setup_wizard
from server.dashboard import dashboard_api
from server.write import write_api


class WindowApi():
    def __init__(self, window: webview.Window):
        self.window = window

    def moveWindow(self, x: float, y: float):
        self.window.move(x, y)


def flask_run():
    app = Flask(__name__, static_folder='ui/dist', static_url_path='')
    c.server_app = app
    from server.window import window_api
    from server.post import post_api
    from server.setting import setting_api
    from server.plugins import plugins_api
    app.register_blueprint(plugins_api)
    app.register_blueprint(window_api)
    app.register_blueprint(post_api)
    app.register_blueprint(setting_api)
    app.register_blueprint(dashboard_api)
    app.register_blueprint(write_api)
    from server import static  # 静态文件托管，不可删除
    app.run(
        debug=c.config['app']['debug'],
        port=c.APP_PORT,
        host=c.APP_HOST,
        use_reloader=False
    )


if __name__ == "__main__":
    # 检测是否安装
    if not c.config['app']['installed']:
        if not setup_wizard():
            exit(1)

    main_window = webview.create_window(
        "PostSync",
        url=f'{c.APP_HTTP}://{c.APP_HOST}:{c.APP_PORT}',
        frameless=True,
        zoomable=False,
        draggable=True,
        resizable=True,
        easy_drag=False,
        width=c.config['view']['width'],
        height=c.config['view']['height'],
    )
    webview.DRAG_REGION_SELECTOR = '#app > section > header > div > div > ul'
    c.main_window = main_window
    threading.Thread(target=flask_run, daemon=True).start()

    webview.start(
        debug=bool(c.config['app']['debug']),
        private_mode=False,
        gui='edgechromium',
        storage_path=c.config['data']['webview']['path']
    )
