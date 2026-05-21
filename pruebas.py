import queue
import sys
import platform
from collections import deque

from PySide6.QtWidgets import QApplication

from core.AdministradorVolumenLinux import 
from core.Interfaz import Interfaz
from core.ListenerProgramas import ListenerProgramas
from core.EventCoordinator import EventCoordinator
from core.SerialArduinoFake import SerialArduinoFake

if __name__ == "__main__":
    bus = queue.Queue()

    app = QApplication(sys.argv)
    interfaz = Interfaz(bus)
    interfaz.inicializar()
    interfaz.mostrar()

    #serialArduino = SerialArduino(bus)
    serialArduinoFake = SerialArduinoFake(bus)

    controladorAudio = ControladorAudio(bus)
    listenerProgramas = None
    if (platform.system() == "Linux"):
        administradorVolumen = AdministradorVolumenLinux(bus)
        listenerProgramas = ListenerProgramasLinux(bus)
    elif (platform.system() == "Windows"):
        administradorVolumen = AdministradorVolumenWindows(bus)
        listenerProgramas = ListenerProgramasWindows(bus)
    else:
        print("Error, sistema operativo no soportado")
        print(platform.system())

    listenerProgramas.listen()

    coordinador = EventCoordinator(bus, administradorVolumen, controladorAudio, serialArduino, interfaz)
    coordinador.start()
    coordinador.senial.connect(interfaz.actualizar)
    interfaz.senial.connect(coordinador.actualizar)
    sys.exit(app.exec())

