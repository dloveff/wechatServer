# -*- coding: utf-8 -*-
__author__ = 'alvinli'

import os
import sys

root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root, 'site-packages'))

import logging
import setting
import time
import requests
from wxcache.KVDB import getValue, setValue, ACCESS_TOKEN_KEY, ACCESS_TOKEN_EXPIRE_TIME_KEY


def getAccessTokenFromWeChat():
    tokenParams = {'grant_type': 'client_credential', 'appid': setting.APPID,
                   'secret': setting.APPSECRET}
    try:
        r = requests.get('https://api.weixin.qq.com/cgi-bin/token', params=tokenParams)
        logging.debug(r.content)
        result = r.json()
        if 'access_token' in result:
            setValue(ACCESS_TOKEN_KEY, result['access_token'])
            # 设置过期时间
            now_time = int(time.time())
            expire_time = now_time + result['expires_in'] - 60
            logging.debug("set token and time ~~ now time:%s  expire time:%s", now_time, expire_time)
            setValue(ACCESS_TOKEN_EXPIRE_TIME_KEY, expire_time)
            return result['access_token']
        else:
            setValue(ACCESS_TOKEN_EXPIRE_TIME_KEY, 0)
            logging.error("errorCode:%s errorMsg:%s", result["errcode"], result["errmsg"])
            return None
    except Exception, e:
        logging.exception(e)
        return None


def isTokenTimeExpire():
    accessTokenExpireSec = getValue(ACCESS_TOKEN_EXPIRE_TIME_KEY)
    if accessTokenExpireSec is None or accessTokenExpireSec == 0:
        logging.debug("None or 0 %s", str(accessTokenExpireSec))
        return True
    now_time = int(time.time())
    if accessTokenExpireSec < now_time:
        logging.debug("Time Expired ~~~ now time:%s expired time:%s", now_time, str(accessTokenExpireSec))
        return True
    else:
        return False


def getAccessToken():
    if getValue(ACCESS_TOKEN_KEY) is None or isTokenTimeExpire() is True:
        return getAccessTokenFromWeChat()
    return getValue(ACCESS_TOKEN_KEY)


if __name__ == '__main__':
    now_time = int(time.time())
    expire_time = now_time + 7200 - 60
    if expire_time < now_time:
        print("yes")
    else:
        print("no")





