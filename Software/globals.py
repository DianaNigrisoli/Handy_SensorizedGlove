# Globals
from SerialWorker_connection import SerialWorker, SerialWorkerSignals

#Serial worker
serial_worker = SerialWorker(None)

# Globals used in the management of the serial connection
CONN_STATUS: bool = False
KILL: bool= False
FAULT_CONNECTION: bool =False

# Signal to send via USART/BT in oder to start the acquisition of sensor values 
START_REC: chr = "s"

# Global variables used for initializing the reading procedure from the serial port
serialData: bool = False
READING: bool = False

#After sending the START_REC signal, the GUI waits maximum EXP_READ_TIME seconds in a while loop for the response of the psoc,
# this is done in oder to prevent an infinit while loop.
EXP_READ_TIME: int = 3

#User Name for game 
UserName=[]