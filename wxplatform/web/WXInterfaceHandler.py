# -*- coding: utf-8 -*-
__author__ = 'alvinli'

import tornado.web
import logging
import hashlib
import time

from ..setting import *
from ..wxCrypt.WXBizMsgCrypt import WXBizMsgCrypt
from ..wxCrypt import ierror
from ..MessageManage import MessageManage


class WXInterfaceHandler(tornado.web.RequestHandler):
    responseString = ""
    wechatPostContent = ""
    crypt_handler = WXBizMsgCrypt(TOKEN, AESKEY, APPID)

    def get(self):
        """接受get请求,提供微信服务器校验本接口地址"""
        self.valid()
        self.write(self.responseString)

    def post(self):
        """ 接受post请求，与微信用户进行消息交互
        :return:
        """
        #检查消息签名
        if self.__checkSignature() is False:
            logging.warning("消息签名错误")
            self.write(self.responseString)
        #解密&检查消息体的签名
        encrypt_type = self.get_argument('encrypt_type', '')
        msg_signature = self.get_argument('msg_signature', '')
        timestamp = self.get_argument('timestamp', '')
        nonce = self.get_argument('nonce', '')
        xml_str = self.request.body
        logging.debug("request_xml", xml_str)
        if encrypt_type.lower() == "aes":
            ret, decrypt_xml = self.crypt_handler.DecryptMsg(xml_str, msg_signature, timestamp, nonce)
            if ret != ierror.WXBizMsgCrypt_OK:
                logging.error("解密失败:%s", ret)
                self.write(self.responseString)
            self.wechatPostContent = decrypt_xml
        else:
            self.wechatPostContent = xml_str

        #处理消息
        self.messageManage = MessageManage()
        self.responseMsg()
        self.write(self.responseString)

    def valid(self):
        """
        接受微信服务器发来的校验码，校验成功后返回微信提供的校验码
        :return: 返回微信提供的随机字符串

        echostr: 微信HTTP发来的随机字符串
        """
        echostr = self.get_argument('echostr', '')
        if self.__checkSignature():
            logging.debug("echostr:%s" % echostr)
            self.responseString = echostr

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
        tokenArray = [TOKEN, timestamp, nonce]
        tokenArray.sort()
        tokenStr = "".join(tokenArray)
        m = hashlib.sha1()
        m.update(tokenStr)
        sign_result = m.hexdigest()
        logging.debug("signStr:%s ; signature:%s" % (sign_result, signature))
        if sign_result == signature:
            logging.debug("return true")
            return True
        else:
            logging.debug("return false")
        return False

    def responseMsg(self):
        """
        解析微信用户推送d消息,并回复微信用户
        :return:
        """
        postStr = self.wechatPostContent
        if postStr:
            self.messageManage.handle(postStr)
            replyMsg = self.messageManage.getReplyMsg()
            logging.debug("replay msg raw:%s", replyMsg)
            #加密
            snonce = str(int(time.time()))
            ret, encrypt_xml = self.crypt_handler.EncryptMsg(replyMsg, snonce)
            if ret == ierror.WXBizMsgCrypt_OK:
                self.responseString = encrypt_xml
            else:
                self.responseString = ""
        else:
            self.responseString = ""
        logging.debug("response str:%s", self.responseString)
