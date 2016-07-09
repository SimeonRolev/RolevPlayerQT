import json
import urllib.request
from xml.dom import minidom
import webbrowser
from _md5 import md5

""" The purpose of this method is to use your API_KEY and SECRET
to create a file with your user information, which will be later
used for some of the player's features. All the info gets
saved into a file named "user_info.txt" in the current directory """


def create_initial_info_file(api_key, secret):
    user_info = {}
    user_info['api_key'] = api_key
    user_info['secret'] = secret

    # getting a token and writing it into the file

    url = "http://ws.audioscrobbler.com/2.0/?method=' + \
          'auth.gettoken&api_key=" + api_key

    response = urllib.request.urlopen(url)
    content = response.read().decode('utf-8')
    file = open("token.xml", 'w')
    file.write(content)
    file.close()

    xmldoc = minidom.parse("token.xml")
    lfm = xmldoc.getElementsByTagName("lfm")[0]
    token = lfm.getElementsByTagName("token")[0].firstChild.data
    print("Token: {}".format(token))

    user_info['token'] = token
    user_info['sk'] = None

    user_info_dump = json.dumps(user_info)
    with open("./user_info.txt", "w") as file:
        file.write(user_info_dump)

    webbrowser.open("http://www.last.fm/api/auth/?api_key=" +
                    user_info['api_key'] + "&token=" + user_info['token'])

#create_initial_info_file("4f095aef8f8ad2b76843515d1ae4050b", "9f43fd9ee06318fe92ba00072e030a4b")
