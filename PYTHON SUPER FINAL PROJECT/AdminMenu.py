import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * #FOR PUTTING THE LOGO
from PyQt5.QtCore import Qt #FOR SMOTHING AND SIZING THE LOGO
from AdminPOS1 import menu

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Computer Shop")
window.setStyleSheet("background-color: white")
window.setFixedSize(800,600)

logo = QLabel(window)
pixmap = QPixmap("D:/Python Final Project/Images/logoo.png")
size = pixmap.scaled(320, 320, Qt.KeepAspectRatio, Qt.SmoothTransformation)
logo.setPixmap(size)
logo.setGeometry(240, 1, pixmap.height(), 305)

title = QLabel("JUSTIN STORE",window)
font = QFont("Ethnocentric", 17)
title.setFont(font)
title.setStyleSheet("color: #2643DE")
title.setGeometry(283, 288, 300, 50)

userrname = QLabel("USERNAME:", window)
font1 = QFont("Ethnocentric", 17)
userrname.setFont(font1)
userrname.setStyleSheet("color: black")
userrname.setGeometry(150, 365, 300, 50)

passsword = QLabel("PASSWORD:", window)
font2 = QFont("Ethnocentric", 17)
passsword.setFont(font2)
passsword.setStyleSheet("color: black")
passsword.setGeometry(150, 430, 300, 50)

username = QLineEdit(window)
size = QFont()
size.setPointSize(12)
username.setFont(size)
username.setGeometry(365, 370, 281, 36)

passw = QLineEdit(window)
size1 = QFont()
size1.setPointSize(12)
passw.setEchoMode(QLineEdit.Password)
passw.setFont(size)
passw.setGeometry(365, 435, 281, 36)

obj = None
def clicked():
    global obj,PoptionPane

    if username.text() == 'admin123' and passw.text() == "1234":
        window.close()

        obj = menu()
        obj.home()


    else:

        PoptionPane = QWidget()
        PoptionPane.setWindowTitle("Error Message")
        PoptionPane.setFixedSize(360, 200)
        PoptionPane.setStyleSheet("background-color: #242222")

        panel = QFrame(PoptionPane)
        panel.setGeometry(15, 15, 330, 170)
        panel.setStyleSheet("background-color: #D9D9D9")

        text = QLabel("INCORRECT USERNAME \n        OR PASSWORD", panel)
        text.setGeometry(10, 60, 400, 40)
        errfont1 = QFont("Ethnocentric", 14)
        text.setFont(errfont1)
        text.setStyleSheet("color: #2842E1")

        PoptionPane.show()

signIn = QPushButton("SIGN IN", window)
butfont = QFont("Ethnocentric", 17)
signIn.setFont(butfont)
signIn.setGeometry(620, 520, 149, 50)
signIn.setStyleSheet("border-radius: 10px; background-color: lightgray; color: #2742DE")
signIn.clicked.connect(clicked)

window.show()
sys.exit(app.exec_())