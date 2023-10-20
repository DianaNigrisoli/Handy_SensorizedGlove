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
    pyqtSlot,
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
import globals
from SerialWorker_connection import SerialWorker, SerialWorkerSignals
from Game_Window import PlayWindow
from Statistics_Window import StatsWindow
import ResourceFiles

# Logging config
logging.basicConfig(format="%(message)s", level=logging.INFO)


class MenuWindow(QWidget): 
    
    def __init__(self):
        super().__init__()
        
        #Initialize the serial worker 
        globals.serial_worker = SerialWorker(None)

        self.no_port_found = True

        #Load of user interface (done with Qt Designer)
        loadUi('01_Graphics/Menu_Window.ui', self)
       
        #CONNECTIONS OF BUTTONS WITH WETHODS
        #Statistics & Play 
        self.statistics_button.clicked.connect(self.statistics_clicked)
        self.play_button.clicked.connect(self.play_clicked)
        self.log_out_btn.clicked.connect(self.back_to_log_in)
        '''
        #Selection and connection to port 
        self.com_list_widget.currentTextChanged.connect(self.port_changed)
        self.conn_btn.setCheckable(True)
        self.conn_btn.clicked.connect(self.on_toggle)

        serial_ports = [
            p.name
            for p in serial.tools.list_ports.comports()
        ]
        self.com_list_widget.addItems(serial_ports)'''
        
       

    ###############################
    # SERIAL SIGNALS - CONNECTION #
    ###############################
    def port_changed(self):
        """!
        @brief Update conn_btn label based on selected port.
        """
        self.port_text = self.com_list_widget.currentText()
        self.conn_btn.setText("Connect to port {}".format(self.port_text))


   
    def start_serialWorker(self, port_name):
        """!
        @brief Allow connection and disconnection from selected serial port.
        """
        
        logging.info('set_up worker')
        # setup worker
        globals.serial_worker = SerialWorker(port_name)  # needs to be re defined
        # connect worker signals to functions
        globals.serial_worker.signals.status.connect(self.check_serialport_status)
        globals.serial_worker.signals.device_port.connect(self.connected_device)
        # execute the worker

        #if (not self.no_port_found): 
        self.threadpool.start(globals.serial_worker)
        
        #else: 
        #    globals.serial_worker.run

       
        

    def check_serialport_status(self, port_name, status):
        """!
        @brief Handle the status of the serial port connection.

        Available status:
            - 0  --> Error during opening of serial port
            - 1  --> Serial port opened correctly
        """
        if status == 0:
            #self.conn_btn.setChecked(False)
             logging.info("NOT connected to port {}".format(port_name))
        elif status == 1:
            # enable all the widgets on the interface
            '''
            self.com_list_widget.setDisabled(True)  # disable the possibility to change COM port when already connected
            self.conn_btn.setText(
                "Disconnect from port {}".format(port_name)
            ) '''
            logging.info("Connected to port {}".format(port_name))


    def connected_device(self, port_name):
        """!
        @brief Checks on the termination of the serial worker.
        """
        logging.info("Port {} closed.".format(port_name))


    def ExitHandler(self):
        """!
        @brief Kill every possible running thread upon exiting application.
        """
        globals.serialData = False
        globals.KILL = True
        globals.serial_worker.killed()


    def find_com(self): 
        """!
        @brief tries to connect to all the available COM and returns the one belonging to the Glove
        """
        serial_ports = [
            p.name
            for p in serial.tools.list_ports.comports()
        ]
        

        self.no_port_found = True
        i=0
        
        logging.info("serial_ports: {}.".format(serial_ports))

        while(self.no_port_found and i<len(serial_ports)):
            port=serial_ports[i]
            self.start_serialWorker(port)
            time.sleep(5)
            
            if globals.CONN_STATUS: 
                globals.serial_worker.send('s') 
                globals.serialData = True

                if self.receive_data(port): 
                    self.no_port_found = False
                    break
                else: 
                    self.ExitHandler()
                    logging.info("Connected but not received")
                    i=i+1

            #elif (i+1) >= len(serial_ports): 
            #    logging.info("No serial port found")
            #    self.ExitHandler()
            #    break
            else: 
                self.ExitHandler()
                logging.info("Not connected to {}.".format(port))
                #logging.info("globals.CONN_STATUS: {}". format(globals.CONN_STATUS))
                i=i+1
                
        return port 
    

    def receive_data(self, port):
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
                logging.info("Something received")
                globals.serialData = False
                globals.READING = False
                return True
            
            #No string has been received in EXP_READ_TIME seconds 
            elif elapsed_time>=globals.EXP_READ_TIME: 
                logging.info("Time expired --> wrong COM {}.".format(port))
                globals.serialData = False
                globals.READING = False
                return False
            
    
    ################
    # OPTIONS MENU #
    ################
        
    @pyqtSlot(bool)
    def play_clicked(self):
       """!
        @brief Starts the game window
        """
       QApplication.setOverrideCursor(Qt.WaitCursor)
       #Start threadpool
       self.threadpool = QThreadPool()
       right_port=self.find_com()

       if not self.no_port_found: 
        #self.start_serialWorker(right_port)
        QApplication.restoreOverrideCursor()
        self.play_window = PlayWindow()
        self.play_window.show()

        
       #else: 
        #QMessageBox.warning(self, 'Error', 'Plese select a port')
        return   
    


    def statistics_clicked(self):
        """!
        @brief Starts the statistics window 
        """
        self.stats_window = StatsWindow()
        self.stats_window.show()
        #close this window - guarda come si fa
 
    def back_to_log_in(self):
        """!
        @brief allows to go back to log in window.
        """
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MenuWindow()
    window.show()
    sys.exit(app.exec_())
