"""
这个文件用来打包项目
"""
import subprocess
import yaml
from yaml import Dumper
from utils.load import get_path
from common import constant as c

# 需要打包的spec文件
specs = ['PostSync.spec', 'PostSyncGUI.spec']

if __name__ == '__main__':
    for spec in specs:
        # 定义命令
        # 修改config.yaml中的debug为False
        c.config['app']['debug'] = False
        with open(get_path('/config.yaml'), 'w', encoding='utf-8') as file:
            yaml.dump(c.config, file, default_flow_style=False, encoding='utf-8', Dumper=Dumper, sort_keys=False,
                      allow_unicode=True)

        command = ['pyinstaller', '-y', spec]
        # 执行命令
        subprocess.run(command)
