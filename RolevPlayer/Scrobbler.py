import json
import time
from _md5 import md5

import requests

import RolevPlayer as r


def now_playing_last_fm(artist, track):

    update_now_playing_sig = md5(("api_key" + r.API_KEY +
                                "artist" + artist +
                                "method" + "track.updateNowPlaying" +
                                "sk" + r.SK +
                                "track" + track +
                                r.SECRET).encode('utf-8')).hexdigest()

    url = "http://ws.audioscrobbler.com/2.0/?method=track.updateNowPlaying" + \
          "&api_key=" + r.API_KEY + \
          "&api_sig=" + update_now_playing_sig + \
          "&artist=" + artist + \
          "&format=json" + \
          "&sk=" + r.SK + \
          "&track=" + track

    req = requests.post(url).text
    json_obj = json.loads(req)


def scrobble(artist, track):

    # this gives us a timestamp, casted to integer
    ts = time.time()
    scrobbling_sig = md5(("api_key" + r.API_KEY +
                            "artist" + artist +
                            "method" + "track.scrobble" +
                            "sk" + r.SK +
                            "timestamp" + str(ts) +
                            "track" + track +
                            r.SECRET).encode('utf-8')).hexdigest()

    req = requests.post(
        "http://ws.audioscrobbler.com/2.0/?method=track.scrobble" +
        "&api_key=" + r.API_KEY +
        "&api_sig=" + scrobbling_sig +
        "&artist=" + artist +
        "&format=json" +
        "&sk=" + r.SK +
        "&timestamp=" + str(ts) +
        "&track=" + track).text
    json_obj = json.loads(req)
