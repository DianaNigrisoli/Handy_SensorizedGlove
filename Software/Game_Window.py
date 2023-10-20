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
import pandas as pd

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
from PyQt5.QtGui import QCursor

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
import os
import globals
from SerialWorker_connection import SerialWorker, SerialWorkerSignals
#from Menu_Window import MenuWindow
import ResourceFiles
from ML_manager import MLPredictor
from Calibration_Window import CalibrationWindow

# Logging config
logging.basicConfig(format="%(message)s", level=logging.INFO)

#Globals 
COUNTDOWN_SECS=10
CALIBRATING= False

###############
# GAME WINDOW #
###############

class PlayWindow(QWidget): 
    
    def __init__(self):
        super().__init__()
        
        loadUi('01_Graphics/Game_Window.ui', self)
       
        #Settings for buttons and labels
        self.Username_label.setText(globals.UserName) 
        self.start_button.clicked.connect(self.handle_start_button)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)
        self.solution_button.clicked.connect(self.show_solution) 
        self.start_button_pressed = False
        

        self.solution_button.setEnabled(False)
        self.exit_btn.clicked.connect(self.BackToMenu)

        self.calibration_btn.clicked.connect(self.calibration_start)

        self.image_label.setScaledContents(True)
        
        self.greatjob_label.setHidden(True)
        self.tryagain_label.setHidden(True)
        self.StayStill_label.setHidden(True)

        #Cursor 

        QApplication.restoreOverrideCursor()

        #Countdown 
        self.countdown_seconds = COUNTDOWN_SECS 
        self.update_countdown()

        #Score
        self.score =0 
        self.score_value.setText("0")

    
        #Machine learning classifier init 
        model_path = 'RandomForest_model.sav'
        scaler_path = 'scaler_acc.sav'
        self.model = MLPredictor(model_path, scaler_path)      

        
    def handle_start_button(self):
        """!
        @brief this function controls whether 
        the start button has been pressed for the first time or not (different management of the timer)
        and triggers the function self.start_game_clicked()
        """
        
        if self.check_calibration() == 0: 
            return

        self.classified_target.setText("?")
        self.solution_button.setEnabled(False)
        self.image_label.clear()
        self.image_label.hide()

        if not self.start_button_pressed:
            self.timer.start(1000)
            self.start_game_clicked()
            self.start_button_pressed = True
            self.start_button.setEnabled(False)
            self.calibration_btn.setEnabled(False)
        else:
            self.restart_timer()
            self.start_game_clicked()
            self.start_button.setEnabled(False)
            self.calibration_btn.setEnabled(False)


    def update_countdown(self):
        """!
        @brief this function updates the countdown 
            and manages the communication with the serial worker for starting the recording  
        """
        self.countdown_label.setText(str(self.countdown_seconds-1))
        self.countdown_seconds -= 1

        if (self.countdown_seconds) < 0:
            #the timer has expired, we expect for some data from the serial worker 
            self.timer.stop()
            self.countdown_label.setText("0")
            self.StayStill_label.setHidden(True)
            
            #we expect to receive some data from serial worker 
            globals.serialData = True
            data = self.receive_data()
            
            self.start_button.setEnabled(True)
            self.calibration_btn.setEnabled(True)

            if data:
                self.prediction = self.model.predict_letter(data, self.open, self.closed)#ML classification of the data
                self.classified_target.setText(self.prediction) 
                self.solution_button.setEnabled(True) #enabling the button for showing solution 
                self.update_csv(data) #update the csv with the new data               
           
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


    def start_game_clicked(self): 
        """!
        @brief this function manages the start of the game.
        """ 
        self.greatjob_label.setHidden(True)
        self.tryagain_label.setHidden(True)
        logging.info("Starting game")
        self.update_letter()


    def update_letter(self):
        """!
        @brief this function updates the letter asked to the player in a randomic way
        """
        self.random_letter = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.letter_target.setText(self.random_letter)
    

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


    def show_solution(self): 
        """!
        @brief this function allows the player to see what was the right gesture.
        """
        image_path = "hand_images\\"+ self.random_letter+".png"
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.show()



    def update_csv(self, data): 
        """!
        @brief updates the csv with the new sensors values, the date, the performance of the player (asked letter and classified letter)
        """
        filename = globals.UserName + '.csv'     
        data.append(self.random_letter)
        data.append(self.classified_target.text()) #append per la lettera classificata dal modello
        
        if(self.random_letter == self.classified_target.text()): 
            data.append(1)
            self.greatjob_label.setHidden(False)
            self.score += 1
            self.score_value.setText(str(self.score))
        else:
            data.append(0)
            self.tryagain_label.setHidden(False)
            self.score_value.setText(str(self.score))

        now = datetime.now() 
        date = now.strftime("%d_%m_%Y")
        data.append(date)

        with open('03_Recordings_game/'+ filename, 'a',newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(data)
    

    def check_calibration(self): 
        """!
        @brief checks whether the user as already done a calibration (at least once).
        """
        folder_path='03_Recordings_game'
        count=0
        for filename in os.listdir(folder_path):
            if filename == 'Calibration_' + globals.UserName + '.csv':
              count += 1
        
        if count == 0: 
            
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("Please, click on calibration button before starting the game")
            msgBox.setWindowTitle("Missing Calibration")
            msgBox.setStyleSheet("background-color: rgb(255, 221, 188)")
            msgBox.exec()
            return 0
        
        else: 
            
            with open(folder_path + '/Calibration_' + globals.UserName + '.csv', newline='') as f:  
                
                csv_reader = csv.reader(f)

                self.open  = next(csv_reader)[:-4]
                self.open=[float(i) for i in self.open]
                logging.info("Open: {}".format(self.open))

                self.closed = next(csv_reader)[:-4]
                self.closed=[float(i) for i in self.closed]
                logging.info("Closed: {}".format(self.closed))

                return 1

    def calibration_start(self): 
        """!
        @brief the function opens another winowo for calibration.
        """
        self.calibration_window = CalibrationWindow()
        self.calibration_window.show()

    def ExitHandler(self):
        """!
        @brief Kill serial worker.
        """
        globals.serialData = False
        globals.KILL = True
        globals.serial_worker.killed()



    def BackToMenu(self):
        """!
        @brief allows to go back to menu.
        """
        self.ExitHandler()
        self.close()
        
    
    

if __name__ == "__main__":
    globals.UserName='Diana'
    app = QApplication(sys.argv)
    window = PlayWindow()
    window.show()
    sys.exit(app.exec_())
