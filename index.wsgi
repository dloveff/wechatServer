# -*- coding: utf-8 -*-
import hashlib

__author__ = 'alvinli'
import os
import sys
import tornado.web
import logging
import time
import json

root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root, 'site-packages'))


from wechatCrypt.WXBizMsgCrypt import SHA1
from platform.tokentools import getAccessToken
from platform.KVDB import getValue, getInfo, ACCESS_TOKEN_KEY, ACCESS_TOKEN_EXPIRE_TIME_KEY
from platform.setting import *
from platform.WebConfigParser import WebConfigParser

if sys.version_info.major < 3:
    reload(sys)
sys.setdefaultencoding('utf8')
logging.basicConfig(level=logging.DEBUG)

sha1 = SHA1()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        token = 'cHtG2014wQ'
        signature = self.get_argument('signature', 'default')
        timestamp = self.get_argument('timestamp', 'default')
        nonce = self.get_argument('nonce', 'default')
        echostr = self.get_argument('echostr', 'default')
        tokenArray = [token, timestamp, nonce]
        tokenArray.sort()
        tokenStr = ''.join(tokenArray)
        m = hashlib.sha1()
        m.update(tokenStr)
        sResult = m.hexdigest()
        if sResult == signature:
            logging.debug('auth ')
            self.write(echostr)
        else:
            logging.debug('error auth')
            self.write('params error')

    def post(self):
        signature = self.get_argument('signature',None)
        timestamp = self.get_argument('timestamp',None)
        nonce = self.get_argument('nonce',None)
        encrypt_type = self.get_argument('encrypt_type',None)
        msg_signature = self.get_argument('msg_signature',None)
        msg_body = self.request.body
        logging.debug(json.dumps({'signature':signature,'timestamp':timestamp,'nonce':nonce,'encrypt_type':encrypt_type,'msg_signature':msg_signature,'msg_body':msg_body}))
        self.write("")


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
        self.write(acc_token)


class TokenHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("token:%s time:%s now time:%s" % (str(getValue(ACCESS_TOKEN_KEY)), str(getValue(ACCESS_TOKEN_EXPIRE_TIME_KEY)), str(int(time.time()))))




settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug": DEBUG
}

webConfig = WebConfigParser(WEB_CONFIG_FILE)
urlPatterns = webConfig.urlPattern()
application = tornado.web.Application(urlPatterns, **settings)