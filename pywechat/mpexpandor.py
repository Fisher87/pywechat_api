#!/usr/bin/env python
# coding=utf-8

import warnings
from urlparse import urljoin

from mpparser import WechatParse
from configure import (WECHAT_URLOPEN_OPTIONS)

class WechatExpandor(object):
    def __init__(self, **settings):
        self.wechatparser = settings.get('wechatparser', WechatParse())

    def set_wechat_parser(self, wechat_parser):
        self.wechatparser = wechat_parser

    def expand(self, keywords, **kwargs):
        baseurl = self.wechatparser.detect_url(keywords)
        options = kwargs.get('options',  WECHAT_URLOPEN_OPTIONS) 
        timeout = kwargs.get('timeout', 30)
        retry   = kwargs.get('retry', 5)
        content = self.wechatparser.readhtml(baseurl, options=options,
                                                      timeout=timeout,
                                                      retry  = retry)
        rawurls = [url for url in self.wechatparser.pageurls(content)]
        pageurls= [urljoin(baseurl, _) for _ in rawurls]
        for resp in self.wechatparser.iter_parse(content):
            yield resp

        for i, pageurl in enumerate(pageurls):
            try:
                pagecontent = self.wechatparser.readhtml(pageurl)
                for resp in self.wechatparser.iter_parse(pagecontent):
                    yield resp
            except Exception as e:
                Warn = ('do not expand completly for [%d]/[%d][%s]:\n%s' % 
                                                   (i+1, len(pageurls)+1, url, e))
                warnings.warn(Warn)
                continue

