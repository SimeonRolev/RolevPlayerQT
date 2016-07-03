import json

user_info = open("../user_info.txt", 'r')
s = user_info.read()

constants = json.loads(s)

API_KEY = constants['api_key']
SECRET = constants['secret']
TOKEN = constants['token']
SK = constants['sk'] # Session key
