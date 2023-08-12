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
                data = self.ser.readline().decode('ascii', errors='replace').strip()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                self.log_file.write(f"{timestamp}, {data}\n")
                print(f"{timestamp}, {data}\n")
                time.sleep(0.001)
        except KeyboardInterrupt:
            self.stop_logging()

    def stop_logging(self):
        print("\n==================================================================")
        print("END")
        self.log_file.close()
        self.ser.close()

if __name__ == '__main__':
    serial_logger = SerialDataLogger('/dev/ttyACM0', 9600)
    serial_logger.start_logging()

