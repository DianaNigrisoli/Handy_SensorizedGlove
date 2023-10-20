###########
# IMPORTS #
###########

import struct
import sys
import time
import logging
import threading

from PyQt5 import QtCore
from PyQt5.QtCore import (
    QObject,
    QThreadPool,
    QRunnable,
    pyqtSignal,
    pyqtSlot,
)
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QComboBox,
    QHBoxLayout,
    QVBoxLayout,
    QWidget, 
    QLabel,
)
import serial
import serial.tools.list_ports

#global variables
import globals 

# Logging config
logging.basicConfig(format="%(message)s", level=logging.INFO)


#########################
# SERIAL_WORKER_SIGNALS #
#########################
class SerialWorkerSignals(QObject):
    """!
    @brief Class that defines the signals available to a serialworker.

    Available signals (with respective inputs) are:
        - device_port:
            str --> port name to which a device is connected
        - status:
            str --> port name
            int --> macro representing the state (0 - error during opening, 1 - success)
    """
    device_port = pyqtSignal(str)
    status = pyqtSignal(str, int)
    


#################
# SERIAL_WORKER #
#################
class SerialWorker(QRunnable):
    """!
    @brief Main class for serial communication: handles connection with device.
    """

    def __init__(self, serial_port_name):
        """!
        @brief Init worker.
        """
        super().__init__()
        # init port, params and signals
        self.port = serial.Serial()
        self.port_name = serial_port_name
        self.baudrate = 9600  # hard coded but can be a global variable, or an input param
        self.signals = SerialWorkerSignals()

    @pyqtSlot()
    def run(self):
        """!
        @brief Estabilish connection with desired serial port.
        """
        
        if not globals.CONN_STATUS:
            try:
                self.port = serial.Serial(port=self.port_name, baudrate=self.baudrate,
                                          write_timeout=0, timeout=2)
                if self.port.is_open:
                    globals.CONN_STATUS = True
                    logging.info("Prova {}".format(self.port_name))
                    self.signals.status.emit(self.port_name, 1)
                    time.sleep(0.01)

                    '''
                    #Check if the port is still connected 
                    port_controller = threading.Thread(target=self.check_presence, args=(self.port_name, 1,))
                    port_controller.setDaemon(True)
                    #A daemon thread is a background thread. 
                    port_controller.start()'''

            except serial.SerialException:
                logging.info("Error with port {}.".format(self.port_name))
                self.signals.status.emit(self.port_name, 0)
                time.sleep(0.01)

    
    #codice alternativo a usare Daemon Thread 
    '''
        while globals.CONN_STATUS: 
            myports = [p.name for p in serial.tools.list_ports.comports()]

            if self.port_name not in myports:
                logging.info("Error:port {} not present.".format(self.port_name))
                globals.KILL = True
                self.serial_worker.killed()
                #self.signals.status.emit(self.port_name, 0) #controllare se funziona questa riga
                break
            time.sleep(1)
            '''


    def check_presence(self, right_port, interval=1):
        
        while globals.CONN_STATUS: 
            myports = [p.name for p in serial.tools.list_ports.comports()]

            if right_port not in myports:
                logging.info("Error:port {} not present.".format(self.port_name))
                globals.KILL = True
                globals.FAULT_CONNECTION = True
                self.killed()
                break
            time.sleep(interval)


    #@pyqtSlot()
    def send(self, char):
        """!
        @brief Basic function to send a single char on serial port.
        """
        try:
            self.port.write(char.encode('utf-8'))
            logging.info("Written {} on port {}.".format(char, self.port_name))
        except:
            logging.info("Could not write {} on port {}.".format(char, self.port_name))

    #@pyqtSlot()
    def receive(self):
        """!
        @brief Basic function to receive a line (the data needs to end with '\n') on serial port.
        """
        #try:
        text = self.port.readline().decode("utf-8").strip()
        
        if len(text) > 0:
            globals.READING = True
            return text
        else:
            globals.READING = False
        #except:
            #logging.info("Could not read on port {}.".format(self.port_name))


    @pyqtSlot()
    def killed(self):
        """!
        @brief Close the serial port before closing the app.
        """
        
        if globals.KILL and globals.CONN_STATUS:
            self.port.close()
            time.sleep(0.01)
            globals.CONN_STATUS = False
            #self.signals.device_port.emit(self.port_name)
            globals.KILL = False
            logging.info("Process killed")

