# -*- coding: utf-8 -*-
import argparse


class PostArgumentParser(argparse.ArgumentParser):
    """
    继承自argparse.ArgumentParser，重写exit方法，防止打印额外内容
    """
    def error(self, message):
        self.exit()