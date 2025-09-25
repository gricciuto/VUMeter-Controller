import sys
import threading
from core.AdministradorVolumen import AdministradorVolumen
from core.ListenerProgramas import ListenerProgramas
import soundcard as sc
import numpy as np
import serial
import time

from numpy.f2py.auxfuncs import throw_error


from core.audio import ControladorAudio
from core.serial_arduino import ControladorSerial, get_puertos
from PyQt6.QtWidgets import QApplication
from core.Ventana import VentanaPrincipal
#Se necesita Python 3.10

BAUD_RATE = 9600

lock = threading.Lock()
c_audio = ControladorAudio()
c_arduino = ControladorSerial(BAUD_RATE) #Este seria el objeto que guarda la conexion que al final puede haber quedado como conectada
def hiloLogico():
    pass

def salir():
    sys.exit(app.exec())

def conectar_arduino():
    global c_arduino
    c_arduino = ControladorSerial(BAUD_RATE) #Esto es porque al ser un hilo, si quiero reintentar la conexion tengo que crear un objeto nuevo.
    puerto = window.ui.comboBox_2.currentText()

    c_arduino.setDatos(puerto,window) #Le paso la ventana para que pueda imprimir mensajes de estado en el panel de texto, y tambien para que si se logra la conexion habilite los botones
    c_arduino.start()
def iniciar_captura_audio():
    global c_audio
    c_audio = ControladorAudio(c_arduino.enviar, window) #Se le pasa al objeto del hilo del controlador de audio la funcion que tiene que llamar para que se le envie el paquete de audio al arduino.
    #Tambien le paso la ventana al controlador de audio para que pueda dibujar en las progress bar el audio del sistema.
    disp_captura = window.ui.comboBox.currentText()
    c_audio.setDispCaptura(disp_captura)
    c_audio.start()

def detener_captura_audio():
    global c_audio
    c_audio.stop()

def boton_iniciar_detener():
    if c_audio.is_alive():
        window.ui.pushButton_2.setText("Iniciar")
        detener_captura_audio()
    else:
        window.ui.pushButton_2.setText("Detener")
        iniciar_captura_audio()
def encender_apagar_luz():
    global c_arduino
    global lock
    with lock:
        try:
            c_arduino.cambiarLuz()
        except Exception as error:
            print(error)
def potenciometros():
    adm = AdministradorVolumen(window)
    listener = ListenerProgramas(adm.actualizarListaProgramas)
    adm.actualizarListaProgramas()
    listener.listener()
#parte de potenciometros


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = VentanaPrincipal()
    for item in c_audio.getMicrofonos():
        window.ui.comboBox.addItem(item.name)
    for item in get_puertos():
        window.ui.comboBox_2.addItem(item.name)
    potenciometros()
    #pushbutton2 es el de iniciar
    #pushbutton3 es el de la luz
    window.ui.pushButton.clicked.connect(salir)
    window.ui.pushButton_4.clicked.connect(conectar_arduino)
    window.ui.pushButton_3.clicked.connect(encender_apagar_luz)
    window.ui.pushButton_2.clicked.connect(boton_iniciar_detener)
    window.ui.textEdit.setEnabled(False)
    window.show()
    sys.exit(app.exec())