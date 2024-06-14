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
    result = asyncio.run(async_post_files(args.filepaths, digests=args.digests, sites=args.sites, tags=args.tags,
                                          categories=args.categories,
                                          covers=args.covers, topics=args.topics, columns=args.columns))
    print(result.message)
    for one_res in result.data:
        print(one_res[0] + ":" + one_res[1])
    print('同步完成！')


if __name__ == '__main__':
    main()
