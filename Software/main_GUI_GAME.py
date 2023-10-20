###########
# IMPORTS #
###########

import struct
import sys
import time
from datetime import datetime
import logging
from PyQt5 import QtCore
from PyQt5.uic import loadUi
from PyQt5.QtCore import (
    QObject,
    QThreadPool,
    QRunnable,
    pyqtSignal,
    pyqtSlot
)
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QComboBox,
    QHBoxLayout,
    QGridLayout,
    QVBoxLayout,
    QWidget, QLabel,
    QTextEdit,
    QMessageBox,
    QLineEdit,
    QDialog,
    qApp,
)
import serial
import serial.tools.list_ports
import csv
import globals
from SerialWorker_connection import SerialWorker, SerialWorkerSignals
from Game_Window import PlayWindow
from Menu_Window_noCOM import MenuWindow

#sys.path.insert(1, '01_Graphics')
import ResourceFiles

# Logging config
logging.basicConfig(format="%(message)s", level=logging.INFO)


################
# LOGIN WINDOW #
################
class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()

        loadUi('01_Graphics/Login_Window.ui', self)
        self.menu_button.clicked.connect(self.show_menu_window)
    
    def show_menu_window(self):
        name = self.name_input.text()
        if name:
            logging.info(f"Starting game for {name}")
        
            globals.UserName = name
            self.menu_window = MenuWindow()
            self.menu_window.show()
            
    
        else:
           #QMessageBox.warning(self, 'Error', 'Please enter an ID.')
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("Please, enter a valid ID.")
            msgBox.setWindowTitle("Login Error")
            msgBox.setStyleSheet("background-color: rgb(255, 221, 188)")
            msgBox.exec()
            return
       


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
