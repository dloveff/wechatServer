# -*- coding: utf-8 -*-
__author__ = 'alvinli'

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import sys
import time
import logging

from tornado.util import import_object

from setting import PUSH_MSG_TYPE, PUSH_EVENT_TYPE, REPLY_PASSIVE_SMG_TYPE
from MsgConfigParser import MsgConfigParser

if sys.version_info.major < 3:
    reload(sys)
sys.setdefaultencoding('utf8')


class PushMsg(object):
    """
    消息推送对象
    """
    # 开发者微信号
    toUserName = ""
    #发送方帐号（一个OpenID）
    fromUserName = ""
    #消息创建时间 （整型）
    createTime = ""
    #消息类型
    msgType = ""
    #文本消息内容
    content = ""
    #消息id，64位整型
    msgId = ""
    #图片链接
    picUrl = ""
    #媒体id
    mediaId = ""
    #语音格式
    format = ""
    #视频消息缩略图的媒体id
    thumbMediaId = ""
    #地理位置纬度 latitude
    location_x = ""
    #地理位置经度 longitude
    location_y = ""
    #地图缩放大小
    scale = ""
    #地理位置信息
    label = ""
    #消息标题
    title = ""
    #消息描述
    description = ""
    #消息链接
    url = ""
    #事件类型
    event = ""
    #事件KEY值
    eventKey = ""
    #二维码的ticket
    ticket = ""
    #地理位置纬度
    latitude = ""
    #地理位置经度
    longitude = ""
    #地理位置精度
    precision = ""
    #语音识别结果，UTF8编码
    recognition = ""
    #发送状态为成功(模板消息)
    status = ""

    def _get_dic(self):
        namelist = filter(lambda x: not x.startswith("_"), dir(PushMsg))
        msgDic = {}
        for name in namelist:
            try:
                temp = getattr(self, name)
                # if name in ("content","label","title","description","recognition"):
                #     temp = temp.encode('utf-8')
                if temp != '':
                    msgDic[name] = str(temp)
            except Exception,e:
                pass
        return msgDic


class PassiveReplyMsg(object):
    """
    被动回复消息对象
    """
    # 接收方帐号（收到的OpenID）
    toUserName = ""
    #开发者微信号
    fromUserName = ""
    #消息创建时间 （整型）
    createTime = ""
    #消息类型
    msgType = ""
    #回复的消息内容（换行：在content中能够换行，微信客户端就支持换行显示）
    content = ""
    #图文消息个数，限制为10条以内
    articleCount = ""
    #多条图文消息信息，默认第一个item为大图
    articles = list()

    def _get_dic(self):
        namelist = filter(lambda x: not x.startswith("_"), dir(PushMsg))
        msgDic = {}
        for name in namelist:
            try:
                temp = getattr(self, name)
                # if name in ("content","label","title","description","recognition"):
                #     temp = temp.encode('utf-8')
                if temp != '':
                    msgDic[name] = str(temp)
            except Exception,e:
                pass
        return msgDic


class NewsArticle(object):
    """
    图文消息对象
    """
    # 图文消息标题
    title = ""
    #图文消息描述
    description = ""
    #图片链接，支持JPG、PNG格式，较好的效果为大图360*200，小图200*200
    picUrl = ""
    #点击图文消息跳转链接
    url = ""


class TextMessageHandler():
    """
    文本回复消息生成类
    """
    msgType = ""

    def msgHandle(self, pushMsg, handler):
        """
        处理文本信息
        :param pushMsg: 回复消息对象
        :param handler: 回复消息配置
        """
        replyMsg = None

        if pushMsg and handler:
            replyMsg = PassiveReplyMsg()
            replyMsg.toUserName = pushMsg.fromUserName
            replyMsg.fromUserName = pushMsg.toUserName
            replyMsg.createTime = str(int(time.time()))
            replyMsg.msgType = REPLY_PASSIVE_SMG_TYPE['text']
            replyMsg.content = handler.get('content', '')
        logging.debug("text replyMsg obj:", str(replyMsg._get_dic()))
        return replyMsg


class NewsMessageHandler():
    """
    图文回复消息生成类
    """
    msgType = ""

    def msgHandle(self, pushMsg, handler):
        """
        处理图文信息
        :param pushMsg: 回复消息对象
        :param handler: 回复消息配置
        """
        replyMsg = None

        if pushMsg and handler:
            replyMsg = PassiveReplyMsg()
            replyMsg.toUserName = pushMsg.fromUserName
            replyMsg.fromUserName = pushMsg.toUserName
            replyMsg.createTime = str(int(time.time()))
            replyMsg.msgType = REPLY_PASSIVE_SMG_TYPE['news']
            # 获取具体内容数据
            logging.debug("articles"+str(handler.get('content', '')))
            articles_list = handler.get('content', '')
            articles = list()
            for article_content in articles_list:
                article = NewsArticle()
                article.title = article_content['title']
                article.description = article_content['description']
                article.picUrl = article_content['picUrl']
                article.url = article_content['url']
                articles.append(article)
            replyMsg.articles = articles
            replyMsg.articleCount = len(replyMsg.articles)
        return replyMsg


