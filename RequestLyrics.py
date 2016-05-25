"""from urllib.request import Request, urlopen

lyricsnmusic_key = 'd232f509b3d2f6a11fab7fa07d38ba'
request = Request(
    "http://api.lyricsnmusic.com/songs?api_key=d232f509b3d2f6a11fab7fa07d38ba&artist=coldplay&track=clocks")
result = urlopen(request).read() """

import urllib.request
import json

lyricsnmusic_key = 'd232f509b3d2f6a11fab7fa07d38ba'
request = urllib.request.urlopen(
    "http://lyricwiki.org/server.php?wsdl").read().decode('UTF-8')
print(json.loads(request))