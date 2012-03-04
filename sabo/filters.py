from twisted.internet import defer
from twisted.web.client import getPage

import urllib
import re

URL_RE = re.compile("https?://[a-zA-Z0-9.@&=%+/:?-]+")

@defer.inlineCallbacks
def tinyurl(text):
    API = "http://tinyurl.com/api-create.php?"
    start = 0
    retval = ""
    for match in URL_RE.finditer(text):
      retval += text[start:match.start()]
      param = urllib.urlencode(dict(url=match.group(0)))
      tiny = yield getPage(API + param)
      retval += tiny
      start = match.end()
    if len(retval) == 0:
	retval = text
    defer.returnValue(retval)
"""
@defer.inlineCallbacks
def tinyurl(text):
    try:
        defer.returnValue(_tinyurl(text))
    except Exception as e:
        print "X" * 80, e
"""
# vims: ts=4 sw=4 ai et
