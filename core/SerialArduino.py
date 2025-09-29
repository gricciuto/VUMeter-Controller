import threading
import time
from queue import Queue

import serial
import serial.tools.list_ports


def get_puertos():
    return serial.tools.list_ports.comports()

#Modulo encargado de manejar la comunicacion con el arduino, se supone que solo debe recibir, decodificar la informacion y mandarla por el bus, ademas de recibir datos del modulo de logica y pasarlos al arduino tambien
class SerialArduino(threading.Thread):
    conexion = None
    baudios = None
    conectado = False
    puerto = None
    luz = False

    def __init__(self,cola: Queue, baudios = 9600):
        super().__init__(daemon=True)
        self.baudios = baudios
        self.cola = cola
    def enviarPaquete(self,paquete):
        try:
            self.conexion.flush()
            self.conexion.write(paquete.encode())
        except serial.SerialException as e:
            self.cola.put(["ERROR","No hay arduino conectado para enviar el paquete"])
        except Exception as e:
            self.cola.put(["ERROR",str(e)])

    def run(self):
        self.cola.put(["INFO",f"Intentando conexion en {self.puerto}"])
        print("corriendo")
        try:
            self.conexion = serial.Serial(port=self.puerto, baudrate=self.baudios, timeout=None)
            time.sleep(2)
            self.cola.put(["INFO",f"Se accedio a un dispositivo en {self.puerto}, enviando paquete HandShake"])
            self.conectado = self.enviarSaludo()
            while True:

                datos = self.conexion.read(3)
                header, comando, checksum = datos
                if header == 0xA1 and checksum == header ^ comando:
                    self.cola.put(["POT1",comando])
                if header == 0xA2 and checksum == header ^ comando:
                    self.cola.put(["POT2",comando])
                if header == 0xA3 and checksum == header ^ comando:
                    self.cola.put(["POT3",comando])
                if header == 0xA4 and checksum == header ^ comando:
                    self.cola.put(["POT4",comando])
                if header == 0xA5 and checksum == header ^ comando:
                    self.cola.put(["POT5",comando])
                if header == 0xA6 and checksum == header ^ comando:
                    self.cola.put(["POT6",comando])
                #Aca es donde si hay paquetes para leer (de que se movio un potenciometro) se va a leer.

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
    def setPuerto(self, data_puerto):
        self.puerto = data_puerto



    def enviarSaludo(self):
        paquete = "5.hs\n".encode()
        self.conexion.write(paquete)
        self.conexion.flush()
        self.cola.put(["INFO","Paquete enviado, esperando respuesta..."])
        time.sleep(1) #Espera 1 segundo por la respuesta
        if self.conexion.in_waiting == 3: #Esto es para que, cuando se espero el tiempo necesario, si hay 3 bytes para leer, que se lean. Esto genera que no se bloquee esperando que lleguen mas bytes.
            datos = self.conexion.read(3) #Aca no va a tener que esperar nada porque ya tiene 3 bytes para leer, lo unico que le queda es saber si son el paquete o no.
            header, comando, checksum = datos
            if header == 0xAA and checksum == (header ^ comando):
                #Una vez que se logro la conexion hay que habilitar los botones de luz  e iniciar y desactivar el de conectar.
                self.cola.put(["ARDUINO_CONECTADO","Se obtuvo respuesta, conexion exitosa"])
                return True
            else:
                return False
        else:
            self.cola.put(["ERROR","Error, no hubo respuesta del arduino, recorda que tiene que tener el programa cargado"])
            return False


    def getConectado(self):
        return self.conectado

    def enviar(self, nivel_derecho, nivel_izquierdo):
        if self.getConectado():
            self.conexion.write(f"1.{nivel_izquierdo},{nivel_derecho}\n".encode())
        else:
            raise Exception("El modulo Controlador no esta conectado.")

