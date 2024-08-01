from common.core import *
from common.start import *
from common.handler import handle_global_exception
import nest_asyncio
import sys


# 同步文件
def main():
    try:
        # 允许嵌套协程
        nest_asyncio.apply()
        # 解析命令行参数
        args = import_commands()
        print()
        print('开始同步文件...')
        file, title, content, digest, category, cover, topic, sites, tags, columns = process_args(args)  # 处理参数
        result = asyncio.run(async_post_file(file, title, content, digest, category, cover, topic, sites, tags, columns))
        print(result.message)
        for one_res in result.data:
            print(one_res[0] + ":" + one_res[1])
        print('同步完成！')
    except BaseException as e:
        # TODO: 开启Debug模式
        if config['app']['debug'] == 'True':
            raise e
        else:
            handle_global_exception(e)


if __name__ == '__main__':
    main()
