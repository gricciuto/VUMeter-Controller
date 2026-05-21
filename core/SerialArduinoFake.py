import threading
from queue import Queue
import time

from PySide6.QtCore import QObject, Signal

def get_puertos():
    return "COM1"
class SerialArduinoFake(QObject):
    hilo = threading.Thread()
    senial_conectado = Signal()
    senial_error = Signal()
    def __init__(self, cola: Queue, baudios = 9600):
        super().__init__()
        self.cola = cola
        self.puerto = None
        self.conectado = False
    def enviarPaquete(self,paquete):
        print("Se envio un paquete")
    def run(self):

        self.cola.put(["INFO",f"Intentando conexion en {self.puerto}"])
        print("corriendo")
        self.cola.put(["INFO",f"Se accedio a un dispositivo en {self.puerto}, enviando paquete HandShake"])
        self.conectado = self.enviarSaludo()
        while self.conectado:
            self.cola.put(["POT1",20])
            time.sleep(1000)
            self.cola.put(["POT1", 50])
    def cambiarLuz(self):
        print("Se modifico la luz")
        pass
    def setPuerto(self,data_puerto):
        self.puerto = str(data_puerto)
    def enviarSaludo(self):
        self.senial_conectado.emit()
        self.conectado = True
        return True
    def getConectado(self):
        return self.conectado
    def conectar(self,puerto :str):
        if not self.hilo.is_alive() and not self.conectado:
            self.hilo = threading.Thread(target=self.run, daemon=True)
            self.puerto = puerto
            self.hilo.start()
    def enviar(self, nivel_derecho, nivel_izquierdo):
        pass
