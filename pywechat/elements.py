#!/usr/bin/env python
# coding=utf-8
"""
pywechat.elements
---------------------------------------
  To display element that can be parsed 
in this project.
"""

class ElementLocation(dict):
    pass

##########################################################################
""" for mp module. """
from configure import (mp_name_xpath, mp_openid_xpath, mp_title_xpath, 
                       mp_logourl_xpath, mp_desc_xpath)

class WeChatElements(object):
    mp_name_location = ElementLocation(xpath = mp_name_xpath,    tag = 'text')
    openid_location  = ElementLocation(xpath = mp_openid_xpath,  tag = 'd')
    mp_title_location= ElementLocation(xpath = mp_title_xpath,   tag = 'text')
    mp_logo_location = ElementLocation(xpath = mp_logourl_xpath, tag = 'src')
    mp_desc_location = ElementLocation(xpath = mp_desc_xpath,    tag = 'text')


##########################################################################
""" for news module. """
from configure import (title_xpath, intro_xpath, news_xpath, 
                       time_xpath, image_xpath, source_xpath)

class NewsElements(object):
    title_location  = ElementLocation(xpath = title_xpath, tag = 'text')
    intro_location  = ElementLocation(xpath = intro_xpath, tag = 'text')
    image_location  = ElementLocation(xpath = image_xpath, tag = 'src')
    time_location   = ElementLocation(xpath = time_xpath,  tag = 'text')
    newsurl_location= ElementLocation(xpath = news_xpath,  tag = 'href')
    source_location = ElementLocation(xpath = source_xpath,tag = 'text')


