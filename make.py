"""
这个文件用来打包项目
"""
import subprocess

# 需要打包的spec文件
specs = ['PostSync.spec', 'PostSyncGUI.spec']

if __name__ == '__main__':
    for spec in specs:
        # 定义命令
        command = ['pyinstaller', '-y', spec]
        # 执行命令
        subprocess.run(command)
