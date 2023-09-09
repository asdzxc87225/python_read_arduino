import serial
import time
import sys
import threading
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QComboBox, QVBoxLayout, QWidget

class main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("serial 讀取資料")
        self.setGeometry(100, 100, 300, 200)
        
        self.port_label = QLabel("Com Port:")
        self.port_combobox = QComboBox()
        self.port_combobox.addItem("/dev/ttyUSB0")

        self.baud_label = QLabel("Baud Rate:")
        self.baud_combobox = QComboBox()
        self.baud_combobox.addItem("9600")
        self.baud_combobox.addItem("115200")

        self.state_button = QPushButton("開始讀取") 
        self.state_button.clicked.connect(self.work_serial)
        self.flage = True
       
        self.ui()

    def ui(self):
       layout  = QVBoxLayout()
       layout.addWidget(self.port_label)
       layout.addWidget(self.port_combobox)
       layout.addWidget(self.baud_label)
       layout.addWidget(self.baud_combobox)
       layout.addWidget(self.state_button)

       central_widget = QWidget()
       central_widget.setLayout(layout)
       self.setCentralWidget(central_widget)

    def work_serial(self):
        if self.flage:
            self.port = self.port_combobox.currentText()
            self.baud = self.baud_combobox.currentText()
            self.ser = serial_read(self.port,self.baud)
            self.flage = False
            self.thread = threading.Thread(target=self.ser.start_serial)
            self.thread.start()
        else:
            self.flage = True
            self.ser.work_type = "stop"

class serial_read():
    def __init__(self,serial_port,buad_rate):
        self.serial_port = serial_port
        self.baud_rate = buad_rate
        self.work_type = "start"
    
    def start_serial(self):
        print("=================ser-start=================")
        while self.work_type == "start":
            self.ser = serial.Serial(self.serial_port,self.baud_rate)
            data_raw = self.ser.readline()  # 讀取一行
            data = data_raw.decode()   # 用預設的UTF-8解碼
            print(data_raw)
            print(data)
        self.stop_serial()
        

    def stop_serial(self):
        self.ser.close()
        print("===================ser-end==================")

        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    From = main_window()
    From.show()
    app.exec_()

