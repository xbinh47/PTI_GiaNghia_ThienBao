from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import *
from PyQt6.QtCore import *
from PyQt6 import uic
import sys
from setup_db import *
import re
from model.song import Song
class MessageBox():
    def success_box(self, message):
        box = QMessageBox()
        box.setWindowTitle("Success")
        box.setText(message)
        box.setIcon(QMessageBox.Icon.Information)
        box.exec()
        
    def error_box(self, message):
        box = QMessageBox()
        box.setWindowTitle("Error")
        box.setText(message)
        box.setIcon(QMessageBox.Icon.Critical)
        box.exec()

class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/Login.ui", self)
        
        self.email = self.findChild(QLineEdit, "txt_email")
        self.password = self.findChild(QLineEdit, "txt_password")
        self.btn_login = self.findChild(QPushButton, "btn_login")
        self.btn_register = self.findChild(QPushButton, "btn_register")
        self.btn_lock = self.findChild(QPushButton, "btn_lock")
        
        self.btn_login.clicked.connect(self.login)
        self.btn_register.clicked.connect(self.show_register)

        self.btn_lock.clicked.connect(lambda: self.hiddenOrShow(self.password, self.btn_lock))
        
    def hiddenOrShow(self, input:QLineEdit, button:QPushButton):
        if input.echoMode() == QLineEdit.EchoMode.Password:
            input.setEchoMode(QLineEdit.EchoMode.Normal)
            button.setIcon(QIcon("img/eye-solid.svg"))
        else:
            input.setEchoMode(QLineEdit.EchoMode.Password)
            button.setIcon(QIcon("img/eye-slash-solid.svg"))
        
    def login(self):
        msg = MessageBox()
        email = self.email.text()
        password = self.password.text()
        
        if email == "":
            msg.error_box("Email can't be empty")
            self.email.setFocus()
            return

        if password == "":
            msg.error_box("Password can't be empty")
            self.password.setFocus()
            return

        user = get_user_by_email_and_password(email,password)
        if user:
            msg.success_box("Welcome")
            self.show_home(user["id"])
            return
        
        msg.error_box("Email or password is incorrect!")
    
    def show_home(self,user_id):
        self.home = Home(user_id)
        self.home.show()
        self.close()   

    def show_register(self):
        self.register = Register()
        self.register.show()
        self.close()

