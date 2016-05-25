import os
from mutagen.id3 import ID3
from Song import Song


def create_song(path):
    audio = ID3(path)
    song_file_name = path.split('\\')[-1].split('.')[0]
    songname = str(audio.get('TIT2', song_file_name))
    artist = str(audio.get('TPE1', 'Unknown Artist'))
    album = str(audio.get('TALB', 'Unknown Album'))
    song = Song(songname, artist, album, path)
    return song


def add_song_to_dict(song, sort_dict):
    if song.artist in sort_dict:
        if song.album in sort_dict[song.artist]:
            sort_dict[song.artist][song.album].append(song.name)
        else:
            sort_dict[song.artist][song.album] = [song.name]
    else:
        sort_dict[song.artist] = {song.album: [song.name]}


def load_music_from_dir(root_dir):
    library = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if os.path.splitext(filename)[1] == ".mp3":
                path = os.path.join(dirpath, filename)
                song = create_song(path)
                add_song_to_dict(song, library)
    return library


if __name__ == '__main__':
    for key, value in load_music_from_dir('.').items():
        print(key, value)
