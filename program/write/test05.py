import sys
import serial
import time
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QComboBox, QVBoxLayout, QWidget, QSpinBox, QLineEdit
from datetime import datetime

class RFTransmitterQtApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("射頻發射程式")
        self.setGeometry(100, 100, 300, 200)

        self.port_label = QLabel("COM 口：")
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


        self.transmit_button = QPushButton("開始發射")
        self.transmit_button.clicked.connect(self.start_transmission)

        self.status_label = QLabel("發射狀態：等待發射")

        self.mode_data1 = QLabel("資料長度(byte):")
        self.target1 = QLineEdit()
        self.target1.setText('10')
        self.mode_data2 = QLabel("資料總數(次數):")
        self.target2 = QLineEdit()
        self.target2.setText('5')
        self.mode_data3 = QLabel("資料間隔時間(s):")
        self.target3 = QLineEdit()
        self.target3.setText('0.5')

        layout = QVBoxLayout()
        layout.addWidget(self.port_label)
        layout.addWidget(self.port_combobox)
        layout.addWidget(self.baud_label)
        layout.addWidget(self.baud_combobox)
        layout.addWidget(self.mode_data1)
        layout.addWidget(self.target1)
        layout.addWidget(self.mode_data2)
        layout.addWidget(self.target2)
        layout.addWidget(self.mode_data3)
        layout.addWidget(self.target3)

        layout.addWidget(self.status_label)
        layout.addWidget(self.transmit_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.transmitter = None
    def start_transmission(self):
        if not self.transmitter:
            port = self.port_combobox.currentText()
            baud_rate = int(self.baud_combobox.currentText())
            len_byte = int(self.target1.text())
            count = int(self.target2.text())
            delay = float(self.target3.text())
            self.transmitter = RFTransmitter(port, baud_rate,len_byte,count,delay)
            self.transmit_button.setText("停止發射")
            self.status_label.setText(f"發射狀態：中...")
            thread = threading.Thread(target=self.transmitter.start_transmission)   # 定义线程
            thread.start()
        else:
            print("\n==================================================================")
            self.transmitter.stop_transmission()
            self.transmit_button.setText("開始發射")
            self.status_label.setText("發射狀態：等待發射")
            self.transmitter = None


class RFTransmitter:
    def __init__(self, port, baud_rate, data_bytes, run_count, delaytime ):
        self.port = port
        self.baud_rate = baud_rate
        self.run_count = run_count
        self.data_bitys = data_bytes
        self.delay_time = delaytime
        self.ser = serial.Serial(self.port, self.baud_rate, timeout=1)
        self.transmitting = False
        self.set_logging()

    def send_data(self, data):
        data1 = [0 for x in range(0,self.data_bitys)]
        data1[0] = data
        for x in range(len(data1)):
            if x < len(data1)-1:
                data1[x+1] = data1[x]//256
                data1[x] =data1[x]%256
            else :
                data1[x] = data1[x]%256
        outData = bytes(data1)
        self.ser.write(outData)
        print("發送次數：", data,"\t發送資料",outData)

    def start_transmission(self):
        self.transmitting = True
        try:
            for i in range(1, self.run_count + 1):
                if not self.transmitting:
                    break
                self.send_data(i)
                self.out_logging(i)
                time.sleep(self.delay_time)
        except Exception as e:
            print("發射出錯：", e)

    def stop_transmission(self):
        self.transmitting = False
        self.stop_logging()
        self.ser.close()

    def set_logging(self):
        current_time = time.strftime("%Y%m%d_%H%M%S")
        self.log_filename = current_time + ".log"
        self.log_file = open(self.log_filename, 'a')

    def out_logging(self,data1):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        self.log_file.write(f"{timestamp}: {hex(data1)}\n")

    def stop_logging(self):
        self.log_file.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RFTransmitterQtApp()
    window.show()
    sys.exit(app.exec_())
#    work = RFTransmitter('/dev/ttyUSB0','9600')
#    work.start_transmission()

