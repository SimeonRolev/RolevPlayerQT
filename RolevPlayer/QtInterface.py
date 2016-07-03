from PyQt5 import QtWidgets
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from RolevPlayer import LibraryLoader
from RolevPlayer import RequestLyrics
from RolevPlayer import AlbumArtwork
from RolevPlayer import Scrobbler
import webbrowser


class Window(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.setGeometry(50, 50, 300, 400)
        self.setWindowTitle("Rolev Player")

# LIBRARY ROOT DIR FOLDER
        self.search_label = QtWidgets.QLabel("Select the root directory of a music folder:", self)
        self.search_label.setGeometry(10, 5, 205, 10)

        self.btn_root_folder = QtWidgets.QPushButton("Browse", self)
        self.btn_root_folder.setGeometry(215, 20, 75, 25)

        # the text field of the currently selected root directory
        self.dir_text_field = QtWidgets.QLineEdit(self)
        self.dir_text_field.setGeometry(10, 20, 200, 25)

        self.btn_root_folder.clicked.connect(self.on_btn_root_folder)

# CURRENT MEDIA LABEL
        self.current_media_label = QtWidgets.QLabel("Now Playing: ", self)
        self.current_media_label.setGeometry(10, 260, 250, 15)

# CURRENT ALBUM COVER
        self.current_album_cover = QtWidgets.QLabel("Image", self)
        self.current_album_cover.setGeometry(10, 180, 75, 75)
        self.current_album_cover.setScaledContents(True)

# ARTIST DROP BOX
        self.artist_select_label = QtWidgets.QLabel("Artist", self)
        self.artist_select_label.setGeometry(10, 50, 250, 25)

        self.artist_select = QtWidgets.QComboBox(self)
        self.artist_select.setGeometry(10, 70, 250, 25)
        self.artist_select.activated[str].connect(self.on_artist_selection)
        
# ALBUMS DROP BOX
        self.album_select_label = QtWidgets.QLabel("Albums", self)
        self.album_select_label.setGeometry(10, 90, 250, 25)

        self.album_select = QtWidgets.QComboBox(self)
        self.album_select.setGeometry(10, 110, 250, 25)
        self.album_select.activated[str].connect(self.on_album_selection)

# SONGS DROP BOX
        self.song_select_label = QtWidgets.QLabel("Current Playlist", self)
        self.song_select_label.setGeometry(10, 130, 250, 25)

        self.song_select = QtWidgets.QComboBox(self)
        self.song_select.setGeometry(10, 150, 250, 25)
        self.song_select.activated[str].connect(self.on_song_selection)

# PLAYLIST
        self.playlist = QMediaPlaylist()
        self.playlist.currentIndexChanged.connect(self.meta_data_changed)

# MEDIA PLAYER
        self.player = QMediaPlayer()
        self.player.setPlaylist(self.playlist)
        self.player.playlist().setPlaybackMode(QMediaPlaylist.Loop)
        self.player.setVolume(50)

        self.player.durationChanged.connect(self.on_dur_change)
        self.player.positionChanged.connect(self.on_pos_change)

# VOLUME SLIDER
        self.slider_volume_label = QtWidgets.QLabel("Volume", self)
        self.slider_volume_label.setGeometry(10, 345, 50, 25)

        self.slider_volume = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.slider_volume.setGeometry(60, 350, 130, 20)
        self.slider_volume.setRange(0, 100)
        self.slider_volume.setValue(50)
        self.slider_volume.valueChanged.connect(self.volume_change)

# PROGRESS SLIDER
        self.slider_progress_label = QtWidgets.QLabel("Progress", self)
        self.slider_progress_label.setGeometry(10, 315, 50, 25)

        self.slider_progress = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.slider_progress.setGeometry(60, 320, 130, 20)
        self.slider_progress.sliderMoved.connect(self.progress_change)

# LYRICS SEARCH
        self.btn_lyrics = QtWidgets.QPushButton("Search\n Lyrics", self)
        self.btn_lyrics.setGeometry(220,310,70,80)
        self.btn_lyrics.clicked.connect(self.on_lyrics)

# ALBUM INFO SEARCH
        self.btn_album_info = QtWidgets.QPushButton("Search\nAlbum\nInfo", self)
        self.btn_album_info.setGeometry(105, 180, 75, 75)
        self.btn_album_info.clicked.connect(self.on_album_info)

# ARTIST INFO SEARCH
        self.btn_artist_info = QtWidgets.QPushButton("Search\nArtist\nInfo", self)
        self.btn_artist_info.setGeometry(200, 180, 75, 75)
        self.btn_artist_info.clicked.connect(self.on_artist_info)

# PREV SONG BUTTON
        self.btn_prev = QtWidgets.QPushButton("Prev", self)
        self.btn_prev.setGeometry(10, 280, 75, 25)
        self.btn_prev.clicked.connect(self.on_btn_prev)

# NEXT SONG BUTTON
        self.btn_next = QtWidgets.QPushButton("Next", self)
        self.btn_next.setGeometry(200, 280, 75, 25)
        self.btn_next.clicked.connect(self.on_btn_next)

# PLAY/PAUSE BUTTON
        self.btn_play_pause = QtWidgets.QPushButton("Play", self)
        self.btn_play_pause.setGeometry(105, 280, 75, 30)
        self.btn_play_pause.clicked.connect(self.on_btn_play_pause)

        self.show()

    def on_btn_root_folder(self):
        self.root_dir = QtWidgets.QFileDialog().getExistingDirectory()
        self.dir_text_field.setText(self.root_dir)
        self.library = LibraryLoader.load_music_from_dir(self.dir_text_field.text())

        self.artist_select.clear()
        self.album_select.clear()
        self.song_select.clear()
        self.playlist.clear()

        self.btn_play_pause.setText("Play")
        self.artist_select.addItem("All Artists")
        for artist in self.library:
            self.artist_select.addItem(artist)
            for album in self.library[artist]:
                self.album_select.addItem(album)
        self.load_all_songs()

    def on_artist_selection(self):
        current_artist = self.artist_select.currentText()

        self.album_select.clear()
        self.song_select.clear()
        self.playlist.clear()

        self.btn_play_pause.setText("Play")
        self.album_select.addItem("All Albums")
        if current_artist == "All Artists":
            for artist in self.library:
                for album in self.library[artist]:
                    self.album_select.addItem(album)
            self.load_all_songs()
        else:
            for album in self.library[current_artist]:
                self.album_select.addItem(album)
            self.load_all_from_artist(current_artist)

    def load_all_songs(self):
        for artist in self.library:
            for album in self.library[artist]:
                for song in self.library[artist][album]:
                    self.song_select.addItem(song[0])
                    self.playlist.addMedia(QMediaContent(QtCore.QUrl.fromLocalFile(song[1])))
                    
    def load_all_from_artist(self, artist):
        for album in self.library[artist]:
            for song in self.library[artist][album]:
                self.song_select.addItem(song[0])
                self.playlist.addMedia(QMediaContent(QtCore.QUrl.fromLocalFile(song[1])))

    def on_album_selection(self):
        current_artist = self.artist_select.currentText()
        current_album = self.album_select.currentText()
        self.song_select.clear()
        self.playlist.clear()
        self.btn_play_pause.setText("Play")
        if current_album == "All Albums" and current_artist == "All Artists":
            self.load_all_songs()

        elif current_album == "All Albums":
            self.load_all_from_artist(current_artist)

        elif current_artist == "All Artists":
            for artist in self.library:
                for album in self.library[artist]:
                    if album == self.album_select.currentText():
                        for song in self.library[artist][album]:
                            self.song_select.addItem(song[0])
                            self.playlist.addMedia(QMediaContent(QtCore.QUrl.fromLocalFile(song[1])))
        else:
            for song in self.library[current_artist][current_album]:
                self.song_select.addItem(song[0])
                self.playlist.addMedia(QMediaContent(QtCore.QUrl.fromLocalFile(song[1])))

    def on_song_selection(self):
        index = self.song_select.currentIndex()
        self.playlist.setCurrentIndex(index)

# GETTING THE CURRENT SONG METADATA
    # Returns a SONG OBJECT and not the current song title
    # For the title of the currently playing song use get_current_title()
    def get_current_song(self):
        curr_url = self.playlist.currentMedia().canonicalUrl().toString()[8:]
        if curr_url:
            return LibraryLoader.create_song(curr_url)

    def get_current_artist(self):
        if self.get_current_song() is not None:
            return self.get_current_song().artist

    def get_current_album(self):
        if self.get_current_song() is not None:
            return self.get_current_song().album

    def get_current_path(self):
        if self.get_current_song() is not None:
            return self.get_current_song().path

    def get_current_album_path(self):
        if self.get_current_path() is not None:
            return self.get_current_path().rsplit("/", 1)[0]

    def get_current_title(self):
        if self.get_current_song() is not None:
            return self.get_current_song().name

    def on_lyrics(self):
        if self.get_current_song() is not None:
            curr_artist = self.get_current_artist()
            curr_song = self.get_current_title()

            found_lyrics = RequestLyrics.search_song_lyrics(curr_artist, curr_song)
            choice = QtWidgets.QMessageBox.question(self, "Lyrics", found_lyrics[0], QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if choice == QtWidgets.QMessageBox.Yes:
                webbrowser.open(found_lyrics[1])
        else:
            QtWidgets.QMessageBox.information(self, "Lyrics", "Sorry, no lyrics found or no media is loaded!")

    def on_album_info(self):
        album = self.get_current_album()
        artist = self.get_current_artist()
        if (album is None) or (artist is None):
            print("Please, load a song first!")
        else:
            artist_info, album_info = AlbumArtwork.album_artist_info(artist, album)
            if album_info is not None:
                webbrowser.open(album_info)

    def on_artist_info(self):
        album = self.get_current_album()
        artist = self.get_current_artist()
        if (album is None) or (artist is None):
            print("Please, load a song first!")
        else:
            artist_info, album_info = AlbumArtwork.album_artist_info(artist, album)
            if artist_info is not None:
                webbrowser.open(artist_info)

    def on_btn_play_pause(self):
        if self.player.state() in (0, 2):
            self.player.play()
            if self.player.state() == 1:
                self.btn_play_pause.setText("Pause")
        else:
            self.player.pause()
            self.btn_play_pause.setText("Play")

    def on_btn_next(self):
        self.player.playlist().next()

    def on_btn_prev(self):
        self.player.playlist().previous()

    def on_dur_change(self, length):
        self.slider_progress.setMaximum(length)

    def on_pos_change(self, position):
        self.slider_progress.setValue(position)

    def volume_change(self):
        volume = self.slider_volume.value()
        self.player.setVolume(volume)

    def progress_change(self):
        position = self.slider_progress.value()
        self.player.setPosition(position)

    def meta_data_changed(self):

        now_playing = self.get_current_title()
        self.current_media_label.setText("Now Playing: " + now_playing)

        # Updating the currently playing album cover
        curr_album_path = self.get_current_album_path()
        curr_album = self.get_current_album()
        curr_artist = self.get_current_artist()
        cover_url = AlbumArtwork.album_cover(curr_album_path, curr_artist, curr_album)

        self.current_album_cover.setPixmap(QPixmap(cover_url))
        Scrobbler.scrobble(self.get_current_artist(), self.get_current_title())
