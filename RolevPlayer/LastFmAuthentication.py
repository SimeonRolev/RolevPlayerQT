from xml.dom import minidom
from _md5 import md5
import urllib.request
import webbrowser
import json

""" this class is meant to get last FM stuff - session key, token, etc."""

last_fm_api_key = "bf8dba2058d06673bddb97e04c6f7c3e"
secret = "d5886f965bf29503c42a849be0794b14"

# WE REQUEST A TOKEN

"""url = "http://ws.audioscrobbler.com/2.0/?method=auth.gettoken&api_key=" + last_fm_api_key

response = urllib.request.urlopen(url)
content = response.read().decode('utf-8')
file = open("token.xml", 'w')
file.write(content)
file.close() """

xmldoc = minidom.parse("token.xml")
lfm = xmldoc.getElementsByTagName("lfm")[0]
token = lfm.getElementsByTagName("token")[0].firstChild.data
print("Token: {}".format(token))

# HERE WE GIVE PERMISSION TO OUR APP TO USE OUR LAST.FM ACCOUNT

#webbrowser.open("http://www.last.fm/api/auth/?api_key=" + last_fm_api_key + "&token=" + token)

# HERE WE GENERATE THE SIGNATURE KEY
api_signature = md5(("api_key" + last_fm_api_key + "methodauth.getSessiontoken" + token + secret).encode('utf-8'))
print("API Signature: {}".format(api_signature.hexdigest()))

# THIS REQUEST DOEST WORK THROUGH PYTHON. I ENTERED IT IN THE BROWSER, REPLACING
# THE ARGUMENTS AND I MANAGED TO GET THE SESSION KEY

"""class AppURLopener(urllib.request.FancyURLopener):
    version = "App/1.7"


opener = AppURLopener()
response = opener.open(
    "http://ws.audioscrobbler.com/2.0/?method=auth.getSession" +
    "&api_key=" + last_fm_api_key +
    "&token=" + token +
    "&api_sig=" + api_signature.hexdigest()).read().decode('utf-8')

json_obj = json.loads(response)
print(json_obj)
"""