import sys
import mutagen
from PyQt5 import QtWidgets
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist, QMediaMetaData, QMediaControl
from PyQt5 import QtCore


class Window(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.setGeometry(50, 50, 300, 400)
        self.setWindowTitle("Rolev Player")
# PLAYLIST
        self.playlist = QMediaPlaylist()
        #self.playlist.addMedia(QMediaContent(QtCore.QUrl.fromLocalFile("TestMusic/Dear Whoever/04 - Tears of Ashes.mp3")))
        self.playlist.addMedia(QMediaContent(QtCore.QUrl.fromLocalFile("01 - A Message To The Unknown.mp3")))
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

app = QtWidgets.QApplication(sys.argv)
GUI = Window()
sys.exit(app.exec_())
