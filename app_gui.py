import threading
# 加载配置
from flask import Flask
from common import constant as c
import webview


def flask_run():
    app = Flask(__name__, static_folder='ui/dist', static_url_path='')
    c.server_app = app
    from server.window import window_api
    from server.post import post_api
    from server.setting import setting_api
    app.register_blueprint(window_api)
    app.register_blueprint(post_api)
    app.register_blueprint(setting_api)
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
    webview.start(debug=bool(c.config['app']['debug']))
