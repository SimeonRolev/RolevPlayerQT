# RolevPlayerQT
## Synopsis

This is a simple player, supporting .mp3 files. It is integrated with last.fm and supports the following features:
scrobbling, automatic album covers downloading, automatic lyrics search (uses lyricsnmusic.com), automatic artist/album info links.

## Usage

Since the project uses the last fm api, you need to add your own api key and secret.
When you have your api_key and secret from last.fm you have to go through the following steps:

1. In the create_empty_info_file.py there is only one method called create_initial_info_file(api_key, secret).
Execute this method with your apy_key and secret. This method will generate a file called user_info.txt
It will save your user information in this file as a dictionary for later usage of your personal info.
It will also generate a token from last.fm and will open your browser for confirmation that you
allow "Rolev Player" to access your last.fm account.

2. After you have provided access to your account, you have to run get_session_key.py.
This will generate a session key for you so you can access the last.fm database and will
save this session key into your user_info.txt file.

3. Execute the Main.py method from the RolevPlayer module.


## API Reference

For more info about the methods and requesting api_key and secret, visit the last.fm API.
http://www.last.fm/api/intro

##License

It's free, yaay!
