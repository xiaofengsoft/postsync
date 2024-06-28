from common.core import *
from common.start import *
import nest_asyncio

# 允许嵌套协程
nest_asyncio.apply()

# 解析命令行参数
args = import_commands()


# 同步文件
def main():
    print()
    print('开始同步文件...')
    file, title, content,digest,  category, cover, topic,sites, tags, columns = process_args(args)  # 处理参数
    result = asyncio.run(async_post_file(file, title, content, digest, category, cover, topic,sites, tags, columns))
    print(result.message)
    for one_res in result.data:
        print(one_res[0] + ":" + one_res[1])
    print('同步完成！')


if __name__ == '__main__':
    main()
