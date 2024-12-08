from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QApplication, QMessageBox, QLineEdit, QPushButton, QMessageBox, QMainWindow, QStackedWidget, QComboBox
from PyQt6 import uic
import sys
from setup_db import *
import re

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
        
        self.btn_login.clicked.connect(self.login)
        self.btn_register.clicked.connect(self.show_register)
        
    def login(self):
        msg = MessageBox()
        email = self.email.text()
        password = self.password.text()
        
        if email == "":
            msg.error_box("Email không được để trống")
            self.email.setFocus()
            return

        if password == "":
            msg.error_box("Mật khẩu không được để trống")
            self.password.setFocus()
            return

        user = get_user_by_email_and_password(email,password)
        if user:
            msg.success_box("Đăng nhập thành công")
            self.show_home(user["id"])
            return
        
        msg.error_box("Email hoặc mật khẩu không đúng")
    
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
        
        self.btn_register.clicked.connect(self.register)
        self.btn_login.clicked.connect(self.show_login)
        
    def register(self):
        msg = MessageBox()
        fullname = self.fullname.text()
        email = self.email.text()
        password = self.password.text()
        confirm_password = self.confirm_password.text()
        
        if fullname == "":
            msg.error_box("Họ tên không được để trống")
            self.fullname.setFocus()
            return
        
        if email == "":
            msg.error_box("Email không được để trống")
            self.email.setFocus()
            return

        if password == "":
            msg.error_box("Mật khẩu không được để trống")
            self.password.setFocus()
            return
        
        if confirm_password == "":
            msg.error_box("Xác nhận mật khẩu không được để trống")
            self.confirm_password.setFocus()
            return
        
        if password != confirm_password:
            msg.error_box("Mật khẩu không trùng khớp")
            self.confirm_password.setText("")
            self.password.setFocus()
            return
        
        if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',email):
            msg.error_box("Email không hợp lệ")
            self.email.setFocus()
            return
        
        if len(password) < 8:
            msg.error_box("Mật khẩu cần ít nhất 8 ký tự")
            self.setFocus()
            return
        
        if get_user_by_email(email):
            msg.error_box("Email đã tồn tại")
            return

        create_user(fullname, email, password)
        msg.success_box("Đăng ký thành công")
        self.show_login()
        
    def show_login(self):
        self.login = Login()
        self.login.show()
        self.close()
        
class Home(QMainWindow):
    def __init__(self,user_id):
        super().__init__()
        uic.loadUi("ui/Main.ui", self)
        self.user_id = user_id
        
        self.stackWidget = self.findChild(QStackedWidget, "stackedWidget")
        self.btn_info = self.findChild(QPushButton, "btn_info")
        self.btn_all = self.findChild(QPushButton, "btn_all")
        self.btn_music = self.findChild(QPushButton, "btn_music")
        self.btn_list = self.findChild(QPushButton, "btn_list")
        self.btn_info.clicked.connect(self.navInfoScreen)
        self.btn_list.clicked.connect(self.navListScreen)
        self.btn_all.clicked.connect(self.navAllScreen)
        self.btn_music.clicked.connect(self.navMusicScreen)
        
        self.txt_email = self.findChild(QLineEdit, "txt_email")
        self.txt_username = self.findChild(QLineEdit, "txt_username")
        self.txt_password = self.findChild(QLineEdit, "txt_password")
        self.txt_time = self.findChild(QLineEdit, "txt_time")
        self.txt_age = self.findChild(QLineEdit, "txt_age")
        self.cb_mctype = self.findChild(QComboBox, "cb_mctype")
        self.cb_gender = self.findChild(QComboBox, "cb_gender")

        self.loadInfo(user_id)

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
        print(user)
        self.txt_email.setText(user["email"])
        self.txt_username.setText(user["name"])
        self.txt_password.setText(user["password"])

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    app.exec()

