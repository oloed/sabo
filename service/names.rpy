#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twisted.web.server import NOT_DONE_YET
from twisted.web.resource import Resource
from twisted.internet import defer, threads
from ujson import encode as json_encode, decode as json_decode

class Page(Resource):
    isLeaf = True

    @defer.inlineCallbacks
    def search(self, request):
        from twisted.web.client import getPage
        import urllib
        request.content.seek(0, 0)
        content = request.content.read()
        input = json_decode(content)
        print input
        users = input["context"]["users"]["&bitlbee"].keys()
        users = ",".join(filter(lambda x: x!= 'root', users))
        reply = dict(text=["online: %s" % (users)])
        request.write(json_encode(reply))
        request.finish()

    def render_POST(self, request):
        self.search(request)
        return NOT_DONE_YET

resource = Page()

# vim: ts=4 sw=4 ai et
