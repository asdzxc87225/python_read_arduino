import serial
import time
from datetime import datetime

class SerialDataLogger:
    def __init__(self, serial_port, baud_rate):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.ser = serial.Serial(self.serial_port, self.baud_rate)

        current_time = time.strftime("%Y%m%d_%H%M%S")
        self.log_filename = current_time + ".log"
        self.log_file = open(self.log_filename, 'w')

    def start_logging(self):
        try:
            while True:
                #data = self.ser.readline().decode('ascii', errors='replace').strip()
                data = self.ser.read(1)
                data = hex(data[0])
                #data = data.hexlify(binary_data).decode('utf-8')
                print(type(data))
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                self.log_file.write(f"{timestamp}: {data}\n")
                print(f"{timestamp}: {data}\n")
        except KeyboardInterrupt:
            self.stop_logging()

    def stop_logging(self):
        print("\n==================================================================")
        print("END")
        self.log_file.close()
        self.ser.close()

if __name__ == '__main__':
    serial_logger = SerialDataLogger('/dev/ttyUSB0', 9600)
    serial_logger.start_logging()

