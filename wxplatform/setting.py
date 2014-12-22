# -*- coding: utf-8 -*-
__author__ = 'alvinli'

"""
全局变量设置
"""

DEBUG = True

# 微信token参数
TOKEN = "gaosanyiban2007"  # "cHtG2014wQ"

# AES 密钥
AESKEY = "HoMIsqaYlhsZLyDDXztfk8I2uPNTZGPfKzFuj6VlrVv"  # "akpAwi1oDIxhqPTbJzRadzxLdJGeJw1keDO9YnK6Sr5"

# APP ID KEY
APPID = "wx76a8945d1b1e830f"  #"wx088d3771f8ed2a91"

#APP SECRET KEY
APPSECRET = "07a2acfac5318b5b85068dbd66512835"  #"1753b7f71c3f8991cb0230cee47da635"

#web配置文件
WEB_CONFIG_FILE = "config/web.yaml"

#消息配置文件
MSG_CONFIG_FILE = "config/msg.yaml"

#推送消息的类型
PUSH_MSG_TYPE = {'text': 'text', 'image': 'image', 'voice': 'voice', 'video': 'video', 'location': 'location',
                 'link': 'link', 'event': 'event'}

PUSH_EVENT_TYPE = {'subscribe': 'subscribe', 'unsubscribe': 'unsubscribe', 'scan': 'SCAN', 'location': 'LOCATION',
                   'click': 'CLICK', 'view': 'VIEW', 'template': 'TEMPLATESENDJOBFINISH'}
#回复被动消息的类型
REPLY_PASSIVE_SMG_TYPE = {'text': 'text', 'news': 'news'}

WARING_BUSY_SYS = -1
SUCCESS = 0