#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.web.server import NOT_DONE_YET
from twisted.web.resource import Resource
from twisted.internet import defer, threads
from ujson import encode as json_encode, decode as json_decode
from twisted.web.client import getPage
from twisted.python.failure import Failure

import urllib
import re

API = "http://tinyurl.com/api-create.php?"
URL_RE = re.compile("https?://[a-zA-Z0-9.@&=%+/:?-]+")

class Page(Resource):
    isLeaf = True

    @defer.inlineCallbacks
    def tinyurl(self, text, request):
        start, retval = 0, ""

        for match in URL_RE.finditer(text):
            retval += text[start:match.start()]
            param = urllib.urlencode(dict(url=match.group(0)))
            tiny = yield getPage(API + param)
            retval += tiny
            start = match.end()

    	retval += text[start:]

        request.write(retval)

    def done(self, retval, request):
        if isinstance(retval, Failure):
            retval.printTraceback()
        request.finish()

    def render_POST(self, request):
        request.content.seek(0, 0)
        content = request.content.read()

        d = self.tinyurl(content, request)
        d.addBoth(self.done, request)
        return NOT_DONE_YET


resource = Page()

# vim: ts=4 sw=4 ai et
