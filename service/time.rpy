import time
import os
from ujson import encode as json_encode
from twisted.web.resource import Resource

class ClockPage(Resource):
    isLeaf = True
    def render_POST(self, request):
        output = []
        timezones = ["Asia/Shanghai", "America/New_York", "America/Chicago"]
        for tz in timezones:
            os.environ["TZ"] = tz
            time.tzset()
            output.append(time.strftime("%X %Y-%m-%d %Z (" + tz + ")"))
        data = dict(text=[" || ".join(output)])
        return json_encode(data)

resource = ClockPage()


# vim: ts=4 sw=4 ai et
