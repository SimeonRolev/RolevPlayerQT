class Song:
    def __init__(self, name, artist, album, path):
        self.name = name
        self.artist = artist
        self.album = album
        self.path = path

    def __str__(self):
        return "SONG {}".format(self.path)

    def __getitem__(self, index):
        return (self.name, self.artist, self.album, self.path)[index]
