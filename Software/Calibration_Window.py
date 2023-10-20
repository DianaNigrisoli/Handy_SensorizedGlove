###########
# IMPORTS #
###########

import struct
import sys
import time
from datetime import datetime
import logging
import random
import csv
import os
import typing

from PyQt5 import QtCore
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap

from PyQt5.QtCore import (
    QObject,
    QThreadPool,
    QRunnable,
    pyqtSignal,
    pyqtSlot, 
    QTimer,
    Qt,
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
       
)
import serial
import serial.tools.list_ports
import csv
import globals
from SerialWorker_connection import SerialWorker, SerialWorkerSignals
#from Menu_Window import MenuWindow
import ResourceFiles

# Logging config
logging.basicConfig(format="%(message)s", level=logging.INFO)

#Globals 
COUNTDOWN_SECS = 5



class CalibrationWindow(QWidget): 

    def __init__(self):
        super().__init__()
        
        loadUi('01_Graphics/Calibration_Window.ui', self)
        
        #Settings for buttons and labels
        self.Username_label.setText(globals.UserName) 
        self.progressBar.setValue(0)
        self.start_button.clicked.connect(self.handle_start_button)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)

        self.exit_btn.clicked.connect(self.BackToGame)

        self.StayStill_label.setHidden(True)

        self.message_label.setText("Let's start calibrating")

        #Countdown 
        self.countdown_seconds = COUNTDOWN_SECS 
        self.update_countdown()

        #Initialization of variables 
        self.start_button_pressed = False
        self.gesture =0
        self.calibration_values =[[] for _ in range(2)]


    def handle_start_button(self):
        """!
        @brief this function controls whether 
        the start button has been pressed for the first time or not (different management of the timer)
        and triggers the function self.start_game_clicked()
        """
        if not self.start_button_pressed and self.gesture ==0:
            self.message_label.setText("Open your hand")
            #self.progressBar.setValue(0)
            self.timer.start(1000)
            self.start_button_pressed = True

        elif self.start_button_pressed and self.gesture ==1:
            self.message_label.setText("Close your hand into a fist")
            #self.progressBar.setValue(50)
            self.restart_timer()

        elif self.start_button_pressed and self.gesture ==0:
            self.message_label.setText("Open your hand")
            self.progressBar.setValue(0)
            self.restart_timer()

        else: 
            self.message_label.setText("Calibration done!")
            self.progressBar.setValue(100)
            self.gesture = 0


    def update_countdown(self):
        """!
        @brief this function updates the countdown 
            and manages the communication with the serial worker for starting the recording  
        """
        self.countdown_label.setText(str(self.countdown_seconds-1))
        self.countdown_seconds -= 1

        if (self.countdown_seconds) < 0:
            # the timer has expired, we expect for some data from the serial worker 
            self.timer.stop()
            self.countdown_label.setText("0")
            self.StayStill_label.setHidden(True)
            
            #we expect to receive some data from serial worker 
            globals.serialData = True
            data = self.receive_data()

            if data:
                self.update_csv(data)                
           
        elif (self.countdown_seconds) < 1:
            #the timer has almost expired -> the recording can start 
            self.countdown_label.setText("0")
            self.StayStill_label.setHidden(False)
            #sending the recording signal to the serial worker
            globals.serial_worker.send('s')


    def restart_timer(self):
        """!
        @brief restarts the timer after the time has expired.
        """
        self.timer.stop()
        self.countdown_seconds = COUNTDOWN_SECS
        self.update_countdown()
        self.timer.start(1000)


    def update_csv(self, data): 
        """!
        @brief updates the csv with the new sensors values, the date, the performance of the player (asked letter and classified letter)
        """
        if self.gesture ==0:     
            data.append('open')
            self.calibration_values[0] = data
            self.gesture = self.gesture +1
            self.progressBar.setValue(50)
            
        elif self.gesture ==1: 
            data.append('closed')
            self.calibration_values[1] = data
            self.gesture = self.gesture +1
            self.progressBar.setValue(100)

            filename = '03_Recordings_game/'+'Calibration_' + globals.UserName + '.csv'
            file_exists = os.path.exists(filename)
            mode = 'w' if file_exists else 'x'  # 'w' for write, 'x' for exclusive creation

            with open(filename, mode,newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerows(self.calibration_values)

    def BackToGame(self):
        """!
        @brief allows to go back to the game.
        """
        self.close()

    def receive_data(self):
        """!
        @brief in a while loop controls if some data has been received.
        """
        #time checking for avoiding an infinite loop
        start_time = time.time()
        elapsed_time=0

        while globals.serialData:  
            
            current_time = time.time()
            elapsed_time = current_time - start_time

            info = globals.serial_worker.receive()

            #A string of data has been received 
            if globals.READING:
                logging.info("Data: {}.".format(info))
                list_means = info.split(",")
                globals.serialData = False
                globals.READING = False
                return list_means
            
            #No string has been received in EXP_READ_TIME seconds 
            elif elapsed_time>=globals.EXP_READ_TIME: 
                logging.info("Time expired, no message arrived")
                globals.serialData = False
                globals.READING = False
                return 






if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalibrationWindow()
    window.show()
    sys.exit(app.exec_())