pywechat
![](https://readthedocs.org/projects/pygorithm/badge/?version=latest) ![](https://img.shields.io/badge/python%20-%202.7-brightgreen.svg)
========

## `Include`
+ [mpdetector]
  根据确定公众号`mp_name`获取其相关的信息, 现版本提供能够获取的信息有(详细见[`elements`]
  - `mp_name`: 公众号英文名称
  - `openid`: 公众号搜索id
  - `mp_title`: 公众号中文名称
  - `mp_logo`: 公众号图片
  - `mp_desc`: 公众号简介

+ [mpexpandor]
  根据提供的相关词进行模糊搜索, 并返回相应信息(同`mpdetector`)；

+ [newshandler]
  获取公众号对应的新闻及相应的信息(详细见[`elements`]
  - `title`: 新闻标题
  - `intro`: 新闻简介
  - `image`: 新闻导图链接
  - `newsurl`: 新闻链接
  - `time`: 新闻发布时间(`timestamp`类型, 不是最终结果，需进一步处理)
  - `source`: 新闻发布来源

## `Basic Usage`
```python
# mpdetector
>>> from mpdetector import WeChatDetector
>>> d = WeChatDetector()
>>> ret = d.detect('rmrbwx')
>>> print ret.mp_name, ret.openid, ret.mp_title, ret.mp_logo, ret.mp_desc

# mpexpandor
>>> from mpexpandor import WechatExpandor
>>> ex = WechatExpandor()
>>> for i in e.expand('篮球'):
        print i.mp_name, i.openid, i.mp_title, i.mp_logo, i.mp_desc


# newshandler
## basic
>>> from pywechat.newshandler import NewsHandler
>>> h = NewsHandler()
>>> news = h.get_news('rmrbwx', 'oIWsFt8_jYUmdw1PQgNVhH9vOEvI', timeid=1)
>>> for n in news:
        print n.title, n.newsurl, n.image, n.time, n.intro, n.source
## user-define
>>> from pywechat.elements import ElementLocation
>>> news_parser = NewsParser()
>>> news_parser.title = ElementLocation(xpath='/a', tag='')
>>> news_parser.newsurl = ElementLocation(xpath='/b', tag='')
>>> h = NewsHandler()
>>> h.set_news_parser(news_parser)
>>> news = h.get_news('rmrbwx', 'oIWsFt8_jYUmdw1PQgNVhH9vOEvI', timeid=1)
>>> for n in news:
        print n.title
```
