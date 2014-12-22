# -*- coding: utf-8 -*-
__author__ = 'alvinli'

import logging
import sys

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class WebConfigParser:

    def __init__(self,configFile):
        self.config == self.__getConfig(configFile)

    def __getConfig(self,configFile):
        try:
            with open(configFile,"r") as f:
                config = load(f)
        except Exception,e:
            logging.debug("配置文件读入错误")
            logging.exception(e)
            sys.exit()
        return config

    def urlPattern(self):
        urlPatterns = list()
        for pair in self.config['urlPatterns']:
            pattern = (pair['url'], pair['handler'])
            urlPatterns.append(pattern)
        logging.debug("urlPatterns:%s" % str(urlPatterns))
        return urlPatterns


if __name__ == '__main__':
    import os
    with open("/home/alvinli/pycode/fanatactivity/1/config/web.yaml",'r') as f:
        data = load(f)
        print str(data)


