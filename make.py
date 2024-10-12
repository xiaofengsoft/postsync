"""
这个文件用来打包项目
"""
import subprocess
import yaml
from yaml import Dumper
from utils.load import get_root_path
from common import constant as c

# 需要打包的spec文件
specs = ['PostSync.spec', 'PostSyncGUI.spec']

if __name__ == '__main__':
    # 修改config.yaml中的参数
    c.config['default']['headless'] = True
    c.config['app']['debug'] = False
    with open(get_root_path() + '/config.yaml', 'w', encoding='utf-8') as file:
        yaml.dump(c.config, file, default_flow_style=False, encoding='utf-8', Dumper=Dumper, sort_keys=False,
                  allow_unicode=True)

    for spec in specs:
        # 定义命令
        command = ['pyinstaller', '-y', spec]
        # 执行命令
        subprocess.run(command)
