import threading
import time
from queue import Queue

import serial
import serial.tools.list_ports
from PySide6.QtCore import QObject, Signal

from core.Evento import Evento, TipoEvento
from core.Paquete import PaqueteSonido, PaqueteSaludo, Paquete, PaqueteLuz, PaqueteArduino


def get_puertos():
    return serial.tools.list_ports.comports()

#Modulo encargado de manejar la comunicacion con el arduino, se supone que solo debe recibir, decodificar la informacion y mandarla por el bus, ademas de recibir datos del modulo de logica y pasarlos al arduino tambien
class SerialArduino(QObject):
    conexion = None
    baudios = None
    puerto = None
    luz = False
    hilo = threading.Thread()
    senial_conectado = Signal()
    senial_error = Signal(str)
    senial_info = Signal(str)
    senial_potenciometro = Signal(PaqueteArduino)
    conectado = False
    def __init__(self,cola: Queue, baudios = 9600):
        super().__init__()
        self.conectado = False
        self.baudios = baudios
        self.cola = cola

    def run(self):
        self.senial_info.emit(f"Intentando conexion en {self.puerto}")
        try:
            self.conexion = serial.Serial(port=self.puerto, baudrate=self.baudios, timeout=None)
            time.sleep(3)
            self.senial_info.emit(f"Se accedio a un dispositivo en {self.puerto}, enviando paquete HandShake")
            self.conectado = True #Para que se pueda enviar el paquete
            self.conectado = self.enviarSaludo()
            while self.conectado:
                header, datos, checksum = self.conexion.read(3)
                paquete = PaqueteArduino(header,datos,checksum)
                if paquete.esPaqueteValido():
                    self.senial_potenciometro.emit(paquete)
            self.conexion.close()
            #si lo que se conecto es el arduino, este deberia contestar con un handshake tambien

        except serial.SerialException as e:
            if "Access is denied" in str(e):
                self.senial_error.emit("Acceso denegado al puerto seleccionado.\nProbablemente otro programa esta utilizandolo")
            else:
                if "FileNotFoundError" in str(e):
                    self.senial_error.emit("No se encotro ningun dispositivo de comunicacion serial o el seleccionado no es valido")
                else:
                    self.senial_error.emit("Error desconocido")

    def cambiarLuz(self):
        paquete = PaqueteLuz()
        paquete.setEstado(not paquete.estado)
        self.enviar(paquete)
    def setPuerto(self,data_puerto):
        self.puerto = str(data_puerto)



    def enviarSaludo(self):
        paquete = PaqueteSaludo()
        self.enviar(paquete)
        self.conexion.flush()
        time.sleep(0.5) #Espera 1 segundo por la respuesta
        if self.conexion.in_waiting == 3: #Esto es para que, cuando se espero el tiempo necesario, si hay 3 bytes para leer, que se lean. Esto genera que no se bloquee esperando que lleguen mas bytes.
            datos = self.conexion.read(3) #Aca no va a tener que esperar nada porque ya tiene 3 bytes para leer, lo unico que le queda es saber si son el paquete o no.
            if paquete.checkRespuesta(datos):
                #Una vez que se logro la conexion hay que habilitar los botones de luz  e iniciar y desactivar el de conectar.
                self.senial_conectado.emit()
                return True
            else:
                self.senial_error.emit("No hubo respuesta al paquete de saludo")
                return False
        else:
            self.senial_error.emit("No hubo respuesta al paquete de saludo")
            return False


    def getConectado(self):
        return self.conectado
    def conectar(self,puerto : str):
        if not self.hilo.is_alive() and not self.conectado and puerto != "":
            self.hilo = threading.Thread(target=self.run, daemon=True)
            self.puerto = puerto
            self.hilo.start()

    def enviar(self, paquete : Paquete):
        if self.getConectado():
            self.conexion.write(paquete.getPaqueteArduino().encode())
        else:
            self.senial_error.emit("No hay arduino conectado")

