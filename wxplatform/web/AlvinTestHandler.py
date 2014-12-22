# -*- coding: utf-8 -*-
__author__ = 'alvinli'

import logging
import time

import tornado
from ..tokentools import getAccessToken
from ..wxcache.KVDB import getValue, getInfo, ACCESS_TOKEN_KEY, ACCESS_TOKEN_EXPIRE_TIME_KEY
from ..setting import *




class TestHandler(tornado.web.RequestHandler):
    def get(self):
        # setValue("hello","world")
        # store_data = getValue("hello")
        # logging.debug(str(store_data))
        # kvdb_info = getInfo()
        # self.write(str(store_data)+"~~~"+kvdb_info)
        acc_token = getAccessToken()
        logging.debug("acc token:%s", str(getValue(ACCESS_TOKEN_KEY)))
        logging.debug(getInfo())
        self.write(str(acc_token))


class TokenHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("token:%s time:%s now time:%s" % (str(getValue(ACCESS_TOKEN_KEY)), str(getValue(ACCESS_TOKEN_EXPIRE_TIME_KEY)), str(int(time.time()))))