class Register(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/CreateAccount.ui", self)
        
        self.fullname = self.findChild(QLineEdit, "txt_fullname")
        self.email = self.findChild(QLineEdit, "txt_email")
        self.password = self.findChild(QLineEdit, "txt_password")
        self.confirm_password = self.findChild(QLineEdit, "txt_conf_pwd")
        self.btn_register = self.findChild(QPushButton, "btn_register")
        self.btn_login = self.findChild(QPushButton, "btn_login")
        self.btn_lock1 = self.findChild(QPushButton, "btn_lock1")
        self.btn_lock2 = self.findChild(QPushButton, "btn_lock2")
        
        self.btn_register.clicked.connect(self.register)
        self.btn_login.clicked.connect(self.show_login)

        self.btn_lock1.clicked.connect(lambda: self.hiddenOrShow(self.password, self.btn_lock1))
        self.btn_lock2.clicked.connect(lambda: self.hiddenOrShow(self.confirm_password, self.btn_lock2))
        
    def hiddenOrShow(self, input:QLineEdit, button:QPushButton):
        if input.echoMode() == QLineEdit.EchoMode.Password:
            input.setEchoMode(QLineEdit.EchoMode.Normal)
            button.setIcon(QIcon("img/eye-solid.svg"))
        else:
            input.setEchoMode(QLineEdit.EchoMode.Password)
            button.setIcon(QIcon("img/eye-slash-solid.svg"))
        
    def register(self):
        msg = MessageBox()
        fullname = self.fullname.text()
        email = self.email.text()
        password = self.password.text()
        confirm_password = self.confirm_password.text()
        
        if fullname == "":
            msg.error_box("Name can't be empty")
            self.fullname.setFocus()
            return
        
        if email == "":
            msg.error_box("Email can't be empty")
            self.email.setFocus()
            return

        if password == "":
            msg.error_box("Password can't be empty")
            self.password.setFocus()
            return
        
        if confirm_password == "":
            msg.error_box("Please comfirm the password")
            self.confirm_password.setFocus()
            return
        
        if password != confirm_password:
            msg.error_box("Comfirm password is not correct with password")
            self.confirm_password.setText("")
            self.password.setFocus()
            return
        
        if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',email):
            msg.error_box("Email is not valid")
            self.email.setFocus()
            return
        
        if len(password) < 8:
            msg.error_box("Password must be at least 8 characters")
            self.setFocus()
            return
        
        if get_user_by_email(email):
            msg.error_box("Email is not ")
            return

        create_user(fullname, email, password)
        msg.success_box("Register sussucfully!")
        self.show_login()
        
    def show_login(self):
        self.login = Login()
        self.login.show()
        self.close()

class SongItemWidget(QWidget):
    play_song = QtCore.pyqtSignal(str)
    add_song_to_playlist = QtCore.pyqtSignal(str)
    def __init__(self, song_id, song_name, image_path):
        super().__init__()
        uic.loadUi("ui/songItems.ui", self)
        self.song_id = song_id
        self.song_name = song_name
        self.image_path = image_path
        
        self.name = self.findChild(QLabel, "lbl_name")
        self.image = self.findChild(QLabel, "lbl_image")
        self.btn_play = self.findChild(QPushButton, "btn_play")
        self.btn_add = self.findChild(QPushButton, "btn_add")
        self.name.setText("Name: " + self.song_name)
        self.image.setPixmap(QPixmap(self.image_path))
        
        self.btn_play.clicked.connect(self.play)
        self.btn_add.clicked.connect(self.add)
        
        self.setMinimumSize(250,180)
        
    def play(self):
        self.play_song.emit(self.song_id)

    def add(self):
        self.add_song_to_playlist.emit(self.song_id)
        
class PlaylistItemWidget(QWidget):
    play_song = QtCore.pyqtSignal(str)
    delete_song_from_playlist = QtCore.pyqtSignal(str)
    def __init__(self, song_id, song_name, image_path):
        super().__init__()
        uic.loadUi("ui/playlistItem.ui", self)
        self.song_id = song_id
        self.song_name = song_name
        self.image_path = image_path
        
        self.name = self.findChild(QLabel, "lbl_name")
        self.image = self.findChild(QLabel, "lbl_image")
        self.btn_play = self.findChild(QPushButton, "btn_play")
        self.btn_delete = self.findChild(QPushButton, "btn_delete")
        self.name.setText("Name: " + self.song_name)
        self.image.setPixmap(QPixmap(self.image_path))
        
        self.btn_play.clicked.connect(self.play)
        self.btn_delete.clicked.connect(self.delete)
        
        self.setMinimumSize(250,180)
        
    def play(self):
        self.play_song.emit(self.song_id)

    def delete(self):
        self.delete_song_from_playlist.emit(self.song_id)  
class Home(QMainWindow):
    def __init__(self,user_id):
        super().__init__()
        uic.loadUi("ui/Main.ui", self)
        self.user_id = user_id
        self.current_song = None
        self.play_list = []
        
        # ui
        self.stackWidget = self.findChild(QStackedWidget, "stackedWidget")
        self.btn_info = self.findChild(QPushButton, "btn_info")
        self.btn_all = self.findChild(QPushButton, "btn_all")
        self.btn_avatar = self.findChild(QPushButton, "btn_avatar")
        self.btn_list = self.findChild(QPushButton, "btn_list")
        self.btn_info_save = self.findChild(QPushButton, "btn_info_save")
        self.songList = self.findChild(QScrollArea, "songList")
        self.playlistList = self.findChild(QScrollArea, "playlistList")
        self.btn_search = self.findChild(QPushButton, "btn_search")
        self.txt_search = self.findChild(QLineEdit, "txt_search")
        self.lbl_detail_img = self.findChild(QLabel, "lbl_detail_img")
        self.lbl_detail_name = self.findChild(QLabel, "lbl_detail_name")
        self.lbl_detail_artist = self.findChild(QLabel, "lbl_detail_artist")
        self.lbl_detail_album = self.findChild(QLabel, "lbl_detail_album")
        self.lbl_detail_playcount = self.findChild(QLabel, "lbl_detail_playcount")
        
        self.btn_info.clicked.connect(self.navInfoScreen)
        self.btn_list.clicked.connect(self.navListScreen)
        self.btn_all.clicked.connect(self.navAllScreen)
        self.btn_avatar.clicked.connect(self.loadAvatarFromFile)
        self.btn_info_save.clicked.connect(self.changeAccountInfo)
        
        self.txt_email = self.findChild(QLineEdit, "txt_email")
        self.txt_username = self.findChild(QLineEdit, "txt_username")
        self.cb_fav_music  = self.findChild(QComboBox, "cb_fav_music")
        self.cb_gender = self.findChild(QComboBox, "cb_gender")
        
        self.songItem = QWidget()
        self.gridLayout = QGridLayout(self.songItem)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setSpacing(10)

        self.songItem.setLayout(self.gridLayout)
        self.songList.setWidget(self.songItem)
        self.songList.setWidgetResizable(True)
        
        self.playlistItem = QWidget()
        self.gridLayout2 = QGridLayout(self.playlistItem)
        self.gridLayout2.setContentsMargins(10, 10, 10, 10)
        self.gridLayout2.setSpacing(10)

        self.playlistItem.setLayout(self.gridLayout2)
        self.playlistList.setWidget(self.playlistItem)
        self.playlistList.setWidgetResizable(True)

        self.loadInfo(user_id)
        self.render_song_list(get_first_15_songs_ordered_by_playcount())
        self.get_and_render_playlist(user_id)
        self.btn_search.clicked.connect(self.search_song)
        
        # media player
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(50)
        
        self.player.errorOccurred.connect(self.handle_player_error)
        
        self.playBtn = self.findChild(QPushButton, "btn_play")
        self.volumeBtn = self.findChild(QPushButton, "btn_volume")
        self.volumeBar = self.findChild(QSlider, "slider_volume")
        self.durationBar = self.findChild(QSlider, "slider_duration")
        self.timeLabel = self.findChild(QLabel, "lbl_time")
        self.curr_name = self.findChild(QLabel, "lbl_curr_name")
        self.curr_img = self.findChild(QLabel, "lbl_curr_img")
        
        self.playIcon = QIcon("img/play-solid.svg")
        self.pauseIcon = QIcon("img/pause-solid.svg")
        self.volumeOffIcon = QIcon("img/volume-off-solid.svg")
        self.volumeLowIcon = QIcon("img/volume-low-solid.svg")
        self.volumeHighIcon = QIcon("img/volume-high-solid.svg")
        self.muteIcon = QIcon("img/volume-off-solid.svg")
        
        self.playBtn.setIcon(self.playIcon)
        self.playBtn.clicked.connect(self.togglePlay)
        self.volumeBtn.setIcon(self.volumeOffIcon)
        self.volumeBtn.clicked.connect(self.toggleMute)

        self.volumeBar.valueChanged.connect(self.setVolume)
        self.durationBar.sliderMoved.connect(self.setPosition)
        self.player.positionChanged.connect(self.positionChanged)
        self.player.durationChanged.connect(self.durationChanged)
        self.player.playbackStateChanged.connect(self.mediaStateChanged)
        self.volumeBar.setValue(50)
        self.durationBar.setValue(0)

    def navInfoScreen(self):
        self.stackWidget.setCurrentIndex(1)

    def navListScreen(self):
        self.stackWidget.setCurrentIndex(0)

    def navAllScreen(self):
        self.stackWidget.setCurrentIndex(2)

    def loadInfo(self, user_id):
        user = get_user_by_id(user_id)
        self.user = user
        self.txt_email.setText(user["email"])
        self.txt_username.setText(user["name"])
        if user["fav_music"]:
            self.cb_fav_music.setCurrentIndex(user["fav_music"])
        if user["gender"] == "Male":
            self.cb_gender.setCurrentIndex(0)
        elif user["gender"] == "Female":
            self.cb_gender.setCurrentIndex(1)
        else: 
            self.cb_gender.setCurrentIndex(2)

    def changeAccountInfo(self):
        name = self.txt_username.text()
        email = self.txt_email.text()
        fav_music = self.cb_fav_music.currentIndex()
        if self.cb_gender.currentIndex() == 0:
            gender = "Male"
        elif self.cb_gender.currentIndex() == 1:
            gender = "Female"
        else:
            gender = "Other"
        avatar = self.user["avatar"]
        u = User(name, email, "", fav_music, gender, avatar)
        update_user(self.user_id, u)
        msg = MessageBox()
        msg.success_box("Account info updated")
        self.loadInfo(self.user_id)

    def loadAvatarFromFile(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *jpeg *.bmp)")
        if file:
            self.user["avatar"] = file
            self.btn_avatar.setIcon(QIcon(file))
            
    def render_song_list(self, song_list:list):
        # clear the grid layout
        for i in reversed(range(self.gridLayout.count())):
            widgetToRemove = self.gridLayout.itemAt(i).widget()
            self.gridLayout.removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)
            
        row = 0
        column = 0
        for song in song_list:
            itemWidget = SongItemWidget(song["id"], song["name"], song["image_path"])
            itemWidget.play_song.connect(self.play_song)
            itemWidget.add_song_to_playlist.connect(self.add_song_to_playlist)
            self.gridLayout.addWidget(itemWidget, row, column)
            column += 1
            if column == 3:
                row += 1
                column = 0
                
    def get_and_render_playlist(self, user_id):
        # clear the grid layout
        for i in reversed(range(self.gridLayout2.count())):
            widgetToRemove = self.gridLayout2.itemAt(i).widget()
            self.gridLayout2.removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)

        playlist = get_playlist_by_user_id(user_id)
        self.play_list = playlist
        row = 0
        column = 0
        for song in playlist:
            itemWidget = PlaylistItemWidget(song["song_id"], song["song_name"], song["image_path"])
            itemWidget.play_song.connect(self.play_song)
            itemWidget.delete_song_from_playlist.connect(self.delete_song_from_playlist)
            self.gridLayout2.addWidget(itemWidget, row, column)
            column += 1
            if column == 3:
                row += 1
                column = 0
                
    def search_song(self):
        name = self.txt_search.text()
        song_list = get_songs_by_name(name)
        self.render_song_list(song_list)

    @QtCore.pyqtSlot(str)
    def add_song_to_playlist(self, song_id):
        song = get_song_by_id(song_id)
        exist_song = get_playlist_by_user_id_and_song_id(self.user_id, song_id)
        msg = MessageBox()
        if exist_song:
            msg.error_box("Song already in playlist")
            return
        add_song_to_playlist(self.user_id, song_id, song["name"], song["image_path"])
        msg.success_box("Song added to playlist")
        self.get_and_render_playlist(self.user_id)
        
    @QtCore.pyqtSlot(str)
    def play_song(self, song_id):
        self.current_song = song_id
        song = get_song_by_id(song_id)
        file_path = QUrl.fromLocalFile(song["file_path"].replace("\\", "/"))
        self.player.setSource(file_path)
        self.player.play()
        self.playBtn.setIcon(self.pauseIcon)
        self.curr_name.setText(f"Now playing: {song['name']}")
        self.curr_img.setPixmap(QPixmap(song["image_path"]))
        self.lbl_detail_img.setPixmap(QPixmap(song["image_path"]))
        self.lbl_detail_name.setText(f"Name: {song['name']}")
        self.lbl_detail_artist.setText(f"Artist: {song['artist_names']}")
        self.lbl_detail_album.setText(f"Album: {song['album_name']}")
        self.lbl_detail_playcount.setText(f"Playcount: {song['playcount']}")
    
    def delete_song_from_playlist(self, song_id):
        delete_song_from_playlist(self.user_id, song_id)
        self.get_and_render_playlist(self.user_id)
        
    def handle_player_error(self, error, error_string):
        print(f"Media player error: {error} - {error_string}")
        
    def mediaStateChanged(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.playBtn.setIcon(self.pauseIcon)
        else:
            self.playBtn.setIcon(self.playIcon)

    def positionChanged(self, position):
        self.durationBar.setValue(position)
        # Convert position and duration from milliseconds to hh:mm:ss format
        current_time = self.formatTime(position)
        total_time = self.formatTime(self.player.duration())
        self.timeLabel.setText(f"{current_time}/{total_time}")
        
    def durationChanged(self, duration):
        self.durationBar.setRange(0, duration)
    
    def handleError(self):
        self.playBtn.setEnabled(False)
        error_message = self.player.errorString()
        self.playBtn.setText(f"Error: {error_message}")
        print(f"Media Player Error: {error_message}")
        
    def play(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        else:
            self.player.play()
    
    def setPosition(self, position):
        if self.player.duration() > 0:  # Only set position if media is loaded
            self.player.setPosition(position)
        
    def setVolume(self, volume):
        # Convert the slider value to a float between 0.0 and 1.0
        volume = volume / 100.0
        self.audio_output.setVolume(volume)
        if volume == 0.0:
            self.volumeBtn.setIcon(self.volumeOffIcon)
        elif volume < 0.5:
            self.audio_output.setMuted(False)
            self.volumeBtn.setIcon(self.volumeLowIcon)
        else:
            self.volumeBtn.setIcon(self.volumeHighIcon)
            self.audio_output.setMuted(False)
    
    def toggleMute(self):
        if self.audio_output.isMuted():
            self.audio_output.setMuted(False)
            if self.current_volume >= 50:
                self.volumeBtn.setIcon(self.volumeHighIcon)
            elif self.current_volume < 50:
                self.volumeBtn.setIcon(self.volumeLowIcon)
            else:
                self.volumeBtn.setIcon(self.volumeOffIcon)
            self.volumeBar.setValue(self.current_volume)
        else:
            self.audio_output.setMuted(True)
            self.volumeBtn.setIcon(self.muteIcon)
            self.current_volume = self.volumeBar.value()
            self.volumeBar.setValue(0)
    
    def togglePlay(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
            self.playBtn.setIcon(self.playIcon)
        else:
            self.player.play()
            self.playBtn.setIcon(self.pauseIcon)

    def formatTime(self, milliseconds):
        total_seconds = milliseconds // 1000
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    window = Home(1)
    window.show()
    app.exec()
    