class MessageManage(object):
    # 微信提交过来的解密后的消息
    pushMsg = None
    #返回给微信的加密后的消息
    replyMsg = None

    def __init__(self):
        self.replyMsg = PassiveReplyMsg()
        #读取配置文件
        msgCfgParser = MsgConfigParser()
        self.config = msgCfgParser.getConfig()

    def handle(self, postStr):
        """
        开放给外部的接口,用来处理接收的消息
        :param postStr:
        :return:
        """
        logging.debug("post xml:%s", postStr)
        #解析消息
        self.pushMsg = self.__pushMsgParser(postStr)
        #处理消息
        if self.pushMsg:
            self.__pushMsgHandler()

    def getReplyMsg(self):
        """
        获得返回给用户的信息
        :return:
        """
        if self.replyMsg:
            if self.replyMsg.msgType == REPLY_PASSIVE_SMG_TYPE['text']:
                replyMsgStr = self.__makeTextReplyMsg()
            else:
                replyMsgStr = self.__makeNewsReplyMsg()
        else:
            self.replyMsg = self.__makeWelcomeReplyMsg(None)
            replyMsgStr = self.__makeTextReplyMsg()
        logging.debug("reply msg:%s", replyMsgStr)
        return replyMsgStr

    def __pushMsgHandler(self):
        """
        将消息进行分类,找到不同类消息对应的处理对象
        :return:
        """
        #分析出消息交由谁处理
        handler_type_template = "{l1}_{l2}"
        if self.pushMsg.msgType == "event":
            level1 = 'event'
            level2 = self.pushMsg.event.lower()
        elif self.pushMsg.msgType == 'voice':
            level1 = "recognition"
            level2 = "voice"
        else:
            level1 = "receive"
            level2 = self.pushMsg.msgType.lower()
        """如果是文本类型,如果不是文本类型"""

        handler_name = handler_type_template.format(l1=level1, l2=level2)
        logging.debug("handler_name:%s", handler_name)

        #根据配置处理消息
        default_handler = self.config['default_handler']
        msg_handler = self.config['msg_handler']
        the_handler = msg_handler.get(handler_name, None)
        #如果handler不存在或者handler对应的关键字不存在
        if handler_name == 'recognition_voice':
            handler_content = the_handler.get(self.pushMsg.recognition, None)
        else:
            handler_content = the_handler.get(self.pushMsg.content, None)

        if the_handler is None or handler_content is None:
            logging.debug("msg content none")
            handler_content = default_handler
        logging.debug("msg handler content:%s", handler_content)
        self.__redirect(handler_content)

    def __redirect(self, msg_handler):
        """
        根据回复消息配置,生成回复消息的对象
        :param msg_handler: 回复消息配置
        """
        msg_handler_class = msg_handler['classes']
        try:
            the_handler = import_object(msg_handler_class)
            handler = the_handler()
            self.replyMsg = handler.msgHandle(self.pushMsg, msg_handler)
        except Exception, e:
            logging.exception(e)
            self.replyMsg = self.__makeWelcomeReplyMsg(None)

    def __makeWelcomeReplyMsg(self, welcome_msg):
        replyMsg = PassiveReplyMsg()
        replyMsg.toUsername = self.pushMsg.fromUsername
        replyMsg.fromUsername = self.pushMsg.toUsername
        replyMsg.createTime = str(int(time.time()))
        replyMsg.msgType = REPLY_PASSIVE_SMG_TYPE['text']
        if welcome_msg is None:
            replyMsg.content = self.config['welcome_msg']
        else:
            replyMsg.content = welcome_msg
        return replyMsg

    def __makeTextReplyMsg(self):
        textTmp = """<xml>
<ToUserName><![CDATA[{0}]]></ToUserName>
<FromUserName><![CDATA[{1}]]></FromUserName>
<CreateTime>{2}</CreateTime>
<MsgType><![CDATA[{3}]]></MsgType>
<Content><![CDATA[{4}]]></Content>
</xml>"""
        textStr = textTmp.format(self.replyMsg.toUserName,
                                 self.replyMsg.fromUserName,
                                 self.replyMsg.createTime,
                                 self.replyMsg.msgType,
                                 self.replyMsg.content)
        return textStr

    def __makeNewsReplyMsg(self):
        articleCount = len(self.replyMsg.articles)
        if articleCount > 0:
            itemTmp = """<item>
<Title><![CDATA[{0}]]></Title>
<Description><![CDATA[{1}]]></Description>
<PicUrl><![CDATA[{2}]]></PicUrl>
<Url><![CDATA[{3}]]></Url>
</item>"""
            articlesContent = ""
            for x in range(articleCount):
                itemStr = itemTmp.format(self.replyMsg.articles[x].title,
                                         self.replyMsg.articles[x].description,
                                         self.replyMsg.articles[x].picUrl,
                                         self.replyMsg.articles[x].url)
                articlesContent = articlesContent + itemStr

            textTmp = """<xml>
<ToUserName><![CDATA[{0}]]></ToUserName>
<FromUserName><![CDATA[{1}]]></FromUserName>
<CreateTime>{2}</CreateTime>
<MsgType><![CDATA[{3}]]></MsgType>
<ArticleCount>{4}</ArticleCount>
<Articles>
{5}
</Articles>
</xml>"""
            replyMsgStr = textTmp.format(self.replyMsg.toUserName,
                                         self.replyMsg.fromUserName,
                                         self.replyMsg.createTime,
                                         self.replyMsg.msgType,
                                         articleCount,
                                         articlesContent)
        else:
            self.replyMsg = self.__makeWelcomeReplyMsg(None)
            replyMsgStr = self.__makeTextReplyMsg()
        return replyMsgStr

    def __pushMsgParser(self, postStr):
        """
        解析微信服务推送过来的消息
        :param postStr 解密过的消息
        :return pushMsg 消息对象
        """
        postObj = ET.fromstring(postStr)
        pushMsg = None
        try:
            pushMsg = PushMsg()
            pushMsg.toUserName = postObj.find('ToUserName').text
            pushMsg.fromUserName = postObj.find('FromUserName').text
            pushMsg.createTime = postObj.find('CreateTime').text
            pushMsg.msgType = postObj.find('MsgType').text

            msgType = pushMsg.msgType

            if msgType != PUSH_MSG_TYPE['event']:
                pushMsg.msgId = postObj.find('MsgId').text

            if msgType == PUSH_MSG_TYPE['text']:
                pushMsg.content = postObj.find('Content').text
            elif msgType == PUSH_MSG_TYPE['image']:
                pushMsg.picUrl = postObj.find('PicUrl').text
                pushMsg.mediaId = postObj.find('MediaId').text
            elif msgType == PUSH_MSG_TYPE['voice']:
                pushMsg.mediaId = postObj.find('MediaId').text
                pushMsg.format = postObj.find('Format').text
                rec = postObj.find('Recognition')
                if rec.text is not None:
                    pushMsg.recognition = rec.text
                else:
                    pushMsg.recognition = "0"
            elif msgType == PUSH_MSG_TYPE['video']:
                pushMsg.mediaId = postObj.find('MediaId').text
                pushMsg.thumbMediaId = postObj.find('ThumbMediaId').text
            elif msgType == PUSH_MSG_TYPE['location']:
                pushMsg.location_x = postObj.find('Location_X').text
                pushMsg.location_y = postObj.find('Location_Y').text
                pushMsg.scale = postObj.find('Scale').text
                pushMsg.label = postObj.find('Label').text
            elif msgType == PUSH_MSG_TYPE['link']:
                pushMsg.title = postObj.find('Title').text
                pushMsg.description = postObj.find('Description').text
                pushMsg.url = postObj.find('Url').text
            elif msgType == PUSH_MSG_TYPE['event']:
                pushMsg.event = postObj.find('Event').text
                event = pushMsg.event
                if event == PUSH_EVENT_TYPE['subscribe']:
                    eventKeyEle = postObj.find('EventKey')
                    if eventKeyEle is not None:
                        pushMsg.eventKey = eventKeyEle.text
                        pushMsg.ticket = postObj.find('Ticket').text
                elif event == PUSH_EVENT_TYPE['unsubscribe']:
                    pass
                elif event == PUSH_EVENT_TYPE['scan']:
                    pushMsg.eventKey = postObj.find('EventKey').text
                    pushMsg.ticket = postObj.find('Ticket').text
                elif event == PUSH_EVENT_TYPE['location']:
                    pushMsg.latitude = postObj.find('Latitude').text
                    pushMsg.longitude = postObj.find('Longitude').text
                    pushMsg.precision = postObj.find('Precision').text
                elif event == PUSH_EVENT_TYPE['click']:
                    pushMsg.eventKey = postObj.find('EventKey').text
                elif event == PUSH_EVENT_TYPE['view']:
                    pushMsg.eventKey = postObj.find('EventKey').text
                elif event == PUSH_EVENT_TYPE['template']:
                    pushMsg.msgId = postObj.find('MsgID').text
                    pushMsg.status = postObj.find('Status').text
            else:
                logging.debug("未知类型 %s", msgType)
        except Exception, e:
            logging.exception(e)
        logging.debug("解析后的消息"+str(pushMsg._get_dic()))
        return pushMsg


# testxml = """<xml><ToUserName><![CDATA[gh_95fd1b1b0bc3]]></ToUserName>
# <FromUserName><![CDATA[o7Hr3joUtQrXS4g6XCeHS98KYuZc]]></FromUserName>
# <CreateTime>1419237008</CreateTime>
# <MsgType><![CDATA[voice]]></MsgType>
# <MediaId><![CDATA[4f7i1JgCdkuMSmd9iY6eoInpN-A65PiO-NFcFFArrHD8rJ2_PLjdm1mPPzzpiWrz]]></MediaId>
# <Format><![CDATA[amr]]></Format>
# <MsgId>6095576534632890368</MsgId>
# <Recognition><![CDATA[]]></Recognition>
# </xml>
# """
# if __name__ == '__main__':
#     pushMsg = pushMsgParser(testxml)
#     print(pushMsg._get_dic())

