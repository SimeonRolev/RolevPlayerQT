import unittest
import requests
import json

from RolevPlayer import Song, LibraryLoader, AlbumArtwork


class TestLibraryLoader(unittest.TestCase):

    def setUp(self):
        self.library = {}
        self.song1 = LibraryLoader.create_song("Test_music/02 - Tragic Magic.mp3")
        self.song2 = LibraryLoader.create_song("Test_music/03 - The Drug In Me is You.mp3")

    def test_create_song(self):
        self.assertEqual(self.song2.artist, "Falling in Reverse")
        self.assertEqual(self.song2.album, "The Drug in Me Is You")
        self.assertEqual(self.song2.name, "The Drug In Me is You")
        self.assertEqual(self.song2.path, "Test_music/03 - The Drug In Me is You.mp3")

    def test_add_song_to_dict(self):
        LibraryLoader.add_song_to_dict(self.song1, self.library)
        self.assertIn("Falling in Reverse", self.library)
        self.assertIn("The Drug in Me Is You", self.library['Falling in Reverse'])
        self.assertIn(('Tragic Magic', 'Test_music/02 - Tragic Magic.mp3'), self.library['Falling in Reverse']['The Drug in Me Is You'])
        self.assertNotIn(('The Drug In Me is You', 'Test_music/03 - The Drug In Me is You.mp3'), self.library['Falling in Reverse']['The Drug in Me Is You'])

    def test_load_music_from_dir(self):
        test = LibraryLoader.load_music_from_dir(".")

        self.assertIn("Falling in Reverse", test)
        self.assertIn("The Drug in Me Is You", test['Falling in Reverse'])
        self.assertEqual(1, len(test))
        self.assertEqual(2, len(test['Falling in Reverse']['The Drug in Me Is You']))


class TestAlbumArtworkAndInfo(unittest.TestCase):

    def test_access_to_lastfm(self):
        url = "http://ws.audioscrobbler.com/2.0/?method=artist.search" +\
              "&artist=cher&api_key=bf8dba2058d06673bddb97e04c6f7c3e&format=json"

        req = requests.post(url).text
        json_obj = json.loads(req)

        self.assertNotIn('error', json_obj)


if __name__ == '__main__':
    unittest.main()
