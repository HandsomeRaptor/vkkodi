

import urllib
try:
    import json
except ImportError:
    import simplejson as json

try:
   from hashlib import md5
except ImportError:
   from md5 import md5

def ApiFromURL(appId, url):
    decoded=urllib.unquote(url)
    start = decoded.find("{")
    obj = json.loads(decoded[start:])
    sid = obj["sid"]
    mid = obj["mid"]
    secret = obj["secret"]
    return VkApp(appId, sid, mid, secret)


class VkApp:
    def __init__(self, api_id, sid, mid, secret):
        #param is API call parameters
        self.param = dict()
        self.param["v"] = "3.0"
        self.param["format"] = "JSON"
        self.param["api_id"] = api_id
        self.param["sid"] = sid
        self.mid = str(mid)
        self.secret = str(secret)

    def call(self, api, **vars):
        v = {"method" : api}
        v.update(self.param)
        v.update(vars)

        keys= sorted(v.keys())

        toCheck = "".join(["%s=%s" % (str(key), str(v[key])) for key in keys if key!="sid"])

        toCheck = self.mid + toCheck + self.secret

        v["sig"]=md5(toCheck).hexdigest()

        request = "&".join(["%s=%s" % (str(key), urllib.quote(str(v[key]))) for key in v.keys()])
        request_url = "http://vkontakte.ru/api.php?"+request

        reply = urllib.urlopen(request_url)
        #replystr = reply.read()
        #resp = json.loads(replystr)
        resp = json.load(reply)
        if "error" in resp:
            raise Exception("Error, error", resp)
        else:
            return resp["response"]


