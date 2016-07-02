import requests
import json
import time

api_key = "bf8dba2058d06673bddb97e04c6f7c3e"
sk = "7da8efaf63e3f9d15a01047763eee758"
api_sig = "fe3f02787652e13f5e4352b9c861f028"
# http://ws.audioscrobbler.com/2.0/?method=


def now_playing_last_fm(artist, track):

    url = "http://ws.audioscrobbler.com/2.0/?method=track.updateNowPlaying" + \
          "&api_key=" + api_key + \
          "&api_sig=" + api_sig + \
          "&artist=Blessthefall" + \
          "&format=json" + \
          "&sk=" + sk + \
          "&track=Higinia"

    req = requests.post(url).text
    json_obj = json.loads(req)
    print(json_obj)


def scrobble(artist, track):
    ts = time.time()
    req = requests.post(
        "http://ws.audioscrobbler.com/2.0/?method=track.scrobble" +
        "&api_key=" + api_key +
        "&api_sig=" + api_sig +
        "&timestamp=" + str(ts) +
        "&artist=" + artist +
        "&format=json" +
        "&sk=" + sk +
        "&track=" + track).text
    json_obj = json.loads(req)
    print(json_obj)


now_playing_last_fm("Blessthefall", "Higinia")
