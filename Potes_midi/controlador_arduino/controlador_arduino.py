import serial
import threading
class ContArduino (threading.Thread):
    puerto = None
    baudios = None
    conexion = None

    def __init__(self, puerto, baudios):
        super().__init__()
        self.puerto = puerto
        self.baudios = baudios
        self.conexion = serial.Serial(self.puerto, self.baudios)
    def run(self):
        while True:
            if self.conexion.in_waiting > 0:
                data = self.conexion.read(6)
                print(data)