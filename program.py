from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QApplication, QMessageBox, QLineEdit, QPushButton, QMessageBox, QMainWindow, QStackedWidget, QComboBox, QFileDialog, QWidget, QLabel, QScrollArea, QGridLayout
from PyQt6.QtGui import QIcon
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
    play_song = QtCore.pyqtSignal(int)
    add_song_to_playlist = QtCore.pyqtSignal(int)
    def __init__(self, song_id, song_name, song_artists, song_album, song_playcount):
        super().__init__()
        uic.loadUi("ui/songItems.ui", self)
        self.song_id = song_id
        self.song_name = song_name
        self.song_artists = song_artists
        self.song_album = song_album
        self.song_playcount = song_playcount
        
        self.name = self.findChild(QLabel, "lbl_name")
        self.artist = self.findChild(QLabel, "lbl_artist")
        self.album = self.findChild(QLabel, "lbl_album")
        self.playcount = self.findChild(QLabel, "lbl_playcount")
        self.btn_play = self.findChild(QPushButton, "btn_play")
        self.btn_add = self.findChild(QPushButton, "btn_add")
        self.name.setText("Name: " + self.song_name)
        self.artist.setText("Artist: " + self.song_artists)
        self.album.setText("Album: " + self.song_album)
        self.playcount.setText("Played: " + str(self.song_playcount))
        
        self.btn_play.clicked.connect(self.play)
        self.btn_add.clicked.connect(self.add)
        
        self.setMinimumSize(250,180)
        
    def play(self):
        self.play_song.emit(self.song_id)

    def add(self):
        self.add_song_to_playlist.emit(self.song_id)
        
class Home(QMainWindow):
    def __init__(self,user_id):
        super().__init__()
        uic.loadUi("ui/Main.ui", self)
        self.play_list = []
        self.user_id = user_id
        
        self.stackWidget = self.findChild(QStackedWidget, "stackedWidget")
        self.btn_info = self.findChild(QPushButton, "btn_info")
        self.btn_all = self.findChild(QPushButton, "btn_all")
        self.btn_music = self.findChild(QPushButton, "btn_music")
        self.btn_avatar = self.findChild(QPushButton, "btn_avatar")
        self.btn_list = self.findChild(QPushButton, "btn_list")
        self.btn_info_save = self.findChild(QPushButton, "btn_info_save")
        self.songList = self.findChild(QScrollArea, "songList")
        
        self.btn_info.clicked.connect(self.navInfoScreen)
        self.btn_list.clicked.connect(self.navListScreen)
        self.btn_all.clicked.connect(self.navAllScreen)
        self.btn_music.clicked.connect(self.navMusicScreen)
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

        self.loadInfo(user_id)
        self.render_song_list(get_first_15_songs_ordered_by_playcount())

    def navInfoScreen(self):
        self.stackWidget.setCurrentIndex(3)

    def navListScreen(self):
        self.stackWidget.setCurrentIndex(2)

    def navMusicScreen(self):
        self.stackWidget.setCurrentIndex(1)

    def navAllScreen(self):
        self.stackWidget.setCurrentIndex(0)

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
        fav_music = self.cb_fav_music.text()
        if self.cb_gender.currentIndex() == 0:
            gender = "Male"
        elif self.cb_gender.currentIndex() == 1:
            gender = "Female"
        else:
            gender = "Other"
        avatar = self.user["avatar"]
        u = User(name, email, "", fav_music, gender, avatar)
        
        update_user(self.user_id, u)
        self.loadInfo(self.user_id)

    def loadAvatarFromFile(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *jpeg *.bmp)")
        if file:
            self.user["avatar"] = file
            self.btn_avatar.setIcon(QIcon(file))
            
    def render_song_list(self, song_list:list):
        row = 0
        column = 0
        for song in song_list:
            itemWidget = SongItemWidget(song["id"], song["name"], song["artist_names"], song["album_name"], song["playcount"])
            itemWidget.play_song.connect(self.play_song)
            itemWidget.add_song_to_playlist.connect(self.add_song_to_playlist)
            self.gridLayout.addWidget(itemWidget, row, column)
            column += 1
            if column == 3:
                row += 1
                column = 0

    @QtCore.pyqtSlot(int)
    def add_song_to_playlist(self, song_id):
        self.play_list.append(song_id)
        
    @QtCore.pyqtSlot(int)
    def play_song(self, song_id):
        self.play_list.append(song_id)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec()
    
