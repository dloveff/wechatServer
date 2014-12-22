# -*- coding: utf-8 -*-
__author__ = 'alvinli'

import logging
import sys

from yaml import load
from setting import MSG_CONFIG_FILE

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class MsgConfigParser:

    def getConfig(self):
        try:
            with open(MSG_CONFIG_FILE, "r") as f:
                config = load(f)
        except Exception, e:
            logging.debug("配置文件读入错误")
            logging.exception(e)
            sys.exit()
        return config
