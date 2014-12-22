# -*- coding: utf-8 -*-
__author__ = 'alvinli'

import os
import sys
import tornado.web
import logging

root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root, 'site-packages'))


from wxplatform.setting import *
from wxplatform.WebConfigParser import WebConfigParser

if sys.version_info.major < 3:
    reload(sys)
sys.setdefaultencoding('utf8')
logging.basicConfig(level=logging.DEBUG)


settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug": DEBUG
}

webConfig = WebConfigParser(WEB_CONFIG_FILE)
urlPatterns = webConfig.urlPattern()

application = tornado.web.Application(urlPatterns, **settings)