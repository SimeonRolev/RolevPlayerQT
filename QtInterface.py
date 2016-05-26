import sys
from PyQt5 import QtWidgets
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist, QMediaMetaData, QMediaControl
from PyQt5 import QtCore
import LibraryLoader

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

# ARTIST DROP BOX
        self.artist_select_label = QtWidgets.QLabel("Artist", self)
        self.artist_select_label.setGeometry(10, 50, 150, 25)

        self.artist_select = QtWidgets.QComboBox(self)
        self.artist_select.setGeometry(10, 70, 150, 25)
        self.artist_select.activated[str].connect(self.on_artist_selection)
        
# ALBUMS DROP BOX
        self.album_select_label = QtWidgets.QLabel("Albums", self)
        self.album_select_label.setGeometry(10, 90, 150, 25)

        self.album_select = QtWidgets.QComboBox(self)
        self.album_select.setGeometry(10, 110, 150, 25)
        self.album_select.activated[str].connect(self.on_album_selection)

# SONGS DROP BOX

        self.song_select_label = QtWidgets.QLabel("Songs", self)
        self.song_select_label.setGeometry(10, 130, 150, 25)

        self.song_select = QtWidgets.QComboBox(self)
        self.song_select.setGeometry(10, 150, 150, 25)
        #self.song_select.activated[str].connect(self.on_song_selection)

# PLAYLIST
        self.playlist = QMediaPlaylist()
        self.btn_load_selected = QtWidgets.QPushButton("Load\n selected\n songs", self)
        self.btn_load_selected.setGeometry(200, 70, 80, 100)
        self.btn_load_selected.clicked.connect(self.on_btn_load_selected)

        # some test files
        self.playlist.addMedia(QMediaContent(QtCore.QUrl.fromLocalFile("Daughter-Smother.mp3")))
        self.playlist.addMedia(QMediaContent(QtCore.QUrl.fromLocalFile("So Far Away.mp3")))

# MEDIA PLAYER
        self.player = QMediaPlayer()
        self.player.setPlaylist(self.playlist)
        self.player.playlist().setPlaybackMode(QMediaPlaylist.Loop)
        self.player.setVolume(50)

        self.player.metaDataChanged.connect(self.meta_data_changed)
        self.player.durationChanged.connect(self.on_dur_change)
        self.player.positionChanged.connect(self.on_pos_change)

# VOLUME SLIDER
        self.slider_volume = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.slider_volume.setGeometry(60, 350, 130, 20)
        self.slider_volume.setRange(0, 100)
        self.slider_volume.setValue(50)
        self.slider_volume.valueChanged.connect(self.volume_change)

# PROGRESS SLIDER
        self.slider_progress = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.slider_progress.setGeometry(60, 320, 130, 20)
        self.slider_progress.sliderMoved.connect(self.progress_change)

# LYRICS SEARCH
        self.btn_wiki = QtWidgets.QPushButton("Search\n Lyrics", self)
        self.btn_wiki.setGeometry(220,310,70,80)

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
        self.artist_select.addItem("All Artists")
        for artist in self.library:
            self.artist_select.addItem(artist)

    def on_artist_selection(self):
        current_artist = self.artist_select.currentText()
        self.album_select.clear()
        self.song_select.clear()
        self.album_select.addItem("All Albums")
        if current_artist == "All Artists":
            for artist in self.library:
                for album in self.library[artist]:
                    self.album_select.addItem(album)
        else:
            for album in self.library[current_artist]:
                self.album_select.addItem(album)

    def on_album_selection(self):
        current_artist = self.artist_select.currentText()
        current_album = self.album_select.currentText()
        self.song_select.clear()
        if current_album == "All Albums" and current_artist == "All Artists":
            for artist in self.library:
                for album in self.library[artist]:
                    for song in self.library[artist][album]:
                        self.song_select.addItem(song[0])

        elif current_album == "All Albums":
            for album in self.library[current_artist]:
                for song in self.library[current_artist][album]:
                    self.song_select.addItem(song[0])

        elif current_artist == "All Artists":
            for artist in self.library:
                for album in self.library[artist]:
                    if album == self.album_select.currentText():
                        for song in self.library[artist][album]:
                            self.song_select.addItem(song[0])
        else:
            for song in self.library[current_artist][current_album]:
                self.song_select.addItem(song[0])

    def on_btn_load_selected(self):
        self.playlist.clear()
        #import all songs to the playlist

    def on_btn_play_pause(self):
        if self.player.state() in (0, 2):
            self.player.play()
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
        print(self.player.currentMedia().canonicalUrl().toString()[5:])
