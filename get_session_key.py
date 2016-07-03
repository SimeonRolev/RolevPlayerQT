from _md5 import md5
import requests
import json

with open("./user_info.txt", 'r') as user_info:
    constants = json.loads(user_info.read())

API_KEY = constants['api_key']
SECRET = constants['secret']
TOKEN = constants['token']
SK = constants['sk'] # Session key

print("\nAPI key: ", API_KEY, "\nSecret: ", SECRET, "\nToken: ", TOKEN)

api_signature = md5(("api_key" + API_KEY + "methodauth.getSessiontoken" + TOKEN + SECRET).encode('utf-8')).hexdigest()

print("API Signature: {}".format(api_signature))

url = "http://ws.audioscrobbler.com//2.0/?method=auth.getSession" + \
    "&api_key=" + API_KEY + \
    "&token=" + TOKEN + \
    "&format=json" + \
    "&api_sig=" + api_signature

req = requests.post(url).text
req = json.loads(req)

try:
    with open("./user_info.txt", 'r') as f:
        user_info = json.loads(f.read())
        user_info['sk'] = req['session']['key']
        user_info_dump = json.dumps(user_info)
        with open("./user_info.txt", "w") as file:
            file.write(user_info_dump)
        print("\nSession Key: ", req['session']['key'])
except:
    print("An error occurred in the response!")
    print("Try to run the create_empty_info_file.py again!")
    print(req)
