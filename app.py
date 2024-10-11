from common.core import ProcessCore
from common.handler import handle_global_exception
# 加载配置
from common.constant import config


if __name__ == '__main__':
    try:
        # 初始化
        process_core = ProcessCore()
        print(process_core.results.message)
        for one_res in process_core.results.data:
            print(one_res[0] + ":" + one_res[1])
    except BaseException as e:
        if 'True' == str(config['app']['debug']):
            raise e
        else:
            handle_global_exception(e)
