#!/usr/bin/env python
# coding=utf-8
from urllib import quote
from lxml import etree, html
from collections import defaultdict, namedtuple

from utils import webpage_open
from elements import WeChatElements
from configure import (MP_PAGE_XPATH)
from configure import (WECHAT_BASE_URL, WECHAT_BOX_XPATH)

class WechatParse(object):
    __WECHAT_BASE_URL  = WECHAT_BASE_URL 
    __WECHAT_BOX_XPATH = WECHAT_BOX_XPATH

    def __init__(self):
        self.mp_name = WeChatElements.mp_name_location 
        self.openid  = WeChatElements.openid_location
        self.mp_title= WeChatElements.mp_title_location
        self.mp_logo = WeChatElements.mp_logo_location
        self.mp_desc = WeChatElements.mp_desc_location

    def detect_url(self, queryword):
        return self.__WECHAT_BASE_URL.format(quote(queryword.encode('utf8')))

    def pageurls(self, content):
        _tree = etree.HTML(content)
        for _ele in _tree.xpath(MP_PAGE_XPATH):
            yield _ele.attrib.get('href', '')

    def parse(self, content):
        """
        :param content:
        """
        _tree = etree.HTML(content)
        for _ele in _tree.xpath(self.__WECHAT_BOX_XPATH):
            _subcontent = html.tostring(_ele, method='html')
            _item_box   = defaultdict(dict)
            for key, setting in self.__dict__.items():
                _subtree = etree.HTML(_subcontent)
                for _e in _subtree.xpath(setting.get('xpath')):
                    if setting.get('tag').lower() == 'text':
                        text = html.tostring(_e, method='text', encoding='utf8')
                        _item_box[key] = text.strip()
                    else:
                        tag = setting.get('tag').lower()
                        tag_info = _e.attrib.get(tag, '') 
                        _item_box[key] = tag_info
            yield _item_box

    def iter_parse(self, content):
        for _resp in self.parse(content):
            Resp = namedtuple('Resp', [key for key in _resp])
            resp = Resp(**_resp)
            yield resp


    @staticmethod
    def readhtml(url, **kwargs):
        """
        :param url:
        :return:
        """
        retry = kwargs.get('retry', 5)
        for i in xrange(retry):
            try:
                resp = webpage_open(url, **kwargs)
                return resp.content
            except Exception as e:
                continue
        raise Exception(e)
