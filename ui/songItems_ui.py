# Form implementation generated from reading ui file '/Users/pinxun/Documents/MindX/PTI/HTLO-PTI03/PTI_GiaNghia_ThienBao/ui/songItems.ui'
#
# Created by: PyQt6 UI code generator 6.8.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(250, 180)
        Form.setStyleSheet("background-color: #2e2e2e; /* Dark gray for the background */\n"
"    border: 2px solid #444444; /* Slightly lighter gray for the border */\n"
"    border-radius: 10px;\n"
"    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.3); /* Subtle shadow for depth */")
        self.lbl_name = QtWidgets.QLabel(parent=Form)
        self.lbl_name.setGeometry(QtCore.QRect(10, 10, 231, 31))
        self.lbl_name.setStyleSheet("color: #dddddd;")
        self.lbl_name.setObjectName("lbl_name")
        self.lbl_image = QtWidgets.QLabel(parent=Form)
        self.lbl_image.setGeometry(QtCore.QRect(10, 60, 100, 100))
        self.lbl_image.setStyleSheet("color: #dddddd;")
        self.lbl_image.setText("")
        self.lbl_image.setScaledContents(True)
        self.lbl_image.setObjectName("lbl_image")
        self.btn_play = QtWidgets.QPushButton(parent=Form)
        self.btn_play.setGeometry(QtCore.QRect(130, 110, 100, 32))
        self.btn_play.setStyleSheet("    background-color: #4caf50; /* Green button for a clean look */\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 5px;\n"
"    padding: 5px 15px;\n"
"    margin-top: 5px;")
        self.btn_play.setObjectName("btn_play")
        self.btn_add = QtWidgets.QPushButton(parent=Form)
        self.btn_add.setGeometry(QtCore.QRect(130, 70, 100, 32))
        self.btn_add.setStyleSheet("    background-color: #4caf50; /* Green button for a clean look */\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 5px;\n"
"    padding: 5px 15px;\n"
"    margin-top: 5px;")
        self.btn_add.setObjectName("btn_add")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lbl_name.setText(_translate("Form", "Name:"))
        self.btn_play.setText(_translate("Form", "Nghe"))
        self.btn_add.setText(_translate("Form", "Thêm"))
