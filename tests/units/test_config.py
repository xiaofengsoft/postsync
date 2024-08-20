# -*- coding: utf-8 -*-
from common.core import config
from common.func import analyse_var

def test_config():
    analyse_var(config)


def test_default():
    analyse_var(config['default'])


def test_default_tags():
    analyse_var(config['default']['tags'])