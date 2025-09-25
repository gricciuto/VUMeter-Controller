import threading
import time

import serial
import serial.tools.list_ports


def get_puertos():
    return serial.tools.list_ports.comports()


class ControladorSerial(threading.Thread):
    conexion = None
    baudios = None
    conectado = False
    puerto = None
    luz = False
    interfaz = None
    def __init__(self, baudios):
        super().__init__(daemon=True)
        self.baudios = baudios

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
    def setDatos(self, data_puerto, ventana):
        self.puerto = data_puerto
        self.interfaz = ventana
    def run(self,):
        self.mostrarMensaje(f"Intentando conexion en {self.puerto}")
        try:
            self.conexion = serial.Serial(port=self.puerto, baudrate=self.baudios, timeout=0.1)
            self.conexion.timeout = 1
            time.sleep(5)
            self.mostrarMensaje(f"Se accedio a un dispositivo en {self.puerto}, enviando paquete HandShake")
            self.conectado = self.enviarSaludo()

            #si lo que se conecto es el arduino, este deberia contestar con un handshake tambien

        except serial.SerialException as e:
            if "Access is denied" in str(e):
                self.mostrarMensaje("Acceso denegado al puerto seleccionado.\n Probablemente otro programa esta utilizandolo")
            else:
                if "FileNotFoundError" in str(e):
                    self.mostrarMensaje("No se encontro ningun dispositivo de comunicacion serial o el seleccionado no es valido")
                else:
                    self.mostrarMensaje("Error desconocido")

    def enviarSaludo(self):
        paquete = "5.hs\n".encode()
        self.conexion.write(paquete)
        self.conexion.flush()
        self.mostrarMensaje("Paquete enviado, esperando respuesta...")
        time.sleep(1) #Espera 1 segundo por la respuesta
        if self.conexion.in_waiting == 3: #Esto es para que, cuando se espero el tiempo necesario, si hay 3 bytes para leer, que se lean. Esto genera que no se bloquee esperando que lleguen mas bytes.
            datos = self.conexion.read(3) #Aca no va a tener que esperar nada porque ya tiene 3 bytes para leer, lo unico que le queda es saber si son el paquete o no.
            header, comando, checksum = datos
            if header == 0xAA and checksum == (header ^ comando):
                self.mostrarMensaje("Se obtuvo respuesta, conexion exitosa.")
                #Una vez que se logro la conexion hay que habilitar los botones de luz  e iniciar y desactivar el de conectar.
                self.interfaz.ui.pushButton_4.setEnabled(False)
                self.interfaz.ui.pushButton_2.setEnabled(True)
                self.interfaz.ui.pushButton_3.setEnabled(True)
                return True
            else:
                return False
        else:
            self.mostrarMensaje("No hubo respuesta del arduino, asegurese de cargar el programa en el mismo.")
            return False

    def mostrarMensaje(self, mensaje):
        self.interfaz.ui.textEdit.append(mensaje)
    def getConectado(self):
        return self.conectado

    def enviar(self, nivel_derecho, nivel_izquierdo):
        if self.getConectado():
            self.conexion.write(f"1.{nivel_izquierdo},{nivel_derecho}\n".encode())
        else:
            raise Exception("El modulo Controlador no esta conectado.")

