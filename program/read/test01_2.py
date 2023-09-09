import serial
import time
import sys
import threading
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QComboBox, QVBoxLayout, QWidget

class main_window(QMainWindow):
    def __init__(self):
        super().__init__()

class serial_read:
    def __init__(self,serial_port,buad_rate):
        self.serial_port = serial_port
        self.baud_rate = buad_rate
        self.start_serial()
        self.stop_serial()
    
    def start_serial(self):
        print("=================start=================")
        self.ser = serial.Serial(self.serial_port,self.baud_rate)
        

    def stop_serial(self):
        self.ser.close()
        print("===================end==================")

        

if __name__ == '__main__':
    serial = serial_read('/dev/ttyUSB0',9600)
    '''
    app = QApplication(sys.argv)
    From = main_window()
    From.show()
    print("=================start================")
    app.exec_()
    print("===================end==================")
    '''

