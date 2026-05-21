import threading
import time
from queue import Queue

import serial
import serial.tools.list_ports
from PySide6.QtCore import QObject, Signal

from core.Evento import Evento, TipoEvento


def get_puertos():
    return serial.tools.list_ports.comports()

#Modulo encargado de manejar la comunicacion con el arduino, se supone que solo debe recibir, decodificar la informacion y mandarla por el bus, ademas de recibir datos del modulo de logica y pasarlos al arduino tambien
class SerialArduinoFake(QObject):
    conexion = None
    baudios = None
    puerto = None
    luz = False
    hilo = threading.Thread()
    senial_conectado = Signal()
    senial_error = Signal()
    def __init__(self,cola: Queue, baudios = 9600):
        super().__init__()
        self.conectado = False
        self.baudios = baudios
        self.cola = cola
    def enviarPaquete(self,paquete):
        #Simula enviar un paquete
        pass

    def run(self):
        self.cola.put(["INFO",f"Intentando conexion en {self.puerto}"])
        print("corriendo")
        try:
            self.conexion = serial.Serial(port=self.puerto, baudrate=self.baudios, timeout=None)
            time.sleep(3)
            self.cola.put(["INFO",f"Se accedio a un dispositivo en {self.puerto}, enviando paquete HandShake"])
            self.conectado = self.enviarSaludo()
            while self.conectado:
                self.cola.put(["POT1",20])
                time.sleep(1000)
                self.cola.put(["POT1", 50])
                #Aca es donde si hay paquetes para leer (de que se movio un potenciometro) se va a leer.
            self.conexion.close()
            #si lo que se conecto es el arduino, este deberia contestar con un handshake tambien

        except serial.SerialException as e:
            if "Access is denied" in str(e):
                self.cola.put(["ERROR","Acceso denegado al puerto seleccionado.\nProbablemente otro programa esta utilizandolo"])
            else:
                if "FileNotFoundError" in str(e):
                    self.cola.put(["ERROR","No se encotro ningun dispositivo de comunicacion serial o el seleccionado no es valido"])
                else:
                    self.cola.put(["ERROR","Error desconocido"])







    def cambiarLuz(self):
        if not self.luz:
            try:

                self.conexion.flush()
                self.conexion.write("2.100\n".encode())
                self.conexion.flush()
                print("Luz prendida")
                self.luz = True
            except serial.SerialException as error:
                print(error)
            except Exception as error:
                print(error)
        else:
            try:

                self.conexion.flush()
                self.conexion.write("2.0\n".encode())
                self.conexion.flush()
                self.luz = False
                print("luz apagada")
            except serial.SerialException as error:
                print(error)
            except Exception as error:
                print(error)
        print(self.luz)
    def setPuerto(self,data_puerto):
        self.puerto = str(data_puerto)



    def enviarSaludo(self):
        self.senial_conectado.emit()
        #self.senial_error.emit()
        return True
        #return False

    def getConectado(self):
        return self.conectado
    def conectar(self,puerto : str):
        if not self.hilo.is_alive() and not self.conectado and puerto != "":
            self.hilo = threading.Thread(target=self.run, daemon=True)
            self.puerto = puerto
            self.hilo.start()

    def enviar(self, nivel_derecho, nivel_izquierdo):
        #Simula enviar niveles 
        pass

