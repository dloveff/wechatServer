# -*- coding: utf-8 -*-
__author__ = 'alvinli'

import tornado
import logging
import hashlib

from ..setting import *


class WXInterfaceHandler(tornado.web.RedirectHandler):
    resonseString = ""

    def get(self):
        """接受get请求,提供微信服务器校验本接口地址"""
        self.valid()
        self.write(self.resonseString)

    def post(self):
        """ 接受post请求，与微信用户进行消息交互
        :return:
        """
        self.messageManage = MessageManage()
        self.responseMSg()
        self.write(self.resonseString)

    def valid(self):
        """
        接受微信服务器发来的校验码，校验成功后返回微信提供的校验码
        :return: 返回微信提供的随机字符串

        echostr: 微信HTTP发来的随机字符串
        """
        echostr = self.get_argument('echostr', '')
        if self.__checkSignature():
            logging.debug("echostr:%s" % echostr)
            self.resonseString = echostr

    def __checkSignature(self):
        """
        接受微信服务器发来的校验信息，并进行校验
        :return: True-校验成功；Flase-校验失败
            HTTPRequst signature: 微信发来的微信加密签名

            HTTPRequst timestamp: 微信发来的时间戳

            HTTPRequst nonce: 微信发来的随机数
        """
        signature = self.get_argument('signature', '')
        timestamp = self.get_argument('timestamp', '')
        nonce = self.get_argument('nonce', '')
        token = TOKEN
        tokenArray = [token, timestamp, nonce]
        tokenArray.sort()
        tokenStr = "".join(tokenArray)
        m = hashlib.sha1()
        m.update(tokenStr)
        sign_result = m.hexdigest()
        logging.debug("signStr:%s ; signature:%s" %(sign_result,signature))
        if sign_result == signature:
            logging.debug("return true")
            return True
        else:
            logging.debug("return false")
        return False

    def responseMsg(self):
        postStr = self.request.body
