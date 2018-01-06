#!/usr/bin/env python
# coding=utf-8
from newshandler import NewsHandler
region_name = u'石景山'
h = NewsHandler()
print 'start'
for i in xrange(5):
    try:
        for n in h.get_news(region_name, '', timeid=1, 
                options={'proxy':'dial'}):
            print n.title
    except Exception:
        continue
print 'end'

