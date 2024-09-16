# -*- coding: utf-8 -*-
from utils.file import load_yaml
from utils.file import get_root_path
import os
from common import constant

config = load_yaml(os.path.join(get_root_path(), constant.CONFIG_FILE_PATH))