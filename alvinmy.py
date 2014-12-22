# -*- coding: utf-8 -*-
__author__ = 'alvinli'

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

#-------------解密



#-------------识别消息类型
testxml = """<xml>
 <ToUserName><![CDATA[toUser]]></ToUserName>
 <FromUserName><![CDATA[fromUser]]></FromUserName>
 <CreateTime>1348831860</CreateTime>
 <MsgType><![CDATA[text]]></MsgType>
 <Content><![CDATA[this is a test]]></Content>
 <MsgId>1234567890123456</MsgId>
 </xml>
"""

root = ET.fromstring(testxml)

handler_name_tmp = "{l1}_{l2}"
msg_type = root.find("MsgType").text

if msg_type == "event":
    #事件类型
    level1 = msg_type.lower()
    event = root.find("Event").text
    level2 = event.lower()
elif msg_type == "voice":
    level1 = "recognition"
    level2 = "voice"
else:
    level1 = 'receive'
    level2 = msg_type.lower()

hanlder_name = handler_name_tmp.format(l1=level1, l2=level2)


class MSGHandler:
    @staticmethod
    def receive_text():
        """
        :return: 发送者openID,content,msgid
        """
        pass

    @staticmethod
    def receive_image():
        """

        :return:
        """
        pass

    @staticmethod
    def receive_voice():
        """

        :return:
        """
        pass

    @staticmethod
    def receive_video():
        """

        :return:
        """
        pass

    @staticmethod
    def receive_location():
        """

        :return:
        """
        pass

    @staticmethod
    def receive_link():
        """

        :return:
        """
        pass

    @staticmethod
    def recognition_voice():
        """
        :return: 发送者openID,recognition,msgid
        """
        pass

    @staticmethod
    def event_subscribe():
        """
        :return: 发送者openID or 发送者openID,eventkey
        """
        pass

    @staticmethod
    def event_unsubscribe():
        """

        :return: 发送者openID
        """
        pass

    @staticmethod
    def event_scan():
        """

        :return: 发送者openID,eventkey
        """
        pass

    @staticmethod
    def event_location():
        """

        :return: 发送者openID,latitude,longitude,precision
        """
        pass

    @staticmethod
    def event_click():
        """

        :return: 发送者openID,eventkey
        """
        pass

    @staticmethod
    def event_view():
        """

        :return: 发送者openID,eventkey
        """
        pass

class MyTest:
    testString = "halle"
    def hello(self):
        print self.testString


if __name__ == '__main__':
    # att = getattr(handler,"test_text")
    # att()
    root = ET.fromstring(testxml)
    test = root.find('hello')
    print str(test)

