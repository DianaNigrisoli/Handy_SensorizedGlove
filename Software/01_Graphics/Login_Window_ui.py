# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Login_Window.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QWidget)
import ResourceFiles_rc

class Ui_Login(object):
    def setupUi(self, Login):
        if not Login.objectName():
            Login.setObjectName(u"Login")
        Login.resize(491, 504)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Login.sizePolicy().hasHeightForWidth())
        Login.setSizePolicy(sizePolicy)
        Login.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.menu_button = QPushButton(Login)
        self.menu_button.setObjectName(u"menu_button")
        self.menu_button.setGeometry(QRect(190, 370, 131, 41))
        font = QFont()
        font.setFamilies([u"Montserrat SemiBold"])
        font.setPointSize(10)
        font.setBold(True)
        self.menu_button.setFont(font)
        self.menu_button.setStyleSheet(u"QPushButton{\n"
"background-color: rgb(166, 30, 34);\n"
"color: rgb(255, 246, 235);\n"
"border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover:!pressed{\n"
"background-color: rgb(255, 255, 255);\n"
"color: rgb(130, 24, 27);\n"
"border: 3px solid;\n"
"border-color: rgb(130, 24, 27);\n"
"}")
        self.name_input = QLineEdit(Login)
        self.name_input.setObjectName(u"name_input")
        self.name_input.setGeometry(QRect(140, 320, 231, 41))
        font1 = QFont()
        font1.setFamilies([u"Montserrat Medium"])
        font1.setPointSize(14)
        self.name_input.setFont(font1)
        self.name_input.setStyleSheet(u"border-radius: 10px;\n"
"background-color: rgb(255, 246, 235);\n"
"border: 2px solid;\n"
"border-color: rgb(166, 30, 34);\n"
"")
        self.name_input.setAlignment(Qt.AlignCenter)
        self.label = QLabel(Login)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(100, 100, 301, 91))
        font2 = QFont()
        font2.setFamilies([u"Forte"])
        font2.setPointSize(48)
        self.label.setFont(font2)
        self.label.setStyleSheet(u"background-color: rgb(255, 222, 191);\n"
"color: rgb(217, 66, 39);\n"
"")
        self.label.setAlignment(Qt.AlignCenter)
        self.label_2 = QLabel(Login)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(110, 280, 291, 31))
        font3 = QFont()
        font3.setFamilies([u"Montserrat Medium"])
        font3.setPointSize(10)
        font3.setItalic(True)
        self.label_2.setFont(font3)
        self.label_2.setStyleSheet(u"background-color: rgb(255, 221, 188);\n"
"color: rgb(217, 66, 39);\n"
"")
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_4 = QLabel(Login)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(130, 210, 261, 41))
        font4 = QFont()
        font4.setFamilies([u"Montserrat Medium"])
        font4.setPointSize(14)
        font4.setBold(False)
        font4.setItalic(True)
        self.label_4.setFont(font4)
        self.label_4.setStyleSheet(u"background-color: rgb(255, 222, 191);\n"
"color: rgb(217, 66, 39);\n"
"")
        self.label_3 = QLabel(Login)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(0, 0, 511, 511))
        self.label_3.setPixmap(QPixmap(u":/Images/download.jpeg"))
        self.label_3.setScaledContents(True)
        self.label_5 = QLabel(Login)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(90, -10, 321, 521))
        self.label_5.setStyleSheet(u"background-color: rgb(255, 221, 188);")
        self.label_6 = QLabel(Login)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(210, 20, 81, 81))
        self.label_6.setStyleSheet(u"background-color: rgb(255, 221, 188);\n"
"")
        self.label_6.setPixmap(QPixmap(u":/Images/hearthands2round.png"))
        self.label_6.setScaledContents(True)
        self.label_3.raise_()
        self.label_5.raise_()
        self.menu_button.raise_()
        self.name_input.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_4.raise_()
        self.label_6.raise_()

        self.retranslateUi(Login)

        QMetaObject.connectSlotsByName(Login)
    # setupUi

    def retranslateUi(self, Login):
        Login.setWindowTitle(QCoreApplication.translate("Login", u"Form", None))
        self.menu_button.setText(QCoreApplication.translate("Login", u"Login", None))
        self.name_input.setText("")
        self.label.setText(QCoreApplication.translate("Login", u"Handy", None))
        self.label_2.setText(QCoreApplication.translate("Login", u"Enter your name:", None))
        self.label_4.setText(QCoreApplication.translate("Login", u"Boost your ASL skills!", None))
        self.label_3.setText("")
        self.label_5.setText("")
        self.label_6.setText("")
    # retranslateUi

