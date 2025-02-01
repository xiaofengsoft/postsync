"""
这个文件用来打包项目
"""
import os
import subprocess
import copy
import yaml
from yaml import Dumper
from utils.load import get_root_path
from common import constant as c
import platform
import sys

# 需要打包的spec文件
specs = ['PostSync.spec']

if __name__ == '__main__':
    if sys.argv.__len__() > 1 and sys.argv[1] != 'no-ui':
        # 切换到UI目录打包前端
        os.chdir(os.path.join(get_root_path(), 'ui'))
        os.system('npm run build')
    os.chdir(get_root_path())
    # 修改config.yaml中的参数
    config_backup = copy.deepcopy(c.config)
    c.config['default']['headless'] = False
    c.config['app']['debug'] = False
    with open(get_root_path() + '/config.yaml', 'w', encoding='utf-8') as file:
        yaml.dump(c.config, file, default_flow_style=False, encoding='utf-8', Dumper=Dumper, sort_keys=False,
                  allow_unicode=True)
        for spec in specs:
            # 定义命令
            command = ['pyinstaller', '-y', spec]
            # 执行命令
            subprocess.run(command)
        # 还原config.yaml
        file.seek(0)
        yaml.dump(config_backup, file, default_flow_style=False, encoding='utf-8', Dumper=Dumper, sort_keys=False,
                  allow_unicode=True)
