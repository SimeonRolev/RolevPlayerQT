import json

with open("../user_info.txt", 'r') as user_info:
    s = user_info.read()

constants = json.loads(s)

API_KEY = constants['api_key']
SECRET = constants['secret']
TOKEN = constants['token']
SK = constants['sk']  # Session key
