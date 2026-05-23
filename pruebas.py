import queue
import sys
from collections import deque

from PySide6.QtWidgets import QApplication

from core.AdministradorVolumen import AdministradorVolumen
from core.ControladorAudio import ControladorAudio
from core.Interfaz import Interfaz
from core.ListenerProgramas import ListenerProgramas
from core.EventCoordinator import EventCoordinator
from core.SerialArduino import SerialArduino
from core.SerialArduinoFake import SerialArduinoFake

if __name__ == "__main__":
    bus = queue.Queue()

    app = QApplication(sys.argv)
    interfaz = Interfaz(bus)
    interfaz.inicializar()
    interfaz.mostrar()

    serialArduino = SerialArduino(bus)

    controladorAudio = ControladorAudio(bus)

    administradorVolumen = AdministradorVolumen(bus)

    listener = ListenerProgramas()
    listener.listen()

    coordinador = EventCoordinator(bus, administradorVolumen, controladorAudio, serialArduino, interfaz, listener)
    coordinador.start()
    coordinador.senial.connect(interfaz.actualizar)
    interfaz.senial.connect(coordinador.actualizar)
    sys.exit(app.exec())

