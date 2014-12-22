# -*- coding: utf-8 -*-
__author__ = 'alvinli'

import sae.kvdb
import logging

ACCESS_TOKEN_KEY = "access_tk"
ACCESS_TOKEN_EXPIRE_TIME_KEY = "access_tk_expire"

kv = sae.kvdb.KVClient()


def setValue(key, value):
    try:
        kv.set(key, value)
    except sae.kvdb.RouterError, e:
        logging.exception(e)
    except sae.kvdb.StatusError, e:
        logging.exception(e)
    except sae.kvdb.Error, e:
        logging.exception(e)


def getValue(key):
    try:
        return kv.get(key)
    except sae.kvdb.RouterError, e:
        logging.exception(e)
        return None
    except sae.kvdb.StatusError, e:
        logging.exception(e)
        return None
    except sae.kvdb.Error, e:
        logging.exception(e)
        return None


def replaceValue(key, value):
    try:
        return kv.replace(key, value)
    except sae.kvdb.RouterError, e:
        logging.exception(e)
    except sae.kvdb.StatusError, e:
        logging.exception(e)
    except sae.kvdb.Error, e:
        logging.exception(e)


def deleteKey(key):
    try:
        return kv.delete(key)
    except sae.kvdb.RouterError, e:
        logging.exception(e)
    except sae.kvdb.StatusError, e:
        logging.exception(e)
    except sae.kvdb.Error, e:
        logging.exception(e)


def getInfo():
    try:
        return str(kv.get_info())
    except sae.kvdb.RouterError, e:
        logging.exception(e)
        return None
    except sae.kvdb.StatusError, e:
        logging.exception(e)
        return None
    except sae.kvdb.Error, e:
        logging.exception(e)
        return None