#!/usr/bin/env python
# coding=utf-8

"""
FOR WECHAT 
"""
###############################################################################
"""search
"""
WECHAT_BASE_URL = (u"http://weixin.sogou.com/weixin?type=1&query={0}"
              u"&ie=utf8&_sug_=y&_sug_type_=&w=01019900")


"""xpath
"""
WECHAT_BOX_XPATH = u'//li[starts-with(@id, "sogou_vr_11002301_box_")]'
MP_PAGE_XPATH    = u'//div[@class="p-fy"]//*[starts-with(@id, "sogou_page_")]'

mp_name_xpath    = u'//label[@name="em_weixinhao"]'
mp_openid_xpath  = u'//li[starts-with(@id, "sogou_vr_11002301_box_")]'
mp_logourl_xpath = u'//img'
mp_title_xpath   = u'//div[@class="txt-box"]//a'
mp_desc_xpath    = u'//dl[1]//dd'


"""spide 
"""
WECHAT_URLOPEN_OPTIONS = {'proxy':'mayi', 'group':3}
# wechat_urlopen_options = {'proxy':'dial'}


"""
FOR NEWS
"""
###############################################################################
"""search
"""
NEWS_BASE_URL = ('http://weixin.sogou.com/weixin?type=2&ie=utf8&query=%(mp_name)s&'
                'tsn=%(timeid)s&ft=%(fromtime)s&et=%(endtime)s&interation='
                '&wxid=%(openid)s&usip=%(mp_name)s')

REFER_BASE_URL= (u'http://weixin.sogou.com/weixin?type=2&ie=utf8&query=%(mp_name)s&'
                'tsn=%(timeid)s&ft=&et=&interation=&wxid=&usip=')

"""xpath
"""
NEWS_BOX_XPATH = u'//li[starts-with(@id, "sogou_vr_11002601_box_")]'
PAGE_XPATH  = u'//div[@class="p-fy"]//*[starts-with(@id, "sogou_page_")]'

title_xpath = u'//h3' 
intro_xpath = u'//p[@class="txt-info"]'
image_xpath = u'//img[1]'
news_xpath  = u'//a[starts-with(@id, "sogou_vr_11002601_title")]'
time_xpath  = u'//div[@class="s-p"]'
source_xpath= u'//a[@class="account"]'


"""spide 
"""
NEWS_URLOPEN_OPTIONS = {'proxy':'mayi', 'group':3}


"""content check
"""
import re
SEARCH_ERROR_MODEL = re.compile(ur'用户您好，您的访问过于频繁，为确认本次访问为正常用户行为，需要您协助验证。')

"""time compile
"""
NEWS_TIME_MODEL    = re.compile(ur"timeConvert\('(\d.+?)'\)") 
