#!/usr/bin/env python
# coding=utf-8
"""
pywechat.detector
---------------------------------------------
  To detect wechat from sogou engine through
input wechat english name.

"""
from utils import check_chinese
from mpparser import WechatParse
from configure import (WECHAT_URLOPEN_OPTIONS)
from exception import NoResultFound, GetContentError


class WeChatDetector(object):

    def __init__(self, **settings):
        """
        :param wechatparser:(optional)
        """
        self.wechatparser = settings.get('wechatparser', WechatParse())

    def set_wechat_parser(self, wechat_parser):
        self.wechatparser = wechat_parser

    def detect(self, keywords, **kwargs):
        """
        :param keywords:
        """
        if not isinstance(keywords, basestring):
            Error = ('input keywords must sting type, [%r] if invalid.' %
                    (type(keywords)))
            raise KeyError(Error)
        if check_chinese(keywords):
            Error = (u'detector should input wechat mp_name(not chinese '
                     u'character[%s])' % keywords)
            raise KeyError(Error)
        detect_url = self.wechatparser.detect_url(keywords)
        options = kwargs.get('options',  WECHAT_URLOPEN_OPTIONS) 
        timeout = kwargs.get('timeout', 30)
        retry   = kwargs.get('retry', 5)

        try:
            content = self.wechatparser.readhtml(detect_url, options=options, 
                                                             timeout=timeout, 
                                                             retry  =retry)
            for ret in self.wechatparser.iter_parse(content):
                if ret.mp_name == keywords:
                    return ret
            raise NoResultFound('no result find for mp_name:[%s]' %keywords)
        except GetContentError:
            raise GetContentError('get content failed for [%s]' %keywords)



