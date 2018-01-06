#!/usr/bin/env python
# coding=utf-8

import re
from functools import wraps
from collections import namedtuple

from urlagency.url_agency import UrlAgency
from exception import GetContentError
from configure import SEARCH_ERROR_MODEL

url_opener = UrlAgency().proxy_url_open


def content_check(func):
    @wraps(func)
    def wraper(*args, **kwargs):
        Response= namedtuple('Response', ['status', 'content'])
        resp    = func(*args, **kwargs)
        if resp['status'] != '200':
            Error = ('get content failed, status_code:[%s]' %resp['status'])
            raise GetContentError(Error)
        content = resp.get('content')
        f_search_error = SEARCH_ERROR_MODEL.search(content)
        if f_search_error:
            raise GetContentError('IP forbidden')
        return Response(resp['status'], resp['content'])

    return wraper

@content_check
def webpage_open(url, **kwargs):
    options = kwargs.get('options', {})
    timeout = kwargs.get('timeout', 30)
    resp    = url_opener(url, options=options, timeout=timeout)
    return resp

def check_chinese(string):
    if not isinstance(string, unicode):
        string = string.decode('utf8')
    f = re.findall(ur'[\u4e00-\u9fff]', string)
    return True if f else False


