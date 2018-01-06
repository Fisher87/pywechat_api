#!/usr/bin/env python
# coding=utf-8
import warnings
from urllib import quote
from datetime import datetime
from lxml import etree, html
from urlparse import urljoin
from collections import defaultdict, namedtuple

from utils import webpage_open
from elements import NewsElements
from exception import GetContentError
from configure import PAGE_XPATH
from configure import NEWS_BOX_XPATH
from configure import NEWS_TIME_MODEL
from configure import (NEWS_URLOPEN_OPTIONS)
from configure import (NEWS_BASE_URL, REFER_BASE_URL)

class NewsParser(object):
    __NEWS_BOX_XPATH = NEWS_BOX_XPATH

    def __init__(self, **kwargs):
        self.title  = NewsElements.title_location
        self.intro  = NewsElements.intro_location
        self.image  = NewsElements.image_location
        self.time   = NewsElements.time_location
        self.newsurl= NewsElements.newsurl_location
        self.source = NewsElements.source_location

    def _parse(self, content):
        """
        :param 
        """
        _tree = etree.HTML(content)
        for _ele in _tree.xpath(self.__NEWS_BOX_XPATH):
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

    def _pageurls(self, content, page_xpath):
        _tree = etree.HTML(content)
        for _ele in _tree.xpath(page_xpath):
            yield _ele.attrib.get('href', '')

class NewsHandler(object):
    __PAGE_XPATH     = PAGE_XPATH
    __NEWS_BASE_URL  = NEWS_BASE_URL
    __REFER_BASE_URL = REFER_BASE_URL

    def __init__(self, **settings):
        self.newsparser = settings.get('news_parser', NewsParser()) 
        self.retry   = settings.get('retry', 5)
        self.timeout = settings.get('timeout', 30)
        self.referer = settings.get('referer', True)

    def readhtml(self, url, **kwargs):
        for i in xrange(self.retry):
            try:
                resp = webpage_open(url, **kwargs)
                return resp.content
            except GetContentError as e:
                continue
        Error = 'get content failed [%s] for \n\r%s' % (url, e)
        raise GetContentError(Error)

    def _init_query(self, mp_name, openid, timeid, **kwargs):
        fromtime = kwargs.get('starttime', '')
        endtime  = kwargs.get('endtime', '')
        if timeid == 5:
            if not all(k in kwargs for k in ['starttime', 'endtime']):
                Warn=('should to configure `fromtime` and `endtime` for timeid=5.'
                        'if not configure will set default.')
                warnings.warn(Warn)
            _g = lambda x:datetime.strftime(x, '%Y-%m-%d')
            fromtime = kwargs.get('starttime', _g(datetime.now()))
            endtime  = kwargs.get('endtime', _g(datetime.now()))
        urlsettings = {'mp_name':mp_name, 'openid':openid, 
                       'timeid' :timeid,  'fromtime':fromtime, 
                       'endtime':endtime}
        refsettings = {'mp_name':mp_name, 'timeid':timeid}
        queryurl = self.__NEWS_BASE_URL % (urlsettings)
        queryrefer = self.__REFER_BASE_URL % (refsettings)
        Query = namedtuple('Query', ['url', 'referer'])
        return Query(queryurl, queryrefer)

    def set_news_parser(self, news_parser):
        self.newsparser = news_parser

    def get_pageurls(self, mp_name, mp_open_id, timeid=1, **kwargs):
        options = kwargs.get('options', NEWS_URLOPEN_OPTIONS)
        query = self._init_query(mp_name, mp_open_id, timeid, **kwargs)
        if self.referer:
            headers = {'Referer':query.referer}
            options.update(({'headers':headers}))
        content = self.readhtml(query.url, options=options)
        rawpages= [url for url in self.newsparser._pageurls(content, self.__PAGE_XPATH)]
        pageurls= [urljoin(query.url, _) for _ in rawpages] 
        pageurls.insert(0, query.url)
        return pageurls

    def iter_parse(self, content):
        for _resp in self.newsparser._parse(content):
            if _resp.has_key('time'):
                f_timestamp = NEWS_TIME_MODEL.search(_resp['time'])
                if f_timestamp: 
                    _resp['time'] = int(f_timestamp.group(1))
                Resp = namedtuple('Resp', [key for key in _resp])
                resp = Resp(**_resp)

            yield resp

    def get_news(self, mp_name, mp_open_id, timeid=1, **kwargs):
        options = kwargs.get('options', NEWS_URLOPEN_OPTIONS)
        if isinstance(mp_name, unicode):
            mp_name = mp_name.encode('utf8')
        mp_name = quote(mp_name)
        query = self._init_query(mp_name, mp_open_id, timeid, **kwargs)
        if self.referer:
            headers = {'Referer':query.referer}
            options.update(({'headers':headers}))
        content = self.readhtml(query.url, options=options)
        for resp in self.iter_parse(content):
            yield resp
        rawpages= [url for url in self.newsparser._pageurls(content, self.__PAGE_XPATH)]
        pageurls= [urljoin(query.url, _) for _ in rawpages] 
        for i, pageurl in enumerate(pageurls):
                try:
                    pagecontent= self.readhtml(pageurl, options=options)
                except Exception as e:
                    Warn = ('do not parse completly for [%d]/[%d] [%s]: \n\r%s' % 
                            (i+1, len(pageurls)+1, pageurl, e))
                    warnings.warn(Warn)
                    continue
                for resp in self.iter_parse(pagecontent):
                    yield resp

