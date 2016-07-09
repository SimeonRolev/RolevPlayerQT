import json
import requests
import urllib.request
import os.path
import RolevPlayer as r

last_fm_api_key = r.API_KEY


def album_cover(album_path, artist, album):

    try:
        image_path = "{}/{}".format(album_path, album + " cover.png")
        return image_path
    except:
        url = "http://ws.audioscrobbler.com//2.0/?method=album.getinfo" + \
              "&api_key=" + last_fm_api_key + \
              "&artist=" + artist + \
              "&album=" + album + \
              "&format=json"

        req = requests.post(url).text
        json_obj = json.loads(req)

        if 'error' in json_obj:
            print("An error occurred")
        else:
            image_path = "{}/{}".format(album_path, album + " cover.png")
            if not os.path.isfile(image_path):

                # list of the found images in size ascending order
                images = json_obj['album']['image']
                index = 3 if len(images) >= 3 else len(images)
                image_name = album + " cover.png"
                urllib.request.urlretrieve(images[index]['#text'], image_path)

            artist_info_url = json_obj['album']['tracks']['track'][0]['artist']['url']
            album_info_url = json_obj['album']['url']

            return image_path


def album_artist_info(artist, album):

    url = "http://ws.audioscrobbler.com//2.0/?method=album.getinfo" + \
          "&api_key=" + last_fm_api_key + \
          "&artist=" + artist + \
          "&album=" + album + \
          "&format=json"

    req = requests.post(url).text
    json_obj = json.loads(req)

    if 'error' in json_obj:
        print("An error occurred")
    else:
        artist_info_url = json_obj['album']['tracks']['track'][0]['artist']['url']
        album_info_url = json_obj['album']['url']

        return artist_info_url, album_info_url
