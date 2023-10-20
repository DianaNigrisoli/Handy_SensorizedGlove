###########
# IMPORTS #
###########

import struct
import sys
import time
from datetime import datetime
import logging
from PyQt5 import QtCore
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
    QVBoxLayout,
    QWidget, QLabel,
    QTextEdit,
    QMessageBox,
)
import serial
import serial.tools.list_ports
import csv
import globals
from SerialWorker_connection import SerialWorker, SerialWorkerSignals

# Logging config
logging.basicConfig(format="%(message)s", level=logging.INFO)

###############
# MAIN WINDOW #
###############
class MainWindow(QMainWindow):
    def __init__(self):
        """!
        @brief Init MainWindow.
        """
        # define worker
        self.serial_worker = SerialWorker(None)

        super(MainWindow, self).__init__()

        # title and geometry
        self.setWindowTitle("Recordings for ML training - GUI")
        width = 400
        height = 320
        self.setMinimumSize(width, height)

        # create thread handler
        self.threadpool = QThreadPool()
        #logging.info("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.connected = globals.CONN_STATUS #a che serve questo? 
        self.serialscan()
        self.initUI()

    #####################
    # GRAPHIC INTERFACE #
    #####################
    def initUI(self):
        """!
        @brief Set up the graphical interface structure.
        """

        self.textEdit = QTextEdit(self)
        self.setCentralWidget(self.textEdit)

        button_hlay = QHBoxLayout()
        button_hlay.addWidget(self.com_list_widget)
        button_hlay.addWidget(self.conn_btn)
        
        start_hlay = QHBoxLayout()
        self.on_btn = QPushButton( text=("Start Recording"))
        self.on_btn.clicked.connect(lambda state, x=globals.START_REC: self.start_recording(state, x))
        start_hlay.addWidget(self.on_btn)
        
        vbox = QHBoxLayout()
        vbox.addWidget(self.textEdit)

        vlay = QVBoxLayout()
        vlay.addLayout(button_hlay)
        vlay.addLayout(start_hlay)
        vlay.addLayout(vbox)
        
        widget = QWidget()
        widget.setLayout(vlay)
        self.setCentralWidget(widget)

    ####################
    # SERIAL INTERFACE #
    ####################
    def serialscan(self):
        """!
        @brief Scans all serial ports and create a list.
        """
        # create the combo box to host port list
        self.port_text = ""
        self.com_list_widget = QComboBox()
        self.com_list_widget.currentTextChanged.connect(self.port_changed)

        # create the connection button
        self.conn_btn = QPushButton(
            text=("Connect to port {}".format(self.port_text)),
            checkable=True,
            toggled=self.on_toggle
        )
        #TODO: add code to make it unchecked if fault with BT 

        # acquire list of serial ports and add it to the combo box
        serial_ports = [
            p.name
            for p in serial.tools.list_ports.comports()
        ]
        self.com_list_widget.addItems(serial_ports)

    ###############################
    # SERIAL SIGNALS - CONNECTION #
    ###############################
    def port_changed(self):
        """!
        @brief Update conn_btn label based on selected port.
        """
        self.port_text = self.com_list_widget.currentText()
        self.conn_btn.setText("Connect to port {}".format(self.port_text))

    @pyqtSlot(bool)
    def on_toggle(self, checked):
        """!
        @brief Allow connection and disconnection from selected serial port.
        """
        if checked:
            # setup reading worker
            self.serial_worker = SerialWorker(self.port_text)  # needs to be re defined
            # connect worker signals to functions
            self.serial_worker.signals.status.connect(self.check_serialport_status)
            self.serial_worker.signals.device_port.connect(self.connected_device)
            # execute the worker
            self.threadpool.start(self.serial_worker)

        
        else:
            # kill thread
            globals.KILL = True
            globals.serialData = False
            self.serial_worker.killed()
            self.com_list_widget.setDisabled(False)  #enable the possibility to change port
            self.conn_btn.setText(
                "Connect to port {}".format(self.port_text)
            )
        

    def check_serialport_status(self, port_name, status):
        """!
        @brief Handle the status of the serial port connection.

        Available status:
            - 0  --> Error during opening of serial port
            - 1  --> Serial port opened correctly
        """
        if status == 0:
            self.conn_btn.setChecked(False)
        elif status == 1:
            # enable all the widgets on the interface

            self.com_list_widget.setDisabled(True)  # disable the possibility to change COM port when already connected
            self.conn_btn.setText(
                "Disconnect from port {}".format(port_name)
            )
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
        self.serial_worker.killed()

    #################################
    # SERIAL SIGNALS - SEND/RECEIVE #
    #################################

    @pyqtSlot()
    def start_recording(self, state, char):
        """!
        @brief Handle the start of the interrupt for signal acquisition.

        @param state is the state of the button
        @param char is the char to be sent on serial port
        """

        #checking the user ID
        id = self.textEdit.toPlainText()
        if not id:
            QMessageBox.warning(self, 'Error', 'Please enter an ID.')
            return
        
        #sending char to USART for starting the recording 
        self.serial_worker.send(char)

        #date saving for csv file definition 
        now = datetime.now() 
        date = now.strftime("%d_%m_%Y")
        
        #definition of file name
        filename = id + '_' + date + '.csv'
        
        #TODO: controllare se necessario questo sleep 
        time_delay = 0.5
        time.sleep(time_delay) 
        
        #Setting true the global variable for starting the while loop in function receive_data
        globals.serialData = True

        data = self.receive_data()

        #if no data has been received -> error 
        if not data: 
            logging.info("Error in writing on csv")
            return

        #open the csv file and write data. 
        # If the csv file already exists it will append data in the first empty row
        with open('02_Recordings/'+ filename, 'a',newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(data)

        
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

            info = self.serial_worker.receive()

            #A string of data has been received 
            if globals.READING:
                logging.info("Mean: {}.".format(info))
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

#TODO: If time expired, reset the connection button 

#############
#  RUN APP  #
#############
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    app.aboutToQuit.connect(w.ExitHandler)
    w.show()
    sys.exit(app.exec_())
