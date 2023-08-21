import serial
import time
import sys
import threading
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QComboBox, QVBoxLayout, QWidget

class widget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("接收模式")
        self.setGeometry(100, 100, 300, 200)

        self.port_label = QLabel("COM Port：")
        self.port_combobox = QComboBox()
        self.port_combobox.addItem("/dev/ttyUSB0")  # 根據您的情況添加串口
        self.port_combobox.addItem("/dev/ttyUSB1")
        self.port_combobox.addItem("/dev/ttyACM0")
        self.port_combobox.addItem("COM1")
        # 添加更多串口

        self.baud_label = QLabel("波特率：")
        self.baud_combobox = QComboBox()
        self.baud_combobox.addItem("9600")
        self.baud_combobox.addItem("115200")
        # 添加更多波特率


        self.transmit_button = QPushButton("開始接收")
        self.transmit_button.clicked.connect(self.rum)
        self.status_label = QLabel("狀態：等待接收")
        self.ui()
    def ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.port_label)
        layout.addWidget(self.port_combobox)
        layout.addWidget(self.baud_label)
        layout.addWidget(self.baud_combobox)
        layout.addWidget(self.transmit_button)
        layout.addWidget(self.status_label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.transmitter = None
    def rum(self):
        if not self.transmitter:
            port = self.port_combobox.currentText()
            baud_rate = int(self.baud_combobox.currentText())
            self.transmitter = SerialDataLogger(port, baud_rate)
            self.transmit_button.setText("停止接收")
            self.status_label.setText(f"狀態：工作中")
            self.thread = threading.Thread(target=self.transmitter.start_logging,)   # 定义线程
            self.thread.start()
        else:
            self.transmitter.stop = False
           # self.transmitter.stop_logging()
            self.transmit_button.setText("開始接收")
            self.status_label.setText("狀態：休息中")
            self.transmitter = None

class SerialDataLogger:
    def __init__(self, serial_port, baud_rate):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.ser = serial.Serial(self.serial_port, self.baud_rate)

        current_time = time.strftime("%Y%m%d_%H%M%S")
        self.log_filename = current_time + ".log"
        self.log_file = open(self.log_filename, 'w')
        self.stop = True

    def start_logging(self):
        try:
            while True:
                if self.stop != True:
                    print('停下')
                    self.stop_logging()
                    break
                else:

                    if (self.ser.in_waiting>0):
                        data = self.ser.read(1)
                        #data = hex(data[0])
                        print(type(data))
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                        self.log_file.write(f"{timestamp}: {data}\n")
                        print(f"{timestamp}: {data}\n")
                    else:
                        print('no')
        except KeyboardInterrupt:
            self.stop_logging()

    def stop_logging(self):
        print("\n==================================================================")
        print("END")
        self.log_file.close()
        self.ser.close()

if __name__ == '__main__':
    #serial_logger = SerialDataLogger('/dev/ttyUSB0', 9600)
    #serial_logger.start_logging()
    app = QApplication(sys.argv)
    From = widget()
    From.show()
    sys.exit(app.exec_())

