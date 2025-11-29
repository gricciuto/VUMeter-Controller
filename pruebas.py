import queue
import sys
from collections import deque

from PySide6.QtWidgets import QApplication

from core.AdministradorVolumen import AdministradorVolumen
from core.ControladorAudio import ControladorAudio
from core.Interfaz import Interfaz
from core.ListenerProgramas import ListenerProgramas
from core.Logica import Logica
from core.SerialArduino import SerialArduino

if __name__ == "__main__":
    bus = queue.Queue()

    app = QApplication(sys.argv)
    interfaz = Interfaz()
    interfaz.inicializar()
    interfaz.mostrar()

    serialArduino = SerialArduino(bus)

    controladorAudio = ControladorAudio(bus)

    administradorVolumen = AdministradorVolumen(bus)

    listener = ListenerProgramas(bus)
    listener.listen()

    logica = Logica(bus, administradorVolumen, controladorAudio, serialArduino)
    logica.start()
    logica.senial.connect(interfaz.actualizar)
    interfaz.senial.connect(logica.actualizar)
    sys.exit(app.exec())

