import json
import urllib.request


class AppURLopener(urllib.request.FancyURLopener):
    version = "App/1.7"


def search_song_lyrics(artist, song_name):
    try:
        opener = AppURLopener()
        response = opener.open(
            'http://api.lyricsnmusic.com/songs?' +
            'api_key=d232f509b3d2f6a11fab7fa07d38ba&artist=' +
            artist + '&track=' + song_name)\
            .read().\
            decode('utf-8')
        json_obj = json.loads(response)

        if json_obj:
            found_artist = json_obj[0]['artist']['name']
            found_song = json_obj[0]['title']
            snippet_lyrics = json_obj[0]['snippet']
            full_lyrics_link = json_obj[0]['url']

            song_found = "{} {}\n".format(found_artist, found_song)
            return "{}\n{}\n\nSee full lyrics?".format(
                song_found, snippet_lyrics), full_lyrics_link
        else:
            return "Lyrics not found!", ""
    except:
        return "Lyrics not found!", ""
